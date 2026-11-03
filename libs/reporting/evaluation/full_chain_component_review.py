from __future__ import annotations

import json
from collections import defaultdict
import os
from pathlib import Path
from typing import Any, Mapping
import sys

from libs.reporting.q8_evaluation_contract import candidate_day
from libs.reporting.quant_shadow_candidate_evaluation import (
    Q9_ROW_KEYS_UNUSED_BY_FULL_CHAIN,
    load_quant_shadow_candidate_payloads_for_range,
)
from libs.reporting.quant_shadow_forward_outcomes import attach_forward_outcomes
from libs.runtime.broker_cost_profile import load_broker_cost_profile

from .contracts import (
    CONTRACT_VERSION,
    DIRECTIONAL_MIN_DAYS,
    DIRECTIONAL_MIN_OBSERVATIONS,
    DecisionClass,
)
from .loss_decomposition import (
    _candidate_rows,
    _checkpoint_return,
    _entry_timing_summary,
    _exit_hold_summary,
    _load_trade_models,
    _realized_trade_summary,
)
from .metrics import performance_metrics
from .scanner_quality import build_scanner_quality_review
from . import full_chain_component_review_number as _a52_number
from . import full_chain_component_review_behavior_metric_eligible as _a52_behavior_metric_eligible
from . import full_chain_component_review_topk_metric as _a52_topk_metric
from . import full_chain_component_review_classify_root_cause as _a52_classify_root_cause
from . import full_chain_component_review_role_metrics as _a52_role_metrics
from . import full_chain_component_review_paired_role_deltas as _a52_paired_role_deltas
from . import full_chain_component_review_selection_availability as _a52_selection_availability
from . import full_chain_component_review_q9_decision_candidate_rows as _a52_q9_decision_candidate_rows
from . import full_chain_component_review_q9_role_row as _a53_q9_role_row
from . import full_chain_component_review_decision_window_attribution as _a53_decision_window_attribution
from . import full_chain_component_review_attribution_component as _a53_attribution_component
from . import full_chain_component_review_scanner_decision as _a53_scanner_decision
from . import full_chain_component_review_unavailable_component as _a53_unavailable_component
from . import full_chain_component_review_render as _a53_render
from . import full_chain_component_review_build_full_chain_component_review as _a56_fc_build


HORIZONS = ("+5m", "+15m", "+30m", "+60m")
MIN_MATERIAL_RANKING_DELTA_PCT = 0.30
MIN_POSITIVE_RANKING_DELTA_RATE = 0.55
DEFAULT_Q9_SLIPPAGE_PCT = 0.05
BEHAVIOR_METRIC_EXCLUSION_DEFECTS = {
    "broker_day_partial_exit_duplicate",
    "confirmed_runtime_defect",
}


def _number(value: Any) -> float | None:
    return _a52_number._number(value, facade=sys.modules[__name__])


def _behavior_metric_eligible(model: Mapping[str, Any]) -> bool:
    return _a52_behavior_metric_eligible._behavior_metric_eligible(model, facade=sys.modules[__name__])


def _topk_metric(
    scanner_quality: Mapping[str, Any],
    *,
    top_k: int,
    horizon: str,
) -> dict[str, Any]:
    return _a52_topk_metric._topk_metric(scanner_quality, top_k=top_k, horizon=horizon, facade=sys.modules[__name__])


def _classify_root_cause(
    *,
    scanner_quality: Mapping[str, Any],
    attribution: Mapping[str, Any],
    entry: Mapping[str, Any],
    exit_hold: Mapping[str, Any],
) -> dict[str, Any]:
    return _a52_classify_root_cause._classify_root_cause(scanner_quality=scanner_quality, attribution=attribution, entry=entry, exit_hold=exit_hold, facade=sys.modules[__name__])


def _role_metrics(
    candidates: list[dict[str, Any]],
    *,
    role: str,
    horizon: str,
    cost_pct: float,
) -> dict[str, Any]:
    return _a52_role_metrics._role_metrics(candidates, role=role, horizon=horizon, cost_pct=cost_pct, facade=sys.modules[__name__])


def _paired_role_deltas(
    candidates: list[dict[str, Any]],
    *,
    horizon: str,
) -> dict[str, Any]:
    return _a52_paired_role_deltas._paired_role_deltas(candidates, horizon=horizon, facade=sys.modules[__name__])


def _selection_availability(models: list[dict[str, Any]]) -> dict[str, Any]:
    return _a52_selection_availability._selection_availability(models, facade=sys.modules[__name__])


def _q9_decision_candidate_rows(payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _a52_q9_decision_candidate_rows._q9_decision_candidate_rows(payloads, facade=sys.modules[__name__])


def _q9_role_row(
    roles: Mapping[str, list[dict[str, Any]]],
    role: str,
) -> dict[str, Any]:
    return _a53_q9_role_row._q9_role_row(roles, role, facade=sys.modules[__name__])


def _decision_window_attribution(
    payloads: list[dict[str, Any]],
    *,
    cost_pct: float,
) -> dict[str, Any]:
    return _a53_decision_window_attribution._decision_window_attribution(payloads, cost_pct=cost_pct, facade=sys.modules[__name__])


def _attribution_component(
    *,
    attribution: Mapping[str, Any],
    component: str,
    question: str,
    missing_comparison: str,
    availability: dict[str, Any],
) -> dict[str, Any]:
    return _a53_attribution_component._attribution_component(attribution=attribution, component=component, question=question, missing_comparison=missing_comparison, availability=availability, facade=sys.modules[__name__])


def _scanner_decision(
    *,
    role_metrics: list[dict[str, Any]],
    paired: list[dict[str, Any]],
) -> dict[str, Any]:
    return _a53_scanner_decision._scanner_decision(role_metrics=role_metrics, paired=paired, facade=sys.modules[__name__])


def _unavailable_component(
    *,
    question: str,
    missing_comparison: str,
    availability: dict[str, Any],
) -> dict[str, Any]:
    return _a53_unavailable_component._unavailable_component(question=question, missing_comparison=missing_comparison, availability=availability, facade=sys.modules[__name__])


def build_full_chain_component_review(
    *,
    reports_root: Path,
    start: str,
    end: str,
    cost_profile_path: Path | None = None,
) -> dict[str, Any]:
    return _a56_fc_build.build_full_chain_component_review(reports_root=reports_root, start=start, end=end, cost_profile_path=cost_profile_path, facade=sys.modules[__name__])


def render_full_chain_component_review(payload: Mapping[str, Any]) -> str:
    return _a53_render.render_full_chain_component_review(payload, facade=sys.modules[__name__])


def write_full_chain_component_review(
    *,
    reports_root: Path,
    start: str,
    end: str,
    output_dir: Path,
    cost_profile_path: Path | None = None,
) -> dict[str, str]:
    payload = build_full_chain_component_review(
        reports_root=reports_root,
        start=start,
        end=end,
        cost_profile_path=cost_profile_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "q9_full_chain_component_review.json"
    md_path = output_dir / "q9_full_chain_component_review.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_full_chain_component_review(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}
