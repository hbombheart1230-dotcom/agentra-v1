"""q8_trusted_reaggregation projections (moved verbatim from q8_trusted_reaggregation).

Module globals and helpers are resolved on ``facade`` (the q8_trusted_reaggregation module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any


def _fmt_num(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except Exception:
        return "0"
