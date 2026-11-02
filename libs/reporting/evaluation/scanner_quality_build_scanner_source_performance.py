"""scanner_quality: ``build_scanner_source_performance`` body (moved verbatim from ``scanner_quality``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def build_scanner_source_performance(
    rows: list[dict[str, Any]],
    *,
    cost_pct: float,
    slippage_pct: float,
    facade: Any,
) -> dict[str, Any]:
    buckets: dict[tuple[str, str], list[float]] = facade.defaultdict(list)
    days: dict[tuple[str, str], set[str]] = facade.defaultdict(set)
    total_drag = float(cost_pct) + float(slippage_pct)
    for row in rows:
        sources = [
            str(value or "")
            for value in row.get("q9_candidate_sources") or row.get("sources") or []
            if str(value or "")
        ] or ["unknown"]
        for horizon in facade.SCANNER_HORIZONS:
            value = facade._checkpoint_return(row, horizon)
            if value is None:
                continue
            for source in sources:
                key = (source, horizon)
                buckets[key].append(value - total_drag)
                day = facade.candidate_day(row)
                if day:
                    days[key].add(day)
    return {
        "schema_version": "q9_scanner_source_performance.v1",
        "behavior_effect": "evaluation_only",
        "rows": [
            {
                "source": source,
                "horizon": horizon,
                "observed_day_count": len(days[(source, horizon)]),
                "cost_pct": round(float(cost_pct), 6),
                "slippage_pct": round(float(slippage_pct), 6),
                **facade.performance_metrics(values),
            }
            for (source, horizon), values in sorted(buckets.items())
        ],
    }
