from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional


def _to_epoch(ts: Any, *, facade: object = None) -> Optional[int]:
    if ts is None:
        return None
    if isinstance(ts, (int, float)):
        return int(ts)

    s = str(ts).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except Exception:
        pass

    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = (facade.datetime if facade is not None else datetime).fromisoformat(s)
        tz = facade.timezone if facade is not None else timezone
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tz.utc)
        return int(dt.timestamp())
    except Exception:
        return None
