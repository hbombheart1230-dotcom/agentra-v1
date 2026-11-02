"""episode_scanner_review: ``_checkpoint_return`` body (moved verbatim from ``episode_scanner_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _checkpoint_return(row: Mapping[str, Any], horizon: str, *, facade: Any) -> float | None:
    checkpoints = facade._mapping(facade._mapping(row.get("shadow_forward_outcome")).get("checkpoints"))
    checkpoint = facade._mapping(checkpoints.get(horizon))
    if str(checkpoint.get("status") or "") != "observed":
        return None
    return facade._number(checkpoint.get("return_pct"))
