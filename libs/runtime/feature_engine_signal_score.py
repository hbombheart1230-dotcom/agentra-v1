from typing import Any, Optional

def _signal_score(*, ma20_gap: Optional[float], rsi14: Optional[float], facade: Any = None) -> float:
    gap=float(ma20_gap or 0.0); rsi=float(rsi14 or 50.0); score=0.0
    if gap > 0.0 and 50.0 <= rsi <= 70.0: score += 0.5
    if gap < 0.0 and 30.0 <= rsi <= 50.0: score -= 0.5
    if rsi >= 75.0: score -= 0.2
    if rsi <= 25.0: score += 0.2
    return float(max(-1.0, min(1.0, score)))
