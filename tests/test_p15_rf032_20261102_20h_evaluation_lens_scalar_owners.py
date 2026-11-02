"""RF-032 A44-1..8: eight ``evaluation_lens_report`` scalar helper bodies, original vs thin wrappers + Owners.

Original = A preimage 513e49b6 (SOURCE blob c9925614 == canonical 35831d3a). Each original function is compiled from
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

A_PRE = "513e49b6894c330dc09ead392fdd127ff1b12906"
CANON = "35831d3add03ec351bcf49dfe791e8c5c8969ff8"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_text": ("evaluation_lens_report", "c99256145787354305f8d008e540499043226a87", "evaluation_lens_report_text"),
    "_num": ("evaluation_lens_report", "c99256145787354305f8d008e540499043226a87", "evaluation_lens_report_num"),
    "_as_dict": ("evaluation_lens_report", "c99256145787354305f8d008e540499043226a87", "evaluation_lens_report_as_dict"),
    "_metric_avg": ("evaluation_lens_report", "c99256145787354305f8d008e540499043226a87", "evaluation_lens_report_metric_avg"),
    "_checkpoint": ("evaluation_lens_report", "c99256145787354305f8d008e540499043226a87", "evaluation_lens_report_checkpoint"),
    "_checkpoint_return": ("evaluation_lens_report", "c99256145787354305f8d008e540499043226a87", "evaluation_lens_report_checkpoint_return"),
    "_checkpoint_mfe": ("evaluation_lens_report", "c99256145787354305f8d008e540499043226a87", "evaluation_lens_report_checkpoint_mfe"),
    "_checkpoint_mae": ("evaluation_lens_report", "c99256145787354305f8d008e540499043226a87", "evaluation_lens_report_checkpoint_mae"),
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
                out[n] = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == n][-1]
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


class _Str:
    def __init__(self, text, truthy=True):
        self.text, self.truthy = text, truthy

    def __repr__(self):
        return f"_Str({self.text!r},{self.truthy})"

    def __str__(self):
        return self.text

    def __bool__(self):
        return self.truthy


class _BadStr:
    def __repr__(self):
        return "_BadStr()"

    def __str__(self):
        raise RuntimeError("str failure")


class _BadFloat:
    def __repr__(self):
        return "_BadFloat()"

    def __float__(self):
        raise RuntimeError("custom float failure")


class _OkFloat:
    def __repr__(self):
        return "_OkFloat()"

    def __float__(self):
        return 2.5


MOD = MODS["evaluation_lens_report"]


def _cp(ret=None, mfe=None, mae=None, status="observed"):
    return {"status": status, "return_pct": ret, "mfe_pct": mfe, "mae_pct": mae}


def _row(h="+5m", **cp):
    return {"shadow_forward_outcome": {"checkpoints": {h: _cp(**cp)}}}


# ---- A44-1 _text ----
@pytest.mark.parametrize("value", [None, 0, 0.0, False, "", "  ", "\t\n", " a ", "한글", " 한글 ", 5, 1.5, [], [1], {}, _Str(" custom "), _Str("  "), _Str("x", truthy=False), "x y "])
def test_text_values(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_text", value)


def test_text_exact_and_errors(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_text", None) == "" and check(orig_nodes, monkeypatch, "_text", 0) == ""  # falsy -> empty string
    assert check(orig_nodes, monkeypatch, "_text", "  한글 ") == "한글" and check(orig_nodes, monkeypatch, "_text", _Str(" cu ")) == "cu"
    assert check(orig_nodes, monkeypatch, "_text", _Str("x", truthy=False)) == ""
    assert check(orig_nodes, monkeypatch, "_text", _BadStr()) == ("err", "RuntimeError", "str failure")
    assert list(inspect.signature(MOD._text).parameters) == ["value"]


# ---- A44-2 _num ----
@pytest.mark.parametrize("value", [None, "", 0, 0.0, "0", " 1.5 ", "abc", "1e3", "nan", "inf", NAN, True, [], {}, b"2", _OkFloat(), _BadFloat(), (), "-0", "１２"])
@pytest.mark.parametrize("default", [None, -1.0, "dflt"])
def test_num_values(orig_nodes, monkeypatch, guards, value, default):
    check(orig_nodes, monkeypatch, "_num", value, default)
    check(orig_nodes, monkeypatch, "_num", value)


def test_num_exact_and_broad_catch(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_num", None) is None and check(orig_nodes, monkeypatch, "_num", "", 7.0) == 7.0
    assert check(orig_nodes, monkeypatch, "_num", 0) == 0.0 and check(orig_nodes, monkeypatch, "_num", "x", 3.0) == 3.0
    assert check(orig_nodes, monkeypatch, "_num", _BadFloat(), -9.0) == -9.0  # broad Exception catch (RuntimeError too)
    out = check(orig_nodes, monkeypatch, "_num", "nan")
    assert out != out
    assert inspect.signature(MOD._num).parameters["default"].default is None


# ---- A44-3 _as_dict ----
@pytest.mark.parametrize("value", [None, {}, {"b": 1, "a": 2}, [], [("a", 1)], "s", 5, {"n": {"deep": [1]}}, ((1, 2),)])
def test_as_dict(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_as_dict", value)


def test_as_dict_copy_order_and_seam(orig_nodes, monkeypatch, guards):
    src = {"z": 1, "a": {"x": 1}}
    out = MOD._as_dict(src)
    assert out == src and out is not src and list(out) == ["z", "a"] and out["a"] is src["a"]  # shallow copy, order kept
    assert MOD._as_dict(None) == {} and MOD._as_dict(None) is not MOD._as_dict(None)

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_as_dict", {"a": 1}, overrides={"Mapping": NeverMapping}) == {}


# ---- A44-4 _metric_avg ----
@pytest.mark.parametrize("metric", [{}, None, "bad", {"count": 0}, {"count": -1, "average_return_pct": 1}, {"count": 1}, {"count": 1, "average_return_pct": 0.123456},
                                    {"count": "2", "average_return_pct": "x"}, {"count": "bad", "average_return_pct": 1}, {"count": 3.7, "average_return_pct": -2}, {"count": True, "average_return_pct": 0},
                                    {"count": None, "average_return_pct": 5}])
def test_metric_avg(orig_nodes, monkeypatch, guards, metric):
    check(orig_nodes, monkeypatch, "_metric_avg", metric)


def test_metric_avg_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_metric_avg", {"count": 0, "average_return_pct": 9}) == "-"
    assert check(orig_nodes, monkeypatch, "_metric_avg", {"count": 1, "average_return_pct": 0.5}) == "0.5"
    assert check(orig_nodes, monkeypatch, "_metric_avg", {"count": 1}) == "None"  # exact str(None)
    assert check(orig_nodes, monkeypatch, "_metric_avg", {"count": "bad"})[0:2] == ("err", "ValueError")
    seen = []
    out = check(orig_nodes, monkeypatch, "_metric_avg", "ignored", overrides={"_as_dict": lambda v: seen.append(v) or {"count": 2, "average_return_pct": "P"}})
    assert out == "P" and seen == ["ignored", "ignored"]


# ---- A44-5 _checkpoint ----
CPS = [{}, None if False else {"shadow_forward_outcome": None}, {"shadow_forward_outcome": "x"}, {"shadow_forward_outcome": {"checkpoints": None}}, {"shadow_forward_outcome": {"checkpoints": "x"}},
       {"shadow_forward_outcome": {"checkpoints": {}}}, _row(ret=1.0), {"shadow_forward_outcome": {"checkpoints": {"+5m": "bad"}}}, {"shadow_forward_outcome": {"checkpoints": {"+5m": None}}},
       _row("+15m", ret=2.0)]


@pytest.mark.parametrize("row", CPS)
@pytest.mark.parametrize("horizon", ["+5m", "+15m", "EOD", None])
def test_checkpoint(orig_nodes, monkeypatch, guards, row, horizon):
    check(orig_nodes, monkeypatch, "_checkpoint", row, horizon)


def test_checkpoint_copy_and_helper_order(orig_nodes, monkeypatch, guards):
    inner = _cp(ret=1.0)
    row = {"shadow_forward_outcome": {"checkpoints": {"+5m": inner}}}
    out = MOD._checkpoint(row, "+5m")
    assert out == inner and out is not inner  # _as_dict shallow copy at the end
    assert check(orig_nodes, monkeypatch, "_checkpoint", None, "+5m")[0] == "err"
    seen = []
    out = check(orig_nodes, monkeypatch, "_checkpoint", {"k": 1}, "+5m", overrides={"_as_dict": lambda v: seen.append(v) or ({"checkpoints": {"+5m": 7}} if len(seen) % 3 == 1 else {"+5m": 8})})
    assert len(seen) == 6 and out == {"+5m": 8}  # three helper calls per side (outcome, checkpoints, horizon)


# ---- A44-6/7/8 _checkpoint_return / _mfe / _mae ----
FIELD = {"_checkpoint_return": "return_pct", "_checkpoint_mfe": "mfe_pct", "_checkpoint_mae": "mae_pct"}
PROJ_ROWS = [{}, _row(ret=1.0, mfe=2.0, mae=-3.0), _row(ret=0, mfe=0, mae=0), _row(ret="1.25", mfe="2.5", mae="-3.5"), _row(ret="bad", mfe="bad", mae="bad"), _row(ret="", mfe="", mae=""),
             _row(ret=None, mfe=None, mae=None), _row(status="pending", ret=1.0, mfe=2.0, mae=-3.0), _row(status="OBSERVED", ret=1.0, mfe=1.0, mae=1.0), _row(status=None, ret=1.0),
             _row("+15m", ret=1.0, mfe=2.0, mae=-3.0), {"shadow_forward_outcome": {"checkpoints": {"+5m": {"status": "observed"}}}}, _row(ret=NAN, mfe=NAN, mae=NAN)]


@pytest.mark.parametrize("name", list(FIELD))
@pytest.mark.parametrize("row", PROJ_ROWS)
@pytest.mark.parametrize("horizon", ["+5m", "+15m"])
def test_checkpoint_projection(orig_nodes, monkeypatch, guards, name, row, horizon):
    check(orig_nodes, monkeypatch, name, row, horizon)


@pytest.mark.parametrize("name", list(FIELD))
def test_checkpoint_projection_exact_none_zero_and_seams(orig_nodes, monkeypatch, guards, name):
    kwargs = {"ret": 0, "mfe": 0, "mae": 0}
    assert check(orig_nodes, monkeypatch, name, _row(**kwargs), "+5m") == 0.0  # 0.0 is returned, not None
    assert check(orig_nodes, monkeypatch, name, _row(status="pending", ret=1, mfe=1, mae=1), "+5m") is None
    assert check(orig_nodes, monkeypatch, name, _row(ret="x", mfe="x", mae="x"), "+5m") is None  # _num -> None
    assert check(orig_nodes, monkeypatch, name, None, "+5m")[0] == "err"
    out = check(orig_nodes, monkeypatch, name, {"z": 1}, "+5m", overrides={"_checkpoint": lambda r, h: {"status": "observed", FIELD[name]: "9"}, "_num": lambda v: float(v) * 2})
    assert out == 18.0
    out = check(orig_nodes, monkeypatch, name, {"z": 1}, "+5m", overrides={"_checkpoint": lambda r, h: {"status": "nope", FIELD[name]: "9"}})
    assert out is None


# ---- structure ----
@pytest.mark.parametrize("name", list(SPEC))
def test_wrapper_thin_and_owner_holds_body(name):
    mod = MODS[SPEC[name][0]]
    wrapper = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name])
    stem = SPEC[name][0]
    assert f"import {stem}" not in src and f"{stem} import" not in src.replace("from . import", "") and f"from .{stem} " not in src
