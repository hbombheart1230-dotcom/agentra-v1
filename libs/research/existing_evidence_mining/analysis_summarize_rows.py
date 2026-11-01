"""RF-039 existing_evidence_mining: ``summarize_rows`` body (moved verbatim from ``analysis``).

``facade`` is the ``analysis`` module; module-level names and helpers are resolved on it at call time so caller
monkeypatching keeps working. This module never imports ``analysis``. Pure, no IO.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


def summarize_rows(rows: list[Mapping[str, Any]], horizon: str, *, facade: Any) -> dict[str, Any]:
    observed = []
    for row in rows:
        value = facade._observed_return(row, horizon)
        if value is None:
            continue
        checkpoint = (row.get("checkpoints") or {}).get(horizon) or {}
        observed.append(
            {
                "return_pct": value,
                "gross_return_pct": float(checkpoint.get("gross_return_pct") or 0.0),
                "mfe_pct": float(checkpoint.get("mfe_pct") or 0.0),
                "mae_pct": float(checkpoint.get("mae_pct") or 0.0),
            }
        )
    by_day: dict[str, list[float]] = facade.defaultdict(list)
    day_counts: facade.Counter[str] = facade.Counter()
    symbol_counts: facade.Counter[str] = facade.Counter()
    for row in rows:
        value = facade._observed_return(row, horizon)
        if value is None:
            continue
        day = str(row.get("day") or "")
        symbol = str(row.get("symbol") or "")
        by_day[day].append(value)
        day_counts[day] += 1
        symbol_counts[symbol] += 1
    positive_days = sum(1 for values in by_day.values() if sum(values) / len(values) > 0.0)
    return {
        "population_count": len(rows),
        "observed_count": len(observed),
        "coverage": round(len(observed) / len(rows), 4) if rows else 0.0,
        "metrics": facade.performance_metrics(item["return_pct"] for item in observed),
        "gross_metrics": facade.performance_metrics(item["gross_return_pct"] for item in observed),
        "average_mfe_pct": round(sum(item["mfe_pct"] for item in observed) / len(observed), 4)
        if observed
        else None,
        "average_mae_pct": round(sum(item["mae_pct"] for item in observed) / len(observed), 4)
        if observed
        else None,
        "day_count": len(by_day),
        "positive_day_ratio": round(positive_days / len(by_day), 4) if by_day else 0.0,
        "largest_day_share": round(max(day_counts.values(), default=0) / len(observed), 4)
        if observed
        else 0.0,
        "largest_symbol_share": round(max(symbol_counts.values(), default=0) / len(observed), 4)
        if observed
        else 0.0,
    }
