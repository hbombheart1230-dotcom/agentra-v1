"""operator_period_summary: ``_same_day_new_trade_rows`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _same_day_new_trade_rows(rows: List[Dict[str, Any]], *, facade: Any) -> List[Dict[str, Any]]:
    return [row for row in rows if not facade._is_carryover_exit_marker(row)]
