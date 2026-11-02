from __future__ import annotations

from typing import Any


def _to_float(value: Any, default: float = 0.0, *, facade: object = None) -> float:
    try:
        return float(value)
    except Exception:
        return float(default)
