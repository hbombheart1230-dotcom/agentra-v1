from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _opening_largecap_watchlist_row(row: Mapping[str, Any], *, metric_row: Mapping[str, Any] | None = None, facade: Any):
    base = facade._candidate_context(row)
    symbol = facade._symbol(row)
    metrics = facade._as_dict(metric_row)
    row_features = facade._as_dict(row.get("features"))
    row_metrics = facade._as_dict(row.get("metrics"))
    metric_factors = facade._factor_snapshot(metrics)
    row_factors = facade._factor_snapshot(row)
    volume_ratio = facade._metric_value(
        metrics.get("volume_ratio"),
        metric_factors.get("volume_ratio"),
        row.get("volume_ratio"),
        row_factors.get("volume_ratio"),
        row_features.get("volume_ratio"),
        row_metrics.get("volume_ratio"),
    )
    vwap_distance = facade._metric_value(
        metrics.get("vwap_distance"),
        metric_factors.get("vwap_distance_pct"),
        metric_factors.get("vwap_distance"),
        row.get("vwap_distance"),
        row.get("vwap_distance_pct"),
        row_factors.get("vwap_distance_pct"),
        row_factors.get("vwap_distance"),
        row_features.get("vwap_distance_pct"),
        row_metrics.get("vwap_distance_pct"),
    )
    breakout_ok = facade._metric_value(
        metrics.get("breakout_ok"),
        metric_factors.get("breakout_ok"),
        row.get("breakout_ok"),
        row_factors.get("breakout_ok"),
        row_features.get("breakout_ok"),
        row_metrics.get("breakout_ok"),
    )
    cost_adjusted_edge_ok = facade._metric_value(
        metrics.get("cost_adjusted_edge_ok"),
        metric_factors.get("cost_adjusted_edge_ok"),
        row.get("cost_adjusted_edge_ok"),
        row_factors.get("cost_adjusted_edge_ok"),
    )
    metric_source = (
        f"{facade._text(metrics.get('shadow_role'))}_same_symbol"
        if metrics
        else "ranked_candidates"
    )
    metric_missing = not any(value not in (None, "") for value in (volume_ratio, vwap_distance, breakout_ok, cost_adjusted_edge_ok))
    factor_snapshot = facade._candidate_factor_snapshot(row)
    if metrics:
        merged_factors = facade._as_dict(factor_snapshot.get("factors"))
        merged_factors.update({key: value for key, value in metric_factors.items() if value not in (None, "")})
        if volume_ratio not in (None, ""):
            merged_factors["volume_ratio"] = volume_ratio
        if vwap_distance not in (None, ""):
            merged_factors["vwap_distance_pct"] = vwap_distance
        if breakout_ok not in (None, ""):
            merged_factors["breakout_ok"] = breakout_ok
        if cost_adjusted_edge_ok not in (None, ""):
            merged_factors["cost_adjusted_edge_ok"] = cost_adjusted_edge_ok
        factor_snapshot = {"factors": merged_factors} if merged_factors else factor_snapshot
    base.update(
        {
            "symbol": symbol,
            "shadow_role": "opening_largecap_watchlist",
            "evaluated": False,
            "reason": "opening_largecap_watchlist_not_evaluated_by_monitor",
            "would_enter": False,
            "volume_ratio": volume_ratio,
            "vwap_distance": vwap_distance,
            "breakout_ok": breakout_ok,
            "cost_adjusted_edge_ok": facade._bool(cost_adjusted_edge_ok),
            "quant_factor_snapshot": factor_snapshot,
            "source": "ranked_candidates",
            "metric_source": metric_source,
            "metric_missing_reason": "minute_metrics_not_available" if metric_missing else "",
        }
    )
    return base
