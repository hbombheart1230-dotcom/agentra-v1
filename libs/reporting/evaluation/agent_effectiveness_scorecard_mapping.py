"""agent_effectiveness_scorecard: ``_mapping`` body (moved verbatim from ``agent_effectiveness_scorecard``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _mapping(value: Any, *, facade: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, facade.Mapping) else {}
