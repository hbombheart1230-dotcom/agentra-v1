"""operator_period_summary: ``_row_report_day`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _row_report_day(row: Dict[str, Any], *, facade: Any) -> str:
    return str(row.get("date") or row.get("day") or "").strip()[:10]
