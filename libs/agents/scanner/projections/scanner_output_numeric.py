"""output_payloads projections (moved verbatim from output_payloads).

Module globals and helpers are resolved on ``facade`` (the output_payloads module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any


def _to_float(value: Any, default: float = 0.0) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)
