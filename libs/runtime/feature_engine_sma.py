from typing import Any, List, Optional

def _sma(values: List[float], period: int, facade: Any) -> Optional[float]:
    p = max(1, int(period))
    if len(values) < p:
        return None
    return float(sum(values[-p:]) / float(p))
