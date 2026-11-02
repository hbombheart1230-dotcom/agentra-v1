from typing import Any, List

def _pct_returns(closes: List[float], period: int, facade: Any) -> List[float]:
    p = max(1, int(period))
    if len(closes) < p + 1:
        return []
    out: List[float] = []
    base = closes[-(p + 1):]
    for i in range(1, len(base)):
        prev = float(base[i - 1]); cur = float(base[i])
        if prev != 0.0:
            out.append(float((cur / prev) - 1.0))
    return out
