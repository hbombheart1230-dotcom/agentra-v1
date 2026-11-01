"""operator_period_summary: ``_metric_observed_return_pct`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _metric_observed_return_pct(row: Dict[str, Any], *, facade: Any) -> float | None:
    if bool(row.get("truth_surface_available")):
        return facade._safe_float(row.get("truth_observed_return_pct"))
    return None
