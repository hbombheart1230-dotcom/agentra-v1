from __future__ import annotations

import sys
from math import sqrt
from typing import Any, Dict, List, Mapping, Optional

from libs.runtime.regime import classify_regime_v2


def _to_float(v: Any) -> Optional[float]:
    from .feature_engine_to_float import _to_float as owner
    return owner(v, facade=sys.modules[__name__])


def _series(candles: List[Mapping[str, Any]], key: str) -> List[float]:
    from .feature_engine_series import _series as owner
    return owner(candles, key, facade=sys.modules[__name__])


def _sma(values: List[float], period: int) -> Optional[float]:
    from .feature_engine_sma import _sma as owner
    return owner(values, period, facade=sys.modules[__name__])


def _std(values: List[float]) -> Optional[float]:
    from .feature_engine_std import _std as owner
    return owner(values, facade=sys.modules[__name__])


def _median(values: List[float]) -> Optional[float]:
    from .feature_engine_median import _median as owner
    return owner(values, facade=sys.modules[__name__])


def _rsi(closes: List[float], period: int = 14) -> Optional[float]:
    from .feature_engine_rsi import _rsi as owner
    return owner(closes, period, facade=sys.modules[__name__])


def _atr(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Optional[float]:
    from .feature_engine_atr import _atr as owner
    return owner(highs, lows, closes, period, facade=sys.modules[__name__])


def _pct_returns(closes: List[float], period: int) -> List[float]:
    from .feature_engine_pct_returns import _pct_returns as owner
    return owner(closes, period, facade=sys.modules[__name__])


def _pct_change(closes: List[float], period: int) -> Optional[float]:
    from .feature_engine_pct_change import _pct_change as owner
    return owner(closes=closes, period=period, facade=sys.modules[__name__])


def _adx(highs: List[float], lows: List[float], closes: List[float], period: int = 14) -> Optional[float]:
    from .feature_engine_adx import _adx as owner
    return owner(highs=highs, lows=lows, closes=closes, period=period, facade=sys.modules[__name__])


def _gap_pct(candles: List[Mapping[str, Any]]) -> Optional[float]:
    from .feature_engine_gap_pct import _gap_pct as owner

    return owner(candles=candles, facade=sys.modules[__name__])


def _vwap_distance(candles: List[Mapping[str, Any]], closes: List[float], vols: List[float]) -> Optional[float]:
    from .feature_engine_vwap_distance import _vwap_distance as owner
    return owner(candles=candles, closes=closes, vols=vols, facade=sys.modules[__name__])


def _rolling_drawdown(closes: List[float], lookback: int = 20) -> Optional[float]:
    from .feature_engine_rolling_drawdown import _rolling_drawdown as owner
    return owner(closes=closes, lookback=lookback, facade=sys.modules[__name__])


def classify_regime(
    *,
    ma20_gap: Optional[float],
    volatility20: Optional[float],
    trend_gap_threshold: float = 0.01,
    high_vol_threshold: float = 0.03,
) -> str:
    from .feature_engine_classify_regime import classify_regime as owner
    return owner(ma20_gap=ma20_gap, volatility20=volatility20, trend_gap_threshold=trend_gap_threshold, high_vol_threshold=high_vol_threshold, facade=sys.modules[__name__])


def _signal_score(*, ma20_gap: Optional[float], rsi14: Optional[float]) -> float:
    from .feature_engine_signal_score import _signal_score as owner
    return owner(ma20_gap=ma20_gap, rsi14=rsi14, facade=sys.modules[__name__])


def build_feature_row(
    candles: List[Mapping[str, Any]],
    *,
    trend_gap_threshold: float = 0.01,
    high_vol_threshold: float = 0.03,
    global_sentiment: Optional[float] = None,
    market_breadth: Optional[float] = None,
    index_trend: Optional[float] = None,
    realized_vol: Optional[float] = None,
    realized_volatility: Optional[float] = None,
) -> Dict[str, Any]:
    from .feature_engine_build_feature_row import build_feature_row as owner

    return owner(candles, trend_gap_threshold=trend_gap_threshold, high_vol_threshold=high_vol_threshold, global_sentiment=global_sentiment, market_breadth=market_breadth, index_trend=index_trend, realized_vol=realized_vol, realized_volatility=realized_volatility, facade=sys.modules[__name__])


def build_feature_map(
    ohlcv_by_symbol: Mapping[str, List[Mapping[str, Any]]],
    *,
    trend_gap_threshold: float = 0.01,
    high_vol_threshold: float = 0.03,
    context: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Dict[str, Any]]:
        from .feature_engine_build_feature_map import build_feature_map as owner
        return owner(ohlcv_by_symbol, trend_gap_threshold=trend_gap_threshold, high_vol_threshold=high_vol_threshold, context=context, facade=sys.modules[__name__])
