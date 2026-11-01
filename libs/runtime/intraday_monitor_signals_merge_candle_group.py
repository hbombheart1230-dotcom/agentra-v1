from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _merge_candle_group(group: Sequence[Mapping[str, Any]], *, facade: Any):
    rows = [row for row in group if isinstance(row, Mapping)]
    if not rows:
        return {}
    open_px = facade._to_float(rows[0].get("open"))
    close_px = facade._to_float(rows[-1].get("close"))
    high_px = max(facade._to_float(row.get("high"), close_px) for row in rows)
    low_px = min(facade._to_float(row.get("low"), open_px if open_px > 0.0 else close_px) for row in rows)
    volume = sum(max(0.0, facade._to_float(row.get("volume"))) for row in rows)
    weighted_vwap_num = 0.0
    weighted_vwap_den = 0.0
    for row in rows:
        row_volume = max(0.0, facade._to_float(row.get("volume")))
        row_vwap = facade._to_float(row.get("vwap"))
        if row_volume > 0.0 and row_vwap > 0.0:
            weighted_vwap_num += row_vwap * row_volume
            weighted_vwap_den += row_volume
    merged: Dict[str, Any] = {
        "ts": rows[-1].get("ts"),
        "open": open_px or close_px,
        "high": high_px,
        "low": low_px,
        "close": close_px or open_px,
        "volume": volume,
    }
    if weighted_vwap_den > 0.0:
        merged["vwap"] = weighted_vwap_num / weighted_vwap_den
    return merged
