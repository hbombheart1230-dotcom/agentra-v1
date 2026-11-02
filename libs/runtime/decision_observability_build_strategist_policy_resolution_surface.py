from __future__ import annotations

def build_strategist_policy_resolution_surface(*, strategist_output: facade.Mapping[str, facade.Any] | None, strategist_llm: facade.Mapping[str, facade.Any] | None, commander_context: facade.Mapping[str, facade.Any] | None=None, facade: facade.Any) -> facade.Dict[str, facade.Any]:
    output = dict(strategist_output or {}) if isinstance(strategist_output, facade.Mapping) else {}
    llm = dict(strategist_llm or {}) if isinstance(strategist_llm, facade.Mapping) else {}
    context = dict(commander_context or {}) if isinstance(commander_context, facade.Mapping) else {}
    llm_status = str(llm.get('status') or llm.get('llm_status') or output.get('llm_frame_status') or '').strip().lower()
    llm_attempted = bool(llm_status not in {'', 'disabled'} or facade._to_int(llm.get('attempts')) > 0 or str(llm.get('prompt_ref') or '').strip() or str(llm.get('response_ref') or '').strip())
    llm_blocked = bool(llm.get('blocked') or output.get('llm_frame_blocked'))
    llm_ok = bool(llm_attempted and (not llm_blocked) and (llm_status in {'ok', 'success', 'applied'}))
    llm_error_message_short = facade._clip(llm.get('blocked_reason') or llm.get('reason') or llm.get('error') or output.get('llm_frame_blocked_reason'), max_len=180)
    fallback_used = bool(output.get('policy_fallback_used') or output.get('strategist_fallback_used') or llm_status in {'fallback', 'error', 'blocked'} or llm_blocked)
    reused_cached_strategy = bool(context.get('strategist_cache_preferred') or str(context.get('strategist_invocation') or '').strip().upper() == 'SKIP')
    if reused_cached_strategy:
        strategy_generation_mode = 'cached'
    elif fallback_used:
        strategy_generation_mode = 'fallback'
    elif llm_attempted and llm_ok:
        strategy_generation_mode = 'live_llm'
    else:
        strategy_generation_mode = 'default_safe'
    fallback_source = ''
    if reused_cached_strategy:
        fallback_source = 'cached_strategy'
    elif fallback_used:
        fallback_source = facade._clip(output.get('policy_source') or output.get('policy_fallback_reason') or 'default_safe_policy', max_len=120)
    effective_schema_version = ''
    monitor_entry_policy = dict(output.get('monitor_entry_policy') or {}) if isinstance(output.get('monitor_entry_policy'), facade.Mapping) else {}
    if str(monitor_entry_policy.get('schema_version') or '').strip():
        effective_schema_version = str(monitor_entry_policy.get('schema_version') or '').strip()
    prompt_ref = str(llm.get('prompt_ref') or '').strip()
    prompt_version = facade.Path(prompt_ref).name if prompt_ref else ''
    policy_staleness = context.get('strategist_refresh_context', {}).get('cache_age_sec') if isinstance(context.get('strategist_refresh_context'), facade.Mapping) else None
    policy_id = facade._clip(monitor_entry_policy.get('policy_id') or output.get('policy_source') or context.get('policy_source'), max_len=120)
    return {'schema_version': 'strategist_policy_resolution.v1', 'llm_attempted': llm_attempted, 'llm_ok': llm_ok, 'llm_error_type': facade._extract_error_type(llm_error_message_short), 'llm_error_message_short': llm_error_message_short, 'latency_ms': facade._to_int(llm.get('latency_ms')), 'fallback_used': fallback_used, 'fallback_source': fallback_source, 'fallback_policy_id': policy_id if fallback_used else '', 'effective_policy_source': facade._clip(output.get('policy_source'), max_len=120), 'effective_prompt_version': prompt_version, 'effective_schema_version': effective_schema_version, 'policy_staleness': policy_staleness, 'reused_cached_strategy': reused_cached_strategy, 'strategy_generation_mode': strategy_generation_mode}
