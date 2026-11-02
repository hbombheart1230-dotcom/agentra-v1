"""entry_timing_attribution: ``_stage_epoch`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _stage_epoch(payload: Mapping[str, Any], *keys: str, facade: Any) -> int:
    for key in keys:
        value = facade._epoch(payload.get(key))
        if value > 0:
            return value
    return 0
