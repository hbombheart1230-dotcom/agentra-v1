"""full_chain_component_review: ``_decision_window_attribution`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _decision_window_attribution(
    payloads: list[dict[str, Any]],
    *,
    cost_pct: float,
    facade: Any,
) -> dict[str, Any]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = facade.defaultdict(
        lambda: facade.defaultdict(list)
    )
    for row in facade._q9_decision_candidate_rows(payloads):
        decision_id = str(row.get("q9_decision_id") or "")
        role = str(row.get("q9_decision_role") or "")
        if decision_id and role:
            grouped[decision_id][role].append(row)
    by_horizon: list[dict[str, Any]] = []
    for horizon in facade.HORIZONS:
        strategist_deltas: list[float] = []
        refresh_deltas: list[float] = []
        commander_deltas: list[float] = []
        strategist_days: set[str] = set()
        refresh_days: set[str] = set()
        commander_days: set[str] = set()
        for roles in grouped.values():
            a_row = facade._q9_role_row(roles, "A_SCANNER_CONTROL")
            b_row = facade._q9_role_row(roles, "B_STRATEGIST_RANKED")
            r1_row = facade._q9_role_row(roles, "R1_PRE_REFRESH_SCANNER")
            r2_row = facade._q9_role_row(roles, "R2_POST_REFRESH_SCANNER")
            c_row = facade._q9_role_row(roles, "C_COMMANDER_FINAL")
            a_value = facade._checkpoint_return(a_row, horizon) if a_row else None
            b_value = facade._checkpoint_return(b_row, horizon) if b_row else None
            if a_value is not None and b_value is not None:
                strategist_deltas.append(b_value - a_value)
                day = facade.candidate_day(b_row)
                if day:
                    strategist_days.add(day)
            r1_value = facade._checkpoint_return(r1_row, horizon) if r1_row else None
            r2_value = facade._checkpoint_return(r2_row, horizon) if r2_row else None
            if r1_value is not None and r2_value is not None:
                refresh_deltas.append(r2_value - r1_value)
                day = facade.candidate_day(r2_row)
                if day:
                    refresh_days.add(day)
            if b_value is None or not c_row:
                continue
            if c_row.get("q9_commander_no_trade"):
                c_net = 0.0
            else:
                c_value = facade._checkpoint_return(c_row, horizon)
                if c_value is None:
                    continue
                c_net = c_value - cost_pct
            b_net = b_value - cost_pct
            commander_deltas.append(c_net - b_net)
            day = facade.candidate_day(c_row)
            if day:
                commander_days.add(day)
        by_horizon.append(
            {
                "horizon": horizon,
                "strategist_comparison_count": len(strategist_deltas),
                "strategist_day_count": len(strategist_days),
                "average_strategist_delta_pct": (
                    round(sum(strategist_deltas) / len(strategist_deltas), 4)
                    if strategist_deltas
                    else None
                ),
                "strategist_positive_delta_rate": (
                    round(sum(value > 0 for value in strategist_deltas) / len(strategist_deltas), 4)
                    if strategist_deltas
                    else None
                ),
                "strategy_ranking_overlay_comparison_count": len(strategist_deltas),
                "strategy_ranking_overlay_day_count": len(strategist_days),
                "average_strategy_ranking_overlay_delta_pct": (
                    round(sum(strategist_deltas) / len(strategist_deltas), 4)
                    if strategist_deltas
                    else None
                ),
                "strategy_ranking_overlay_positive_delta_rate": (
                    round(sum(value > 0 for value in strategist_deltas) / len(strategist_deltas), 4)
                    if strategist_deltas
                    else None
                ),
                "post_scanner_refresh_comparison_count": len(refresh_deltas),
                "post_scanner_refresh_day_count": len(refresh_days),
                "average_post_scanner_refresh_delta_pct": (
                    round(sum(refresh_deltas) / len(refresh_deltas), 4)
                    if refresh_deltas
                    else None
                ),
                "post_scanner_refresh_positive_delta_rate": (
                    round(sum(value > 0 for value in refresh_deltas) / len(refresh_deltas), 4)
                    if refresh_deltas
                    else None
                ),
                "commander_comparison_count": len(commander_deltas),
                "commander_day_count": len(commander_days),
                "average_commander_delta_pct": (
                    round(sum(commander_deltas) / len(commander_deltas), 4)
                    if commander_deltas
                    else None
                ),
                "commander_positive_delta_rate": (
                    round(sum(value > 0 for value in commander_deltas) / len(commander_deltas), 4)
                    if commander_deltas
                    else None
                ),
            }
        )
    return {
        "schema_version": "q9_decision_window_attribution.v1",
        "role_semantics": {
            "A_SCANNER_CONTROL": "same-universe intrinsic Scanner ranking; not a full pre-Strategist control",
            "B_STRATEGIST_RANKED": "strategy-weighted Scanner ranking",
            "R1_PRE_REFRESH_SCANNER": "first Scanner result before optional tactical refresh",
            "R2_POST_REFRESH_SCANNER": "Scanner result after optional tactical refresh",
            "C_COMMANDER_FINAL": "Commander final approval or veto",
        },
        "full_strategist_contribution_status": "NOT_MEASURABLE",
        "full_strategist_missing_control": "strategy-neutral candidate sourcing and ranking shadow",
        "decision_window_count": len(grouped),
        "candidate_row_count": sum(
            len(rows) for roles in grouped.values() for rows in roles.values()
        ),
        "by_horizon": by_horizon,
    }
