from __future__ import annotations
from typing import Any, List, Optional

def _pct_change(closes: List[float], period: int, facade: Any) -> Optional[float]:
    p = max(1, int(period))
    if len(closes) < p + 1:
        return None
    prev = float(closes[-(p + 1)])
    cur = float(closes[-1])
    if prev == 0.0:
        return None
    return float((cur / prev) - 1.0)
