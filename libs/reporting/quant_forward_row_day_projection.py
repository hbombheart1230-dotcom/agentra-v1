"""quant_shadow_forward_outcomes projections (moved verbatim from quant_shadow_forward_outcomes).

Module globals and helpers are resolved on ``facade`` (the quant_shadow_forward_outcomes module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def _row_day(row: Mapping[str, Any], *, facade: Any) -> str:
    raw_ts = facade._text(row.get("raw_ts"))
    if len(raw_ts) >= 8 and raw_ts[:8].isdigit():
        return raw_ts[:8]
    return facade._kst_day_from_epoch(row.get("ts"))
