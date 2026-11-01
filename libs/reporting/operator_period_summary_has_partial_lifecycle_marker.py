"""operator_period_summary: ``_has_partial_lifecycle_marker`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _has_partial_lifecycle_marker(row: Dict[str, Any], *, facade: Any) -> bool:
    return (
        facade._trade_status(row) == "partial"
        or str(row.get("trade_origin") or "").strip().lower() == "recovered_partial"
    )
