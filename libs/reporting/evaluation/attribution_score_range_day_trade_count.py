"""attribution_score_range: ``_day_trade_count`` body (moved verbatim from ``attribution_score_range``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _day_trade_count(reports_root: Path, day: str, *, facade: Any) -> int:
    scorecard_count = (
        facade._read_json(reports_root / "evaluation" / "daily" / day / "daily_scorecard.json")
        .get("artifact_integrity", {})
        .get("trade_count")
    )
    if scorecard_count is not None:
        try:
            return int(scorecard_count)
        except (TypeError, ValueError):
            pass
    return facade._trade_dir_count(reports_root, day)
