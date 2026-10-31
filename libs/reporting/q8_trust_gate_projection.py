"""q8_evaluation_contract projections (moved verbatim from q8_evaluation_contract).

Module globals and helpers are resolved on ``facade`` (the q8_evaluation_contract module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def build_q8_trust_gate(
    *,
    raw_candidate_count: int,
    deduped_candidate_count: int,
    trusted_forward_count: int,
    trusted_forward_coverage: float,
    candidate_watchlist: Sequence[Mapping[str, Any]],
    facade: Any,
) -> Dict[str, Any]:
    duplicate_count = max(0, int(raw_candidate_count) - int(deduped_candidate_count))
    duplicate_rate = (
        round(float(duplicate_count) / float(raw_candidate_count), 4)
        if raw_candidate_count
        else 0.0
    )
    repeatable = [row for row in candidate_watchlist if facade.promotion_candidate_is_repeatable(row)]
    reasons: List[str] = []
    if trusted_forward_count < facade.TRUSTED_FORWARD_MIN_COUNT:
        reasons.append("trusted_forward_sample_below_100")
    if trusted_forward_coverage < facade.TRUSTED_FORWARD_MIN_COVERAGE:
        reasons.append("trusted_forward_coverage_below_70pct")
    if duplicate_rate > facade.DUPLICATE_RATE_MAX:
        reasons.append("duplicate_rate_above_75pct")
    if not repeatable:
        reasons.append("no_repeatable_promotion_watch_candidate")

    promotion_allowed = not reasons
    if promotion_allowed:
        status = facade.TRUST_GATE_STATUS_READY
    elif "trusted_forward_sample_below_100" in reasons or "trusted_forward_coverage_below_70pct" in reasons:
        status = facade.TRUST_GATE_STATUS_SAMPLE_BLOCKED
    else:
        status = facade.TRUST_GATE_STATUS_NO_REPEATABLE_CANDIDATE

    return {
        "status": status,
        "promotion_allowed": bool(promotion_allowed),
        "block_reasons": reasons,
        "trusted_forward_count": int(trusted_forward_count),
        "trusted_forward_coverage": round(float(trusted_forward_coverage), 4),
        "duplicate_rate": duplicate_rate,
        "duplicate_count": duplicate_count,
        "minimums": {
            "trusted_forward_count": facade.TRUSTED_FORWARD_MIN_COUNT,
            "trusted_forward_coverage": facade.TRUSTED_FORWARD_MIN_COVERAGE,
            "duplicate_rate_max": facade.DUPLICATE_RATE_MAX,
            "candidate_observed_count": facade.PROMOTION_CANDIDATE_MIN_OBSERVED,
            "candidate_observed_day_count": facade.PROMOTION_CANDIDATE_MIN_DAYS,
        },
    }
