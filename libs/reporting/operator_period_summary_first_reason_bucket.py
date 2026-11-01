"""operator_period_summary: ``_first_reason_bucket`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _first_reason_bucket(values: Any, *, facade: Any) -> str:
    rows = facade._first_nonempty_list(values)
    return rows[0] if rows else ""
