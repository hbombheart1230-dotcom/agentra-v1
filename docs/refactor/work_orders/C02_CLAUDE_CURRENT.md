# C02 — Claude A | A-20261101-06 | FAST-3 EIGHT NEW VERIFIED SOURCE BODY MOVEs

**SINGLE ENTRY ONLY.** At start pin integration HEAD, C02 blob, A owner HEAD, ORDER_ID. Execute A1–A8 independently in order; continue after an item BLOCKED. Read this C02 plus named source/target/test code ONLY; no D00, RF, queue, C03, CURRENT or HANDOFF. Prior pinned order may finish without retroactive cancellation.

**REMOTE_DONE:** old C02 blob `68deb4acbc2efbda94a70e68738498fc89afd92f` A-20261101-05 8/8 already remotely implemented at A HEAD `9bb820c710c12ada9fdb06deb680252fbcc54b98` (#11 6548637687), normal unittest 8/8 exit0; integration accepted exact source at `faded947e62e7fc4dd153fbe94d3a72d92b27c02` (#36 6548799065). Do not reimplement/retest same SHA. New eight source bodies below were inspected on current A/integration and are still executable (not delegated).

**OWNER/SAFETY:** RF-035 CLAUDE_A, exclusive reporting/Q8 read-model scope. Only edit three named SOURCE files below, eight new `libs/reporting/*_projection.py` Owners and NEW `tests/test_p15_rf035_20261101_06h_owners.py` on A branch. No D00/RF/STATUS/queue/other C-docs, B branch, frozen CI, live/operational state, Broker/Guard/Step5C/UEF/RunLab, real network/order or live promotion. All output is evaluation/report data, NOT permission to execute trade or promotion. Never force push.

**IMPLEMENTATION:** For each item preserve exact SOURCE signature/annotations and replace executable body with ONLY thin delegation. New Owner has original parameters plus keyword-only `facade` for every helper/global listed; resolve each through `facade.<name>` at call time to retain monkeypatch seams, not import SOURCE from Owner. Preserve original output order, exceptions, alias/copy, defaults, and direct caller semantics. Use unique Owner aliases; `q8_evaluation_contract.py` needs `import sys` for facade. No duplicate computation in SOURCE. When moving nested `score` or comprehension, move whole body, not a stub.

**TARGETED G2:** Before editing capture golden from pinned original blobs. Create eight distinct unittest methods `test_a1_*`–`test_a8_*` in NEW file. Compare golden-original, SOURCE wrapper, direct Owner on positive/negative/exception, call-time facade monkeypatch; assert AST SOURCE no old calculation BODY. Patch runtime builders in A7 to in-memory fakes; never call real trade/effect. Command `python -m unittest tests/test_p15_rf035_20261101_06h_owners.py -v` normal exit0; optionally related scoped tests, not full/-O/full peer compulsory. Commit ONLY allowed code/test on A branch, normal push, re-fetch owner branch HEAD and SOURCE/TARGET/test blobs; report exact per-item status/normal exit/START_KST/END_KST measured to #11. Git auth failure=PUSH_BLOCKED, not code failure; continue remaining safe items. On SOURCE divergence or safety concern mark item BLOCKED with exact SHA and continue other verified items. No self-selection.

## A1 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_mismatch_examples` @ L60 | CURRENT_BLOB `e60c4c541b23e8073eef2f23224c42aa4c6867c3`
**NEW TARGET (404 A/integration):** `libs/reporting/quant_tactic_eval_mismatch_examples_projection.py::_mismatch_examples`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _mismatch_examples(rows: List[Dict[str, Any]], *, limit: int = 4) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        count = _int(row.get("quant_tactic_mismatch_count"))
        if count <= 0:
            continue
        out.append(
            {
                "trade_id": _text(row.get("trade_id")),
                "symbol": _text(row.get("symbol")),
                "tactic_id": _text(row.get("quant_tactic_id")),
                "mismatch_count": count,
            }
        )
        if len(out) >= limit:
            break
    return out
```
**SOURCE thin wrapper:** retain original signature; import `libs.reporting.quant_tactic_eval_mismatch_examples_projection` as `_a1_owner`, sole delegation `return _a1_owner._mismatch_examples(rows, limit=limit, facade=sys.modules[__name__])`. **CALL-TIME GLOBALS/PATCH:** _int,_text; in Owner replace these references with `facade.<name>` (including runtime builders; no live effect).
**NORMAL TARGETED `test_a1_mismatch_examples`:** [{'trade_id':'T','symbol':'S','quant_tactic_id':'Q','quant_tactic_mismatch_count':2}] -> one example with mismatch_count=2; count 0 -> []; limit=0 original parity. Golden==wrapper==direct Owner, AST original calculation removed. **BLOCKED→NEXT:** log exact error, continue A2.

## A2 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::build_quant_tactic_evaluation` @ L79 | CURRENT_BLOB `e60c4c541b23e8073eef2f23224c42aa4c6867c3`
**NEW TARGET (404 A/integration):** `libs/reporting/quant_tactic_eval_builder_projection.py::build_quant_tactic_evaluation`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def build_quant_tactic_evaluation(rows: Iterable[Mapping[str, Any]]) -> Dict[str, Any]:
    all_evaluation_rows = _evaluation_rows(rows)
    invalid_examples = _invalid_sample_examples(all_evaluation_rows)
    evaluation_rows = _valid_evaluation_rows(all_evaluation_rows)
    field_gaps = _field_gap_rows(evaluation_rows)
    gap_fields = [row["field"] for row in field_gaps if not bool(row.get("coverage_ok"))]
    mismatch_count = sum(_int(row.get("quant_tactic_mismatch_count")) for row in evaluation_rows)
    mismatch_trade_count = sum(1 for row in evaluation_rows if _int(row.get("quant_tactic_mismatch_count")) > 0)
    exit_drift_count = sum(_int(row.get("quant_exit_tactic_drift_count")) for row in evaluation_rows)
    exit_drift_trade_count = sum(1 for row in evaluation_rows if _int(row.get("quant_exit_tactic_drift_count")) > 0)
    source_counts = Counter(_text(row.get("quant_tactic_id_source")) for row in evaluation_rows)
    source_counts.pop("", None)

    if invalid_examples:
        status = "hold_invalid_truth_samples"
    elif len(evaluation_rows) < _MIN_REVIEW_SAMPLE:
        status = "hold_sample_insufficient"
    elif mismatch_trade_count > 0:
        status = "hold_tactic_id_mismatch"
    elif gap_fields:
        status = "hold_field_gaps"
    elif len(evaluation_rows) < _TARGET_PROMOTION_SAMPLE:
        status = "review_sample_building"
    else:
        status = "promotion_review_ready"

    return {
        "schema_version": "quant_tactic_evaluation.v1",
        "behavior_effect": "evaluation_only",
        "status": status,
        "live_trade_readiness": status,
        "promotion_action": "hold" if status.startswith("hold_") else "manual_review",
        "closed_or_realized_sample_count": len(evaluation_rows),
        "raw_closed_or_realized_sample_count": len(all_evaluation_rows),
        "invalid_sample_count": max(0, len(all_evaluation_rows) - len(evaluation_rows)),
        "invalid_sample_examples": invalid_examples,
        "review_sample_floor": _MIN_REVIEW_SAMPLE,
        "promotion_sample_target": _TARGET_PROMOTION_SAMPLE,
        "required_fields": list(_REQUIRED_FIELDS),
        "field_coverage_floor": _FIELD_COVERAGE_FLOOR,
        "field_gaps": field_gaps,
        "missing_required_fields": gap_fields,
        "tactic_id_mismatch_trade_count": mismatch_trade_count,
        "tactic_id_mismatch_count": mismatch_count,
        "tactic_id_mismatch_examples": _mismatch_examples(evaluation_rows),
        "exit_tactic_drift_trade_count": exit_drift_trade_count,
        "exit_tactic_drift_count": exit_drift_count,
        "tactic_id_source_counts": dict(source_counts),
    }
```
**SOURCE thin wrapper:** retain original signature; import `libs.reporting.quant_tactic_eval_builder_projection` as `_a2_owner`, sole delegation `return _a2_owner.build_quant_tactic_evaluation(rows, facade=sys.modules[__name__])`. **CALL-TIME GLOBALS/PATCH:** _evaluation_rows,_invalid_sample_examples,_valid_evaluation_rows,_field_gap_rows,_int,_text,_mismatch_examples,Counter,_MIN_REVIEW_SAMPLE,_TARGET_PROMOTION_SAMPLE,_REQUIRED_FIELDS,_FIELD_COVERAGE_FLOOR; in Owner replace these references with `facade.<name>` (including runtime builders; no live effect).
**NORMAL TARGETED `test_a2_build_quant_tactic_evaluation`:** [] -> status='hold_sample_insufficient', closed_or_realized_sample_count=0; invalid closed row -> hold_invalid_truth_samples; no promotion effect. Golden==wrapper==direct Owner, AST original calculation removed. **BLOCKED→NEXT:** log exact error, continue A3.

## A3 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::render_quant_tactic_evaluation_lines` @ L130 | CURRENT_BLOB `e60c4c541b23e8073eef2f23224c42aa4c6867c3`
**NEW TARGET (404 A/integration):** `libs/reporting/quant_tactic_eval_render_projection.py::render_quant_tactic_evaluation_lines`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def render_quant_tactic_evaluation_lines(payload: Mapping[str, Any] | None) -> List[str]:
    evaluation = dict(payload or {})
    if not evaluation:
        return []
    missing = list(evaluation.get("missing_required_fields") or [])
    missing_text = ", ".join(str(field) for field in missing) if missing else "none"
    source_counts = dict(evaluation.get("tactic_id_source_counts") or {})
    source_text = ", ".join(f"{key}={value}" for key, value in source_counts.items()) if source_counts else "none"
    lines = [
        "- Quant Q8 readiness: "
        f"`{evaluation.get('status') or 'not_available'}` / action `{evaluation.get('promotion_action') or 'hold'}` "
        f"/ sample {evaluation.get('closed_or_realized_sample_count') or 0}"
        f" valid, invalid {evaluation.get('invalid_sample_count') or 0}"
        f"/{evaluation.get('promotion_sample_target') or _TARGET_PROMOTION_SAMPLE}",
        "- Quant Q8 live-trade readiness: "
        f"`{evaluation.get('live_trade_readiness') or evaluation.get('status') or 'not_available'}` "
        "(actual closed-trade performance only)",
        f"- Quant Q8 missing fields: {missing_text}",
        "- Quant Q8 tactic ID integrity: "
        f"mismatch trades {evaluation.get('tactic_id_mismatch_trade_count') or 0}, "
        f"mismatch rows {evaluation.get('tactic_id_mismatch_count') or 0}, "
        f"exit drift trades {evaluation.get('exit_tactic_drift_trade_count') or 0}, "
        f"exit drift rows {evaluation.get('exit_tactic_drift_count') or 0}, "
        f"sources {source_text}",
    ]
    invalid_examples = [row for row in list(evaluation.get("invalid_sample_examples") or []) if isinstance(row, Mapping)]
    if invalid_examples:
        rendered = []
        for row in invalid_examples[:5]:
            trade_id = _text(row.get("trade_id")) or "-"
            symbol = _text(row.get("symbol")) or "-"
            reason = _text(row.get("reason")) or "unknown"
            rendered.append(f"{trade_id}/{symbol}:{reason}")
        lines.append(f"- Quant Q8 invalid samples: {', '.join(rendered)}")
    mismatch_examples = [row for row in list(evaluation.get("tactic_id_mismatch_examples") or []) if isinstance(row, Mapping)]
    if mismatch_examples:
        rendered = []
        for row in mismatch_examples[:4]:
            trade_id = _text(row.get("trade_id")) or "-"
            symbol = _text(row.get("symbol")) or "-"
            count = _int(row.get("mismatch_count"))
            rendered.append(f"{trade_id}/{symbol}:{count}")
        lines.append(f"- Quant Q8 tactic mismatch examples: {', '.join(rendered)}")
    return lines
```
**SOURCE thin wrapper:** retain original signature; import `libs.reporting.quant_tactic_eval_render_projection` as `_a3_owner`, sole delegation `return _a3_owner.render_quant_tactic_evaluation_lines(payload, facade=sys.modules[__name__])`. **CALL-TIME GLOBALS/PATCH:** Mapping,_text,_int,_TARGET_PROMOTION_SAMPLE; in Owner replace these references with `facade.<name>` (including runtime builders; no live effect).
**NORMAL TARGETED `test_a3_render_quant_tactic_evaluation_lines`:** {} -> []; {'status':'hold_sample_insufficient'} -> nonempty Quant Q8 readiness line. Golden==wrapper==direct Owner, AST original calculation removed. **BLOCKED→NEXT:** log exact error, continue A4.

## A4 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_report.py::_selected_candidate_row` @ L84 | CURRENT_BLOB `3cf76659bc4970c9f262405bbf829327203b7474`
**NEW TARGET (404 A/integration):** `libs/reporting/quant_tactic_selected_candidate_projection.py::_selected_candidate_row`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _selected_candidate_row(report: Mapping[str, Any], symbol: str) -> Dict[str, Any]:
    target = str(symbol or "").strip()
    if not target:
        return {}
    candidates: List[Dict[str, Any]] = []
    for item in _nested_dicts(report):
        if _candidate_symbol(item) != target:
            continue
        if any(
            key in item
            for key in (
                "quant_factor_snapshot",
                "tactic_suitability",
                "scanner_chart_fit_score",
                "scanner_chart_fit_components",
                "score_total",
                "confidence",
            )
        ):
            candidates.append(dict(item))
    if not candidates:
        return {}

    def score(row: Mapping[str, Any]) -> tuple[int, int]:
        has_quant = 1 if _mapping(row.get("quant_factor_snapshot")) else 0
        has_suitability = 1 if _mapping(row.get("tactic_suitability")) else 0
        has_chart = 1 if row.get("scanner_chart_fit_score") not in (None, "") else 0
        # Prefer final/fallback candidates over top-pick snapshots when labels exist.
        final_hint = 1 if str(row.get("final_selected_symbol") or row.get("selected_symbol") or row.get("entry_final_symbol") or "") == target else 0
        return (has_quant + has_suitability + has_chart + final_hint, len(row))

    candidates.sort(key=score, reverse=True)
    return candidates[0]
```
**SOURCE thin wrapper:** retain original signature; import `libs.reporting.quant_tactic_selected_candidate_projection` as `_a4_owner`, sole delegation `return _a4_owner._selected_candidate_row(report, symbol, facade=sys.modules[__name__])`. **CALL-TIME GLOBALS/PATCH:** _nested_dicts,_candidate_symbol,_mapping; in Owner replace these references with `facade.<name>` (including runtime builders; no live effect).
**NORMAL TARGETED `test_a4_selected_candidate_row`:** nested matching symbol with quant_factor_snapshot -> selected candidate dict; unknown symbol -> {}. Golden==wrapper==direct Owner, AST original calculation removed. **BLOCKED→NEXT:** log exact error, continue A5.

## A5 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_report.py::_tactic_sources` @ L127 | CURRENT_BLOB `3cf76659bc4970c9f262405bbf829327203b7474`
**NEW TARGET (404 A/integration):** `libs/reporting/quant_tactic_sources_projection.py::_tactic_sources`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _tactic_sources(
    *,
    entry_decision: Mapping[str, Any],
    factor_snapshot: Mapping[str, Any],
    selected_row: Mapping[str, Any],
    tactic_suitability: Mapping[str, Any],
    exit_decision: Mapping[str, Any],
) -> List[tuple[str, str]]:
    selected_factor = _mapping(selected_row.get("quant_factor_snapshot"))
    rows = (
        ("entry_quant_decision", entry_decision.get("tactic_id")),
        ("factor_snapshot", factor_snapshot.get("tactic_id")),
        ("selected_quant_factor_snapshot", selected_factor.get("tactic_id")),
        ("selected_candidate", selected_row.get("tactical_strategy")),
        ("tactic_suitability", tactic_suitability.get("tactic_id")),
        ("exit_quant_decision", exit_decision.get("tactic_id")),
    )
    return [(source, tactic_id) for source, value in rows if (tactic_id := _tactic_value(value))]
```
**SOURCE thin wrapper:** retain original signature; import `libs.reporting.quant_tactic_sources_projection` as `_a5_owner`, sole delegation `return _a5_owner._tactic_sources(entry_decision=entry_decision, factor_snapshot=factor_snapshot, selected_row=selected_row, tactic_suitability=tactic_suitability, exit_decision=exit_decision, facade=sys.modules[__name__])`. **CALL-TIME GLOBALS/PATCH:** _mapping,_tactic_value; in Owner replace these references with `facade.<name>` (including runtime builders; no live effect).
**NORMAL TARGETED `test_a5_tactic_sources`:** entry_decision={'tactic_id':'A'}, others={} -> [('entry_quant_decision','A')]. Golden==wrapper==direct Owner, AST original calculation removed. **BLOCKED→NEXT:** log exact error, continue A6.

## A6 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_report.py::render_quant_tactic_report_lines` @ L222 | CURRENT_BLOB `3cf76659bc4970c9f262405bbf829327203b7474`
**NEW TARGET (404 A/integration):** `libs/reporting/quant_tactic_report_lines_projection.py::render_quant_tactic_report_lines`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def render_quant_tactic_report_lines(report: Mapping[str, Any] | None, *, compact: bool = False) -> List[str]:
    surface = quant_tactic_surface(report)
    if not surface:
        return []
    entry = _mapping(surface.get("entry_quant_decision"))
    exit_decision = _mapping(surface.get("exit_quant_decision"))
    factors = _mapping(surface.get("factors"))
    suitability = _mapping(surface.get("tactic_suitability"))
    lines: List[str] = []
    tactic = surface.get("tactic_id") or "-"
    playbook = surface.get("playbook") or "-"
    if compact:
        lines.append(f"* 전술 진단: `{tactic}` / 플레이북 `{playbook}`")
    else:
        lines.append(f"- 전술 ID: `{tactic}`")
        lines.append(f"- 플레이북: `{playbook}`")
    if suitability:
        lines.append(
            f"- 스캐너 전술 적합도: {suitability.get('tier') or '-'} "
            f"({_fmt(suitability.get('score'))})"
        )
    if entry:
        lines.append(
            f"- 진입 quant 판단: {_decision_label(entry.get('decision'))} "
            f"/ blocker={_reason_text(entry.get('blockers'))} "
            f"/ warning={_reason_text(entry.get('warnings'))}"
        )
        cost = _mapping(entry.get("cost_edge"))
        if cost:
            lines.append(
                f"- 비용 엣지: {'통과' if cost.get('ok') else '미통과'} "
                f"/ edge={_pct(cost.get('cost_adjusted_edge_pct'))} "
                f"/ drag={_pct(cost.get('cost_drag_pct'))}"
            )
        if bool(entry.get("commander_override_required")):
            lines.append(f"- commander override 필요 항목: {_reason_text(entry.get('override_reason_required_for'))}")
    if exit_decision:
        lines.append(
            f"- 청산 quant 판단: {_decision_label(exit_decision.get('decision'))} "
            f"/ hard_exit={'예' if exit_decision.get('hard_exit') else '아니오'} "
            f"/ confirmation_pending={'예' if exit_decision.get('confirmation_pending') else '아니오'}"
        )
        if exit_decision.get("early_exit_flag") or exit_decision.get("actual_hold_sec") not in (None, ""):
            window = _mapping(exit_decision.get("expected_hold_window"))
            lines.append(
                f"- 보유시간 비교: 실제 {_fmt(exit_decision.get('actual_hold_sec'))}초 "
                f"/ 기대 최소 {_fmt(window.get('min_sec'))}초 "
                f"/ mismatch={'예' if exit_decision.get('hold_window_mismatch') else '아니오'}"
            )
        if exit_decision.get("blockers") or exit_decision.get("warnings"):
            lines.append(
                f"- 청산 진단 사유: blocker={_reason_text(exit_decision.get('blockers'))} "
                f"/ warning={_reason_text(exit_decision.get('warnings'))}"
            )
    if not compact and factors:
        factor_bits = []
        for key in ("vwap_distance_pct", "volume_ratio", "cost_floor_state", "confidence_score", "human_chart_entry_score"):
            if factors.get(key) not in (None, ""):
                factor_bits.append(f"{key}={_fmt(factors.get(key))}")
        if factor_bits:
            lines.append("- 핵심 factor snapshot: " + ", ".join(factor_bits[:6]))
    return lines
```
**SOURCE thin wrapper:** retain original signature; import `libs.reporting.quant_tactic_report_lines_projection` as `_a6_owner`, sole delegation `return _a6_owner.render_quant_tactic_report_lines(report, compact=compact, facade=sys.modules[__name__])`. **CALL-TIME GLOBALS/PATCH:** quant_tactic_surface,_mapping,_fmt,_pct,_reason_text,_decision_label; in Owner replace these references with `facade.<name>` (including runtime builders; no live effect).
**NORMAL TARGETED `test_a6_render_quant_tactic_report_lines`:** {} -> []; patched quant_tactic_surface -> {'tactic_id':'T'} yields '- 전술 ID:' line; compact=True yields '* 전술 진단:'. Golden==wrapper==direct Owner, AST original calculation removed. **BLOCKED→NEXT:** log exact error, continue A7.

## A7 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_report.py::quant_tactic_surface` @ L155 | CURRENT_BLOB `3cf76659bc4970c9f262405bbf829327203b7474`
**NEW TARGET (404 A/integration):** `libs/reporting/quant_tactic_surface_projection.py::quant_tactic_surface`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def quant_tactic_surface(report: Mapping[str, Any] | None) -> Dict[str, Any]:
    root = _mapping(report)
    monitor = _monitor(root)
    visibility = _entry_visibility(root)
    symbol = _symbol(root)
    selection = _mapping(root.get("why_this_symbol_was_chosen"))
    scanner_trace = _mapping(selection.get("scanner_selection_trace"))
    selected_row = _selected_candidate_row(root, symbol)
    entry_decision = _mapping(
        monitor.get("entry_quant_decision")
        or root.get("entry_quant_decision")
        or _first_nested_mapping(root, "entry_quant_decision")
    )
    exit_decision = _mapping(monitor.get("exit_quant_decision") or root.get("exit_quant_decision"))
    factor_snapshot = _mapping(
        monitor.get("quant_factor_snapshot")
        or root.get("quant_factor_snapshot")
        or selected_row.get("quant_factor_snapshot")
    )
    factors = _mapping(factor_snapshot.get("factors"))
    tactic_suitability = _mapping(
        selection.get("tactic_suitability")
        or scanner_trace.get("tactic_suitability")
        or selected_row.get("tactic_suitability")
        or entry_decision.get("tactic_suitability")
    )
    tactic_sources = _tactic_sources(
        entry_decision=entry_decision,
        factor_snapshot=factor_snapshot,
        selected_row=selected_row,
        tactic_suitability=tactic_suitability,
        exit_decision=exit_decision,
    )
    tactic_id_source, tactic_id = tactic_sources[0] if tactic_sources else ("", "")
    playbook = str(entry_decision.get("playbook") or exit_decision.get("playbook") or factor_snapshot.get("playbook") or _playbook(root)).strip()
    if not tactic_suitability and selected_row:
        tactic_suitability = score_candidate_tactic_suitability(selected_row, tactic_id=tactic_id, playbook=playbook)
    if not entry_decision:
        entry_info = _entry_info_from_visibility(visibility, monitor)
        if entry_info or selected_row or factor_snapshot:
            entry_decision = build_entry_quant_decision(
                entry_info,
                selected=selected_row,
                factor_snapshot=factor_snapshot,
                state=root,
                tactic_id=tactic_id,
                playbook=playbook,
            )
    scanner_chart_fit = _mapping(selection.get("scanner_chart_fit")) or _mapping(scanner_trace.get("scanner_chart_fit")) or _scanner_chart_fit_from_row(selected_row)
    if not any((entry_decision, exit_decision, factor_snapshot, tactic_suitability, tactic_id, scanner_chart_fit)):
        return {}
    return {
        "schema_version": "quant_tactic_report_surface.v1",
        "tactic_id": tactic_id,
        "tactic_id_source": tactic_id_source,
        "tactic_id_mismatches": _tactic_mismatches(tactic_sources, tactic_id),
        "exit_tactic_drifts": _exit_tactic_drifts(tactic_sources, tactic_id),
        "playbook": playbook,
        "entry_quant_decision": entry_decision,
        "exit_quant_decision": exit_decision,
        "factor_snapshot": factor_snapshot,
        "factors": factors,
        "tactic_suitability": tactic_suitability,
        "scanner_chart_fit": scanner_chart_fit,
    }
```
**SOURCE thin wrapper:** retain original signature; import `libs.reporting.quant_tactic_surface_projection` as `_a7_owner`, sole delegation `return _a7_owner.quant_tactic_surface(report, facade=sys.modules[__name__])`. **CALL-TIME GLOBALS/PATCH:** _mapping,_monitor,_entry_visibility,_symbol,_selected_candidate_row,_first_nested_mapping,_tactic_sources,_playbook,_entry_info_from_visibility,_scanner_chart_fit_from_row,_tactic_mismatches,_exit_tactic_drifts,score_candidate_tactic_suitability,build_entry_quant_decision; in Owner replace these references with `facade.<name>` (including runtime builders; no live effect).
**NORMAL TARGETED `test_a7_quant_tactic_surface`:** {} -> {}; fake report with entry_quant_decision={'tactic_id':'T','playbook':'P'} and fake no-effect runtime helpers -> surface.tactic_id='T', schema_version='quant_tactic_report_surface.v1'. Golden==wrapper==direct Owner, AST original calculation removed. **BLOCKED→NEXT:** log exact error, continue A8.

## A8 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::candidate_day` @ L32 | CURRENT_BLOB `f6b08711f965df8e8f27d42f90b4213db82e27a8`
**NEW TARGET (404 A/integration):** `libs/reporting/q8_candidate_day_projection.py::candidate_day`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def candidate_day(row: Mapping[str, Any]) -> str:
    base = forward_base(row)
    raw_ts = text_value(base.get("baseline_raw_ts"))
    if len(raw_ts) >= 8 and raw_ts[:8].isdigit():
        return raw_ts[:8]
    generated = text_value(row.get("_payload_generated_at") or row.get("generated_at"))
    return generated[:10].replace("-", "") if len(generated) >= 10 else ""
```
**SOURCE thin wrapper:** retain original signature; import `libs.reporting.q8_candidate_day_projection` as `_a8_owner`, sole delegation `return _a8_owner.candidate_day(row, facade=sys.modules[__name__])`. **CALL-TIME GLOBALS/PATCH:** forward_base,text_value; in Owner replace these references with `facade.<name>` (including runtime builders; no live effect).
**NORMAL TARGETED `test_a8_candidate_day`:** {'shadow_forward_base':{'baseline_raw_ts':'20260217T010000'}} -> '20260217'; {'generated_at':'2026-11-01T00:00:00Z'} -> '20261101'. Golden==wrapper==direct Owner, AST original calculation removed. **BLOCKED→NEXT:** log exact error, continue A1–A8 remaining / push.

## FUTURE RESERVE — 6/6 VERIFIED DESIGN ONLY; NOT EXECUTABLE THIS ORDER
Each distinct SOURCE BODY and blob below verified on A/integration; six unique TARGET paths absent both. RF-035 Owner exclusive. Future C03 must recheck HEAD, caller/patch seam, safety and issue new order. A must NOT execute reserves now.

### R1 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::text_value` @ L22 | BLOB `f6b08711f965df8e8f27d42f90b4213db82e27a8`
**TARGET ABSENT A/integration:** `libs/reporting/q8_text_value_projection.py::text_value`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def text_value(value: Any) -> str:
    text = str(value or "").strip()
    return "" if text.lower() in {"", "-", "none", "null", "unknown", "not_captured"} else text
```
**Future normal fake fixture:** ' none ' -> ''; 'A' -> 'A'. **Seam:** none; preserve SOURCE wrapper and use-time facade, report/Q8 data-only, no trading or live promotion.

### R2 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::forward_base` @ L27 | BLOB `f6b08711f965df8e8f27d42f90b4213db82e27a8`
**TARGET ABSENT A/integration:** `libs/reporting/q8_forward_base_projection.py::forward_base`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def forward_base(row: Mapping[str, Any]) -> Dict[str, Any]:
    base = row.get("shadow_forward_base")
    return dict(base) if isinstance(base, Mapping) else {}
```
**Future normal fake fixture:** {'shadow_forward_base':{'x':1}} -> {'x':1} copied, not aliased. **Seam:** Mapping; preserve SOURCE wrapper and use-time facade, report/Q8 data-only, no trading or live promotion.

### R3 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::canonical_dedupe_key` @ L48 | BLOB `f6b08711f965df8e8f27d42f90b4213db82e27a8`
**TARGET ABSENT A/integration:** `libs/reporting/q8_dedupe_key_projection.py::canonical_dedupe_key`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def canonical_dedupe_key(row: Mapping[str, Any]) -> tuple[str, str, int, str]:
    base = forward_base(row)
    try:
        baseline_epoch = int(float(base.get("baseline_epoch") or 0))
    except Exception:
        baseline_epoch = 0
    return (
        candidate_day(row),
        text_value(row.get("symbol")).upper(),
        baseline_epoch,
        entry_lane_subtype(row),
    )
```
**Future normal fake fixture:** fixed baseline_epoch and fake entry_lane_subtype -> (day,symbol,epoch,lane). **Seam:** forward_base,candidate_day,text_value,entry_lane_subtype; preserve SOURCE wrapper and use-time facade, report/Q8 data-only, no trading or live promotion.

### R4 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::dedupe_q8_candidates` @ L62 | BLOB `f6b08711f965df8e8f27d42f90b4213db82e27a8`
**TARGET ABSENT A/integration:** `libs/reporting/q8_dedupe_candidates_projection.py::dedupe_q8_candidates`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def dedupe_q8_candidates(rows: Sequence[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen: set[tuple[str, str, int, str]] = set()
    for row in rows:
        key = canonical_dedupe_key(row)
        if key in seen:
            continue
        seen.add(key)
        out.append(dict(row))
    return out
```
**Future normal fake fixture:** duplicate key rows -> one copied row, preserve order. **Seam:** canonical_dedupe_key; preserve SOURCE wrapper and use-time facade, report/Q8 data-only, no trading or live promotion.

### R5 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::promotion_candidate_is_repeatable` @ L74 | BLOB `f6b08711f965df8e8f27d42f90b4213db82e27a8`
**TARGET ABSENT A/integration:** `libs/reporting/q8_repeatable_projection.py::promotion_candidate_is_repeatable`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def promotion_candidate_is_repeatable(row: Mapping[str, Any]) -> bool:
    observed_count = int(row.get("observed_count") or 0)
    observed_day_count = int(row.get("observed_day_count") or 0)
    avg_return_5m = float(row.get("avg_return_5m_pct") or 0.0)
    avg_return_15m = float(row.get("avg_return_15m_pct") or 0.0)
    return (
        observed_count >= PROMOTION_CANDIDATE_MIN_OBSERVED
        and observed_day_count >= PROMOTION_CANDIDATE_MIN_DAYS
        and avg_return_5m > 0.0
        and avg_return_15m > 0.0
    )
```
**Future normal fake fixture:** 50 observations,2 days,positive 5m/15m -> True; zero return -> False. **Seam:** PROMOTION_CANDIDATE_MIN_OBSERVED,PROMOTION_CANDIDATE_MIN_DAYS; preserve SOURCE wrapper and use-time facade, report/Q8 data-only, no trading or live promotion.

### R6 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::entry_lane_subtype` @ L41 | BLOB `f6b08711f965df8e8f27d42f90b4213db82e27a8`
**TARGET ABSENT A/integration:** `libs/reporting/q8_entry_lane_projection.py::entry_lane_subtype`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def entry_lane_subtype(row: Mapping[str, Any]) -> str:
    observation = build_entry_lane_observation(row)
    lane = text_value(observation.get("primary_lane")) or "unknown"
    subtype = text_value(observation.get("subtype")) or "unknown"
    return f"{lane}:{subtype}"
```
**Future normal fake fixture:** fake build_entry_lane_observation returning primary_lane='x',subtype='y' -> 'x:y'. **Seam:** build_entry_lane_observation,text_value; preserve SOURCE wrapper and use-time facade, report/Q8 data-only, no trading or live promotion.

**COUNTS:** A-05 REMOTE_DONE=8/8; A-06 NEW_READY=8; RESERVE_VERIFIED=6. C03 document-only supply, not code G1/G2/G3 or RF DONE.