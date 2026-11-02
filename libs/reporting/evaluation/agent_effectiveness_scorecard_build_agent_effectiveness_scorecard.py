"""agent_effectiveness_scorecard: ``build_agent_effectiveness_scorecard`` body (moved verbatim from ``agent_effectiveness_scorecard``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def build_agent_effectiveness_scorecard(
    full_chain_review: Mapping[str, Any],
    *,
    facade: Any,
) -> dict[str, Any]:
    evidence = facade._mapping(full_chain_review.get("evidence"))
    attribution = facade._mapping(evidence.get("decision_window_attribution"))
    primary = next(
        (
            dict(row)
            for row in attribution.get("by_horizon") or []
            if isinstance(row, facade.Mapping) and row.get("horizon") == "+30m"
        ),
        {},
    )
    components = facade._mapping(full_chain_review.get("component_decisions"))
    scanner = facade._mapping(components.get("scanner"))
    scanner_measurable = str(scanner.get("decision") or "") != "INSUFFICIENT_EVIDENCE"
    scanner_relative = (
        "VALUE_ADD"
        if scanner_measurable and bool(scanner.get("relative_ranking_effect_positive"))
        else "DEGRADING"
        if scanner_measurable
        else "NOT_MEASURABLE"
    )
    scanner_absolute = (
        "VALUE_ADD"
        if scanner_measurable and bool(scanner.get("absolute_cost_adjusted_edge_positive"))
        else "DEGRADING"
        if scanner_measurable
        else "NOT_MEASURABLE"
    )
    overlay_metrics = {
        "strategy_ranking_overlay_comparison_count": primary.get(
            "strategy_ranking_overlay_comparison_count",
            primary.get("strategist_comparison_count"),
        ),
        "strategy_ranking_overlay_day_count": primary.get(
            "strategy_ranking_overlay_day_count",
            primary.get("strategist_day_count"),
        ),
        "average_strategy_ranking_overlay_delta_pct": primary.get(
            "average_strategy_ranking_overlay_delta_pct",
            primary.get("average_strategist_delta_pct"),
        ),
        "strategy_ranking_overlay_positive_delta_rate": primary.get(
            "strategy_ranking_overlay_positive_delta_rate",
            primary.get("strategist_positive_delta_rate"),
        ),
    }
    overlay = facade._delta_state(
        overlay_metrics,
        prefix="strategy_ranking_overlay",
        missing_control="paired same-universe intrinsic and strategy-weighted outcomes",
    )
    refresh = facade._delta_state(
        primary,
        prefix="post_scanner_refresh",
        missing_control="paired first-Scanner and post-refresh Scanner outcomes",
    )
    commander = facade._delta_state(
        primary,
        prefix="commander",
        missing_control="paired presented-candidate and Commander approve/veto outcomes",
    )
    trade_total = int(evidence.get("total_trade_model_count") or 0)
    excluded = int(evidence.get("excluded_trade_model_count") or 0)
    return {
        "schema_version": "agent_effectiveness_scorecard.v1",
        "contract_version": facade.CONTRACT_VERSION,
        "behavior_effect": "evaluation_only",
        "range": dict(facade._mapping(full_chain_review.get("range"))),
        "runtime_order": [
            "commander_operating_context",
            "strategist_initial_frame",
            "strategy_guided_scanner",
            "optional_post_scanner_strategist_refresh",
            "optional_scanner_rerun",
            "monitor_entry",
            "commander_decision",
            "execution",
            "monitor_exit_horizon",
        ],
        "state_contract": [
            "NOT_MEASURABLE",
            "DEFECT",
            "DEGRADING",
            "NEUTRAL",
            "VALUE_ADD",
        ],
        "integrity": {
            "state": "PASS_WITH_EXCLUSIONS" if excluded else "PASS",
            "trade_model_count": trade_total,
            "excluded_trade_model_count": excluded,
        },
        "components": {
            "scanner": {
                "relative_ranking_state": scanner_relative,
                "absolute_edge_state": scanner_absolute,
                "question": "Given the Strategist frame, did Scanner rank cost-positive candidates well?",
                "source": "q9_full_chain_component_review.component_decisions.scanner",
            },
            "strategist": {
                "full_contribution": {
                    "state": "NOT_MEASURABLE",
                    "reason": "Strategist runs before Scanner and influences candidate sourcing.",
                    "missing_control": "parallel strategy-neutral candidate sourcing and ranking shadow",
                },
                "scenario_quality": {
                    "state": "NOT_MEASURABLE",
                    "reason": "scenario forecasts are not yet joined to a fixed subsequent-market target in this scorecard",
                    "missing_control": "scenario/horizon forecast outcome join",
                },
                "ranking_overlay": overlay,
                "post_scanner_refresh": refresh,
            },
            "commander": commander,
            "monitor_entry": {
                "state": facade._decision_state(facade._mapping(components.get("monitor_entry"))),
                "source_decision": facade._mapping(components.get("monitor_entry")).get("decision"),
                "reason": facade._mapping(components.get("monitor_entry")).get("finding"),
            },
            "monitor_exit_horizon": {
                "state": facade._decision_state(facade._mapping(components.get("monitor_exit"))),
                "source_decision": facade._mapping(components.get("monitor_exit")).get("decision"),
                "reason": facade._mapping(components.get("monitor_exit")).get("finding"),
            },
            "full_system": {
                "state": facade._decision_state(facade._mapping(components.get("full_system"))),
                "source_decision": facade._mapping(components.get("full_system")).get("decision"),
                "reason": facade._mapping(components.get("full_system")).get("finding"),
            },
        },
        "controls": {
            "A_SCANNER_CONTROL": {
                "semantic_role": "SCANNER_INTRINSIC_SAME_UNIVERSE",
                "full_pre_strategist_control": False,
            },
            "B_STRATEGIST_RANKED": {
                "semantic_role": "STRATEGY_WEIGHTED_SCANNER_RANKING",
            },
            "R1_PRE_REFRESH_SCANNER": {
                "semantic_role": "SCANNER_BEFORE_POST_SCANNER_STRATEGIST_REFRESH",
            },
            "R2_POST_REFRESH_SCANNER": {
                "semantic_role": "SCANNER_AFTER_POST_SCANNER_STRATEGIST_REFRESH",
            },
        },
        "behavior_change_authorized": False,
    }
