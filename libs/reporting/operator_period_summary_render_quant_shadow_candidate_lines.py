"""operator_period_summary: ``_render_quant_shadow_candidate_lines`` body (moved verbatim from ``operator_period_summary``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple


def _render_quant_shadow_candidate_lines(payload: Dict[str, Any], *, facade: Any) -> List[str]:
    shadow_eval = payload.get("quant_shadow_candidate_evaluation")
    if not isinstance(shadow_eval, dict):
        return []
    return facade.render_quant_shadow_candidate_evaluation_lines(shadow_eval)
