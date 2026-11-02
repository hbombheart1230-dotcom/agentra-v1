from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping, Sequence
import sys

from .metrics import performance_metrics
from . import scanner_alignment_root_cause_mapping as _a49_sca_mapping
from . import scanner_alignment_root_cause_rows as _a49_sca_rows
from . import scanner_alignment_root_cause_num as _a49_sca_num
from . import scanner_alignment_root_cause_symbol as _a50_symbol
from . import scanner_alignment_root_cause_selected_rank as _a50_selected_rank
from . import scanner_alignment_root_cause_score_gap as _a50_score_gap
from . import scanner_alignment_root_cause_outcome_return as _a50_outcome_return
from . import scanner_alignment_root_cause_impact_score as _a50_impact_score
from . import scanner_alignment_root_cause_diagnostic_kind as _a50_diagnostic_kind
from . import scanner_alignment_root_cause_largest_cause as _a50_largest_cause
from . import scanner_alignment_root_cause_patch_candidate as _a50_patch_candidate
from . import scanner_alignment_root_cause_classify as _a53_classify
from . import scanner_alignment_root_cause_render as _a53_render
from . import scanner_alignment_root_cause_build_scanner_alignment_root_cause_report as _a55_sar_build
from . import scanner_alignment_root_cause_load_day_models_and_evaluations as _a55_sar_load
from . import scanner_alignment_root_cause_build_scanner_alignment_root_cause_range as _a55_sar_range
from . import scanner_alignment_root_cause_read_json as _a55_sar_read_json


ROOT_CAUSES = (
    "Scanner Ranking Failure",
    "Rank Drift",
    "Strategist Override",
    "Candidate Filtering",
    "Symbol Mapping",
    "Missing Evidence",
    "Aligned / No Alignment Issue",
)

OUTCOME_CONDITIONED_CAUSES = {
    "Scanner Ranking Failure",
    "Aligned / No Alignment Issue",
}

EVIDENCE_GAP_CAUSES = {"Missing Evidence"}


def _mapping(value: Any) -> Mapping[str, Any]:
    return _a49_sca_mapping._mapping(value, facade=sys.modules[__name__])


def _rows(value: Any) -> list[Mapping[str, Any]]:
    return _a49_sca_rows._rows(value, facade=sys.modules[__name__])


def _num(value: Any) -> float | None:
    return _a49_sca_num._num(value, facade=sys.modules[__name__])


def _symbol(value: Any) -> str:
    return _a50_symbol._symbol(value, facade=sys.modules[__name__])


def _read_json(path: Path) -> dict[str, Any]:
    return _a55_sar_read_json._read_json(path, facade=sys.modules[__name__])


def _selected_rank(model: Mapping[str, Any]) -> int | None:
    return _a50_selected_rank._selected_rank(model, facade=sys.modules[__name__])


def _score_gap(model: Mapping[str, Any]) -> float | None:
    return _a50_score_gap._score_gap(model, facade=sys.modules[__name__])


def _outcome_return(evaluation: Mapping[str, Any], model: Mapping[str, Any]) -> float | None:
    return _a50_outcome_return._outcome_return(evaluation, model, facade=sys.modules[__name__])


def classify_scanner_alignment_root_cause(
    *,
    row: Mapping[str, Any],
    model: Mapping[str, Any],
    net_return_pct: float | None,
) -> dict[str, Any]:
    return _a53_classify.classify_scanner_alignment_root_cause(row=row, model=model, net_return_pct=net_return_pct, facade=sys.modules[__name__])


def _impact_score(returns: list[float]) -> float:
    return _a50_impact_score._impact_score(returns, facade=sys.modules[__name__])


def _diagnostic_kind(cause: str) -> str:
    return _a50_diagnostic_kind._diagnostic_kind(cause, facade=sys.modules[__name__])


def _largest_cause(
    cause_summary: Sequence[Mapping[str, Any]],
    *,
    excluded: set[str] | None = None,
) -> dict[str, Any]:
    return _a50_largest_cause._largest_cause(cause_summary, excluded=excluded, facade=sys.modules[__name__])


def _patch_candidate(cause: str) -> str:
    return _a50_patch_candidate._patch_candidate(cause, facade=sys.modules[__name__])


def build_scanner_alignment_root_cause_report(
    *,
    day: str,
    models: Sequence[Mapping[str, Any]],
    evaluations: Sequence[Mapping[str, Any]],
    selection_authority: Mapping[str, Any],
) -> dict[str, Any]:
    return _a55_sar_build.build_scanner_alignment_root_cause_report(day=day, models=models, evaluations=evaluations, selection_authority=selection_authority, facade=sys.modules[__name__])


def render_scanner_alignment_root_cause_report(payload: Mapping[str, Any]) -> str:
    return _a53_render.render_scanner_alignment_root_cause_report(payload, facade=sys.modules[__name__])


def _load_day_models_and_evaluations(reports_root: Path, day: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    return _a55_sar_load._load_day_models_and_evaluations(reports_root, day, facade=sys.modules[__name__])


def build_scanner_alignment_root_cause_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
) -> dict[str, Any]:
    return _a55_sar_range.build_scanner_alignment_root_cause_range(reports_root=reports_root, start=start, end=end, facade=sys.modules[__name__])


def write_scanner_alignment_root_cause_range(
    *,
    reports_root: Path = Path("reports"),
    start: str,
    end: str,
) -> dict[str, str]:
    reports_root = Path(reports_root)
    payload = build_scanner_alignment_root_cause_range(
        reports_root=reports_root,
        start=start,
        end=end,
    )
    out_dir = reports_root / "evaluation" / "range" / f"{start}_{end}"
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "scanner_alignment_root_cause_report.json"
    md_path = out_dir / "scanner_alignment_root_cause_report.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_scanner_alignment_root_cause_report(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}


__all__ = [
    "build_scanner_alignment_root_cause_report",
    "render_scanner_alignment_root_cause_report",
    "build_scanner_alignment_root_cause_range",
    "write_scanner_alignment_root_cause_range",
]
