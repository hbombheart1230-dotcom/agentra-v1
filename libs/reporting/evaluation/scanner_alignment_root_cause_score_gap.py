"""scanner_alignment_root_cause: ``_score_gap`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _score_gap(model: Mapping[str, Any], *, facade: Any) -> float | None:
    selection = facade._mapping(model.get("selection"))
    top1 = facade._mapping(selection.get("scanner_top1"))
    selected = facade._mapping(selection.get("selected_candidate"))
    top_score = facade._num(top1.get("score_total"))
    selected_score = facade._num(selected.get("score_total"))
    if top_score is None or selected_score is None:
        return None
    return round(top_score - selected_score, 6)
