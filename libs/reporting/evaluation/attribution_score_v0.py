from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping
import sys
from . import attribution_score_v0_as_rows as _a34_as_rows
from . import attribution_score_v0_num as _a34_num
from . import attribution_score_v0_clamp_score as _a34_clamp_score
from . import attribution_score_v0_score as _a34_score
from . import attribution_score_v0_selection_integrity as _a34_selection_integrity
from . import attribution_score_v0_scanner_alignment as _a34_scanner_alignment
from . import attribution_score_v0_entry_timing as _a34_entry_timing
from . import attribution_score_v0_exit_horizon as _a34_exit_horizon
from . import attribution_score_v0_evidence_quality as _a35_evidence_quality
from . import attribution_score_v0_render_attribution_score_v0 as _a35_render_attribution_score_v0


INSUFFICIENT = "INSUFFICIENT_EVIDENCE"
OK = "OK"


def _mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _as_rows(value: Any) -> list[Mapping[str, Any]]:
    return _a34_as_rows._as_rows(value=value, facade=sys.modules[__name__])


def _num(value: Any) -> float | None:
    return _a34_num._num(value=value, facade=sys.modules[__name__])


def _clamp_score(value: float) -> int:
    return _a34_clamp_score._clamp_score(value=value, facade=sys.modules[__name__])


def _score(status: str, value: int | None, reasons: list[str], evidence: Mapping[str, Any] | None = None) -> dict[str, Any]:
    return _a34_score._score(status=status, value=value, reasons=reasons, evidence=evidence, facade=sys.modules[__name__])


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _ledger_day_record(reports_root: Path, day: str) -> dict[str, Any]:
    root = reports_root / "evaluation" / "freeze_window"
    for path in sorted(root.glob("*/daily_ledger.json"), key=lambda item: str(item)):
        payload = _read_json(path)
        for row in payload.get("days") or []:
            if isinstance(row, dict) and str(row.get("day") or "") == day:
                return dict(row)
    return {}


def _selection_integrity(selection_authority: Mapping[str, Any]) -> dict[str, Any]:
    return _a34_selection_integrity._selection_integrity(selection_authority=selection_authority, facade=sys.modules[__name__])


def _scanner_alignment(selection_authority: Mapping[str, Any], models: list[Mapping[str, Any]]) -> dict[str, Any]:
    return _a34_scanner_alignment._scanner_alignment(selection_authority=selection_authority, models=models, facade=sys.modules[__name__])


def _entry_timing(entry_timing_report: Mapping[str, Any]) -> dict[str, Any]:
    return _a34_entry_timing._entry_timing(entry_timing_report=entry_timing_report, facade=sys.modules[__name__])


def _exit_horizon(horizon_report: Mapping[str, Any]) -> dict[str, Any]:
    return _a34_exit_horizon._exit_horizon(horizon_report=horizon_report, facade=sys.modules[__name__])


def _evidence_quality(
    *,
    daily_scorecard: Mapping[str, Any],
    selection_authority: Mapping[str, Any],
    horizon_report: Mapping[str, Any],
    entry_timing_report: Mapping[str, Any],
    ledger_day: Mapping[str, Any],
) -> dict[str, Any]:
    return _a35_evidence_quality._evidence_quality(daily_scorecard=daily_scorecard, selection_authority=selection_authority, horizon_report=horizon_report, entry_timing_report=entry_timing_report, ledger_day=ledger_day, facade=sys.modules[__name__])


def build_attribution_score_v0(
    *,
    day: str,
    reports_root: Path,
    models: list[Mapping[str, Any]],
    daily_scorecard: Mapping[str, Any],
    selection_authority: Mapping[str, Any],
    horizon_compliance: Mapping[str, Any],
    entry_timing: Mapping[str, Any],
) -> dict[str, Any]:
    ledger_day = _ledger_day_record(Path(reports_root), day)
    scores = {
        "selection_integrity_score": _selection_integrity(selection_authority),
        "scanner_alignment_score": _scanner_alignment(selection_authority, models),
        "entry_timing_score": _entry_timing(entry_timing),
        "exit_horizon_score": _exit_horizon(horizon_compliance),
        "evidence_quality_score": _evidence_quality(
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
        if value.get("status") != INSUFFICIENT and value.get("score") is not None
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


def render_attribution_score_v0(payload: Mapping[str, Any]) -> str:
    return _a35_render_attribution_score_v0.render_attribution_score_v0(payload=payload, facade=sys.modules[__name__])


__all__ = ["build_attribution_score_v0", "render_attribution_score_v0"]
