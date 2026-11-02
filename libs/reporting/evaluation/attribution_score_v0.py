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
    integrity = _mapping(daily_scorecard.get("artifact_integrity"))
    counts = _mapping(integrity.get("status_counts"))
    total = sum(int(value or 0) for value in counts.values())
    if total <= 0:
        return _score(INSUFFICIENT, None, ["artifact_integrity_counts_missing"])
    selection_summary = _mapping(selection_authority.get("summary"))
    explicitly_excluded = sum(
        int(value or 0)
        for key, value in selection_summary.items()
        if str(key).startswith("excluded:")
    )
    if explicitly_excluded >= total:
        return _score(
            OK,
            100,
            ["all_trade_rows_explicitly_excluded_from_behavior_metrics"],
            {
                "integrity_status_counts": dict(counts),
                "explicitly_excluded_trade_count": explicitly_excluded,
                "ledger_day_present": bool(ledger_day),
                "ledger_evidence_status": ledger_day.get("evidence_status") if ledger_day else "",
            },
        )
    pass_count = int(counts.get("PASS") or 0)
    watch_count = int(counts.get("WATCH") or 0)
    score = ((pass_count + (0.7 * watch_count)) / total) * 100.0
    reasons: list[str] = []
    if int(counts.get("FAIL") or 0) > 0:
        reasons.append("fail_integrity_rows_present")
    if int(counts.get("BLOCKER") or 0) > 0:
        reasons.append("blocker_integrity_rows_present")
    if not _as_rows(selection_authority.get("rows")):
        score -= 10.0
        reasons.append("selection_authority_rows_missing")
    if not _as_rows(horizon_report.get("rows")):
        score -= 10.0
        reasons.append("horizon_rows_missing")
    if not _as_rows(entry_timing_report.get("rows")):
        score -= 10.0
        reasons.append("entry_timing_rows_missing")
    if ledger_day:
        evidence_status = str(ledger_day.get("evidence_status") or "")
        if evidence_status and evidence_status.upper() != "COMPLETE":
            score -= 15.0
            reasons.append(f"ledger_evidence_status:{evidence_status}")
    return _score(
        OK,
        _clamp_score(score),
        reasons or ["evidence_surfaces_available"],
        {
            "integrity_status_counts": dict(counts),
            "ledger_day_present": bool(ledger_day),
            "ledger_evidence_status": ledger_day.get("evidence_status") if ledger_day else "",
        },
    )


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
    lines = [
        f"# Q13 Attribution Score v0 - {payload.get('day', '')}",
        "",
        f"- Behavior effect: `{payload.get('behavior_effect', '')}`",
        f"- Weakest observed axis: `{_mapping(payload.get('weakest_observed_axis')).get('name') or '-'}` "
        f"({_mapping(payload.get('weakest_observed_axis')).get('score')})",
        "",
        "## Scores",
        "",
        "| Axis | Status | Score | Reasons |",
        "| --- | --- | ---: | --- |",
    ]
    for key, item in _mapping(payload.get("scores")).items():
        obj = _mapping(item)
        score = obj.get("score")
        reasons = ", ".join(str(reason) for reason in obj.get("reasons") or []) or "-"
        lines.append(
            f"| {key} | {obj.get('status')} | "
            f"{'-' if score is None else int(score)} | {reasons} |"
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        f"- {payload.get('interpretation_rule', '')}",
        "",
        "## Limitations",
        "",
    ])
    for item in payload.get("limitations") or []:
        lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)


__all__ = ["build_attribution_score_v0", "render_attribution_score_v0"]
