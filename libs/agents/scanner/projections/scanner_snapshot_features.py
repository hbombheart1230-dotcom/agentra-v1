"""output_snapshots projections (moved verbatim from output_snapshots).

Module globals and helpers are resolved on ``facade`` (the output_snapshots module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict


def compact_feature_snapshot(row: Dict[str, Any], *, facade: Any) -> Dict[str, Any]:
    features = row.get("features") if isinstance(row.get("features"), dict) else {}
    if not isinstance(features, dict):
        return {}
    return {
        "skill_quote_price": features.get("skill_quote_price"),
        "quote_trading_value": features.get("quote_trading_value"),
        "quote_volume": features.get("quote_volume"),
        "quote_best_bid": features.get("quote_best_bid"),
        "quote_best_ask": features.get("quote_best_ask"),
        "quote_spread_bps": features.get("quote_spread_bps"),
        "quote_payload_available": features.get("quote_payload_available"),
        "quote_source": features.get("quote_source"),
        "quote_evidence_status": features.get("quote_evidence_status"),
        "intraday_change_pct": features.get("intraday_change_pct"),
        "entry_compatibility_score": features.get("entry_compatibility_score"),
        "compatibility_bias": features.get("compatibility_bias"),
        "compatibility_source": features.get("compatibility_source"),
        "compat_vwap_distance_abs": features.get("compat_vwap_distance_abs"),
        "compat_is_below_vwap": features.get("compat_is_below_vwap"),
        "compat_reclaim_proximity": features.get("compat_reclaim_proximity"),
        "compat_volume_ratio": features.get("compat_volume_ratio"),
        "compat_breakout_gap_pct": features.get("compat_breakout_gap_pct"),
        "engine_ma20_gap": features.get("engine_ma20_gap"),
        "engine_close_last": features.get("engine_close_last"),
        "engine_ma60": features.get("engine_ma60"),
        "engine_ma120": features.get("engine_ma120"),
        "engine_adx14": features.get("engine_adx14"),
        "engine_trend_strength": features.get("engine_trend_strength"),
        "engine_atr14": features.get("engine_atr14"),
        "engine_volume_spike20": features.get("engine_volume_spike20"),
        "engine_volatility20": features.get("engine_volatility20"),
        "engine_vwap_distance": features.get("engine_vwap_distance"),
        "engine_sector_relative_strength": features.get("engine_sector_relative_strength"),
        "engine_cross_section_rank": features.get("engine_cross_section_rank"),
        "engine_regime": features.get("engine_regime"),
        "engine_signal_score": features.get("engine_signal_score"),
    }
