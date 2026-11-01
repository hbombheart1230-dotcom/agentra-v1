"""q8_lane_decision_table projections (moved verbatim from q8_lane_decision_table).

Module globals and helpers are resolved on ``facade`` (the q8_lane_decision_table module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any


def _text(value: Any) -> str:
    return str(value or "").strip()
