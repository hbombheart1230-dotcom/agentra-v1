from __future__ import annotations
import sys

from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, Sequence

from libs.core.symbols import normalize_symbol


_DECISION_OUTCOMES = {"BUY", "SELL", "WAIT", "NOOP"}


def _to_float(value: Any) -> float:
    from . import decision_observability_to_float as owner
    return owner._to_float(value, facade=sys.modules[__name__])


def _to_int(value: Any) -> int:
    from . import decision_observability_to_int as owner
    return owner._to_int(value, facade=sys.modules[__name__])


def _clip(value: Any, *, max_len: int = 200) -> str:
    from . import decision_observability_clip as owner
    return owner._clip(value, max_len=max_len, facade=sys.modules[__name__])


def _dedupe_non_empty(values: Iterable[Any], *, limit: int | None = None) -> List[str]:
    from . import decision_observability_dedupe_non_empty as owner
    return owner._dedupe_non_empty(values, limit=limit, facade=sys.modules[__name__])


def _humanize_reason_code(value: Any) -> str:
    from . import decision_observability_humanize_reason_code as owner
    return owner._humanize_reason_code(value, facade=sys.modules[__name__])


def _reclaim_evidence_explanation(
    *,
    reclaim_blocked: bool,
    reclaim_gate_ok: bool | None,
    vwap_hold_ok: bool | None,
    vwap_reclaim_ok: bool | None,
    reclaim_distance_to_ready: Any,
    reclaim_readiness_tuned: bool,
) -> str:
    from .decision_observability_reclaim_evidence_explanation import _reclaim_evidence_explanation as owner
    return owner(reclaim_blocked=reclaim_blocked, reclaim_gate_ok=reclaim_gate_ok, vwap_hold_ok=vwap_hold_ok, vwap_reclaim_ok=vwap_reclaim_ok, reclaim_distance_to_ready=reclaim_distance_to_ready, reclaim_readiness_tuned=reclaim_readiness_tuned, facade=sys.modules[__name__])


def _extract_failed_names(rows: Any, *, statuses: Sequence[str]) -> List[str]:
    from . import decision_observability_extract_failed_names as owner
    return owner._extract_failed_names(rows, statuses=statuses, facade=sys.modules[__name__])


def _blocker_family(
    *,
    code: str,
    primary_failure_axis: str,
    guard_blocked: bool,
) -> str:
    from .decision_observability_blocker_family import _blocker_family as owner
    return owner(code=code, primary_failure_axis=primary_failure_axis, guard_blocked=guard_blocked, facade=sys.modules[__name__])


def _normalize_decision_outcome(value: Any, *, fallback: str = "WAIT") -> str:
    from . import decision_observability_normalize_decision_outcome as owner
    return owner._normalize_decision_outcome(value, fallback=fallback, facade=sys.modules[__name__])


def build_monitor_no_trade_surface(
    entry_info: Mapping[str, Any] | None,
    *,
    final_decision: Any,
    buy_submitted: bool,
    guard_blocked: bool = False,
    guard_reason: Any = None,
    commander_no_trade_reason_code: Any = None,
) -> Dict[str, Any]:
        from .decision_observability_build_monitor_no_trade_surface import build_monitor_no_trade_surface as owner
        return owner(entry_info, final_decision=final_decision, buy_submitted=buy_submitted, guard_blocked=guard_blocked, guard_reason=guard_reason, commander_no_trade_reason_code=commander_no_trade_reason_code, facade=sys.modules[__name__])


def _resolve_check_state(
    *,
    name: str,
    metrics: Mapping[str, Any],
    passed_checks: Sequence[Any],
    failed_checks: Sequence[Any],
    check_status: Mapping[str, Any],
) -> Any:
        from .decision_observability_resolve_check_state import _resolve_check_state as owner
        return owner(name=name, metrics=metrics, passed_checks=passed_checks, failed_checks=failed_checks, check_status=check_status, facade=sys.modules[__name__])


def _resolve_structure_state(chart_features: Mapping[str, Any], check_status: Mapping[str, Any]) -> str:
        from .decision_observability_resolve_structure_state import _resolve_structure_state as owner
        return owner(chart_features, check_status, facade=sys.modules[__name__])


def build_entry_blocker_surface(
    entry_info: Mapping[str, Any] | None,
    *,
    final_decision: Any,
    no_trade_surface: Mapping[str, Any] | None = None,
    entry_blockers: Sequence[Any] | None = None,
    buy_blocked_open_position: bool = False,
    buy_blocked_closeout_window: bool = False,
    buy_blocked_post_exit_cooldown: bool = False,
    post_exit_cooldown_remaining_sec: Any = None,
    open_position_count: Any = None,
    minutes_to_close: Any = None,
    eod_flat_cutoff_min: Any = None,
) -> Dict[str, Any]:
        from .decision_observability_build_entry_blocker_surface import build_entry_blocker_surface as owner
        return owner(entry_info, final_decision=final_decision, no_trade_surface=no_trade_surface, entry_blockers=entry_blockers, buy_blocked_open_position=buy_blocked_open_position, buy_blocked_closeout_window=buy_blocked_closeout_window, buy_blocked_post_exit_cooldown=buy_blocked_post_exit_cooldown, post_exit_cooldown_remaining_sec=post_exit_cooldown_remaining_sec, open_position_count=open_position_count, minutes_to_close=minutes_to_close, eod_flat_cutoff_min=eod_flat_cutoff_min, facade=sys.modules[__name__])


def build_scanner_monitor_handoff_surface(
    *,
    selected: Mapping[str, Any] | None,
    ranked_candidates: Sequence[Mapping[str, Any]] | None,
    scanner_output: Mapping[str, Any] | None,
    final_decision: Any,
    no_trade_surface: Mapping[str, Any] | None,
    entry_info: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
        from .decision_observability_build_scanner_monitor_handoff_surface import build_scanner_monitor_handoff_surface as owner
        return owner(selected=selected, ranked_candidates=ranked_candidates, scanner_output=scanner_output, final_decision=final_decision, no_trade_surface=no_trade_surface, entry_info=entry_info, facade=sys.modules[__name__])


def _extract_error_type(value: Any) -> str:
    from . import decision_observability_extract_error_type as owner
    return owner._extract_error_type(value, facade=sys.modules[__name__])


def build_strategist_policy_resolution_surface(
    *,
    strategist_output: Mapping[str, Any] | None,
    strategist_llm: Mapping[str, Any] | None,
    commander_context: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
        from .decision_observability_build_strategist_policy_resolution_surface import build_strategist_policy_resolution_surface as owner
        return owner(strategist_output=strategist_output, strategist_llm=strategist_llm, commander_context=commander_context, facade=sys.modules[__name__])


def build_commander_route_observability_surface(
    *,
    selected_route: str,
    route_reason: str,
    commander_decision: Mapping[str, Any] | None,
    runtime_fast_path: Mapping[str, Any] | None,
    resilience: Mapping[str, Any] | None,
    runtime_status: Any,
    runtime_transition: Any,
) -> Dict[str, Any]:
        from .decision_observability_build_commander_route_observability_surface import build_commander_route_observability_surface as owner
        return owner(selected_route=selected_route, route_reason=route_reason, commander_decision=commander_decision, runtime_fast_path=runtime_fast_path, resilience=resilience, runtime_status=runtime_status, runtime_transition=runtime_transition, facade=sys.modules[__name__])
