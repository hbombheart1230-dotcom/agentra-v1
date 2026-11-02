"""full_chain_component_review: ``_q9_role_row`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _q9_role_row(
    roles: Mapping[str, list[dict[str, Any]]],
    role: str,
    *,
    facade: Any,
) -> dict[str, Any]:
    rows = roles.get(role) or []
    if role == "B_STRATEGIST_RANKED":
        selected = next((row for row in rows if row.get("q9_selected")), None)
        if selected:
            return selected
    return min(
        rows,
        key=lambda row: int(float(row.get("rank") or 999)),
        default={},
    )
