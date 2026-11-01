"""operator_period_summary: ``_trade_dir_for_row`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _trade_dir_for_row(row: Dict[str, Any], reports_root: Path, *, facade: Any) -> Path | None:
    explicit_path = str(row.get("trade_root_path") or "").strip()
    if explicit_path:
        explicit = facade.Path(explicit_path)
        if explicit.exists() and explicit.is_dir():
            return explicit
    trade_id = str(row.get("trade_id") or "").strip()
    day = str(row.get("date") or row.get("day") or "").strip()[:10]
    if not trade_id or not day:
        return None
    found = facade.find_trade_dir(facade.canonical_trade_day_root(facade.Path(reports_root), day), trade_id)
    if found is not None:
        return found
    fallback = facade.Path(reports_root) / "trades" / day / trade_id
    return fallback if fallback.exists() else None
