"""full_chain_component_review: ``_scanner_decision`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _scanner_decision(
    *,
    role_metrics: list[dict[str, Any]],
    paired: list[dict[str, Any]],
    facade: Any,
) -> dict[str, Any]:
    top_30 = next(
        (row for row in role_metrics if row["role"] == "top_pick" and row["horizon"] == "+30m"),
        {},
    )
    pair_30 = next((row for row in paired if row["horizon"] == "+30m"), {})
    enough = (
        int(pair_30.get("paired_window_count") or 0) >= facade.DIRECTIONAL_MIN_OBSERVATIONS
        and int(pair_30.get("observed_day_count") or 0) >= facade.DIRECTIONAL_MIN_DAYS
    )
    relative_positive = (
        enough
        and float(pair_30.get("average_delta_pct") or 0.0) >= facade.MIN_MATERIAL_RANKING_DELTA_PCT
        and float(pair_30.get("positive_delta_rate") or 0.0) >= facade.MIN_POSITIVE_RANKING_DELTA_RATE
    )
    absolute_positive = float(top_30.get("expectancy_pct") or 0.0) > 0
    decision = (
        facade.DecisionClass.RETAIN.value
        if relative_positive and absolute_positive
        else facade.DecisionClass.ADJUST_AND_RETEST.value
        if relative_positive
        else facade.DecisionClass.ADJUST_AND_RETEST.value
        if enough
        else facade.DecisionClass.INSUFFICIENT_EVIDENCE.value
    )
    return {
        "decision": decision,
        "question": "Does Scanner ranking put stronger candidates ahead of runner-ups and retain cost-positive edge?",
        "relative_ranking_effect_positive": relative_positive,
        "absolute_cost_adjusted_edge_positive": absolute_positive,
        "primary_horizon": "+30m",
        "finding": (
            "Top-pick ordering is directionally better than evaluated runner-ups, but the selected "
            "Top-pick set remains cost-negative; ranking direction is useful while candidate quality "
            "and horizon calibration require adjustment."
            if relative_positive and not absolute_positive
            else "Scanner Top-pick ordering does not establish a material ranking effect after "
            "applying the fixed +0.30% delta and 55% positive-window thresholds."
            if not relative_positive
            else "Scanner ranking and absolute cost-adjusted edge are both positive."
        ),
        "missing_comparison": None if enough else "paired Top-pick and runner-up forward outcomes",
        "materiality_contract": {
            "minimum_average_delta_pct": facade.MIN_MATERIAL_RANKING_DELTA_PCT,
            "minimum_positive_delta_rate": facade.MIN_POSITIVE_RANKING_DELTA_RATE,
        },
    }
