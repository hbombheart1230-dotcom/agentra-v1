from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence

from datetime import datetime
from zoneinfo import ZoneInfo


def _market_snapshot_for_symbol(state: Mapping[str, Any], symbol: str, *, now_epoch: int, facade: Any):
    rows = facade._normalize_minute_rows(facade._minute_root(state).get(symbol))
    if not rows:
        return {"available": False, "reason": "minute_rows_unavailable"}
    now_day = datetime.fromtimestamp(int(now_epoch), tz=ZoneInfo("Asia/Seoul")).date()
    same_day_rows = [
        row
        for row in rows
        if datetime.fromtimestamp(int(row.get("ts") or 0), tz=ZoneInfo("Asia/Seoul")).date()
        == now_day
    ]
    if not same_day_rows:
        latest = rows[-1]
        return {
            "available": False,
            "reason": "same_day_minute_rows_unavailable",
            "latest_epoch": int(latest.get("ts") or 0),
            "latest_raw_ts": facade._text(latest.get("raw_ts")),
        }
    usable = [
        row for row in same_day_rows if int(row.get("ts") or 0) <= int(now_epoch)
    ]
    if not usable:
        return {"available": False, "reason": "same_day_baseline_not_reached"}
    baseline = usable[-1]
    return {
        "available": True,
        "baseline_epoch": int(baseline["ts"]),
        "baseline_price": float(baseline["close"]),
        "baseline_raw_ts": facade._text(baseline.get("raw_ts")),
        "source": "state.minute_ohlcv_by_symbol",
    }
