from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path
from typing import Any, Iterable
import sys
from . import artifact_inventory_synthetic_identity as _a35_synthetic_identity
from . import artifact_inventory_regular_session_window as _a35_regular_session_window
from . import artifact_inventory_parse_window_kst as _a35_parse_window_kst
from . import artifact_inventory_record as _a36_record
from . import artifact_inventory__iter_shadow_payloads as _a37_iter_shadow_payloads
from . import artifact_inventory_load_q9_pre_strategist_rows as _a37_load_q9_pre_strategist_rows
from . import artifact_inventory__load_forward_recovery_candles as _a37_load_forward_recovery_candles
from . import artifact_inventory_inventory_trade as _a37_inventory_trade
from . import artifact_inventory_build_artifact_inventory as _a37_build_artifact_inventory
from . import artifact_inventory__q9_daily_diagnostics as _a37_q9_daily_diagnostics
from . import artifact_inventory_iter_trade_dirs as _a37_iter_trade_dirs

from libs.reporting.json_array_stream import iter_json_array
from libs.reporting.quant_shadow_forward_outcomes import attach_forward_outcomes


Q9_DECISION_SCHEMA = "q9_decision_windows.v1"
_KRX_SYMBOL_RE = re.compile(r"^\d{6}$")


def _synthetic_identity(row: dict[str, Any]) -> bool:
    return _a35_synthetic_identity._synthetic_identity(row=row, facade=sys.modules[__name__])


def _regular_session_window(row: dict[str, Any]) -> bool:
    return _a35_regular_session_window._regular_session_window(row=row, facade=sys.modules[__name__])


def is_synthetic_evaluation_row(row: dict[str, Any]) -> bool:
    return _synthetic_identity(row)


def is_regular_session_evaluation_row(row: dict[str, Any]) -> bool:
    return _regular_session_window(row)


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def iter_trade_dirs(reports_root: Path, day: str) -> list[Path]:
    return _a37_iter_trade_dirs.iter_trade_dirs(reports_root=reports_root, day=day, facade=sys.modules[__name__])


def _record(path: Path, *, required: bool) -> dict[str, Any]:
    return _a36_record._record(path=path, required=required, facade=sys.modules[__name__])


def _iter_shadow_payloads(reports_root: Path, day: str):
    """Yield each non-empty shadow payload of `day` one at a time, in file-name order.

    Streaming (rather than collecting a list) keeps only one parsed payload alive at a
    time; a trading day's full list was ~300 MiB of parsed objects and, loaded twice
    here, was a large part of the closeout peak that OOM-killed the 1 GiB container.
    """
    yield from _a37_iter_shadow_payloads._iter_shadow_payloads(reports_root=reports_root, day=day, facade=sys.modules[__name__])


def load_q9_pre_strategist_rows(reports_root: Path, day: str) -> list[dict[str, Any]]:
    return _a37_load_q9_pre_strategist_rows.load_q9_pre_strategist_rows(reports_root=reports_root, day=day, facade=sys.modules[__name__])


def _load_forward_recovery_candles(
    reports_root: Path, day: str
) -> dict[str, list[dict[str, Any]]]:
    return _a37_load_forward_recovery_candles._load_forward_recovery_candles(reports_root=reports_root, day=day, facade=sys.modules[__name__])


def _q9_daily_diagnostics(reports_root: Path, day: str, record: dict[str, Any]) -> dict[str, Any]:
    return _a37_q9_daily_diagnostics._q9_daily_diagnostics(reports_root=reports_root, day=day, record=record, facade=sys.modules[__name__])


def _parse_window_kst(value: Any):
    return _a35_parse_window_kst._parse_window_kst(value=value, facade=sys.modules[__name__])


def inventory_trade(trade_dir: Path) -> dict[str, Any]:
    return _a37_inventory_trade.inventory_trade(trade_dir=trade_dir, facade=sys.modules[__name__])


def build_artifact_inventory(reports_root: Path, day: str) -> dict[str, Any]:
    return _a37_build_artifact_inventory.build_artifact_inventory(reports_root=reports_root, day=day, facade=sys.modules[__name__])
