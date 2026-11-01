"""operator_period_summary: ``_daily_symbol_history_rows`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _daily_symbol_history_rows(reports_root: Path, day: str, *, facade: Any) -> List[Dict[str, Any]]:
    normalized_day = str(day or "").strip()
    return [
        row
        for row in facade._iter_symbol_trade_history(reports_root)
        if str(row.get("date") or "").strip() == normalized_day
    ]
