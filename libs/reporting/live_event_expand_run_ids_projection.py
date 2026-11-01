"""live_execution_event_evidence projections (moved verbatim from live_execution_event_evidence).

Module globals and helpers are resolved on ``facade`` (the live_execution_event_evidence module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Set


def expand_targeted_run_ids_with_cached_strategist_sources(
    *,
    event_rows: List[Dict[str, Any]],
    targeted_run_ids: Iterable[str],
    facade: Any,
) -> Set[str]:
    out: Set[str] = {
        str(run_id or "").strip()
        for run_id in list(targeted_run_ids or [])
        if str(run_id or "").strip()
    }
    if not out:
        return out

    strategist_frame_rows = [
        row
        for row in list(event_rows or [])
        if str(row.get("agent") or row.get("stage") or "").strip().lower() == "strategist"
        and facade.row_event_name(row) == "strategist.decision_frame"
    ]
    strategist_frame_rows.sort(key=lambda row: facade.to_epoch(row.get("ts")) or 0)
    if not strategist_frame_rows:
        return out

    fast_path_rows = [
        row
        for row in list(event_rows or [])
        if str(row.get("run_id") or "").strip() in out
        and facade.row_event_name(row) == "commander_router.fast_path"
    ]
    for fast_path in fast_path_rows:
        payload = fast_path.get("payload") if isinstance(fast_path.get("payload"), dict) else {}
        if str(payload.get("path") or "").strip() != "integrated_chain_cached_frame":
            continue
        target_run_id = str(fast_path.get("run_id") or "").strip()
        target_ts = facade.to_epoch(fast_path.get("ts")) or 0
        reuse_sec = max(30, facade.safe_int(payload.get("reuse_sec"), 180))
        candidate_rows = [
            row
            for row in strategist_frame_rows
            if str(row.get("run_id") or "").strip() != target_run_id
            and (facade.to_epoch(row.get("ts")) or 0) <= target_ts
            and target_ts - (facade.to_epoch(row.get("ts")) or 0) <= reuse_sec + 30
        ]
        if not candidate_rows:
            continue
        source_run_id = str(candidate_rows[-1].get("run_id") or "").strip()
        if source_run_id:
            out.add(source_run_id)
    return out
