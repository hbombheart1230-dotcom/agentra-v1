"""horizon_alignment: ``_lane_observation`` body (moved verbatim from ``horizon_alignment``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _lane_observation(row: Mapping[str, Any], *, facade: Any) -> dict[str, Any]:
    value = row.get("entry_lane_observation")
    return dict(value) if isinstance(value, facade.Mapping) else {}
