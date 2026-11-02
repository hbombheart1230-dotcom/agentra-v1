"""agent_effectiveness_scorecard: ``_delta_state`` body (moved verbatim from ``agent_effectiveness_scorecard``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _delta_state(
    metrics: Mapping[str, Any],
    *,
    prefix: str,
    missing_control: str,
    facade: Any,
) -> dict[str, Any]:
    count = int(metrics.get(f"{prefix}_comparison_count") or 0)
    days = int(metrics.get(f"{prefix}_day_count") or 0)
    delta = facade._number(metrics.get(f"average_{prefix}_delta_pct"))
    positive_rate = facade._number(metrics.get(f"{prefix}_positive_delta_rate"))
    enough = count >= facade.DIRECTIONAL_MIN_OBSERVATIONS and days >= facade.DIRECTIONAL_MIN_DAYS
    if not enough or delta is None or positive_rate is None:
        state = "NOT_MEASURABLE"
        reason = (
            f"requires {facade.DIRECTIONAL_MIN_OBSERVATIONS} paired observations across "
            f"{facade.DIRECTIONAL_MIN_DAYS} days; current={count}/{days}"
        )
    elif delta >= facade.MIN_MATERIAL_DELTA_PCT and positive_rate >= facade.MIN_POSITIVE_RATE:
        state = "VALUE_ADD"
        reason = "paired cost-adjusted effect meets the fixed positive materiality contract"
    elif delta <= -facade.MIN_MATERIAL_DELTA_PCT and positive_rate <= facade.MAX_DEGRADING_POSITIVE_RATE:
        state = "DEGRADING"
        reason = "paired cost-adjusted effect meets the fixed negative materiality contract"
    else:
        state = "NEUTRAL"
        reason = "paired effect is measurable but does not meet positive or negative materiality"
    return {
        "state": state,
        "reason": reason,
        "comparison_count": count,
        "day_count": days,
        "average_delta_pct": delta,
        "positive_delta_rate": positive_rate,
        "missing_control": missing_control if state == "NOT_MEASURABLE" else None,
    }
