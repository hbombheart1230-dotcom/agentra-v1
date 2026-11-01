"""quant_shadow_forward_outcomes projections (moved verbatim from quant_shadow_forward_outcomes).

Module globals and helpers are resolved on ``facade`` (the quant_shadow_forward_outcomes module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict


def _normalize_rows(value: Any, *, facade: Any) -> list[Dict[str, Any]]:
    if isinstance(value, facade.Mapping) and isinstance(value.get("rows"), list):
        raw_rows = value.get("rows") or []
    elif isinstance(value, list):
        raw_rows = value
    else:
        raw_rows = []
    rows: list[Dict[str, Any]] = []
    for raw in raw_rows:
        if not isinstance(raw, facade.Mapping):
            continue
        ts = facade._to_int(raw.get("ts"), 0)
        close = facade._to_float(raw.get("close") or raw.get("price"), None)
        if ts <= 0 or close is None or close <= 0:
            continue
        high = facade._to_float(raw.get("high"), close) or close
        low = facade._to_float(raw.get("low"), close) or close
        rows.append(
            {
                "ts": ts,
                "close": float(close),
                "high": float(high),
                "low": float(low),
                "raw_ts": facade._text(raw.get("raw_ts") or raw.get("datetime") or raw.get("time")),
            }
        )
    rows.sort(key=lambda item: int(item["ts"]))
    return rows
