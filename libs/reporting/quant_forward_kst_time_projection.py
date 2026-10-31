"""quant_shadow_forward_outcomes projections (moved verbatim from quant_shadow_forward_outcomes).

Module globals and helpers are resolved on ``facade`` (the quant_shadow_forward_outcomes module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Mapping


def _kst_time_tuple(row: Mapping[str, Any], *, facade: Any) -> tuple[int, int]:
    epoch = facade._parse_raw_ts_epoch(row.get("raw_ts")) or facade._to_int(row.get("ts"), 0)
    if epoch <= 0:
        return (0, 0)
    dt = facade.datetime.fromtimestamp(epoch, tz=facade.KST)
    return (dt.hour, dt.minute)
