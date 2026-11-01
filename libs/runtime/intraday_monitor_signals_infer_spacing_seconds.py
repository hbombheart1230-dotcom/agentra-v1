from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence

import statistics


def _infer_spacing_seconds(candles: Sequence[Mapping[str, Any]], *, facade: Any):
    ts_values: List[int] = []
    for row in candles:
        ts = facade._to_int(row.get("ts"), 0)
        if ts > 0:
            ts_values.append(ts)
    if len(ts_values) < 4:
        return None
    diffs: List[int] = []
    for prev_ts, cur_ts in zip(ts_values, ts_values[1:]):
        diff = int(cur_ts) - int(prev_ts)
        if diff > 0:
            diffs.append(diff)
    if len(diffs) < 3:
        return None
    try:
        return float(statistics.median(diffs))
    except Exception:
        return None
