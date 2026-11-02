"""artifact_inventory: ``_load_forward_recovery_candles`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _load_forward_recovery_candles(
    reports_root: Path, day: str,
    *,
    facade: Any,
) -> dict[str, list[dict[str, Any]]]:
    payload = facade.read_json(
        facade.Path(reports_root)
        / "evaluation"
        / "daily"
        / day
        / "q9_forward_recovery_candles.json"
    )
    by_symbol = payload.get("minute_rows_by_symbol")
    return {
        str(symbol): [dict(row) for row in rows if isinstance(row, dict)]
        for symbol, rows in (by_symbol.items() if isinstance(by_symbol, dict) else [])
        if isinstance(rows, list)
    }
