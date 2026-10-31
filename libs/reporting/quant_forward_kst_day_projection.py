"""quant_shadow_forward_outcomes projections (moved verbatim from quant_shadow_forward_outcomes).

Module globals and helpers are resolved on ``facade`` (the quant_shadow_forward_outcomes module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any


def _kst_day_from_epoch(value: Any, *, facade: Any) -> str:
    epoch = facade._to_int(value, 0)
    if epoch <= 0:
        return ""
    try:
        return facade.datetime.fromtimestamp(epoch, tz=facade.KST).strftime("%Y%m%d")
    except Exception:
        return ""
