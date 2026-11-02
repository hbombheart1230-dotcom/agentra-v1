from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Mapping
import sys
from . import horizon_alignment_group_key as _a38_group_key
from . import horizon_alignment_profit_factor as _a38_profit_factor
from . import horizon_alignment_text as _a41_text
from . import horizon_alignment_lane_observation as _a41_lane_observation
from . import horizon_alignment_combo_rows as _a41_combo_rows
from . import horizon_alignment_build_horizon_alignment_review as _a41_build_horizon_alignment_review
from . import horizon_alignment_render_horizon_alignment_review as _a41_render_horizon_alignment_review

from libs.reporting.q8_evaluation_contract import candidate_day
from libs.reporting.quant_shadow_candidate_evaluation import (
    load_quant_shadow_candidate_payloads_for_range,
)
from libs.runtime.broker_cost_profile import load_broker_cost_profile

from .loss_decomposition import _candidate_rows, _checkpoint_return
from .metrics import performance_metrics


HORIZONS = ("+5m", "+15m", "+30m", "+60m")
MIN_OBSERVATIONS = 20
MIN_DAYS = 3
MAX_DAY_SHARE = 0.60
MAX_SYMBOL_SHARE = 0.40
MIN_AVERAGE_NET_RETURN_PCT = 0.30
MIN_NET_PROFIT_FACTOR = 1.20


def _text(value: Any, fallback: str = "unknown") -> str:
    return _a41_text._text(value, fallback, facade=sys.modules[__name__])


def _lane_observation(row: Mapping[str, Any]) -> dict[str, Any]:
    return _a41_lane_observation._lane_observation(row, facade=sys.modules[__name__])


def _group_key(row: Mapping[str, Any], dimensions: tuple[str, ...]) -> tuple[str, ...]:
    return _a38_group_key._group_key(row=row, dimensions=dimensions, facade=sys.modules[__name__])


def _profit_factor(values: list[float]) -> float:
    return _a38_profit_factor._profit_factor(values=values, facade=sys.modules[__name__])


def _combo_rows(
    candidates: list[dict[str, Any]],
    *,
    dimensions: tuple[str, ...],
    cost_pct: float,
) -> list[dict[str, Any]]:
    return _a41_combo_rows._combo_rows(candidates, dimensions=dimensions, cost_pct=cost_pct, facade=sys.modules[__name__])


def build_horizon_alignment_review(
    *,
    reports_root: Path,
    start: str,
    end: str,
    cost_profile_path: Path | None = None,
) -> dict[str, Any]:
    return _a41_build_horizon_alignment_review.build_horizon_alignment_review(reports_root=reports_root, start=start, end=end, cost_profile_path=cost_profile_path, facade=sys.modules[__name__])


def render_horizon_alignment_review(payload: Mapping[str, Any]) -> str:
    return _a41_render_horizon_alignment_review.render_horizon_alignment_review(payload, facade=sys.modules[__name__])


def write_horizon_alignment_review(
    *,
    reports_root: Path,
    start: str,
    end: str,
    output_dir: Path,
    cost_profile_path: Path | None = None,
) -> dict[str, str]:
    payload = build_horizon_alignment_review(
        reports_root=reports_root,
        start=start,
        end=end,
        cost_profile_path=cost_profile_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "horizon_alignment_review.json"
    md_path = output_dir / "horizon_alignment_review.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_horizon_alignment_review(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}
