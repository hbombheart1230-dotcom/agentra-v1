from pathlib import Path

from scripts.diagnostics import check_trade_report_runtime_regression as runtime
from scripts.diagnostics import trade_artifact_validation_evidence_projection as owner


_NAMES = ("entry_json", "hold_json", "exit_json", "lifecycle_bundle_json", "ai_trade_report_input_json", "ai_trade_report_json", "ai_trade_report_md")


def _context(tmp_path: Path, *, complete: bool = False, open_conflict: bool = False):
    paths = {name: tmp_path / name for name in _NAMES}
    if complete:
        for path in paths.values(): path.write_text("x")
    status = "open" if open_conflict else "closed"
    return {"trade_paths": paths, "entry_payload": {"run_id":"run-buy", "ts":"2026-04-16T00:07:45+00:00", "action":"BUY", "symbol":"000660", "qty":1, "reason_human":"selected"}, "exit_payload": {} if open_conflict else {"run_id":"run-sell", "ts":"2026-04-16T00:08:47+00:00", "action":"SELL", "symbol":"000660", "reason_human":"peak_drawdown"}, "hold_payload": {"hold_duration":"1.0m", "hold_duration_sec":62}, "lifecycle_bundle": {"trade_lifecycle_status":status, "linked_run_ids":[] if open_conflict else ["run-buy", "run-sell"], "lifecycle_completeness":"partial", "same_day_reporter_linkage":{"status":"missing", "reporter_analysis_json_path":"", "reporter_analysis_md_path":""}}, "story_input": {"symbol":"000660", "selected_symbol":"000660", "selected_rank":1, "candidate_count":5, "status":"closed", "action":"SELL"}, "report": {"generation":{"status":"ok"}, "section_provenance":{"market_context_at_entry":{"source":"canonical"}}}, "provenance": {"lifecycle_status":status}, "health": {}}


def test_absent_artifacts_facade_equals_owner(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime, "_resolve_trade_context", lambda *_: _context(tmp_path))
    facade = runtime.validate_trade_artifact_chain(tmp_path, "2026-04-16", "t")
    direct = owner.validate_trade_artifact_chain(tmp_path, "2026-04-16", "t", facade=runtime)
    assert facade == direct and facade["ok"] is False
    assert facade["failures"][:7] == [f"missing_artifact:{name}" for name in _NAMES]


def test_complete_closed_fixture_is_internal_parity(monkeypatch, tmp_path: Path):
    monkeypatch.setattr(runtime, "_resolve_trade_context", lambda *_: _context(tmp_path, complete=True))
    facade = runtime.validate_trade_artifact_chain(tmp_path, "2026-04-16", "t")
    direct = owner.validate_trade_artifact_chain(tmp_path, "2026-04-16", "t", facade=runtime)
    assert facade == direct
    assert facade["ok"] is True and facade["failures"] == [] and facade["warnings"] == []
    assert facade["entry_run_id"] == "run-buy" and facade["selected_rank"] == 1


def test_open_conflict_order_and_call_time_facade(monkeypatch, tmp_path: Path):
    calls = []
    monkeypatch.setattr(runtime, "_resolve_trade_context", lambda *_: calls.append("context") or _context(tmp_path, complete=True, open_conflict=True))
    original_safe_int = runtime._safe_int
    monkeypatch.setattr(runtime, "_safe_int", lambda value, default=0: calls.append("safe") or original_safe_int(value, default))
    monkeypatch.setattr(runtime, "_run_python_json", lambda *_a, **_k: (_ for _ in ()).throw(AssertionError("subprocess path used")))
    facade = runtime.validate_trade_artifact_chain(tmp_path, "2026-04-16", "t")
    direct = owner.validate_trade_artifact_chain(tmp_path, "2026-04-16", "t", facade=runtime)
    expected = ["story_input_status_conflicts_with_authoritative_status", "story_input_action_conflicts_with_open_trade"]
    assert facade == direct and facade["failures"] == expected
    assert "context" in calls and "safe" in calls
