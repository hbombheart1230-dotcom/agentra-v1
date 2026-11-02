"""full_chain_component_review: ``_role_metrics`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _role_metrics(
    candidates: list[dict[str, Any]],
    *,
    role: str,
    horizon: str,
    cost_pct: float,
    facade: Any,
) -> dict[str, Any]:
    values: list[float] = []
    days: set[str] = set()
    for row in candidates:
        if str(row.get("shadow_role") or "") != role:
            continue
        value = facade._checkpoint_return(row, horizon)
        if value is None:
            continue
        values.append(value - cost_pct)
        day = facade.candidate_day(row)
        if day:
            days.add(day)
    return {
        "role": role,
        "horizon": horizon,
        "evidence_class": "TRUSTED_SHADOW",
        "observed_count": len(values),
        "observed_day_count": len(days),
        "cost_adjusted": True,
        **facade.performance_metrics(values),
    }
