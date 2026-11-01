from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _session_vwap(candles: Sequence[Mapping[str, Any]], *, facade: Any):
    source_rows = facade._current_kst_session_rows(candles) or list(candles or [])
    weighted_num = 0.0
    weighted_den = 0.0
    for row in source_rows:
        volume = max(0.0, facade._to_float(row.get("volume")))
        if volume <= 0.0:
            continue
        vwap = facade._to_float(row.get("vwap"))
        if vwap <= 0.0:
            high_px = facade._to_float(row.get("high"))
            low_px = facade._to_float(row.get("low"))
            close_px = facade._to_float(row.get("close"))
            vwap = (high_px + low_px + close_px) / 3.0
        if vwap <= 0.0:
            continue
        weighted_num += vwap * volume
        weighted_den += volume
    if weighted_den <= 0.0:
        return None
    return weighted_num / weighted_den
