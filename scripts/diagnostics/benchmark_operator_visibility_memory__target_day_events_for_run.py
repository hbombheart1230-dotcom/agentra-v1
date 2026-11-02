from __future__ import annotations
from typing import Any, Dict

def _target_day_events_for_run(day: str, run_idx: int, sec_offset: int, facade: Any) -> list[Dict[str, Any]]:
    """A realistic-shaped RUN for the target day -- one run_id producing
    the same multi-event sequence a real commander tick actually emits
    (decision -> router -> scanner -> monitor -> execute_from_packet, plus
    a couple of skill calls in between), not one row per run_id. A real
    production day has many rows per run, not one row = one run; an
    earlier version of this benchmark used 1 row per run_id, which
    overstated day-size memory scaling by inflating the distinct-run-id
    count (and therefore the by_run accumulator's own size) far beyond
    what a real trading day produces."""
    run_id = f"benchday-run-{run_idx:06d}"

    def _ts(k: int) -> str:
        total = sec_offset + k
        return f"{day}T{(total // 3600) % 24:02d}:{(total // 60) % 60:02d}:{total % 60:02d}+00:00"

    return [
        {"run_id": run_id, "ts": _ts(0), "stage": "skill_execute", "event": "call",
         "payload": {"skill": "market.minute_ohlcv", "api_id": "ka10080", "step": 0, "path": "/api/dostk/chart"}},
        {"run_id": run_id, "ts": _ts(1), "stage": "skill_result", "event": "ok",
         "payload": {"skill": "market.minute_ohlcv", "outputs": "MinuteOHLCVDTO"}},
        {"run_id": run_id, "ts": _ts(2), "stage": "decision", "event": "trace",
         "payload": {"decision_packet": {"intent": {"action": "BUY", "symbol": "005930", "qty": 1, "reason": "entry"}}}},
        {"run_id": run_id, "ts": _ts(3), "stage": "commander_router", "event": "route_selected",
         "payload": {"route_selected": "full_cycle"}},
        {"run_id": run_id, "ts": _ts(4), "stage": "scanner", "event": "candidate_selection_reason",
         "payload": {"selected_symbol": "005930", "score_total": 0.7}},
        {"run_id": run_id, "ts": _ts(5), "stage": "monitor", "event": "entry_decision_detail",
         "payload": {"no_trade_surface": {"no_trade_stage": "guard_block", "dominant_blocker": "spread_too_wide"}}},
        {"run_id": run_id, "ts": _ts(6), "stage": "execute_from_packet", "event": "verdict",
         "payload": {"allowed": False, "reason": "blocked_by_guard"}},
    ]
