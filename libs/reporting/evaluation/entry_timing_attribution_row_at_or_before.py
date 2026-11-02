"""entry_timing_attribution: ``_row_at_or_before`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _row_at_or_before(rows: Sequence[Mapping[str, Any]], epoch: int, *, facade: Any) -> Mapping[str, Any] | None:
    prior = [row for row in rows if int(row.get("ts") or 0) <= epoch]
    return prior[-1] if prior else None
