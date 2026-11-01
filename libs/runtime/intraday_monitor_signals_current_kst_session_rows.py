from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence


def _current_kst_session_rows(candles: Sequence[Mapping[str, Any]], *, facade: Any):
    latest_key, start_idx, _latest_minute = facade._current_kst_session_anchor(candles)
    if latest_key is None or start_idx is None:
        return []
    out: List[Mapping[str, Any]] = []
    for row in candles[start_idx:]:
        row_key, row_minute = facade._kst_session_key_and_minute(row.get("ts"))
        if row_key == latest_key and row_minute is not None and row_minute >= float(facade._MARKET_OPEN_MINUTE):
            out.append(row)
    return out
