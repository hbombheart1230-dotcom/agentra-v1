"""full_chain_component_review: ``_topk_metric`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _topk_metric(
    scanner_quality: Mapping[str, Any],
    *,
    top_k: int,
    horizon: str,
    facade: Any,
) -> dict[str, Any]:
    topk = scanner_quality.get("topk_forward_performance")
    topk = topk if isinstance(topk, facade.Mapping) else {}
    return next(
        (
            dict(row)
            for row in topk.get("rows") or []
            if isinstance(row, facade.Mapping)
            and int(row.get("top_k") or 0) == top_k
            and str(row.get("horizon") or "") == horizon
        ),
        {},
    )
