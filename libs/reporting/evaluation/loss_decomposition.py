from __future__ import annotations

import json
from collections import defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path
from statistics import median
from typing import Any, Iterable, Mapping
import sys

from libs.reporting.q8_evaluation_contract import dedupe_q8_candidates
from libs.reporting.quant_shadow_candidate_evaluation import (
    build_quant_shadow_candidate_evaluation,
    load_quant_shadow_candidate_payloads_for_range,
)
from libs.reporting.quant_shadow_forward_outcomes import attach_forward_outcomes

from .artifact_inventory import iter_trade_dirs
from .metrics import performance_metrics
from .trade_read_model import build_q9_trade_read_model
from . import loss_decomposition_to_float as _a42_to_float
from . import loss_decomposition_parse_ts as _a42_parse_ts
from . import loss_decomposition_iter_days as _a42_iter_days
from . import loss_decomposition_checkpoint_return as _a42_checkpoint_return
from . import loss_decomposition_rank_bucket as _a42_rank_bucket
from . import loss_decomposition_candidate_rows as _a42_candidate_rows
from . import loss_decomposition_group_forward as _a42_group_forward
from . import loss_decomposition_realized_trade_summary as _a42_realized_trade_summary
from . import loss_decomposition_entry_timing_summary as _a45_entry_timing_summary
from . import loss_decomposition_exit_hold_summary as _a45_exit_hold_summary
from . import loss_decomposition_diagnosis as _a45_diagnosis
from . import loss_decomposition_next_action as _a45_next_action
from . import loss_decomposition_render_loss_decomposition as _a45_render_loss_decomposition


def _to_float(value: Any) -> float | None:
    return _a42_to_float._to_float(value, facade=sys.modules[__name__])


def _parse_ts(value: Any) -> datetime | None:
    return _a42_parse_ts._parse_ts(value, facade=sys.modules[__name__])


def _iter_days(start: str, end: str) -> Iterable[str]:
    yield from _a42_iter_days._iter_days(start, end, facade=sys.modules[__name__])


def _checkpoint_return(row: Mapping[str, Any], label: str) -> float | None:
    return _a42_checkpoint_return._checkpoint_return(row, label, facade=sys.modules[__name__])


def _rank_bucket(value: Any) -> str:
    return _a42_rank_bucket._rank_bucket(value, facade=sys.modules[__name__])


def _candidate_rows(payloads: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _a42_candidate_rows._candidate_rows(payloads, facade=sys.modules[__name__])


def _group_forward(rows: list[dict[str, Any]], key_fn: Any) -> list[dict[str, Any]]:
    return _a42_group_forward._group_forward(rows, key_fn, facade=sys.modules[__name__])


def _load_trade_models(reports_root: Path, start: str, end: str) -> list[dict[str, Any]]:
    models: list[dict[str, Any]] = []
    for day in _iter_days(start, end):
        models.extend(build_q9_trade_read_model(path) for path in iter_trade_dirs(reports_root, day))
    return models


def _realized_trade_summary(models: list[dict[str, Any]]) -> dict[str, Any]:
    return _a42_realized_trade_summary._realized_trade_summary(models, facade=sys.modules[__name__])


def _entry_timing_summary(
    models: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
) -> dict[str, Any]:
    return _a45_entry_timing_summary._entry_timing_summary(models, candidates, facade=sys.modules[__name__])


def _exit_hold_summary(models: list[dict[str, Any]]) -> dict[str, Any]:
    return _a45_exit_hold_summary._exit_hold_summary(models, facade=sys.modules[__name__])


def _diagnosis(
    *,
    shadow: dict[str, Any],
    candidate_rank: list[dict[str, Any]],
    realized: dict[str, Any],
    entry: dict[str, Any],
    exit_hold: dict[str, Any],
) -> list[dict[str, Any]]:
    return _a45_diagnosis._diagnosis(shadow=shadow, candidate_rank=candidate_rank, realized=realized, entry=entry, exit_hold=exit_hold, facade=sys.modules[__name__])


def _next_action(
    *,
    role_rows: list[dict[str, Any]],
    realized: dict[str, Any],
    exit_hold: dict[str, Any],
) -> dict[str, Any]:
    return _a45_next_action._next_action(role_rows=role_rows, realized=realized, exit_hold=exit_hold, facade=sys.modules[__name__])


def build_loss_decomposition(*, reports_root: Path, start: str, end: str) -> dict[str, Any]:
    payloads = load_quant_shadow_candidate_payloads_for_range(
        reports_root=reports_root,
        start=start,
        end=end,
    )
    shadow = build_quant_shadow_candidate_evaluation(payloads)
    candidates = _candidate_rows(payloads)
    models = _load_trade_models(reports_root, start, end)
    rank_rows = _group_forward(candidates, lambda row: _rank_bucket(row.get("rank")))
    role_rows = _group_forward(candidates, lambda row: row.get("shadow_role"))
    tactic_rows = _group_forward(candidates, lambda row: row.get("quant_tactic_id"))
    realized = _realized_trade_summary(models)
    entry = _entry_timing_summary(models, candidates)
    exit_hold = _exit_hold_summary(models)
    observed_days = sorted({
        str(day)
        for row in ((shadow.get("entry_lane_forward_outcomes") or {}).get("by_time_bucket") or [])
        if isinstance(row, Mapping)
        for day in row.get("observed_days") or []
    })
    return {
        "schema_version": "full_chain_loss_decomposition.v1",
        "behavior_effect": "evaluation_only",
        "range": {"start": start[:10], "end": end[:10]},
        "evidence": {
            "shadow_payload_count": len(payloads),
            "raw_shadow_candidate_count": shadow.get("candidate_count"),
            "deduped_shadow_candidate_count": shadow.get("deduped_candidate_count"),
            "trusted_forward_count": shadow.get("forward_outcome_available_count"),
            "trusted_forward_coverage": shadow.get("forward_outcome_coverage"),
            "trusted_forward_observed_days": observed_days,
            "trade_model_count": len(models),
        },
        "raw_candidate_edge": {
            "by_time_bucket": ((shadow.get("entry_lane_forward_outcomes") or {}).get("by_time_bucket") or []),
            "by_lane": ((shadow.get("entry_lane_forward_outcomes") or {}).get("by_primary_lane") or []),
            "by_tactic": tactic_rows,
        },
        "scanner_ranking": {
            "by_rank_bucket": rank_rows,
            "by_selection_role": role_rows,
            "control_status": "RECONSTRUCTED_ONLY",
        },
        "strategist_commander": {
            "status": "UNAVAILABLE",
            "reason": "true pre-Strategist Scanner control and explicit Commander alternative outcomes were not historically persisted",
        },
        "monitor_entry": entry,
        "monitor_exit": exit_hold,
        "realized_system": realized,
        "diagnosis": _diagnosis(
            shadow=shadow,
            candidate_rank=rank_rows,
            realized=realized,
            entry=entry,
            exit_hold=exit_hold,
        ),
        "next_action": _next_action(
            role_rows=role_rows,
            realized=realized,
            exit_hold=exit_hold,
        ),
    }


def render_loss_decomposition(payload: Mapping[str, Any]) -> str:
    return _a45_render_loss_decomposition.render_loss_decomposition(payload, facade=sys.modules[__name__])


def write_loss_decomposition(
    *,
    reports_root: Path,
    start: str,
    end: str,
    output_dir: Path,
) -> dict[str, str]:
    payload = build_loss_decomposition(reports_root=reports_root, start=start, end=end)
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "full_chain_loss_decomposition.json"
    md_path = output_dir / "full_chain_loss_decomposition.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_path.write_text(render_loss_decomposition(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(md_path)}
