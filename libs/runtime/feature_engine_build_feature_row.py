from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional

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
    facade: Any,
) -> Dict[str, Any]:
    closes = facade._series(candles, "close")
    highs = facade._series(candles, "high")
    lows = facade._series(candles, "low")
    vols = facade._series(candles, "volume")

    close_last = float(closes[-1]) if closes else None
    sma20 = facade._sma(closes, 20)
    sma60 = facade._sma(closes, 60)
    sma120 = facade._sma(closes, 120)
    rsi14 = facade._rsi(closes, 14)
    atr14 = facade._atr(highs, lows, closes, 14)
    adx14 = facade._adx(highs, lows, closes, 14)
    vol_ret = facade._pct_returns(closes, 20)
    volatility20 = facade._std(vol_ret)
    return20 = facade._pct_change(closes, 20)

    vol_avg20 = facade._sma(vols, 20)
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

    gap_pct = facade._gap_pct(candles)
    vwap_distance = facade._vwap_distance(candles, closes, vols)
    rolling_drawdown20 = facade._rolling_drawdown(closes, 20)

    vol_ctx_input = realized_volatility if realized_volatility is not None else realized_vol
    regime_obj = facade.classify_regime_v2(
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
    signal = facade._signal_score(ma20_gap=ma20_gap, rsi14=rsi14)
    # Signed trend strength in [-1, 1], derived from ADX magnitude + trend direction.
    trend_strength: Optional[float] = None
    if adx14 is not None:
        direction_ref = ma20_gap if ma20_gap is not None else index_trend
        direction_num = facade._to_float(direction_ref)
        direction = 1.0 if (direction_num is None or direction_num >= 0.0) else -1.0
        trend_strength = max(-1.0, min(1.0, (float(adx14) / 100.0) * direction))
    realized_vol_out = facade._to_float(vol_ctx_input)
    if realized_vol_out is None:
        realized_vol_out = facade._to_float(volatility20)

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
