from __future__ import annotations

import sys
from typing import Any, Dict, Optional


def _to_float(v: Any, default: float = 0.0) -> float:
    from .regime_to_float import _to_float as owner
    return owner(v, default, facade=sys.modules[__name__])


def classify_regime_v2(
    *,
    ma20_gap: Optional[float],
    volatility20: Optional[float],
    index_trend: Optional[float] = None,
    realized_vol: Optional[float] = None,
    realized_volatility: Optional[float] = None,
    global_sentiment: Optional[float] = None,
    market_breadth: Optional[float] = None,
    trend_gap_threshold: float = 0.01,
    high_vol_threshold: float = 0.03,
    weight_ma_gap: float = 0.50,
    weight_index_trend: float = 0.25,
    weight_global_sentiment: float = 0.15,
    weight_market_breadth: float = 0.10,
    weight_volatility_penalty: float = 0.05,
) -> Dict[str, Any]:
    from .regime_classify_regime_v2 import classify_regime_v2 as owner
    return owner(ma20_gap=ma20_gap, volatility20=volatility20, index_trend=index_trend, realized_vol=realized_vol, realized_volatility=realized_volatility, global_sentiment=global_sentiment, market_breadth=market_breadth, trend_gap_threshold=trend_gap_threshold, high_vol_threshold=high_vol_threshold, weight_ma_gap=weight_ma_gap, weight_index_trend=weight_index_trend, weight_global_sentiment=weight_global_sentiment, weight_market_breadth=weight_market_breadth, weight_volatility_penalty=weight_volatility_penalty, facade=sys.modules[__name__])
