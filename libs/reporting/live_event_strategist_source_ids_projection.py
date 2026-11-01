"""live_execution_event_evidence projections (moved verbatim from live_execution_event_evidence).

Module globals and helpers are resolved on ``facade`` (the live_execution_event_evidence module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List, Tuple


def resolve_strategist_source_run_ids(
    *,
    event_rows: List[Dict[str, Any]],
    lifecycle: Dict[str, Any],
    facade: Any,
) -> Tuple[List[str], Dict[str, str]]:
    lifecycle_run_ids = [str(x or "").strip() for x in list(lifecycle.get("run_ids_all") or []) if str(x or "").strip()]
    if not lifecycle_run_ids:
        return [], {}

    strategist_event_names = {
        "strategist.market_context_snapshot",
        "strategist.global_sentiment_breakdown",
        "strategist.news_evidence_ranked",
        "strategist.decision_frame",
        "strategist.llm_response_saved",
    }
    strategist_run_ids = {
        str(row.get("run_id") or "").strip()
        for row in event_rows
        if str(row.get("run_id") or "").strip() in set(lifecycle_run_ids)
        and str(row.get("agent") or row.get("stage") or "").strip().lower() == "strategist"
        and facade.row_event_name(row) in strategist_event_names
    }

    strategist_frame_rows = [
        row
        for row in event_rows
        if str(row.get("agent") or row.get("stage") or "").strip().lower() == "strategist"
        and facade.row_event_name(row) == "strategist.decision_frame"
    ]
    strategist_frame_rows.sort(key=lambda row: facade.to_epoch(row.get("ts")) or 0)

    linked_cached_frames: Dict[str, str] = {}
    for run_id in lifecycle_run_ids:
        if run_id in strategist_run_ids:
            continue
        fast_path_rows = [
            row
            for row in event_rows
            if str(row.get("run_id") or "").strip() == run_id
            and facade.row_event_name(row) == "commander_router.fast_path"
        ]
        if not fast_path_rows:
            continue
        fast_path = fast_path_rows[-1]
        payload = fast_path.get("payload") if isinstance(fast_path.get("payload"), dict) else {}
        if str(payload.get("path") or "").strip() != "integrated_chain_cached_frame":
            continue
        target_ts = facade.to_epoch(fast_path.get("ts")) or 0
        reuse_sec = max(30, facade.safe_int(payload.get("reuse_sec"), 180))
        candidate_rows = [
            row
            for row in strategist_frame_rows
            if str(row.get("run_id") or "").strip() != run_id
            and (facade.to_epoch(row.get("ts")) or 0) <= target_ts
            and target_ts - (facade.to_epoch(row.get("ts")) or 0) <= reuse_sec + 30
        ]
        if not candidate_rows:
            continue
        source_run_id = str(candidate_rows[-1].get("run_id") or "").strip()
        if not source_run_id:
            continue
        strategist_run_ids.add(source_run_id)
        linked_cached_frames[run_id] = source_run_id

    return sorted(strategist_run_ids), linked_cached_frames
