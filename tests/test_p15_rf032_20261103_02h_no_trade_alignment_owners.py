"""RF-032 A49-1..8: eight ``no_trade_attribution`` / ``scanner_alignment_root_cause`` helper bodies, original vs thin wrappers + Owners.

Original = A preimage 87548b34 (SOURCE blobs 967aca16 / 8774bea2 == canonical 08ecb864). Each original function is compiled from
``git show`` into a copy of the live module namespace and compared with the final wrapper + Owner (output repr,
exception type/message, input immutability). Fake objects only: attach/dedupe/performance helpers are faked, no real
file reads/writes, sockets, subprocess or UEF/validation-id writer.
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
from pathlib import Path

import pytest

A_PRE = "87548b34d58308bc3686842bdd42ec0d10f767e7"
CANON = "08ecb864acce08d92aad03b31be82a1b968f3425"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "nt_mapping": ("no_trade_attribution", "967aca16db2926cc00b0a7761d1534cf4b84540b", "no_trade_attribution_mapping", "_mapping"),
    "nt_num": ("no_trade_attribution", "967aca16db2926cc00b0a7761d1534cf4b84540b", "no_trade_attribution_num", "_num"),
    "nt_pct": ("no_trade_attribution", "967aca16db2926cc00b0a7761d1534cf4b84540b", "no_trade_attribution_pct", "_pct"),
    "nt_top": ("no_trade_attribution", "967aca16db2926cc00b0a7761d1534cf4b84540b", "no_trade_attribution_top", "_top"),
    "nt_q9_window_view": ("no_trade_attribution", "967aca16db2926cc00b0a7761d1534cf4b84540b", "no_trade_attribution_q9_window_view", "_q9_window_view"),
    "sar_mapping": ("scanner_alignment_root_cause", "8774bea29dd8ebd83283b28c5109e5fc6210fd1a", "scanner_alignment_root_cause_mapping", "_mapping"),
    "sar_rows": ("scanner_alignment_root_cause", "8774bea29dd8ebd83283b28c5109e5fc6210fd1a", "scanner_alignment_root_cause_rows", "_rows"),
    "sar_num": ("scanner_alignment_root_cause", "8774bea29dd8ebd83283b28c5109e5fc6210fd1a", "scanner_alignment_root_cause_num", "_num"),
}
MODS = {s: importlib.import_module(f"libs.reporting.evaluation.{s}") for s in {v[0] for v in SPEC.values()}}
OWNERS = {n: importlib.import_module(f"libs.reporting.evaluation.{v[2]}") for n, v in SPEC.items()}
NAN = float("nan")


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    out = {}
    for stem, blob in {(v[0], v[1]) for v in SPEC.values()}:
        raws = {}
        for label, rev in (("A", A_PRE), ("canonical", CANON)):
            try:
                raws[label] = subprocess.run(["git", "show", f"{rev}:{EV}{stem}.py"], check=True, capture_output=True).stdout
            except subprocess.CalledProcessError as exc:
                pytest.fail(f"BLOCKED_PIN {stem} {label}: {exc.stderr!r}")
            assert _sha(raws[label]) == blob, f"BLOCKED_PIN {stem} {label} blob"
        tree = ast.parse(raws["A"].decode("utf-8"))
        for n, v in SPEC.items():
            if v[0] == stem:
                out[n] = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == v[3]][-1]
    assert sorted(out) == sorted(SPEC)
    return out


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("real filesystem/effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    for attr in ("read_text", "read_bytes", "write_text", "write_bytes", "mkdir", "touch", "unlink", "rename", "replace",
                 "exists", "is_dir", "is_file", "rglob", "glob", "iterdir"):
        monkeypatch.setattr(Path, attr, boom)
    real_open = builtins.open

    def guarded_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+") or str(file).replace("\\", "/").startswith(("/rep", "/fake")):
            raise AssertionError("open attempted")
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)


def check(orig_nodes, monkeypatch, name, *args, overrides=None, **kwargs):
    mod = MODS[SPEC[name][0]]
    ns = dict(vars(mod))
    tree = ast.Module(body=[copy.deepcopy(orig_nodes[name])], type_ignores=[])
    exec(compile(ast.fix_missing_locations(tree), f"<{A_PRE[:8]}:{name}>", "exec"), ns)
    fname = SPEC[name][3]
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(mod, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[fname]), ("new", getattr(mod, fname))):
        a, k = copy.deepcopy((args, kwargs))
        try:
            values[label] = fn(*a, **k)
            got[label] = ("ok", repr(values[label]))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert repr((a, k)) == repr((args, kwargs)), f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


import collections

NT = MODS["no_trade_attribution"]
SAR = MODS["scanner_alignment_root_cause"]


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


class _Num:
    def __repr__(self):
        return "_Num()"

    def __float__(self):
        return 2.5


class _FloatErr:
    def __init__(self, exc):
        self.exc = exc

    def __repr__(self):
        return f"_FloatErr({self.exc.__name__})"

    def __float__(self):
        raise self.exc("custom float failure")


class _Cnt(collections.Counter):
    def __repr__(self):
        return f"_Cnt({dict(self)!r})"


VALS = [None, "", 0, 0.0, "0", " 1.5 ", "abc", "1e3", "nan", "inf", NAN, True, [], {}, b"2", _Num(), _FloatErr(TypeError), _FloatErr(ValueError), (), "-0", -3]
MAPPINGS = [None, {}, {"a": 1}, _MapSub(a=1), [], [("a", 1)], "s", 5, {"n": {"deep": [1]}}]


def _scalar_checks(orig_nodes, monkeypatch, key):
    assert check(orig_nodes, monkeypatch, key, None) is None and check(orig_nodes, monkeypatch, key, "") is None and check(orig_nodes, monkeypatch, key, 0) == 0.0
    assert check(orig_nodes, monkeypatch, key, _FloatErr(TypeError)) is None and check(orig_nodes, monkeypatch, key, _FloatErr(ValueError)) is None
    assert check(orig_nodes, monkeypatch, key, _FloatErr(RuntimeError)) == ("err", "RuntimeError", "custom float failure")  # only TypeError/ValueError caught
    out = check(orig_nodes, monkeypatch, key, "nan")
    assert out != out


def _mapping_checks(orig_nodes, monkeypatch, key, mod):
    src = {"a": 1}
    assert mod._mapping(src) is src and mod._mapping(None) == {} and mod._mapping(None) is not mod._mapping(None)

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, key, {"a": 1}, overrides={"Mapping": NeverMapping}) == {}


# ---- A49-1 no_trade_attribution._mapping ----
@pytest.mark.parametrize("value", MAPPINGS)
def test_nt_mapping(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "nt_mapping", value)


def test_nt_mapping_identity_and_seam(orig_nodes, monkeypatch, guards):
    _mapping_checks(orig_nodes, monkeypatch, "nt_mapping", NT)


# ---- A49-2 _num ----
@pytest.mark.parametrize("value", VALS)
def test_nt_num(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "nt_num", value)


def test_nt_num_exact(orig_nodes, monkeypatch, guards):
    _scalar_checks(orig_nodes, monkeypatch, "nt_num")


# ---- A49-3 _pct ----
@pytest.mark.parametrize("value", VALS + [1.23456, "2.5", -0.00004, 100])
def test_nt_pct(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "nt_pct", value)


def test_nt_pct_exact_and_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "nt_pct", None) == "-" and check(orig_nodes, monkeypatch, "nt_pct", "") == "-" and check(orig_nodes, monkeypatch, "nt_pct", "x") == "-"
    assert check(orig_nodes, monkeypatch, "nt_pct", 1.23456) == "1.2346%" and check(orig_nodes, monkeypatch, "nt_pct", 0) == "0.0000%" and check(orig_nodes, monkeypatch, "nt_pct", -0.00004) == "-0.0000%"
    assert check(orig_nodes, monkeypatch, "nt_pct", NAN) == "nan%" and check(orig_nodes, monkeypatch, "nt_pct", _FloatErr(RuntimeError)) == ("err", "RuntimeError", "custom float failure")
    seen = []
    out = check(orig_nodes, monkeypatch, "nt_pct", "raw", overrides={"_num": lambda v: seen.append(v) or 9.0})
    assert out == "9.0000%" and seen == ["raw", "raw"]
    assert check(orig_nodes, monkeypatch, "nt_pct", "raw", overrides={"_num": lambda v: None}) == "-"


# ---- A49-4 _top ----
CNTS = [collections.Counter(), collections.Counter("aabbbc"), collections.Counter({"x": 3, "y": 3, "z": 1}), collections.Counter({"": 5, "k": 1}), collections.Counter({"a": 0, "b": 2}),
        collections.Counter({str(i): 20 - i for i in range(15)}), _Cnt({"q": 2.7, "r": 1}), collections.Counter({"한글": 2})]


@pytest.mark.parametrize("counter", CNTS)
@pytest.mark.parametrize("limit", [None, 0, 1, 2, 10, 100, -1])
def test_nt_top(orig_nodes, monkeypatch, guards, counter, limit):
    if limit is None:
        check(orig_nodes, monkeypatch, "nt_top", counter)
    else:
        check(orig_nodes, monkeypatch, "nt_top", counter, limit)


def test_nt_top_exact_and_errors(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "nt_top", collections.Counter({"x": 3, "y": 3, "z": 1}), 2) == [{"name": "x", "count": 3}, {"name": "y", "count": 3}]  # ties keep insertion order
    assert check(orig_nodes, monkeypatch, "nt_top", collections.Counter({"": 5, "k": 1})) == [{"name": "k", "count": 1}]  # blank key dropped
    assert check(orig_nodes, monkeypatch, "nt_top", _Cnt({"q": 2.7})) == [{"name": "q", "count": 2}]  # int() truncation
    assert len(check(orig_nodes, monkeypatch, "nt_top", CNTS[5])) == 10 and NT._top.__defaults__ == (10,)
    assert check(orig_nodes, monkeypatch, "nt_top", None)[0] == "err" and check(orig_nodes, monkeypatch, "nt_top", {"a": 1})[0] == "err"
    assert check(orig_nodes, monkeypatch, "nt_top", collections.Counter({"a": 1}), "x")[0] == "err"


# ---- A49-5 _q9_window_view ----
WV = [{}, None, "row", {"scanner_control": {"top1_symbol": "A", "x": 1}}, {"scanner_control": "bad"}, {"strategist_selection": {"selected_symbol": "B", "y": 2}}, {"strategist_selection": []},
      {"commander_final": {"selected_symbol": "C", "decision": "APPROVE", "monitor_intent": "i", "reason": "r", "detail": "d", "monitor_reason": "mr", "extra": 1}},
      {"commander_final": {"monitor_observation": {"reason": "obs", "z": 1}}}, {"commander_final": {"monitor_observation": "bad"}}, {"commander_final": "bad"}, {"commander_final": {}},
      {"scanner_control": {}, "strategist_selection": {}, "commander_final": {"monitor_observation": {}}}, {"scanner_control": _MapSub(top1_symbol="M")}]


@pytest.mark.parametrize("row", WV)
def test_nt_q9_window_view(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "nt_q9_window_view", row)


def test_nt_q9_window_view_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "nt_q9_window_view", {**WV[3], **WV[5], **WV[7], "commander_final": {**WV[7]["commander_final"], "monitor_observation": {"reason": "obs"}}})
    assert list(out) == ["scanner_control", "strategist_selection", "commander_final"] and out["scanner_control"] == {"top1_symbol": "A"}
    assert list(out["commander_final"]) == ["selected_symbol", "decision", "monitor_intent", "reason", "detail", "monitor_reason", "monitor_observation"] and out["commander_final"]["monitor_observation"] == {"reason": "obs"}
    assert check(orig_nodes, monkeypatch, "nt_q9_window_view", {}) == {} and check(orig_nodes, monkeypatch, "nt_q9_window_view", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "nt_q9_window_view", {"commander_final": {}})["commander_final"] == {k: None for k in ("selected_symbol", "decision", "monitor_intent", "reason", "detail", "monitor_reason")}
    assert NT._q9_window_view.__doc__.startswith("The only parts of a q9 window")  # wrapper keeps the docstring

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "nt_q9_window_view", WV[7], overrides={"Mapping": NeverMapping}) == {}


# ---- A49-6 scanner_alignment_root_cause._mapping ----
@pytest.mark.parametrize("value", MAPPINGS)
def test_sar_mapping(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "sar_mapping", value)


def test_sar_mapping_identity_and_seam(orig_nodes, monkeypatch, guards):
    _mapping_checks(orig_nodes, monkeypatch, "sar_mapping", SAR)


# ---- A49-7 _rows ----
@pytest.mark.parametrize("value", [None, [], [{}], [{"a": 1}, "bad", None, 5, {"b": 2}], ({"a": 1},), {"a": 1}, "str", 0, [_MapSub(a=1), []], {}, [[("a", 1)]], 5.5])
def test_sar_rows(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "sar_rows", value)


def test_sar_rows_exact_identity_and_seams(orig_nodes, monkeypatch, guards):
    row = {"a": 1}
    out = SAR._rows([row, "x"])
    assert out == [row] and out[0] is row and SAR._rows(None) == [] and SAR._rows(None) is not SAR._rows(None)  # element identity kept, fresh list
    assert check(orig_nodes, monkeypatch, "sar_rows", [{"a": 1}, "x", {"b": 2}]) == [{"a": 1}, {"b": 2}]
    assert check(orig_nodes, monkeypatch, "sar_rows", 5)[0] == "err"
    assert check(orig_nodes, monkeypatch, "sar_rows", {"k": 1}) == []  # dict iterates over keys (str) -> not mappings

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "sar_rows", [{"a": 1}], overrides={"Mapping": NeverMapping}) == []


def test_sar_rows_generator_consumed_once(guards):
    consumed = []

    def gen():
        for r in ({"a": 1}, "x", {"b": 2}):
            consumed.append(r)
            yield r
    assert SAR._rows(gen()) == [{"a": 1}, {"b": 2}] and len(consumed) == 3  # a generator is consumed exactly once, in order


# ---- A49-8 scanner_alignment_root_cause._num ----
@pytest.mark.parametrize("value", VALS)
def test_sar_num(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "sar_num", value)


def test_sar_num_exact(orig_nodes, monkeypatch, guards):
    _scalar_checks(orig_nodes, monkeypatch, "sar_num")


# ---- structure ----
@pytest.mark.parametrize("name", list(SPEC))
def test_wrapper_thin_and_owner_holds_body(name):
    mod = MODS[SPEC[name][0]]
    fname = SPEC[name][3]
    wrapper = ast.parse(inspect.getsource(getattr(mod, fname))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], fname)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name])
    stem = SPEC[name][0]
    assert f"import {stem}" not in src and f"{stem} import" not in src.replace("from . import", "") and f"from .{stem} " not in src
