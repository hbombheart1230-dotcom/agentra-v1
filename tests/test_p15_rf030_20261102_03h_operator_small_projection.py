"""RF-030 A27-1..6: six small operator_visibility helpers, original vs thin wrappers + Owners.

Pins: actor preimage 8ea0702d blob f879b2d7; canonical cf60c30c blob 03baa1c1. The six original function texts must be
identical across both before any parity claim. Originals are compiled in a copy of the live module namespace.
"""
from __future__ import annotations

import ast
import copy
import datetime as _dt
import hashlib
import importlib
import inspect
import socket
import subprocess
from pathlib import Path

import pytest

A_PRE = "8ea0702dcc322caae176c0eab9d7349a1fbeed20"
A_BLOB = "f879b2d7a1fc1d7dd65d321938025b2030cd6b0a"
CANON = "cf60c30cbd45eeeea4606a5e1b2aabe65603caf5"
CANON_BLOB = "03baa1c1554b10a012d4abb56248caf0e44c2e78"
PATH = "libs/reporting/operator_visibility.py"
NAMES = ["_pick_day", "_safe_int", "_safe_float", "_health_badge", "_compact_blocking_features", "_decision_trace_inner"]
ov = importlib.import_module("libs.reporting.operator_visibility")
OWNERS = {n: importlib.import_module(f"libs.reporting.operator_visibility_{n.lstrip('_')}") for n in NAMES}


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


def _show(commit):
    return subprocess.run(["git", "show", f"{commit}:{PATH}"], check=True, capture_output=True).stdout


def _nodes(raw):
    tree = ast.parse(raw.decode("utf-8"))
    found = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in NAMES}
    assert sorted(found) == sorted(NAMES)
    return found


@pytest.fixture(scope="module")
def orig_nodes():
    try:
        a_raw, c_raw = _show(A_PRE), _show(CANON)
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(a_raw) == A_BLOB, "BLOCKED_PIN actor blob"
    assert _sha(c_raw) == CANON_BLOB, "BLOCKED_PIN canonical blob"
    a, c = _nodes(a_raw), _nodes(c_raw)
    for n in NAMES:
        sa = ast.get_source_segment(a_raw.decode(), a[n])
        sc = ast.get_source_segment(c_raw.decode(), c[n])
        assert sa == sc, f"HOLD RF030: {n} differs actor vs canonical"
    return a


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(Path, "mkdir", boom)
    monkeypatch.setattr(Path, "write_text", boom)
    monkeypatch.setattr(Path, "read_text", boom)


def check(orig_nodes, monkeypatch, name, *args, overrides=None, **kwargs):
    ns = dict(vars(ov))
    mod = ast.Module(body=[copy.deepcopy(orig_nodes[name])], type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), f"<{A_PRE[:8]}:{PATH}>", "exec"), ns)
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(ov, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[name]), ("new", getattr(ov, name))):
        a, k = copy.deepcopy((args, kwargs))
        try:
            values[label] = fn(*a, **k)
            got[label] = ("ok", repr(values[label]))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert repr((a, k)) == repr((args, kwargs)), f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


# A27-1 _pick_day
class _FakeDate:
    @staticmethod
    def today():
        return _dt.date(2031, 2, 3)


@pytest.mark.parametrize("rows,requested", [
    ([], None), ([], ""), ([], "  2026-04-16  "), ([{"_day": "2026-04-16"}, {"_day": "2026-04-15"}, {"_day": "2026-04-17"}], None),
    ([{"_day": ""}, {}, {"_day": None}, {"_day": 20260416}], None), ([{"_day": "b"}, {"_day": "a"}, {"_day": "b"}], ""),
    ([{"_day": "x"}], 0), ([{"_day": "x"}], "   "),
])
def test_pick_day(orig_nodes, monkeypatch, guards, rows, requested):
    check(orig_nodes, monkeypatch, "_pick_day", rows, requested)


def test_pick_day_facade_date_patch(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_pick_day", [], None, overrides={"date": _FakeDate}) == "2031-02-03"
    assert check(orig_nodes, monkeypatch, "_pick_day", [{"_day": "z"}], None, overrides={"date": _FakeDate}) == "z"


# A27-2/3 _safe_int / _safe_float
@pytest.mark.parametrize("v", [0, -3, 2.9, -2.9, "7", "7.9", " 8 ", None, "", "abc", float("nan"), float("inf"), [1], True, "1e3"])
@pytest.mark.parametrize("default", [0, 5, -1.5, "x"])
def test_safe_int(orig_nodes, monkeypatch, guards, v, default):
    check(orig_nodes, monkeypatch, "_safe_int", v, default)


def test_safe_int_default_arg_and_exception_paths(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_safe_int", "3.7") == 3
    assert check(orig_nodes, monkeypatch, "_safe_int", None) == 0
    out = check(orig_nodes, monkeypatch, "_safe_int", None, "not-an-int")  # int(default) raises -> same error both sides
    assert out[0] == "err" and out[1] == "ValueError"


@pytest.mark.parametrize("v", [0, -3, 2.5, "7.25", " 8 ", None, "", "abc", float("nan"), float("inf"), "-inf", [1], True])
@pytest.mark.parametrize("default", [0.0, 5, -1.5, "y"])
def test_safe_float(orig_nodes, monkeypatch, guards, v, default):
    check(orig_nodes, monkeypatch, "_safe_float", v, default)


# A27-4 _health_badge
@pytest.mark.parametrize("level", ["GREEN", "yellow", " Red ", "unknown", "", None, "  ", "BLUE", 0, "green\n"])
def test_health_badge(orig_nodes, monkeypatch, guards, level):
    check(orig_nodes, monkeypatch, "_health_badge", level)


def test_health_badge_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_health_badge", "red") == "[RED]"
    assert check(orig_nodes, monkeypatch, "_health_badge", None) == "[UNKNOWN]"
    assert check(orig_nodes, monkeypatch, "_health_badge", "mauve") == "[MAUVE]"


# A27-5 _compact_blocking_features
@pytest.mark.parametrize("raw", [None, "abc", {"a": 1}, [], ["", "  ", None], ["a", " b ", "", "c", "d"], ["한글", "é", "x"], [1, 2, 3, 4]])
@pytest.mark.parametrize("limit", [0, 1, 3, 10, -1])
def test_compact_blocking_features(orig_nodes, monkeypatch, guards, raw, limit):
    check(orig_nodes, monkeypatch, "_compact_blocking_features", raw, limit=limit)


def test_compact_blocking_features_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_compact_blocking_features", ["a", "", " b ", "c", "d"]) == "a, b, c"
    assert check(orig_nodes, monkeypatch, "_compact_blocking_features", ["a"], limit=0) == ""
    assert check(orig_nodes, monkeypatch, "_compact_blocking_features", "nope") == "-"


# A27-6 _decision_trace_inner
INNER = {"k": 1}


@pytest.mark.parametrize("payload", [{}, {"payload": INNER}, {"payload": "bad"}, {"payload": None}, {"payload": []}, {"payload": {}},
                                     {"other": 1}, {"payload": {"payload": {"deep": 1}}}])
def test_decision_trace_inner(orig_nodes, monkeypatch, guards, payload):
    check(orig_nodes, monkeypatch, "_decision_trace_inner", payload)


def test_decision_trace_inner_identity(guards):
    payload = {"payload": INNER}
    assert ov._decision_trace_inner(payload) is INNER


# structure
@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(ov, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.SetComp))]
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    assert "operator_visibility import" not in inspect.getsource(OWNERS[name])
