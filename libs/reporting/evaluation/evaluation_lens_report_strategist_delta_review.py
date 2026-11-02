"""evaluation_lens_report: ``_strategist_delta_review`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _strategist_delta_review(q9_rows: list[dict[str, Any]], *, facade: Any) -> dict[str, Any]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = facade.defaultdict(lambda: facade.defaultdict(list))
    for row in q9_rows:
        decision_id = facade._text(row.get("q9_decision_id"))
        role = facade._text(row.get("q9_decision_role"))
        if decision_id and role:
            grouped[decision_id][role].append(row)
    deltas_by_horizon: list[dict[str, Any]] = []
    for horizon in facade.HORIZONS:
        strategist_delta: list[float] = []
        commander_delta: list[float] = []
        for roles in grouped.values():
            a = min(roles.get("A_SCANNER_CONTROL") or [], key=lambda r: int(float(r.get("rank") or 999)), default={})
            b = next((r for r in roles.get("B_STRATEGIST_RANKED") or [] if r.get("q9_selected")), None)
            if not b:
                b = min(roles.get("B_STRATEGIST_RANKED") or [], key=lambda r: int(float(r.get("rank") or 999)), default={})
            c = min(roles.get("C_COMMANDER_FINAL") or [], key=lambda r: int(float(r.get("rank") or 999)), default={})
            av = facade._checkpoint_return(a, horizon) if a else None
            bv = facade._checkpoint_return(b, horizon) if b else None
            cv = facade._checkpoint_return(c, horizon) if c else None
            if av is not None and bv is not None:
                strategist_delta.append(bv - av)
            if bv is not None and cv is not None:
                commander_delta.append(cv - bv)
        deltas_by_horizon.append(
            {
                "horizon": horizon,
                "strategist_minus_scanner_control": facade.performance_metrics(strategist_delta),
                "commander_minus_strategist": facade.performance_metrics(commander_delta),
            }
        )
    return {
        "schema_version": "strategist_delta_review.v1",
        "behavior_effect": "evaluation_only",
        "decision_window_count": len(grouped),
        "best_role_by_horizon": [facade._best_role_by_horizon(q9_rows, horizon) for horizon in facade.HORIZONS],
        "deltas_by_horizon": deltas_by_horizon,
    }
