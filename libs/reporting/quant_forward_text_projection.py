"""quant_shadow_forward_outcomes projections (moved verbatim from quant_shadow_forward_outcomes).

Module globals and helpers are resolved on ``facade`` (the quant_shadow_forward_outcomes module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any


def _text(value: Any) -> str:
    return str(value or "").strip()
