"""historical_prior: ``_group_metrics`` body (moved verbatim from ``historical_prior``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Iterable


def _group_metrics(rows: Iterable[tuple[str, float]], *, facade: Any) -> dict[str, Any]:
    grouped: dict[str, list[float]] = facade.defaultdict(list)
    for key, value in rows:
        grouped[str(key or "unknown")].append(float(value))
    return {
        key: facade.performance_metrics(values)
        for key, values in sorted(grouped.items())
    }
