"""evaluation_lens_report: ``_rail`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _rail(row: Mapping[str, Any], *, facade: Any) -> str:
    lane = facade._as_dict(row.get("entry_lane_observation"))
    if lane.get("market_regime_rail"):
        return facade._text(lane.get("market_regime_rail"))
    shadow = facade._as_dict(lane.get("market_regime_rail_shadow"))
    return facade._text(shadow.get("market_regime_rail")) or "unknown"
