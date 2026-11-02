"""evaluation_lens_report: ``_checkpoint_return`` body (moved verbatim from ``evaluation_lens_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _checkpoint_return(row: Mapping[str, Any], horizon: str, *, facade: Any) -> float | None:
    checkpoint = facade._checkpoint(row, horizon)
    if checkpoint.get("status") != "observed":
        return None
    return facade._num(checkpoint.get("return_pct"))
