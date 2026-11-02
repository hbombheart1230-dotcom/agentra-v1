"""attribution_score_v0: ``_exit_horizon`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def _exit_horizon(horizon_report: Mapping[str, Any], *, facade: Any) -> dict[str, Any]:
    rows = facade._as_rows(horizon_report.get("rows"))
    if not rows:
        return facade._score(facade.INSUFFICIENT, None, ["horizon_rows_missing"])
    scores: list[float] = []
    reasons: list[str] = []
    for row in rows:
        penalty = 0.0
        if row.get("horizon_violation_candidate"):
            penalty += 20.0
            reasons.append(f"{row.get('trade_id')}:horizon_violation_candidate")
        if row.get("exited_before_min_hold"):
            penalty += 20.0
            reasons.append(f"{row.get('trade_id')}:before_min_hold")
        if row.get("exited_before_target_hold"):
            penalty += 10.0
            reasons.append(f"{row.get('trade_id')}:before_target_hold")
        if row.get("target_hold_would_improve_exit"):
            penalty += 30.0
            reasons.append(f"{row.get('trade_id')}:target_hold_would_improve")
        scores.append(max(0.0, 100.0 - min(100.0, penalty)))
    return facade._score(
        facade.OK,
        facade._clamp_score(sum(scores) / len(scores)),
        reasons or ["exit_horizon_aligned"],
        {"trade_count": len(rows)},
    )
