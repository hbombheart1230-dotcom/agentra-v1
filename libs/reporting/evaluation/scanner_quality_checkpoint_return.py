"""scanner_quality: ``_checkpoint_return`` body (moved verbatim from ``scanner_quality``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _checkpoint_return(row: Mapping[str, Any], horizon: str, *, facade: Any) -> float | None:
    outcome = row.get("shadow_forward_outcome")
    outcome = outcome if isinstance(outcome, facade.Mapping) else {}
    checkpoints = outcome.get("checkpoints")
    checkpoints = checkpoints if isinstance(checkpoints, facade.Mapping) else {}
    checkpoint = checkpoints.get(horizon)
    checkpoint = checkpoint if isinstance(checkpoint, facade.Mapping) else {}
    if str(checkpoint.get("status") or "") != "observed":
        return None
    return facade._number(checkpoint.get("return_pct"))
