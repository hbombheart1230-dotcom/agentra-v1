from __future__ import annotations

import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence
import sys
from . import entry_timing_attribution_epoch as _a39_epoch
from . import entry_timing_attribution_iso as _a39_iso
from . import entry_timing_attribution_stage_epoch as _a39_stage_epoch
from . import entry_timing_attribution_candidate_symbol as _a39_candidate_symbol
from . import entry_timing_attribution_candidate_rank as _a39_candidate_rank
from . import entry_timing_attribution_row_at_or_before as _a39_row_at_or_before
from . import entry_timing_attribution_daily_windows_by_id as _a39_daily_windows_by_id
from . import entry_timing_attribution_pre_entry_move_pct as _a39_pre_entry_move_pct
from . import entry_timing_attribution_mapping as _a40_mapping
from . import entry_timing_attribution_num as _a40_num
from . import entry_timing_attribution_read_json as _a40_read_json
from . import entry_timing_attribution_entry_forward as _a40_entry_forward
from . import entry_timing_attribution_checkpoint as _a40_checkpoint
from . import entry_timing_attribution_label as _a40_label
from . import entry_timing_attribution_fmt as _a40_fmt
from . import entry_timing_attribution_render_entry_timing_attribution_report as _a40_render_entry_timing_attribution_report

from libs.reporting.quant_shadow_forward_outcomes import (
    attach_forward_outcomes,
    load_minute_rows_from_state,
)

from .metrics import performance_metrics


HORIZONS = ("+5m", "+15m", "+30m", "+60m")
LABELS = (
    "ENTRY_TOO_EARLY",
    "ENTRY_TOO_LATE",
    "ENTRY_APPROPRIATE",
    "INSUFFICIENT_EVIDENCE",
)


def _mapping(value: Any) -> Mapping[str, Any]:
    return _a40_mapping._mapping(value=value, facade=sys.modules[__name__])


def _num(value: Any) -> float | None:
    return _a40_num._num(value=value, facade=sys.modules[__name__])


def _epoch(value: Any) -> int:
    return _a39_epoch._epoch(value=value, facade=sys.modules[__name__])


def _iso(epoch: int) -> str:
    return _a39_iso._iso(epoch=epoch, facade=sys.modules[__name__])


def _stage_epoch(payload: Mapping[str, Any], *keys: str) -> int:
    return _a39_stage_epoch._stage_epoch(payload, *keys, facade=sys.modules[__name__])


def _read_json(path: Path) -> dict[str, Any]:
    return _a40_read_json._read_json(path=path, facade=sys.modules[__name__])


def _daily_windows_by_id(reports_root: Path, day: str) -> dict[str, dict[str, Any]]:
    return _a39_daily_windows_by_id._daily_windows_by_id(reports_root=reports_root, day=day, facade=sys.modules[__name__])


def _candidate_symbol(candidate: Any) -> str:
    return _a39_candidate_symbol._candidate_symbol(candidate=candidate, facade=sys.modules[__name__])


def _candidate_rank(candidate: Any) -> int | None:
    return _a39_candidate_rank._candidate_rank(candidate=candidate, facade=sys.modules[__name__])


def _row_at_or_before(rows: Sequence[Mapping[str, Any]], epoch: int) -> Mapping[str, Any] | None:
    return _a39_row_at_or_before._row_at_or_before(rows=rows, epoch=epoch, facade=sys.modules[__name__])


def _pre_entry_move_pct(
    *,
    symbol: str,
    decision_epoch: int,
    entry_price: float | None,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
) -> tuple[float | None, dict[str, Any]]:
    return _a39_pre_entry_move_pct._pre_entry_move_pct(symbol=symbol, decision_epoch=decision_epoch, entry_price=entry_price, minute_rows_by_symbol=minute_rows_by_symbol, facade=sys.modules[__name__])


def _entry_forward(
    *,
    trade_id: str,
    symbol: str,
    entry_epoch: int,
    entry_price: float | None,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
) -> dict[str, Any]:
    return _a40_entry_forward._entry_forward(trade_id=trade_id, symbol=symbol, entry_epoch=entry_epoch, entry_price=entry_price, minute_rows_by_symbol=minute_rows_by_symbol, facade=sys.modules[__name__])


def _checkpoint(forward: Mapping[str, Any], horizon: str) -> Mapping[str, Any]:
    return _a40_checkpoint._checkpoint(forward=forward, horizon=horizon, facade=sys.modules[__name__])


def _label(
    *,
    scanner_to_entry_delay_sec: int | None,
    pre_entry_move_pct: float | None,
    forward: Mapping[str, Any],
    strategy_horizon: str = "",
) -> tuple[str, list[str]]:
    return _a40_label._label(scanner_to_entry_delay_sec=scanner_to_entry_delay_sec, pre_entry_move_pct=pre_entry_move_pct, forward=forward, strategy_horizon=strategy_horizon, facade=sys.modules[__name__])


def build_entry_timing_attribution_report(
    *,
    day: str,
    models: Sequence[Mapping[str, Any]],
    reports_root: Path = Path("reports"),
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]] | None = None,
) -> dict[str, Any]:
    rows_by_symbol = (
        minute_rows_by_symbol
        if minute_rows_by_symbol is not None
        else load_minute_rows_from_state()
    )
    windows = _daily_windows_by_id(Path(reports_root), day)
    rows: list[dict[str, Any]] = []
    excluded_count = 0
    for model in models:
        defects = {
            str(value)
            for value in (_mapping(model.get("integrity")).get("defects") or [])
        }
        if "broker_day_partial_exit_duplicate" in defects or "confirmed_runtime_defect" in defects:
            excluded_count += 1
            continue
        trade_id = str(model.get("trade_id") or "")
        symbol = str(model.get("symbol") or "")
        selection = _mapping(model.get("selection"))
        controlled_lane = _mapping(model.get("controlled_mock_lane"))
        entry = _mapping(model.get("entry"))
        outcome = _mapping(model.get("outcome"))
        horizon_contract = _mapping(model.get("horizon_contract"))
        strategy_horizon = str(
            horizon_contract.get("strategy_horizon")
            or horizon_contract.get("source_strategy_horizon")
            or ""
        )
        decision_id = str(selection.get("q9_decision_id") or "")
        window = windows.get(decision_id, {})
        independent_lane = str(controlled_lane.get("selection_authority") or "") == "deterministic_independent_lane"
        lane_signal_epoch = int(_num(controlled_lane.get("signal_epoch")) or 0)
        decision_epoch = (
            lane_signal_epoch
            if independent_lane and lane_signal_epoch > 0
            else int(_num(window.get("decision_epoch")) or _epoch(window.get("generated_at")))
        )
        entry_epoch = _epoch(entry.get("timestamp"))
        entry_price = _num(entry.get("price"))
        scanner_time = 0 if independent_lane else decision_epoch
        strategist_payload = _mapping(window.get("strategist_selection"))
        strategist_time = 0 if independent_lane else _stage_epoch(
            strategist_payload,
            "generated_at",
            "confirmed_at",
            "updated_at",
            "timestamp",
        )
        selected_time = lane_signal_epoch if independent_lane else _stage_epoch(
            selection, "selected_at", "selected_candidate_time", "timestamp"
        )
        scanner_delay = int(entry_epoch - scanner_time) if entry_epoch > 0 and scanner_time > 0 else None
        strategist_delay = int(entry_epoch - strategist_time) if entry_epoch > 0 and strategist_time > 0 else None
        selected_delay = int(entry_epoch - selected_time) if entry_epoch > 0 and selected_time > 0 else None
        decision_delay = int(entry_epoch - decision_epoch) if entry_epoch > 0 and decision_epoch > 0 else None
        pre_move, pre_move_meta = _pre_entry_move_pct(
            symbol=symbol,
            decision_epoch=decision_epoch,
            entry_price=entry_price,
            minute_rows_by_symbol=rows_by_symbol,
        )
        forward = _entry_forward(
            trade_id=trade_id,
            symbol=symbol,
            entry_epoch=entry_epoch,
            entry_price=entry_price,
            minute_rows_by_symbol=rows_by_symbol,
        )
        label, reasons = _label(
            scanner_to_entry_delay_sec=scanner_delay,
            pre_entry_move_pct=pre_move,
            forward=forward,
            strategy_horizon=strategy_horizon,
        )
        cp5 = _checkpoint(forward, "+5m")
        cp15 = _checkpoint(forward, "+15m")
        cp30 = _checkpoint(forward, "+30m")
        cp60 = _checkpoint(forward, "+60m")
        missing_stage_timestamps = [] if independent_lane else [
            name
            for name, value in (
                ("strategist_confirm_time", strategist_time),
                ("selected_candidate_time", selected_time),
            )
            if value <= 0
        ]
        rows.append({
            "trade_id": trade_id,
            "symbol": symbol,
            "label": label,
            "label_reasons": reasons,
            "scanner_top1_symbol": _candidate_symbol(selection.get("raw_scanner_top1")),
            "post_strategy_top1_symbol": _candidate_symbol(selection.get("scanner_top1")),
            "selected_symbol": str(selection.get("selected_symbol") or ""),
            "selected_rank": (
                None
                if independent_lane
                else selection.get("selected_rank") or _candidate_rank(selection.get("selected_candidate"))
            ),
            "selection_authority": (
                "deterministic_independent_lane" if independent_lane else "main_scanner_pipeline"
            ),
            "controlled_lane_id": str(controlled_lane.get("lane_id") or ""),
            "decision_anchor_time": _iso(decision_epoch),
            "strategy_horizon": strategy_horizon or "unknown",
            "stage_timing_status": "COMPLETE" if not missing_stage_timestamps else "PARTIAL",
            "missing_stage_timestamps": missing_stage_timestamps,
            "scanner_top1_time": _iso(scanner_time),
            "post_strategy_top1_time": _iso(strategist_time),
            "strategist_confirm_time": _iso(strategist_time),
            "selected_candidate_time": _iso(selected_time),
            "actual_entry_time": _iso(entry_epoch),
            "scanner_to_entry_delay_sec": scanner_delay,
            "strategist_to_entry_delay_sec": strategist_delay,
            "selected_to_entry_delay_sec": selected_delay,
            "decision_window_to_entry_delay_sec": decision_delay,
            "pre_entry_move_pct": pre_move,
            "pre_entry_move_meta": pre_move_meta,
            "entry_return_pct": outcome.get("net_return_pct"),
            "entry_forward_quality": {
                "+5m_return_pct": cp5.get("return_pct"),
                "+15m_return_pct": cp15.get("return_pct"),
                "+30m_return_pct": cp30.get("return_pct"),
                "+60m_return_pct": cp60.get("return_pct"),
                "+5m_mfe_pct": cp5.get("mfe_pct"),
                "+15m_mfe_pct": cp15.get("mfe_pct"),
                "+30m_mfe_pct": cp30.get("mfe_pct"),
                "+60m_mfe_pct": cp60.get("mfe_pct"),
                "+5m_mae_pct": cp5.get("mae_pct"),
                "+15m_mae_pct": cp15.get("mae_pct"),
                "+30m_mae_pct": cp30.get("mae_pct"),
                "+60m_mae_pct": cp60.get("mae_pct"),
                "immediate_adverse_move": bool((_num(cp5.get("mae_pct")) or 0.0) <= -0.55),
                "immediate_favorable_move": bool((_num(cp5.get("mfe_pct")) or 0.0) >= 0.50),
                "forward_available": bool(forward.get("available")),
            },
        })

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get("label") or "INSUFFICIENT_EVIDENCE")].append(row)
    label_rows: list[dict[str, Any]] = []
    for label in LABELS:
        label_group = groups.get(label, [])
        realized = [_num(row.get("entry_return_pct")) for row in label_group]
        realized_values = [float(value) for value in realized if value is not None]
        mfe_values = [
            _num(_mapping(row.get("entry_forward_quality")).get("+5m_mfe_pct"))
            for row in label_group
        ]
        mae_values = [
            _num(_mapping(row.get("entry_forward_quality")).get("+5m_mae_pct"))
            for row in label_group
        ]
        delays = [_num(row.get("scanner_to_entry_delay_sec")) for row in label_group]
        label_rows.append({
            "label": label,
            "trade_count": len(label_group),
            "performance": performance_metrics(realized_values),
            "avg_scanner_to_entry_delay_sec": (
                round(sum(float(v) for v in delays if v is not None) / len([v for v in delays if v is not None]), 2)
                if any(v is not None for v in delays)
                else None
            ),
            "avg_5m_mfe_pct": (
                round(sum(float(v) for v in mfe_values if v is not None) / len([v for v in mfe_values if v is not None]), 4)
                if any(v is not None for v in mfe_values)
                else None
            ),
            "avg_5m_mae_pct": (
                round(sum(float(v) for v in mae_values if v is not None) / len([v for v in mae_values if v is not None]), 4)
                if any(v is not None for v in mae_values)
                else None
            ),
        })

    return {
        "schema_version": "entry_timing_attribution_report.v1",
        "measurement_contract_version": "q13_stage_timing.v2",
        "evaluation_program_id": "Q13_ENTRY_TIMING_ATTRIBUTION",
        "behavior_effect": "observation_only",
        "day": day,
        "trade_count": len(rows),
        "excluded_trade_count": excluded_count,
        "label_summary": label_rows,
        "rows": rows,
        "limitations": [
            "Scanner time uses the Q9 decision snapshot. Strategist and selected-candidate times remain empty unless an explicit stage timestamp exists.",
            "Labels are attribution hypotheses, not trading behavior.",
            "INSUFFICIENT_EVIDENCE is used when forward minute observations are missing or ambiguous.",
        ],
    }


def _fmt(value: Any, suffix: str = "") -> str:
    return _a40_fmt._fmt(value=value, suffix=suffix, facade=sys.modules[__name__])


def render_entry_timing_attribution_report(payload: Mapping[str, Any]) -> str:
    return _a40_render_entry_timing_attribution_report.render_entry_timing_attribution_report(payload=payload, facade=sys.modules[__name__])


__all__ = [
    "build_entry_timing_attribution_report",
    "render_entry_timing_attribution_report",
]
