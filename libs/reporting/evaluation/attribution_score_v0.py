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
from . import attribution_score_v0_build_attribution_score_v0 as _a37_build_attribution_score_v0
from . import attribution_score_v0_ledger_day_record as _a38_ledger_day_record
from . import attribution_score_v0_read_json as _a38_read_json


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
    return _a38_read_json._read_json(path=path, facade=sys.modules[__name__])


def _ledger_day_record(reports_root: Path, day: str) -> dict[str, Any]:
    return _a38_ledger_day_record._ledger_day_record(reports_root=reports_root, day=day, facade=sys.modules[__name__])


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
    return _a37_build_attribution_score_v0.build_attribution_score_v0(day=day, reports_root=reports_root, models=models, daily_scorecard=daily_scorecard, selection_authority=selection_authority, horizon_compliance=horizon_compliance, entry_timing=entry_timing, facade=sys.modules[__name__])


def render_attribution_score_v0(payload: Mapping[str, Any]) -> str:
    return _a35_render_attribution_score_v0.render_attribution_score_v0(payload=payload, facade=sys.modules[__name__])


__all__ = ["build_attribution_score_v0", "render_attribution_score_v0"]
