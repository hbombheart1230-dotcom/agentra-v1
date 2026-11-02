"""agent_effectiveness_scorecard: ``_decision_state`` body (moved verbatim from ``agent_effectiveness_scorecard``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _decision_state(component: Mapping[str, Any], *, facade: Any) -> str:
    decision = str(component.get("decision") or "")
    if decision == "INSUFFICIENT_EVIDENCE":
        return "NOT_MEASURABLE"
    if decision in {"REJECT", "DEPRECATE_CANDIDATE"}:
        return "DEGRADING"
    if decision == "ADJUST_AND_RETEST":
        return "DEGRADING"
    if decision == "PROMOTION_CANDIDATE":
        return "VALUE_ADD"
    return "NEUTRAL"
