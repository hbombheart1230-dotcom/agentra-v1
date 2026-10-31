from __future__ import annotations

import sys
from typing import Any, Dict, List, Mapping, Sequence

from libs.runtime.quant.entry_lane_observation import build_entry_lane_observation
from libs.reporting import q8_candidate_day_projection as _o6a8_owner
from libs.reporting import q8_text_value_projection as _o7a1_owner
from libs.reporting import q8_forward_base_projection as _o7a2_owner
from libs.reporting import q8_dedupe_key_projection as _o7a3_owner
from libs.reporting import q8_dedupe_candidates_projection as _o7a4_owner
from libs.reporting import q8_repeatable_projection as _o7a5_owner
from libs.reporting import q8_entry_lane_projection as _o7a6_owner
from libs.reporting import q8_trust_gate_projection as _o7a7_owner


TRUSTED_FORWARD_MIN_COUNT = 100
TRUSTED_FORWARD_MIN_COVERAGE = 0.70
DUPLICATE_RATE_MAX = 0.75
PROMOTION_CANDIDATE_MIN_OBSERVED = 50
PROMOTION_CANDIDATE_MIN_DAYS = 2
FORWARD_MAX_OBSERVATION_DELAY_SEC = 180

CANONICAL_DEDUPE_KEY_FIELDS = ["day", "symbol", "baseline_epoch", "entry_lane_subtype"]

TRUST_GATE_STATUS_READY = "promotion_review_ready"
TRUST_GATE_STATUS_SAMPLE_BLOCKED = "promotion_blocked_sample_or_coverage"
TRUST_GATE_STATUS_NO_REPEATABLE_CANDIDATE = "promotion_blocked_no_repeatable_candidate"


def text_value(value: Any) -> str:
    return _o7a1_owner.text_value(value)


def forward_base(row: Mapping[str, Any]) -> Dict[str, Any]:
    return _o7a2_owner.forward_base(row, facade=sys.modules[__name__])


def candidate_day(row: Mapping[str, Any]) -> str:
    return _o6a8_owner.candidate_day(row, facade=sys.modules[__name__])


def entry_lane_subtype(row: Mapping[str, Any]) -> str:
    return _o7a6_owner.entry_lane_subtype(row, facade=sys.modules[__name__])


def canonical_dedupe_key(row: Mapping[str, Any]) -> tuple[str, str, int, str]:
    return _o7a3_owner.canonical_dedupe_key(row, facade=sys.modules[__name__])


def dedupe_q8_candidates(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return _o7a4_owner.dedupe_q8_candidates(rows, facade=sys.modules[__name__])


def promotion_candidate_is_repeatable(row: Mapping[str, Any]) -> bool:
    return _o7a5_owner.promotion_candidate_is_repeatable(row, facade=sys.modules[__name__])


def build_q8_trust_gate(
    *,
    raw_candidate_count: int,
    deduped_candidate_count: int,
    trusted_forward_count: int,
    trusted_forward_coverage: float,
    candidate_watchlist: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    return _o7a7_owner.build_q8_trust_gate(raw_candidate_count=raw_candidate_count, deduped_candidate_count=deduped_candidate_count, trusted_forward_count=trusted_forward_count, trusted_forward_coverage=trusted_forward_coverage, candidate_watchlist=candidate_watchlist, facade=sys.modules[__name__])


__all__ = [
    "CANONICAL_DEDUPE_KEY_FIELDS",
    "DUPLICATE_RATE_MAX",
    "FORWARD_MAX_OBSERVATION_DELAY_SEC",
    "PROMOTION_CANDIDATE_MIN_DAYS",
    "PROMOTION_CANDIDATE_MIN_OBSERVED",
    "TRUSTED_FORWARD_MIN_COUNT",
    "TRUSTED_FORWARD_MIN_COVERAGE",
    "build_q8_trust_gate",
    "candidate_day",
    "canonical_dedupe_key",
    "dedupe_q8_candidates",
    "entry_lane_subtype",
    "forward_base",
    "promotion_candidate_is_repeatable",
    "text_value",
]
