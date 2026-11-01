"""output_snapshots projections (moved verbatim from output_snapshots).

Module globals and helpers are resolved on ``facade`` (the output_snapshots module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any


def to_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return float(default)
