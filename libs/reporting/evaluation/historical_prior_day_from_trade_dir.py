"""historical_prior: ``_day_from_trade_dir`` body (moved verbatim from ``historical_prior``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _day_from_trade_dir(trade_dir: Path, *, facade: Any) -> str:
    parts = list(trade_dir.parts)
    for index, part in enumerate(parts):
        if part == "trades" and index + 1 < len(parts):
            return parts[index + 1]
    return ""
