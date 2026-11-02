from typing import Any, List, Optional

def _rolling_drawdown(closes: List[float], lookback: int = 20, facade: Any = None) -> Optional[float]:
    lb = max(2, int(lookback))
    if len(closes) < lb:
        return None
    window = closes[-lb:]
    peak = max(window)
    cur = float(window[-1])
    if peak <= 0.0:
        return None
    return float((cur / peak) - 1.0)
