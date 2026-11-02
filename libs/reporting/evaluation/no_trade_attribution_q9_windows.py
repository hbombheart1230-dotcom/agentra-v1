"""no_trade_attribution: ``_q9_windows`` body (moved verbatim from ``no_trade_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _q9_windows(reports_root: Path, day: str, *, facade: Any) -> list[dict[str, Any]]:
    # Streamed and reduced to the fields the report reads: the ~120 MB windows file is no longer parsed
    # whole (and its regular rows are not all kept) just to count a handful of fields per window.
    path = reports_root / "operator_summary" / "daily" / day / "q9_decision_windows.json"
    windows: list[dict[str, Any]] = []
    try:
        for row in facade.iter_json_array(path, "windows"):
            if isinstance(row, dict) and not facade.is_synthetic_evaluation_row(row) and facade.is_regular_session_evaluation_row(row):
                windows.append(facade._q9_window_view(row))
    except ValueError:
        return []  # unreadable windows file == no windows (what _read_json -> {} gave)
    return windows
