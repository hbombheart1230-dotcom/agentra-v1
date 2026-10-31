# C02 — Claude A | A-20261101-05 | FAST-3 NEW 8 VERIFIED SOURCE BODY MOVEs

**SINGLE ENTRY, NO SELF-SELECTION.** At start pin CANONICAL_HEAD (integration/p1.5), C02 blob, A remote HEAD and ORDER_ID. Read ONLY this C02 and named code/test paths; never D00/RF/queue/C03/CURRENT/HANDOFF. Execute ALL A1–A8; a blocked item must not stop other safe items. An Actor already running a previously pinned order may finish it without retroactive cancellation.

**C03 REMOTE DONE DELTA:** #11 comment 6548002115 reports previous A-20261101-04 A1–A8 actual BODY MOVEs and targeted normal 8/8 exit0, with remote A HEAD `b36a995bda540d439e0b9d0aa713604023e3b34f`, source `quant_tactic_report.py` changed to blob `3cf76659bc4970c9f262405bbf829327203b7474`. Previous C02 blob `c31908af688a76cddbb8177665f024ea5892fc0f` exhausted 8/8 REMOTE_DONE; do NOT repeat those 8 or same-SHA tests. This is a new eight-item order using `quant_tactic_evaluation.py` original blob `f11bd1e71dedb5494242fa88f3996885d1a3cef2`, identical on A and integration. All 8 new Owner TARGET paths and new test are 404 on both.

**OWNERSHIP & ISOLATION:** RF-035 CLAUDE_A, reporting-only evaluation transformations. Edit ONLY `libs/reporting/quant_tactic_evaluation.py`, eight NEW Owner files below, and NEW `tests/test_p15_rf035_20261101_05h_quant_eval_owners.py` on A `work/p15-a-reporter-pure-20261021`. Do not touch B branch, D00/RF/queue/STATUS/C04/C05, other code/tests, frozen oracle, CI, operational state, real account, Broker/Guard/Step5C/UEF/RunLab or live trade/promotion. This is evaluation *data*, not an authority to change live readiness or execute promotion. No force push.

**MOVE MECHANISM:** Capture original golden function before edit, move its complete executable calculation into unique new Owner (not duplicate), leave same SOURCE signature/annotations with only the listed `return` delegation. SOURCE currently lacks `import sys`; add `import sys` for `sys.modules[__name__]` facade calls. Use unique module aliases or local imports, avoid circular imports. Owner must NOT import SOURCE; when helper/global dependencies exist, Owner adds keyword-only `facade` and reads `facade.<name>` at invocation, preserving SOURCE monkeypatch and mutable constants. Preserve exact values, key order, copy/identity, exceptions and output.

**G2 & PUSH:** Write NEW eight-case `tests/test_p15_rf035_20261101_05h_quant_eval_owners.py` with `test_a1_text` through `test_a8_field_gap_rows`; golden-original vs wrapper vs direct Owner, positive/negative/exception, monkeypatch seams and AST SOURCE thin-wrapper/no duplicated BODY. Run `python -m py_compile libs/reporting/quant_tactic_evaluation.py` and each new Owner, then `python -m unittest tests/test_p15_rf035_20261101_05h_quant_eval_owners.py -v` normal exit0, plus directly affected existing `tests/test_quant_tactic_evaluation.py` if present. Only in-memory fake rows, no network, subprocess, runtime/main, real filesystem or broker. Commit ONLY SOURCE/new Owner/new test on A branch, normal push, re-fetch A remote HEAD and all SOURCE/Owner/test blobs. If push fails, mark PUSH_BLOCKED, continue safe items; local-only != REMOTE_DONE. Report #11 `ORDER_ID | CANONICAL_HEAD | ORDER_BLOB | A_REMOTE_BEFORE→AFTER | per-item MOVE/TEST/PUSH | NORMAL_EXIT | SOURCE/TARGET/TEST_BLOBS | FIRST_BLOCKER | NEXT | measured START/END`. -O/full peer/hosted CI not mandatory. C04 G3 and C05 RF DONE remain separate.

## A1 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_text` @ L19 | CURRENT_BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**NEW TARGET (404 actor/integration):** `libs/reporting/quant_tactic_eval_text_projection.py::_text`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY:**
```python
def _text(value: Any) -> str:
    text = str(value or "").strip()
    return "" if text.lower() in {"", "-", "none", "null", "unknown", "not_captured"} else text
```
**SOURCE thin wrapper:** keep exact signature, import `libs.reporting.quant_tactic_eval_text_projection` as `_a1_owner`, replace old body with sole `return _a1_owner._text(value)`. **CALLER/MONKEYPATCH:** pure string normalization; no facade; retain negative/error and copy semantics.
**NORMAL TARGETED `test_a1_text`:** ' X '→'X'; ' unknown '→''; None→''. Assert original-golden == wrapper == direct Owner and AST SOURCE body removed. **BLOCKED→NEXT:** log exact error, continue A2.

## A2 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_int` @ L24 | CURRENT_BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**NEW TARGET (404 actor/integration):** `libs/reporting/quant_tactic_eval_int_projection.py::_int`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY:**
```python
def _int(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except Exception:
        return int(default)
```
**SOURCE thin wrapper:** keep exact signature, import `libs.reporting.quant_tactic_eval_int_projection` as `_a2_owner`, replace old body with sole `return _a2_owner._int(value, default)`. **CALLER/MONKEYPATCH:** pure integer fallback; retain negative/error and copy semantics.
**NORMAL TARGETED `test_a2_int`:** '3.9'→3; ('bad',4)→4; invalid default exception parity. Assert original-golden == wrapper == direct Owner and AST SOURCE body removed. **BLOCKED→NEXT:** log exact error, continue A3.

## A3 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_closed_or_realized` @ L31 | CURRENT_BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**NEW TARGET (404 actor/integration):** `libs/reporting/quant_tactic_eval_closed_projection.py::_closed_or_realized`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY:**
```python
def _closed_or_realized(row: Mapping[str, Any]) -> bool:
    status = str(row.get("status") or row.get("last_status") or "").strip().lower()
    action = str(row.get("last_action") or row.get("action") or "").strip().upper()
    origin = str(row.get("trade_origin") or "").strip().lower()
    partial = status == "partial" or origin == "recovered_partial"
    return bool(
        row.get("is_closed_trade")
        or row.get("is_realized_nonclosed_exit")
        or (status == "closed" and not partial)
        or (action == "SELL" and partial)
    )
```
**SOURCE thin wrapper:** keep exact signature, import `libs.reporting.quant_tactic_eval_closed_projection` as `_a3_owner`, replace old body with sole `return _a3_owner._closed_or_realized(row)`. **CALLER/MONKEYPATCH:** report-only status classifier; no broker access; retain negative/error and copy semantics.
**NORMAL TARGETED `test_a3_closed_or_realized`:** {'status':'closed'}→True; {'status':'partial','action':'SELL'}→True; {}→False. Assert original-golden == wrapper == direct Owner and AST SOURCE body removed. **BLOCKED→NEXT:** log exact error, continue A4.

## A4 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_evaluation_rows` @ L44 | CURRENT_BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**NEW TARGET (404 actor/integration):** `libs/reporting/quant_tactic_eval_rows_projection.py::_evaluation_rows`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY:**
```python
def _evaluation_rows(rows: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [dict(row) for row in rows if isinstance(row, Mapping) and _closed_or_realized(row)]
```
**SOURCE thin wrapper:** keep exact signature, import `libs.reporting.quant_tactic_eval_rows_projection` as `_a4_owner`, replace old body with sole `return _a4_owner._evaluation_rows(rows,facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade.Mapping and facade._closed_or_realized at call time; retain negative/error and copy semantics.
**NORMAL TARGETED `test_a4_evaluation_rows`:** [{'status':'closed','trade_id':'T'},{'status':'open'}]→[{'status':'closed','trade_id':'T'}]. Assert original-golden == wrapper == direct Owner and AST SOURCE body removed. **BLOCKED→NEXT:** log exact error, continue A5.

## A5 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_invalid_sample_reason` @ L48 | CURRENT_BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**NEW TARGET (404 actor/integration):** `libs/reporting/quant_tactic_eval_invalid_reason_projection.py::_invalid_sample_reason`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY:**
```python
def _invalid_sample_reason(row: Mapping[str, Any]) -> str:
    status = _text(row.get("broker_alignment_status")).lower()
    if status and status not in {"ok"}:
        return f"broker_alignment_{status}"
    if _int(row.get("broker_alignment_missing_in_local_total")) > 0:
        return "broker_missing_in_local"
    if _int(row.get("broker_alignment_missing_in_broker_total")) > 0:
        return "broker_missing_in_broker"
    snapshot_status = _text(row.get("broker_account_snapshot_status")).lower()
    if snapshot_status and snapshot_status not in {"ok"}:
        return f"account_snapshot_{snapshot_status}"
    if _int(row.get("broker_alignment_account_snapshot_error_count")) > 0:
        return "account_snapshot_partial_errors"
    return ""
```
**SOURCE thin wrapper:** keep exact signature, import `libs.reporting.quant_tactic_eval_invalid_reason_projection` as `_a5_owner`, replace old body with sole `return _a5_owner._invalid_sample_reason(row,facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade._text/_int at call time; observation only, never broker; retain negative/error and copy semantics.
**NORMAL TARGETED `test_a5_invalid_sample_reason`:** {'broker_alignment_status':'bad'}→'broker_alignment_bad'; {'broker_alignment_missing_in_local_total':1}→'broker_missing_in_local'; {}→''. Assert original-golden == wrapper == direct Owner and AST SOURCE body removed. **BLOCKED→NEXT:** log exact error, continue A6.

## A6 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_valid_evaluation_rows` @ L64 | CURRENT_BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**NEW TARGET (404 actor/integration):** `libs/reporting/quant_tactic_eval_valid_rows_projection.py::_valid_evaluation_rows`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY:**
```python
def _valid_evaluation_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [row for row in rows if not _invalid_sample_reason(row)]
```
**SOURCE thin wrapper:** keep exact signature, import `libs.reporting.quant_tactic_eval_valid_rows_projection` as `_a6_owner`, replace old body with sole `return _a6_owner._valid_evaluation_rows(rows,facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade._invalid_sample_reason at call time; retain negative/error and copy semantics.
**NORMAL TARGETED `test_a6_valid_evaluation_rows`:** [{'broker_alignment_status':'bad'},{}]→[{}]. Assert original-golden == wrapper == direct Owner and AST SOURCE body removed. **BLOCKED→NEXT:** log exact error, continue A7.

## A7 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_invalid_sample_examples` @ L68 | CURRENT_BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**NEW TARGET (404 actor/integration):** `libs/reporting/quant_tactic_eval_invalid_examples_projection.py::_invalid_sample_examples`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY:**
```python
def _invalid_sample_examples(rows: List[Dict[str, Any]], *, limit: int = 5) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows:
        reason = _invalid_sample_reason(row)
        if not reason:
            continue
        out.append(
            {
                "trade_id": _text(row.get("trade_id")),
                "symbol": _text(row.get("symbol")),
                "reason": reason,
            }
        )
        if len(out) >= limit:
            break
    return out
```
**SOURCE thin wrapper:** keep exact signature, import `libs.reporting.quant_tactic_eval_invalid_examples_projection` as `_a7_owner`, replace old body with sole `return _a7_owner._invalid_sample_examples(rows,limit=limit,facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade._invalid_sample_reason/_text at call time; preserve limit ordering; retain negative/error and copy semantics.
**NORMAL TARGETED `test_a7_invalid_sample_examples`:** [{'trade_id':'T','symbol':'S','broker_alignment_status':'bad'}]→[{'trade_id':'T','symbol':'S','reason':'broker_alignment_bad'}]; limit=0 parity. Assert original-golden == wrapper == direct Owner and AST SOURCE body removed. **BLOCKED→NEXT:** log exact error, continue A8.

## A8 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_field_gap_rows` @ L86 | CURRENT_BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**NEW TARGET (404 actor/integration):** `libs/reporting/quant_tactic_eval_field_gaps_projection.py::_field_gap_rows`. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY:**
```python
def _field_gap_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    count = len(rows)
    out: List[Dict[str, Any]] = []
    for field in _REQUIRED_FIELDS:
        captured = sum(1 for row in rows if _text(row.get(field)))
        coverage = float(captured) / float(count) if count else 0.0
        out.append(
            {
                "field": field,
                "captured_count": captured,
                "missing_count": max(0, count - captured),
                "coverage": coverage,
                "coverage_ok": coverage >= _FIELD_COVERAGE_FLOOR,
            }
        )
    return out
```
**SOURCE thin wrapper:** keep exact signature, import `libs.reporting.quant_tactic_eval_field_gaps_projection` as `_a8_owner`, replace old body with sole `return _a8_owner._field_gap_rows(rows,facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade._REQUIRED_FIELDS/_text/_FIELD_COVERAGE_FLOOR at call time; retain negative/error and copy semantics.
**NORMAL TARGETED `test_a8_field_gap_rows`:** [{'quant_tactic_id':'X'}]→five rows; quant_tactic_id coverage=1.0, others=0.0; []→coverage=0.0. Assert original-golden == wrapper == direct Owner and AST SOURCE body removed. **BLOCKED→NEXT:** log exact error, continue A1–A8 remaining / push.

## FUTURE RESERVE — 6/6 VERIFIED DESIGN ONLY, NOT EXECUTABLE
Six distinct original SOURCE bodies checked on actor and integration at matching blobs; six unique TARGETs absent in BOTH. RF-035 owns these reporting paths. These are evaluation/Markdown projections, never live trading, Broker, Guard, Step5C, UEF or RunLab effects. Before future issue C03 must recheck remote source/target/caller and safety; A must NOT implement these now.

### R1 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::_mismatch_examples` @ L104 | BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**TARGET ABSENT actor/integration:** `libs/reporting/quant_tactic_eval_mismatch_examples_projection.py::_mismatch_examples`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future normal fake fixture:** row with quant_tactic_mismatch_count=2,trade_id='T'→one example mismatch_count=2; zero→[]. **Safety/seam:** facade._int/_text; report-only; keep original SOURCE thin wrapper, use-time facade, no duplicated calculation and no effects.

### R2 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::build_quant_tactic_evaluation` @ L123 | BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**TARGET ABSENT actor/integration:** `libs/reporting/quant_tactic_eval_builder_projection.py::build_quant_tactic_evaluation`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future normal fake fixture:** []→status='hold_sample_insufficient',sample_count=0; 1 invalid closed row→status='hold_invalid_truth_samples'. **Safety/seam:** facade.Counter, all helper functions/constants at call time; evaluation data only, no live promotion; keep original SOURCE thin wrapper, use-time facade, no duplicated calculation and no effects.

### R3 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_evaluation.py::render_quant_tactic_evaluation_lines` @ L174 | BLOB `f11bd1e71dedb5494242fa88f3996885d1a3cef2`
**TARGET ABSENT actor/integration:** `libs/reporting/quant_tactic_eval_render_projection.py::render_quant_tactic_evaluation_lines`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future normal fake fixture:** {}→[]; {'status':'hold_sample_insufficient'}→nonempty Quant Q8 readiness lines. **Safety/seam:** facade._text/_int/_TARGET_PROMOTION_SAMPLE/Mapping; pure Markdown rendering; keep original SOURCE thin wrapper, use-time facade, no duplicated calculation and no effects.

### R4 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_report.py::_selected_candidate_row` @ L84 | BLOB `3cf76659bc4970c9f262405bbf829327203b7474`
**TARGET ABSENT actor/integration:** `libs/reporting/quant_tactic_selected_candidate_projection.py::_selected_candidate_row`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future normal fake fixture:** report with nested matching symbol + quant_factor_snapshot→selected row; no symbol→{}. **Safety/seam:** facade._nested_dicts/_candidate_symbol/_mapping, preserve nested score sort, no trading; keep original SOURCE thin wrapper, use-time facade, no duplicated calculation and no effects.

### R5 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_report.py::_tactic_sources` @ L127 | BLOB `3cf76659bc4970c9f262405bbf829327203b7474`
**TARGET ABSENT actor/integration:** `libs/reporting/quant_tactic_sources_projection.py::_tactic_sources`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future normal fake fixture:** entry_decision={'tactic_id':'A'}, others={}→[('entry_quant_decision','A')]. **Safety/seam:** facade._mapping/_tactic_value; pure observation; keep original SOURCE thin wrapper, use-time facade, no duplicated calculation and no effects.

### R6 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_tactic_report.py::render_quant_tactic_report_lines` @ L222 | BLOB `3cf76659bc4970c9f262405bbf829327203b7474`
**TARGET ABSENT actor/integration:** `libs/reporting/quant_tactic_report_lines_projection.py::render_quant_tactic_report_lines`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future normal fake fixture:** {}→[]; fake report with patched facade.quant_tactic_surface returning {'tactic_id':'T'}→nonempty '- 전술 ID:' line. **Safety/seam:** facade.quant_tactic_surface/_mapping/_fmt/_pct/_reason_text/_decision_label; pure render, no runtime decision; keep original SOURCE thin wrapper, use-time facade, no duplicated calculation and no effects.

**COUNTS:** previous A-04 REMOTE_DONE=8/8; NEW_READY=8; RESERVE_VERIFIED=6. C03 order publication is not code G1/G2/G3 or RF DONE. If source/target changes before execution, precisely BLOCKED and continue safe items; no self-selection.
