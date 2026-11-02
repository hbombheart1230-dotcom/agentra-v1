"""loss_decomposition: ``_checkpoint_return`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _checkpoint_return(row: Mapping[str, Any], label: str, *, facade: Any) -> float | None:
    outcome = row.get("shadow_forward_outcome")
    outcome = outcome if isinstance(outcome, facade.Mapping) else {}
    checkpoints = outcome.get("checkpoints")
    checkpoints = checkpoints if isinstance(checkpoints, facade.Mapping) else {}
    checkpoint = checkpoints.get(label)
    if not isinstance(checkpoint, facade.Mapping) or checkpoint.get("status") != "observed":
        return None
    return facade._to_float(checkpoint.get("return_pct"))
