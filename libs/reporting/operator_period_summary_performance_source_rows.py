"""operator_period_summary: ``_performance_source_rows`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _performance_source_rows(rows: List[Dict[str, Any]], *, facade: Any) -> List[Dict[str, Any]]:
    return [row for row in rows if facade._is_closed_trade(row) or facade._is_realized_nonclosed_exit(row)]
