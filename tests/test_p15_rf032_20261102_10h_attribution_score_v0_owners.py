"""RF-032 A34-1..8: eight ``attribution_score_v0`` helpers, original vs thin wrappers + Owners.

Pure in-memory evaluation scope; no UEF/validation-id writer is touched. Original: A preimage 2ae46be0 blob a7a47252
(canonical c93efc73 has the same blob). AST-extracted and compiled in a copy of the live namespace; dependency
overrides apply to both sides. No IO, sockets or writes.
"""
from __future__ import annotations

import ast
import builtins
import copy
import hashlib
import importlib
import inspect
import socket
import subprocess
from collections import OrderedDict
from pathlib import Path

import pytest

A_PRE = "2ae46be02864031bf2aa9bb3fa63fc35c6a6ef95"
CANON = "c93efc73fd7ee4715efc3a67a430f6eb2f00b8d0"
PATH = "libs/reporting/evaluation/attribution_score_v0.py"
BLOB = "a7a47252a2b7dbc82a20a1b89831fd71540533a6"
NAMES = ["_as_rows", "_num", "_clamp_score", "_score", "_selection_integrity", "_scanner_alignment", "_entry_timing", "_exit_horizon"]
mod = importlib.import_module("libs.reporting.evaluation.attribution_score_v0")
OWNERS = {n: importlib.import_module(f"libs.reporting.evaluation.attribution_score_v0_{n.lstrip('_')}") for n in NAMES}
NAN, INF = float("nan"), float("inf")


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    try:
        a_raw = subprocess.run(["git", "show", f"{A_PRE}:{PATH}"], check=True, capture_output=True).stdout
        c_raw = subprocess.run(["git", "show", f"{CANON}:{PATH}"], check=True, capture_output=True).stdout
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(a_raw) == BLOB, "BLOCKED_PIN actor blob"
    assert _sha(c_raw) == BLOB, "BLOCKED_PIN canonical blob"
    tree = ast.parse(a_raw.decode("utf-8"))
    nodes = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in NAMES}
    assert sorted(nodes) == sorted(NAMES)
    return nodes


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    for attr in ("read_text", "read_bytes", "write_text", "write_bytes", "mkdir", "touch", "unlink", "rename", "replace"):
        monkeypatch.setattr(Path, attr, boom)
    real_open = builtins.open

    def guarded_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+"):
            raise AssertionError("write open attempted")
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)


def check(orig_nodes, monkeypatch, name, *args, overrides=None, **kwargs):
    ns = dict(vars(mod))
    tree = ast.Module(body=[copy.deepcopy(orig_nodes[name])], type_ignores=[])
    exec(compile(ast.fix_missing_locations(tree), f"<{A_PRE[:8]}:{name}>", "exec"), ns)
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(mod, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[name]), ("new", getattr(mod, name))):
        a, k = copy.deepcopy((args, kwargs))
        try:
            values[label] = fn(*a, **k)
            got[label] = ("ok", repr(values[label]))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert repr((a, k)) == repr((args, kwargs)), f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


# A34-1 _as_rows
@pytest.mark.parametrize("value", [None, [], (), [{"a": 1}], [{"a": 1}, 3, None, "x", {"b": 2}], [OrderedDict([("z", 1)])], "str", 5, [[1]], {"k": 1}])
def test_as_rows(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_as_rows", value)


def test_as_rows_identity_order_and_generator(guards):
    a, b = {"a": 1}, {"b": 2}
    out = mod._as_rows([a, 3, b])
    assert out[0] is a and out[1] is b and len(out) == 2
    assert mod._as_rows((r for r in [a, None, b])) == [a, b]
    assert mod._as_rows(None) == []


# A34-2 _num
@pytest.mark.parametrize("value", [None, "", 0, 1, -2.5, "3.5", " 4 ", "abc", NAN, INF, "-inf", [1], {}, True, b"1", (1,)])
def test_num(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_num", value)


# A34-3 _clamp_score
@pytest.mark.parametrize("value", [-1000.0, -0.4, 0.0, 0.4, 0.5, 1.5, 2.5, 49.5, 99.5, 100.0, 100.5, 1e9, NAN, INF, -INF])
def test_clamp_score(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_clamp_score", value)


def test_clamp_score_values(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_clamp_score", 250.0) == 100
    assert check(orig_nodes, monkeypatch, "_clamp_score", -3.0) == 0
    assert check(orig_nodes, monkeypatch, "_clamp_score", 2.5) == 2  # banker's rounding preserved


# A34-4 _score
@pytest.mark.parametrize("status,value,reasons,evidence", [
    ("OK", 80, ["r1", "r2"], None), ("OK", 0, [], {}), ("INSUFFICIENT_EVIDENCE", 50, ["x"], {"a": 1}), ("INSUFFICIENT_EVIDENCE", None, [], None),
    ("OK", None, ["z"], {"n": {"deep": 1}}), ("weird", 1, ["한글"], OrderedDict([("b", 1), ("a", 2)])), ("OK", 5, ["r"], "notamapping"), ("OK", 5, ["r"], []),
])
def test_score(orig_nodes, monkeypatch, guards, status, value, reasons, evidence):
    check(orig_nodes, monkeypatch, "_score", status, value, reasons, evidence)


def test_score_shape_and_shallow_copy(orig_nodes, monkeypatch, guards):
    nested = {"deep": 1}
    out = mod._score("OK", 7, ["r"], {"a": nested})
    assert list(out) == ["status", "score", "reasons", "evidence"] and out["evidence"]["a"] is nested
    reasons = ["r"]
    assert mod._score("OK", 7, reasons)["reasons"] is reasons  # reasons list passed through, not copied
    assert check(orig_nodes, monkeypatch, "_score", "INSUFFICIENT_EVIDENCE", 9, ["x"], {"e": 1},
                 overrides={"INSUFFICIENT": "FAKE_INSUFF"})["score"] == 9  # constant read from the facade at call time


# A34-5 _selection_integrity
def _row(tid, **kw):
    r = {"trade_id": tid}
    r.update(kw)
    return r


SEL = [
    {}, {"rows": []}, {"rows": None}, {"rows": "bad"}, {"rows": [_row("T1")]},
    {"rows": [_row("T1", final_to_executed_changed=True)]}, {"rows": [_row("T1", monitor_to_commander_changed=True)]},
    {"rows": [_row("T1", post_to_selected_changed=True)]}, {"rows": [_row("T1", selection_mismatch={"a": 1})]},
    {"rows": [_row("T1", selection_mismatch={"a": 1}, post_to_selected_changed=True)]},
    {"rows": [_row("T1", final_to_executed_changed=True, monitor_to_commander_changed=True, post_to_selected_changed=True, selection_mismatch={"x": 1}),
              _row("T2"), "bad", None]},
    {"rows": [_row("T1", final_to_executed_changed=1), _row("T2", final_to_executed_changed="yes")]},
]


@pytest.mark.parametrize("sel", SEL)
def test_selection_integrity(orig_nodes, monkeypatch, guards, sel):
    check(orig_nodes, monkeypatch, "_selection_integrity", sel)


def test_selection_integrity_values_and_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_selection_integrity",
                {"rows": [_row("T1", final_to_executed_changed=True, monitor_to_commander_changed=True), _row("T2")]})
    assert out["status"] == "OK" and out["score"] == 65 and out["evidence"] == {"trade_count": 2}
    assert out["reasons"] == ["T1:final_to_executed_changed", "T1:monitor_to_commander_changed"]
    out = check(orig_nodes, monkeypatch, "_selection_integrity", {"rows": [_row("T1")]},
                overrides={"_clamp_score": lambda v: 11, "OK": "FAKE_OK"})
    assert out["score"] == 11 and out["status"] == "FAKE_OK" and out["reasons"] == ["selection_chain_consistent"]


# A34-6 _scanner_alignment
def _model(tid, rank=None, cand_rank=None):
    return {"trade_id": tid, "selection": {"selected_rank": rank, "selected_candidate": {"rank": cand_rank}}}


ALIGN = [
    ({}, []), ({"rows": []}, []), ({"rows": [_row("T1", selected_symbol="A", raw_scanner_top1="A", post_strategy_top1="A")]}, []),
    ({"rows": [_row("T1", selected_symbol="A", raw_scanner_top1="B", post_strategy_top1="C")]}, []),
    ({"rows": [_row("T1", selected_symbol="A", raw_scanner_top1="A")]}, [_model("T1", rank=3)]),
    ({"rows": [_row("T1", selected_symbol="A")]}, [_model("T1", rank=None, cand_rank=2)]),
    ({"rows": [_row("T1", selected_symbol="A")]}, [_model("T1", rank=1)]),
    ({"rows": [_row("T1", selected_symbol="A")]}, [_model("T1", rank=9)]),
    ({"rows": [_row("T1", selected_symbol="A", raw_to_post_changed=True)]}, []),
    ({"rows": [_row("T1", selected_symbol="A", raw_scanner_top1="B", post_strategy_top1="C", raw_to_post_changed=True), _row("T2", selected_symbol="X"), "bad"]},
     [_model("T1", rank="3"), _model("T2", rank="bad")]),
    ({"rows": [_row("T1")]}, ["not-a-mapping-model"]),
]


@pytest.mark.parametrize("sel,models", ALIGN)
def test_scanner_alignment(orig_nodes, monkeypatch, guards, sel, models):
    check(orig_nodes, monkeypatch, "_scanner_alignment", sel, models)


def test_scanner_alignment_values_and_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_scanner_alignment",
                {"rows": [_row("T1", selected_symbol="A", raw_scanner_top1="B", post_strategy_top1="C", raw_to_post_changed=True)]}, [_model("T1", rank=3)])
    assert out["reasons"] == ["T1:selected_not_raw_top1", "T1:selected_not_post_strategy_top1", "T1:selected_rank_3", "T1:raw_to_post_changed"]
    assert out["score"] == 25 and out["evidence"] == {"trade_count": 1}  # penalty 20+20+30+5 = 75
    out = check(orig_nodes, monkeypatch, "_scanner_alignment", {"rows": [_row("T1", selected_symbol="A")]}, [_model("T1", rank=1)],
                overrides={"_num": lambda v: 4.0})
    assert out["reasons"] == ["T1:selected_rank_4"]


# A34-7 _entry_timing
ENTRY = [{}, {"rows": []}, {"rows": None}, {"rows": [{"label": "INSUFFICIENT_EVIDENCE"}]},
         {"rows": [_row("T1", label="ENTRY_APPROPRIATE")]}, {"rows": [_row("T1", label="ENTRY_TOO_EARLY"), _row("T2", label="ENTRY_TOO_LATE")]},
         {"rows": [_row("T1", label="UNKNOWN_LABEL"), _row("T2", label="ENTRY_APPROPRIATE"), _row("T3", label="INSUFFICIENT_EVIDENCE"), "bad"]},
         {"rows": [_row("T1")]}]


@pytest.mark.parametrize("report", ENTRY)
def test_entry_timing(orig_nodes, monkeypatch, guards, report):
    check(orig_nodes, monkeypatch, "_entry_timing", report)


def test_entry_timing_values_and_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_entry_timing", ENTRY[6])
    assert out["score"] == 75 and out["evidence"] == {"classified_trade_count": 2, "total_trade_count": 3}  # (50+100)/2
    out = check(orig_nodes, monkeypatch, "_entry_timing", ENTRY[3], overrides={"INSUFFICIENT": "NOPE"})
    assert out["status"] == "OK"  # facade constant read at call time: nothing equals the fake marker


# A34-8 _exit_horizon
HOR = [{}, {"rows": []}, {"rows": None}, {"rows": [_row("T1")]}, {"rows": [_row("T1", horizon_violation_candidate=True)]},
       {"rows": [_row("T1", exited_before_min_hold=True)]}, {"rows": [_row("T1", exited_before_target_hold=1)]},
       {"rows": [_row("T1", target_hold_would_improve_exit="yes")]},
       {"rows": [_row("T1", horizon_violation_candidate=True, exited_before_min_hold=True, exited_before_target_hold=True, target_hold_would_improve_exit=True)]},
       {"rows": [_row("T1", horizon_violation_candidate=True), _row("T2"), "bad", None]}]


@pytest.mark.parametrize("report", HOR)
def test_exit_horizon(orig_nodes, monkeypatch, guards, report):
    check(orig_nodes, monkeypatch, "_exit_horizon", report)


def test_exit_horizon_values_and_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_exit_horizon", HOR[8])
    assert out["score"] == 20 and out["reasons"] == ["T1:horizon_violation_candidate", "T1:before_min_hold", "T1:before_target_hold", "T1:target_hold_would_improve"]
    out = check(orig_nodes, monkeypatch, "_exit_horizon", HOR[3], overrides={"_as_rows": lambda v: [{"trade_id": "P", "horizon_violation_candidate": 1}]})
    assert out["reasons"] == ["P:horizon_violation_candidate"] and out["score"] == 80


# structure
@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = wrapper.body[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name]).replace("attribution_score_v0_", "")
    assert "attribution_score_v0 import" not in src and "import attribution_score_v0" not in src
