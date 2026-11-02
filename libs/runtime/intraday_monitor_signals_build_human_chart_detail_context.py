from __future__ import annotations

def _build_human_chart_detail_context(candles: facade.Sequence[facade.Mapping[str, facade.Any]], *, current_close: float, current_vwap: float, recent_high: float, breakout_level: float, volume_ratio: float, facade: facade.Any) -> facade.Dict[str, facade.Any]:
    out: facade.Dict[str, facade.Any] = facade._empty_human_chart_detail_context()
    if not candles:
        out['notes'] = ['minute_candles_unavailable']
        return out
    last = dict(candles[-1] or {})
    current_open = facade._to_float(last.get('open'), facade._to_float(last.get('close')))
    current_high = max(facade._to_float(last.get('high')), current_close, current_open)
    current_low = min(facade._to_float(last.get('low')), current_close, current_open)
    candle_range = max(0.0, current_high - current_low)
    if candle_range > 0.0:
        body_ratio = facade._clamp_score(abs(current_close - current_open) / candle_range)
        close_location = facade._clamp_score((current_close - current_low) / candle_range)
        upper_wick_ratio = facade._clamp_score((current_high - max(current_open, current_close)) / candle_range)
        lower_wick_ratio = facade._clamp_score((min(current_open, current_close) - current_low) / candle_range)
        candle_quality_score = facade._clamp_score(0.15 + 0.35 * close_location + 0.2 * body_ratio + (0.15 if current_close >= current_open else 0.0) + 0.1 * lower_wick_ratio - 0.25 * upper_wick_ratio)
    else:
        body_ratio = 0.0
        close_location = 0.5
        upper_wick_ratio = 0.0
        lower_wick_ratio = 0.0
        candle_quality_score = 0.5
    explicit_vwap_count = sum((1 for row in candles if facade._to_float((row or {}).get('vwap')) > 0.0))
    volume_count = sum((1 for row in candles if facade._to_float((row or {}).get('volume')) > 0.0))
    row_count = len(candles)
    explicit_vwap_ratio = explicit_vwap_count / float(row_count or 1)
    volume_presence_ratio = volume_count / float(row_count or 1)
    last_has_explicit_vwap = facade._to_float(last.get('vwap')) > 0.0
    vwap_source = 'explicit_bar_vwap' if last_has_explicit_vwap else 'session_vwap_fallback'
    vwap_reference_quality_score = 0.0 if current_vwap <= 0.0 else facade._clamp_score(0.25 + 0.35 * explicit_vwap_ratio + 0.2 * min(1.0, row_count / 10.0) + 0.2 * volume_presence_ratio)
    prior_highs = [facade._to_float(row.get('high')) for row in candles[-20:-1] if isinstance(row, facade.Mapping) and facade._to_float(row.get('high')) > 0.0]
    prior_resistance = max(prior_highs, default=recent_high)
    reward_room_pct: float | None = None
    breakout_extension_pct: float | None = None
    if current_close > 0.0 and prior_resistance > 0.0:
        if current_close <= prior_resistance:
            reward_room_pct = prior_resistance / current_close - 1.0
            reward_room_score = facade._min_threshold_score(reward_room_pct, 0.006)
        else:
            breakout_extension_pct = current_close / prior_resistance - 1.0
            reward_room_score = facade._clamp_score(0.72 - max(0.0, breakout_extension_pct - 0.008) / 0.04)
    else:
        reward_room_score = 0.5
    closes = [facade._to_float(row.get('close')) for row in candles if isinstance(row, facade.Mapping) and facade._to_float(row.get('close')) > 0.0]
    lows = [facade._to_float(row.get('low')) for row in candles if isinstance(row, facade.Mapping) and facade._to_float(row.get('low')) > 0.0]
    if len(closes) >= 5:
        short_base = closes[-3] if len(closes) >= 3 else closes[0]
        mid_base = closes[-6] if len(closes) >= 6 else closes[0]
        short_progress = facade._clamp_score(current_close / short_base if short_base > 0.0 else 0.0)
        mid_progress = facade._clamp_score(current_close / mid_base if mid_base > 0.0 else 0.0)
        recent_lows = lows[-3:] if len(lows) >= 3 else lows
        prior_lows = lows[-6:-3] if len(lows) >= 6 else lows[:-3]
        higher_low_score = 0.5
        if recent_lows and prior_lows:
            higher_low_score = 1.0 if min(recent_lows) >= min(prior_lows) else 0.35
        multi_window_structure_score = facade._clamp_score(0.34 * short_progress + 0.28 * mid_progress + 0.23 * higher_low_score + 0.15 * facade._min_threshold_score(volume_ratio, 1.0))
    else:
        short_progress = 0.5
        mid_progress = 0.5
        higher_low_score = 0.5
        multi_window_structure_score = 0.5
    out.update({'available': True, 'candle_quality_score': round(float(candle_quality_score), 4), 'vwap_reference_quality_score': round(float(vwap_reference_quality_score), 4), 'reward_room_score': round(float(reward_room_score), 4), 'multi_window_structure_score': round(float(multi_window_structure_score), 4), 'observed': {'current_open': current_open if current_open > 0.0 else None, 'current_close': current_close if current_close > 0.0 else None, 'current_high': current_high if current_high > 0.0 else None, 'current_low': current_low if current_low > 0.0 else None, 'body_ratio': round(float(body_ratio), 4), 'close_location': round(float(close_location), 4), 'upper_wick_ratio': round(float(upper_wick_ratio), 4), 'lower_wick_ratio': round(float(lower_wick_ratio), 4), 'vwap_source': vwap_source, 'vwap_bar_count': int(row_count), 'explicit_vwap_count': int(explicit_vwap_count), 'explicit_vwap_ratio': round(float(explicit_vwap_ratio), 4), 'volume_presence_ratio': round(float(volume_presence_ratio), 4), 'prior_resistance': prior_resistance if prior_resistance > 0.0 else None, 'breakout_level': breakout_level if breakout_level > 0.0 else None, 'reward_room_pct': round(float(reward_room_pct), 6) if reward_room_pct is not None else None, 'breakout_extension_pct': round(float(breakout_extension_pct), 6) if breakout_extension_pct is not None else None, 'short_progress': round(float(short_progress), 4), 'mid_progress': round(float(mid_progress), 4), 'higher_low_score': round(float(higher_low_score), 4)}})
    return out
