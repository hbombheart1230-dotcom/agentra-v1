"""episode_scanner_review: ``_rank_bucket`` body (moved verbatim from ``episode_scanner_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _rank_bucket(rank: int, *, facade: Any) -> str:
    if rank == 1:
        return "rank1"
    if 2 <= rank <= 3:
        return "rank2_3"
    if rank >= 4:
        return "rank4_plus"
    return "unknown"
