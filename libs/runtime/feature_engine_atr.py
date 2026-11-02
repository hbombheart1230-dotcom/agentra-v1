from typing import Any, List, Optional

def _atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14, facade: Any = None) -> Optional[float]:
    p = max(1, int(period))
    if len(highs) < p + 1 or len(lows) < p + 1 or len(closes) < p + 1:
        return None
    trs: List[float] = []
    for i in range(len(closes) - p, len(closes)):
        hi = float(highs[i]); lo = float(lows[i]); prev_close = float(closes[i - 1])
        trs.append(float(max(hi - lo, abs(hi - prev_close), abs(lo - prev_close))))
    return float(sum(trs) / float(len(trs))) if trs else None
