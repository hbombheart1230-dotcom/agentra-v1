"""entry_timing_attribution: ``_checkpoint`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _checkpoint(forward: Mapping[str, Any], horizon: str, *, facade: Any) -> Mapping[str, Any]:
    return facade._mapping(facade._mapping(forward.get("checkpoints")).get(horizon))
