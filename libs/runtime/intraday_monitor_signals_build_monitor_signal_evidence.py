from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _build_monitor_signal_evidence(*, reclaim_score: float, volume_score: float, pullback_score: float, breakout_score: float, confidence_score: float, confidence_threshold: float, entry_quality_score: float, breakout_quality_score: float, pullback_quality_score: float, entry_quality_path: str, reclaim_ok: bool, volume_ok: bool, pullback_ok: bool, breakout_ok: bool, rebound_ok: bool, reclaim_gate_ok: bool, breakout_path_ok: bool, pullback_volume_path_ok: bool, extension_ok: bool, too_extended: bool, reclaim_strength: float, rebound_strength: float, transition_readiness_score: float, reclaim_distance_to_ready: float | None, volume_distance_to_ready: float | None, breakout_distance_to_ready: float | None, score_breakdown: Mapping[str, Any] | None=None, score_threshold: float=3.0, facade: Any):
    weighted_scores = dict(score_breakdown or {})
    total_weighted_score = round(sum(facade._to_float(v) for v in weighted_scores.values()), 4) if weighted_scores else 0.0
    threshold_value = float(score_threshold if score_threshold > 0.0 else 3.0)
    return {
        "scores": {
            "reclaim_score": round(facade._clamp_score(reclaim_score), 4),
            "volume_score": round(facade._clamp_score(volume_score), 4),
            "pullback_score": round(facade._clamp_score(pullback_score), 4),
            "breakout_score": round(facade._clamp_score(breakout_score), 4),
            "breakout_proximity_score": round(facade._clamp_score(breakout_score), 4),
            "confidence_score": round(facade._clamp_score(confidence_score), 4),
            "entry_quality_score": round(facade._clamp_score(entry_quality_score), 4),
            "breakout_quality_score": round(facade._clamp_score(breakout_quality_score), 4),
            "pullback_quality_score": round(facade._clamp_score(pullback_quality_score), 4),
        },
        "checks": {
            "reclaim_ok": bool(reclaim_ok),
            "volume_ok": bool(volume_ok),
            "pullback_ok": bool(pullback_ok),
            "breakout_ok": bool(breakout_ok),
            "rebound_ok": bool(rebound_ok),
            "reclaim_gate_ok": bool(reclaim_gate_ok),
            "breakout_path_ok": bool(breakout_path_ok),
            "pullback_volume_path_ok": bool(pullback_volume_path_ok),
            "extension_ok": bool(extension_ok),
            "confidence_ok": bool(confidence_score >= confidence_threshold),
        },
        "derived": {
            "too_extended": bool(too_extended),
            "reclaim_strength": round(facade._clamp_score(reclaim_strength), 4),
            "rebound_strength": round(facade._clamp_score(rebound_strength), 4),
            "transition_readiness_score": round(facade._clamp_score(transition_readiness_score), 4),
            "reclaim_distance_to_ready": reclaim_distance_to_ready,
            "volume_distance_to_ready": volume_distance_to_ready,
            "breakout_distance_to_ready": breakout_distance_to_ready,
            "confidence_threshold": round(float(confidence_threshold), 4),
            "entry_quality_tier": facade._entry_quality_tier(entry_quality_score),
            "entry_quality_path": str(entry_quality_path or ""),
            "entry_quality_observability_only": True,
            "weighted_score_total": total_weighted_score,
            "weighted_score_threshold": threshold_value,
            "weighted_score_passed": bool(total_weighted_score >= threshold_value),
        },
        "weighted_scores": weighted_scores,
    }
