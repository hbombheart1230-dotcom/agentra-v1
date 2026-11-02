"""attribution_score_range: ``_date_range`` body (moved verbatim from ``attribution_score_range``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _date_range(start: str, end: str, *, facade: Any) -> list[str]:
    cursor = facade._parse_date(start)
    final = facade._parse_date(end)
    if cursor > final:
        raise ValueError("start must be before or equal to end")
    days: list[str] = []
    while cursor <= final:
        days.append(cursor.isoformat())
        cursor += facade.timedelta(days=1)
    return days
