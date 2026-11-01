"""q8_lane_decision_table projections (moved verbatim from q8_lane_decision_table).

Module globals and helpers are resolved on ``facade`` (the q8_lane_decision_table module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, Mapping


def _counts_by_name(rows: Iterable[Mapping[str, Any]], *, facade: Any) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for row in rows:
        name = facade._text(row.get("name"))
        if name:
            out[name] = facade._int(row.get("count"))
    return out
