"""evaluation_lens_report: ``_checkpoint`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _checkpoint(row: Mapping[str, Any], horizon: str, *, facade: Any) -> dict[str, Any]:
    outcome = facade._as_dict(row.get("shadow_forward_outcome"))
    checkpoints = facade._as_dict(outcome.get("checkpoints"))
    return facade._as_dict(checkpoints.get(horizon))
