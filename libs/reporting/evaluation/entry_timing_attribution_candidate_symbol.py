"""entry_timing_attribution: ``_candidate_symbol`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _candidate_symbol(candidate: Any, *, facade: Any) -> str:
    return str(candidate.get("symbol") or "").strip() if isinstance(candidate, facade.Mapping) else ""
