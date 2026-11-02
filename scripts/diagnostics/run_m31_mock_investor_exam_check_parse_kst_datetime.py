from __future__ import annotations

from datetime import datetime
from typing import Optional

from libs.runtime.market_hours import KST


def _parse_kst_datetime(value: str, *, facade: object = None) -> Optional[datetime]:
    raw = str(value or "").strip()
    if not raw:
        return None
    s = raw.replace("Z", "+00:00")
    try:
        dt = (facade.datetime if facade is not None else datetime).fromisoformat(s)
    except Exception:
        return None
    kst = facade.KST if facade is not None else KST
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=kst)
    return dt.astimezone(kst)
