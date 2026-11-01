from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _normalize_minute_rows(value: Any, *, facade: Any):
    if isinstance(value, Mapping) and isinstance(value.get("rows"), list):
        raw_rows = list(value.get("rows") or [])
    elif isinstance(value, list):
        raw_rows = list(value)
    else:
        raw_rows = []
    rows: List[Dict[str, Any]] = []
    for raw in raw_rows:
        if not isinstance(raw, Mapping):
            continue
        ts = facade._float(raw.get("ts"), None)
        close = facade._float(raw.get("close") or raw.get("price"), None)
        if ts is None or close is None or close <= 0:
            continue
        rows.append(
            {
                "ts": int(ts),
                "open": facade._float(raw.get("open"), close),
                "high": facade._float(raw.get("high"), close),
                "low": facade._float(raw.get("low"), close),
                "close": float(close),
                "volume": facade._float(raw.get("volume"), None),
                "raw_ts": facade._text(raw.get("raw_ts") or raw.get("datetime") or raw.get("time")),
            }
        )
    rows.sort(key=lambda item: int(item["ts"]))
    return rows
