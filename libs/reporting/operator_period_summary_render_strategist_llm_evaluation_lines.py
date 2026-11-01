"""operator_period_summary: ``_render_strategist_llm_evaluation_lines`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _render_strategist_llm_evaluation_lines(payload: Dict[str, Any], *, facade: Any) -> List[str]:
    evaluation = payload.get("strategist_llm_evaluation")
    if not isinstance(evaluation, dict):
        return []
    return facade.render_strategist_llm_evaluation_lines(evaluation)
