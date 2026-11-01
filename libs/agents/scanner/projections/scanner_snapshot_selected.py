"""output_snapshots projections (moved verbatim from output_snapshots).

Module globals and helpers are resolved on ``facade`` (the output_snapshots module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict


def compact_selected_snapshot(selected: Dict[str, Any] | None, *, facade: Any) -> Dict[str, Any]:
    if not isinstance(selected, dict):
        return {}
    candidate = selected.get("candidate") if isinstance(selected.get("candidate"), dict) else {}
    features = selected.get("features") if isinstance(selected.get("features"), dict) else {}
    components = selected.get("components") if isinstance(selected.get("components"), dict) else {}
    return {
        "symbol": str(selected.get("symbol") or ""),
        "why": str(selected.get("why") or ""),
        "asset_class_detected": str(selected.get("asset_class_detected") or ""),
        "detection_source": str(selected.get("detection_source") or ""),
        "detection_field": str(selected.get("detection_field") or ""),
        "sources": list(candidate.get("sources") or [])[:8],
        "source_scores": dict(candidate.get("source_scores") or {}),
        "source_observations": dict(candidate.get("source_observations") or {}),
        "rank_score": facade.to_float(candidate.get("rank_score") or 0.0),
        "universe_score": facade.to_float(candidate.get("universe_score") or 0.0),
        "score_total": facade.to_float(selected.get("score_total") or selected.get("score") or 0.0),
        "risk_score": facade.to_float(selected.get("risk_score") or 0.0),
        "confidence": facade.to_float(selected.get("confidence") or 0.0),
        "best_bid": features.get("quote_best_bid"),
        "best_ask": features.get("quote_best_ask"),
        "spread_bps": features.get("quote_spread_bps"),
        "score_breakdown": dict(selected.get("score_breakdown") or {}),
        "feature_snapshot": {
            "quote_trading_value": features.get("quote_trading_value"),
            "quote_volume": features.get("quote_volume"),
            "intraday_change_pct": features.get("intraday_change_pct"),
            "skill_quote_price": features.get("skill_quote_price"),
            "quote_best_bid": features.get("quote_best_bid"),
            "quote_best_ask": features.get("quote_best_ask"),
            "quote_spread_bps": features.get("quote_spread_bps"),
            "quote_payload_available": features.get("quote_payload_available"),
            "quote_source": features.get("quote_source"),
            "quote_evidence_status": features.get("quote_evidence_status"),
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
            "engine_volume_spike20": features.get("engine_volume_spike20"),
            "engine_volatility20": features.get("engine_volatility20"),
            "engine_vwap_distance": features.get("engine_vwap_distance"),
            "engine_sector_relative_strength": features.get("engine_sector_relative_strength"),
            "engine_cross_section_rank": features.get("engine_cross_section_rank"),
            "engine_regime": features.get("engine_regime"),
            "engine_signal_score": features.get("engine_signal_score"),
        },
        "component_snapshot": {
            "news_sentiment": components.get("news_sentiment"),
            "global_sentiment": components.get("global_sentiment"),
            "trading_value_component": components.get("trading_value_component"),
            "momentum_component": components.get("momentum_component"),
            "trend_component": components.get("trend_component"),
            "volume_surge_component": components.get("volume_surge_component"),
            "intraday_strength_component": components.get("intraday_strength_component"),
            "theme_boost_component": components.get("theme_boost_component"),
            "sentiment_component": components.get("sentiment_component"),
            "volatility_penalty_component": components.get("volatility_penalty_component"),
            "gap_penalty_component": components.get("gap_penalty_component"),
            "avoid_theme_penalty_component": components.get("avoid_theme_penalty_component"),
        },
        "quant_factor_snapshot": facade.build_factor_snapshot_from_candidate(
            selected,
            tactic_id=str(selected.get("tactical_strategy") or ""),
            playbook=str(selected.get("playbook") or ""),
        ),
        "tactic_suitability": dict(selected.get("tactic_suitability") or {}),
    }
