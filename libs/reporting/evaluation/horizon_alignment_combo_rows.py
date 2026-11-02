"""horizon_alignment: ``_combo_rows`` body (moved verbatim from ``horizon_alignment``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _combo_rows(
    candidates: list[dict[str, Any]],
    *,
    dimensions: tuple[str, ...],
    cost_pct: float,
    facade: Any,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, ...], list[dict[str, Any]]] = facade.defaultdict(list)
    for row in candidates:
        grouped[facade._group_key(row, dimensions)].append(row)

    output: list[dict[str, Any]] = []
    for key, members in grouped.items():
        for horizon in facade.HORIZONS:
            observations: list[tuple[dict[str, Any], float]] = []
            for row in members:
                gross = facade._checkpoint_return(row, horizon)
                if gross is not None:
                    observations.append((row, gross))
            if not observations:
                continue
            gross_values = [value for _, value in observations]
            net_values = [value - cost_pct for value in gross_values]
            days = facade.Counter(facade.candidate_day(row) or "unknown" for row, _ in observations)
            symbols = facade.Counter(facade._text(row.get("symbol")) for row, _ in observations)
            count = len(observations)
            max_day_share = max(days.values()) / count if days else 1.0
            max_symbol_share = max(symbols.values()) / count if symbols else 1.0
            avg_gross = sum(gross_values) / count
            avg_net = sum(net_values) / count
            profit_factor = facade._profit_factor(net_values)
            daily_net: dict[str, list[float]] = facade.defaultdict(list)
            for (row, _), net_value in zip(observations, net_values):
                daily_net[facade.candidate_day(row) or "unknown"].append(net_value)
            daily_net_returns = {
                day: round(sum(values) / len(values), 4)
                for day, values in sorted(daily_net.items())
            }
            leave_one_day_out = {}
            for excluded_day in daily_net:
                retained = [
                    value
                    for day, values in daily_net.items()
                    if day != excluded_day
                    for value in values
                ]
                leave_one_day_out[excluded_day] = (
                    round(sum(retained) / len(retained), 4)
                    if retained
                    else None
                )
            observed_lodo = [
                value for value in leave_one_day_out.values()
                if value is not None
            ]
            worst_lodo = min(observed_lodo) if observed_lodo else None
            robust_across_days = bool(observed_lodo) and all(
                value > 0 for value in observed_lodo
            )
            eligible = (
                count >= facade.MIN_OBSERVATIONS
                and len(days) >= facade.MIN_DAYS
                and max_day_share <= facade.MAX_DAY_SHARE
                and max_symbol_share <= facade.MAX_SYMBOL_SHARE
            )
            positive = (
                eligible
                and avg_net >= facade.MIN_AVERAGE_NET_RETURN_PCT
                and profit_factor >= facade.MIN_NET_PROFIT_FACTOR
                and robust_across_days
            )
            output.append({
                "dimensions": dict(zip(dimensions, key)),
                "horizon": horizon,
                "candidate_count": len(members),
                "observed_count": count,
                "observed_day_count": len(days),
                "observed_symbol_count": len(symbols),
                "coverage": round(count / len(members), 4) if members else 0.0,
                "average_gross_return_pct": round(avg_gross, 4),
                "round_trip_cost_pct": round(cost_pct, 4),
                "average_net_return_pct": round(avg_net, 4),
                "net_win_rate": round(sum(1 for value in net_values if value > 0) / count, 4),
                "net_profit_factor": profit_factor,
                "net_maximum_drawdown_pct": facade.performance_metrics(net_values)["maximum_drawdown_pct"],
                "daily_net_returns_pct": daily_net_returns,
                "positive_day_count": sum(
                    1 for value in daily_net_returns.values() if value > 0
                ),
                "leave_one_day_out_net_returns_pct": leave_one_day_out,
                "worst_leave_one_day_out_net_return_pct": worst_lodo,
                "robust_across_days": robust_across_days,
                "maximum_day_share": round(max_day_share, 4),
                "maximum_symbol_share": round(max_symbol_share, 4),
                "top_days": [{"day": name, "count": value} for name, value in days.most_common(3)],
                "top_symbols": [{"symbol": name, "count": value} for name, value in symbols.most_common(5)],
                "evidence_eligible": eligible,
                "cost_positive": positive,
                "decision": (
                    "CONTROLLED_ADOPTION_CANDIDATE"
                    if positive
                    else "INSUFFICIENT_EVIDENCE"
                    if not eligible
                    else "RETAIN_UNDER_OBSERVATION"
                    if avg_net > 0
                    else "REJECT_COST_NEGATIVE"
                ),
            })
    return sorted(
        output,
        key=lambda row: (
            not bool(row["cost_positive"]),
            -float(row["average_net_return_pct"]),
            -int(row["observed_count"]),
        ),
    )
