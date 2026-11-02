"""evaluation_lens_report: ``_blocker`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _blocker(row: Mapping[str, Any], *, facade: Any) -> str:
    for key in ("guard_reason", "reason", "primary_failure_axis"):
        value = facade._text(row.get(key))
        if value:
            return value
    decision = facade._as_dict(row.get("entry_quant_decision"))
    blockers = decision.get("blockers")
    if isinstance(blockers, list) and blockers:
        return facade._text(blockers[0])
    return "unknown"
