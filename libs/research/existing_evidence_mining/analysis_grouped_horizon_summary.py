"""RF-039 existing_evidence_mining: ``grouped_horizon_summary`` body (moved verbatim from ``analysis``).

``facade`` is the ``analysis`` module; module-level names and helpers are resolved on it at call time so caller
monkeypatching keeps working. This module never imports ``analysis``. Pure, no IO.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping


def grouped_horizon_summary(
    episodes: list[Mapping[str, Any]],
    *,
    field: str,
    facade: Any,
) -> dict[str, Any]:
    grouped: dict[str, list[Mapping[str, Any]]] = facade.defaultdict(list)
    for row in episodes:
        value = row.get(field)
        values: Iterable[Any] = value if isinstance(value, list) else [value]
        for item in values:
            key = str(item or "missing")
            grouped[key].append(row)
    return {
        key: {horizon: facade.summarize_rows(rows, horizon) for horizon in facade.HORIZONS}
        for key, rows in sorted(grouped.items())
    }
