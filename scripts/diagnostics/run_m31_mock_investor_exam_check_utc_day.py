from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from scripts.diagnostics.run_m31_mock_investor_exam_check_to_epoch import _to_epoch


def _utc_day(ts: Any, *, facade: object = None) -> Optional[str]:
    e = (facade._to_epoch if facade is not None else _to_epoch)(ts)
    if e is None:
        return None
    dt_type = facade.datetime if facade is not None else datetime
    tz = facade.timezone if facade is not None else timezone
    return dt_type.fromtimestamp(e, tz=tz.utc).strftime("%Y-%m-%d")
