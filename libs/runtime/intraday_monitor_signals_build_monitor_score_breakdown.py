from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _build_monitor_score_breakdown(*, vwap_reclaim_ok: bool, breakout_ok: bool, pullback_mature: bool, volume_ok: bool, confidence_gate_ok: bool, chart_structure_features: Mapping[str, Any] | None = None, facade: Any):
    breakdown = {
        "vwap_reclaim_ok": 2.0 if bool(vwap_reclaim_ok) else 0.0,
        "breakout_ok": 2.0 if bool(breakout_ok) else 0.0,
        "pullback_mature": 1.0 if bool(pullback_mature) else 0.0,
        "volume_ok": 1.0 if bool(volume_ok) else 0.0,
        "confidence_gate_ok": 1.0 if bool(confidence_gate_ok) else 0.0,
    }
    chart_payload = dict(chart_structure_features or {}) if isinstance(chart_structure_features, Mapping) else {}
    chart_context = (
        dict(chart_payload.get("human_chart_context") or {})
        if isinstance(chart_payload.get("human_chart_context"), Mapping)
        else {}
    )
    if bool(chart_context.get("available")):
        entry_chart_score = facade._clamp_score(facade._to_float(chart_context.get("entry_chart_score")))
        exit_risk_score = facade._clamp_score(facade._to_float(chart_context.get("exit_risk_score")))
        late_entry_risk = str(chart_context.get("late_entry_risk") or "").strip().lower()
        breakdown["chart_structure_confirmation"] = round(0.75 * entry_chart_score, 4)
        if late_entry_risk in {"medium", "high"}:
            breakdown["late_entry_risk_penalty"] = -0.25 if late_entry_risk == "medium" else -0.5
        if exit_risk_score >= 0.55:
            breakdown["chart_exit_risk_penalty"] = -0.25
    return breakdown
