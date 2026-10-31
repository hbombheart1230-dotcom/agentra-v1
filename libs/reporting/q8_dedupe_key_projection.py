"""q8_evaluation_contract projections (moved verbatim from q8_evaluation_contract).

Module globals and helpers are resolved on ``facade`` (the q8_evaluation_contract module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def canonical_dedupe_key(row: Mapping[str, Any], *, facade: Any) -> tuple[str, str, int, str]:
    base = facade.forward_base(row)
    try:
        baseline_epoch = int(float(base.get("baseline_epoch") or 0))
    except Exception:
        baseline_epoch = 0
    return (
        facade.candidate_day(row),
        facade.text_value(row.get("symbol")).upper(),
        baseline_epoch,
        facade.entry_lane_subtype(row),
    )
