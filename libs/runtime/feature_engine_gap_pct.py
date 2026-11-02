from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

def _gap_pct(candles: List[Mapping[str, Any]], facade: Any) -> Optional[float]:
    if len(candles) < 2:
        return None
    prev_close = facade._to_float(candles[-2].get("close"))
    cur_open = facade._to_float(candles[-1].get("open"))
    if prev_close is None or cur_open is None or prev_close == 0.0:
        return None
    return float((cur_open / prev_close) - 1.0)
