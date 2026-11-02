from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping
import sys

from libs.reporting.json_array_stream import iter_json_array
from libs.reporting.evaluation.artifact_inventory import (
    is_regular_session_evaluation_row,
    is_synthetic_evaluation_row,
)
from . import no_trade_attribution_mapping as _a49_no__mapping
from . import no_trade_attribution_num as _a49_no__num
from . import no_trade_attribution_pct as _a49_no__pct
from . import no_trade_attribution_top as _a49_no__top
from . import no_trade_attribution_q9_window_view as _a49_no__q9_window_view
from . import no_trade_attribution_render as _a54_nt_render
from . import no_trade_attribution_baseline_samsung as _a54_nt_baseline_samsung
from . import no_trade_attribution_q12_btc_woori as _a54_nt_q12_btc_woori
from . import no_trade_attribution_q9_windows as _a54_nt_q9_windows
from . import no_trade_attribution_q11_opening as _a54_nt_q11_opening
from . import no_trade_attribution_build_no_trade_attribution_report as _a55_nt_build
from . import no_trade_attribution_read_json as _a55_nt_read_json


def _read_json(path: Path) -> dict[str, Any]:
    return _a55_nt_read_json._read_json(path, facade=sys.modules[__name__])


def _mapping(value: Any) -> Mapping[str, Any]:
    return _a49_no__mapping._mapping(value, facade=sys.modules[__name__])


def _num(value: Any) -> float | None:
    return _a49_no__num._num(value, facade=sys.modules[__name__])


def _pct(value: Any) -> str:
    return _a49_no__pct._pct(value, facade=sys.modules[__name__])


def _top(counter: Counter[str], limit: int = 10) -> list[dict[str, Any]]:
    return _a49_no__top._top(counter, limit, facade=sys.modules[__name__])


def _q9_window_view(row: Mapping[str, Any]) -> dict[str, Any]:
    """The only parts of a q9 window `build_no_trade_attribution_report` reads (non-mappings read as {})."""
    return _a49_no__q9_window_view._q9_window_view(row, facade=sys.modules[__name__])


def _q9_windows(reports_root: Path, day: str) -> list[dict[str, Any]]:
    return _a54_nt_q9_windows._q9_windows(reports_root, day, facade=sys.modules[__name__])


def _baseline_samsung(reports_root: Path, day: str) -> dict[str, Any]:
    return _a54_nt_baseline_samsung._baseline_samsung(reports_root, day, facade=sys.modules[__name__])


def _q11_opening(reports_root: Path, day: str) -> dict[str, Any]:
    return _a54_nt_q11_opening._q11_opening(reports_root, day, facade=sys.modules[__name__])


def _q12_btc_woori(reports_root: Path, day: str) -> dict[str, Any]:
    return _a54_nt_q12_btc_woori._q12_btc_woori(reports_root, day, facade=sys.modules[__name__])


def build_no_trade_attribution_report(
    *,
    day: str,
    reports_root: Path,
    trade_count: int,
) -> dict[str, Any]:
    return _a55_nt_build.build_no_trade_attribution_report(day=day, reports_root=reports_root, trade_count=trade_count, facade=sys.modules[__name__])


def render_no_trade_attribution_report(payload: Mapping[str, Any]) -> str:
    return _a54_nt_render.render_no_trade_attribution_report(payload, facade=sys.modules[__name__])
