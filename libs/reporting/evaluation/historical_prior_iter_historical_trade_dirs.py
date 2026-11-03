"""historical_prior: ``iter_historical_trade_dirs`` body (moved verbatim from ``historical_prior``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def iter_historical_trade_dirs(
    reports_root: Path,
    *,
    from_day: str = "",
    before_day: str,
    facade: Any,
) -> list[Path]:
    trades_root = facade.Path(reports_root) / "trades"
    if not trades_root.exists():
        return []
    rows: list[facade.Path] = []
    for path in sorted({item.parent for item in trades_root.rglob("lifecycle_bundle.json")}):
        day = facade._day_from_trade_dir(path)
        if not day:
            continue
        if from_day and day < from_day:
            continue
        if before_day and day >= before_day:
            continue
        rows.append(path)
    return rows
