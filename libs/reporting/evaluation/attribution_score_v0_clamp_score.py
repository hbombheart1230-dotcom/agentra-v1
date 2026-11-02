"""attribution_score_v0: ``_clamp_score`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def _clamp_score(value: float, *, facade: Any) -> int:
    return int(round(max(0.0, min(100.0, value))))
