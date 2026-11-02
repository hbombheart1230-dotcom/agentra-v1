"""episode_scanner_review: ``_epoch`` body (moved verbatim from ``episode_scanner_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _epoch(row: Mapping[str, Any], *, facade: Any) -> int:
    base = facade._mapping(row.get("shadow_forward_base"))
    value = facade._number(base.get("baseline_epoch"))
    return int(value or 0)
