"""full_chain_component_review: ``_unavailable_component`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _unavailable_component(
    *,
    question: str,
    missing_comparison: str,
    availability: dict[str, Any],
    facade: Any,
) -> dict[str, Any]:
    return {
        "decision": facade.DecisionClass.INSUFFICIENT_EVIDENCE.value,
        "question": question,
        "finding": "Historical value-add cannot be measured without the named control comparison.",
        "missing_comparison": missing_comparison,
        "availability": availability,
        "behavior_change_authorized": False,
    }
