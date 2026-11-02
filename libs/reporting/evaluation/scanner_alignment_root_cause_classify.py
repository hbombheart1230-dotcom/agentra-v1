"""scanner_alignment_root_cause: ``classify_scanner_alignment_root_cause`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def classify_scanner_alignment_root_cause(
    *,
    row: Mapping[str, Any],
    model: Mapping[str, Any],
    net_return_pct: float | None,
    facade: Any,
) -> dict[str, Any]:
    raw = str(row.get("raw_scanner_top1") or "")
    post = str(row.get("post_strategy_top1") or "")
    selected = str(row.get("selected_symbol") or "")
    executed = str(row.get("executed_symbol") or "")
    rank = facade._selected_rank(model)
    score_gap = facade._score_gap(model)
    reasons: list[str] = []

    if not raw or not post or not selected or not executed:
        return {
            "root_cause": "Missing Evidence",
            "confidence": "high",
            "reasons": ["raw/post/selected/executed symbol missing"],
            "selected_rank": rank,
            "score_gap": score_gap,
        }

    if (
        row.get("final_to_executed_changed") is True
        or row.get("monitor_to_commander_changed") is True
        or row.get("selected_to_monitor_changed") is True
    ):
        return {
            "root_cause": "Symbol Mapping",
            "confidence": "high",
            "reasons": ["symbol changed after selection path"],
            "selected_rank": rank,
            "score_gap": score_gap,
        }

    if selected != post and rank is not None and rank > 1:
        reasons.append("selected candidate is below post-strategy top1")
        reasons.append(f"selected_rank={rank}")
        if score_gap is not None:
            reasons.append(f"score_gap={score_gap}")
        return {
            "root_cause": "Candidate Filtering",
            "confidence": "high",
            "reasons": reasons,
            "selected_rank": rank,
            "score_gap": score_gap,
        }

    if raw != post and selected == post:
        return {
            "root_cause": "Strategist Override",
            "confidence": "medium",
            "reasons": ["post-strategy top1 differs from raw top1 and final selection followed post-strategy top1"],
            "selected_rank": rank,
            "score_gap": score_gap,
        }

    if raw != post or (rank is not None and rank > 1):
        reasons.append("top candidate changed or selected rank drifted")
        if raw != post:
            reasons.append("raw_top1_differs_from_post_strategy_top1")
        if rank is not None and rank > 1:
            reasons.append(f"selected_rank={rank}")
        return {
            "root_cause": "Rank Drift",
            "confidence": "medium",
            "reasons": reasons,
            "selected_rank": rank,
            "score_gap": score_gap,
        }

    if net_return_pct is not None and net_return_pct < 0:
        return {
            "root_cause": "Scanner Ranking Failure",
            "confidence": "medium",
            "reasons": ["top-ranked selected candidate produced negative realized return"],
            "selected_rank": rank,
            "score_gap": score_gap,
        }

    return {
        "root_cause": "Aligned / No Alignment Issue",
        "confidence": "medium",
        "reasons": ["raw/post/selected/executed symbols are aligned"],
        "selected_rank": rank,
        "score_gap": score_gap,
    }
