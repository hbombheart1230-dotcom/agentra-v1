"""RF-039 existing_evidence_mining: ``score_component_diagnostics`` body (moved verbatim from ``analysis``).

``facade`` is the ``analysis`` module; module-level names and helpers are resolved on it at call time so caller
monkeypatching keeps working. This module never imports ``analysis``. Pure, no IO.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


def score_component_diagnostics(episodes: list[Mapping[str, Any]], *, facade: Any) -> dict[str, Any]:
    values: dict[str, list[tuple[float, Mapping[str, Any]]]] = facade.defaultdict(list)
    for row in episodes:
        if facade._observed_return(row, facade.PRIMARY_HORIZON) is None:
            continue
        for name, raw in dict(row.get("score_breakdown") or {}).items():
            try:
                values[str(name)].append((float(raw), row))
            except Exception:
                continue
    output: dict[str, Any] = {}
    for name, pairs in sorted(values.items()):
        if len(pairs) < 30:
            continue
        threshold = facade.median(value for value, _ in pairs)
        low = [row for value, row in pairs if value < threshold]
        high = [row for value, row in pairs if value >= threshold]
        if len(low) < 15 or len(high) < 15 or len({value for value, _ in pairs}) < 3:
            continue
        low_summary = facade.summarize_rows(low, facade.PRIMARY_HORIZON)
        high_summary = facade.summarize_rows(high, facade.PRIMARY_HORIZON)
        output[name] = {
            "median": round(float(threshold), 6),
            "low": low_summary,
            "high": high_summary,
            "high_minus_low_expectancy_pct": round(
                float((high_summary.get("metrics") or {}).get("expectancy_pct") or 0.0)
                - float((low_summary.get("metrics") or {}).get("expectancy_pct") or 0.0),
                4,
            ),
        }
    return output
