"""full_chain_component_review: ``_attribution_component`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _attribution_component(
    *,
    attribution: Mapping[str, Any],
    component: str,
    question: str,
    missing_comparison: str,
    availability: dict[str, Any],
    facade: Any,
) -> dict[str, Any]:
    prefix = "strategist" if component == "strategist" else "commander"
    primary = next(
        (
            row for row in attribution.get("by_horizon") or []
            if row.get("horizon") == "+30m"
        ),
        {},
    )
    count = int(primary.get(f"{prefix}_comparison_count") or 0)
    days = int(primary.get(f"{prefix}_day_count") or 0)
    delta = facade._number(primary.get(f"average_{prefix}_delta_pct"))
    positive_rate = facade._number(primary.get(f"{prefix}_positive_delta_rate"))
    enough = count >= facade.DIRECTIONAL_MIN_OBSERVATIONS and days >= facade.DIRECTIONAL_MIN_DAYS
    material = (
        enough
        and delta is not None
        and positive_rate is not None
        and delta >= facade.MIN_MATERIAL_RANKING_DELTA_PCT
        and positive_rate >= facade.MIN_POSITIVE_RANKING_DELTA_RATE
    )
    if not enough:
        return {
            "decision": facade.DecisionClass.INSUFFICIENT_EVIDENCE.value,
            "question": question,
            "finding": (
                f"{component.title()} has {count} comparable +30m windows across {days} day(s); "
                "the fixed 20-observation and 2-day threshold is not complete."
            ),
            "missing_comparison": (
                f"at least {facade.DIRECTIONAL_MIN_OBSERVATIONS} comparable +30m windows across "
                f"{facade.DIRECTIONAL_MIN_DAYS} days; current={count} windows/{days} days"
            ),
            "availability": dict(availability),
            "primary_horizon": "+30m",
            "metrics": dict(primary),
            "behavior_change_authorized": False,
        }
    return {
        "decision": (
            facade.DecisionClass.PROMOTION_CANDIDATE.value
            if material
            else facade.DecisionClass.ADJUST_AND_RETEST.value
        ),
        "question": question,
        "finding": (
            f"{component.title()} shows a material +30m delta."
            if material
            else f"{component.title()} does not show a material +30m delta under the fixed contract."
        ),
        "missing_comparison": None,
        "primary_horizon": "+30m",
        "metrics": dict(primary),
        "behavior_change_authorized": False,
    }
