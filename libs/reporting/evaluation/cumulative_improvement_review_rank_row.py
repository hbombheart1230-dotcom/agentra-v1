"""cumulative_improvement_review: ``_rank_row`` body (moved verbatim from ``cumulative_improvement_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _rank_row(
    review: Mapping[str, Any],
    *,
    bucket: str,
    horizon: str,
    facade: Any,
) -> Mapping[str, Any]:
    return next(
        (
            row
            for row in review.get("rank_horizon_rows") or []
            if isinstance(row, facade.Mapping)
            and row.get("rank_bucket") == bucket
            and row.get("horizon") == horizon
        ),
        {},
    )
