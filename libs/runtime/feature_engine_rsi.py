from typing import Any, List, Optional

def _rsi(closes: List[float], period: int = 14, facade: Any = None) -> Optional[float]:
    p = max(1, int(period))
    if len(closes) < p + 1:
        return None
    diffs = [float(closes[i] - closes[i - 1]) for i in range(len(closes) - p, len(closes))]
    gains = [d for d in diffs if d > 0.0]
    losses = [-d for d in diffs if d < 0.0]
    avg_gain = float(sum(gains) / float(p)) if gains else 0.0
    avg_loss = float(sum(losses) / float(p)) if losses else 0.0
    if avg_loss <= 0.0:
        return 100.0
    return float(100.0 - (100.0 / (1.0 + float(avg_gain / avg_loss))))
