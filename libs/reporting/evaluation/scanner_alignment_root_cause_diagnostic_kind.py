"""scanner_alignment_root_cause: ``_diagnostic_kind`` body (moved verbatim from ``scanner_alignment_root_cause``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _diagnostic_kind(cause: str, *, facade: Any) -> str:
    if cause in facade.OUTCOME_CONDITIONED_CAUSES:
        return "outcome_conditioned"
    if cause in facade.EVIDENCE_GAP_CAUSES:
        return "evidence_gap"
    return "structural"
