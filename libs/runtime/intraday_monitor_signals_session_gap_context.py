from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _session_gap_context(candles: Sequence[Mapping[str, Any]], current_close: float, *, facade: Any):
    context: Dict[str, Any] = {
        "session_context_available": False,
        "session_open": None,
        "previous_close": None,
        "open_gap_pct": None,
        "prev_close_distance_pct": None,
        "minutes_since_session_open": None,
    }
    _latest_key, start_idx, _latest_minute = facade._current_kst_session_anchor(candles)
    if start_idx is None:
        return context
    first = candles[start_idx]
    prior = candles[start_idx - 1] if start_idx > 0 else {}
    session_open = facade._to_float(first.get("open"), facade._to_float(first.get("close")))
    previous_close = facade._to_float(prior.get("close"))
    first_ts = facade._to_int(first.get("ts"), 0)
    last_ts = facade._to_int(candles[-1].get("ts"), 0)
    minutes_since_open = None
    if first_ts > 0 and last_ts >= first_ts:
        minutes_since_open = round(float(last_ts - first_ts) / 60.0, 3)
    open_gap_pct = None
    if previous_close > 0.0 and session_open > 0.0:
        open_gap_pct = (session_open / previous_close) - 1.0
    prev_close_distance_pct = None
    if previous_close > 0.0 and current_close > 0.0:
        prev_close_distance_pct = (current_close / previous_close) - 1.0
    context.update(
        {
            "session_context_available": bool(previous_close > 0.0 and session_open > 0.0),
            "session_open": session_open if session_open > 0.0 else None,
            "previous_close": previous_close if previous_close > 0.0 else None,
            "open_gap_pct": open_gap_pct,
            "prev_close_distance_pct": prev_close_distance_pct,
            "minutes_since_session_open": minutes_since_open,
        }
    )
    return context
