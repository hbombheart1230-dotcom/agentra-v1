"""quant_tactic_report projections (moved verbatim from quant_tactic_report).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_report module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, List, Mapping


def render_quant_tactic_report_lines(report: Mapping[str, Any] | None, *, compact: bool = False, facade: Any) -> List[str]:
    surface = facade.quant_tactic_surface(report)
    if not surface:
        return []
    entry = facade._mapping(surface.get("entry_quant_decision"))
    exit_decision = facade._mapping(surface.get("exit_quant_decision"))
    factors = facade._mapping(surface.get("factors"))
    suitability = facade._mapping(surface.get("tactic_suitability"))
    lines: List[str] = []
    tactic = surface.get("tactic_id") or "-"
    playbook = surface.get("playbook") or "-"
    if compact:
        lines.append(f"* 전술 진단: `{tactic}` / 플레이북 `{playbook}`")
    else:
        lines.append(f"- 전술 ID: `{tactic}`")
        lines.append(f"- 플레이북: `{playbook}`")
    if suitability:
        lines.append(
            f"- 스캐너 전술 적합도: {suitability.get('tier') or '-'} "
            f"({facade._fmt(suitability.get('score'))})"
        )
    if entry:
        lines.append(
            f"- 진입 quant 판단: {facade._decision_label(entry.get('decision'))} "
            f"/ blocker={facade._reason_text(entry.get('blockers'))} "
            f"/ warning={facade._reason_text(entry.get('warnings'))}"
        )
        cost = facade._mapping(entry.get("cost_edge"))
        if cost:
            lines.append(
                f"- 비용 엣지: {'통과' if cost.get('ok') else '미통과'} "
                f"/ edge={facade._pct(cost.get('cost_adjusted_edge_pct'))} "
                f"/ drag={facade._pct(cost.get('cost_drag_pct'))}"
            )
        if bool(entry.get("commander_override_required")):
            lines.append(f"- commander override 필요 항목: {facade._reason_text(entry.get('override_reason_required_for'))}")
    if exit_decision:
        lines.append(
            f"- 청산 quant 판단: {facade._decision_label(exit_decision.get('decision'))} "
            f"/ hard_exit={'예' if exit_decision.get('hard_exit') else '아니오'} "
            f"/ confirmation_pending={'예' if exit_decision.get('confirmation_pending') else '아니오'}"
        )
        if exit_decision.get("early_exit_flag") or exit_decision.get("actual_hold_sec") not in (None, ""):
            window = facade._mapping(exit_decision.get("expected_hold_window"))
            lines.append(
                f"- 보유시간 비교: 실제 {facade._fmt(exit_decision.get('actual_hold_sec'))}초 "
                f"/ 기대 최소 {facade._fmt(window.get('min_sec'))}초 "
                f"/ mismatch={'예' if exit_decision.get('hold_window_mismatch') else '아니오'}"
            )
        if exit_decision.get("blockers") or exit_decision.get("warnings"):
            lines.append(
                f"- 청산 진단 사유: blocker={facade._reason_text(exit_decision.get('blockers'))} "
                f"/ warning={facade._reason_text(exit_decision.get('warnings'))}"
            )
    if not compact and factors:
        factor_bits = []
        for key in ("vwap_distance_pct", "volume_ratio", "cost_floor_state", "confidence_score", "human_chart_entry_score"):
            if factors.get(key) not in (None, ""):
                factor_bits.append(f"{key}={facade._fmt(factors.get(key))}")
        if factor_bits:
            lines.append("- 핵심 factor snapshot: " + ", ".join(factor_bits[:6]))
    return lines
