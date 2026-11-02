"""attribution_score_window: ``_mapping`` body (moved verbatim from ``attribution_score_window``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _mapping(value: Any, *, facade: Any) -> Mapping[str, Any]:
    return value if isinstance(value, facade.Mapping) else {}
