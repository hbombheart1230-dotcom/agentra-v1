"""Pure ISO timestamp parsing owner for monitor gate diagnostics."""
from __future__ import annotations

from typing import Any, Optional


def _parse_iso_utc_seconds(value: Any, *, facade: Any) -> Optional[int]:
    text = str(value or "").strip()
    if not text:
        return None
    try:
        return int(facade.datetime.fromisoformat(text).timestamp())
    except Exception:
        return None
