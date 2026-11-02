"""scanner_alignment_root_cause: ``_impact_score`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _impact_score(returns: list[float], *, facade: Any) -> float:
    return round(sum(value for value in returns if value < 0), 4)
