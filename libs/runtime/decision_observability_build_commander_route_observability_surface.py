from __future__ import annotations

def build_commander_route_observability_surface(*, selected_route: str, route_reason: str, commander_decision: facade.Mapping[str, facade.Any] | None, runtime_fast_path: facade.Mapping[str, facade.Any] | None, resilience: facade.Mapping[str, facade.Any] | None, runtime_status: facade.Any, runtime_transition: facade.Any, facade: facade.Any) -> facade.Dict[str, facade.Any]:
    decision = dict(commander_decision or {}) if isinstance(commander_decision, facade.Mapping) else {}
    fast_path = dict(runtime_fast_path or {}) if isinstance(runtime_fast_path, facade.Mapping) else {}
    resilience_row = dict(resilience or {}) if isinstance(resilience, facade.Mapping) else {}
    strategist_invocation = str(decision.get('strategist_invocation') or '').strip().upper()
    cache_hit = bool(selected_route == 'cached_strategist' or fast_path.get('cache_age_sec'))
    if strategist_invocation in {'RUN', 'RUN_REFRESH'}:
        strategist_call_decision = 'call'
    elif strategist_invocation == 'SKIP' or cache_hit or selected_route == 'monitor_only':
        strategist_call_decision = 'skip'
    else:
        strategist_call_decision = 'observe'
    if cache_hit:
        strategy_generation_mode = 'cached'
    elif bool(decision.get('strategist_fallback_used') or decision.get('policy_fallback_used')):
        strategy_generation_mode = 'fallback'
    elif strategist_call_decision == 'call':
        strategy_generation_mode = 'live_llm'
    else:
        strategy_generation_mode = 'default_safe'
    applied_policy = dict(decision.get('applied_policy') or {}) if isinstance(decision.get('applied_policy'), facade.Mapping) else {}
    applied_policy_id = facade._clip(applied_policy.get('policy_id') or applied_policy.get('id') or decision.get('policy_source'), max_len=120)
    route_reason_text = facade._clip(route_reason or decision.get('decision_summary'), max_len=220)
    return {'schema_version': 'commander_route_observability.v1', 'route_selected': str(selected_route or ''), 'route_reason': route_reason_text, 'strategist_call_decision': strategist_call_decision, 'strategist_call_reason': facade._clip(decision.get('strategist_refresh_reason') or route_reason_text if strategist_call_decision == 'call' else '', max_len=180), 'strategist_skip_reason': facade._clip(decision.get('strategist_cache_preference_reason') or fast_path.get('reason') or route_reason_text if strategist_call_decision == 'skip' else '', max_len=180), 'policy_refresh_reason': facade._clip(decision.get('strategist_refresh_reason'), max_len=180), 'cache_hit': cache_hit, 'cache_age_sec': fast_path.get('cache_age_sec'), 'applied_policy_source': facade._clip(decision.get('policy_source'), max_len=120), 'applied_policy_id': applied_policy_id, 'monitor_only_reason': route_reason_text if str(selected_route or '') == 'monitor_only' else '', 'full_cycle_reason': route_reason_text if str(selected_route or '') == 'full_cycle' else '', 'resilience_state': {'runtime_status': str(runtime_status or ''), 'runtime_transition': str(runtime_transition or ''), 'incident_count': facade._to_int(resilience_row.get('incident_count')), 'degrade_mode': bool(resilience_row.get('degrade_mode')), 'cooldown_until_epoch': facade._to_int(resilience_row.get('cooldown_until_epoch')), 'last_error_type': facade._clip(resilience_row.get('last_error_type'), max_len=80)}, 'intervention_reason': facade._clip(runtime_transition or resilience_row.get('degrade_reason') or route_reason_text, max_len=180), 'strategy_generation_mode': strategy_generation_mode}
