"""attribution_score_window: ``_ledger_days`` body (moved verbatim from ``attribution_score_window``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping


def _ledger_days(freeze_root: Path, *, facade: Any) -> list[dict[str, Any]]:
    ledger = facade._read_json(freeze_root / "daily_ledger.json")
    return [dict(row) for row in ledger.get("days") or [] if isinstance(row, dict)]
