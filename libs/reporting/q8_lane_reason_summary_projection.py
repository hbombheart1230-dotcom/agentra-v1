"""q8_lane_decision_table projections (moved verbatim from q8_lane_decision_table).

Module globals and helpers are resolved on ``facade`` (the q8_lane_decision_table module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def _reason_summary(evaluation: Mapping[str, Any], *, limit: int = 6, facade: Any) -> str:
    parts = []
    for row in facade._rows(evaluation.get("by_reason"))[:limit]:
        name = facade._text(row.get("name"))
        if name:
            parts.append(f"{name} {row.get('count') or 0}")
    return ", ".join(parts) if parts else "-"
