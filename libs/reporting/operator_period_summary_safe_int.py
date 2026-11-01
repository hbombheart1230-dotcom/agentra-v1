"""operator_period_summary: ``_safe_int`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _safe_int(value: Any, default: int = 0, *, facade: Any) -> int:
    try:
        return int(float(value))
    except Exception:
        return int(default)
