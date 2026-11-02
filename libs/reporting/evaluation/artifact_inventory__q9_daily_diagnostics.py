"""artifact_inventory: ``_q9_daily_diagnostics`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _q9_daily_diagnostics(reports_root: Path, day: str, record: dict[str, Any], *, facade: Any) -> dict[str, Any]:
    path = facade.Path(record.get("path") or "")
    # The ~120 MB windows file is streamed one window at a time; each window is classified
    # (synthetic / post-session / trusted scanner window) and only the counts and trusted windows'
    # generated_at survive. Holding every parsed window (and the whole-file text) was a major part of
    # the closeout peak. `row not in synthetic_windows` was an equality test, so identical windows
    # always classify identically and per-window flags give the same sets.
    window_count = synthetic_count = post_session_count = trusted_count = 0
    abc_count = pabc_count = pre_universe_count = missing_selected_count = 0
    trusted_window_times: list[Any] = []
    if path.exists():
        try:
            for row in facade.iter_json_array(path, "windows", strict=True):
                if not isinstance(row, dict):
                    continue
                window_count += 1
                if not isinstance(row.get("scanner_control"), dict):
                    continue
                if facade._synthetic_identity(row):
                    synthetic_count += 1
                    continue
                if not facade._regular_session_window(row):
                    post_session_count += 1
                    continue
                trusted_count += 1
                parsed_time = facade._parse_window_kst(row.get("generated_at"))
                if parsed_time is not None:
                    trusted_window_times.append(parsed_time)
                strategist = row.get("strategist_selection")
                commander = row.get("commander_final")
                universe = row.get("scanner_pre_strategist_universe")
                if isinstance(strategist, dict) and isinstance(commander, dict):
                    abc_count += 1
                    if isinstance(universe, dict):
                        pabc_count += 1
                if isinstance(universe, dict) and bool(universe.get("intrinsic_ranked_top20")):
                    pre_universe_count += 1
                if bool((strategist or {}).get("post_strategist_top10")) and not str(
                    (strategist or {}).get("selected_symbol") or ""
                ):
                    missing_selected_count += 1
        except (OSError, ValueError):
            # unreadable windows file == no windows (what read_json -> {} gave)
            window_count = synthetic_count = post_session_count = trusted_count = 0
            abc_count = pabc_count = pre_universe_count = missing_selected_count = 0
            trusted_window_times = []
    # Only the payload count and the generated_at of payloads that carry q9 decision
    # candidates are needed below, so reduce each payload to that as it streams past.
    shadow_payload_count = 0
    shadow_times = []
    for shadow in facade._iter_shadow_payloads(reports_root, day):
        shadow_payload_count += 1
        if shadow.get("q9_decision_candidates"):
            parsed = facade._parse_window_kst(shadow.get("generated_at"))
            if parsed is not None:
                shadow_times.append(parsed)
    pre_rows = facade.load_q9_pre_strategist_rows(reports_root, day)
    recovery_candles = facade._load_forward_recovery_candles(reports_root, day)
    observed_rows = (
        facade.attach_forward_outcomes(
            pre_rows,
            minute_rows_by_symbol=recovery_candles or None,
        )
        if pre_rows
        else []
    )
    forward_observed = sum(
        1
        for row in observed_rows
        if bool((row.get("shadow_forward_outcome") or {}).get("available"))
    )
    forward_pending = 0
    forward_unavailable = 0
    forward_invalid = 0
    forward_reason_counts: facade.Counter[str] = facade.Counter()
    forward_status_signature_counts: facade.Counter[str] = facade.Counter()
    for row in observed_rows:
        outcome = row.get("shadow_forward_outcome")
        outcome = outcome if isinstance(outcome, dict) else {}
        if outcome.get("available"):
            continue
        reason = str(outcome.get("reason") or "")
        forward_reason_counts[reason or "checkpoint_status_only"] += 1
        checkpoints = outcome.get("checkpoints")
        checkpoints = checkpoints if isinstance(checkpoints, dict) else {}
        statuses = {
            str(checkpoint.get("status") or "")
            for checkpoint in checkpoints.values()
            if isinstance(checkpoint, dict)
        }
        signature = "+".join(sorted(statuses)) or "NO_CHECKPOINT_STATUS"
        forward_status_signature_counts[signature] += 1
        if reason in {"", "forward_window_pending"} and statuses <= {"", "pending"}:
            forward_pending += 1
        elif reason in {
            "baseline_or_minute_rows_unavailable",
            "baseline_unavailable",
            "minute_rows_unavailable",
        }:
            forward_unavailable += 1
        else:
            forward_invalid += 1
    window_times = trusted_window_times
    first_window = min(window_times) if window_times else None
    last_window = max(window_times) if window_times else None
    last_runtime_evidence = max(window_times + shadow_times) if (window_times or shadow_times) else None
    closeout = facade.read_json(facade.Path(reports_root) / "operator_summary" / "daily" / day / "closeout_maintenance.json")
    closeout_steps = closeout.get("steps") if isinstance(closeout.get("steps"), dict) else {}
    residual = closeout_steps.get("closeout_residual_position_reconciliation")
    residual = residual if isinstance(residual, dict) else {}
    account_snapshot = closeout_steps.get("account_snapshot")
    account_snapshot = account_snapshot if isinstance(account_snapshot, dict) else {}
    post_close_account_ok = bool(
        closeout.get("ok")
        and account_snapshot.get("ok")
        and residual.get("ok")
        and not residual.get("requires_next_open_flatten")
    )
    late_session_runtime_evidence = bool(
        last_runtime_evidence
        and (last_runtime_evidence.hour, last_runtime_evidence.minute) >= (15, 10)
    )
    closeout_trigger = str(closeout.get("trigger") or "")
    closeout_trigger_ok = bool(
        closeout_trigger.startswith("kiwoom_market_status_")
        or (
            closeout_trigger
            and post_close_account_ok
            and late_session_runtime_evidence
        )
    )
    time_coverage_ok = bool(
        first_window
        and last_runtime_evidence
        and (first_window.hour, first_window.minute) <= (9, 10)
        and late_session_runtime_evidence
    )
    post_close_override = bool(
        first_window
        and (first_window.hour, first_window.minute) <= (9, 10)
        and post_close_account_ok
        and closeout_trigger_ok
    )
    record.update(
        {
            "expected_schema_version": facade.Q9_DECISION_SCHEMA,
            "schema_match": bool(record.get("schema_version") == facade.Q9_DECISION_SCHEMA),
            "window_count": window_count,
            "scanner_selection_window_count": trusted_count,
            "complete_abc_window_count": abc_count,
            "complete_pabc_window_count": pabc_count,
            "pre_strategist_universe_window_count": pre_universe_count,
            "missing_selected_candidate_count": missing_selected_count,
            "synthetic_window_count": synthetic_count,
            "post_session_window_count": post_session_count,
            "first_scanner_window_kst": first_window.isoformat() if first_window else "",
            "last_scanner_window_kst": last_window.isoformat() if last_window else "",
            "last_q9_runtime_evidence_kst": (
                last_runtime_evidence.isoformat() if last_runtime_evidence else ""
            ),
            "session_coverage_source": (
                "post_close_account_snapshot_override"
                if post_close_override and not time_coverage_ok
                else
                "scanner_selection_plus_q9_shadow_runtime"
                if last_runtime_evidence and last_runtime_evidence != last_window
                else "scanner_selection"
            ),
            "full_session_coverage": bool(time_coverage_ok or post_close_override),
            "post_close_account_snapshot_coverage": bool(post_close_override),
            "post_close_account_snapshot_ok": bool(post_close_account_ok),
            "post_close_trigger": closeout_trigger,
            "late_session_runtime_evidence": bool(late_session_runtime_evidence),
            "shadow_payload_count": shadow_payload_count,
            "pre_strategist_forward_candidate_count": len(pre_rows),
            "forward_observed_candidate_count": forward_observed,
            "forward_missing_candidate_count": max(0, len(pre_rows) - forward_observed),
            "forward_pending_candidate_count": forward_pending,
            "forward_unavailable_candidate_count": forward_unavailable,
            "forward_invalid_candidate_count": forward_invalid,
            "forward_outcome_reason_counts": dict(forward_reason_counts),
            "forward_outcome_status_signature_counts": dict(
                forward_status_signature_counts
            ),
            "forward_recovery_artifact_used": bool(recovery_candles),
        }
    )
    return record
