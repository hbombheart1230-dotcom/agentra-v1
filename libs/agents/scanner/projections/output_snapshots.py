from __future__ import annotations

import sys
from typing import Any, Dict, List

from libs.runtime.quant.factors import build_factor_snapshot_from_candidate
from libs.runtime.scanner.theme_filter import candidate_theme_match
from libs.agents.scanner.projections import scanner_snapshot_numeric as _c03_12_a1_owner
from libs.agents.scanner.projections import scanner_snapshot_selected as _c03_12_a2_owner
from libs.agents.scanner.projections import scanner_snapshot_coverage as _c03_12_a3_owner
from libs.agents.scanner.projections import scanner_snapshot_features as _c03_12_a4_owner
from libs.agents.scanner.projections import scanner_snapshot_ranking as _c03_12_a5_owner


def to_float(v: Any, default: float = 0.0) -> float:
    return _c03_12_a1_owner.to_float(v, default)


def compact_selected_snapshot(selected: Dict[str, Any] | None) -> Dict[str, Any]:
    return _c03_12_a2_owner.compact_selected_snapshot(selected, facade=sys.modules[__name__])


def feature_coverage_summary(row: Dict[str, Any]) -> Dict[str, Any]:
    return _c03_12_a3_owner.feature_coverage_summary(row, facade=sys.modules[__name__])


def compact_feature_snapshot(row: Dict[str, Any]) -> Dict[str, Any]:
    return _c03_12_a4_owner.compact_feature_snapshot(row, facade=sys.modules[__name__])


def ranking_table_rows(rows: List[Dict[str, Any]], *, max_rows: int = 5) -> List[Dict[str, Any]]:
    return _c03_12_a5_owner.ranking_table_rows(rows, max_rows=max_rows, facade=sys.modules[__name__])
