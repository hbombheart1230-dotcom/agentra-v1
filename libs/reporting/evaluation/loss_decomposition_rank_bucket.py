"""loss_decomposition: ``_rank_bucket`` body (moved verbatim from ``loss_decomposition``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _rank_bucket(value: Any, *, facade: Any) -> str:
    try:
        rank = int(float(value))
    except (TypeError, ValueError):
        return "unknown"
    if rank == 1:
        return "rank1"
    if rank <= 3:
        return "rank2-3"
    if rank <= 5:
        return "rank4-5"
    if rank <= 10:
        return "rank6-10"
    return "rank11+"
