"""Pure UTC-day projection owner."""
from __future__ import annotations

from typing import Any


def _utc_day(ts: Any, *, facade: Any) -> str:
    epoch = facade._to_epoch(ts)
    if epoch is None:
        return facade.datetime.now(facade.timezone.utc).strftime("%Y-%m-%d")
    return facade.datetime.fromtimestamp(epoch, tz=facade.timezone.utc).strftime("%Y-%m-%d")
