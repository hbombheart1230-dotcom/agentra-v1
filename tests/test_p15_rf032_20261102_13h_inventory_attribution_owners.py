"""RF-032 A37-1..8: seven ``artifact_inventory`` + one ``attribution_score_v0`` bodies, original vs wrappers + Owners.

Pure/fake only; no UEF/validation-id writer is touched. Originals: A preimage 7d1bc3ed (artifact_inventory e444c7af,
attribution_score_v0 adf75adc); canonical 5d79fd29 has the same blobs. AST-extracted and compiled in a copy of the
live namespace; dependency overrides apply to both sides. ``Path.exists`` / ``rglob`` / ``glob`` are faked where the
original uses them; ``read_json`` / ``iter_json_array`` / forward-outcome loaders are fakes. Streaming is checked
by pulling from a counting generator. No real file access, sockets, subprocess or writes.
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

A_PRE = "7d1bc3edfa3f5c12c19f385c038d80d235032afe"
CANON = "5d79fd29a90d6e9ce631da17d9a6ad1f08dbf691"
EV = "libs/reporting/evaluation/"
FILES = {
    "inv": (EV + "artifact_inventory.py", "e444c7af5ac8775d4a5b664a98a0c57c7a7fcee0", "artifact_inventory",
            ["_iter_shadow_payloads", "load_q9_pre_strategist_rows", "_load_forward_recovery_candles", "inventory_trade",
             "build_artifact_inventory", "_q9_daily_diagnostics", "iter_trade_dirs"]),
    "v0": (EV + "attribution_score_v0.py", "adf75adc0f9e67cbc0114042e616552b6cac94f3", "attribution_score_v0", ["build_attribution_score_v0"]),
}
MODS = {k: importlib.import_module(f"libs.reporting.evaluation.{v[2]}") for k, v in FILES.items()}
CASES = [(k, n) for k, v in FILES.items() for n in v[3]]
OWNERS = {(k, n): importlib.import_module(f"libs.reporting.evaluation.{FILES[k][2]}_{n}") for k, n in CASES}


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    nodes = {}
    for key, (path, blob, _stem, names) in FILES.items():
        try:
            a_raw = subprocess.run(["git", "show", f"{A_PRE}:{path}"], check=True, capture_output=True).stdout
            c_raw = subprocess.run(["git", "show", f"{CANON}:{path}"], check=True, capture_output=True).stdout
        except subprocess.CalledProcessError as exc:
            pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
        assert _sha(a_raw) == blob, f"BLOCKED_PIN actor blob {path}"
        assert _sha(c_raw) == blob, f"BLOCKED_PIN canonical blob {path}"
        tree = ast.parse(a_raw.decode("utf-8"))
        found = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names}
        assert sorted(found) == sorted(names)
        nodes[key] = found
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
        if any(c in str(mode) for c in "wax+") or str(file).replace("\\", "/").startswith(("/rep", "/fake", "/data")):
            raise AssertionError("open attempted")
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)


def check(orig_nodes, monkeypatch, key, name, *args, overrides=None, drain=False, mutates=False, **kwargs):
    mod = MODS[key]
    ns = dict(vars(mod))
    tree = ast.Module(body=[copy.deepcopy(orig_nodes[key][name])], type_ignores=[])
    exec(compile(ast.fix_missing_locations(tree), f"<{A_PRE[:8]}:{name}>", "exec"), ns)
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(mod, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[name]), ("new", getattr(mod, name))):
        a, k = copy.deepcopy((args, kwargs))
        try:
            out = fn(*a, **k)
            if drain:
                out = list(out)
            values[label] = out
            got[label] = ("ok", repr(out)) + ((repr((a, k)),) if mutates else ())
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        if not mutates:
            assert repr((a, k)) == repr((args, kwargs)), f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


# fake Path tree: shadow files under <reports_root>.parent/data/logs/quant_shadow_candidates/<day>
def _fake_glob_tree(monkeypatch, root_exists=True, names=()):
    seen = {"exists": [], "glob": []}
    monkeypatch.setattr(Path, "exists", lambda self: seen["exists"].append(str(self)) or root_exists)
    monkeypatch.setattr(Path, "glob", lambda self, pattern: seen["glob"].append((str(self), pattern)) or iter([self / n for n in names]))
    return seen


# ---- A37-1 _iter_shadow_payloads (streaming generator) ----
@pytest.mark.parametrize("root_exists,names,payloads", [
    (False, [], {}), (True, [], {}), (True, ["b.json", "a.json", "latest.json"], {"a.json": {"x": 1}, "b.json": {"y": 2}, "latest.json": {"z": 3}}),
    (True, ["a.json", "b.json"], {"a.json": {}, "b.json": {"k": 1}}), (True, ["a.json"], {}), (True, ["z.json", "a.json", "m.json"], {n: {"n": n} for n in ("z.json", "a.json", "m.json")}),
])
def test_iter_shadow_payloads(orig_nodes, monkeypatch, guards, root_exists, names, payloads):
    _fake_glob_tree(monkeypatch, root_exists, names)
    out = check(orig_nodes, monkeypatch, "inv", "_iter_shadow_payloads", Path("/rep/reports"), "D", drain=True,
                overrides={"read_json": lambda p: copy.deepcopy(payloads.get(Path(p).name, {}))})
    assert isinstance(out, list)


def test_iter_shadow_payloads_is_lazy_and_ordered(orig_nodes, monkeypatch, guards):
    reads = []
    _fake_glob_tree(monkeypatch, True, ["b.json", "a.json", "latest.json", "c.json"])
    ns_read = lambda p: reads.append(Path(p).name) or {"n": Path(p).name}  # noqa: E731
    monkeypatch.setattr(MODS["inv"], "read_json", ns_read)
    gen = MODS["inv"]._iter_shadow_payloads(Path("/rep/reports"), "D")
    assert inspect.isgenerator(gen) and reads == []  # nothing happens before iteration
    assert next(gen) == {"n": "a.json"} and reads == ["a.json"]  # one payload at a time, sorted, latest.json skipped
    assert list(gen) == [{"n": "b.json"}, {"n": "c.json"}] and reads == ["a.json", "b.json", "c.json"]
    assert inspect.isgeneratorfunction(MODS["inv"]._iter_shadow_payloads) and "Yield each non-empty shadow payload" in MODS["inv"]._iter_shadow_payloads.__doc__


# ---- A37-2 load_q9_pre_strategist_rows ----
ROLE = "P_SCANNER_PRE_STRATEGIST_UNIVERSE"


def _cand(**kw):
    base = {"q9_decision_role": ROLE, "symbol": "005930"}
    base.update(kw)
    return base


SHADOWS = [
    [], [{}], [{"generated_at": "2026-04-16T10:00:00+09:00", "q9_decision_candidates": [_cand()]}],
    [{"generated_at": "2026-04-16T10:00:00+09:00", "q9_decision_candidates": ["bad", {"q9_decision_role": "OTHER"}, {}, _cand(symbol="000660"), _cand(run_id="test-1")]}],
    [{"generated_at": "2026-04-16T16:00:00+09:00", "q9_decision_candidates": [_cand()]}],
    [{"q9_decision_candidates": [_cand(_payload_generated_at="keep")]}],
    [{"generated_at": "2026-04-16T09:30:00+09:00", "q9_decision_candidates": [_cand(symbol="A")]}, {"generated_at": "2026-04-16T11:00:00+09:00", "q9_decision_candidates": [_cand(symbol="B"), _cand(symbol="BAD")]}],
    [{"generated_at": "2026-04-16T10:00:00+09:00", "q9_decision_candidates": None}],
]


@pytest.mark.parametrize("shadows", SHADOWS)
def test_load_q9_pre_strategist_rows(orig_nodes, monkeypatch, guards, shadows):
    out = check(orig_nodes, monkeypatch, "inv", "load_q9_pre_strategist_rows", Path("/rep"), "D",
                overrides={"_iter_shadow_payloads": lambda r, d: iter(copy.deepcopy(shadows))})
    assert isinstance(out, list)


def test_load_q9_values_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "inv", "load_q9_pre_strategist_rows", Path("/rep"), "D",
                overrides={"_iter_shadow_payloads": lambda r, d: iter(copy.deepcopy(SHADOWS[3]))})
    assert [r["symbol"] for r in out] == ["000660"] and out[0]["_payload_generated_at"] == "2026-04-16T10:00:00+09:00"
    out = check(orig_nodes, monkeypatch, "inv", "load_q9_pre_strategist_rows", Path("/rep"), "D",
                overrides={"_iter_shadow_payloads": lambda r, d: iter(copy.deepcopy(SHADOWS[6])), "_synthetic_identity": lambda row: row["symbol"] == "BAD",
                           "_regular_session_window": lambda row: True})
    assert [r["symbol"] for r in out] == ["A", "B"]


# ---- A37-3 _load_forward_recovery_candles ----
RECOVERY = [{}, {"minute_rows_by_symbol": None}, {"minute_rows_by_symbol": "bad"}, {"minute_rows_by_symbol": {}},
            {"minute_rows_by_symbol": {"005930": [{"ts": 1}, "bad", {"ts": 2}], "000660": "notalist", "X": [], 5: [{"a": 1}]}},
            {"minute_rows_by_symbol": {"B": [{"n": {"deep": 1}}], "A": [{"n": 2}]}}]


@pytest.mark.parametrize("payload", RECOVERY)
def test_load_forward_recovery_candles(orig_nodes, monkeypatch, guards, payload):
    seen = []
    out = check(orig_nodes, monkeypatch, "inv", "_load_forward_recovery_candles", Path("/rep"), "D",
                overrides={"read_json": lambda p: seen.append(str(p)) or copy.deepcopy(payload)})
    assert seen[0] == str(Path("/rep/evaluation/daily/D/q9_forward_recovery_candles.json")) and len(seen) == 2
    assert isinstance(out, dict) and all(isinstance(k, str) for k in out)


def test_forward_recovery_copy_semantics(monkeypatch, guards):
    nested = {"deep": 1}
    src = {"minute_rows_by_symbol": {"B": [{"n": nested}], "A": []}}
    monkeypatch.setattr(MODS["inv"], "read_json", lambda p: src)
    out = MODS["inv"]._load_forward_recovery_candles(Path("/rep"), "D")
    assert list(out) == ["B", "A"] and out["B"][0] is not src["minute_rows_by_symbol"]["B"][0] and out["B"][0]["n"] is nested


# ---- A37-4 inventory_trade ----
class _Rec:
    def __init__(self, existing):
        self.existing, self.calls = set(existing), []

    def __call__(self, path, *, required):
        self.calls.append((str(path), required))
        return {"path": str(path), "required": required, "exists": Path(path).name in self.existing or str(path) in self.existing}


@pytest.mark.parametrize("existing", [set(), {"lifecycle_bundle.json", "entry.json"}, {"lifecycle_bundle.json", "entry.json", "scanner_evidence.json", "strategist_evidence.json",
                                                                                        "commander_evidence.json", "monitor_evidence.json"},
                                      {"exit.json", "ai_trade_summary.json"}])
def test_inventory_trade(orig_nodes, monkeypatch, guards, existing):
    rec = _Rec(existing)
    out = check(orig_nodes, monkeypatch, "inv", "inventory_trade", Path("/rep/trades/D/TRD_1"), overrides={"_record": rec})
    names = ["lifecycle_bundle", "entry", "exit", "scanner_evidence", "strategist_evidence", "commander_evidence", "monitor_evidence", "ai_trade_summary", "post_exit_shadow"]
    assert list(out["artifacts"]) == names and out["trade_id"] == "TRD_1" and len(rec.calls) == 18  # 9 per side
    assert [c[1] for c in rec.calls[:9]] == [True, True, False, True, True, True, True, False, False]
    assert out["complete"] is (not out["missing_required"])


# ---- A37-5 build_artifact_inventory ----
def _inv_overrides(trade_dirs, existing_daily=(), trade_missing=()):
    rec_calls = []

    def _record(path, *, required):
        rec_calls.append((str(path), required))
        return {"path": str(path), "required": required, "exists": Path(path).name in set(existing_daily)}

    def inventory_trade(path):
        return {"trade_id": Path(path).name, "artifacts": {"a": {"required": True, "exists": Path(path).name not in trade_missing},
                                                            "b": {"required": False, "exists": False}}}
    return {"iter_trade_dirs": lambda root, day: list(trade_dirs), "inventory_trade": inventory_trade, "_record": _record,
            "_q9_daily_diagnostics": lambda root, day, record: {**record, "diag": True}}


@pytest.mark.parametrize("trade_dirs,existing_daily,missing", [
    ([], (), ()), ([], ("daily_summary.json", "q8_shadow_blocker_review.json"), ()), ([Path("/t/T1")], (), ()), ([Path("/t/T1"), Path("/t/T2")], ("daily_summary.json",), ("T2",)),
    ([Path("/t/T1")], ("daily_summary.json", "q8_shadow_blocker_review.json", "operator_summary.json"), ()),
])
def test_build_artifact_inventory(orig_nodes, monkeypatch, guards, trade_dirs, existing_daily, missing):
    out = check(orig_nodes, monkeypatch, "inv", "build_artifact_inventory", Path("/rep"), "D", overrides=_inv_overrides(trade_dirs, existing_daily, missing))
    assert list(out)[:3] == ["schema_version", "day", "trade_count"] and 0.0 <= out["required_coverage"] <= 1.0
    assert list(out["daily_artifacts"]) == ["daily_summary", "operator_summary", "q8_shadow_blocker_review", "closeout_maintenance", "q9_decision_windows", "q9_vs_samsung_hynix_comparison"]


def test_build_inventory_values(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "inv", "build_artifact_inventory", Path("/rep"), "D", overrides=_inv_overrides([], ("daily_summary.json", "q8_shadow_blocker_review.json")))
    assert out["required_artifact_count"] == 2 and out["present_required_artifact_count"] == 2 and out["required_coverage"] == 1.0
    out = check(orig_nodes, monkeypatch, "inv", "build_artifact_inventory", Path("/rep"), "D", overrides=_inv_overrides([Path("/t/T1")]))
    assert out["required_artifact_count"] == 3 and out["present_required_artifact_count"] == 1 and out["required_coverage"] == 0.3333
    assert out["daily_artifacts"]["q9_decision_windows"]["diag"] is True  # replaced by the diagnostics seam


# ---- A37-6 build_attribution_score_v0 ----
def _v0_overrides(statuses):
    def mk(name):
        status, score = statuses[name]
        return lambda *a, **k: {"status": status, "score": score, "reasons": [name], "evidence": {}}
    return {"_ledger_day_record": lambda root, day: {"evidence_status": "COMPLETE", "day": day},
            "_selection_integrity": mk("sel"), "_scanner_alignment": mk("scan"), "_entry_timing": mk("entry"), "_exit_horizon": mk("exit"),
            "_evidence_quality": mk("ev")}


STAT = [
    {"sel": ("OK", 90), "scan": ("OK", 70), "entry": ("OK", 35), "exit": ("OK", 80), "ev": ("OK", 10)},
    {"sel": ("INSUFFICIENT_EVIDENCE", None), "scan": ("INSUFFICIENT_EVIDENCE", None), "entry": ("INSUFFICIENT_EVIDENCE", None), "exit": ("INSUFFICIENT_EVIDENCE", None), "ev": ("OK", 50)},
    {"sel": ("OK", 60), "scan": ("OK", 60), "entry": ("OK", 60), "exit": ("OK", 60), "ev": ("OK", 5)},
    {"sel": ("OK", None), "scan": ("OK", 0), "entry": ("OK", 100), "exit": ("INSUFFICIENT_EVIDENCE", 5), "ev": ("INSUFFICIENT_EVIDENCE", None)},
]


@pytest.mark.parametrize("statuses", STAT)
def test_build_attribution_score_v0(orig_nodes, monkeypatch, guards, statuses):
    out = check(orig_nodes, monkeypatch, "v0", "build_attribution_score_v0", day="2026-04-16", reports_root=Path("/rep"), models=[{"trade_id": "T"}],
                daily_scorecard={"a": 1}, selection_authority={"rows": []}, horizon_compliance={}, entry_timing={}, overrides=_v0_overrides(statuses))
    assert list(out) == ["schema_version", "evaluation_program_id", "behavior_effect", "day", "scores", "weakest_observed_axis", "interpretation_rule", "limitations"]
    assert list(out["scores"]) == ["selection_integrity_score", "scanner_alignment_score", "entry_timing_score", "exit_horizon_score", "evidence_quality_score"]


def test_build_v0_weakest_and_seams(orig_nodes, monkeypatch, guards):
    kw = dict(day="d", reports_root=Path("/rep"), models=[], daily_scorecard={}, selection_authority={}, horizon_compliance={}, entry_timing={})
    out = check(orig_nodes, monkeypatch, "v0", "build_attribution_score_v0", **kw, overrides=_v0_overrides(STAT[0]))
    assert out["weakest_observed_axis"] == {"name": "entry_timing_score", "score": 35}  # evidence quality (10) is excluded
    out = check(orig_nodes, monkeypatch, "v0", "build_attribution_score_v0", **kw, overrides=_v0_overrides(STAT[1]))
    assert out["weakest_observed_axis"] == {"name": "", "score": None}
    out = check(orig_nodes, monkeypatch, "v0", "build_attribution_score_v0", **kw, overrides={**_v0_overrides(STAT[3]), "INSUFFICIENT": "NOPE"})
    assert out["weakest_observed_axis"]["name"] in {"scanner_alignment_score", "exit_horizon_score"}  # constant read from the facade at call time


# ---- A37-7 _q9_daily_diagnostics ----
def _w(gen="2026-04-16T10:00:00+09:00", **kw):
    row = {"scanner_control": {"c": 1}, "generated_at": gen}
    row.update(kw)
    return row


WINDOWS = [
    [], ["bad", 5, None], [{"no_control": 1}],
    [_w(), _w("2026-04-16T09:05:00+09:00", strategist_selection={"selected_symbol": "005930"}, commander_final={"d": 1}, scanner_pre_strategist_universe={"intrinsic_ranked_top20": [1]})],
    [_w(run_id="test-1"), _w("2026-04-16T16:00:00+09:00"), _w("2026-04-16T15:20:00+09:00")],
    [_w(strategist_selection={"post_strategist_top10": [1], "selected_symbol": ""}), _w(strategist_selection={"post_strategist_top10": [1], "selected_symbol": "X"})],
    [_w("2026-04-16T09:00:00+09:00", scanner_pre_strategist_universe={"intrinsic_ranked_top20": []}), _w("2026-04-16T15:30:00+09:00", strategist_selection={}, commander_final={})],
    [_w("bad-timestamp"), _w(None)],
]


def _q9_overrides(windows, raises=None, shadows=(), pre_rows=(), candles=None, outcomes=None, closeout=None, window_exists=True):
    seen = {"iter": [], "exists": []}

    def iter_json_array(path, key, **kw):
        seen["iter"].append((str(path), key, kw))
        if raises is not None:
            raise raises
        for r in windows:
            yield copy.deepcopy(r)

    def attach(rows, *, minute_rows_by_symbol=None):
        out = []
        for i, r in enumerate(rows):
            r = dict(r)
            if outcomes and i < len(outcomes):
                r["shadow_forward_outcome"] = copy.deepcopy(outcomes[i])
            out.append(r)
        return out
    ov = {"iter_json_array": iter_json_array, "_iter_shadow_payloads": lambda root, day: iter(copy.deepcopy(list(shadows))),
          "load_q9_pre_strategist_rows": lambda root, day: copy.deepcopy(list(pre_rows)), "_load_forward_recovery_candles": lambda root, day: copy.deepcopy(candles or {}),
          "attach_forward_outcomes": attach, "read_json": lambda p: copy.deepcopy(closeout or {})}
    return ov, seen, window_exists


@pytest.mark.parametrize("windows", WINDOWS)
def test_q9_daily_diagnostics_windows(orig_nodes, monkeypatch, guards, windows):
    ov, seen, exists = _q9_overrides(windows)
    monkeypatch.setattr(Path, "exists", lambda self: exists)
    out = check(orig_nodes, monkeypatch, "inv", "_q9_daily_diagnostics", Path("/rep"), "D", {"path": "/rep/q9_decision_windows.json", "exists": True}, overrides=ov, mutates=True)
    assert out["window_count"] == sum(1 for w in windows if isinstance(w, dict))
    assert all(call[1] == "windows" and call[2] == {"strict": True} for call in seen["iter"])


def test_q9_daily_diagnostics_classification_values(orig_nodes, monkeypatch, guards):
    ov, _, _ = _q9_overrides(WINDOWS[4] + WINDOWS[3])
    monkeypatch.setattr(Path, "exists", lambda self: True)
    out = check(orig_nodes, monkeypatch, "inv", "_q9_daily_diagnostics", Path("/rep"), "D", {"path": "/rep/w.json"}, overrides=ov, mutates=True)
    assert (out["window_count"], out["synthetic_window_count"], out["post_session_window_count"], out["scanner_selection_window_count"]) == (5, 1, 1, 3)
    assert out["complete_abc_window_count"] == 1 and out["complete_pabc_window_count"] == 1 and out["pre_strategist_universe_window_count"] == 1
    assert out["first_scanner_window_kst"].startswith("2026-04-16T09:05:00") and out["last_scanner_window_kst"].startswith("2026-04-16T15:20:00")


@pytest.mark.parametrize("raises", [OSError("fake io"), ValueError("fake bad json")])
def test_q9_daily_diagnostics_unreadable_window_file(orig_nodes, monkeypatch, guards, raises):
    ov, _, _ = _q9_overrides(WINDOWS[3], raises=raises)
    monkeypatch.setattr(Path, "exists", lambda self: True)
    out = check(orig_nodes, monkeypatch, "inv", "_q9_daily_diagnostics", Path("/rep"), "D", {"path": "/rep/w.json"}, overrides=ov, mutates=True)
    assert out["window_count"] == 0 and out["scanner_selection_window_count"] == 0 and out["first_scanner_window_kst"] == ""


def test_q9_daily_diagnostics_missing_window_file_and_streaming_args(orig_nodes, monkeypatch, guards):
    ov, seen, _ = _q9_overrides(WINDOWS[3])
    monkeypatch.setattr(Path, "exists", lambda self: False)
    out = check(orig_nodes, monkeypatch, "inv", "_q9_daily_diagnostics", Path("/rep"), "D", {"path": "/rep/w.json"}, overrides=ov, mutates=True)
    assert out["window_count"] == 0 and seen["iter"] == []
    out = check(orig_nodes, monkeypatch, "inv", "_q9_daily_diagnostics", Path("/rep"), "D", {}, overrides=ov, mutates=True)  # path falls back to Path("")
    assert out["window_count"] == 0


SHADOW = [{"generated_at": "2026-04-16T10:00:00+09:00", "q9_decision_candidates": [{"a": 1}]}, {"generated_at": "2026-04-16T15:20:00+09:00"},
          {"generated_at": "2026-04-16T15:25:00+09:00", "q9_decision_candidates": [{"b": 1}]}]
OUTCOMES = [{"available": True}, {"available": False, "reason": "forward_window_pending", "checkpoints": {"+5m": {"status": "pending"}}},
            {"available": False, "reason": "minute_rows_unavailable", "checkpoints": {"+5m": {"status": "missing"}}},
            {"available": False, "reason": "weird", "checkpoints": {"+5m": {"status": "observed"}, "+15m": {"status": "pending"}}}, {"available": False}]


def test_q9_daily_diagnostics_shadow_forward_and_closeout(orig_nodes, monkeypatch, guards):
    closeout = {"ok": True, "trigger": "kiwoom_market_status_x", "steps": {"account_snapshot": {"ok": True}, "closeout_residual_position_reconciliation": {"ok": True}}}
    ov, _, _ = _q9_overrides(WINDOWS[3], shadows=SHADOW, pre_rows=[{"i": i} for i in range(5)], candles={"005930": [{"ts": 1}]}, outcomes=OUTCOMES, closeout=closeout)
    monkeypatch.setattr(Path, "exists", lambda self: True)
    out = check(orig_nodes, monkeypatch, "inv", "_q9_daily_diagnostics", Path("/rep"), "D", {"path": "/rep/w.json"}, overrides=ov, mutates=True)
    assert out["shadow_payload_count"] == 3 and out["pre_strategist_forward_candidate_count"] == 5 and out["forward_observed_candidate_count"] == 1
    assert out["forward_pending_candidate_count"] == 2 and out["forward_unavailable_candidate_count"] == 1 and out["forward_invalid_candidate_count"] == 1
    assert out["post_close_account_snapshot_ok"] is True and out["post_close_trigger"] == "kiwoom_market_status_x"
    assert out["last_q9_runtime_evidence_kst"].startswith("2026-04-16T15:25:00") and out["late_session_runtime_evidence"] is True
    assert out["forward_recovery_artifact_used"] is True and out["forward_outcome_reason_counts"] == {"forward_window_pending": 1, "minute_rows_unavailable": 1, "weird": 1, "checkpoint_status_only": 1}
    assert out["forward_outcome_status_signature_counts"]["NO_CHECKPOINT_STATUS"] == 1 and out["full_session_coverage"] is True and out["post_close_account_snapshot_coverage"] is True


def test_q9_daily_diagnostics_non_dict_outcome_error_parity(orig_nodes, monkeypatch, guards):
    ov, _, _ = _q9_overrides(WINDOWS[3], pre_rows=[{"i": 0}], outcomes=["bad"])
    monkeypatch.setattr(Path, "exists", lambda self: True)
    out = check(orig_nodes, monkeypatch, "inv", "_q9_daily_diagnostics", Path("/rep"), "D", {"path": "/rep/w.json"}, overrides=ov, mutates=True)
    assert out[0] == "err" and out[1] == "AttributeError"


@pytest.mark.parametrize("closeout", [{}, {"ok": True, "trigger": "manual", "steps": {}}, {"ok": True, "trigger": "manual", "steps": {"account_snapshot": {"ok": True}, "closeout_residual_position_reconciliation": {"ok": True}}},
                                      {"ok": True, "trigger": "manual", "steps": {"account_snapshot": {"ok": True}, "closeout_residual_position_reconciliation": {"ok": True, "requires_next_open_flatten": True}}}, {"steps": "bad"}])
def test_q9_daily_diagnostics_closeout_variants(orig_nodes, monkeypatch, guards, closeout):
    ov, _, _ = _q9_overrides([_w("2026-04-16T09:05:00+09:00")], shadows=[{"generated_at": "2026-04-16T15:20:00+09:00", "q9_decision_candidates": [1]}], closeout=closeout)
    monkeypatch.setattr(Path, "exists", lambda self: True)
    check(orig_nodes, monkeypatch, "inv", "_q9_daily_diagnostics", Path("/rep"), "D", {"path": "/rep/w.json"}, overrides=ov, mutates=True)


def test_q9_daily_diagnostics_mutates_and_returns_same_record(monkeypatch, guards):
    ov, _, _ = _q9_overrides([])
    for k, v in ov.items():
        monkeypatch.setattr(MODS["inv"], k, v)
    monkeypatch.setattr(Path, "exists", lambda self: False)
    record = {"path": "/rep/w.json"}
    assert MODS["inv"]._q9_daily_diagnostics(Path("/rep"), "D", record) is record and record["window_count"] == 0


# ---- A37-8 iter_trade_dirs ----
@pytest.mark.parametrize("exists,found", [
    (False, []), (True, []), (True, ["TRD_2/lifecycle_bundle.json", "TRD_1/lifecycle_bundle.json"]), (True, ["TRD_1/lifecycle_bundle.json", "TRD_1/lifecycle_bundle.json"]),
    (True, ["A/TRD_9/lifecycle_bundle.json", "B/TRD_1/lifecycle_bundle.json", "A/TRD_9/lifecycle_bundle.json"]),
])
def test_iter_trade_dirs(orig_nodes, monkeypatch, guards, exists, found):
    seen = []
    monkeypatch.setattr(Path, "exists", lambda self: seen.append(str(self)) or exists)
    monkeypatch.setattr(Path, "rglob", lambda self, pattern: iter([self / f for f in found]) if pattern == "lifecycle_bundle.json" else iter([]))
    out = check(orig_nodes, monkeypatch, "inv", "iter_trade_dirs", Path("/rep"), "D")
    assert out == (sorted({(Path("/rep/trades/D") / f).parent for f in found}) if exists else [])
    assert seen[: len(seen) // 2] == seen[len(seen) // 2:] == [str(Path("/rep/trades/D"))]


# ---- structure ----
@pytest.mark.parametrize("key,name", CASES)
def test_wrapper_thin_and_owner_holds_body(key, name):
    wrapper = ast.parse(inspect.getsource(getattr(MODS[key], name))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]  # docstring allowed
    assert len(stmts) == 1
    if inspect.isgeneratorfunction(getattr(MODS[key], name)):
        assert isinstance(stmts[0], ast.Expr) and isinstance(stmts[0].value, ast.YieldFrom)
        call = stmts[0].value.value
    else:
        assert isinstance(stmts[0], ast.Return)
        call = stmts[0].value
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[(key, name)], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[(key, name)].__name__
    stem = FILES[key][2]
    src = inspect.getsource(OWNERS[(key, name)]).replace(f"{stem}_", "")
    assert f"{stem} import" not in src and f"import {stem}" not in src
