from __future__ import annotations

def build_feature_map(ohlcv_by_symbol: facade.Mapping[str, facade.List[facade.Mapping[str, facade.Any]]], *, trend_gap_threshold: float=0.01, high_vol_threshold: float=0.03, context: facade.Optional[facade.Mapping[str, facade.Any]]=None, facade: facade.Any) -> facade.Dict[str, facade.Dict[str, facade.Any]]:
    out: facade.Dict[str, facade.Dict[str, facade.Any]] = {}
    ctx = dict(context or {})
    gs = facade._to_float(ctx.get('global_sentiment')) if isinstance(ctx, dict) else None
    breadth = facade._to_float(ctx.get('market_breadth')) if isinstance(ctx, dict) else None
    idx_trend = facade._to_float(ctx.get('index_trend')) if isinstance(ctx, dict) else None
    rv = facade._to_float(ctx.get('realized_vol')) if isinstance(ctx, dict) else None
    if rv is None:
        rv = facade._to_float(ctx.get('realized_volatility')) if isinstance(ctx, dict) else None
    for k, rows in ohlcv_by_symbol.items():
        sym = str(k or '').strip()
        if not sym or not isinstance(rows, list) or (not rows):
            continue
        out[sym] = facade.build_feature_row(rows, trend_gap_threshold=trend_gap_threshold, high_vol_threshold=high_vol_threshold, global_sentiment=gs, market_breadth=breadth, index_trend=idx_trend, realized_vol=rv, realized_volatility=rv)
    if not out:
        return out
    signal_pairs = [(sym, float(out[sym].get('signal_score') or 0.0)) for sym in out.keys()]
    signal_pairs.sort(key=lambda x: x[1])
    n = len(signal_pairs)
    if n > 1:
        for i, (sym, _score) in enumerate(signal_pairs):
            out[sym]['cross_section_rank_signal'] = float(i / float(n - 1))
            out[sym]['cross_section_rank'] = float(i / float(n - 1))
    else:
        only_sym = signal_pairs[0][0]
        out[only_sym]['cross_section_rank_signal'] = 1.0
        out[only_sym]['cross_section_rank'] = 1.0
    returns = [float(v.get('return20')) for v in out.values() if v.get('return20') is not None]
    med_ret = facade._median(returns)
    for sym, row in out.items():
        r20 = row.get('return20')
        if r20 is None or med_ret is None:
            row['relative_strength20'] = None
            row['sector_relative_strength'] = None
        else:
            rs = float(float(r20) - float(med_ret))
            row['relative_strength20'] = rs
            row['sector_relative_strength'] = rs
    breadth_val = sum((1 for _sym, s in signal_pairs if s > 0.0)) / float(len(signal_pairs))
    for row in out.values():
        row['market_breadth'] = float(breadth_val)
    vol_pairs = [(sym, float(out[sym].get('volatility20'))) for sym in out.keys() if out[sym].get('volatility20') is not None]
    vol_pairs.sort(key=lambda x: x[1])
    m = len(vol_pairs)
    if m > 1:
        for i, (sym, _vol) in enumerate(vol_pairs):
            out[sym]['volatility_percentile'] = float(i / float(m - 1))
    elif m == 1:
        out[vol_pairs[0][0]]['volatility_percentile'] = 0.5
    for sym in out.keys():
        if out[sym].get('volatility_percentile') is None:
            out[sym]['volatility_percentile'] = 0.5
    return out
