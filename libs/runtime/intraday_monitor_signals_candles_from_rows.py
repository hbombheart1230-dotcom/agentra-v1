from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _candles_from_rows(rows: Sequence[Mapping[str, Any]] | None, *, facade: Any):
    out: List[Dict[str, Any]] = []
    for raw in list(rows or []):
        if not isinstance(raw, Mapping):
            continue
        open_px = facade._to_float(raw.get("open"))
        high_px = facade._to_float(raw.get("high"))
        low_px = facade._to_float(raw.get("low"))
        close_px = facade._to_float(raw.get("close"))
        volume = facade._to_float(raw.get("volume"))
        if high_px <= 0.0 and low_px <= 0.0 and close_px <= 0.0:
            continue
        out.append(
            {
                "ts": raw.get("ts"),
                "open": open_px or close_px,
                "high": max(high_px, open_px, close_px),
                "low": min(low_px if low_px > 0.0 else close_px or open_px, open_px or close_px, close_px or open_px),
                "close": close_px or open_px,
                "volume": max(0.0, volume),
                "vwap": raw.get("vwap"),
            }
        )
    return out
