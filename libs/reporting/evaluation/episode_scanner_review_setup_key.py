"""episode_scanner_review: ``_setup_key`` body (moved verbatim from ``episode_scanner_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _setup_key(row: Mapping[str, Any], *, facade: Any) -> str:
    lane = facade._mapping(row.get("entry_lane_observation"))
    return str(
        lane.get("subtype_v2")
        or lane.get("subtype")
        or lane.get("primary_lane")
        or row.get("reason")
        or "unknown"
    )
