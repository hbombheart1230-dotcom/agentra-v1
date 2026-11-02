"""entry_timing_attribution: ``_daily_windows_by_id`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _daily_windows_by_id(reports_root: Path, day: str, *, facade: Any) -> dict[str, dict[str, Any]]:
    path = reports_root / "operator_summary" / "daily" / day / "q9_decision_windows.json"
    payload = facade._read_json(path)
    out: dict[str, dict[str, Any]] = {}
    for row in payload.get("windows") or []:
        if not isinstance(row, dict):
            continue
        decision_id = str(row.get("decision_id") or "").strip()
        if decision_id:
            out[decision_id] = dict(row)
    return out
