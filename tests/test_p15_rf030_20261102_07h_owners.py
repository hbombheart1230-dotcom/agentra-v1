"""RF-030 A31-1..8: eight ``operator_period_summary`` helpers, original vs thin wrappers + Owners.

Originals: A preimage a3dd561b blob cf13bb0b (canonical fa317c98 has the same blob). AST-extracted and compiled in a
copy of the live namespace; dependency overrides apply to both sides. Pure/fake only; no IO, sockets or writes.
"""
from __future__ import annotations

import ast
import builtins
import copy
import datetime as _dt
import hashlib
import importlib
import inspect
import socket
import subprocess
from pathlib import Path

import pytest

A_PRE = "a3dd561b308f3d6c9a08145f189476e5e2810cd5"
CANON = "fa317c98fc1e7828e97b751a3a4f28bfd655d869"
PATH = "libs/reporting/operator_period_summary.py"
BLOB = "cf13bb0bb9135fea3139bce3abd1936c14090473"
NAMES = ["_safe_int", "_iso_to_kst_text", "_has_partial_lifecycle_marker", "_is_realized_nonclosed_exit",
         "_render_quant_shadow_candidate_lines", "_render_strategist_llm_evaluation_lines", "_first_reason_bucket", "_trade_status"]
ops = importlib.import_module("libs.reporting.operator_period_summary")
OWNERS = {n: importlib.import_module(f"libs.reporting.operator_period_summary_{n.lstrip('_')}") for n in NAMES}
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
    for attr in ("read_text", "write_text", "write_bytes", "mkdir", "touch", "unlink", "rename", "replace"):
        monkeypatch.setattr(Path, attr, boom)
    real_open = builtins.open

    def guarded_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+"):
            raise AssertionError("write open attempted")
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)


def check(orig_nodes, monkeypatch, name, *args, overrides=None, **kwargs):
    ns = dict(vars(ops))
    tree = ast.Module(body=[copy.deepcopy(orig_nodes[name])], type_ignores=[])
    exec(compile(ast.fix_missing_locations(tree), f"<{A_PRE[:8]}:{name}>", "exec"), ns)
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(ops, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[name]), ("new", getattr(ops, name))):
        a, k = copy.deepcopy((args, kwargs))
        try:
            values[label] = fn(*a, **k)
            got[label] = ("ok", repr(values[label]))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert repr((a, k)) == repr((args, kwargs)), f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


# A31-1 _safe_int
@pytest.mark.parametrize("value", [0, 1, -2, 2.9, -2.9, "7", "7.9", " 8 ", None, "", "abc", NAN, INF, -INF, [1], True, "1e3", 10**20])
@pytest.mark.parametrize("default", [0, 5, -1.5, "x", None])
def test_safe_int(orig_nodes, monkeypatch, guards, value, default):
    check(orig_nodes, monkeypatch, "_safe_int", value, default)


def test_safe_int_default_and_fallback(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_safe_int", "3.7") == 3
    assert check(orig_nodes, monkeypatch, "_safe_int", "bad") == 0
    assert check(orig_nodes, monkeypatch, "_safe_int", "bad", 4.8) == 4
    assert check(orig_nodes, monkeypatch, "_safe_int", NAN) == 0  # int(float(nan)) raises -> default
    out = check(orig_nodes, monkeypatch, "_safe_int", None, "oops")  # int(default) raises ValueError on both sides
    assert out[0] == "err" and out[1] == "ValueError"


# A31-2 _iso_to_kst_text
def _fake_dt(value):
    return value if isinstance(value, _dt.datetime) else None


@pytest.mark.parametrize("value", [None, "", "bad", "2026-04-16T09:30:00+09:00", "2026-04-16T00:30:00Z", "2026-04-16T09:30:00", "2026-04-16 09:30:00", 5, []])
def test_iso_to_kst_text_real_helper(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_iso_to_kst_text", value)


@pytest.mark.parametrize("value", [None, _dt.datetime(2026, 4, 16, 9, 30, 5), _dt.datetime(2026, 4, 16, 9, 30, 5, tzinfo=_dt.timezone.utc), "str"])
def test_iso_to_kst_text_fake_helper(orig_nodes, monkeypatch, guards, value):
    out = check(orig_nodes, monkeypatch, "_iso_to_kst_text", value, overrides={"_iso_to_kst_dt": _fake_dt})
    assert out == ("" if not isinstance(value, _dt.datetime) else value.strftime("%Y-%m-%d %H:%M:%S KST"))


# A31-3 _has_partial_lifecycle_marker  / A31-8 _trade_status
ROWS = [{}, {"status": "partial"}, {"last_status": "PARTIAL"}, {"status": "closed", "last_status": "Partial"}, {"last_status": "", "status": " Partial "},
        {"trade_origin": "recovered_partial"}, {"trade_origin": " RECOVERED_PARTIAL "}, {"trade_origin": "other", "status": "open"},
        {"status": None, "last_status": None}, {"status": 5}, {"last_status": ["x"]}, {"status": "한글"}, {"last_status": 0, "status": "Closed"}]


@pytest.mark.parametrize("row", ROWS)
def test_has_partial_lifecycle_marker(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_has_partial_lifecycle_marker", row)


def test_has_partial_trade_status_seam(orig_nodes, monkeypatch, guards):
    seen = []
    out = check(orig_nodes, monkeypatch, "_has_partial_lifecycle_marker", {"x": 1},
                overrides={"_trade_status": lambda r: seen.append(dict(r)) or "partial"})
    assert out is True and seen == [{"x": 1}, {"x": 1}]


@pytest.mark.parametrize("row", ROWS)
def test_trade_status(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_trade_status", row)


def test_trade_status_precedence(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_trade_status", {"last_status": "Open", "status": "closed"}) == "open"
    assert check(orig_nodes, monkeypatch, "_trade_status", {"last_status": "", "status": " CLOSED "}) == "closed"
    assert check(orig_nodes, monkeypatch, "_trade_status", {}) == ""


# A31-4 _is_realized_nonclosed_exit
@pytest.mark.parametrize("row", [
    {}, {"broker_reconciliation_status": "skipped_unresolved", "action": "SELL"}, {"action": "SELL", "status": "partial"},
    {"action": "BUY", "status": "partial"}, {"action": "SELL", "status": "closed"}, {"action": "SELL", "trade_origin": "recovered_partial"},
    {"last_action": "sell", "last_status": "partial"}, {"action": "SELL", "status": "open"}, {"broker_reconciliation_status": None, "action": "SELL", "status": "partial"},
])
def test_is_realized_nonclosed_exit_real_helpers(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_is_realized_nonclosed_exit", row)


@pytest.mark.parametrize("closed,action,partial", [(True, "SELL", True), (False, "BUY", True), (False, "SELL", True), (False, "SELL", False)])
def test_is_realized_nonclosed_exit_fake_helpers(orig_nodes, monkeypatch, guards, closed, action, partial):
    calls = []
    out = check(orig_nodes, monkeypatch, "_is_realized_nonclosed_exit", {"id": 1},
                overrides={"_is_closed_trade": lambda r: calls.append("closed") or closed,
                           "_trade_action": lambda r: calls.append("action") or action,
                           "_is_recovered_partial_marker": lambda r: calls.append("partial") or partial})
    assert out is (not closed and action == "SELL" and partial)
    assert calls[: len(calls) // 2] == calls[len(calls) // 2:]  # identical call order on both sides


# A31-5 / A31-6 render lines
RENDER_PAYLOADS = [{}, {"k": None}, {"k": "str"}, {"k": []}, {"k": {}}, {"k": {"a": 1}}, {"k": {"rows": [1, 2]}}]


@pytest.mark.parametrize("payload", RENDER_PAYLOADS)
def test_render_quant_shadow_candidate_lines(orig_nodes, monkeypatch, guards, payload):
    payload = {"quant_shadow_candidate_evaluation": payload.get("k")} if "k" in payload else {}
    seen = []
    out = check(orig_nodes, monkeypatch, "_render_quant_shadow_candidate_lines", payload,
                overrides={"render_quant_shadow_candidate_evaluation_lines": lambda e: seen.append(dict(e)) or ["l1", "한글"]})
    if isinstance(payload.get("quant_shadow_candidate_evaluation"), dict):
        assert out == ["l1", "한글"] and len(seen) == 2
    else:
        assert out == [] and seen == []


@pytest.mark.parametrize("payload", RENDER_PAYLOADS)
def test_render_strategist_llm_evaluation_lines(orig_nodes, monkeypatch, guards, payload):
    payload = {"strategist_llm_evaluation": payload.get("k")} if "k" in payload else {}
    seen = []
    out = check(orig_nodes, monkeypatch, "_render_strategist_llm_evaluation_lines", payload,
                overrides={"render_strategist_llm_evaluation_lines": lambda e: seen.append(dict(e)) or ["s1"]})
    if isinstance(payload.get("strategist_llm_evaluation"), dict):
        assert out == ["s1"] and len(seen) == 2
    else:
        assert out == [] and seen == []


def test_render_lines_real_renderers_empty_evaluation(orig_nodes, monkeypatch, guards):
    check(orig_nodes, monkeypatch, "_render_quant_shadow_candidate_lines", {"quant_shadow_candidate_evaluation": {}})
    check(orig_nodes, monkeypatch, "_render_strategist_llm_evaluation_lines", {"strategist_llm_evaluation": {}})


# A31-7 _first_reason_bucket
@pytest.mark.parametrize("values", [None, [], "abc", ["", None], ["a", "b"], [" a ", "b"], ["", " x "], ["한글", "z"], [0, False, 1], {"a": 1}, 5])
def test_first_reason_bucket(orig_nodes, monkeypatch, guards, values):
    check(orig_nodes, monkeypatch, "_first_reason_bucket", values)


def test_first_reason_bucket_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_first_reason_bucket", ["x"], overrides={"_first_nonempty_list": lambda v: ["patched", "p2"]}) == "patched"
    assert check(orig_nodes, monkeypatch, "_first_reason_bucket", ["x"], overrides={"_first_nonempty_list": lambda v: []}) == ""


# structure
@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(ops, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = wrapper.body[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name]).replace("operator_period_summary_", "")
    assert "operator_period_summary import" not in src and "import operator_period_summary" not in src
