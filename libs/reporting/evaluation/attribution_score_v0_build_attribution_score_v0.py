"""attribution_score_v0: ``build_attribution_score_v0`` body (moved verbatim from ``attribution_score_v0``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def build_attribution_score_v0(
    *,
    day: str,
    reports_root: Path,
    models: list[Mapping[str, Any]],
    daily_scorecard: Mapping[str, Any],
    selection_authority: Mapping[str, Any],
    horizon_compliance: Mapping[str, Any],
    entry_timing: Mapping[str, Any],
    facade: Any,
) -> dict[str, Any]:
    ledger_day = facade._ledger_day_record(facade.Path(reports_root), day)
    scores = {
        "selection_integrity_score": facade._selection_integrity(selection_authority),
        "scanner_alignment_score": facade._scanner_alignment(selection_authority, models),
        "entry_timing_score": facade._entry_timing(entry_timing),
        "exit_horizon_score": facade._exit_horizon(horizon_compliance),
        "evidence_quality_score": facade._evidence_quality(
            daily_scorecard=daily_scorecard,
            selection_authority=selection_authority,
            horizon_report=horizon_compliance,
            entry_timing_report=entry_timing,
            ledger_day=ledger_day,
        ),
    }
    scored = {
        key: value["score"]
        for key, value in scores.items()
        if value.get("status") != facade.INSUFFICIENT and value.get("score") is not None
    }
    behavior_scored = {
        key: value
        for key, value in scored.items()
        if key != "evidence_quality_score"
    }
    weakest = (
        min(behavior_scored.items(), key=lambda item: item[1])
        if behavior_scored
        else ("", None)
    )
    return {
        "schema_version": "attribution_score_v0.v1",
        "evaluation_program_id": "Q13_ATTRIBUTION_SCORE_V0",
        "behavior_effect": "observation_only",
        "day": day,
        "scores": scores,
        "weakest_observed_axis": {
            "name": weakest[0],
            "score": weakest[1],
        },
        "interpretation_rule": (
            "Lower score means the axis is a stronger diagnostic suspect. "
            "INSUFFICIENT_EVIDENCE is excluded from weakest-axis selection."
        ),
        "limitations": [
            "Scores are simple explainable diagnostics, not prediction models.",
            "No trading behavior is changed by this report.",
            "A low score identifies a patch candidate; it does not authorize a behavior patch by itself.",
        ],
    }
