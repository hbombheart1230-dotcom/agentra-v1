"""evaluation_lens_report: ``_blocker_forward_review`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _blocker_forward_review(rows: list[dict[str, Any]], *, cost_floor_pct: float, facade: Any) -> dict[str, Any]:
    prepared: list[dict[str, Any]] = []
    for row in rows:
        item = dict(row)
        item["blocker"] = facade._blocker(row)
        item["market_rail"] = facade._rail(row)
        prepared.append(item)
    interested = [
        row
        for row in prepared
        if any(token in facade._text(row.get("blocker")) for token in facade.BLOCKERS_OF_INTEREST)
    ]
    return {
        "schema_version": "blocker_forward_review.v1",
        "behavior_effect": "evaluation_only",
        "cost_floor_pct": round(cost_floor_pct, 4),
        "candidate_count": len(prepared),
        "focused_candidate_count": len(interested),
        "by_blocker": facade._forward_group(interested, "blocker", cost_floor_pct=cost_floor_pct),
        "by_market_rail": facade._forward_group(prepared, "market_rail", cost_floor_pct=cost_floor_pct),
    }
