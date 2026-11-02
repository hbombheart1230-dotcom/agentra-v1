"""scanner_quality: ``build_scanner_topk_forward_performance`` body (moved verbatim from ``scanner_quality``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def build_scanner_topk_forward_performance(
    rows: list[dict[str, Any]],
    *,
    cost_pct: float,
    slippage_pct: float,
    facade: Any,
) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = facade.defaultdict(list)
    for row in rows:
        decision_id = str(row.get("q9_decision_id") or "")
        if decision_id:
            grouped[decision_id].append(row)
    output: list[dict[str, Any]] = []
    total_drag = float(cost_pct) + float(slippage_pct)
    for horizon in facade.SCANNER_HORIZONS:
        for top_k in facade.TOP_K_VALUES:
            gross_values: list[float] = []
            net_values: list[float] = []
            days: set[str] = set()
            candidate_observations = 0
            for decision_rows in grouped.values():
                ranked = sorted(
                    decision_rows,
                    key=lambda row: int(facade._number(row.get("rank")) or 999),
                )
                observed = [
                    value
                    for row in ranked[:top_k]
                    for value in [facade._checkpoint_return(row, horizon)]
                    if value is not None
                ]
                if not observed:
                    continue
                window_return = sum(observed) / len(observed)
                gross_values.append(window_return)
                net_values.append(window_return - total_drag)
                candidate_observations += len(observed)
                day = next((facade.candidate_day(row) for row in ranked[:top_k] if facade.candidate_day(row)), "")
                if day:
                    days.add(day)
            output.append(
                {
                    "top_k": top_k,
                    "horizon": horizon,
                    "window_count": len(gross_values),
                    "candidate_observation_count": candidate_observations,
                    "observed_day_count": len(days),
                    "cost_pct": round(float(cost_pct), 6),
                    "slippage_pct": round(float(slippage_pct), 6),
                    "gross": facade.performance_metrics(gross_values),
                    "net": facade.performance_metrics(net_values),
                }
            )
    return {
        "schema_version": "q9_scanner_topk_forward_performance.v1",
        "behavior_effect": "evaluation_only",
        "decision_window_count": len(grouped),
        "candidate_row_count": len(rows),
        "top_k_values": list(facade.TOP_K_VALUES),
        "horizons": list(facade.SCANNER_HORIZONS),
        "rows": output,
    }
