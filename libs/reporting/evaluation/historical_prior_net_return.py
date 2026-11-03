"""historical_prior: ``_net_return`` body (moved verbatim from ``historical_prior``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _net_return(evaluation: dict[str, Any], *, facade: Any) -> float | None:
    value = (evaluation.get("realized_outcome") or {}).get("net_return_pct")
    try:
        return float(value)
    except (TypeError, ValueError):
        return None
