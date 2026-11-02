from __future__ import annotations

import sys

import sys

import sys

import statistics
from datetime import datetime, timedelta, timezone
from dataclasses import replace
from typing import Any, Dict, List, Mapping, Sequence

from libs.runtime.chart_structure_features import (
    build_chart_structure_features,
    empty_chart_structure_features,
)
from libs.runtime.etf_deviation import (
    is_etf_asset_class,
    normalize_deviation_pct,
    score_etf_deviation_for_entry,
)
from libs.runtime.monitor_policy import (
    MonitorEntryPolicy,
    extract_monitor_entry_policy_mapping,
    normalize_monitor_entry_policy_schema,
    normalize_policy_check_spec,
)
from libs.runtime.volume_confirmation import evaluate_intraday_volume_confirmation
import sys as _r3_sys
from libs.runtime.monitor.signal_features import (
    signal_feature_candles_out,
    breakout_level_features,
    signal_feature_asset_class_detected_breakout_distance_t,
    signal_feature_etf_deviation_chart_ok_etf_deviation_dis,
    signal_feature_effect_free_block_2745,
)
from libs.runtime.monitor.signal_features_breakout_volume_gate import (
    signal_feature_breakout_volume_gate_ok_breakout_volume,
    volume_pullback_breakout_gate_features,
)
from libs.runtime.monitor.signal_score_projection import (
    signal_score_entry_condition_path_entry_condition_pat,
    signal_score_entry_condition_path_entry_hard_gate_blo,
    signal_score_chart_structure_features_legacy_decision,
)
from libs.runtime.monitor.signal_score_projection_chart_structure_decision import (
    signal_score_chart_structure_decision_hint_policy_ali,
)
from libs.runtime.monitor.signal_explanation import (
    signal_explain_effect_free_block_3479,
)


_RECLAIM_TUNING_VERSION = "small_relaxation_v1"
_RECLAIM_TUNING_SCOPE = "below_vwap_reclaim_not_ready_only"
_RECLAIM_NEAR_READY_DISTANCE_MIN_BASE = -0.0015
_RECLAIM_NEAR_READY_DISTANCE_MIN_TUNED = -0.0018
_KST = timezone(timedelta(hours=9))
_MARKET_OPEN_MINUTE = 9 * 60
_OPENING_GAP_CHASE_WINDOW_MINUTES = 10.0
_OPENING_GAP_CHASE_MIN_PCT = 0.01
_BREAKOUT_CHASE_VOLUME_GATE_MIN_EXTENDED_PCT = 0.02
_LOWER_VWAP_REBOUND_MIN_DISTANCE_PCT = -0.008
_LOWER_VWAP_REBOUND_MAX_DISTANCE_PCT = -0.0015
_LOWER_VWAP_REBOUND_MIN_CONFIDENCE = 0.50


import sys as _monitor_view_sys
import libs.agents.monitor.projections.signal_evidence_defaults as _monitor_views

def _to_float(value: Any, default: float = 0.0) -> float:
    from . import intraday_monitor_signals_to_float as _owner
    return _owner._to_float(value, default, facade=sys.modules[__name__])


def _to_int(value: Any, default: int = 0) -> int:
    from . import intraday_monitor_signals_to_int as _owner
    return _owner._to_int(value, default, facade=sys.modules[__name__])


def _to_bool(value: Any, default: bool = False) -> bool:
    from . import intraday_monitor_signals_to_bool as _owner
    return _owner._to_bool(value, default, facade=sys.modules[__name__])


def _clamp_score(value: float) -> float:
    from . import intraday_monitor_signals_clamp_score as _owner
    return _owner._clamp_score(value, facade=sys.modules[__name__])


def _min_threshold_score(actual: float, threshold: float) -> float:
    from . import intraday_monitor_signals_min_threshold_score as _owner
    return _owner._min_threshold_score(actual, threshold, facade=sys.modules[__name__])


def _range_threshold_score(actual: float, minimum: float, maximum: float) -> float:
    from . import intraday_monitor_signals_range_threshold_score as _owner
    return _owner._range_threshold_score(actual, minimum, maximum, facade=sys.modules[__name__])


def _entry_quality_tier(score: float) -> str:
    from . import intraday_monitor_signals_entry_quality_tier as _owner
    return _owner._entry_quality_tier(score, facade=sys.modules[__name__])


def _empty_entry_transition_trace() -> Dict[str, Any]:
    return _monitor_views._empty_entry_transition_trace(facade=_monitor_view_sys.modules[__name__])


def _env_trueish(value: Any, default: bool = False) -> bool:
    from . import intraday_monitor_signals_env_trueish as _owner
    return _owner._env_trueish(value, default, facade=sys.modules[__name__])


def _resolve_monitor_scoring_settings(scoring: Mapping[str, Any] | None = None) -> Dict[str, Any]:
    from . import intraday_monitor_signals_resolve_monitor_scoring_settings as _owner
    return _owner._resolve_monitor_scoring_settings(scoring, facade=sys.modules[__name__])


def _build_monitor_score_breakdown(
    *,
    vwap_reclaim_ok: bool,
    breakout_ok: bool,
    pullback_mature: bool,
    volume_ok: bool,
    confidence_gate_ok: bool,
    chart_structure_features: Mapping[str, Any] | None = None,
) -> Dict[str, float]:
    from . import intraday_monitor_signals_build_monitor_score_breakdown as _owner
    return _owner._build_monitor_score_breakdown(vwap_reclaim_ok=vwap_reclaim_ok, breakout_ok=breakout_ok, pullback_mature=pullback_mature, volume_ok=volume_ok, confidence_gate_ok=confidence_gate_ok, chart_structure_features=chart_structure_features, facade=sys.modules[__name__])


def _build_monitor_signal_evidence(
    *,
    reclaim_score: float,
    volume_score: float,
    pullback_score: float,
    breakout_score: float,
    confidence_score: float,
    confidence_threshold: float,
    entry_quality_score: float,
    breakout_quality_score: float,
    pullback_quality_score: float,
    entry_quality_path: str,
    reclaim_ok: bool,
    volume_ok: bool,
    pullback_ok: bool,
    breakout_ok: bool,
    rebound_ok: bool,
    reclaim_gate_ok: bool,
    breakout_path_ok: bool,
    pullback_volume_path_ok: bool,
    extension_ok: bool,
    too_extended: bool,
    reclaim_strength: float,
    rebound_strength: float,
    transition_readiness_score: float,
    reclaim_distance_to_ready: float | None,
    volume_distance_to_ready: float | None,
    breakout_distance_to_ready: float | None,
    score_breakdown: Mapping[str, Any] | None = None,
    score_threshold: float = 3.0,
) -> Dict[str, Any]:
    from . import intraday_monitor_signals_build_monitor_signal_evidence as _owner
    return _owner._build_monitor_signal_evidence(reclaim_score=reclaim_score, volume_score=volume_score, pullback_score=pullback_score, breakout_score=breakout_score, confidence_score=confidence_score, confidence_threshold=confidence_threshold, entry_quality_score=entry_quality_score, breakout_quality_score=breakout_quality_score, pullback_quality_score=pullback_quality_score, entry_quality_path=entry_quality_path, reclaim_ok=reclaim_ok, volume_ok=volume_ok, pullback_ok=pullback_ok, breakout_ok=breakout_ok, rebound_ok=rebound_ok, reclaim_gate_ok=reclaim_gate_ok, breakout_path_ok=breakout_path_ok, pullback_volume_path_ok=pullback_volume_path_ok, extension_ok=extension_ok, too_extended=too_extended, reclaim_strength=reclaim_strength, rebound_strength=rebound_strength, transition_readiness_score=transition_readiness_score, reclaim_distance_to_ready=reclaim_distance_to_ready, volume_distance_to_ready=volume_distance_to_ready, breakout_distance_to_ready=breakout_distance_to_ready, score_breakdown=score_breakdown, score_threshold=score_threshold, facade=sys.modules[__name__])


def _empty_monitor_signal_evidence(*, score_threshold: float=3.0) -> Dict[str, Any]:
    return _monitor_views._empty_monitor_signal_evidence(score_threshold=score_threshold, facade=_monitor_view_sys.modules[__name__])


def _dedupe_non_empty(values: Sequence[Any]) -> List[str]:
    from . import intraday_monitor_signals_dedupe_non_empty as _owner
    return _owner._dedupe_non_empty(values, facade=sys.modules[__name__])


def _volume_priority_hint(volume_ratio_min: float) -> str:
    from . import intraday_monitor_signals_volume_priority_hint as _owner
    return _owner._volume_priority_hint(volume_ratio_min, facade=sys.modules[__name__])


def _empty_monitor_policy_interpretation() -> Dict[str, Any]:
    return _monitor_views._empty_monitor_policy_interpretation(facade=_monitor_view_sys.modules[__name__])


def _empty_monitor_policy_interpreter_trace() -> Dict[str, Any]:
    return _monitor_views._empty_monitor_policy_interpreter_trace(facade=_monitor_view_sys.modules[__name__])


def _empty_monitor_policy_alignment_summary() -> Dict[str, Any]:
    return _monitor_views._empty_monitor_policy_alignment_summary(facade=_monitor_view_sys.modules[__name__])


def _empty_monitor_policy_aware_gating() -> Dict[str, Any]:
    return _monitor_views._empty_monitor_policy_aware_gating(facade=_monitor_view_sys.modules[__name__])


def _empty_chart_structure_decision_hint() -> Dict[str, Any]:
    return _monitor_views._empty_chart_structure_decision_hint(facade=_monitor_view_sys.modules[__name__])


def _empty_human_chart_buy_guard() -> Dict[str, Any]:
    from . import intraday_monitor_signals_empty_human_chart_buy_guard as _owner
    return _owner._empty_human_chart_buy_guard(facade=sys.modules[__name__])


def _empty_human_chart_entry_setup() -> Dict[str, Any]:
    from . import intraday_monitor_signals_empty_human_chart_entry_setup as _owner
    return _owner._empty_human_chart_entry_setup(facade=sys.modules[__name__])


def _empty_human_chart_detail_context() -> Dict[str, Any]:
    return _monitor_views._empty_human_chart_detail_context(facade=_monitor_view_sys.modules[__name__])


def _build_human_chart_detail_context(
    candles: Sequence[Mapping[str, Any]],
    *,
    current_close: float,
    current_vwap: float,
    recent_high: float,
    breakout_level: float,
    volume_ratio: float,
) -> Dict[str, Any]:
        from .intraday_monitor_signals_build_human_chart_detail_context import _build_human_chart_detail_context as owner
        return owner(candles, current_close=current_close, current_vwap=current_vwap, recent_high=recent_high, breakout_level=breakout_level, volume_ratio=volume_ratio, facade=sys.modules[__name__])


def _build_human_chart_buy_guard(
    *,
    chart_human_context: Mapping[str, Any] | None = None,
    chart_detail_context: Mapping[str, Any] | None = None,
    prev_close_distance_pct: Any = None,
    open_gap_pct: Any = None,
    candidate_triggered: bool = False,
    entry_condition_path: str | None = None,
) -> Dict[str, Any]:
    """Final sanity guard for human-like chart context before emitting BUY.

    The chart feature layer is intentionally allowed to be soft inside scoring,
    but a BUY should not pass when the same snapshot already shows a broken
    VWAP structure or elevated exit risk. This guard only blocks; it never
    creates a BUY.
    """

    out = _empty_human_chart_buy_guard()
    context = dict(chart_human_context or {}) if isinstance(chart_human_context, Mapping) else {}
    if not bool(context.get("available")):
        out["notes"] = ["human_chart_context_unavailable"]
        return out
    out["available"] = True
    if not bool(candidate_triggered):
        out["notes"] = ["candidate_decision_not_buy"]
        return out

    min_entry_score = float(out["thresholds"]["min_entry_chart_score"])
    max_exit_risk = float(out["thresholds"]["max_exit_risk_score"])
    min_late_entry_score = float(out["thresholds"]["min_late_entry_chart_score"])
    near_upper_prev_close_distance = float(out["thresholds"]["near_upper_prev_close_distance_pct"])
    no_reward_room_score_threshold = float(out["thresholds"]["no_reward_room_score"])
    no_reward_room_pct_threshold = float(out["thresholds"]["no_reward_room_pct"])
    entry_score = _clamp_score(_to_float(context.get("entry_chart_score")))
    exit_risk_score = _clamp_score(_to_float(context.get("exit_risk_score")))
    vwap_breakdown = str(context.get("vwap_breakdown_persistence") or "").strip().lower()
    vwap_reclaim = str(context.get("vwap_reclaim_persistence") or "").strip().lower()
    late_entry_risk = str(context.get("late_entry_risk") or "").strip().lower()
    swing_low_break = bool(context.get("swing_low_break"))
    lower_high_failure = bool(context.get("lower_high_failure"))
    detail = dict(chart_detail_context or {}) if isinstance(chart_detail_context, Mapping) else {}
    detail_observed = dict(detail.get("observed") or {}) if isinstance(detail.get("observed"), Mapping) else {}
    detail_available = bool(detail.get("available"))
    reward_room_score = _clamp_score(_to_float(detail.get("reward_room_score"))) if detail_available else None
    reward_room_pct = (
        _to_float(detail_observed.get("reward_room_pct"))
        if detail_observed.get("reward_room_pct") not in (None, "")
        else None
    )
    breakout_extension_pct = (
        _to_float(detail_observed.get("breakout_extension_pct"))
        if detail_observed.get("breakout_extension_pct") not in (None, "")
        else None
    )
    prev_close_distance = (
        _to_float(prev_close_distance_pct) if prev_close_distance_pct not in (None, "") else None
    )
    open_gap = _to_float(open_gap_pct) if open_gap_pct not in (None, "") else None
    no_reward_room = bool(
        detail_available
        and (
            (reward_room_score is not None and reward_room_score <= no_reward_room_score_threshold)
            or (reward_room_pct is not None and reward_room_pct <= no_reward_room_pct_threshold)
        )
    )
    near_upper_limit_zone = bool(
        (prev_close_distance is not None and prev_close_distance >= near_upper_prev_close_distance)
        or (open_gap is not None and open_gap >= near_upper_prev_close_distance)
    )

    out["observed"] = {
        "entry_chart_score": entry_score,
        "exit_risk_score": exit_risk_score,
        "vwap_breakdown_persistence": vwap_breakdown,
        "vwap_reclaim_persistence": vwap_reclaim,
        "late_entry_risk": late_entry_risk,
        "swing_low_break": swing_low_break,
        "lower_high_failure": lower_high_failure,
        "reward_room_score": reward_room_score,
        "reward_room_pct": reward_room_pct,
        "breakout_extension_pct": breakout_extension_pct,
        "prev_close_distance_pct": prev_close_distance,
        "open_gap_pct": open_gap,
        "no_reward_room": bool(no_reward_room),
        "near_upper_limit_zone": bool(near_upper_limit_zone),
    }

    blockers: List[str] = []
    if exit_risk_score >= max_exit_risk:
        blockers.append(f"exit_risk_score>={max_exit_risk:.2f}")
    if vwap_breakdown == "strong":
        blockers.append("vwap_breakdown_persistence=strong")
    if entry_score < min_entry_score and (vwap_breakdown == "strong" or vwap_reclaim == "absent"):
        blockers.append(f"entry_chart_score<{min_entry_score:.2f}")
    if swing_low_break:
        blockers.append("swing_low_break=true")
    if lower_high_failure and vwap_reclaim != "strong":
        blockers.append("lower_high_failure_without_strong_vwap_reclaim")
    if late_entry_risk == "high" and entry_score < 0.45:
        blockers.append("late_entry_risk=high_with_weak_entry_score")
    if late_entry_risk == "high" and no_reward_room:
        blockers.append("late_entry_risk=high_with_no_reward_room")
    if late_entry_risk == "high" and entry_score < min_late_entry_score and no_reward_room:
        blockers.append(f"entry_chart_score<{min_late_entry_score:.2f}_with_late_entry_no_reward_room")
    if near_upper_limit_zone and late_entry_risk == "high" and no_reward_room:
        blockers.append("near_upper_limit_zone_with_late_entry_no_reward_room")
    insufficient_reward_room = bool(
        reward_room_pct is not None
        and 0.0 <= reward_room_pct < no_reward_room_pct_threshold
        and (late_entry_risk in {"medium", "high"} or near_upper_limit_zone)
    )
    if insufficient_reward_room:
        blockers.append(f"reward_room_pct<{no_reward_room_pct_threshold:.3f}_cost_floor")

    lower_probe_path = str(entry_condition_path or "").strip() == "lower_vwap_rebound_probe_path"
    if lower_probe_path and blockers:
        soft_lower_probe_blockers = {
            "vwap_breakdown_persistence=strong",
            f"entry_chart_score<{min_entry_score:.2f}",
        }
        remaining_blockers = [item for item in blockers if item not in soft_lower_probe_blockers]
        if len(remaining_blockers) < len(blockers):
            out["notes"] = [
                "lower_vwap_rebound_probe_allows_vwap_breakdown_observation",
            ]
            blockers = remaining_blockers

    if not blockers:
        if not out.get("notes"):
            out["notes"] = ["human_chart_context_not_blocking"]
        out["observed"]["entry_condition_path"] = str(entry_condition_path or "")
        return out

    out["applied"] = True
    out["mode"] = "block"
    out["blocking_features"] = blockers
    out["observed"]["entry_condition_path"] = str(entry_condition_path or "")
    out["notes"] = ["human_chart_sanity_guard_blocked_buy"]
    return out


def _build_human_chart_entry_setup(
    *,
    chart_human_context: Mapping[str, Any] | None = None,
    chart_detail_context: Mapping[str, Any] | None = None,
    signal_evidence: Mapping[str, Any] | None = None,
    policy_alignment_summary: Mapping[str, Any] | None = None,
    candidate_triggered: bool = False,
    legacy_reason: str | None = None,
) -> Dict[str, Any]:
    """Promote only clear human-chart A setups that legacy gates nearly caught.

    This is the positive counterpart to the buy guard. It can turn WAIT into BUY,
    but only when the legacy engine is already near a valid entry and the chart
    context shows a clean reclaim/continuation setup without exit-risk pressure.
    """

    out = _empty_human_chart_entry_setup()
    context = dict(chart_human_context or {}) if isinstance(chart_human_context, Mapping) else {}
    detail = dict(chart_detail_context or {}) if isinstance(chart_detail_context, Mapping) else {}
    evidence = dict(signal_evidence or {}) if isinstance(signal_evidence, Mapping) else {}
    checks = dict(evidence.get("checks") or {}) if isinstance(evidence.get("checks"), Mapping) else {}
    derived = dict(evidence.get("derived") or {}) if isinstance(evidence.get("derived"), Mapping) else {}
    scores = dict(evidence.get("scores") or {}) if isinstance(evidence.get("scores"), Mapping) else {}
    summary = (
        dict(policy_alignment_summary or {})
        if isinstance(policy_alignment_summary, Mapping)
        else {}
    )

    if not bool(context.get("available")):
        out["notes"] = ["human_chart_context_unavailable"]
        return out
    out["available"] = True
    if bool(candidate_triggered):
        out["notes"] = ["candidate_decision_already_buy"]
        return out
    if not bool(summary.get("policy_available")):
        out["notes"] = ["policy_context_unavailable"]
        return out

    min_a_setup_score = float(out["thresholds"]["min_a_setup_score"])
    min_entry_score = float(out["thresholds"]["min_entry_chart_score"])
    min_live_entry_score = float(out["thresholds"]["min_live_promotion_entry_chart_score"])
    min_live_entry_quality = float(out["thresholds"]["min_live_promotion_entry_quality_score"])
    min_live_transition = float(out["thresholds"]["min_live_promotion_transition_readiness_score"])
    max_exit_risk = float(out["thresholds"]["max_exit_risk_score"])
    min_candle_quality_score = float(out["thresholds"]["min_candle_quality_score"])
    min_vwap_reference_quality_score = float(out["thresholds"]["min_vwap_reference_quality_score"])
    min_reward_room_score = float(out["thresholds"]["min_reward_room_score"])
    min_multi_window_structure_score = float(out["thresholds"]["min_multi_window_structure_score"])
    reclaim_near_ready_min = float(out["thresholds"]["reclaim_near_ready_distance_min"])
    breakout_near_ready_min = float(out["thresholds"]["breakout_near_ready_distance_min"])
    volume_near_ready_min = float(out["thresholds"]["volume_near_ready_distance_min"])

    entry_score = _clamp_score(_to_float(context.get("entry_chart_score")))
    exit_risk_score = _clamp_score(_to_float(context.get("exit_risk_score")))
    vwap_reclaim = str(context.get("vwap_reclaim_persistence") or "").strip().lower()
    vwap_breakdown = str(context.get("vwap_breakdown_persistence") or "").strip().lower()
    volume_state = str(context.get("volume_expansion_persistence") or "").strip().lower()
    late_entry_risk = str(context.get("late_entry_risk") or "").strip().lower()
    swing_low_above_vwap = bool(context.get("swing_low_above_vwap"))
    higher_low_continuation = bool(context.get("higher_low_continuation"))
    box_breakout_retest_hold = bool(context.get("box_breakout_retest_hold"))
    swing_low_break = bool(context.get("swing_low_break"))
    lower_high_failure = bool(context.get("lower_high_failure"))
    detail_available = bool(detail.get("available"))
    candle_quality_score = _clamp_score(_to_float(detail.get("candle_quality_score"), 0.5))
    vwap_reference_quality_score = _clamp_score(_to_float(detail.get("vwap_reference_quality_score"), 0.5))
    reward_room_score = _clamp_score(_to_float(detail.get("reward_room_score"), 0.5))
    multi_window_structure_score = _clamp_score(_to_float(detail.get("multi_window_structure_score"), 0.5))
    required_failures = _dedupe_non_empty(summary.get("top_failed_required_checks") or [])
    legacy_reason_text = str(legacy_reason or "").strip()

    reclaim_distance = derived.get("reclaim_distance_to_ready")
    volume_distance = derived.get("volume_distance_to_ready")
    breakout_distance = derived.get("breakout_distance_to_ready")
    entry_quality_score = _clamp_score(_to_float(scores.get("entry_quality_score")))
    transition_readiness_score = _clamp_score(_to_float(derived.get("transition_readiness_score")))
    reclaim_distance_value = _to_float(reclaim_distance, default=-999.0) if reclaim_distance not in (None, "") else None
    volume_distance_value = _to_float(volume_distance, default=-999.0) if volume_distance not in (None, "") else None
    breakout_distance_value = _to_float(breakout_distance, default=-999.0) if breakout_distance not in (None, "") else None

    reclaim_near_ready = bool(
        reclaim_distance_value is not None
        and reclaim_near_ready_min <= reclaim_distance_value < 0.0
    )
    breakout_near_ready = bool(
        breakout_distance_value is not None
        and breakout_near_ready_min <= breakout_distance_value < 0.0
    )
    volume_near_ready = bool(
        volume_distance_value is None
        or volume_distance_value >= volume_near_ready_min
    )
    strong_quality_near_ready = bool(
        entry_quality_score >= min_live_entry_quality
        and transition_readiness_score >= min_live_transition
    )
    vwap_support_ok = bool(
        checks.get("reclaim_gate_ok")
        or vwap_reclaim in {"strong", "partial"}
        or reclaim_near_ready
    )
    volume_support_ok = bool(checks.get("volume_ok") or volume_state in {"strong", "partial"} or volume_near_ready)
    structure_support_ok = bool(
        checks.get("breakout_path_ok")
        or checks.get("pullback_volume_path_ok")
        or breakout_near_ready
        or swing_low_above_vwap
        or higher_low_continuation
        or box_breakout_retest_hold
    )
    near_legacy_path = bool(
        checks.get("breakout_path_ok")
        or checks.get("pullback_volume_path_ok")
        or reclaim_near_ready
        or breakout_near_ready
    )
    extension_ok = bool(checks.get("extension_ok"))
    confidence_ok = bool(checks.get("confidence_ok"))
    too_extended = bool(derived.get("too_extended"))

    setup_score = _clamp_score(
        (0.30 * entry_score)
        + (0.12 if vwap_support_ok else 0.0)
        + (0.10 if volume_support_ok else 0.0)
        + (0.12 if structure_support_ok else 0.0)
        + (0.08 * candle_quality_score)
        + (0.07 * vwap_reference_quality_score)
        + (0.08 * reward_room_score)
        + (0.07 * multi_window_structure_score)
        + (0.05 if confidence_ok else 0.0)
        + (0.06 if extension_ok else 0.0)
        - (0.18 * exit_risk_score)
    )
    if setup_score >= min_a_setup_score:
        setup_quality = "A"
    elif setup_score >= 0.62:
        setup_quality = "B"
    elif setup_score > 0.0:
        setup_quality = "C"
    else:
        setup_quality = "reject"

    matched: List[str] = []
    if vwap_support_ok:
        matched.append("vwap_reclaim_or_near_ready")
    if volume_support_ok:
        matched.append("volume_expansion_or_near_ready")
    if structure_support_ok:
        matched.append("structure_support")
    if box_breakout_retest_hold:
        matched.append("box_breakout_retest_hold")
    if higher_low_continuation:
        matched.append("higher_low_continuation")
    if swing_low_above_vwap:
        matched.append("swing_low_above_vwap")
    if "reclaim_gate_ok" in required_failures and reclaim_near_ready:
        matched.append("required_reclaim_gate_near_ready")
    if detail_available and candle_quality_score >= min_candle_quality_score:
        matched.append("candle_quality_confirmed")
    if detail_available and vwap_reference_quality_score >= min_vwap_reference_quality_score:
        matched.append("vwap_reference_quality_confirmed")
    if detail_available and reward_room_score >= min_reward_room_score:
        matched.append("reward_room_confirmed")
    if detail_available and multi_window_structure_score >= min_multi_window_structure_score:
        matched.append("multi_window_structure_confirmed")

    out["observed"] = {
        "entry_chart_score": entry_score,
        "exit_risk_score": exit_risk_score,
        "candle_quality_score": candle_quality_score,
        "vwap_reference_quality_score": vwap_reference_quality_score,
        "reward_room_score": reward_room_score,
        "multi_window_structure_score": multi_window_structure_score,
        "chart_detail_context_available": detail_available,
        "chart_detail_observed": dict(detail.get("observed") or {}) if isinstance(detail.get("observed"), Mapping) else {},
        "vwap_reclaim_persistence": vwap_reclaim,
        "vwap_breakdown_persistence": vwap_breakdown,
        "volume_expansion_persistence": volume_state,
        "late_entry_risk": late_entry_risk,
        "swing_low_above_vwap": swing_low_above_vwap,
        "higher_low_continuation": higher_low_continuation,
        "box_breakout_retest_hold": box_breakout_retest_hold,
        "swing_low_break": swing_low_break,
        "lower_high_failure": lower_high_failure,
        "reclaim_distance_to_ready": reclaim_distance_value,
        "volume_distance_to_ready": volume_distance_value,
        "breakout_distance_to_ready": breakout_distance_value,
        "entry_quality_score": round(entry_quality_score, 4),
        "transition_readiness_score": round(transition_readiness_score, 4),
        "strong_quality_near_ready": bool(strong_quality_near_ready),
        "legacy_reason": legacy_reason_text,
    }
    out["matched_features"] = matched
    out["setup_score"] = round(setup_score, 4)
    out["setup_quality"] = setup_quality

    blockers: List[str] = []
    hard_required_failures = [
        name
        for name in required_failures
        if not (name == "reclaim_gate_ok" and reclaim_near_ready)
    ]
    if hard_required_failures:
        blockers.extend(f"required_check_failed:{name}" for name in hard_required_failures)
    if legacy_reason_text in {"volume_confirmation_missing", "volume_insufficient"} and not (
        bool(checks.get("volume_ok")) and strong_quality_near_ready
    ):
        blockers.append(f"legacy_reason_not_promotable:{legacy_reason_text}")
    if "vwap_reclaim_not_ready" in legacy_reason_text and not (bool(checks.get("reclaim_gate_ok")) or reclaim_near_ready):
        blockers.append("vwap_reclaim_not_near_ready")
    if entry_score < min_entry_score and not (
        entry_score >= min_live_entry_score and strong_quality_near_ready
    ):
        blockers.append(f"entry_chart_score<{min_entry_score:.2f}")
    if exit_risk_score > max_exit_risk:
        blockers.append(f"exit_risk_score>{max_exit_risk:.2f}")
    if not confidence_ok:
        blockers.append("confidence_gate_not_confirmed")
    if not extension_ok or too_extended:
        blockers.append("extension_safety_not_confirmed")
    if vwap_breakdown == "strong":
        blockers.append("vwap_breakdown_persistence=strong")
    if swing_low_break:
        blockers.append("swing_low_break=true")
    if lower_high_failure and vwap_reclaim != "strong":
        blockers.append("lower_high_failure_without_strong_vwap_reclaim")
    if late_entry_risk == "high":
        blockers.append("late_entry_risk=high")
    if detail_available and candle_quality_score < min_candle_quality_score:
        blockers.append(f"candle_quality_score<{min_candle_quality_score:.2f}")
    if detail_available and vwap_reference_quality_score < min_vwap_reference_quality_score:
        blockers.append(f"vwap_reference_quality_score<{min_vwap_reference_quality_score:.2f}")
    if detail_available and reward_room_score < min_reward_room_score:
        blockers.append(f"reward_room_score<{min_reward_room_score:.2f}")
    if detail_available and multi_window_structure_score < min_multi_window_structure_score:
        blockers.append(f"multi_window_structure_score<{min_multi_window_structure_score:.2f}")
    if not vwap_support_ok:
        blockers.append("vwap_reclaim_or_near_ready_missing")
    if not volume_support_ok:
        blockers.append("volume_confirmation_or_near_ready_missing")
    if not structure_support_ok:
        blockers.append("structure_support_missing")
    if not near_legacy_path:
        blockers.append("legacy_entry_path_not_near_ready")
    if setup_quality != "A":
        blockers.append("setup_quality_below_A")

    overrideable_blockers = {
        f"entry_chart_score<{min_entry_score:.2f}",
        "confidence_gate_not_confirmed",
        "legacy_entry_path_not_near_ready",
        "required_check_failed:rebound_ok",
    }
    selective_live_promotion_candidate = bool(
        setup_quality == "A"
        and setup_score >= (min_a_setup_score if strong_quality_near_ready else max(min_a_setup_score, 0.78))
        and (
            entry_score >= 0.60
            or (entry_score >= min_live_entry_score and strong_quality_near_ready)
        )
        and exit_risk_score <= max_exit_risk
        and vwap_support_ok
        and volume_support_ok
        and structure_support_ok
        and extension_ok
        and not too_extended
        and vwap_breakdown != "strong"
        and not swing_low_break
        and late_entry_risk != "high"
        and detail_available
        and candle_quality_score >= min_candle_quality_score
        and vwap_reference_quality_score >= min_vwap_reference_quality_score
        and reward_room_score >= max(min_reward_room_score, 0.35)
        and multi_window_structure_score >= max(min_multi_window_structure_score, 0.50)
        and strong_quality_near_ready
    )
    overridden_blockers: List[str] = []
    if selective_live_promotion_candidate and blockers:
        remaining_blockers: List[str] = []
        for blocker in blockers:
            if blocker in overrideable_blockers:
                overridden_blockers.append(blocker)
            else:
                remaining_blockers.append(blocker)
        if overridden_blockers:
            blockers = remaining_blockers
            matched.append("selective_human_chart_live_promotion")

    observed = dict(out.get("observed") or {})
    observed["selective_live_promotion_candidate"] = bool(selective_live_promotion_candidate)
    observed["selective_live_promotion_overridden_blockers"] = list(overridden_blockers)
    out["observed"] = observed
    out["matched_features"] = _dedupe_non_empty(matched)

    if blockers:
        out["blocking_features"] = _dedupe_non_empty(blockers)
        out["notes"] = ["human_chart_setup_not_actionable"]
        return out

    if box_breakout_retest_hold:
        setup_label = "breakout_retest_hold"
    elif higher_low_continuation and vwap_support_ok:
        setup_label = "higher_low_vwap_reclaim"
    elif swing_low_above_vwap:
        setup_label = "vwap_support_reclaim"
    else:
        setup_label = "clean_vwap_continuation"

    out["applied"] = True
    out["mode"] = "promote_wait_to_buy"
    out["setup_label"] = setup_label
    out["notes"] = _dedupe_non_empty(
        [
            "human_chart_a_setup_confirmed",
            "selective_live_promotion_override_used" if overridden_blockers else "",
        ]
    )
    return out


def _extract_explicit_policy_interpretation_fields(
    policy_contract: Mapping[str, Any] | None,
) -> Dict[str, Any]:
    from .intraday_monitor_signals_extract_explicit_policy_interpretation_fields import _extract_explicit_policy_interpretation_fields as owner
    return owner(policy_contract, facade=sys.modules[__name__])


def _build_monitor_policy_interpretation(
    *,
    received_policy: Mapping[str, Any] | MonitorEntryPolicy | None = None,
    effective_policy: Mapping[str, Any] | MonitorEntryPolicy | None = None,
    frame: Mapping[str, Any] | None = None,
    policy_contract: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    from .intraday_monitor_signals_build_monitor_policy_interpretation import _build_monitor_policy_interpretation as owner
    return owner(
        received_policy=received_policy,
        effective_policy=effective_policy,
        frame=frame,
        policy_contract=policy_contract,
        facade=sys.modules[__name__],
    )


_CHART_FEATURE_GROUP_PATHS: Dict[str, str] = {
    "structure_hh_hl": "structure",
    "structure_range_compression": "structure",
    "structure_breakout_attempt": "structure",
    "ma_alignment_state": "trend_alignment",
    "ma_slope_strength": "trend_alignment",
    "trend_regime": "trend_alignment",
    "support_holding": "support_resistance",
    "resistance_break_confirmed": "support_resistance",
    "failed_breakout": "support_resistance",
    "momentum_follow_through": "continuity_momentum",
    "volume_sustain": "continuity_momentum",
    "momentum_decay": "continuity_momentum",
}


_CHART_FEATURE_STATUS_RULES: Dict[str, Dict[str, set[str]]] = {
    "structure_hh_hl": {
        "pass": {"intact"},
        "fail": {"weakening", "broken"},
        "blocker_active": {"broken"},
        "blocker_inactive": {"intact", "weakening"},
    },
    "structure_range_compression": {
        "pass": {"moderate", "tight"},
        "fail": {"none"},
        "blocker_active": set(),
        "blocker_inactive": {"none", "moderate", "tight"},
    },
    "structure_breakout_attempt": {
        "pass": {"confirmed"},
        "fail": {"rejected"},
        "blocker_active": {"rejected"},
        "blocker_inactive": {"forming", "attempting", "confirmed", "none"},
    },
    "ma_alignment_state": {
        "pass": {"bullish"},
        "fail": {"bearish"},
        "blocker_active": {"bearish"},
        "blocker_inactive": {"bullish", "neutral", "mixed"},
    },
    "ma_slope_strength": {
        "pass": {"rising_strong", "rising_weak"},
        "fail": {"falling_weak", "falling_strong"},
        "blocker_active": {"falling_strong"},
        "blocker_inactive": {"rising_strong", "rising_weak", "flat", "falling_weak"},
    },
    "trend_regime": {
        "pass": {"trending"},
        "fail": set(),
        "blocker_active": set(),
        "blocker_inactive": {"trending", "ranging", "transition"},
    },
    "support_holding": {
        "pass": {"holding"},
        "fail": {"lost"},
        "blocker_active": {"lost"},
        "blocker_inactive": {"holding", "testing"},
    },
    "resistance_break_confirmed": {
        "pass": {"confirmed"},
        "fail": {"failed"},
        "blocker_active": {"failed"},
        "blocker_inactive": {"confirmed", "attempting", "none"},
    },
    "failed_breakout": {
        "pass": {"none"},
        "fail": {"suspected", "confirmed"},
        "blocker_active": {"confirmed"},
        "blocker_inactive": {"none", "suspected"},
    },
    "momentum_follow_through": {
        "pass": {"strong", "moderate"},
        "fail": {"weak", "none"},
        "blocker_active": {"none"},
        "blocker_inactive": {"strong", "moderate", "weak"},
    },
    "volume_sustain": {
        "pass": {"strong", "adequate"},
        "fail": {"fading", "absent"},
        "blocker_active": {"absent"},
        "blocker_inactive": {"strong", "adequate", "fading"},
    },
    "momentum_decay": {
        "pass": {"none"},
        "fail": {"strong"},
        "blocker_active": {"strong"},
        "blocker_inactive": {"none", "mild"},
    },
}


def _flatten_chart_structure_feature_states(
    chart_structure_features: Mapping[str, Any] | None,
) -> Dict[str, Dict[str, Any]]:
    from . import intraday_monitor_signals_flatten_chart_structure_feature_states as _owner
    return _owner._flatten_chart_structure_feature_states(chart_structure_features, facade=sys.modules[__name__])


def _parse_policy_signal_spec(spec: Any) -> Dict[str, Any]:
    from . import intraday_monitor_signals_parse_policy_signal_spec as _owner
    return _owner._parse_policy_signal_spec(spec, facade=sys.modules[__name__])


def _chart_feature_status_item(
    *,
    spec: Mapping[str, Any],
    chart_states: Mapping[str, Any],
    blocker: bool = False,
) -> Dict[str, Any] | None:
    from . import intraday_monitor_signals_chart_feature_status_item as _owner
    return _owner._chart_feature_status_item(spec=spec, chart_states=chart_states, blocker=blocker, facade=sys.modules[__name__])


def _build_monitor_policy_interpreter_trace(
    *,
    policy_interpretation: Mapping[str, Any] | None = None,
    signal_evidence: Mapping[str, Any] | None = None,
    chart_structure_features: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    from .intraday_monitor_signals_build_monitor_policy_interpreter_trace import _build_monitor_policy_interpreter_trace as owner
    return owner(
        policy_interpretation=policy_interpretation,
        signal_evidence=signal_evidence,
        chart_structure_features=chart_structure_features,
        facade=sys.modules[__name__],
    )


def _build_monitor_policy_alignment_summary(
    *,
    policy_interpreter_trace: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    from .intraday_monitor_signals_build_monitor_policy_alignment_summary import _build_monitor_policy_alignment_summary as owner
    return owner(policy_interpreter_trace=policy_interpreter_trace, facade=sys.modules[__name__])


def _build_monitor_policy_aware_gating(
    *,
    policy_interpretation: Mapping[str, Any] | None = None,
    signal_evidence: Mapping[str, Any] | None = None,
    policy_interpreter_trace: Mapping[str, Any] | None = None,
    policy_alignment_summary: Mapping[str, Any] | None = None,
    legacy_triggered: bool = False,
    legacy_reason: str | None = None,
) -> Dict[str, Any]:
    interpretation = dict(policy_interpretation or {}) if isinstance(policy_interpretation, Mapping) else {}
    evidence = dict(signal_evidence or {}) if isinstance(signal_evidence, Mapping) else {}
    trace = dict(policy_interpreter_trace or {}) if isinstance(policy_interpreter_trace, Mapping) else {}
    summary = dict(policy_alignment_summary or {}) if isinstance(policy_alignment_summary, Mapping) else {}

    out = _empty_monitor_policy_aware_gating()
    policy_available = bool(interpretation.get("policy_available"))
    if not policy_available:
        return out

    out["available"] = True
    relaxable_checks = _dedupe_non_empty(interpretation.get("relaxable_checks") or [])
    out["relaxations_considered"] = list(relaxable_checks)
    failed_required = _dedupe_non_empty(summary.get("top_failed_required_checks") or [])
    out["required_failures"] = list(failed_required)

    checks = dict(evidence.get("checks") or {}) if isinstance(evidence.get("checks"), Mapping) else {}
    derived = dict(evidence.get("derived") or {}) if isinstance(evidence.get("derived"), Mapping) else {}
    entry_style = str(interpretation.get("entry_style") or "").strip().lower()
    alignment_state = str(summary.get("alignment_state") or "").strip().lower()
    legacy_reason_code = str(legacy_reason or "").strip()

    if failed_required:
        out["blocked_by_required"] = list(failed_required)
        out["notes"] = _dedupe_non_empty(
            [
                *list(out.get("notes") or []),
                "required_checks_failed",
            ]
        )
        return out
    if bool(legacy_triggered):
        out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "legacy_gate_already_triggered"])
        return out

    can_consider_reclaim_relax = (
        entry_style == "breakout"
        and "reclaim_gate_ok" in relaxable_checks
    )
    if not can_consider_reclaim_relax:
        return out

    reclaim_distance = derived.get("reclaim_distance_to_ready")
    reclaim_distance_value: float | None = None
    if reclaim_distance not in (None, ""):
        try:
            reclaim_distance_value = float(reclaim_distance)
        except Exception:
            reclaim_distance_value = None

    standard_near_ready = (
        reclaim_distance_value is not None
        and _RECLAIM_NEAR_READY_DISTANCE_MIN_BASE <= reclaim_distance_value < 0.0
    )
    tuned_near_ready = (
        reclaim_distance_value is not None
        and _RECLAIM_NEAR_READY_DISTANCE_MIN_TUNED <= reclaim_distance_value < 0.0
    )
    tuned_only_band = (
        legacy_reason_code == "below_vwap_reclaim_not_ready"
        and not standard_near_ready
        and tuned_near_ready
    )
    near_ready = bool(standard_near_ready or tuned_only_band)
    safe_to_relax = (
        bool(checks.get("breakout_path_ok"))
        and bool(checks.get("confidence_ok"))
        and not bool(derived.get("too_extended"))
        and alignment_state in {"aligned", "partial"}
    )
    relaxable_reason = legacy_reason_code in {
        "",
        "below_vwap_reclaim_not_ready",
    }
    if not relaxable_reason:
        out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "legacy_reason_not_relaxable"])
        return out
    if bool(checks.get("reclaim_gate_ok")):
        out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "reclaim_gate_already_passed"])
        return out
    if not near_ready:
        out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "reclaim_not_near_ready"])
        return out
    if not safe_to_relax:
        out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "safe_relaxation_conditions_not_met"])
        return out
    if tuned_only_band and not bool(checks.get("volume_ok")):
        out["notes"] = _dedupe_non_empty(
            [*list(out.get("notes") or []), "tuned_reclaim_requires_volume_confirmation"]
        )
        return out
    if not (bool(checks.get("volume_ok")) or bool(checks.get("breakout_path_ok"))):
        out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "supporting_path_not_ready"])
        return out

    if tuned_only_band:
        out["entry_tuning_flags"] = ["reclaim_small_relaxation_v1"]
        out["reclaim_readiness_tuned"] = True
        out["reclaim_near_ready_distance_min"] = _RECLAIM_NEAR_READY_DISTANCE_MIN_TUNED
        out["reclaim_tuning_band_used"] = "tuned"
        out["reclaim_evidence_explanation"] = (
            "VWAP reclaim is slightly short of the standard near-ready band, "
            "but small_relaxation_v1 allows it when breakout path and volume confirmation remain intact."
        )
    elif standard_near_ready:
        out["reclaim_tuning_band_used"] = "standard"
        out["reclaim_evidence_explanation"] = (
            "VWAP reclaim is already inside the standard near-ready band."
        )

    out["applied"] = True
    out["applied_hints"] = ["reclaim_relaxed_near_ready"]
    out["relaxations_applied"] = ["reclaim_gate_ok"]
    out["notes"] = _dedupe_non_empty(
        [
            *list(out.get("notes") or []),
            "breakout_reclaim_near_ready_relaxation_applied",
        ]
    )
    return out


def _build_chart_structure_decision_hint(
    *,
    policy_interpretation: Mapping[str, Any] | None = None,
    signal_evidence: Mapping[str, Any] | None = None,
    chart_structure_features: Mapping[str, Any] | None = None,
    legacy_triggered: bool = False,
    legacy_decision: str | None = None,
    legacy_reason: str | None = None,
    legacy_entry_condition_path: str | None = None,
) -> Dict[str, Any]:
    interpretation = dict(policy_interpretation or {}) if isinstance(policy_interpretation, Mapping) else {}
    evidence = dict(signal_evidence or {}) if isinstance(signal_evidence, Mapping) else {}
    chart_payload = dict(chart_structure_features or {}) if isinstance(chart_structure_features, Mapping) else {}
    out = _empty_chart_structure_decision_hint()

    policy_available = bool(interpretation.get("policy_available"))
    if not policy_available:
        return out

    out["available"] = True
    entry_style = str(interpretation.get("entry_style") or "").strip().lower() or None
    out["entry_style"] = entry_style
    if entry_style == "breakout":
        out["considered_features"] = [
            "structure_hh_hl",
            "momentum_follow_through",
            "failed_breakout",
        ]
    elif entry_style in {"pullback", "reversal"}:
        out["considered_features"] = [
            "support_holding",
            "trend_regime",
            "ma_alignment_state",
        ]
    else:
        out["notes"] = ["entry_style_not_chart_structure_guard_target"]
        return out

    if not bool(chart_payload.get("available")):
        out["notes"] = ["chart_structure_features_unavailable"]
        return out

    if not bool(legacy_triggered) or str(legacy_decision or "").strip().upper() != "BUY":
        out["notes"] = ["legacy_decision_not_structure_guard_target_buy"]
        return out

    chart_states = _flatten_chart_structure_feature_states(chart_payload)
    checks = dict(evidence.get("checks") or {}) if isinstance(evidence.get("checks"), Mapping) else {}
    if entry_style == "breakout":
        if str(legacy_entry_condition_path or "").strip() != "breakout_path":
            out["notes"] = ["legacy_entry_path_not_breakout"]
            return out

        structure_state = str(((chart_states.get("structure_hh_hl") or {}).get("state")) or "").strip().lower()
        follow_through_state = str(((chart_states.get("momentum_follow_through") or {}).get("state")) or "").strip().lower()
        failed_breakout_state = str(((chart_states.get("failed_breakout") or {}).get("state")) or "").strip().lower()

        if structure_state == "intact":
            out["matched_features"].append("structure_hh_hl=intact")
        elif structure_state:
            out["blocking_features"].append(f"structure_hh_hl={structure_state}")
        if follow_through_state == "strong":
            out["matched_features"].append("momentum_follow_through=strong")
        elif follow_through_state:
            out["blocking_features"].append(f"momentum_follow_through={follow_through_state}")
        if failed_breakout_state == "none":
            out["matched_features"].append("failed_breakout=none")
        elif failed_breakout_state:
            out["blocking_features"].append(f"failed_breakout={failed_breakout_state}")

        if not bool(checks.get("breakout_path_ok")):
            out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "breakout_path_not_confirmed"])
            return out
        if not bool(checks.get("confidence_ok")):
            out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "confidence_not_confirmed"])
            return out

        should_block = False
        if failed_breakout_state == "confirmed":
            should_block = True
        elif structure_state == "weakening" and follow_through_state in {"moderate", "weak", "none"}:
            should_block = True

        if not should_block:
            out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "continuation_quality_not_blocking"])
            return out

        out["applied"] = True
        out["mode"] = "block"
        out["notes"] = _dedupe_non_empty(
            [
                *list(out.get("notes") or []),
                "breakout_continuation_structure_guard_applied",
                str(legacy_reason or "").strip() or "legacy_reason_not_provided",
            ]
        )
        return out

    if str(legacy_entry_condition_path or "").strip() != "pullback_volume_path":
        out["notes"] = ["legacy_entry_path_not_pullback"]
        return out

    support_state = str(((chart_states.get("support_holding") or {}).get("state")) or "").strip().lower()
    trend_regime_state = str(((chart_states.get("trend_regime") or {}).get("state")) or "").strip().lower()
    ma_alignment_state = str(((chart_states.get("ma_alignment_state") or {}).get("state")) or "").strip().lower()

    if support_state == "holding":
        out["matched_features"].append("support_holding=holding")
    elif support_state:
        out["blocking_features"].append(f"support_holding={support_state}")
    if trend_regime_state == "trending":
        out["matched_features"].append("trend_regime=trending")
    elif trend_regime_state:
        out["blocking_features"].append(f"trend_regime={trend_regime_state}")
    if ma_alignment_state == "bullish":
        out["matched_features"].append("ma_alignment_state=bullish")
    elif ma_alignment_state:
        out["blocking_features"].append(f"ma_alignment_state={ma_alignment_state}")

    if not bool(checks.get("pullback_volume_path_ok")):
        out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "pullback_path_not_confirmed"])
        return out
    if not bool(checks.get("confidence_ok")):
        out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "confidence_not_confirmed"])
        return out

    should_block = False
    if support_state == "lost":
        should_block = True
    elif ma_alignment_state == "bearish" and trend_regime_state in {"transition", "ranging"}:
        should_block = True

    if not should_block:
        out["notes"] = _dedupe_non_empty([*list(out.get("notes") or []), "pullback_structure_not_blocking"])
        return out

    out["applied"] = True
    out["mode"] = "block"
    out["notes"] = _dedupe_non_empty(
        [
            *list(out.get("notes") or []),
            "pullback_reversal_structure_guard_applied",
            str(legacy_reason or "").strip() or "legacy_reason_not_provided",
        ]
    )
    return out


def _apply_monitor_scoring_fields(
    out: Dict[str, Any],
    *,
    scoring_settings: Dict[str, Any],
    hard_filter_passed: bool,
    hard_filter_fail_reasons: Sequence[str] | None,
    score_breakdown: Mapping[str, Any] | None = None,
    legacy_entry_decision: str = "WAIT",
    scoring_entry_decision: str = "WAIT",
) -> Dict[str, Any]:
    from . import intraday_monitor_signals_apply_monitor_scoring_fields as _owner
    return _owner._apply_monitor_scoring_fields(
        out, scoring_settings=scoring_settings, hard_filter_passed=hard_filter_passed,
        hard_filter_fail_reasons=hard_filter_fail_reasons, score_breakdown=score_breakdown,
        legacy_entry_decision=legacy_entry_decision, scoring_entry_decision=scoring_entry_decision,
        facade=sys.modules[__name__],
    )


def _candles_from_rows(rows: Sequence[Mapping[str, Any]] | None) -> List[Dict[str, Any]]:
    from . import intraday_monitor_signals_candles_from_rows as _owner
    return _owner._candles_from_rows(rows, facade=sys.modules[__name__])


def _merge_candle_group(group: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    from . import intraday_monitor_signals_merge_candle_group as _owner
    return _owner._merge_candle_group(group, facade=sys.modules[__name__])


def _compress_candles(rows: Sequence[Mapping[str, Any]], timeframe_minutes: int) -> List[Dict[str, Any]]:
    from . import intraday_monitor_signals_compress_candles as _owner
    return _owner._compress_candles(rows, timeframe_minutes, facade=sys.modules[__name__])


def _kst_session_key_and_minute(ts_value: Any) -> tuple[Any | None, float | None]:
    from . import intraday_monitor_signals_kst_session_key_and_minute as _owner
    return _owner._kst_session_key_and_minute(ts_value, facade=sys.modules[__name__])


def _current_kst_session_anchor(candles: Sequence[Mapping[str, Any]]) -> tuple[Any | None, int | None, float | None]:
    from . import intraday_monitor_signals_current_kst_session_anchor as _owner
    return _owner._current_kst_session_anchor(candles, facade=sys.modules[__name__])


def _current_kst_session_rows(candles: Sequence[Mapping[str, Any]]) -> List[Mapping[str, Any]]:
    from . import intraday_monitor_signals_current_kst_session_rows as _owner
    return _owner._current_kst_session_rows(candles, facade=sys.modules[__name__])


def _session_vwap(candles: Sequence[Mapping[str, Any]]) -> float | None:
    from . import intraday_monitor_signals_session_vwap as _owner
    return _owner._session_vwap(candles, facade=sys.modules[__name__])


def _session_gap_context(candles: Sequence[Mapping[str, Any]], current_close: float) -> Dict[str, Any]:
    from . import intraday_monitor_signals_session_gap_context as _owner
    return _owner._session_gap_context(candles, current_close, facade=sys.modules[__name__])


def _infer_spacing_seconds(candles: Sequence[Mapping[str, Any]]) -> float | None:
    from . import intraday_monitor_signals_infer_spacing_seconds as _owner
    return _owner._infer_spacing_seconds(candles, facade=sys.modules[__name__])


def _classify_series_quality(
    candles: Sequence[Mapping[str, Any]],
    *,
    timeframe_minutes: int,
) -> Dict[str, Any]:
    from . import intraday_monitor_signals_classify_series_quality as _owner
    return _owner._classify_series_quality(candles, timeframe_minutes=timeframe_minutes, facade=sys.modules[__name__])


def _extract_commander_entry_control(
    policy: Mapping[str, Any] | MonitorEntryPolicy | None,
    frame: Mapping[str, Any] | None,
) -> Dict[str, Any]:
    from . import intraday_monitor_signals_extract_commander_entry_control as _owner
    return _owner._extract_commander_entry_control(policy, frame, facade=sys.modules[__name__])


def resolve_intraday_entry_policy(
    policy: Mapping[str, Any] | MonitorEntryPolicy | None = None,
    *,
    frame: Mapping[str, Any] | None = None,
) -> MonitorEntryPolicy:
    resolved = policy if isinstance(policy, MonitorEntryPolicy) else MonitorEntryPolicy.from_mapping(policy)
    adjustments: List[str] = []
    entry_control = _extract_commander_entry_control(policy, frame)
    playbook = str((frame or {}).get("playbook") or "").strip().lower()
    guidance = str((frame or {}).get("monitor_guidance") or "").strip().lower()
    risk_tone = str((frame or {}).get("risk_tone") or "").strip().lower()
    aggressiveness = str((frame or {}).get("trade_aggressiveness") or "").strip().lower()

    if playbook == "breakout":
        resolved = replace(
            resolved,
            volume_ratio_min=max(1.0, float(resolved.volume_ratio_min)),
            max_extended_from_vwap_pct=min(0.03, max(float(resolved.max_extended_from_vwap_pct), 0.02)),
            pullback_max_pct=min(0.04, max(float(resolved.pullback_max_pct), 0.03)),
        )
        adjustments.append("playbook:breakout")
    elif playbook in ("pullback", "reversal"):
        resolved = replace(
            resolved,
            breakout_lookback=max(3, int(resolved.breakout_lookback) - 1),
            volume_ratio_min=max(0.68, min(float(resolved.volume_ratio_min), 0.9)),
            min_extended_from_vwap_pct=min(float(resolved.min_extended_from_vwap_pct), -0.005),
            max_extended_from_vwap_pct=max(float(resolved.max_extended_from_vwap_pct), 0.05),
            pullback_min_pct=max(0.008, float(resolved.pullback_min_pct) - 0.004),
            pullback_max_pct=max(float(resolved.pullback_max_pct), 0.06),
        )
        # Keep shallow pullback entries available during live pullback monitoring.
        adjustments.append(f"playbook:{playbook}")
    elif playbook == "defensive":
        resolved = replace(
            resolved,
            volume_ratio_min=min(1.1, float(resolved.volume_ratio_min) + 0.03),
            max_extended_from_vwap_pct=max(0.03, min(float(resolved.max_extended_from_vwap_pct), 0.05)),
            pullback_max_pct=min(float(resolved.pullback_max_pct), 0.05),
        )
        adjustments.append("playbook:defensive")

    if guidance == "hold_through_noise":
        resolved = replace(
            resolved,
            pullback_max_pct=min(0.07, float(resolved.pullback_max_pct) + 0.005),
        )
        adjustments.append("guidance:hold_through_noise")
    elif guidance == "defensive_exit":
        if playbook in ("pullback", "reversal"):
            resolved = replace(
                resolved,
                volume_ratio_min=max(0.68, min(1.0, float(resolved.volume_ratio_min) - 0.04)),
                max_extended_from_vwap_pct=max(0.05, float(resolved.max_extended_from_vwap_pct)),
            )
            adjustments.append("guidance:defensive_exit_pullback")
        else:
            next_max_extended = float(resolved.max_extended_from_vwap_pct)
            if playbook != "defensive":
                next_max_extended = max(0.03, float(resolved.max_extended_from_vwap_pct) - 0.0025)
            resolved = replace(
                resolved,
                volume_ratio_min=min(1.1, float(resolved.volume_ratio_min) + 0.01),
                max_extended_from_vwap_pct=next_max_extended,
            )
            adjustments.append("guidance:defensive_exit")

    if risk_tone == "conservative":
        if playbook in ("pullback", "reversal"):
            resolved = replace(
                resolved,
                volume_ratio_min=min(1.0, float(resolved.volume_ratio_min)),
                max_extended_from_vwap_pct=max(0.05, float(resolved.max_extended_from_vwap_pct)),
            )
            adjustments.append("risk_tone:conservative_pullback")
        else:
            next_max_extended = float(resolved.max_extended_from_vwap_pct)
            if playbook != "defensive":
                next_max_extended = max(0.03, float(resolved.max_extended_from_vwap_pct) - 0.0025)
            resolved = replace(
                resolved,
                volume_ratio_min=min(1.1, float(resolved.volume_ratio_min) + 0.01),
                max_extended_from_vwap_pct=next_max_extended,
            )
            adjustments.append("risk_tone:conservative")
    elif risk_tone == "aggressive":
        resolved = replace(
            resolved,
            volume_ratio_min=max(0.9, float(resolved.volume_ratio_min) - 0.05),
            max_extended_from_vwap_pct=min(0.08, float(resolved.max_extended_from_vwap_pct) + 0.01),
        )
        adjustments.append("risk_tone:aggressive")

    if aggressiveness == "low":
        if playbook in ("pullback", "reversal"):
            resolved = replace(
                resolved,
                volume_ratio_min=min(1.1, float(resolved.volume_ratio_min) + 0.02),
            )
            adjustments.append("trade_aggressiveness:low_pullback")
        else:
            resolved = replace(
                resolved,
                volume_ratio_min=min(1.2, float(resolved.volume_ratio_min) + 0.02),
            )
            adjustments.append("trade_aggressiveness:low")
    elif aggressiveness == "high":
        resolved = replace(
            resolved,
            volume_ratio_min=max(0.9, float(resolved.volume_ratio_min) - 0.05),
            max_extended_from_vwap_pct=min(0.08, float(resolved.max_extended_from_vwap_pct) + 0.005),
        )
        adjustments.append("trade_aggressiveness:high")

    if _to_bool(entry_control.get("allow_dynamic_entry_band"), False):
        raw_target = entry_control.get(
            "adaptive_max_extended_from_vwap_pct",
            entry_control.get("max_extended_from_vwap_pct"),
        )
        target = _to_float(raw_target, 0.0)
        cap = _to_float(entry_control.get("max_extended_from_vwap_pct_cap"), 0.10)
        cap = max(float(resolved.max_extended_from_vwap_pct), min(0.12, max(0.03, cap)))
        next_max_extended = min(cap, max(float(resolved.max_extended_from_vwap_pct), target))
        if next_max_extended > float(resolved.max_extended_from_vwap_pct):
            resolved = replace(
                resolved,
                max_extended_from_vwap_pct=round(float(next_max_extended), 6),
            )
            adjustments.append("commander_entry_control:dynamic_entry_band")

    return replace(resolved, adjustments=tuple(adjustments))


def evaluate_intraday_entry_signal(
    rows: Sequence[Mapping[str, Any]] | None,
    *,
    current_price: Any = None,
    features: Mapping[str, Any] | None = None,
    policy: Mapping[str, Any] | MonitorEntryPolicy | None = None,
    frame: Mapping[str, Any] | None = None,
    scoring: Mapping[str, Any] | None = None,
    policy_contract: Mapping[str, Any] | None = None,
) -> Dict[str, Any]:
    # When monitor passes a MonitorEntryPolicy instance, it has already resolved
    # the strategy frame for this cycle. Re-applying the frame here would tighten
    # thresholds a second time and drift away from the commander-confirmed baseline.
    candles, out, resolved_policy, scoring_settings, timeframe_minutes = signal_feature_candles_out(policy=policy, frame=frame, scoring=scoring, rows=rows, policy_contract=policy_contract, facade=_r3_sys.modules[__name__])
    _apply_monitor_scoring_fields(
        out,
        scoring_settings=scoring_settings,
        hard_filter_passed=False,
        hard_filter_fail_reasons=[],
        score_breakdown={},
        legacy_entry_decision="WAIT",
        scoring_entry_decision="WAIT",
    )
    if not out["enabled"]:
        out["reason"] = "intraday_entry_disabled"
        return out
    if not candles:
        out["reason"] = "minute_candle_missing"
        out["metrics"] = {
            "bar_count": 0,
            "min_required_bars": 0,
            "timeframe_minutes": timeframe_minutes,
            "price": _to_float(current_price) if _to_float(current_price) > 0.0 else None,
            "vwap": None,
            "vwap_distance": None,
            "volume_ratio": None,
            "recent_high": None,
            "pullback_pct": None,
        }
        _apply_monitor_scoring_fields(
            out,
            scoring_settings=scoring_settings,
            hard_filter_passed=False,
            hard_filter_fail_reasons=["minute_candle_missing"],
            score_breakdown={},
            legacy_entry_decision="WAIT",
            scoring_entry_decision="WAIT",
        )
        return out
    min_required_bars = max(
        int(resolved_policy.breakout_lookback or 5) + 1,
        int(resolved_policy.volume_lookback or 5) + 1,
        4,
    )
    series_quality = _classify_series_quality(candles, timeframe_minutes=timeframe_minutes)
    out["series_quality"] = dict(series_quality)
    if not bool(series_quality.get("intraday_compatible")):
        out["reason"] = "minute_candle_missing"
        out["metrics"] = {
            "bar_count": len(candles),
            "min_required_bars": min_required_bars,
            "timeframe_minutes": timeframe_minutes,
            "price": _to_float(current_price) if _to_float(current_price) > 0.0 else None,
            "vwap": _to_float(_session_vwap(candles), 0.0) or None,
            "vwap_distance": None,
            "volume_ratio": None,
            "recent_high": None,
            "pullback_pct": None,
            "inferred_spacing_minutes": series_quality.get("inferred_spacing_minutes"),
            "series_class": series_quality.get("series_class"),
            "compatibility_reason": series_quality.get("compatibility_reason"),
        }
        _apply_monitor_scoring_fields(
            out,
            scoring_settings=scoring_settings,
            hard_filter_passed=False,
            hard_filter_fail_reasons=["minute_candle_missing"],
            score_breakdown={},
            legacy_entry_decision="WAIT",
            scoring_entry_decision="WAIT",
        )
        return out
    if len(candles) < min_required_bars:
        out["reason"] = "data_incomplete"
        out["metrics"] = {
            "bar_count": len(candles),
            "min_required_bars": min_required_bars,
            "timeframe_minutes": timeframe_minutes,
            "price": _to_float(current_price) if _to_float(current_price) > 0.0 else None,
            "vwap": _to_float(_session_vwap(candles), 0.0) or None,
            "vwap_distance": None,
            "volume_ratio": None,
            "recent_high": None,
            "pullback_pct": None,
            "inferred_spacing_minutes": series_quality.get("inferred_spacing_minutes"),
            "series_class": series_quality.get("series_class"),
        }
        _apply_monitor_scoring_fields(
            out,
            scoring_settings=scoring_settings,
            hard_filter_passed=False,
            hard_filter_fail_reasons=["data_incomplete"],
            score_breakdown={},
            legacy_entry_decision="WAIT",
            scoring_entry_decision="WAIT",
        )
        return out

    breakout_buffer_pct, breakout_level, breakout_ok, current_close, current_high, current_low, current_volume, current_vwap, extended_from_vwap_pct, minutes_since_session_open, open_gap_pct, prev_close_distance_pct, prior_bar_high, prior_bar_low, prior_close, pullback_depth_pct, rebound_ok, recent_high, reclaim_tolerance_pct, session_gap_context, volume_confirmation, volume_ratio_raw, vwap_hold_ok, vwap_reclaim_ok = breakout_level_features(out=out, candles=candles, resolved_policy=resolved_policy, current_price=current_price, facade=_r3_sys.modules[__name__])
    average_volume, breakout_chase_extension_observed, breakout_path_ok, breakout_score, breakout_volume_gate_ok, breakout_volume_gate_required, confirmation_ok, extension_ok, max_extended_from_vwap_pct, median_volume, min_extended_from_vwap_pct, opening_gap_chase_observed, pullback_mature, pullback_max_pct, pullback_min_pct, pullback_not_too_deep, pullback_ok, pullback_score, pullback_volume_path_ok, reclaim_gate_ok, volume_ok, volume_ratio, volume_score, vwap_structure_ok = volume_pullback_breakout_gate_features(volume_confirmation=volume_confirmation, resolved_policy=resolved_policy, extended_from_vwap_pct=extended_from_vwap_pct, pullback_depth_pct=pullback_depth_pct, vwap_hold_ok=vwap_hold_ok, vwap_reclaim_ok=vwap_reclaim_ok, rebound_ok=rebound_ok, breakout_ok=breakout_ok, minutes_since_session_open=minutes_since_session_open, open_gap_pct=open_gap_pct, prev_close_distance_pct=prev_close_distance_pct, session_gap_context=session_gap_context, current_close=current_close, breakout_level=breakout_level, facade=_r3_sys.modules[__name__])
    asset_class_detected, breakout_distance_to_ready, breakout_gap_pct, breakout_path_score, breakout_quality_score, confidence_gate_ok, confidence_score, confidence_threshold, confirmation_score, entry_quality_path, entry_quality_score, etf_deviation_pct, etf_deviation_source, extension_score, pullback_quality_score, pullback_volume_path_score, rebound_progress, reclaim_distance_to_ready, transition_readiness_score, volume_distance_to_ready, vwap_reclaim_progress, vwap_structure_score = signal_feature_asset_class_detected_breakout_distance_t(breakout_score=breakout_score, pullback_score=pullback_score, volume_score=volume_score, recent_high=recent_high, current_close=current_close, reclaim_tolerance_pct=reclaim_tolerance_pct, extended_from_vwap_pct=extended_from_vwap_pct, current_vwap=current_vwap, min_extended_from_vwap_pct=min_extended_from_vwap_pct, prior_bar_high=prior_bar_high, prior_close=prior_close, max_extended_from_vwap_pct=max_extended_from_vwap_pct, vwap_hold_ok=vwap_hold_ok, vwap_reclaim_ok=vwap_reclaim_ok, volume_ratio=volume_ratio, resolved_policy=resolved_policy, breakout_buffer_pct=breakout_buffer_pct, features=features, facade=_r3_sys.modules[__name__])
    etf_deviation_tradeable = bool(is_etf_asset_class(asset_class_detected) or etf_deviation_pct is not None)
    etf_deviation_chart_ok, etf_deviation_discount_entry_ok, etf_deviation_entry_path_ok, etf_deviation_entry_score, inverse_hedge_confidence_ok, inverse_hedge_reclaim_path_ok, inverse_hedge_volume_ok, lower_rebound_higher_lows, lower_rebound_volume_ok, lower_rebound_vwap_band_ok, lower_vwap_rebound_probe_path_ok, market_regime = signal_feature_etf_deviation_chart_ok_etf_deviation_dis(etf_deviation_tradeable=etf_deviation_tradeable, etf_deviation_pct=etf_deviation_pct, reclaim_gate_ok=reclaim_gate_ok, extension_ok=extension_ok, confirmation_ok=confirmation_ok, frame=frame, asset_class_detected=asset_class_detected, volume_ratio=volume_ratio, resolved_policy=resolved_policy, confidence_threshold=confidence_threshold, confidence_score=confidence_score, rebound_ok=rebound_ok, vwap_reclaim_ok=vwap_reclaim_ok, candles=candles, current_vwap=current_vwap, extended_from_vwap_pct=extended_from_vwap_pct, breakout_path_ok=breakout_path_ok, facade=_r3_sys.modules[__name__])

    if current_close <= 0.0 or recent_high <= 0.0 or current_vwap <= 0.0:
        signal_feature_effect_free_block_2745(out=out, timeframe_minutes=timeframe_minutes, pullback_depth_pct=pullback_depth_pct, candles=candles, current_close=current_close, current_vwap=current_vwap, extended_from_vwap_pct=extended_from_vwap_pct, volume_ratio=volume_ratio, volume_ratio_raw=volume_ratio_raw, average_volume=average_volume, median_volume=median_volume, volume_confirmation=volume_confirmation, recent_high=recent_high, series_quality=series_quality, facade=_r3_sys.modules[__name__])
        _apply_monitor_scoring_fields(
            out,
            scoring_settings=scoring_settings,
            hard_filter_passed=False,
            hard_filter_fail_reasons=["data_incomplete"],
            score_breakdown={},
            legacy_entry_decision="WAIT",
            scoring_entry_decision="WAIT",
        )
        return out

    breakout_volume_gate_ok, breakout_volume_gate_required, failed_checks, passed_checks, playbook, relevant_checks, signal_chain = signal_feature_breakout_volume_gate_ok_breakout_volume(breakout_ok=breakout_ok, vwap_hold_ok=vwap_hold_ok, vwap_reclaim_ok=vwap_reclaim_ok, volume_ok=volume_ok, rebound_ok=rebound_ok, pullback_ok=pullback_ok, confirmation_ok=confirmation_ok, extension_ok=extension_ok, reclaim_gate_ok=reclaim_gate_ok, breakout_path_ok=breakout_path_ok, pullback_volume_path_ok=pullback_volume_path_ok, opening_gap_chase_observed=opening_gap_chase_observed, breakout_chase_extension_observed=breakout_chase_extension_observed, etf_deviation_pct=etf_deviation_pct, etf_deviation_discount_entry_ok=etf_deviation_discount_entry_ok, etf_deviation_entry_path_ok=etf_deviation_entry_path_ok, inverse_hedge_reclaim_path_ok=inverse_hedge_reclaim_path_ok, lower_vwap_rebound_probe_path_ok=lower_vwap_rebound_probe_path_ok, frame=frame, vwap_structure_ok=vwap_structure_ok, breakout_volume_gate_ok=breakout_volume_gate_ok, pullback_mature=pullback_mature, pullback_not_too_deep=pullback_not_too_deep, confidence_gate_ok=confidence_gate_ok, etf_deviation_chart_ok=etf_deviation_chart_ok, lower_rebound_higher_lows=lower_rebound_higher_lows, lower_rebound_volume_ok=lower_rebound_volume_ok, lower_rebound_vwap_band_ok=lower_rebound_vwap_band_ok, etf_deviation_tradeable=etf_deviation_tradeable, breakout_volume_gate_required=breakout_volume_gate_required, facade=_r3_sys.modules[__name__])
    entry_condition_path, entry_condition_paths_passed, pattern, primary_failure_axis, reason, threshold_margins, triggered = signal_score_entry_condition_path_entry_condition_pat(volume_ratio=volume_ratio, volume_ratio_raw=volume_ratio_raw, average_volume=average_volume, median_volume=median_volume, extended_from_vwap_pct=extended_from_vwap_pct, min_extended_from_vwap_pct=min_extended_from_vwap_pct, max_extended_from_vwap_pct=max_extended_from_vwap_pct, pullback_depth_pct=pullback_depth_pct, pullback_min_pct=pullback_min_pct, pullback_max_pct=pullback_max_pct, breakout_gap_pct=breakout_gap_pct, breakout_buffer_pct=breakout_buffer_pct, open_gap_pct=open_gap_pct, prev_close_distance_pct=prev_close_distance_pct, minutes_since_session_open=minutes_since_session_open, etf_deviation_pct=etf_deviation_pct, etf_deviation_source=etf_deviation_source, asset_class_detected=asset_class_detected, market_regime=market_regime, volume_confirmation=volume_confirmation, opening_gap_chase_observed=opening_gap_chase_observed, volume_ok=volume_ok, breakout_chase_extension_observed=breakout_chase_extension_observed, etf_deviation_entry_path_ok=etf_deviation_entry_path_ok, inverse_hedge_volume_ok=inverse_hedge_volume_ok, inverse_hedge_confidence_ok=inverse_hedge_confidence_ok, inverse_hedge_reclaim_path_ok=inverse_hedge_reclaim_path_ok, lower_rebound_higher_lows=lower_rebound_higher_lows, lower_rebound_volume_ok=lower_rebound_volume_ok, rebound_ok=rebound_ok, lower_vwap_rebound_probe_path_ok=lower_vwap_rebound_probe_path_ok, resolved_policy=resolved_policy, breakout_level=breakout_level, current_close=current_close, etf_deviation_entry_score=etf_deviation_entry_score, confidence_score=confidence_score, breakout_path_ok=breakout_path_ok, pullback_volume_path_ok=pullback_volume_path_ok, facade=_r3_sys.modules[__name__])
    entry_condition_path, entry_hard_gate_blockers, entry_hard_gate_passed, entry_quality_tier, entry_quality_vs_gate_summary, grouped_logic_trace, pattern, primary_failure_axis, reason, triggered = signal_score_entry_condition_path_entry_hard_gate_blo(etf_deviation_pct=etf_deviation_pct, etf_deviation_source=etf_deviation_source, asset_class_detected=asset_class_detected, reclaim_gate_ok=reclaim_gate_ok, breakout_volume_gate_required=breakout_volume_gate_required, breakout_volume_gate_ok=breakout_volume_gate_ok, opening_gap_chase_observed=opening_gap_chase_observed, breakout_chase_extension_observed=breakout_chase_extension_observed, extension_ok=extension_ok, breakout_path_ok=breakout_path_ok, pullback_volume_path_ok=pullback_volume_path_ok, etf_deviation_discount_entry_ok=etf_deviation_discount_entry_ok, etf_deviation_chart_ok=etf_deviation_chart_ok, etf_deviation_entry_path_ok=etf_deviation_entry_path_ok, inverse_hedge_reclaim_path_ok=inverse_hedge_reclaim_path_ok, lower_vwap_rebound_probe_path_ok=lower_vwap_rebound_probe_path_ok, entry_condition_paths_passed=entry_condition_paths_passed, confidence_gate_ok=confidence_gate_ok, resolved_policy=resolved_policy, volume_confirmation=volume_confirmation, threshold_margins=threshold_margins, playbook=playbook, extended_from_vwap_pct=extended_from_vwap_pct, max_extended_from_vwap_pct=max_extended_from_vwap_pct, volume_ok=volume_ok, vwap_hold_ok=vwap_hold_ok, rebound_ok=rebound_ok, vwap_reclaim_ok=vwap_reclaim_ok, pullback_ok=pullback_ok, pullback_mature=pullback_mature, pullback_not_too_deep=pullback_not_too_deep, breakout_ok=breakout_ok, triggered=triggered, primary_failure_axis=primary_failure_axis, failed_checks=failed_checks, relevant_checks=relevant_checks, entry_quality_score=entry_quality_score, entry_condition_path=entry_condition_path, pattern=pattern, facade=_r3_sys.modules[__name__])
    if entry_quality_tier in {"strong", "watch"} and not entry_hard_gate_passed:
        blocker_text = ", ".join(entry_hard_gate_blockers[:4]) or reason or primary_failure_axis or "hard_gate_not_passed"
        entry_quality_vs_gate_summary = (
            f"entry_quality_{entry_quality_tier}_but_hard_gate_failed:{blocker_text}"
        )
    elif entry_hard_gate_passed:
        entry_quality_vs_gate_summary = f"hard_gate_passed:{entry_condition_path or reason or 'entry_confirmed'}"
    chart_structure_features, legacy_decision, legacy_entry_condition_path, legacy_pattern, legacy_reason, legacy_triggered, score_breakdown = signal_score_chart_structure_features_legacy_decision(entry_condition_path=entry_condition_path, grouped_logic_trace=grouped_logic_trace, triggered=triggered, reason=reason, pattern=pattern, candles=candles, current_close=current_close, current_vwap=current_vwap, recent_high=recent_high, breakout_ok=breakout_ok, pullback_ok=pullback_ok, vwap_reclaim_ok=vwap_reclaim_ok, volume_ok=volume_ok, confidence_gate_ok=confidence_gate_ok, volume_ratio=volume_ratio, extension_ok=extension_ok, extended_from_vwap_pct=extended_from_vwap_pct, max_extended_from_vwap_pct=max_extended_from_vwap_pct, pullback_mature=pullback_mature, facade=_r3_sys.modules[__name__])
    if etf_deviation_tradeable:
        score_breakdown["etf_deviation_discount"] = round(float(etf_deviation_entry_score), 4)
    chart_structure_decision_hint, policy_alignment_summary, policy_aware_gating, policy_interpreter_trace, signal_evidence = signal_score_chart_structure_decision_hint_policy_ali(scoring_settings=scoring_settings, score_breakdown=score_breakdown, vwap_reclaim_progress=vwap_reclaim_progress, volume_score=volume_score, pullback_score=pullback_score, breakout_score=breakout_score, confidence_score=confidence_score, confidence_threshold=confidence_threshold, entry_quality_score=entry_quality_score, breakout_quality_score=breakout_quality_score, pullback_quality_score=pullback_quality_score, entry_quality_path=entry_quality_path, vwap_reclaim_ok=vwap_reclaim_ok, volume_ok=volume_ok, pullback_ok=pullback_ok, breakout_ok=breakout_ok, rebound_ok=rebound_ok, reclaim_gate_ok=reclaim_gate_ok, breakout_path_ok=breakout_path_ok, pullback_volume_path_ok=pullback_volume_path_ok, extension_ok=extension_ok, rebound_progress=rebound_progress, transition_readiness_score=transition_readiness_score, reclaim_distance_to_ready=reclaim_distance_to_ready, volume_distance_to_ready=volume_distance_to_ready, breakout_distance_to_ready=breakout_distance_to_ready, extended_from_vwap_pct=extended_from_vwap_pct, max_extended_from_vwap_pct=max_extended_from_vwap_pct, chart_structure_features=chart_structure_features, out=out, legacy_triggered=legacy_triggered, legacy_reason=legacy_reason, legacy_decision=legacy_decision, legacy_entry_condition_path=legacy_entry_condition_path, facade=_r3_sys.modules[__name__])
    if bool(chart_structure_decision_hint.get("available")):
        policy_interpreter_trace["notes"] = _dedupe_non_empty(
            [
                *list(policy_interpreter_trace.get("notes") or []),
                "chart_structure_decision_hint_evaluated",
            ]
        )
    if bool(chart_structure_decision_hint.get("applied")):
        policy_alignment_summary["summary_notes"] = _dedupe_non_empty(
            [
                *list(policy_alignment_summary.get("summary_notes") or []),
                "chart_structure_decision_hint_applied",
            ]
        )
    chart_human_context = (
        dict(chart_structure_features.get("human_chart_context") or {})
        if isinstance(chart_structure_features.get("human_chart_context"), Mapping)
        else {}
    )
    human_chart_detail_context = _build_human_chart_detail_context(
        candles,
        current_close=current_close,
        current_vwap=current_vwap,
        recent_high=recent_high,
        breakout_level=breakout_level,
        volume_ratio=volume_ratio,
    )
    if bool(policy_aware_gating.get("applied")):
        triggered = True
        pattern = "breakout_policy_reclaim_near_ready"
        reason = "breakout_above_recent_high_with_policy_reclaim_near_ready"
        entry_condition_path = "breakout_path"
        primary_failure_axis = "confirmed_entry"
        if "breakout_path" not in entry_condition_paths_passed:
            entry_condition_paths_passed.append("breakout_path")
        if "policy_reclaim_near_ready" not in signal_chain:
            signal_chain.append("policy_reclaim_near_ready")
    elif bool(chart_structure_decision_hint.get("applied")):
        triggered = False
        hint_entry_style = str(chart_structure_decision_hint.get("entry_style") or "").strip().lower()
        if hint_entry_style in {"pullback", "reversal"}:
            reason = "pullback_reversal_structure_guard_blocked"
            primary_failure_axis = "chart_structure_support"
            if "chart_structure_pullback_reversal_guard" not in signal_chain:
                signal_chain.append("chart_structure_pullback_reversal_guard")
        else:
            reason = "breakout_continuation_structure_guard_blocked"
            primary_failure_axis = "chart_structure_continuation"
            if "chart_structure_breakout_continuation_guard" not in signal_chain:
                signal_chain.append("chart_structure_breakout_continuation_guard")

    human_chart_entry_setup = _build_human_chart_entry_setup(
        chart_human_context=chart_human_context,
        chart_detail_context=human_chart_detail_context,
        signal_evidence=signal_evidence,
        policy_alignment_summary=policy_alignment_summary,
        candidate_triggered=bool(triggered),
        legacy_reason=legacy_reason,
    )
    if bool(human_chart_entry_setup.get("applied")):
        triggered = True
        setup_label = str(human_chart_entry_setup.get("setup_label") or "clean_vwap_continuation")
        pattern = f"human_chart_{setup_label}"
        reason = "human_chart_entry_setup_confirmed"
        entry_condition_path = "human_chart_setup_path"
        primary_failure_axis = "confirmed_entry"
        if "human_chart_setup_path" not in entry_condition_paths_passed:
            entry_condition_paths_passed.append("human_chart_setup_path")
        if "human_chart_entry_setup" not in signal_chain:
            signal_chain.append("human_chart_entry_setup")
        if "human_chart_entry_setup" not in passed_checks:
            passed_checks.append("human_chart_entry_setup")
        policy_alignment_summary["summary_notes"] = _dedupe_non_empty(
            [
                *list(policy_alignment_summary.get("summary_notes") or []),
                "human_chart_entry_setup_applied",
            ]
        )

    human_chart_buy_guard = _build_human_chart_buy_guard(
        chart_human_context=chart_human_context,
        chart_detail_context=human_chart_detail_context,
        prev_close_distance_pct=prev_close_distance_pct,
        open_gap_pct=open_gap_pct,
        candidate_triggered=bool(triggered),
        entry_condition_path=entry_condition_path,
    )
    if bool(human_chart_buy_guard.get("applied")):
        triggered = False
        reason = "human_chart_sanity_guard_blocked"
        primary_failure_axis = "human_chart_sanity"
        if "human_chart_buy_guard" not in signal_chain:
            signal_chain.append("human_chart_buy_guard")
        if "human_chart_buy_guard" not in failed_checks:
            failed_checks.append("human_chart_buy_guard")
        policy_alignment_summary["summary_notes"] = _dedupe_non_empty(
            [
                *list(policy_alignment_summary.get("summary_notes") or []),
                "human_chart_buy_guard_applied",
            ]
        )

    metrics = {
        "timeframe_minutes": timeframe_minutes,
        "bar_count": len(candles),
        "price": current_close if current_close > 0.0 else None,
        "current_price": current_close if current_close > 0.0 else None,
        "current_high": current_high if current_high > 0.0 else None,
        "current_low": current_low if current_low > 0.0 else None,
        "recent_high": recent_high if recent_high > 0.0 else None,
        "breakout_level": breakout_level if breakout_level > 0.0 else None,
        "prior_bar_high": prior_bar_high if prior_bar_high > 0.0 else None,
        "prior_bar_low": prior_bar_low if prior_bar_low > 0.0 else None,
        "vwap": current_vwap if current_vwap > 0.0 else None,
        "vwap_distance": extended_from_vwap_pct,
        "volume_ratio": volume_ratio if volume_ratio > 0.0 else None,
        "volume_ratio_raw": volume_ratio_raw if volume_ratio_raw > 0.0 else None,
        "volume_ratio_effective": volume_ratio if volume_ratio > 0.0 else None,
        "current_volume": current_volume if current_volume > 0.0 else None,
        "average_volume": average_volume if average_volume > 0.0 else None,
        "median_volume": median_volume if median_volume > 0.0 else None,
        "max_reference_volume": (
            float(volume_confirmation.max_reference_volume)
            if float(volume_confirmation.max_reference_volume) > 0.0
            else None
        ),
        "volume_adjusted": bool(volume_confirmation.adjusted),
        "volume_adjustment_reason": volume_confirmation.adjustment_reason,
        "volume_spike_skew_ratio": float(volume_confirmation.spike_skew_ratio),
        "pullback_pct": pullback_depth_pct,
        "pullback_depth_pct": pullback_depth_pct,
        "extended_from_vwap_pct": extended_from_vwap_pct,
        "reclaim_distance_to_ready": reclaim_distance_to_ready,
        "vwap_reclaim_progress": vwap_reclaim_progress,
        "rebound_progress": rebound_progress,
        "volume_distance_to_ready": volume_distance_to_ready,
        "breakout_gap_pct": breakout_gap_pct,
        "breakout_distance_to_ready": breakout_distance_to_ready,
        "session_context_available": bool(session_gap_context.get("session_context_available")),
        "session_open": session_gap_context.get("session_open"),
        "previous_close": session_gap_context.get("previous_close"),
        "open_gap_pct": open_gap_pct,
        "prev_close_distance_pct": prev_close_distance_pct,
        "minutes_since_session_open": minutes_since_session_open,
        "opening_gap_chase_observed": bool(opening_gap_chase_observed),
        "breakout_chase_extension_observed": bool(breakout_chase_extension_observed),
        "opening_gap_context_observation_only": True,
        "breakout_volume_gate_required": bool(breakout_volume_gate_required),
        "breakout_volume_gate_ok": bool(breakout_volume_gate_ok),
        "transition_readiness_score": transition_readiness_score,
        "entry_quality_score": entry_quality_score,
        "entry_quality_tier": entry_quality_tier,
        "entry_quality_path": entry_quality_path,
        "entry_quality_observability_only": True,
        "entry_hard_gate_passed": bool(entry_hard_gate_passed),
        "entry_hard_gate_blockers": list(entry_hard_gate_blockers),
        "entry_quality_vs_gate_summary": entry_quality_vs_gate_summary,
        "breakout_quality_score": breakout_quality_score,
        "pullback_quality_score": pullback_quality_score,
        "extension_score": round(_clamp_score(extension_score), 4),
        "vwap_structure_score": round(_clamp_score(vwap_structure_score), 4),
        "confirmation_score": round(_clamp_score(confirmation_score), 4),
        "breakout_ok": bool(breakout_ok),
        "vwap_hold_ok": bool(vwap_hold_ok),
        "vwap_reclaim_ok": bool(vwap_reclaim_ok),
        "rebound_ok": bool(rebound_ok),
        "volume_ok": bool(volume_ok),
        "extension_ok": bool(extension_ok),
        "pullback_ok": bool(pullback_ok),
        "pullback_mature": bool(pullback_mature),
        "pullback_not_too_deep": bool(pullback_not_too_deep),
        "confirmation_ok": bool(confirmation_ok),
        "vwap_structure_ok": bool(vwap_structure_ok),
        "reclaim_gate_ok": bool(reclaim_gate_ok),
        "breakout_path_ok": bool(breakout_path_ok),
        "pullback_volume_path_ok": bool(pullback_volume_path_ok),
        "breakout_score": breakout_score,
        "breakout_proximity_score": breakout_score,
        "volume_score": volume_score,
        "pullback_score": pullback_score,
        "breakout_path_score": breakout_path_score,
        "pullback_volume_path_score": pullback_volume_path_score,
        "confidence_score": confidence_score,
        "confidence_threshold": confidence_threshold,
        "confidence_gate_ok": bool(confidence_gate_ok),
        "engine_vwap_distance": (features or {}).get("engine_vwap_distance"),
        "engine_volume_spike20": (features or {}).get("engine_volume_spike20"),
        "engine_trend_strength": (features or {}).get("engine_trend_strength"),
        "inferred_spacing_minutes": series_quality.get("inferred_spacing_minutes"),
        "series_class": series_quality.get("series_class"),
        "human_chart_entry_score": chart_human_context.get("entry_chart_score"),
        "human_chart_exit_risk_score": chart_human_context.get("exit_risk_score"),
        "human_chart_setup_quality": human_chart_entry_setup.get("setup_quality"),
        "human_chart_setup_label": human_chart_entry_setup.get("setup_label"),
        "human_chart_setup_score": human_chart_entry_setup.get("setup_score"),
        "human_chart_entry_setup_applied": bool(human_chart_entry_setup.get("applied")),
        "human_candle_quality_score": human_chart_detail_context.get("candle_quality_score"),
        "human_vwap_reference_quality_score": human_chart_detail_context.get("vwap_reference_quality_score"),
        "human_reward_room_score": human_chart_detail_context.get("reward_room_score"),
        "human_multi_window_structure_score": human_chart_detail_context.get("multi_window_structure_score"),
        "human_chart_detail_observed": dict(human_chart_detail_context.get("observed") or {}),
        "vwap_reclaim_persistence": chart_human_context.get("vwap_reclaim_persistence"),
        "ma_bullish_persistence": chart_human_context.get("ma_bullish_persistence"),
        "volume_expansion_persistence": chart_human_context.get("volume_expansion_persistence"),
        "late_entry_risk": chart_human_context.get("late_entry_risk"),
        "swing_low_above_vwap": chart_human_context.get("swing_low_above_vwap"),
        "box_breakout_retest_hold": chart_human_context.get("box_breakout_retest_hold"),
        "etf_deviation_pct": etf_deviation_pct,
        "etf_deviation_source": etf_deviation_source,
        "asset_class_detected": asset_class_detected,
        "etf_deviation_discount_entry_ok": bool(etf_deviation_discount_entry_ok),
        "etf_deviation_entry_score": round(float(etf_deviation_entry_score), 4),
        "etf_deviation_entry_path_ok": bool(etf_deviation_entry_path_ok),
        "inverse_hedge_reclaim_path_ok": bool(inverse_hedge_reclaim_path_ok),
        "inverse_hedge_volume_ok": bool(inverse_hedge_volume_ok),
        "inverse_hedge_confidence_ok": bool(inverse_hedge_confidence_ok),
        "lower_vwap_rebound_probe_path_ok": bool(lower_vwap_rebound_probe_path_ok),
        "lower_rebound_higher_lows": bool(lower_rebound_higher_lows),
        "lower_rebound_volume_ok": bool(lower_rebound_volume_ok),
        "lower_rebound_vwap_band_ok": bool(lower_rebound_vwap_band_ok),
        "lower_vwap_rebound_probe": dict(threshold_margins.get("lower_vwap_rebound_probe") or {}),
    }
    transition_trace = _empty_entry_transition_trace()
    transition_trace.update(
        {
            "reclaim_distance_to_ready": reclaim_distance_to_ready,
            "vwap_reclaim_progress": round(vwap_reclaim_progress, 4),
            "rebound_progress": rebound_progress,
            "volume_distance_to_ready": volume_distance_to_ready,
            "breakout_distance_to_ready": breakout_distance_to_ready,
            "transition_readiness_score": transition_readiness_score,
            "last_blocking_axis": primary_failure_axis if not triggered else "",
            "became_ready_this_cycle": bool(
                policy_aware_gating.get("applied") or human_chart_entry_setup.get("applied")
            ),
        }
    )
    signal_explain_effect_free_block_3479(entry_condition_path=entry_condition_path, grouped_logic_trace=grouped_logic_trace, scoring_settings=scoring_settings, score_breakdown=score_breakdown, policy_aware_gating=policy_aware_gating, chart_structure_decision_hint=chart_structure_decision_hint, chart_human_context=chart_human_context, human_chart_entry_setup=human_chart_entry_setup, human_chart_detail_context=human_chart_detail_context, human_chart_buy_guard=human_chart_buy_guard, entry_quality_score=entry_quality_score, entry_quality_tier=entry_quality_tier, entry_quality_path=entry_quality_path, entry_hard_gate_passed=entry_hard_gate_passed, entry_hard_gate_blockers=entry_hard_gate_blockers, entry_quality_vs_gate_summary=entry_quality_vs_gate_summary, breakout_score=breakout_score, etf_deviation_entry_score=etf_deviation_entry_score, facade=_r3_sys.modules[__name__])
    _apply_monitor_scoring_fields(
        out,
        scoring_settings=scoring_settings,
        hard_filter_passed=not bool(human_chart_buy_guard.get("applied")),
        hard_filter_fail_reasons=list(human_chart_buy_guard.get("blocking_features") or [])
        if bool(human_chart_buy_guard.get("applied"))
        else [],
        score_breakdown=score_breakdown,
        legacy_entry_decision=legacy_decision,
        scoring_entry_decision="BUY" if sum(_to_float(v) for v in score_breakdown.values()) >= float(scoring_settings.get("entry_threshold") or 3.0) else "WAIT",
    )
    out.update(
        {
            "triggered": bool(triggered),
            "decision": "BUY" if triggered else "WAIT",
            "pattern": pattern,
            "reason": reason,
            "signal_chain": signal_chain,
            "metrics": metrics,
            "passed_checks": passed_checks,
            "failed_checks": failed_checks,
            "primary_failure_axis": primary_failure_axis,
            "threshold_margins": threshold_margins,
            "entry_condition_path": entry_condition_path,
            "entry_condition_paths_passed": entry_condition_paths_passed,
            "condition_scores": {
                "breakout_score": breakout_score,
                "breakout_proximity_score": breakout_score,
                "volume_score": volume_score,
                "pullback_score": pullback_score,
                "breakout_path_score": breakout_path_score,
                "pullback_volume_path_score": pullback_volume_path_score,
                "confidence_score": confidence_score,
                "confidence_threshold": confidence_threshold,
                "confidence_gate_ok": bool(confidence_gate_ok),
                "transition_readiness_score": transition_readiness_score,
                "entry_quality_score": entry_quality_score,
                "entry_quality_tier": entry_quality_tier,
                "entry_quality_path": entry_quality_path,
                "entry_quality_observability_only": True,
                "entry_hard_gate_passed": bool(entry_hard_gate_passed),
                "entry_hard_gate_blockers": list(entry_hard_gate_blockers),
                "entry_quality_vs_gate_summary": entry_quality_vs_gate_summary,
                "breakout_quality_score": breakout_quality_score,
                "pullback_quality_score": pullback_quality_score,
                "etf_deviation_entry_score": round(float(etf_deviation_entry_score), 4),
                "etf_deviation_discount_entry_ok": bool(etf_deviation_discount_entry_ok),
                "etf_deviation_entry_path_ok": bool(etf_deviation_entry_path_ok),
                "extension_score": round(_clamp_score(extension_score), 4),
                "vwap_structure_score": round(_clamp_score(vwap_structure_score), 4),
                "confirmation_score": round(_clamp_score(confirmation_score), 4),
            },
            "grouped_logic_trace": grouped_logic_trace,
            "legacy_entry_reason": legacy_reason,
            "legacy_entry_pattern": legacy_pattern,
            "legacy_entry_condition_path": legacy_entry_condition_path,
            "signal_evidence": signal_evidence,
            "chart_structure_features": chart_structure_features,
            "policy_interpreter_trace": policy_interpreter_trace,
            "policy_alignment_summary": policy_alignment_summary,
            "policy_aware_gating": policy_aware_gating,
            "chart_structure_decision_hint": chart_structure_decision_hint,
            "human_chart_detail_context": human_chart_detail_context,
            "human_chart_entry_setup": human_chart_entry_setup,
            "human_chart_buy_guard": human_chart_buy_guard,
            "reclaim_distance_to_ready": reclaim_distance_to_ready,
            "vwap_reclaim_progress": round(vwap_reclaim_progress, 4),
            "rebound_progress": rebound_progress,
            "volume_distance_to_ready": volume_distance_to_ready,
            "breakout_distance_to_ready": breakout_distance_to_ready,
            "transition_readiness_score": transition_readiness_score,
            "last_blocking_axis": str(primary_failure_axis or "") if not triggered else "",
            "became_ready_this_cycle": bool(
                policy_aware_gating.get("applied") or human_chart_entry_setup.get("applied")
            ),
            "entry_transition_trace": transition_trace,
        }
    )
    return out
