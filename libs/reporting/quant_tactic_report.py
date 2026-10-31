from __future__ import annotations

import sys
from typing import Any, Dict, List, Mapping

from libs.runtime.quant.decision import build_entry_quant_decision
from libs.runtime.quant.suitability import score_candidate_tactic_suitability
from libs.reporting import quant_tactic_items_projection as _items_owner
from libs.reporting import quant_tactic_fmt_projection as _fmt_owner
from libs.reporting import quant_tactic_mapping_projection as _mapping_owner
from libs.reporting import quant_tactic_pct_projection as _pct_owner
from libs.reporting import quant_tactic_decision_label_projection as _decision_label_owner
from libs.reporting import quant_tactic_reason_text_projection as _reason_text_owner
from libs.reporting import quant_tactic_monitor_projection as _monitor_owner
from libs.reporting import quant_tactic_nested_dicts_projection as _nested_dicts_owner
from libs.reporting import quant_tactic_first_nested_mapping_projection as _first_nested_owner
from libs.reporting import quant_tactic_symbol_projection as _symbol_owner
from libs.reporting import quant_tactic_playbook_projection as _playbook_owner
from libs.reporting import quant_tactic_entry_visibility_projection as _entry_vis_owner
from libs.reporting import quant_tactic_entry_info_projection as _entry_info_owner
from libs.reporting import quant_tactic_candidate_symbol_projection as _cand_symbol_owner
from libs.reporting import quant_tactic_scanner_chart_fit_projection as _chart_fit_owner
from libs.reporting import quant_tactic_value_projection as _tactic_value_owner
from libs.reporting import quant_tactic_mismatches_projection as _mismatches_owner
from libs.reporting import quant_tactic_exit_drifts_projection as _exit_drifts_owner
from libs.reporting import quant_tactic_selected_candidate_projection as _o6a4_owner
from libs.reporting import quant_tactic_sources_projection as _o6a5_owner
from libs.reporting import quant_tactic_report_lines_projection as _o6a6_owner
from libs.reporting import quant_tactic_surface_projection as _o6a7_owner


def _mapping(value: Any) -> Dict[str, Any]:
    return _mapping_owner._mapping(value, facade=sys.modules[__name__])


def _items(value: Any) -> List[str]:
    return _items_owner._items(value)


def _fmt(value: Any) -> str:
    return _fmt_owner._fmt(value)


def _pct(value: Any) -> str:
    return _pct_owner._pct(value)


def _decision_label(value: Any) -> str:
    return _decision_label_owner._decision_label(value)


def _reason_text(values: Any) -> str:
    return _reason_text_owner._reason_text(values, facade=sys.modules[__name__])


def _monitor(report: Mapping[str, Any]) -> Dict[str, Any]:
    return _monitor_owner._monitor(report, facade=sys.modules[__name__])


def _nested_dicts(value: Any, *, max_depth: int = 9) -> List[Dict[str, Any]]:
    return _nested_dicts_owner._nested_dicts(value, max_depth=max_depth, facade=sys.modules[__name__])


def _first_nested_mapping(root: Mapping[str, Any], key: str) -> Dict[str, Any]:
    return _first_nested_owner._first_nested_mapping(root, key, facade=sys.modules[__name__])


def _symbol(report: Mapping[str, Any]) -> str:
    return _symbol_owner._symbol(report, facade=sys.modules[__name__])


def _playbook(report: Mapping[str, Any], *, fallback: str = "") -> str:
    return _playbook_owner._playbook(report, fallback=fallback, facade=sys.modules[__name__])


def _entry_visibility(report: Mapping[str, Any]) -> Dict[str, Any]:
    return _entry_vis_owner._entry_visibility(report, facade=sys.modules[__name__])


def _entry_info_from_visibility(visibility: Mapping[str, Any], monitor: Mapping[str, Any]) -> Dict[str, Any]:
    return _entry_info_owner._entry_info_from_visibility(visibility, monitor, facade=sys.modules[__name__])


def _candidate_symbol(row: Mapping[str, Any]) -> str:
    return _cand_symbol_owner._candidate_symbol(row)


def _selected_candidate_row(report: Mapping[str, Any], symbol: str) -> Dict[str, Any]:
    return _o6a4_owner._selected_candidate_row(report, symbol, facade=sys.modules[__name__])


def _scanner_chart_fit_from_row(row: Mapping[str, Any]) -> Dict[str, Any]:
    return _chart_fit_owner._scanner_chart_fit_from_row(row, facade=sys.modules[__name__])


def _tactic_value(value: Any) -> str:
    return _tactic_value_owner._tactic_value(value)


def _tactic_sources(
    *,
    entry_decision: Mapping[str, Any],
    factor_snapshot: Mapping[str, Any],
    selected_row: Mapping[str, Any],
    tactic_suitability: Mapping[str, Any],
    exit_decision: Mapping[str, Any],
) -> List[tuple[str, str]]:
    return _o6a5_owner._tactic_sources(entry_decision=entry_decision, factor_snapshot=factor_snapshot, selected_row=selected_row, tactic_suitability=tactic_suitability, exit_decision=exit_decision, facade=sys.modules[__name__])


def _tactic_mismatches(sources: List[tuple[str, str]], tactic_id: str) -> List[Dict[str, str]]:
    return _mismatches_owner._tactic_mismatches(sources, tactic_id)


def _exit_tactic_drifts(sources: List[tuple[str, str]], tactic_id: str) -> List[Dict[str, str]]:
    return _exit_drifts_owner._exit_tactic_drifts(sources, tactic_id)


def quant_tactic_surface(report: Mapping[str, Any] | None) -> Dict[str, Any]:
    return _o6a7_owner.quant_tactic_surface(report, facade=sys.modules[__name__])


def render_quant_tactic_report_lines(report: Mapping[str, Any] | None, *, compact: bool = False) -> List[str]:
    return _o6a6_owner.render_quant_tactic_report_lines(report, compact=compact, facade=sys.modules[__name__])
