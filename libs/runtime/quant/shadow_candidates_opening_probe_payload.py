from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _opening_probe_payload(row: Mapping[str, Any], *, opening_minutes: int | None, facade: Any):
    if opening_minutes is None or opening_minutes > 20:
        return {
            "eligible": False,
            "would_probe": False,
            "reason": "outside_opening_window",
            "minutes_since_open": opening_minutes,
        }

    factors = facade._factor_snapshot(row)
    volume_ratio = facade._float(row.get("volume_ratio"), facade._float(factors.get("volume_ratio"), 0.0)) or 0.0
    vwap_distance = facade._float(row.get("vwap_distance"), facade._float(factors.get("vwap_distance_pct"), 0.0)) or 0.0
    human_chart_entry_score = facade._float(factors.get("human_chart_entry_score"), 0.0) or 0.0
    breakout_ok = facade._bool(row.get("breakout_ok")) or facade._bool(factors.get("breakout_ok"))
    weighted_score_passed = facade._bool(factors.get("weighted_score_passed"))
    cost_ok = facade._cost_ok_for_opening_probe(row)
    momentum_ok = bool(
        cost_ok
        and volume_ratio >= 0.8
        and vwap_distance >= 0.0
        and (
            breakout_ok
            or weighted_score_passed
            or human_chart_entry_score >= 0.65
        )
    )
    reason_parts: List[str] = []
    if not cost_ok:
        reason_parts.append("cost_edge_not_met")
    if volume_ratio < 0.8:
        reason_parts.append("volume_ratio_below_probe_floor")
    if vwap_distance < 0.0:
        reason_parts.append("below_vwap")
    if not (breakout_ok or weighted_score_passed or human_chart_entry_score >= 0.65):
        reason_parts.append("momentum_structure_not_confirmed")
    return {
        "eligible": True,
        "would_probe": momentum_ok,
        "reason": "opening_momentum_probe_ready" if momentum_ok else ",".join(reason_parts),
        "minutes_since_open": opening_minutes,
        "cost_ok": cost_ok,
        "volume_ratio": volume_ratio,
        "vwap_distance_pct": vwap_distance,
        "breakout_ok": breakout_ok,
        "weighted_score_passed": weighted_score_passed,
        "human_chart_entry_score": human_chart_entry_score,
        "probe_size_hint": "small",
        "behavior_effect": "observation_only",
    }
