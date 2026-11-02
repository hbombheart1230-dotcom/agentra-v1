"""horizon_alignment: ``_group_key`` body (moved verbatim from ``horizon_alignment``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def _group_key(row: Mapping[str, Any], dimensions: tuple[str, ...], *, facade: Any) -> tuple[str, ...]:
    lane = facade._lane_observation(row)
    values = {
        "time_bucket": facade._text(lane.get("time_bucket")),
        "tactic": facade._text(row.get("quant_tactic_id")),
        "primary_lane": facade._text(lane.get("primary_lane")),
        "market_regime_rail": facade._text(lane.get("market_regime_rail")),
        "selection_role": facade._text(row.get("shadow_role")),
    }
    return tuple(values[name] for name in dimensions)
