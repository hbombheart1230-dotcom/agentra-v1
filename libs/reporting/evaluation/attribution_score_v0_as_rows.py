"""attribution_score_v0: ``_as_rows`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def _as_rows(value: Any, *, facade: Any) -> list[Mapping[str, Any]]:
    return [row for row in (value or []) if isinstance(row, facade.Mapping)]
