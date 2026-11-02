"""attribution_score_v0: ``_ledger_day_record`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _ledger_day_record(reports_root: Path, day: str, *, facade: Any) -> dict[str, Any]:
    root = reports_root / "evaluation" / "freeze_window"
    for path in sorted(root.glob("*/daily_ledger.json"), key=lambda item: str(item)):
        payload = facade._read_json(path)
        for row in payload.get("days") or []:
            if isinstance(row, dict) and str(row.get("day") or "") == day:
                return dict(row)
    return {}
