"""entry_timing_attribution: ``_candidate_rank`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _candidate_rank(candidate: Any, *, facade: Any) -> int | None:
    value = facade._num(candidate.get("rank") if isinstance(candidate, facade.Mapping) else None)
    return int(value) if value is not None else None
