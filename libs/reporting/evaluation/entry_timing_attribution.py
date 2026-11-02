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
from . import entry_timing_attribution_build_entry_timing_attribution_report as _a41_build_entry_timing_attribution_report

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
    return _a41_build_entry_timing_attribution_report.build_entry_timing_attribution_report(day=day, models=models, reports_root=reports_root, minute_rows_by_symbol=minute_rows_by_symbol, facade=sys.modules[__name__])


def _fmt(value: Any, suffix: str = "") -> str:
    return _a40_fmt._fmt(value=value, suffix=suffix, facade=sys.modules[__name__])


def render_entry_timing_attribution_report(payload: Mapping[str, Any]) -> str:
    return _a40_render_entry_timing_attribution_report.render_entry_timing_attribution_report(payload=payload, facade=sys.modules[__name__])


__all__ = [
    "build_entry_timing_attribution_report",
    "render_entry_timing_attribution_report",
]
