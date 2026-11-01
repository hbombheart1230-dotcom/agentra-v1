"""operator_period_summary: ``_runtime_activity_payload`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _runtime_activity_payload(
    *,
    reports_root: Path,
    day: str,
    source_payload: Dict[str, Any],
    facade: Any,
) -> Dict[str, Any]:
    explicit_runtime_keys = {
        "events",
        "approvals",
        "blocks",
        "symbols_observed",
        "generated_symbol_report_count",
    }
    q9_path = (
        facade.Path(reports_root)
        / "operator_summary"
        / "daily"
        / day
        / "q9_decision_windows.json"
    )
    # Streamed one window at a time: only the three filter ids and `commander_final`'s
    # decision/monitor_intent are read, and the file is ~120 MB (see json_array_stream).
    q9_window_count = 0
    decisions: list[str] = []
    monitor_intents: list[str] = []
    try:
        for row in facade.iter_json_array(q9_path, "windows"):
            if not isinstance(row, dict):
                continue
            if any(
                marker in " ".join(
                    str(row.get(key) or "").lower()
                    for key in ("decision_id", "run_id", "candidate_pool_id")
                )
                for marker in ("test", "fixture", "synthetic")
            ):
                continue
            q9_window_count += 1
            commander_final = row.get("commander_final")
            if isinstance(commander_final, dict):
                decisions.append(str(commander_final.get("decision") or "").strip().lower())
                monitor_intents.append(str(commander_final.get("monitor_intent") or "").strip().upper())
    except ValueError:
        q9_window_count, decisions, monitor_intents = 0, [], []  # unreadable file == no windows (as _read_json did)
    if q9_window_count:
        return {
            "source": "q9_decision_windows",
            "source_path": str(q9_path),
            "events": q9_window_count,
            "commander_decision_count": len(decisions),
            "missing_commander_decision_count": max(0, q9_window_count - len(decisions)),
            "approvals": sum(value in {"approve", "approved", "allow"} for value in decisions),
            "blocks": sum(value in {"reject", "blocked", "veto"} for value in decisions),
            "noops": sum(value in {"noop", "no_trade"} for value in decisions),
            "monitor_buy_count": sum(value == "BUY" for value in monitor_intents),
            "monitor_noop_count": sum(value == "NOOP" for value in monitor_intents),
            "symbols_observed_count": 0,
            "generated_symbol_report_count": 0,
        }

    if source_payload and any(key in source_payload for key in explicit_runtime_keys):
        return {
            "source": "daily_report_payload",
            "events": facade._safe_int(source_payload.get("events")),
            "approvals": facade._safe_int(source_payload.get("approvals")),
            "blocks": facade._safe_int(source_payload.get("blocks")),
            "symbols_observed_count": len(list(source_payload.get("symbols_observed") or [])),
            "generated_symbol_report_count": facade._safe_int(source_payload.get("generated_symbol_report_count")),
        }

    live_payload, live_path = facade._latest_live_summary_payload(reports_root, day)
    if not live_payload:
        return {
            "source": "not_available",
            "events": 0,
            "approvals": 0,
            "blocks": 0,
            "symbols_observed_count": 0,
            "generated_symbol_report_count": 0,
        }

    events = live_payload.get("events") if isinstance(live_payload.get("events"), dict) else {}
    execution = live_payload.get("execution") if isinstance(live_payload.get("execution"), dict) else {}
    return {
        "source": "live_summary_fallback",
        "source_path": live_path,
        "lookback_min": facade._safe_int(live_payload.get("lookback_min")),
        "events": facade._safe_int(events.get("window_total")),
        "events_scanned_total": facade._safe_int(events.get("scanned_total")),
        "approvals": facade._safe_int(execution.get("allowed_total")),
        "blocks": facade._safe_int(execution.get("blocked_total")),
        "executed_total": facade._safe_int(execution.get("executed_total")),
        "broker_fail_total": facade._safe_int(execution.get("executed_broker_fail_total")),
        "symbols_observed_count": 0,
        "generated_symbol_report_count": 0,
    }
