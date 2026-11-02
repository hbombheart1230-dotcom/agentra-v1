from typing import Any, Optional

def classify_regime(*, ma20_gap: Optional[float], volatility20: Optional[float], trend_gap_threshold: float = 0.01, high_vol_threshold: float = 0.03, facade: Any = None) -> str:
    gap=float(ma20_gap or 0.0); vol=float(volatility20 or 0.0)
    if vol >= float(high_vol_threshold): return "high_volatility"
    if abs(gap) >= float(trend_gap_threshold): return "trend"
    return "range"
