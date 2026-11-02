"""scanner_alignment_root_cause: ``_patch_candidate`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _patch_candidate(cause: str, *, facade: Any) -> str:
    if cause == "Candidate Filtering":
        return "Tighten runner-up/candidate filtering evidence before selecting below post-strategy top1."
    if cause == "Strategist Override":
        return "Audit strategy-context rank adjustments before allowing post-strategy top1 to replace raw top1."
    if cause == "Rank Drift":
        return "Require explicit rank-drift reason and score-gap evidence when Top1 changes."
    if cause == "Scanner Ranking Failure":
        return "Decompose scanner raw score components for aligned losing Top1 trades."
    if cause == "Symbol Mapping":
        return "Fix symbol propagation before any trading behavior patch."
    if cause == "Missing Evidence":
        return "Fix missing selection evidence before interpreting scanner alignment."
    return "No scanner-alignment behavior patch candidate from aligned rows."
