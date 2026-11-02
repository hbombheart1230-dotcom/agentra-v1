"""evaluation_lens_report: ``_best_role_by_horizon`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _best_role_by_horizon(rows: list[dict[str, Any]], horizon: str, *, facade: Any) -> dict[str, Any]:
    by_role: dict[str, list[float]] = facade.defaultdict(list)
    for row in rows:
        role = facade._text(row.get("q9_decision_role"))
        if role not in {"P_SCANNER_PRE_STRATEGIST_UNIVERSE", "A_SCANNER_CONTROL", "B_STRATEGIST_RANKED", "C_COMMANDER_FINAL"}:
            continue
        value = facade._checkpoint_return(row, horizon)
        if value is not None:
            by_role[role].append(value)
    ranked = [
        {"role": role, **facade.performance_metrics(values)}
        for role, values in by_role.items()
        if values
    ]
    ranked.sort(key=lambda row: float(row.get("expectancy_pct") or 0.0), reverse=True)
    return {"horizon": horizon, "roles": ranked, "best_role": ranked[0]["role"] if ranked else ""}
