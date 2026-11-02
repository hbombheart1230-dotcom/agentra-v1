"""full_chain_component_review: ``_behavior_metric_eligible`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _behavior_metric_eligible(model: Mapping[str, Any], *, facade: Any) -> bool:
    integrity = model.get("integrity") if isinstance(model.get("integrity"), facade.Mapping) else {}
    defects = {str(value) for value in (integrity.get("defects") or [])}
    return not bool(defects & facade.BEHAVIOR_METRIC_EXCLUSION_DEFECTS)
