from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _empty_human_chart_entry_setup(*, facade: Any):
    return {
        "schema_version": "human_chart_entry_setup.v1",
        "available": False,
        "applied": False,
        "mode": "none",
        "authority": "qualified_buy_promotion",
        "setup_label": "",
        "setup_quality": "none",
        "setup_score": 0.0,
        "thresholds": {
            "min_a_setup_score": 0.72,
            "min_entry_chart_score": 0.68,
            "min_live_promotion_entry_chart_score": 0.48,
            "min_live_promotion_entry_quality_score": 0.78,
            "min_live_promotion_transition_readiness_score": 0.72,
            "max_exit_risk_score": 0.20,
            "min_candle_quality_score": 0.45,
            "min_vwap_reference_quality_score": 0.35,
            "min_reward_room_score": 0.25,
            "min_multi_window_structure_score": 0.35,
            "reclaim_near_ready_distance_min": -0.0025,
            "breakout_near_ready_distance_min": -0.0015,
            "volume_near_ready_distance_min": -0.15,
        },
        "observed": {},
        "matched_features": [],
        "blocking_features": [],
        "notes": [],
    }
