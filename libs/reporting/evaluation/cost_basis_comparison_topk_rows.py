"""cost_basis_comparison: ``_topk_rows`` body (moved verbatim from ``cost_basis_comparison``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _topk_rows(review: Mapping[str, Any], *, facade: Any) -> dict[tuple[int, str], dict[str, Any]]:
    topk = review.get("topk_forward_performance")
    topk = topk if isinstance(topk, facade.Mapping) else {}
    return {
        (int(row.get("top_k") or 0), str(row.get("horizon") or "")): dict(row)
        for row in topk.get("rows") or []
        if isinstance(row, facade.Mapping)
    }
