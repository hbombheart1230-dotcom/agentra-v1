from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _compress_candles(rows: Sequence[Mapping[str, Any]], timeframe_minutes: int, *, facade: Any):
    candles = facade._candles_from_rows(rows)
    bucket = max(1, int(timeframe_minutes or 1))
    if bucket <= 1 or len(candles) <= 1:
        return candles
    out: List[Dict[str, Any]] = []
    chunk: List[Mapping[str, Any]] = []
    for row in candles:
        chunk.append(row)
        if len(chunk) >= bucket:
            merged = facade._merge_candle_group(chunk)
            if merged:
                out.append(merged)
            chunk = []
    if chunk:
        merged = facade._merge_candle_group(chunk)
        if merged:
            out.append(merged)
    return out
