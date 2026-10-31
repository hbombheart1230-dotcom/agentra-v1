"""quant_tactic_evaluation projections (moved verbatim from quant_tactic_evaluation).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_evaluation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any


def _text(value: Any) -> str:
    text = str(value or "").strip()
    return "" if text.lower() in {"", "-", "none", "null", "unknown", "not_captured"} else text
