"""RF-030 A30-1..8: eight pure ``operator_period_summary`` helpers, original vs thin wrappers + Owners.

Originals: A preimage eab2e67e blob 8515b041 (canonical b8e21e62 has the same blob). AST-extracted and compiled in a
copy of the live namespace; dependency overrides apply to both sides. Pure computation: no IO, sockets or writes.
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

A_PRE = "eab2e67ea2a3835a36eb35d5633b603c0866c13f"
CANON = "b8e21e62d7ddb087eca1251ffe1ca2d631837aa8"
PATH = "libs/reporting/operator_period_summary.py"
BLOB = "8515b041eaa391ce9d62a9f666ef21cbb707030f"
NAMES = ["_text_value", "_first_text", "_is_unavailable_pnl", "_ratio_to_pct", "_normalize_symbol_code",
         "_metric_return_pct", "_first_dict", "_metric_observed_return_pct"]
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


# A30-1 _text_value
@pytest.mark.parametrize("value", [None, "", " ", "-", "None", "NULL", " Unknown ", "not_captured", "NOT_CAPTURED", "ok", " 한글 ", 0, False, 12, [], {}, "n/a"])
def test_text_value(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_text_value", value)


def test_text_value_markers(orig_nodes, monkeypatch, guards):
    for marker in ("-", "none", "NULL", "Unknown", "not_captured", "", "  "):
        assert check(orig_nodes, monkeypatch, "_text_value", marker) == ""
    assert check(orig_nodes, monkeypatch, "_text_value", "  A b ") == "A b"


# A30-2 _first_text
@pytest.mark.parametrize("values", [(), (None,), (None, "", "-"), ("a", "b"), (None, " x ", "y"), ("unknown", "한글"), (0, False, 5), ([], {}, "z")])
def test_first_text(orig_nodes, monkeypatch, guards, values):
    check(orig_nodes, monkeypatch, "_first_text", *values)


def test_first_text_use_time_text_value(orig_nodes, monkeypatch, guards):
    seen = []
    out = check(orig_nodes, monkeypatch, "_first_text", 1, 2, 3,
                overrides={"_text_value": lambda v: seen.append(v) or ("hit" if v == 2 else "")})
    assert out == "hit" and seen == [1, 2, 1, 2]  # once per side (original, wrapper)


# A30-3 _is_unavailable_pnl
@pytest.mark.parametrize("value", [None, "", " ", "-", "None", "NULL", " Unavailable ", "not_available", "NOT_AVAILABLE", "0", 0, 0.0, "1.5", -3, "n/a", False])
def test_is_unavailable_pnl(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_is_unavailable_pnl", value)


def test_is_unavailable_pnl_fake_values_set(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_is_unavailable_pnl", "custom", overrides={"_UNAVAILABLE_PNL_VALUES": {"custom"}}) is True
    assert check(orig_nodes, monkeypatch, "_is_unavailable_pnl", "none", overrides={"_UNAVAILABLE_PNL_VALUES": {"custom"}}) is False


# A30-4 _ratio_to_pct
@pytest.mark.parametrize("value", [None, "", 0, 0.5, "0.25", -0.1, "abc", NAN, INF, -INF, "nan", True, [1]])
def test_ratio_to_pct(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_ratio_to_pct", value)


def test_ratio_to_pct_safe_float_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_ratio_to_pct", "0.5") == 50.0
    assert check(orig_nodes, monkeypatch, "_ratio_to_pct", "x", overrides={"_safe_float": lambda v: 0.07}) == pytest.approx(7.0)
    assert check(orig_nodes, monkeypatch, "_ratio_to_pct", 1, overrides={"_safe_float": lambda v: None}) is None


# A30-5 _normalize_symbol_code
@pytest.mark.parametrize("value", [None, "", " ", "005930", "A005930", " a005930 ", "a00593", "A0059300", "abc1234", "A123456", 5930, "  ", "삼성"])
def test_normalize_symbol_code(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_normalize_symbol_code", value)


def test_normalize_symbol_code_values(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_normalize_symbol_code", " a005930 ") == "005930"
    assert check(orig_nodes, monkeypatch, "_normalize_symbol_code", "A00593") == "A00593"


# A30-6 _metric_return_pct / A30-8 _metric_observed_return_pct
ROWS = [{}, {"truth_surface_available": True}, {"truth_surface_available": False, "result_pct": "1.5", "truth_net_return_pct": 9},
        {"truth_surface_available": True, "truth_net_return_pct": "2.5", "result_pct": 9, "truth_observed_return_pct": "3.5"},
        {"truth_surface_available": 0, "result_pct": None}, {"truth_surface_available": "yes", "truth_net_return_pct": "bad"},
        {"truth_surface_available": True, "truth_net_return_pct": NAN, "truth_observed_return_pct": INF}, {"result_pct": ""}]


@pytest.mark.parametrize("row", ROWS)
def test_metric_return_pct(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_metric_return_pct", row)


@pytest.mark.parametrize("row", ROWS)
def test_metric_observed_return_pct(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_metric_observed_return_pct", row)


def test_metric_precedence_and_safe_float_seam(orig_nodes, monkeypatch, guards):
    row = {"truth_surface_available": True, "truth_net_return_pct": "2.5", "result_pct": "9", "truth_observed_return_pct": "3.5"}
    assert check(orig_nodes, monkeypatch, "_metric_return_pct", row) == 2.5
    assert check(orig_nodes, monkeypatch, "_metric_observed_return_pct", row) == 3.5
    assert check(orig_nodes, monkeypatch, "_metric_observed_return_pct", {"result_pct": "1"}) is None
    seen = []
    out = check(orig_nodes, monkeypatch, "_metric_return_pct", {"result_pct": "7"},
                overrides={"_safe_float": lambda v: seen.append(v) or 0.5})
    assert out == 0.5 and seen == ["7", "7"]


# A30-7 _first_dict
@pytest.mark.parametrize("values", [(), (None,), ({},), ({"a": 1},), ({}, {"b": 2}, {"c": 3}), ([1], "x", {"d": 4}), ({"z": 1, "a": 2},)])
def test_first_dict(orig_nodes, monkeypatch, guards, values):
    check(orig_nodes, monkeypatch, "_first_dict", *values)


def test_first_dict_copy_identity_and_order(orig_nodes, monkeypatch, guards):
    src = {"z": 1, "a": {"n": 1}}
    out = ops._first_dict(src)
    assert out == src and out is not src and out["a"] is src["a"] and list(out) == ["z", "a"]
    assert check(orig_nodes, monkeypatch, "_first_dict", {}, src) == src


# structure
@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(ops, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 2 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name]).replace("operator_period_summary_", "")
    assert "operator_period_summary import" not in src and "import operator_period_summary" not in src
