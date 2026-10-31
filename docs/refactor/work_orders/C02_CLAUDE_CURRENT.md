# C02 — Claude A | A-20261101-07 | FAST-3 EIGHT NEW VERIFIED BODY MOVEs

**SINGLE ENTRY.** At start pin integration HEAD, C02 blob, A owner HEAD and ORDER_ID. Execute ALL A1–A8. Read this C02 and named source/target/test code only; no D00/RF/queue/C03/CURRENT/HANDOFF. A pinned earlier order is not retroactively cancelled. A-20261101-06 8/8 REMOTE_DONE at actor `770fb5cd288b7f482e1315ffa6ce037b6f3eedd5`, normal unittest 8/8 exit0 (#11 6549268472), exact selective integration `45082e6e675fdf7e42bf54c3c6572e0635ec6e7b` (#36 6549457962). Never redo completed functions or same-SHA tests.

**OWNER/SAFETY:** RF-035 CLAUDE_A exclusively, reporting/Q8 read-model only. Edit ONLY two named SOURCE files, eight new projection Owner files below, and NEW `tests/test_p15_rf035_20261101_07h_owners.py` on `work/p15-a-reporter-pure-20261021`. No B branch, D00/RF/STATUS/queue/C04/C05, protected Broker/Guard/Step5C/UEF/RunLab/real order/operational state/network, frozen oracle/CI, or real promotion. A7 is a read-model trust-gate **exact-body MOVE only**; NEVER change thresholds or permission semantics. A8 fake loader only, never access actual report directories. No force push.

**MOVE/TEST:** Preserve exact SOURCE signature, original computation/exception/output, thin SOURCE delegation, use-time facade monkeypatch and alias/copy behavior. The source q8 module already imports sys; add `import sys` to quant_shadow source only if absent (it already imports sys). Owner cannot import SOURCE. Capture original golden BEFORE editing. Create eight distinct stdlib unittest cases `test_a1_*`–`test_a8_*`, with in-memory/fake fixtures and positive/negative/exception/patch seams; test A7 no real promotion and A8 no disk. `python -m unittest tests/test_p15_rf035_20261101_07h_owners.py -v` normal exit0 required. Related targeted tests optional; not mandatory -O/full peer/hosted CI. Commit only code/test on A branch, normal push, re-fetch A HEAD and SOURCE/Owner/test blob SHA; report exact exit, status and measured START/END in #11. If push blocked, mark PUSH_BLOCKED, continue other safe items; blocked one does not end the order. If original SHA differs, re-evaluate only that item and report conflict, never blindly overwrite.

## A1 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::text_value` @ L24 | CURRENT_BLOB `9e0f385932819f67f7b1eba7d82d5cd07d9c5df7`
**NEW TARGET (A/integration 404 VERIFIED):** `libs/reporting/q8_text_value_projection.py::text_value`. MOVE **ENTIRE executable body below**, preserving signature/annotations and any nested functions; Owner adds keyword-only `facade` argument. No duplicate computation in SOURCE.
```python
def text_value(value: Any) -> str:
    text = str(value or "").strip()
    return "" if text.lower() in {"", "-", "none", "null", "unknown", "not_captured"} else text
```
**THIN WRAPPER:** Keep original signature in SOURCE; use unique alias `_a07_1_owner` (avoid collision with existing aliases); sole body is import `libs.reporting.q8_text_value_projection as _a07_1_owner` and `return _a07_1_owner.text_value(<original args forwarded>, facade=sys.modules[__name__])`. For A8 forward all keyword-only args; for A7 forward all five keyword-only args. **CALL-TIME PATCH SEAMS:** none; Owner references each through `facade.<name>`, including constants, and imports only safe typing/stdlib, never SOURCE. Preserve error/ordering/copy behavior.
**NORMAL TARGETED `test_a1_text_value`:** ' none ' → ''; 'A' → 'A'; odd object exception parity. Compare pinned original golden, SOURCE wrapper and direct Owner, including exception and patch seam parity; AST asserts SOURCE original computation removed. **BLOCKED→NEXT:** record exact SHA/error; continue A2.

## A2 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::forward_base` @ L29 | CURRENT_BLOB `9e0f385932819f67f7b1eba7d82d5cd07d9c5df7`
**NEW TARGET (A/integration 404 VERIFIED):** `libs/reporting/q8_forward_base_projection.py::forward_base`. MOVE **ENTIRE executable body below**, preserving signature/annotations and any nested functions; Owner adds keyword-only `facade` argument. No duplicate computation in SOURCE.
```python
def forward_base(row: Mapping[str, Any]) -> Dict[str, Any]:
    base = row.get("shadow_forward_base")
    return dict(base) if isinstance(base, Mapping) else {}
```
**THIN WRAPPER:** Keep original signature in SOURCE; use unique alias `_a07_2_owner` (avoid collision with existing aliases); sole body is import `libs.reporting.q8_forward_base_projection as _a07_2_owner` and `return _a07_2_owner.forward_base(<original args forwarded>, facade=sys.modules[__name__])`. For A8 forward all keyword-only args; for A7 forward all five keyword-only args. **CALL-TIME PATCH SEAMS:** Mapping; Owner references each through `facade.<name>`, including constants, and imports only safe typing/stdlib, never SOURCE. Preserve error/ordering/copy behavior.
**NORMAL TARGETED `test_a2_forward_base`:** {'shadow_forward_base':{'x':1}} → {'x':1} (not aliased); absent→{}. Compare pinned original golden, SOURCE wrapper and direct Owner, including exception and patch seam parity; AST asserts SOURCE original computation removed. **BLOCKED→NEXT:** record exact SHA/error; continue A3.

## A3 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::canonical_dedupe_key` @ L45 | CURRENT_BLOB `9e0f385932819f67f7b1eba7d82d5cd07d9c5df7`
**NEW TARGET (A/integration 404 VERIFIED):** `libs/reporting/q8_dedupe_key_projection.py::canonical_dedupe_key`. MOVE **ENTIRE executable body below**, preserving signature/annotations and any nested functions; Owner adds keyword-only `facade` argument. No duplicate computation in SOURCE.
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
**THIN WRAPPER:** Keep original signature in SOURCE; use unique alias `_a07_3_owner` (avoid collision with existing aliases); sole body is import `libs.reporting.q8_dedupe_key_projection as _a07_3_owner` and `return _a07_3_owner.canonical_dedupe_key(<original args forwarded>, facade=sys.modules[__name__])`. For A8 forward all keyword-only args; for A7 forward all five keyword-only args. **CALL-TIME PATCH SEAMS:** forward_base,candidate_day,text_value,entry_lane_subtype; Owner references each through `facade.<name>`, including constants, and imports only safe typing/stdlib, never SOURCE. Preserve error/ordering/copy behavior.
**NORMAL TARGETED `test_a3_canonical_dedupe_key`:** fixed generated_at 2026-11-01, symbol 005930, baseline_epoch 42, fake lane trend:x → ('20261101','005930',42,'trend:x'); invalid epoch→0. Compare pinned original golden, SOURCE wrapper and direct Owner, including exception and patch seam parity; AST asserts SOURCE original computation removed. **BLOCKED→NEXT:** record exact SHA/error; continue A4.

## A4 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::dedupe_q8_candidates` @ L59 | CURRENT_BLOB `9e0f385932819f67f7b1eba7d82d5cd07d9c5df7`
**NEW TARGET (A/integration 404 VERIFIED):** `libs/reporting/q8_dedupe_candidates_projection.py::dedupe_q8_candidates`. MOVE **ENTIRE executable body below**, preserving signature/annotations and any nested functions; Owner adds keyword-only `facade` argument. No duplicate computation in SOURCE.
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
**THIN WRAPPER:** Keep original signature in SOURCE; use unique alias `_a07_4_owner` (avoid collision with existing aliases); sole body is import `libs.reporting.q8_dedupe_candidates_projection as _a07_4_owner` and `return _a07_4_owner.dedupe_q8_candidates(<original args forwarded>, facade=sys.modules[__name__])`. For A8 forward all keyword-only args; for A7 forward all five keyword-only args. **CALL-TIME PATCH SEAMS:** canonical_dedupe_key; Owner references each through `facade.<name>`, including constants, and imports only safe typing/stdlib, never SOURCE. Preserve error/ordering/copy behavior.
**NORMAL TARGETED `test_a4_dedupe_q8_candidates`:** two rows with same fake key→one copied first row, stable order; distinct keys→two. Compare pinned original golden, SOURCE wrapper and direct Owner, including exception and patch seam parity; AST asserts SOURCE original computation removed. **BLOCKED→NEXT:** record exact SHA/error; continue A5.

## A5 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::promotion_candidate_is_repeatable` @ L71 | CURRENT_BLOB `9e0f385932819f67f7b1eba7d82d5cd07d9c5df7`
**NEW TARGET (A/integration 404 VERIFIED):** `libs/reporting/q8_repeatable_projection.py::promotion_candidate_is_repeatable`. MOVE **ENTIRE executable body below**, preserving signature/annotations and any nested functions; Owner adds keyword-only `facade` argument. No duplicate computation in SOURCE.
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
**THIN WRAPPER:** Keep original signature in SOURCE; use unique alias `_a07_5_owner` (avoid collision with existing aliases); sole body is import `libs.reporting.q8_repeatable_projection as _a07_5_owner` and `return _a07_5_owner.promotion_candidate_is_repeatable(<original args forwarded>, facade=sys.modules[__name__])`. For A8 forward all keyword-only args; for A7 forward all five keyword-only args. **CALL-TIME PATCH SEAMS:** PROMOTION_CANDIDATE_MIN_OBSERVED,PROMOTION_CANDIDATE_MIN_DAYS; Owner references each through `facade.<name>`, including constants, and imports only safe typing/stdlib, never SOURCE. Preserve error/ordering/copy behavior.
**NORMAL TARGETED `test_a5_promotion_candidate_is_repeatable`:** observed_count=50, observed_day_count=2, avg_return_5m_pct=1, avg_return_15m_pct=1→True; zero return→False. Compare pinned original golden, SOURCE wrapper and direct Owner, including exception and patch seam parity; AST asserts SOURCE original computation removed. **BLOCKED→NEXT:** record exact SHA/error; continue A6.

## A6 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::entry_lane_subtype` @ L38 | CURRENT_BLOB `9e0f385932819f67f7b1eba7d82d5cd07d9c5df7`
**NEW TARGET (A/integration 404 VERIFIED):** `libs/reporting/q8_entry_lane_projection.py::entry_lane_subtype`. MOVE **ENTIRE executable body below**, preserving signature/annotations and any nested functions; Owner adds keyword-only `facade` argument. No duplicate computation in SOURCE.
```python
def entry_lane_subtype(row: Mapping[str, Any]) -> str:
    observation = build_entry_lane_observation(row)
    lane = text_value(observation.get("primary_lane")) or "unknown"
    subtype = text_value(observation.get("subtype")) or "unknown"
    return f"{lane}:{subtype}"
```
**THIN WRAPPER:** Keep original signature in SOURCE; use unique alias `_a07_6_owner` (avoid collision with existing aliases); sole body is import `libs.reporting.q8_entry_lane_projection as _a07_6_owner` and `return _a07_6_owner.entry_lane_subtype(<original args forwarded>, facade=sys.modules[__name__])`. For A8 forward all keyword-only args; for A7 forward all five keyword-only args. **CALL-TIME PATCH SEAMS:** build_entry_lane_observation,text_value; Owner references each through `facade.<name>`, including constants, and imports only safe typing/stdlib, never SOURCE. Preserve error/ordering/copy behavior.
**NORMAL TARGETED `test_a6_entry_lane_subtype`:** fake observation {'primary_lane':'trend','subtype':'pullback'}→'trend:pullback'; empty→'unknown:unknown'. Compare pinned original golden, SOURCE wrapper and direct Owner, including exception and patch seam parity; AST asserts SOURCE original computation removed. **BLOCKED→NEXT:** record exact SHA/error; continue A7.

## A7 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_evaluation_contract.py::build_q8_trust_gate` @ L84 | CURRENT_BLOB `9e0f385932819f67f7b1eba7d82d5cd07d9c5df7`
**NEW TARGET (A/integration 404 VERIFIED):** `libs/reporting/q8_trust_gate_projection.py::build_q8_trust_gate`. MOVE **ENTIRE executable body below**, preserving signature/annotations and any nested functions; Owner adds keyword-only `facade` argument. No duplicate computation in SOURCE.
```python
def build_q8_trust_gate(
    *,
    raw_candidate_count: int,
    deduped_candidate_count: int,
    trusted_forward_count: int,
    trusted_forward_coverage: float,
    candidate_watchlist: Sequence[Mapping[str, Any]],
) -> Dict[str, Any]:
    duplicate_count = max(0, int(raw_candidate_count) - int(deduped_candidate_count))
    duplicate_rate = (
        round(float(duplicate_count) / float(raw_candidate_count), 4)
        if raw_candidate_count
        else 0.0
    )
    repeatable = [row for row in candidate_watchlist if promotion_candidate_is_repeatable(row)]
    reasons: List[str] = []
    if trusted_forward_count < TRUSTED_FORWARD_MIN_COUNT:
        reasons.append("trusted_forward_sample_below_100")
    if trusted_forward_coverage < TRUSTED_FORWARD_MIN_COVERAGE:
        reasons.append("trusted_forward_coverage_below_70pct")
    if duplicate_rate > DUPLICATE_RATE_MAX:
        reasons.append("duplicate_rate_above_75pct")
    if not repeatable:
        reasons.append("no_repeatable_promotion_watch_candidate")

    promotion_allowed = not reasons
    if promotion_allowed:
        status = TRUST_GATE_STATUS_READY
    elif "trusted_forward_sample_below_100" in reasons or "trusted_forward_coverage_below_70pct" in reasons:
        status = TRUST_GATE_STATUS_SAMPLE_BLOCKED
    else:
        status = TRUST_GATE_STATUS_NO_REPEATABLE_CANDIDATE

    return {
        "status": status,
        "promotion_allowed": bool(promotion_allowed),
        "block_reasons": reasons,
        "trusted_forward_count": int(trusted_forward_count),
        "trusted_forward_coverage": round(float(trusted_forward_coverage), 4),
        "duplicate_rate": duplicate_rate,
        "duplicate_count": duplicate_count,
        "minimums": {
            "trusted_forward_count": TRUSTED_FORWARD_MIN_COUNT,
            "trusted_forward_coverage": TRUSTED_FORWARD_MIN_COVERAGE,
            "duplicate_rate_max": DUPLICATE_RATE_MAX,
            "candidate_observed_count": PROMOTION_CANDIDATE_MIN_OBSERVED,
            "candidate_observed_day_count": PROMOTION_CANDIDATE_MIN_DAYS,
        },
    }
```
**THIN WRAPPER:** Keep original signature in SOURCE; use unique alias `_a07_7_owner` (avoid collision with existing aliases); sole body is import `libs.reporting.q8_trust_gate_projection as _a07_7_owner` and `return _a07_7_owner.build_q8_trust_gate(<original args forwarded>, facade=sys.modules[__name__])`. For A8 forward all keyword-only args; for A7 forward all five keyword-only args. **CALL-TIME PATCH SEAMS:** promotion_candidate_is_repeatable,TRUSTED_FORWARD_MIN_COUNT,TRUSTED_FORWARD_MIN_COVERAGE,DUPLICATE_RATE_MAX,PROMOTION_CANDIDATE_MIN_OBSERVED,PROMOTION_CANDIDATE_MIN_DAYS,TRUST_GATE_STATUS_READY,TRUST_GATE_STATUS_SAMPLE_BLOCKED,TRUST_GATE_STATUS_NO_REPEATABLE_CANDIDATE; Owner references each through `facade.<name>`, including constants, and imports only safe typing/stdlib, never SOURCE. Preserve error/ordering/copy behavior.
**NORMAL TARGETED `test_a7_build_q8_trust_gate`:** raw=100,deduped=100,trusted=100,coverage=.9,watchlist=[repeatable row]→status promotion_review_ready and promotion_allowed True; trusted=0→promotion_blocked_sample_or_coverage; no live promotion. Compare pinned original golden, SOURCE wrapper and direct Owner, including exception and patch seam parity; AST asserts SOURCE original computation removed. **BLOCKED→NEXT:** record exact SHA/error; continue A8.

## A8 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_candidate_evaluation.py::load_quant_shadow_candidate_payloads_for_range` @ L188 | CURRENT_BLOB `fa261af58f87966f22d8f00c4510245f3a54067f`
**NEW TARGET (A/integration 404 VERIFIED):** `libs/reporting/quant_shadow_range_load_projection.py::load_quant_shadow_candidate_payloads_for_range`. MOVE **ENTIRE executable body below**, preserving signature/annotations and any nested functions; Owner adds keyword-only `facade` argument. No duplicate computation in SOURCE.
```python
def load_quant_shadow_candidate_payloads_for_range(
    *,
    reports_root: Path,
    start: str,
    end: str,
    drop_q9_row_keys: Optional[Sequence[str]] = None,
    keys: Optional[Sequence[str]] = None,
) -> List[Dict[str, Any]]:
    return load_quant_shadow_candidate_payloads(
        reports_root=reports_root,
        days=list(_iter_days(start, end)),
        keys=keys,
        drop_q9_row_keys=drop_q9_row_keys,
    )
```
**THIN WRAPPER:** Keep original signature in SOURCE; use unique alias `_a07_8_owner` (avoid collision with existing aliases); sole body is import `libs.reporting.quant_shadow_range_load_projection as _a07_8_owner` and `return _a07_8_owner.load_quant_shadow_candidate_payloads_for_range(<original args forwarded>, facade=sys.modules[__name__])`. For A8 forward all keyword-only args; for A7 forward all five keyword-only args. **CALL-TIME PATCH SEAMS:** _iter_days,load_quant_shadow_candidate_payloads; Owner references each through `facade.<name>`, including constants, and imports only safe typing/stdlib, never SOURCE. Preserve error/ordering/copy behavior.
**NORMAL TARGETED `test_a8_load_quant_shadow_candidate_payloads_for_range`:** fake _iter_days('2026-11-01','2026-11-01')→['20261101']; fake loader returns [{'id':'x'}]; expect same list and forwarded keys/drop_q9_row_keys; never read disk. Compare pinned original golden, SOURCE wrapper and direct Owner, including exception and patch seam parity; AST asserts SOURCE original computation removed. **BLOCKED→NEXT:** record exact SHA/error; continue A1–A8 remaining/push.


## FUTURE RESERVE — RESERVE_NOT_VERIFIED 0/6 (NOT EXECUTABLE)
The previous six verified reserves have become A1–A6. **No new six have yet been independently proven on the current A/integration source/target set.** Do not select work yourself; C03 must replenish six with actual source bodies, owner proof, missing targets and fake tests before another issue. Possible future reporting source exploration is C03-only and NOT a work order.

**COUNTS:** A-06 REMOTE_DONE=8/8; A-07 NEW_READY=8 distinct; RESERVE_VERIFIED=0/6; no C03 code G1/G2/G3 or RF DONE claim.
