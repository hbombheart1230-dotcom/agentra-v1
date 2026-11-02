"""attribution_score_range: ``_trade_dir_count`` body (moved verbatim from ``attribution_score_range``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping


def _trade_dir_count(reports_root: Path, day: str, *, facade: Any) -> int:
    trade_dir = reports_root / "trades" / day
    if not trade_dir.exists():
        return 0
    return sum(1 for path in trade_dir.rglob("TRD_*") if path.is_dir())
