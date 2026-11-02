"""attribution_score_v0: ``_selection_integrity`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def _selection_integrity(selection_authority: Mapping[str, Any], *, facade: Any) -> dict[str, Any]:
    rows = facade._as_rows(selection_authority.get("rows"))
    if not rows:
        return facade._score(facade.INSUFFICIENT, None, ["selection_authority_rows_missing"])
    penalties: list[float] = []
    reasons: list[str] = []
    for row in rows:
        penalty = 0.0
        if row.get("final_to_executed_changed") is True:
            penalty += 40.0
            reasons.append(f"{row.get('trade_id')}:final_to_executed_changed")
        if row.get("monitor_to_commander_changed") is True:
            penalty += 30.0
            reasons.append(f"{row.get('trade_id')}:monitor_to_commander_changed")
        if row.get("post_to_selected_changed") is True:
            penalty += 10.0
            reasons.append(f"{row.get('trade_id')}:post_to_selected_changed")
        mismatch = facade._mapping(row.get("selection_mismatch"))
        if mismatch and row.get("post_to_selected_changed") is not True:
            penalty += 10.0
            reasons.append(f"{row.get('trade_id')}:selection_mismatch_present")
        penalties.append(min(100.0, penalty))
    score = facade._clamp_score(100.0 - (sum(penalties) / len(penalties)))
    return facade._score(
        facade.OK,
        score,
        reasons or ["selection_chain_consistent"],
        {"trade_count": len(rows)},
    )
