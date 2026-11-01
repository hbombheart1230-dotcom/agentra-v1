"""operator_period_summary: ``_ratio_to_pct`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _ratio_to_pct(value: Any, *, facade: Any) -> float | None:
    parsed = facade._safe_float(value)
    if parsed is None:
        return None
    return float(parsed) * 100.0
