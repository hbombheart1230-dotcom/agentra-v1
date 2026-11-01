"""output_snapshots projections (moved verbatim from output_snapshots).

Module globals and helpers are resolved on ``facade`` (the output_snapshots module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict


def feature_coverage_summary(row: Dict[str, Any], *, facade: Any) -> Dict[str, Any]:
    features = row.get("features") if isinstance(row.get("features"), dict) else {}
    if not isinstance(features, dict):
        return {
            "present": 0,
            "total": 0,
            "coverage_ratio": 0.0,
            "quality": "missing",
            "present_keys": [],
            "missing_keys": [],
        }
    interesting_keys = [
        "engine_ma20_gap",
        "engine_ma60",
        "engine_ma120",
        "engine_adx14",
        "engine_trend_strength",
        "engine_atr14",
        "engine_volume_spike20",
        "engine_volatility20",
        "engine_vwap_distance",
        "engine_sector_relative_strength",
        "engine_cross_section_rank",
        "engine_regime",
        "engine_signal_score",
    ]
    present_keys = [key for key in interesting_keys if features.get(key) not in (None, "")]
    missing_keys = [key for key in interesting_keys if features.get(key) in (None, "")]
    total = len(interesting_keys)
    present = len(present_keys)
    ratio = float(present) / float(total) if total else 0.0
    if ratio >= 0.75:
        quality = "strong"
    elif ratio >= 0.5:
        quality = "partial"
    else:
        quality = "weak"
    return {
        "present": int(present),
        "total": int(total),
        "coverage_ratio": float(ratio),
        "quality": quality,
        "present_keys": present_keys,
        "missing_keys": missing_keys,
    }
