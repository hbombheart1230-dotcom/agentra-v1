from __future__ import annotations

def build_scanner_monitor_handoff_surface(*, selected: facade.Mapping[str, facade.Any] | None, ranked_candidates: facade.Sequence[facade.Mapping[str, facade.Any]] | None, scanner_output: facade.Mapping[str, facade.Any] | None, final_decision: facade.Any, no_trade_surface: facade.Mapping[str, facade.Any] | None, entry_info: facade.Mapping[str, facade.Any] | None=None, facade: facade.Any) -> facade.Dict[str, facade.Any]:
    selected_row = dict(selected or {}) if isinstance(selected, facade.Mapping) else {}
    scanner_row = dict(scanner_output or {}) if isinstance(scanner_output, facade.Mapping) else {}
    no_trade = dict(no_trade_surface or {}) if isinstance(no_trade_surface, facade.Mapping) else {}
    entry_row = dict(entry_info or {}) if isinstance(entry_info, facade.Mapping) else {}
    selected_symbol = facade.normalize_symbol(selected_row.get('symbol') or scanner_row.get('scanner_selected_symbol') or scanner_row.get('top_stock') or '')
    selected_score_total = facade._to_float(selected_row.get('score_total') if selected_row.get('score_total') not in (None, '') else selected_row.get('score'))
    selected_score_breakdown = dict(selected_row.get('score_breakdown') or {}) if isinstance(selected_row.get('score_breakdown'), facade.Mapping) else {}
    top_candidates: facade.List[facade.Dict[str, facade.Any]] = []
    selected_rank = 0
    for rank, row in enumerate(list(ranked_candidates or [])[:3], start=1):
        if not isinstance(row, facade.Mapping):
            continue
        symbol = facade.normalize_symbol(row.get('symbol') or '')
        score_total = facade._to_float(row.get('score_total') if row.get('score_total') not in (None, '') else row.get('score'))
        score_breakdown = dict(row.get('score_breakdown') or {}) if isinstance(row.get('score_breakdown'), facade.Mapping) else {}
        top_candidates.append({'rank': rank, 'symbol': symbol, 'score_total': score_total, 'score_breakdown': score_breakdown})
        if symbol and symbol == selected_symbol:
            selected_rank = rank
    if selected_rank <= 0 and selected_symbol:
        selected_rank = facade._to_int(scanner_row.get('selected_rank')) or 1
    final_outcome = facade._normalize_decision_outcome(final_decision, fallback='WAIT')
    no_trade_reason_code = str(no_trade.get('no_trade_reason_code') or '').strip()
    expected_monitor_block_reason = facade._clip(scanner_row.get('expected_monitor_block_reason') or selected_row.get('expected_monitor_block_reason'), max_len=120)
    dominant_block_reason = facade._clip(scanner_row.get('dominant_block_reason') or selected_row.get('dominant_block_reason'), max_len=120)
    scanner_vs_monitor_alignment = 'unknown'
    if final_outcome == 'BUY':
        scanner_vs_monitor_alignment = 'aligned'
    elif not selected_symbol:
        scanner_vs_monitor_alignment = 'unknown'
    elif str(no_trade.get('no_trade_stage') or '') == 'guard_block':
        scanner_vs_monitor_alignment = 'guard_block'
    elif expected_monitor_block_reason and no_trade_reason_code and (expected_monitor_block_reason == no_trade_reason_code):
        scanner_vs_monitor_alignment = 'expected_mismatch'
    elif dominant_block_reason and no_trade_reason_code and (dominant_block_reason == no_trade_reason_code or dominant_block_reason in no_trade_reason_code or no_trade_reason_code in dominant_block_reason):
        scanner_vs_monitor_alignment = 'partial_mismatch'
    elif no_trade_reason_code:
        scanner_vs_monitor_alignment = 'mismatch'
    handoff_trace = facade._dedupe_non_empty([f'scanner_top_pick:{selected_symbol}' if selected_symbol else '', f'scanner_rank:{selected_rank}' if selected_rank > 0 else '', f'monitor_outcome:{final_outcome}', f'monitor_reason:{no_trade_reason_code}' if no_trade_reason_code else '', f'expected_monitor_block_reason:{expected_monitor_block_reason}' if expected_monitor_block_reason else ''], limit=6)
    return {'schema_version': 'scanner_monitor_handoff.v1', 'scanner_selected_symbol': selected_symbol, 'scanner_rank': int(selected_rank), 'scanner_score_total': selected_score_total, 'scanner_score_breakdown': selected_score_breakdown, 'scanner_top_candidates': top_candidates, 'scanner_vs_monitor_alignment': scanner_vs_monitor_alignment, 'monitor_rejection_after_top_pick': bool(selected_symbol and final_outcome not in {'BUY', 'SELL'}), 'monitor_rejection_reason_code': no_trade_reason_code, 'monitor_rejection_reason_summary': str(no_trade.get('no_trade_reason_summary') or ''), 'handoff_trace': handoff_trace, 'entry_style': str((entry_row.get('policy_interpretation') or {}).get('entry_style') if isinstance(entry_row.get('policy_interpretation'), facade.Mapping) else '')}
