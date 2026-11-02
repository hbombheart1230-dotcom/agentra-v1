"""episode_scanner_review: ``_day`` body (moved verbatim from ``episode_scanner_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _day(row: Mapping[str, Any], *, facade: Any) -> str:
    value = facade.candidate_day(row) or str(row.get("day") or "")
    value = value.replace("-", "")
    return value if len(value) == 8 and value.isdigit() else ""
