"""scanner_alignment_root_cause: ``_selected_rank`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _selected_rank(model: Mapping[str, Any], *, facade: Any) -> int | None:
    selection = facade._mapping(model.get("selection"))
    selected_candidate = facade._mapping(selection.get("selected_candidate"))
    value = facade._num(selection.get("selected_rank") or selected_candidate.get("rank"))
    return int(value) if value is not None else None
