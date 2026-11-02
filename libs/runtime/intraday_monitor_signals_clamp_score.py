from __future__ import annotations

from typing import Any


def _clamp_score(value: float, *, facade: Any) -> float:
    try:
        return float(max(0.0, min(1.0, float(value))))
    except Exception:
        return 0.0
