"""Pure candle follow-up projection owner for monitor gate diagnostics."""
from __future__ import annotations

from typing import Any, Dict, List


def _followup_from_rows(case: Dict[str, Any], rows: List[Dict[str, Any]], *, facade: Any) -> Dict[str, Any]:
    latest_candle_ts = int(case.get("latest_candle_ts") or 0)
    blocked_price = facade._to_float(case.get("current_price"))
    breakout_level = facade._to_float(case.get("breakout_level"))
    reclaim_price = facade._to_float(case.get("reclaim_price"))
    later = [row for row in rows if int(row.get("ts") or 0) > latest_candle_ts]
    if not later or blocked_price in (None, 0.0):
        return {"later_bars": 0}
    max_high = max(facade._to_float(row.get("high")) or 0.0 for row in later)
    min_low = min(facade._to_float(row.get("low")) or 0.0 for row in later)
    last_close = facade._to_float(later[-1].get("close"))
    return {
        "later_bars": len(later),
        "max_high_after": max_high,
        "min_low_after": min_low,
        "last_close_now": last_close,
        "move_to_max_pct": ((max_high / blocked_price) - 1.0) * 100.0 if max_high > 0 else None,
        "move_to_min_pct": ((min_low / blocked_price) - 1.0) * 100.0 if min_low > 0 else None,
        "move_to_last_pct": ((last_close / blocked_price) - 1.0) * 100.0 if last_close else None,
        "crossed_breakout_after": bool(breakout_level and max_high >= breakout_level),
        "crossed_reclaim_after": bool(reclaim_price and max_high >= reclaim_price),
    }
