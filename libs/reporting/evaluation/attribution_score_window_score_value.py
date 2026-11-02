"""attribution_score_window: ``_score_value`` body (moved verbatim from ``attribution_score_window``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _score_value(row: Mapping[str, Any], key: str, *, facade: Any) -> int | None:
    item = facade._mapping(facade._mapping(row.get("scores")).get(key))
    if item.get("status") == "INSUFFICIENT_EVIDENCE":
        return None
    value = item.get("score")
    if value is None:
        return None
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return None
