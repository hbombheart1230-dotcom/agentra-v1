from __future__ import annotations

def build_monitor_no_trade_surface(entry_info: facade.Mapping[str, facade.Any] | None, *, final_decision: facade.Any, buy_submitted: bool, guard_blocked: bool=False, guard_reason: facade.Any=None, commander_no_trade_reason_code: facade.Any=None, facade: facade.Any) -> facade.Dict[str, facade.Any]:
    row = dict(entry_info or {}) if isinstance(entry_info, facade.Mapping) else {}
    summary = dict(row.get('policy_alignment_summary') or {}) if isinstance(row.get('policy_alignment_summary'), facade.Mapping) else {}
    trace = dict(row.get('policy_interpreter_trace') or {}) if isinstance(row.get('policy_interpreter_trace'), facade.Mapping) else {}
    check_status = dict(trace.get('check_status') or {}) if isinstance(trace.get('check_status'), facade.Mapping) else {}
    condition_scores = dict(row.get('condition_scores') or {}) if isinstance(row.get('condition_scores'), facade.Mapping) else {}
    policy_interpretation = dict(row.get('policy_interpretation') or {}) if isinstance(row.get('policy_interpretation'), facade.Mapping) else {}
    policy_gating = dict(row.get('policy_aware_gating') or {}) if isinstance(row.get('policy_aware_gating'), facade.Mapping) else {}
    chart_hint = dict(row.get('chart_structure_decision_hint') or {}) if isinstance(row.get('chart_structure_decision_hint'), facade.Mapping) else {}
    decision_outcome = facade._normalize_decision_outcome(final_decision, fallback='BUY' if buy_submitted else 'WAIT')
    evaluated = bool(row.get('evaluated'))
    pre_intent_decision = 'BUY' if bool(row.get('triggered')) else 'NOOP' if not evaluated else 'WAIT'
    no_trade_stage = 'none'
    if decision_outcome not in {'BUY', 'SELL'}:
        if guard_blocked:
            no_trade_stage = 'guard_block'
        elif pre_intent_decision == 'NOOP':
            no_trade_stage = 'pre_intent_noop'
        else:
            no_trade_stage = 'pre_intent_wait'
    no_trade_reason_code = str(guard_reason or '').strip() if guard_blocked else str(row.get('reason') or commander_no_trade_reason_code or row.get('primary_failure_axis') or '').strip()
    dominant_blocker = str(summary.get('primary_blocker') or no_trade_reason_code or row.get('primary_failure_axis') or commander_no_trade_reason_code or '').strip()
    confidence_score = facade._to_float(condition_scores.get('confidence_score'))
    confidence_threshold = facade._to_float(condition_scores.get('confidence_threshold'))
    confidence_gap = max(0.0, confidence_threshold - confidence_score) if confidence_threshold > 0.0 else 0.0
    confidence_near_miss = bool(decision_outcome not in {'BUY', 'SELL'} and confidence_threshold > 0.0 and (0.0 < confidence_gap <= 0.005))
    entry_quality_score = facade._to_float(condition_scores.get('entry_quality_score') if condition_scores.get('entry_quality_score') not in (None, '') else row.get('entry_quality_score'))
    reclaim_distance = row.get('reclaim_distance_to_ready')
    volume_distance = row.get('volume_distance_to_ready')
    breakout_distance = row.get('breakout_distance_to_ready')
    reclaim_gap = max(0.0, -facade._to_float(reclaim_distance)) if reclaim_distance not in (None, '') else None
    volume_gap = max(0.0, -facade._to_float(volume_distance)) if volume_distance not in (None, '') else None
    breakout_gap = max(0.0, -facade._to_float(breakout_distance)) if breakout_distance not in (None, '') else None
    transition_readiness_score = facade._to_float(row.get('transition_readiness_score'))
    blocker_metrics = {'reclaim_margin': reclaim_distance, 'breakout_margin': breakout_distance, 'volume_margin': volume_distance, 'confidence_margin': round(confidence_score - confidence_threshold, 4) if confidence_threshold > 0.0 else None, 'confidence_gap': round(confidence_gap, 4) if confidence_threshold > 0.0 else None, 'confidence_near_miss': confidence_near_miss, 'transition_readiness_score': transition_readiness_score if transition_readiness_score > 0.0 else None, 'entry_quality_score': round(entry_quality_score, 4) if entry_quality_score > 0.0 else None}
    blocker_metrics = {k: v for k, v in blocker_metrics.items() if v not in (None, '')}
    distance_to_ready = {'reclaim_score_gap': round(reclaim_gap, 4) if reclaim_gap is not None else None, 'breakout_gap': round(breakout_gap, 4) if breakout_gap is not None else None, 'volume_gap': round(volume_gap, 4) if volume_gap is not None else None, 'confidence_gap': round(confidence_gap, 4) if confidence_threshold > 0.0 else None}
    distance_to_ready = {k: v for k, v in distance_to_ready.items() if v is not None}
    near_ready_flag = bool(decision_outcome not in {'BUY', 'SELL'} and (transition_readiness_score >= 0.75 or (reclaim_gap is not None and reclaim_gap <= 0.03) or (breakout_gap is not None and breakout_gap <= 0.01) or (volume_gap is not None and volume_gap <= 0.2) or (confidence_threshold > 0.0 and confidence_gap <= 0.05)))
    near_ready_reasons = facade._dedupe_non_empty(['transition_readiness_near_ready' if transition_readiness_score >= 0.75 else '', 'reclaim_near_ready' if reclaim_gap is not None and reclaim_gap <= 0.03 else '', 'breakout_near_ready' if breakout_gap is not None and breakout_gap <= 0.01 else '', 'volume_near_ready' if volume_gap is not None and volume_gap <= 0.2 else '', 'confidence_threshold_near_miss' if confidence_near_miss else ''], limit=6)
    required_checks_failed = facade._dedupe_non_empty(list(summary.get('top_failed_required_checks') or []) or facade._extract_failed_names(check_status.get('required'), statuses=('fail',)), limit=6)
    preferred_checks_failed = facade._dedupe_non_empty(list(summary.get('top_failed_preferred_checks') or []) or facade._extract_failed_names(check_status.get('preferred'), statuses=('fail',)), limit=6)
    relaxable_checks_failed = facade._dedupe_non_empty(list(summary.get('top_relaxable_gaps') or []) or facade._extract_failed_names(check_status.get('relaxable'), statuses=('fail',)), limit=6)
    evidence_snapshot = {'entry_style': str(policy_interpretation.get('entry_style') or ''), 'entry_condition_path': str(row.get('entry_condition_path') or ''), 'paths_passed': facade._dedupe_non_empty(list(row.get('entry_condition_paths_passed') or []), limit=4), 'policy_alignment_state': str(summary.get('alignment_state') or ''), 'primary_failure_axis': str(row.get('primary_failure_axis') or ''), 'transition_readiness_score': round(transition_readiness_score, 4) if transition_readiness_score > 0.0 else None, 'entry_quality_score': round(entry_quality_score, 4) if entry_quality_score > 0.0 else None, 'entry_quality_tier': str(condition_scores.get('entry_quality_tier') or row.get('entry_quality_tier') or '').strip(), 'policy_aware_gating_applied': bool(policy_gating.get('applied')), 'chart_structure_hint_applied': bool(chart_hint.get('applied')), 'confidence_score': round(confidence_score, 4) if confidence_score > 0.0 else None, 'confidence_threshold': round(confidence_threshold, 4) if confidence_threshold > 0.0 else None, 'confidence_gap': round(confidence_gap, 4) if confidence_threshold > 0.0 else None, 'confidence_near_miss': confidence_near_miss}
    evidence_snapshot = {k: v for k, v in evidence_snapshot.items() if v not in (None, '', [])}
    return {'schema_version': 'monitor_no_trade_surface.v1', 'decision_outcome': decision_outcome, 'pre_intent_decision': pre_intent_decision, 'no_trade_stage': no_trade_stage, 'guard_intervened': bool(guard_blocked), 'guard_reason': str(guard_reason or '').strip(), 'no_trade_reason_code': no_trade_reason_code, 'no_trade_reason_summary': facade._humanize_reason_code(no_trade_reason_code or dominant_blocker), 'dominant_blocker': dominant_blocker, 'blocker_family': facade._blocker_family(code=str(dominant_blocker or no_trade_reason_code), primary_failure_axis=str(row.get('primary_failure_axis') or ''), guard_blocked=bool(guard_blocked)), 'blocker_metrics': blocker_metrics, 'distance_to_ready': distance_to_ready, 'near_ready_flag': near_ready_flag, 'near_ready_reasons': near_ready_reasons, 'confidence_near_miss': confidence_near_miss, 'required_checks_failed': required_checks_failed, 'preferred_checks_failed': preferred_checks_failed, 'relaxable_checks_failed': relaxable_checks_failed, 'evidence_snapshot': evidence_snapshot}
