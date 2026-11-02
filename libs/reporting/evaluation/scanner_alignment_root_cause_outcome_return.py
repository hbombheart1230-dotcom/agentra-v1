"""scanner_alignment_root_cause: ``_outcome_return`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _outcome_return(evaluation: Mapping[str, Any], model: Mapping[str, Any], *, facade: Any) -> float | None:
    value = facade._num(facade._mapping(evaluation.get("realized_outcome")).get("net_return_pct"))
    if value is not None:
        return value
    return facade._num(facade._mapping(model.get("outcome")).get("net_return_pct"))
