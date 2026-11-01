"""operator_period_summary: ``_price_matches`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _price_matches(left: Any, right: Any, *, facade: Any) -> bool:
    left_value = facade._safe_float(left)
    right_value = facade._safe_float(right)
    if left_value is None or right_value is None or left_value <= 0 or right_value <= 0:
        return False
    tolerance = max(1.0, abs(left_value) * 0.001)
    return abs(left_value - right_value) <= tolerance
