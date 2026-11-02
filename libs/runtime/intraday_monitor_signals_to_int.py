from __future__ import annotations

from typing import Any


def _to_int(value: Any, default: int = 0, *, facade: Any) -> int:
    try:
        return int(float(value))
    except Exception:
        return int(default)
