"""RF-032 A39-1..8: eight ``entry_timing_attribution`` bodies, original vs thin wrappers + Owners.

Pure/fake only; no UEF/validation-id writer is touched. Original: A preimage c591babc (blob a7559c35); canonical
2967c382 has the same blob. AST-extracted and compiled in a copy of the live namespace; dependency overrides apply to
both sides. ``_read_json`` is a fake and the report root is a fake path object, so there is no real file access,
and sockets, subprocess and writes are blocked.
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

A_PRE = "c591babc2fe7c50f4009e22fd5b532998a58e941"
CANON = "2967c3825c1036f838ef728a33df3993d5c72202"
PATH = "libs/reporting/evaluation/entry_timing_attribution.py"
BLOB = "a7559c358b7ff8e6048586ba1d42a97480ad3c79"
NAMES = ["_epoch", "_iso", "_stage_epoch", "_candidate_symbol", "_candidate_rank", "_row_at_or_before", "_daily_windows_by_id", "_pre_entry_move_pct"]
mod = importlib.import_module("libs.reporting.evaluation.entry_timing_attribution")
OWNERS = {n: importlib.import_module(f"libs.reporting.evaluation.entry_timing_attribution_{n.lstrip('_')}") for n in NAMES}
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


# ---- A39-1 _epoch ----
@pytest.mark.parametrize("value", [None, "", " ", 0, 5, -3, 5.9, True, False, "12", " 12.7 ", "-4.5", "1e3", "bad", NAN, "nan", INF, "inf",
                                   "2026-04-16T00:00:00Z", "2026-04-16T09:00:00+09:00", "2026-04-16T09:00:00", "2026-04-16", "2026-13-01T00:00:00Z", [], {}, b"5"])
def test_epoch(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_epoch", value)


def test_epoch_values_and_datetime_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_epoch", "2026-04-16T00:00:00Z") == 1776297600
    assert check(orig_nodes, monkeypatch, "_epoch", "bad") == 0

    class FakeDT:
        calls = []

        @classmethod
        def fromisoformat(cls, text):
            cls.calls.append(text)
            if text == "boom":
                raise ValueError("fake")
            return _dt.datetime(1970, 1, 1, 0, 0, 7, tzinfo=_dt.timezone.utc)
    assert check(orig_nodes, monkeypatch, "_epoch", "ISO+text", overrides={"datetime": FakeDT}) == 7
    assert check(orig_nodes, monkeypatch, "_epoch", "boom", overrides={"datetime": FakeDT}) == 0
    assert FakeDT.calls == ["ISO+text", "ISO+text", "boom", "boom"]


# ---- A39-2 _iso ----
@pytest.mark.parametrize("epoch", [0, -1, 1, 59, 1776297600, 4102444800, 10**11, 10**18, 10**20, 1.5, True, "5", None])
def test_iso(orig_nodes, monkeypatch, guards, epoch):
    check(orig_nodes, monkeypatch, "_iso", epoch)


def test_iso_values_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_iso", 0) == "" and check(orig_nodes, monkeypatch, "_iso", -5) == ""
    assert check(orig_nodes, monkeypatch, "_iso", 1776297600) == "2026-04-16T00:00:00+00:00"

    class FakeDT:
        @staticmethod
        def fromtimestamp(epoch, tz=None):
            return _dt.datetime(2000, 1, 1, 0, 0, 0, tzinfo=tz)
    assert check(orig_nodes, monkeypatch, "_iso", 5, overrides={"datetime": FakeDT}) == "2000-01-01T00:00:00+00:00"
    assert check(orig_nodes, monkeypatch, "_iso", 5, overrides={"datetime": FakeDT, "timezone": type("TZ", (), {"utc": _dt.timezone(_dt.timedelta(hours=9))})}) == "2000-01-01T00:00:00+09:00"


# ---- A39-3 _stage_epoch ----
@pytest.mark.parametrize("payload,keys", [
    ({}, ()), ({}, ("a",)), ({"a": 0}, ("a",)), ({"a": 5}, ("a",)), ({"a": 0, "b": "7"}, ("a", "b")), ({"b": 7, "a": 5}, ("a", "b")), ({"a": "bad", "b": "2026-04-16T00:00:00Z"}, ("a", "b")),
    ({"a": -4, "b": -5}, ("a", "b")), ({"a": 3}, ("x", "y", "a")), ({"a": None}, ("a",)),
])
def test_stage_epoch(orig_nodes, monkeypatch, guards, payload, keys):
    check(orig_nodes, monkeypatch, "_stage_epoch", payload, *keys)


def test_stage_epoch_epoch_seam_and_call_order(orig_nodes, monkeypatch, guards):
    seen = []
    out = check(orig_nodes, monkeypatch, "_stage_epoch", {"a": "x", "b": "y", "c": "z"}, "a", "b", "c",
                overrides={"_epoch": lambda v: seen.append(v) or (9 if v == "y" else 0)})
    assert out == 9 and seen == ["x", "y", "x", "y"]  # stops at the first positive; once per side


# ---- A39-4 _candidate_symbol / A39-5 _candidate_rank ----
@pytest.mark.parametrize("candidate", [None, "str", [], {}, {"symbol": None}, {"symbol": ""}, {"symbol": "  005930 "}, {"symbol": 5930}, {"symbol": "한글"}, {"rank": 1}, {"symbol": ["x"]}])
def test_candidate_symbol(orig_nodes, monkeypatch, guards, candidate):
    check(orig_nodes, monkeypatch, "_candidate_symbol", candidate)


def test_candidate_symbol_mapping_seam(orig_nodes, monkeypatch, guards):
    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_candidate_symbol", {"symbol": "A"}, overrides={"Mapping": NeverMapping}) == ""


def test_candidate_symbol_strips(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_candidate_symbol", {"symbol": " A "}) == "A"


@pytest.mark.parametrize("candidate", [None, "str", {}, {"rank": None}, {"rank": ""}, {"rank": 0}, {"rank": 3}, {"rank": 3.9}, {"rank": "4"}, {"rank": " 5 "}, {"rank": "bad"},
                                       {"rank": NAN}, {"rank": INF}, {"rank": True}, {"rank": [1]}, {"rank": -2}])
def test_candidate_rank(orig_nodes, monkeypatch, guards, candidate):
    check(orig_nodes, monkeypatch, "_candidate_rank", candidate)


def test_candidate_rank_num_seam(orig_nodes, monkeypatch, guards):
    seen = []
    out = check(orig_nodes, monkeypatch, "_candidate_rank", {"rank": "x"}, overrides={"_num": lambda v: seen.append(v) or 7.8})
    assert out == 7 and seen == ["x", "x"]
    assert check(orig_nodes, monkeypatch, "_candidate_rank", {"rank": 1}, overrides={"_num": lambda v: None}) is None
    assert check(orig_nodes, monkeypatch, "_candidate_rank", "notmapping", overrides={"_num": lambda v: seen.append(("n", v)) or None}) is None and ("n", None) in seen


# ---- A39-6 _row_at_or_before ----
R = [{"ts": 10, "id": "a"}, {"ts": 20, "id": "b"}, {"ts": 20, "id": "c"}, {"ts": 30, "id": "d"}]


@pytest.mark.parametrize("rows,epoch", [
    ([], 5), (R, 5), (R, 10), (R, 15), (R, 20), (R, 99), (R[::-1], 20), ([{"ts": 0}, {}], 0), ([{"ts": "15"}, {"ts": None}], 15), ([{"ts": "bad"}], 5), ([{"ts": 5.9}], 5), ([{"ts": 5}, "notarow"], 10),
])
def test_row_at_or_before(orig_nodes, monkeypatch, guards, rows, epoch):
    check(orig_nodes, monkeypatch, "_row_at_or_before", rows, epoch)


def test_row_at_or_before_identity_and_last_wins(guards):
    out = mod._row_at_or_before(R, 25)
    assert out is R[2] and out["id"] == "c"  # the LAST row with ts <= epoch, same object
    assert mod._row_at_or_before(R, 5) is None and mod._row_at_or_before([], 5) is None


# ---- A39-7 _daily_windows_by_id (fake root path) ----
class FakeRoot:
    def __init__(self, label="/rep"):
        self.label = label

    def __truediv__(self, other):
        return FakeRoot(f"{self.label}/{other}")

    def __repr__(self):
        return f"FakeRoot({self.label!r})"

    def __str__(self):
        return self.label


WINDOWS = [{}, {"windows": None}, {"windows": []}, {"windows": ["bad", None, 5]},
           {"windows": [{"decision_id": " d1 ", "n": 1}, {"decision_id": "d2"}, {"decision_id": "", "n": 9}, {"n": 8}, {"decision_id": None}]},
           {"windows": [{"decision_id": "d1", "v": "first"}, {"decision_id": "d1", "v": "last"}]},
           {"windows": [{"decision_id": "한글", "nested": {"deep": 1}}]}, {"windows": "notalist"}, {"windows": {"decision_id": "d"}}]


@pytest.mark.parametrize("payload", WINDOWS)
def test_daily_windows_by_id(orig_nodes, monkeypatch, guards, payload):
    seen = []
    out = check(orig_nodes, monkeypatch, "_daily_windows_by_id", FakeRoot(), "2026-04-16",
                overrides={"_read_json": lambda p: seen.append(str(p)) or copy.deepcopy(payload)})
    assert seen[0] == "/rep/operator_summary/daily/2026-04-16/q9_decision_windows.json" and len(seen) == 2
    assert isinstance(out, dict)


def test_daily_windows_values_and_copy(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_daily_windows_by_id", FakeRoot(), "D", overrides={"_read_json": lambda p: copy.deepcopy(WINDOWS[5])})
    assert out == {"d1": {"decision_id": "d1", "v": "last"}}  # last duplicate wins
    out = check(orig_nodes, monkeypatch, "_daily_windows_by_id", FakeRoot(), "D", overrides={"_read_json": lambda p: copy.deepcopy(WINDOWS[4])})
    assert list(out) == ["d1", "d2"]
    nested = {"deep": 1}
    src = {"windows": [{"decision_id": "x", "nested": nested}]}
    monkeypatch.setattr(mod, "_read_json", lambda p: src)
    live = mod._daily_windows_by_id(FakeRoot(), "D")
    assert live["x"] is not src["windows"][0] and live["x"]["nested"] is nested


# ---- A39-8 _pre_entry_move_pct ----
ROWS = {"005930": [{"ts": 100, "close": 100.0, "raw_ts": "R1"}, {"ts": 200, "price": 110.0}, {"ts": 300, "close": 0}]}


@pytest.mark.parametrize("kwargs", [
    dict(symbol="", decision_epoch=250, entry_price=120.0), dict(symbol="005930", decision_epoch=0, entry_price=120.0), dict(symbol="005930", decision_epoch=-5, entry_price=120.0),
    dict(symbol="005930", decision_epoch=250, entry_price=None), dict(symbol="005930", decision_epoch=250, entry_price=0.0), dict(symbol="005930", decision_epoch=250, entry_price=-1.0),
    dict(symbol="005930", decision_epoch=50, entry_price=120.0), dict(symbol="UNKNOWN", decision_epoch=250, entry_price=120.0),
    dict(symbol="005930", decision_epoch=150, entry_price=105.0), dict(symbol="005930", decision_epoch=250, entry_price=121.0), dict(symbol="005930", decision_epoch=350, entry_price=121.0),
    dict(symbol="005930", decision_epoch=100, entry_price=100.0),
])
def test_pre_entry_move_pct(orig_nodes, monkeypatch, guards, kwargs):
    check(orig_nodes, monkeypatch, "_pre_entry_move_pct", minute_rows_by_symbol=ROWS, **kwargs)


def test_pre_entry_values_and_seams(orig_nodes, monkeypatch, guards):
    move, meta = check(orig_nodes, monkeypatch, "_pre_entry_move_pct", symbol="005930", decision_epoch=150, entry_price=105.0, minute_rows_by_symbol=ROWS)
    assert move == 5.0 and list(meta) == ["available", "decision_base_price", "decision_base_ts"] and meta["decision_base_ts"] == "R1"
    move, meta = check(orig_nodes, monkeypatch, "_pre_entry_move_pct", symbol="005930", decision_epoch=250, entry_price=121.0, minute_rows_by_symbol=ROWS)
    assert move == 10.0 and meta["decision_base_ts"] == 200  # raw_ts missing -> ts fallback
    move, meta = check(orig_nodes, monkeypatch, "_pre_entry_move_pct", symbol="005930", decision_epoch=350, entry_price=121.0, minute_rows_by_symbol=ROWS)
    assert move is None and meta == {"available": False, "reason": "decision_base_price_unavailable"}
    out = check(orig_nodes, monkeypatch, "_pre_entry_move_pct", symbol="005930", decision_epoch=250, entry_price=50.0, minute_rows_by_symbol=ROWS,
                overrides={"_row_at_or_before": lambda rows, epoch: {"close": 25.0, "ts": 1}, "_num": lambda v: v})
    assert out[0] == 100.0


# ---- structure ----
@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name]).replace("entry_timing_attribution_", "")
    assert "entry_timing_attribution import" not in src and "import entry_timing_attribution" not in src
