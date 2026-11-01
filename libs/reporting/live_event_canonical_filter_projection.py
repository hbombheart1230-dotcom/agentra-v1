"""live_execution_event_evidence projections (moved verbatim from live_execution_event_evidence).

Module globals and helpers are resolved on ``facade`` (the live_execution_event_evidence module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List


def filter_canonical_events(
    rows: List[Dict[str, Any]],
    *,
    run_ids: List[str],
    agent: str,
    event_names: List[str],
    facade: Any,
) -> List[Dict[str, Any]]:
    run_set = {str(item or "").strip() for item in list(run_ids or []) if str(item or "").strip()}
    names = {str(item or "").strip() for item in list(event_names or []) if str(item or "").strip()}
    out: List[Dict[str, Any]] = []
    for row in rows:
        if run_set and str(row.get("run_id") or "").strip() not in run_set:
            continue
        row_agent = str(row.get("agent") or row.get("stage") or "").strip().lower()
        if row_agent != str(agent or "").strip().lower():
            continue
        if names and facade.row_event_name(row) not in names:
            continue
        out.append(
            {
                "ts": str(row.get("ts") or ""),
                "event_name": facade.row_event_name(row),
                "level": str(row.get("level") or "info"),
                "run_id": str(row.get("run_id") or ""),
                "trade_id": str(row.get("trade_id") or ""),
                "session_id": str(row.get("session_id") or ""),
                "cycle_id": str(row.get("cycle_id") or ""),
                "agent": str(row.get("agent") or row.get("stage") or ""),
                "phase": str(row.get("phase") or ""),
                "symbol": str(row.get("symbol") or ""),
                "payload": dict(row.get("payload") or {}) if isinstance(row.get("payload"), dict) else {},
            }
        )
    out.sort(key=lambda item: facade.to_epoch(item.get("ts")) or 0)
    return out
