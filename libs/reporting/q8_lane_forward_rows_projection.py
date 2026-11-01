"""q8_lane_decision_table projections (moved verbatim from q8_lane_decision_table).

Module globals and helpers are resolved on ``facade`` (the q8_lane_decision_table module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, List, Mapping


def _forward_rows(evaluation: Mapping[str, Any], *, facade: Any) -> List[Dict[str, Any]]:
    forward = evaluation.get("entry_lane_forward_outcomes")
    if not isinstance(forward, facade.Mapping):
        return []
    return facade._rows(forward.get("by_primary_lane"))
