"""scanner_score_decomposition: ``decompose_scanner_score`` body (moved verbatim from ``scanner_score_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def decompose_scanner_score(candidate: Mapping[str, Any] | None, *, facade: Any) -> dict[str, Any]:
    """Return an additive, read-only score view for scanner candidates.

    This does not change ranking behavior. It only separates the fields that are
    often conflated in reports: raw technical quality, strategy context,
    cost/horizon fit, and execution readiness.
    """

    row = candidate if isinstance(candidate, facade.Mapping) else {}
    score_breakdown = facade._nested_mapping(row, "score_breakdown")
    features = facade._nested_mapping(row, "features")
    quant = facade._nested_mapping(row, "quant_factors")
    cost = facade._nested_mapping(row, "cost_filter")
    monitor = facade._nested_mapping(row, "monitor")

    raw_momentum = facade._first_num(
        row,
        (
            "raw_momentum_quality_score",
            "momentum_score",
            "trend_score",
            "breakout_score",
            "score_intrinsic",
        ),
    )
    if raw_momentum is None:
        raw_momentum = facade._first_num(score_breakdown, ("momentum", "trend", "breakout", "intrinsic"))

    strategy_context = facade._first_num(
        row,
        (
            "strategy_context_score",
            "strategist_score",
            "theme_score",
            "rank_score",
        ),
    )
    if strategy_context is None:
        strategy_context = facade._first_num(score_breakdown, ("strategy", "strategist", "theme", "rank_score"))

    cost_horizon = facade._first_num(
        row,
        (
            "cost_horizon_fit_score",
            "cost_adjusted_edge_pct",
            "expected_edge_pct",
            "reward_room_pct",
        ),
    )
    if cost_horizon is None:
        cost_horizon = facade._first_num(cost, ("cost_adjusted_edge_pct", "expected_edge_pct"))
    if cost_horizon is None:
        cost_horizon = facade._first_num(quant, ("cost_adjusted_edge_pct", "reward_room_pct"))
    if cost_horizon is None:
        cost_horizon = facade._first_num(features, ("reward_room_pct", "expected_move_pct"))

    execution_readiness = facade._first_num(
        row,
        (
            "execution_readiness_score",
            "entry_quality_score",
            "transition_readiness_score",
            "confidence_score",
        ),
    )
    if execution_readiness is None:
        execution_readiness = facade._first_num(monitor, ("entry_quality_score", "transition_readiness_score"))
    if execution_readiness is None:
        execution_readiness = facade._first_num(quant, ("entry_quality_score", "confidence_score"))

    return {
        "schema_version": "scanner_score_decomposition.v1",
        "behavior_effect": "observation_only",
        "symbol": str(row.get("symbol") or ""),
        "rank": row.get("rank"),
        "total_score": facade._first_num(row, ("score_total", "score", "combined_score")),
        "raw_momentum_quality_score": raw_momentum,
        "strategy_context_score": strategy_context,
        "cost_horizon_fit_score": cost_horizon,
        "execution_readiness_score": execution_readiness,
        "source_fields_present": {
            "score_breakdown": bool(score_breakdown),
            "features": bool(features),
            "quant_factors": bool(quant),
            "cost_filter": bool(cost),
            "monitor": bool(monitor),
        },
        "limitations": [
            "Field names vary by artifact source; missing components mean unavailable, not zero.",
            "This decomposition is report-only and does not alter scanner ranking.",
        ],
    }
