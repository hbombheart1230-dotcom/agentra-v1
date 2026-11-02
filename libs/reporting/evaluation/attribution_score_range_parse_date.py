"""attribution_score_range: ``_parse_date`` body (moved verbatim from ``attribution_score_range``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any, Iterable, Mapping


def _parse_date(value: str, *, facade: Any) -> date:
    return facade.date.fromisoformat(str(value))
