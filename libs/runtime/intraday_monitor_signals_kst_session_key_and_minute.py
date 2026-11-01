from __future__ import annotations

from typing import Any, Dict, List, Mapping, Sequence

from datetime import datetime


def _kst_session_key_and_minute(ts_value: Any, *, facade: Any):
    epoch = facade._to_int(ts_value, 0)
    if epoch <= 0:
        return None, None
    try:
        dt = datetime.fromtimestamp(epoch, tz=timezone.utc).astimezone(facade._KST)
    except Exception:
        return None, None
    minute_of_day = float((dt.hour * 60) + dt.minute) + (float(dt.second) / 60.0)
    return dt.date(), minute_of_day
