"""quant_shadow_forward_outcomes projections (moved verbatim from quant_shadow_forward_outcomes).

Module globals and helpers are resolved on ``facade`` (the quant_shadow_forward_outcomes module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any


def _parse_raw_ts_epoch(value: Any, *, facade: Any) -> int:
    text = facade._text(value)
    if len(text) >= 14 and text[:14].isdigit():
        try:
            return int(facade.datetime.strptime(text[:14], "%Y%m%d%H%M%S").replace(tzinfo=facade.KST).timestamp())
        except Exception:
            return 0
    return facade._parse_epoch(text)
