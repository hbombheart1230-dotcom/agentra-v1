"""q8_evaluation_contract projections (moved verbatim from q8_evaluation_contract).

Module globals and helpers are resolved on ``facade`` (the q8_evaluation_contract module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def promotion_candidate_is_repeatable(row: Mapping[str, Any], *, facade: Any) -> bool:
    observed_count = int(row.get("observed_count") or 0)
    observed_day_count = int(row.get("observed_day_count") or 0)
    avg_return_5m = float(row.get("avg_return_5m_pct") or 0.0)
    avg_return_15m = float(row.get("avg_return_15m_pct") or 0.0)
    return (
        observed_count >= facade.PROMOTION_CANDIDATE_MIN_OBSERVED
        and observed_day_count >= facade.PROMOTION_CANDIDATE_MIN_DAYS
        and avg_return_5m > 0.0
        and avg_return_15m > 0.0
    )
