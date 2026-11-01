from __future__ import annotations
from typing import Any, Mapping, Sequence

def _current_kst_session_anchor(candles: Sequence[Mapping[str, Any]], *, facade: Any) -> tuple[Any | None, int | None, float | None]:
    if not candles: return None, None, None
    latest_key, latest_minute=facade._kst_session_key_and_minute(candles[-1].get("ts"))
    if latest_key is None: return None, None, None
    for idx,row in enumerate(candles):
        row_key,row_minute=facade._kst_session_key_and_minute(row.get("ts"))
        if row_key == latest_key and row_minute is not None and row_minute >= float(facade._MARKET_OPEN_MINUTE): return latest_key,idx,latest_minute
    return latest_key,None,latest_minute
