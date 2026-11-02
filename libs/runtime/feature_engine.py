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
    closes = _series(candles, "close")
    highs = _series(candles, "high")
    lows = _series(candles, "low")
    vols = _series(candles, "volume")

    close_last = float(closes[-1]) if closes else None
    sma20 = _sma(closes, 20)
    sma60 = _sma(closes, 60)
    sma120 = _sma(closes, 120)
    rsi14 = _rsi(closes, 14)
    atr14 = _atr(highs, lows, closes, 14)
    adx14 = _adx(highs, lows, closes, 14)
    vol_ret = _pct_returns(closes, 20)
    volatility20 = _std(vol_ret)
    return20 = _pct_change(closes, 20)

    vol_avg20 = _sma(vols, 20)
    volume_spike20: Optional[float] = None
    if vols and vol_avg20 is not None and vol_avg20 > 0.0:
        volume_spike20 = float(vols[-1] / vol_avg20)

    ma20_gap: Optional[float] = None
    if close_last is not None and sma20 is not None and sma20 != 0.0:
        ma20_gap = float((close_last / sma20) - 1.0)
    ma60_gap: Optional[float] = None
    if close_last is not None and sma60 is not None and sma60 != 0.0:
        ma60_gap = float((close_last / sma60) - 1.0)
    ma120_gap: Optional[float] = None
    if close_last is not None and sma120 is not None and sma120 != 0.0:
        ma120_gap = float((close_last / sma120) - 1.0)

    gap_pct = _gap_pct(candles)
    vwap_distance = _vwap_distance(candles, closes, vols)
    rolling_drawdown20 = _rolling_drawdown(closes, 20)

    vol_ctx_input = realized_volatility if realized_volatility is not None else realized_vol
    regime_obj = classify_regime_v2(
        ma20_gap=ma20_gap,
        volatility20=volatility20,
        index_trend=index_trend if index_trend is not None else ma20_gap,
        realized_vol=vol_ctx_input if vol_ctx_input is not None else volatility20,
        global_sentiment=global_sentiment,
        market_breadth=market_breadth,
        trend_gap_threshold=trend_gap_threshold,
        high_vol_threshold=high_vol_threshold,
    )
    regime = str(regime_obj.get("regime") or "range")
    signal = _signal_score(ma20_gap=ma20_gap, rsi14=rsi14)
    # Signed trend strength in [-1, 1], derived from ADX magnitude + trend direction.
    trend_strength: Optional[float] = None
    if adx14 is not None:
        direction_ref = ma20_gap if ma20_gap is not None else index_trend
        direction_num = _to_float(direction_ref)
        direction = 1.0 if (direction_num is None or direction_num >= 0.0) else -1.0
        trend_strength = max(-1.0, min(1.0, (float(adx14) / 100.0) * direction))
    realized_vol_out = _to_float(vol_ctx_input)
    if realized_vol_out is None:
        realized_vol_out = _to_float(volatility20)

    return {
        "close_last": close_last,
        "rsi14": rsi14,
        "ma20": sma20,
        "ma60": sma60,
        "ma120": sma120,
        "ma20_gap": ma20_gap,
        "ma60_gap": ma60_gap,
        "ma120_gap": ma120_gap,
        "atr14": atr14,
        # Alias kept for strategy contracts that refer to generic ADX.
        "adx": adx14,
        "adx14": adx14,
        "trend_strength": trend_strength,
        "gap_pct": gap_pct,
        "vwap_distance": vwap_distance,
        "return20": return20,
        "rolling_drawdown20": rolling_drawdown20,
        "volume_spike20": volume_spike20,
        "volatility20": volatility20,
        "realized_volatility": realized_vol_out,
        "regime": regime,
        "regime_score": regime_obj.get("score"),
        "regime_factors": regime_obj.get("factors"),
        "signal_score": signal,
    }


def build_feature_map(
    ohlcv_by_symbol: Mapping[str, List[Mapping[str, Any]]],
    *,
    trend_gap_threshold: float = 0.01,
    high_vol_threshold: float = 0.03,
    context: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    ctx = dict(context or {})
    gs = _to_float(ctx.get("global_sentiment")) if isinstance(ctx, dict) else None
    breadth = _to_float(ctx.get("market_breadth")) if isinstance(ctx, dict) else None
    idx_trend = _to_float(ctx.get("index_trend")) if isinstance(ctx, dict) else None
    rv = _to_float(ctx.get("realized_vol")) if isinstance(ctx, dict) else None
    if rv is None:
        rv = _to_float(ctx.get("realized_volatility")) if isinstance(ctx, dict) else None
    for k, rows in ohlcv_by_symbol.items():
        sym = str(k or "").strip()
        if not sym or not isinstance(rows, list) or not rows:
            continue
        out[sym] = build_feature_row(
            rows,
            trend_gap_threshold=trend_gap_threshold,
            high_vol_threshold=high_vol_threshold,
            global_sentiment=gs,
            market_breadth=breadth,
            index_trend=idx_trend,
            realized_vol=rv,
            realized_volatility=rv,
        )

    if not out:
        return out

    # Cross-sectional enrichments (deterministic and additive).
    signal_pairs = [
        (sym, float(out[sym].get("signal_score") or 0.0))
        for sym in out.keys()
    ]
    signal_pairs.sort(key=lambda x: x[1])
    n = len(signal_pairs)
    if n > 1:
        for i, (sym, _score) in enumerate(signal_pairs):
            out[sym]["cross_section_rank_signal"] = float(i / float(n - 1))
            out[sym]["cross_section_rank"] = float(i / float(n - 1))
    else:
        only_sym = signal_pairs[0][0]
        out[only_sym]["cross_section_rank_signal"] = 1.0
        out[only_sym]["cross_section_rank"] = 1.0

    returns = [float(v.get("return20")) for v in out.values() if v.get("return20") is not None]
    med_ret = _median(returns)
    for sym, row in out.items():
        r20 = row.get("return20")
        if r20 is None or med_ret is None:
            row["relative_strength20"] = None
            row["sector_relative_strength"] = None
        else:
            rs = float(float(r20) - float(med_ret))
            row["relative_strength20"] = rs
            row["sector_relative_strength"] = rs

    breadth_val = sum(1 for _sym, s in signal_pairs if s > 0.0) / float(len(signal_pairs))
    for row in out.values():
        row["market_breadth"] = float(breadth_val)

    # Cross-sectional volatility percentile for downstream sizing.
    vol_pairs = [
        (sym, float(out[sym].get("volatility20")))
        for sym in out.keys()
        if out[sym].get("volatility20") is not None
    ]
    vol_pairs.sort(key=lambda x: x[1])
    m = len(vol_pairs)
    if m > 1:
        for i, (sym, _vol) in enumerate(vol_pairs):
            out[sym]["volatility_percentile"] = float(i / float(m - 1))
    elif m == 1:
        out[vol_pairs[0][0]]["volatility_percentile"] = 0.5
    for sym in out.keys():
        if out[sym].get("volatility_percentile") is None:
            out[sym]["volatility_percentile"] = 0.5

    return out
