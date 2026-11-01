"""RF-030 A28-1..8: eight read-only/pure ``operator_period_summary`` helpers, original vs thin wrappers + Owners.

Originals are AST-extracted from the pinned preimage (b77d8559, blob d6d1dd1c) and compiled in a copy of the live
module namespace; dependency overrides apply to both sides. All filesystem/env access is faked or temp-only; sockets,
subprocess and every write path are blocked.
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

PRE = "b77d8559cf8e2ae86ce640439278c84a36ee92c9"
PATH = "libs/reporting/operator_period_summary.py"
PRE_BLOB = "d6d1dd1ceb95842926095228c02bc5b35849ca17"
NAMES = ["_looks_like_mojibake", "_truth_surface_candidate_paths", "_closeout_broker_skip_for_row",
         "_state_snapshot_candidate_paths", "_first_snapshot_call_payload", "_price_matches",
         "_sell_guard_candidate_paths", "_trade_dir_for_row"]
ops = importlib.import_module("libs.reporting.operator_period_summary")
OWNERS = {n: importlib.import_module(f"libs.reporting.operator_period_summary_{n.lstrip('_')}") for n in NAMES}


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    try:
        raw = subprocess.run(["git", "show", f"{PRE}:{PATH}"], check=True, capture_output=True).stdout
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(raw) == PRE_BLOB, "BLOCKED_PIN original blob"
    tree = ast.parse(raw.decode("utf-8"))
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
    for attr in ("write_text", "write_bytes", "mkdir", "touch", "unlink", "rename", "replace"):
        monkeypatch.setattr(Path, attr, boom)
    real_open = builtins.open

    def guarded_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+"):
            raise AssertionError("write open attempted")
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)


def check(orig_nodes, monkeypatch, name, *args, overrides=None, **kwargs):
    ns = dict(vars(ops))
    mod = ast.Module(body=[copy.deepcopy(orig_nodes[name])], type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), f"<{PRE[:8]}:{PATH}>", "exec"), ns)
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


# ---- A28-1 _looks_like_mojibake ----
@pytest.mark.parametrize("text", ["", "ascii text", "a?b", "정상 한글", "깨짐�", "豈", "한??", "한?", "??", "é??", "ok?刺", None])
def test_looks_like_mojibake(orig_nodes, monkeypatch, guards, text):
    check(orig_nodes, monkeypatch, "_looks_like_mojibake", text)


def test_looks_like_mojibake_values(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_looks_like_mojibake", "한??") is True
    assert check(orig_nodes, monkeypatch, "_looks_like_mojibake", "??") is False
    assert check(orig_nodes, monkeypatch, "_looks_like_mojibake", "") is False


# ---- A28-2 _truth_surface_candidate_paths ----
class _Resolver:
    def __init__(self, hit):
        self.hit, self.calls = hit, []

    def find(self, root, trade_id):
        self.calls.append((str(root), trade_id))
        return Path(self.hit) if self.hit else None


def _truth_overrides(hit):
    r = _Resolver(hit)
    return r, {"find_trade_dir": r.find, "canonical_trade_day_root": lambda root, day: Path(root) / "CANON" / day}


ROWS = [
    {}, {"trade_root_path": "/t/root"}, {"report_path": "/t/rep/report.md"}, {"lifecycle_bundle_path": "/t/life/bundle.json"},
    {"trade_id": "T1", "date": "2026-04-16T09:00:00"}, {"trade_id": "T1", "day": "2026-04-16"}, {"trade_id": "T1"},
    {"trade_root_path": "/t/root", "report_path": "/t/root/reports/x.md", "lifecycle_bundle_path": "/t/root/b.json",
     "trade_id": "T1", "date": "2026-04-16"},  # duplicates -> dedup keeps first
    {"trade_root_path": "  ", "report_path": None},
]


@pytest.mark.parametrize("row", ROWS)
@pytest.mark.parametrize("hit", [None, "/found/T1"])
def test_truth_surface_candidate_paths(orig_nodes, monkeypatch, guards, row, hit):
    _, ov = _truth_overrides(hit)
    check(orig_nodes, monkeypatch, "_truth_surface_candidate_paths", row, Path("/reports"), overrides=ov)


def test_truth_surface_dedup_and_order(orig_nodes, monkeypatch, guards):
    _, ov = _truth_overrides(None)
    out = check(orig_nodes, monkeypatch, "_truth_surface_candidate_paths", ROWS[7], Path("/reports"), overrides=ov)
    keys = [str(p) for p in out]
    assert keys == list(dict.fromkeys(keys)) and keys[0].endswith("/t/root/reports/ai_trade_summary.json")
    assert any("/reports/trades/2026-04-16/T1/reports/ai_trade_summary.json" in k for k in keys)


# ---- A28-3 _closeout_broker_skip_for_row ----
def _json_fake(table):
    seen = []

    def _read_json(path):
        seen.append(str(path))
        return copy.deepcopy(table.get(str(path), {}))
    _read_json.seen = seen
    return _read_json


CLOSEOUT = "/reports/operator_summary/daily/2026-04-16/closeout_maintenance.json"
BROKER = {"steps": {"broker_closed_trade_reconciliation": {"snapshot_path": "/snap.json",
                                                           "skipped": [{"trade_id": "T0", "reason": "x"},
                                                                       "bad", {"trade_id": "T1", "reason": "no_fill"}]}}}


@pytest.mark.parametrize("row,table", [
    ({}, {}), ({"trade_id": "T1"}, {}), ({"date": "2026-04-16"}, {}),
    ({"trade_id": "T1", "date": "2026-04-16"}, {}),
    ({"trade_id": "T1", "date": "2026-04-16"}, {CLOSEOUT: BROKER}),
    ({"trade_id": "T9", "day": "2026-04-16"}, {CLOSEOUT: BROKER}),
    ({"trade_id": "T1", "date": "2026-04-16"}, {CLOSEOUT: {"steps": "bad"}}),
    ({"trade_id": "T1", "date": "2026-04-16"}, {CLOSEOUT: {"steps": {"broker_closed_trade_reconciliation": {"skipped": None}}}}),
    ({"trade_id": "T1", "date": "2026-04-16"}, {CLOSEOUT: ["not a dict"]}),
])
def test_closeout_broker_skip_for_row(orig_nodes, monkeypatch, guards, row, table):
    check(orig_nodes, monkeypatch, "_closeout_broker_skip_for_row", row, Path("/reports"),
          overrides={"_read_json": _json_fake(table)})


def test_closeout_broker_skip_values(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_closeout_broker_skip_for_row", {"trade_id": "T1", "date": "2026-04-16"},
                Path("/reports"), overrides={"_read_json": _json_fake({CLOSEOUT: BROKER})})
    assert out == {"broker_reconciliation_status": "skipped_unresolved", "broker_reconciliation_reason": "no_fill",
                   "broker_reconciliation_snapshot_path": "/snap.json"}


# ---- A28-4 _state_snapshot_candidate_paths / A28-7 _sell_guard_candidate_paths ----
@pytest.mark.parametrize("env", [None, "", "  ", "/env/state.json", "/data/state.json"])
def test_state_snapshot_candidate_paths(orig_nodes, monkeypatch, guards, env):
    if env is None:
        monkeypatch.delenv("STATE_STORE_PATH", raising=False)
    else:
        monkeypatch.setenv("STATE_STORE_PATH", env)
    check(orig_nodes, monkeypatch, "_state_snapshot_candidate_paths", Path("/root/reports"))


def test_state_snapshot_duplicate_resolved_and_resolver_exception(orig_nodes, monkeypatch, guards):
    monkeypatch.setenv("STATE_STORE_PATH", "/alias/state.json")
    monkeypatch.setattr(Path, "resolve", lambda self, *a, **k: Path("/same/resolved"))
    out = check(orig_nodes, monkeypatch, "_state_snapshot_candidate_paths", Path("/root/reports"))
    assert [str(p) for p in out] == ["/alias/state.json"]  # both resolve to one key -> first kept

    def raising(self, *a, **k):
        raise OSError("fake resolve failure")
    monkeypatch.setattr(Path, "resolve", raising)
    out = check(orig_nodes, monkeypatch, "_state_snapshot_candidate_paths", Path("/root/reports"))
    assert [str(p) for p in out] == ["/alias/state.json", "/root/data/state.json"]


@pytest.mark.parametrize("state_path", ["", "  ", None, "/x/data/state.json", "/root/data/state.json"])
def test_sell_guard_candidate_paths(orig_nodes, monkeypatch, guards, state_path):
    check(orig_nodes, monkeypatch, "_sell_guard_candidate_paths", reports_root=Path("/root/reports"), state_path=state_path)


def test_sell_guard_duplicate_and_resolve_exception(orig_nodes, monkeypatch, guards):
    monkeypatch.setattr(Path, "resolve", lambda self, *a, **k: Path("/one"))
    out = check(orig_nodes, monkeypatch, "_sell_guard_candidate_paths", reports_root=Path("/root/reports"), state_path="/a/s.json")
    assert len(out) == 1

    def raising(self, *a, **k):
        raise RuntimeError("fake")
    monkeypatch.setattr(Path, "resolve", raising)
    out = check(orig_nodes, monkeypatch, "_sell_guard_candidate_paths", reports_root=Path("/root/reports"), state_path="/a/s.json")
    assert [str(p) for p in out] == ["/a/state/execution_recent_sell_guard.json",
                                     "/root/data/state/execution_recent_sell_guard.json"]


# ---- A28-5 _first_snapshot_call_payload ----
@pytest.mark.parametrize("snapshot,api", [
    ({}, "a"), ({"calls": None}, "a"), ({"calls": ["x", 1, None]}, "a"),
    ({"calls": [{"api_id": "b", "payload": {"n": 1}}, {"api_id": " a ", "payload": {"n": 2}}, {"api_id": "a", "payload": {"n": 3}}]}, "a"),
    ({"calls": [{"api_id": "a", "payload": [1]}, {"api_id": "a", "payload": {"n": 9}}]}, "a"),
    ({"calls": [{"api_id": "a"}]}, "a"), ({"calls": [{"api_id": "a", "payload": {}}]}, "z"),
])
def test_first_snapshot_call_payload(orig_nodes, monkeypatch, guards, snapshot, api):
    check(orig_nodes, monkeypatch, "_first_snapshot_call_payload", snapshot, api)


# ---- A28-6 _price_matches ----
NUMS = [None, 0, -1, 1.0, 100.0, 100.05, 100.5, 1000.0, 1000.9, 1001.1, 2.0, 2.9, 3.1, float("nan"), float("inf"), "x", "10", True]


@pytest.mark.parametrize("left", NUMS)
@pytest.mark.parametrize("right", [None, 0, 1.0, 100.0, 100.9, 1000.0, 1001.0, float("nan"), float("inf"), "x"])
def test_price_matches(orig_nodes, monkeypatch, guards, left, right):
    check(orig_nodes, monkeypatch, "_price_matches", left, right)


def test_price_matches_tolerance_and_safe_float_patch(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_price_matches", 1000.0, 1001.0) is True  # 0.1% -> 1.0 absolute floor
    assert check(orig_nodes, monkeypatch, "_price_matches", 1000000.0, 1000999.0) is True
    assert check(orig_nodes, monkeypatch, "_price_matches", 1000000.0, 1001001.0) is False
    assert check(orig_nodes, monkeypatch, "_price_matches", 5, 5, overrides={"_safe_float": lambda v: None}) is False
    assert check(orig_nodes, monkeypatch, "_price_matches", 1, 99, overrides={"_safe_float": lambda v: 50.0}) is True


# ---- A28-8 _trade_dir_for_row ----
@pytest.mark.parametrize("row", [
    {}, {"trade_root_path": "/explicit"}, {"trade_root_path": "/bad"}, {"trade_id": "T1"}, {"date": "2026-04-16"},
    {"trade_id": "T1", "date": "2026-04-16"}, {"trade_id": "T1", "day": "2026-04-16T10:00"},
    {"trade_root_path": "/bad", "trade_id": "T1", "date": "2026-04-16"},
])
@pytest.mark.parametrize("hit", [None, "/found/T1"])
@pytest.mark.parametrize("fallback_exists", [False, True])
def test_trade_dir_for_row(orig_nodes, monkeypatch, guards, row, hit, fallback_exists):
    r = _Resolver(hit)
    existing_dirs = {"/explicit"}

    def fake_exists(self):
        s = str(self)
        return s in existing_dirs or (fallback_exists and "/trades/" in s)

    monkeypatch.setattr(Path, "exists", fake_exists)
    monkeypatch.setattr(Path, "is_dir", lambda self: str(self) in existing_dirs)
    check(orig_nodes, monkeypatch, "_trade_dir_for_row", row, Path("/reports"),
          overrides={"find_trade_dir": r.find, "canonical_trade_day_root": lambda root, day: Path(root) / "CANON" / day})


# ---- structure ----
@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(ops, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    owner_fn = getattr(OWNERS[name], name)
    assert len(list(ast.walk(ast.parse(inspect.getsource(owner_fn)).body[0]))) > 20
    assert owner_fn.__module__ == OWNERS[name].__name__
    assert "operator_period_summary import" not in inspect.getsource(OWNERS[name]).replace("operator_period_summary_", "")
