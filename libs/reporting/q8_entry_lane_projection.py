"""q8_evaluation_contract projections (moved verbatim from q8_evaluation_contract).

Module globals and helpers are resolved on ``facade`` (the q8_evaluation_contract module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def entry_lane_subtype(row: Mapping[str, Any], *, facade: Any) -> str:
    observation = facade.build_entry_lane_observation(row)
    lane = facade.text_value(observation.get("primary_lane")) or "unknown"
    subtype = facade.text_value(observation.get("subtype")) or "unknown"
    return f"{lane}:{subtype}"
