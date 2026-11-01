"""operator_period_summary: ``_trade_status`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _trade_status(row: Dict[str, Any], *, facade: Any) -> str:
    return str(row.get("last_status") or row.get("status") or "").strip().lower()
