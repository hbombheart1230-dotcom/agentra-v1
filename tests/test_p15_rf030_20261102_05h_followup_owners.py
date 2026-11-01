"""RF-030 A29-1..8: two operator_visibility + six operator_period_summary bodies, original vs thin wrappers + Owners.

Visibility originals: A preimage 2f92f2b8 blob 03649403; their function text must equal canonical blob 54905c2d.
Period originals: A preimage 2f92f2b8 blob 389e0299 (canonical identical). Originals compile in a copy of the live
module namespace; dependency overrides apply to both sides. Everything is fake/temp; no real Q9 stream, no writes.
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

A_PRE = "2f92f2b803427be61de96253937962994566d84e"
VIS_PATH, VIS_A_BLOB, VIS_CANON_BLOB = "libs/reporting/operator_visibility.py", "0364940365a003ebcf7aa8c534a88a461a6899b6", "54905c2dfe82f8b0a50d97490cc790f7aa6188f8"
PER_PATH, PER_BLOB = "libs/reporting/operator_period_summary.py", "389e0299bd4ce331e410f200d83d4d744b544c4f"
VIS = ["_build_trading_health_status", "_operator_brief_trade_model_is_valid"]
PER = ["_safe_float", "_same_day_flatten_reconciliation", "_daily_symbol_history_rows", "_runtime_activity_payload",
       "_first_recursive_dict", "_first_nonempty_list"]
ov = importlib.import_module("libs.reporting.operator_visibility")
ops = importlib.import_module("libs.reporting.operator_period_summary")
MODS = {**{n: ov for n in VIS}, **{n: ops for n in PER}}
STEM = {**{n: "operator_visibility" for n in VIS}, **{n: "operator_period_summary" for n in PER}}
OWNERS = {n: importlib.import_module(f"libs.reporting.{STEM[n]}_{n.lstrip('_')}") for n in VIS + PER}


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


def _show(commit, path):
    return subprocess.run(["git", "show", f"{commit}:{path}"], check=True, capture_output=True).stdout


def _nodes(raw, names):
    tree = ast.parse(raw.decode("utf-8"))
    found = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names}
    assert sorted(found) == sorted(names)
    return found


@pytest.fixture(scope="module")
def orig_nodes():
    try:
        vis_a, per = _show(A_PRE, VIS_PATH), _show(A_PRE, PER_PATH)
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(vis_a) == VIS_A_BLOB and _sha(per) == PER_BLOB, "BLOCKED_PIN"
    nodes = {**_nodes(vis_a, VIS), **_nodes(per, PER)}
    # canonical text equality for the two visibility functions (canonical blob 54905c2d is fetched from origin)
    try:
        canon = subprocess.run(["git", "cat-file", "blob", VIS_CANON_BLOB], check=True, capture_output=True).stdout
    except subprocess.CalledProcessError:
        pytest.fail("BLOCKED_PIN: canonical blob 54905c2d not present locally (git fetch origin integration/p1.5)")
    assert _sha(canon) == VIS_CANON_BLOB
    cn = _nodes(canon, VIS)
    for n in VIS:
        assert ast.get_source_segment(vis_a.decode(), nodes[n]) == ast.get_source_segment(canon.decode(), cn[n]), \
            f"HOLD: {n} differs actor vs canonical"
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
    mod = MODS[name]
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


def jtable(table):
    seen = []

    def _read_json(path):
        seen.append(str(path))
        return copy.deepcopy(table.get(str(path), {}))
    _read_json.seen = seen
    return _read_json


# ---- A29-1 _build_trading_health_status ----
SUMMARY = "/rep/performance/2026-04-16/summary.json"


@pytest.mark.parametrize("summary", [
    {}, {"x": 1}, {"return_sample_count": 0, "total_trades": 5}, {"return_sample_count": 1, "win_rate": 0.1, "avg_return": -0.05},
    {"return_sample_count": 2, "win_rate": 0.39, "avg_return": 0.01}, {"return_sample_count": 2, "win_rate": 0.40, "avg_return": 0.01},
    {"return_sample_count": 3, "win_rate": 0.24, "avg_return": 0.02}, {"return_sample_count": 3, "win_rate": 0.25, "avg_return": 0.02},
    {"return_sample_count": 3, "win_rate": 0.9, "avg_return": -0.008}, {"return_sample_count": 3, "win_rate": 0.9, "avg_return": -0.0079},
    {"return_sample_count": 5, "win_rate": 0.6, "avg_return": 0.02, "profit_factor": 1.8, "total_trades": 7},
    {"return_sample_count": "bad", "win_rate": "x", "avg_return": None}, {"return_sample_count": 4, "win_rate": 0.5, "avg_return": -0.001},
])
@pytest.mark.parametrize("day", ["2026-04-16", " 2026-04-16 ", None, ""])
def test_build_trading_health_status(orig_nodes, monkeypatch, guards, summary, day):
    table = {SUMMARY: summary, "/rep/performance/2026-04-16/summary.json": summary}
    check(orig_nodes, monkeypatch, "_build_trading_health_status", Path("/rep"), day, overrides={"_read_json": jtable(table)})


def test_trading_health_levels_and_seams(orig_nodes, monkeypatch, guards):
    def level(summary):
        return check(orig_nodes, monkeypatch, "_build_trading_health_status", Path("/rep"), "2026-04-16",
                     overrides={"_read_json": jtable({SUMMARY: summary})})["trading_health_level"]
    assert level({}) == "UNKNOWN" and level({"return_sample_count": 0}) == "UNKNOWN"
    assert level({"return_sample_count": 3, "win_rate": 0.2, "avg_return": 0.0}) == "RED"
    assert level({"return_sample_count": 2, "win_rate": 0.3, "avg_return": 0.01}) == "YELLOW"
    assert level({"return_sample_count": 4, "win_rate": 0.6, "avg_return": 0.02}) == "GREEN"
    out = check(orig_nodes, monkeypatch, "_build_trading_health_status", Path("/rep"), "2026-04-16",
                overrides={"_read_json": lambda p: {"x": 1}, "_safe_int": lambda v, d=0: 9, "_safe_float": lambda v, d=0.0: 0.5})
    assert out["sample_count"] == 9 and out["win_rate"] == 0.5 and out["trading_health_level"] == "GREEN"


# ---- A29-2 _operator_brief_trade_model_is_valid ----
@pytest.mark.parametrize("model", [None, {}, [], "x", {"facts": {"a": 1}}, {"provenance": {"b": 1}}, {"facts": {"a": 1}, "provenance": {"b": 1}},
                                   {"facts": [1], "provenance": {"b": 1}}, {"facts": {}, "provenance": {"b": 1}}, {"facts": {"a": 1}, "provenance": "x"}])
def test_operator_brief_trade_model_is_valid(orig_nodes, monkeypatch, guards, model):
    check(orig_nodes, monkeypatch, "_operator_brief_trade_model_is_valid", model)


# ---- A29-3 _safe_float ----
@pytest.mark.parametrize("value", [None, "", 0, 1, 1.5, "2.5", " 3 ", "abc", float("nan"), float("inf"), "-inf", "nan", [1], {}, True, "1e3"])
def test_safe_float(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_safe_float", value)


# ---- A29-4 _same_day_flatten_reconciliation ----
def _bundle(entry_qty=10, exit_qty=10, price=1000.0, action="SELL", trade_id="TRD1"):
    return {"trade_id": trade_id, "entry": {"qty": entry_qty, "price": price},
            "exit": {"action": action, "qty": exit_qty, "reason_human": "사유", "ts": "2026-04-16T10:00:00"}}


def _flatten(monkeypatch, paths, table, exists=True):
    monkeypatch.setattr(Path, "exists", lambda self: exists)
    seen = []
    monkeypatch.setattr(Path, "rglob", lambda self, pattern: (seen.append(pattern) or iter([Path(p) for p in paths])))
    return seen, {"_read_json": jtable(table)}


KW = dict(reports_root=Path("/rep"), day="2026-04-16", symbol="005930", qty=10, avg_price=1000.0)


@pytest.mark.parametrize("override", [{"day": None}, {"day": " "}, {"symbol": ""}, {"qty": 0}, {"qty": -1}, {}])
def test_flatten_guards_and_empty(orig_nodes, monkeypatch, guards, override):
    _, ov_ = _flatten(monkeypatch, [], {})
    check(orig_nodes, monkeypatch, "_same_day_flatten_reconciliation", **{**KW, **override}, overrides=ov_)


def test_flatten_absent_day_root(orig_nodes, monkeypatch, guards):
    _, ov_ = _flatten(monkeypatch, ["/rep/trades/2026-04-16/TRD_x/lifecycle_bundle.json"], {}, exists=False)
    assert check(orig_nodes, monkeypatch, "_same_day_flatten_reconciliation", **KW, overrides=ov_) == {}


P1, P2, P3 = (f"/rep/trades/2026-04-16/TRD_20260416_005930_{i}/lifecycle_bundle.json" for i in (3, 1, 2))


@pytest.mark.parametrize("table", [
    {}, {P1: _bundle(action="BUY")}, {P1: _bundle(entry_qty=5)}, {P1: _bundle(exit_qty=5)}, {P1: _bundle(price=2000.0)},
    {P1: _bundle(trade_id="A"), P2: _bundle(trade_id="B"), P3: _bundle(trade_id="C")},
    {P1: ["not a dict"], P2: _bundle(trade_id="ok")}, {P2: {"entry": "x", "exit": "y"}},
])
@pytest.mark.parametrize("avg", [1000.0, None, "bad", 1000.5])
def test_flatten_bundles(orig_nodes, monkeypatch, guards, table, avg):
    seen, ov_ = _flatten(monkeypatch, [P1, P2, P3], table)
    out = check(orig_nodes, monkeypatch, "_same_day_flatten_reconciliation", **{**KW, "avg_price": avg}, overrides=ov_)
    assert seen and seen[-1] == "TRD_20260416_005930_*/lifecycle_bundle.json"
    if out:
        assert out["reason"] == "same_day_lifecycle_full_sell_after_flatten_decision"


def test_flatten_sorted_path_order_and_price_seam(orig_nodes, monkeypatch, guards):
    seen, ov_ = _flatten(monkeypatch, [P1, P2, P3], {P1: _bundle(trade_id="A"), P2: _bundle(trade_id="B"), P3: _bundle(trade_id="C")})
    out = check(orig_nodes, monkeypatch, "_same_day_flatten_reconciliation", **KW, overrides=ov_)
    assert out["lifecycle_bundle_path"] == P2 and out["trade_id"] == "B"  # sorted() picks the lowest path
    ov_["_price_matches"] = lambda a, b: False
    assert check(orig_nodes, monkeypatch, "_same_day_flatten_reconciliation", **KW, overrides=ov_) == {}


# ---- A29-5 _daily_symbol_history_rows ----
def _hist(rows):
    return lambda reports_root: iter(rows)  # one-shot generator semantics


@pytest.mark.parametrize("rows,day", [
    ([], "2026-04-16"),
    ([{"date": "2026-04-16", "n": 1}, {"date": "2026-04-15", "n": 2}, {"date": " 2026-04-16 ", "n": 3}, {"n": 4}, {"date": None}], "2026-04-16"),
    ([{"date": "2026-04-16", "n": 1}], " 2026-04-16 "), ([{"date": ""}], None), ([{"date": "bad"}, {"date": "2026-04-16"}], "2026-04-16"),
])
def test_daily_symbol_history_rows(orig_nodes, monkeypatch, guards, rows, day):
    check(orig_nodes, monkeypatch, "_daily_symbol_history_rows", Path("/rep"), day,
          overrides={"_iter_symbol_trade_history": _hist(rows)})


# ---- A29-6 _runtime_activity_payload ----
Q9_PATH = "/rep/operator_summary/daily/2026-04-16/q9_decision_windows.json"


def _q9(rows=None, raises=None):
    seen = []

    def iter_json_array(path, key):
        seen.append((str(path), key))
        if raises:
            raise raises
        for r in rows or []:
            yield copy.deepcopy(r)
    iter_json_array.seen = seen
    return iter_json_array


def _win(decision=None, intent=None, **ids):
    row = dict(ids)
    if decision is not None or intent is not None:
        row["commander_final"] = {"decision": decision, "monitor_intent": intent}
    return row


LIVE = ({"lookback_min": "60", "events": {"window_total": 11, "scanned_total": 99},
         "execution": {"allowed_total": 4, "blocked_total": 2, "executed_total": 3, "executed_broker_fail_total": 1}}, "/live/summary.json")


@pytest.mark.parametrize("rows,raises,source,live", [
    ([], None, {}, ({}, "")),
    ([], None, {"events": 3, "approvals": 2, "blocks": 1, "symbols_observed": ["a", "b"], "generated_symbol_report_count": "4"}, ({}, "")),
    ([], None, {"unrelated": 1}, LIVE), ([], None, {}, LIVE), ([], None, {}, ({"events": "bad", "execution": 5}, "/live/x.json")),
    ([_win("APPROVE", "buy", decision_id="d1"), _win("Reject", "noop", run_id="r1"), _win("no_trade", "BUY"), _win(), "bad", None], None, {}, ({}, "")),
    ([_win("approve", "buy", decision_id="TEST-1"), _win("approve", "buy", run_id="my_fixture"), _win("veto", "x", candidate_pool_id="Synthetic")], None, {}, ({}, "")),
    ([_win("approved", "buy", decision_id="ok"), {"commander_final": "str"}, {"commander_final": {"decision": None}}], None, {"events": 9}, LIVE),
    ([_win("allow", "BUY")], ValueError("unreadable"), {"events": 5}, ({}, "")),
])
def test_runtime_activity_payload(orig_nodes, monkeypatch, guards, rows, raises, source, live):
    it = _q9(rows, raises)
    out = check(orig_nodes, monkeypatch, "_runtime_activity_payload", reports_root=Path("/rep"), day="2026-04-16",
                source_payload=source, overrides={"iter_json_array": it, "_latest_live_summary_payload": lambda root, day: live})
    assert it.seen and it.seen[-1] == (Q9_PATH, "windows")
    assert out["source"] in {"q9_decision_windows", "daily_report_payload", "live_summary_fallback", "not_available"}


def test_runtime_activity_q9_counts_and_key_order(orig_nodes, monkeypatch, guards):
    rows = [_win("approve", "buy", decision_id="d1"), _win("reject", "noop", decision_id="d2"), _win("noop", "buy", decision_id="d3"),
            _win(decision_id="d4"), _win("approve", "buy", decision_id="test-5")]
    out = check(orig_nodes, monkeypatch, "_runtime_activity_payload", reports_root=Path("/rep"), day="2026-04-16",
                source_payload={}, overrides={"iter_json_array": _q9(rows), "_latest_live_summary_payload": lambda r, d: ({}, "")})
    assert list(out) == ["source", "source_path", "events", "commander_decision_count", "missing_commander_decision_count",
                         "approvals", "blocks", "noops", "monitor_buy_count", "monitor_noop_count",
                         "symbols_observed_count", "generated_symbol_report_count"]
    assert (out["events"], out["commander_decision_count"], out["missing_commander_decision_count"]) == (4, 3, 1)
    assert (out["approvals"], out["blocks"], out["noops"], out["monitor_buy_count"], out["monitor_noop_count"]) == (1, 1, 1, 2, 1)


def test_runtime_activity_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_runtime_activity_payload", reports_root=Path("/rep"), day="2026-04-16",
                source_payload={"events": 1}, overrides={"iter_json_array": _q9([]), "_safe_int": lambda v, d=0: 77})
    assert out["events"] == 77 and out["source"] == "daily_report_payload"


# ---- A29-7 _first_recursive_dict ----
def _find(root, key):
    return root.get(key) if isinstance(root, dict) else None


@pytest.mark.parametrize("roots,key", [
    ((), "k"), (({},), "k"), (({"k": {}},), "k"), (({"k": {"a": 1}},), "k"), (({"k": {}}, {"k": {"b": 2}}, {"k": {"c": 3}}), "k"),
    (({"k": [1]}, "str", None, {"k": {"z": 0}}), "k"), (({"x": {"k": {"deep": 1}}},), "k"),
])
def test_first_recursive_dict(orig_nodes, monkeypatch, guards, roots, key):
    check(orig_nodes, monkeypatch, "_first_recursive_dict", *roots, key=key, overrides={"_find_key_recursive": _find})


def test_first_recursive_dict_real_helper_and_copy(orig_nodes, monkeypatch, guards):
    src = {"k": {"a": [1]}}
    out = check(orig_nodes, monkeypatch, "_first_recursive_dict", {"x": 1}, {"y": src}, key="k")
    assert out == {"a": [1]} and out is not src["k"]
    calls = []
    out = check(orig_nodes, monkeypatch, "_first_recursive_dict", {"n": 1}, key="k",
                overrides={"_find_key_recursive": lambda r, k: calls.append((r, k)) or {"patched": 1}})
    assert out == {"patched": 1} and calls == [({"n": 1}, "k")] * 2  # once per side (original, wrapper)


# ---- A29-8 _first_nonempty_list ----
@pytest.mark.parametrize("value", [None, "abc", {"a": 1}, (1,), [], ["", "  ", None], ["a", " b ", "", "c"], ["한글", " é "], [0, False, 1, "0"], [1.5, None, [], {}]])
def test_first_nonempty_list(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_first_nonempty_list", value)


def test_first_nonempty_list_values(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_first_nonempty_list", ["a", " b ", "", None, "c"]) == ["a", "b", "c"]
    assert check(orig_nodes, monkeypatch, "_first_nonempty_list", [0, False]) == []  # falsy items are dropped


# ---- structure ----
@pytest.mark.parametrize("name", VIS + PER)
def test_wrapper_thin_and_owner_holds_body(name):
    mod = MODS[name]
    wrapper = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    owner_fn = getattr(OWNERS[name], name)
    assert len(list(ast.walk(ast.parse(inspect.getsource(owner_fn)).body[0]))) > 15
    assert owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name]).replace(f"{STEM[name]}_", "")
    assert f"{STEM[name]} import" not in src and f"import {STEM[name]}" not in src
