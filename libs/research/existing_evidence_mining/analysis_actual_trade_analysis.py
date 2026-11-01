"""RF-039 existing_evidence_mining: ``actual_trade_analysis`` body (moved verbatim from ``analysis``).

``facade`` is the ``analysis`` module; module-level names and helpers are resolved on it at call time so caller
monkeypatching keeps working. This module never imports ``analysis``. Pure, no IO.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


def actual_trade_analysis(rows: list[Mapping[str, Any]], *, facade: Any) -> dict[str, Any]:
    realized = []
    eligible = []
    early = 0
    violation = 0
    hold_values = []
    ranks: dict[str, list[float]] = facade.defaultdict(list)
    early_returns: list[float] = []
    compliant_returns: list[float] = []
    horizon_returns: dict[str, list[float]] = facade.defaultdict(list)
    hold_bucket_returns: dict[str, list[float]] = facade.defaultdict(list)
    for row in rows:
        outcome = row.get("realized_outcome") if isinstance(row.get("realized_outcome"), Mapping) else {}
        if outcome.get("net_return_pct") is None:
            continue
        value = float(outcome.get("net_return_pct") or 0.0)
        realized.append(value)
        integrity = row.get("integrity") if isinstance(row.get("integrity"), Mapping) else {}
        if bool(integrity.get("promotion_metric_eligible")):
            eligible.append(value)
        horizon = row.get("horizon_alignment") if isinstance(row.get("horizon_alignment"), Mapping) else {}
        hold = outcome.get("holding_seconds")
        if hold is not None:
            hold_values.append(float(hold))
        if bool(horizon.get("exited_before_min_hold")):
            early += 1
            early_returns.append(value)
        else:
            compliant_returns.append(value)
        if bool(horizon.get("horizon_violation_candidate")):
            violation += 1
        rank = int(((row.get("selection_context") or {}).get("selected_rank")) or 0)
        if rank > 0:
            ranks[f"rank{rank}"].append(value)
        strategy_horizon = str(horizon.get("strategy_horizon") or "missing")
        horizon_returns[strategy_horizon].append(value)
        hold_seconds = float(hold or 0.0)
        if hold_seconds < 60:
            hold_bucket = "under_60s"
        elif hold_seconds < 300:
            hold_bucket = "60_300s"
        elif hold_seconds < 1800:
            hold_bucket = "300_1800s"
        else:
            hold_bucket = "1800s_plus"
        hold_bucket_returns[hold_bucket].append(value)
    count = len(realized)
    return {
        "trade_count": count,
        "all_realized": facade.performance_metrics(realized),
        "promotion_eligible": facade.performance_metrics(eligible),
        "promotion_eligible_rate": round(len(eligible) / count, 4) if count else 0.0,
        "before_min_hold_count": early,
        "before_min_hold_rate": round(early / count, 4) if count else 0.0,
        "horizon_violation_count": violation,
        "horizon_violation_rate": round(violation / count, 4) if count else 0.0,
        "average_holding_seconds": round(sum(hold_values) / len(hold_values), 2) if hold_values else None,
        "by_selected_rank": {key: facade.performance_metrics(values) for key, values in sorted(ranks.items())},
        "early_exit_metrics": facade.performance_metrics(early_returns),
        "min_hold_compliant_metrics": facade.performance_metrics(compliant_returns),
        "by_strategy_horizon": {
            key: facade.performance_metrics(values) for key, values in sorted(horizon_returns.items())
        },
        "by_hold_bucket": {
            key: facade.performance_metrics(values) for key, values in sorted(hold_bucket_returns.items())
        },
    }
