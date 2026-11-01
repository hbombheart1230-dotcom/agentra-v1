# C02 — Claude A | A-20261101-09 | FAST-3 EIGHT NEW VERIFIED BODY MOVEs

**SINGLE ENTRY / PIN:** At start pin `integration/p1.5` HEAD, this C02 blob, A owner HEAD and ORDER_ID. Execute ALL A1–A8 in this file. Read this C02 and named code/test only; do not open D00/RF/queue/C03/CURRENT/HANDOFF or self-select tasks. An already start-pinned earlier order is not retroactively cancelled.

**REMOTE_DONE:** A-20261101-08 A1–A8 8/8 at A remote `a379b27414509c4b417bd8be9bc51853cecf09c1` (#11 comment `6550479929`), normal `python -m unittest tests/test_p15_rf035_20261101_08h_forward_owners.py` exit0 8/8; C04 exact integration `93a1a4b2e2b27b3ad4e9b853fa4baef0c6fc52b1`, C05 scoped acceptance at `a88bdecc489b57bffd694e41db3d368addb8a373`. Do NOT reimplement A-08 or rerun same-SHA tests. Existing RF-035 DONE is preserved; this C03 document is not a code G1/G2/G3 result.

**OWNER/SAFETY:** RF-035 CLAUDE_A only. SOURCE `libs/reporting/q8_lane_decision_table.py` A/integration exact Git blob `d997eef97b2a2077c1be638948e4355503d7c018`. Only edit this SOURCE, eight unique NEW `libs/reporting/q8_lane_*_projection.py` Owner files named below, and NEW `tests/test_p15_rf035_20261101_09h_q8_lane_owners.py` on `work/p15-a-reporter-pure-20261021`. All eight targets independently 404 at BOTH A and integration before issuance. Evaluation/read-model calculations ONLY; preserve Q8 trust/promotion policy EXACTLY; do not alter threshold, guard or actual permission. No live data, disk reports, real CLI, promotion action, state, Broker/Guard/Step5C/UEF/RunLab, network, frozen oracle/CI workflow, other Owner files, force push. Use in-memory rows and patched fake helpers. Do not call real `build_q8_lane_decision_table` or `write_q8_lane_decision_table` during tests.

**BODY MOVE / WRAPPER CONTRACT:** Before edit capture original golden from pinned SOURCE for all 8. Copy each complete original executable body below into target Owner with original args plus keyword-only `facade` where indicated. Target imports stdlib typing only as needed, NEVER SOURCE. Replace listed unqualified globals in target BODY with `facade.<name>` at call time (do not snapshot at import time). In SOURCE add `import sys` (not present at pinned blob); keep exact original public/private signatures, annotations and defaults; each original becomes a sole thin delegate with a **unique local import alias `_a09_N_owner`** inside the function, `return _a09_N_owner.<original_function>(<original args>, facade=sys.modules[__name__])` for facade-dependent items, or direct Owner call without facade for pure items. No duplicate calculation in SOURCE. Preserve exception behavior, ordering, copies, patched helper seams and Q8 policy decisions; original caller imports remain intact. Test direct Owner and SOURCE wrapper vs ORIGINAL golden, positive/negative/exception and call-time monkeypatch. AST assert original computation moved and Owner holds actual BODY (not a stub). Run `python -m unittest tests/test_p15_rf035_20261101_09h_q8_lane_owners.py -v` normal exit0 8/8. Optional relevant narrow tests, no mandatory blanket -O/full peer/hosted CI. Commit ONLY A code/test, normal non-force push, independently re-fetch A HEAD and SOURCE/Owner/test blobs; report per item + exact normal command/exit + actual START/END/ELAPSED to #11. If one item blocked by drift/safety/test, report exact SHA/error and CONTINUE all other safe items. Git auth failure=PUSH_BLOCKED, not remote G1; C04 integrates, C05 owns G1/G2/G3/STATUS/DONE.

## A1 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::_text` @ L14 | CURRENT_BLOB `d997eef97b2a2077c1be638948e4355503d7c018`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/q8_lane_text_projection.py::_text`. MOVE **EXACT executable BODY** below, retaining original signature in SOURCE as thin wrapper only.
```python
def _text(value: Any) -> str:
    return str(value or "").strip()
```
**WRAPPER / CALL-TIME PATCH:** SOURCE local import `from libs.reporting import q8_lane_text_projection as _a09_1_owner` inside `_text`; delegate `_a09_1_owner._text(value)`. Owner patch globals: none. Owner must not import SOURCE. Exact argument forwarding and output/error order mandatory.
**NORMAL TARGETED `test_a1_text`:** ' A '→'A'; None→''; odd __str__ raises same exception. Original golden vs wrapper vs direct Owner; assert AST BODY removal and no cyclic import. In-memory only, no operational effects. **BLOCKED→NEXT:** record precise SHA/error; continue A2.

## A2 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::_float` @ L18 | CURRENT_BLOB `d997eef97b2a2077c1be638948e4355503d7c018`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/q8_lane_float_projection.py::_float`. MOVE **EXACT executable BODY** below, retaining original signature in SOURCE as thin wrapper only.
```python
def _float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return float(default)
        return float(value)
    except Exception:
        return float(default)
```
**WRAPPER / CALL-TIME PATCH:** SOURCE local import `from libs.reporting import q8_lane_float_projection as _a09_2_owner` inside `_float`; delegate `_a09_2_owner._float(value, default)`. Owner patch globals: none. Owner must not import SOURCE. Exact argument forwarding and output/error order mandatory.
**NORMAL TARGETED `test_a2_float`:** '1.5'→1.5; bad default=3→3; None default=2→2. Original golden vs wrapper vs direct Owner; assert AST BODY removal and no cyclic import. In-memory only, no operational effects. **BLOCKED→NEXT:** record precise SHA/error; continue A3.

## A3 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::_int` @ L27 | CURRENT_BLOB `d997eef97b2a2077c1be638948e4355503d7c018`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/q8_lane_int_projection.py::_int`. MOVE **EXACT executable BODY** below, retaining original signature in SOURCE as thin wrapper only.
```python
def _int(value: Any, default: int = 0) -> int:
    try:
        if value in (None, ""):
            return int(default)
        return int(float(value))
    except Exception:
        return int(default)
```
**WRAPPER / CALL-TIME PATCH:** SOURCE local import `from libs.reporting import q8_lane_int_projection as _a09_3_owner` inside `_int`; delegate `_a09_3_owner._int(value, default)`. Owner patch globals: none. Owner must not import SOURCE. Exact argument forwarding and output/error order mandatory.
**NORMAL TARGETED `test_a3_int`:** '2.9'→2; bad default=4→4; None default=4→4. Original golden vs wrapper vs direct Owner; assert AST BODY removal and no cyclic import. In-memory only, no operational effects. **BLOCKED→NEXT:** record precise SHA/error; continue A4.

## A4 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::_rows` @ L36 | CURRENT_BLOB `d997eef97b2a2077c1be638948e4355503d7c018`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/q8_lane_rows_projection.py::_rows`. MOVE **EXACT executable BODY** below, retaining original signature in SOURCE as thin wrapper only.
```python
def _rows(value: Any) -> List[Dict[str, Any]]:
    return [dict(row) for row in list(value or []) if isinstance(row, Mapping)]
```
**WRAPPER / CALL-TIME PATCH:** SOURCE local import `from libs.reporting import q8_lane_rows_projection as _a09_4_owner` inside `_rows`; delegate `_a09_4_owner._rows(value, facade=sys.modules[__name__])`. Owner patch globals: Mapping via facade.Mapping. Owner must not import SOURCE. Exact argument forwarding and output/error order mandatory.
**NORMAL TARGETED `test_a4_rows`:** [{'x':1},None]→[{'x':1}]; result dict is copy, not alias; non-list Mapping {'rows':[]} yields []. Original golden vs wrapper vs direct Owner; assert AST BODY removal and no cyclic import. In-memory only, no operational effects. **BLOCKED→NEXT:** record precise SHA/error; continue A5.

## A5 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::_forward_rows` @ L40 | CURRENT_BLOB `d997eef97b2a2077c1be638948e4355503d7c018`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/q8_lane_forward_rows_projection.py::_forward_rows`. MOVE **EXACT executable BODY** below, retaining original signature in SOURCE as thin wrapper only.
```python
def _forward_rows(evaluation: Mapping[str, Any]) -> List[Dict[str, Any]]:
    forward = evaluation.get("entry_lane_forward_outcomes")
    if not isinstance(forward, Mapping):
        return []
    return _rows(forward.get("by_primary_lane"))
```
**WRAPPER / CALL-TIME PATCH:** SOURCE local import `from libs.reporting import q8_lane_forward_rows_projection as _a09_5_owner` inside `_forward_rows`; delegate `_a09_5_owner._forward_rows(evaluation, facade=sys.modules[__name__])`. Owner patch globals: Mapping, _rows via facade.Mapping/facade._rows. Owner must not import SOURCE. Exact argument forwarding and output/error order mandatory.
**NORMAL TARGETED `test_a5_forward_rows`:** {'entry_lane_forward_outcomes':{'by_primary_lane':[{'name':'x'}]}}→[{'name':'x'}]; missing/nonmapping→[]; monkeypatch _rows. Original golden vs wrapper vs direct Owner; assert AST BODY removal and no cyclic import. In-memory only, no operational effects. **BLOCKED→NEXT:** record precise SHA/error; continue A6.

## A6 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::_counts_by_name` @ L47 | CURRENT_BLOB `d997eef97b2a2077c1be638948e4355503d7c018`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/q8_lane_counts_projection.py::_counts_by_name`. MOVE **EXACT executable BODY** below, retaining original signature in SOURCE as thin wrapper only.
```python
def _counts_by_name(rows: Iterable[Mapping[str, Any]]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for row in rows:
        name = _text(row.get("name"))
        if name:
            out[name] = _int(row.get("count"))
    return out
```
**WRAPPER / CALL-TIME PATCH:** SOURCE local import `from libs.reporting import q8_lane_counts_projection as _a09_6_owner` inside `_counts_by_name`; delegate `_a09_6_owner._counts_by_name(rows, facade=sys.modules[__name__])`. Owner patch globals: _text, _int via facade. Owner must not import SOURCE. Exact argument forwarding and output/error order mandatory.
**NORMAL TARGETED `test_a6_counts_by_name`:** [{'name':' A ','count':'2.9'},{'name':'B','count':3}]→{'A':2,'B':3}; empty name excluded; patched _int. Original golden vs wrapper vs direct Owner; assert AST BODY removal and no cyclic import. In-memory only, no operational effects. **BLOCKED→NEXT:** record precise SHA/error; continue A7.

## A7 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::_reason_summary` @ L56 | CURRENT_BLOB `d997eef97b2a2077c1be638948e4355503d7c018`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/q8_lane_reason_summary_projection.py::_reason_summary`. MOVE **EXACT executable BODY** below, retaining original signature in SOURCE as thin wrapper only.
```python
def _reason_summary(evaluation: Mapping[str, Any], *, limit: int = 6) -> str:
    parts = []
    for row in _rows(evaluation.get("by_reason"))[:limit]:
        name = _text(row.get("name"))
        if name:
            parts.append(f"{name} {row.get('count') or 0}")
    return ", ".join(parts) if parts else "-"
```
**WRAPPER / CALL-TIME PATCH:** SOURCE local import `from libs.reporting import q8_lane_reason_summary_projection as _a09_7_owner` inside `_reason_summary`; delegate `_a09_7_owner._reason_summary(evaluation, limit=limit, facade=sys.modules[__name__])`. Owner patch globals: _rows, _text via facade. Owner must not import SOURCE. Exact argument forwarding and output/error order mandatory.
**NORMAL TARGETED `test_a7_reason_summary`:** {'by_reason':[{'name':'A','count':2}]}→'A 2'; missing→'-'; limit=0→'-'; patched _rows. Original golden vs wrapper vs direct Owner; assert AST BODY removal and no cyclic import. In-memory only, no operational effects. **BLOCKED→NEXT:** record precise SHA/error; continue A8.

## A8 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::_verdict` @ L65 | CURRENT_BLOB `d997eef97b2a2077c1be638948e4355503d7c018`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/q8_lane_verdict_projection.py::_verdict`. MOVE **EXACT executable BODY** below, retaining original signature in SOURCE as thin wrapper only.
```python
def _verdict(row: Mapping[str, Any], *, promotion_allowed: bool) -> Dict[str, str]:
    observed = _int(row.get("observed_count"))
    coverage = _float(row.get("coverage"))
    ret5 = _float(row.get("avg_return_5m_pct"))
    ret15 = _float(row.get("avg_return_15m_pct"))
    mfe5 = _float(row.get("avg_mfe_5m_pct"))
    mae5 = _float(row.get("avg_mae_5m_pct"))
    lane = _text(row.get("name"))

    if not promotion_allowed:
        return {
            "verdict": "TRUST_GATE_BLOCKED",
            "decision": "retain under observation",
            "rationale": "Q8 trust gate blocked promotion review; lane signal is diagnostic only.",
        }
    if observed < 10 or coverage < TRUSTED_FORWARD_MIN_COVERAGE:
        return {
            "verdict": "DATA_INCOMPLETE",
            "decision": "observe",
            "rationale": "sample or trusted forward coverage is insufficient.",
        }
    if lane == "vwap_reclaim" and ret5 < 0.0 and ret15 < 0.0:
        return {
            "verdict": "GOOD_BLOCK",
            "decision": "keep blocked",
            "rationale": "VWAP reclaim lane showed weak short/mid forward returns.",
        }
    if ret5 >= 0.50 or ret15 >= 0.80 or mfe5 >= 1.50:
        risk_note = " MAE is high, so only small probe or rule review is allowed." if mae5 <= -1.50 else ""
        return {
            "verdict": "MISSED_OPPORTUNITY",
            "decision": "relaxation candidate",
            "rationale": f"Blocked candidates showed positive forward potential.{risk_note}".strip(),
        }
    if ret5 <= 0.0 and ret15 <= 0.0:
        return {
            "verdict": "GOOD_BLOCK",
            "decision": "keep blocked",
            "rationale": "Blocked candidates showed weak forward returns.",
        }
    return {
        "verdict": "DATA_INCOMPLETE",
        "decision": "observe",
        "rationale": "Signal direction is not decisive enough for a policy review.",
    }
```
**WRAPPER / CALL-TIME PATCH:** SOURCE local import `from libs.reporting import q8_lane_verdict_projection as _a09_8_owner` inside `_verdict`; delegate `_a09_8_owner._verdict(row, promotion_allowed=promotion_allowed, facade=sys.modules[__name__])`. Owner patch globals: _int,_float,_text,TRUSTED_FORWARD_MIN_COVERAGE via facade. Owner must not import SOURCE. Exact argument forwarding and output/error order mandatory.
**NORMAL TARGETED `test_a8_verdict`:** promotion_allowed=False→TRUST_GATE_BLOCKED; allowed=True observed_count=5→DATA_INCOMPLETE; observed=12 coverage=1 lane=vwap_reclaim ret5=-1 ret15=-1→GOOD_BLOCK; observed=12 coverage=1 ret5=0.6→MISSED_OPPORTUNITY; threshold patched at SOURCE changes result. Original golden vs wrapper vs direct Owner; assert AST BODY removal and no cyclic import. In-memory only, no operational effects. **BLOCKED→NEXT:** record precise SHA/error; continue remaining safe A items and push.

## FUTURE RESERVE — VERIFIED 6/6 (DESIGN ONLY; NOT EXECUTABLE)
These six are separate, unissued RF-035 CLAUDE_A candidates. Both actor/integration SOURCE blobs match; all six unique target paths independently 404 on BOTH refs. Do not execute or self-select without a NEW C03-issued C02. No other Owner/real trading effects; use fake/in-memory data. C03 must revalidate SHA/target at future issuance.

### RESERVE 1 | RF-035 CLAUDE_A | `libs/reporting/q8_lane_decision_table.py::_fmt_pct` @ L173 | SOURCE_BLOB `d997eef97b2a2077c1be638948e4355503d7c018` → `libs/reporting/q8_lane_pct_projection.py::_fmt_pct` (404 both)
```python
def _fmt_pct(value: Any) -> str:
    if value in (None, ""):
        return "-"
    return f"{_float(value):.4f}%"
```
**DESIGN:** Complete BODY to unique Owner, original SOURCE thin wrapper; call-time seams _float via facade. Normal targeted original/Owner/wrapper fixture: None→'-', 0.125→'0.1250%'. Safe in-memory/mock only, no real IO. **RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 2 | RF-035 CLAUDE_A | `libs/reporting/q8_lane_decision_table.py::render_q8_lane_decision_table_markdown` @ L179 | SOURCE_BLOB `d997eef97b2a2077c1be638948e4355503d7c018` → `libs/reporting/q8_lane_render_projection.py::render_q8_lane_decision_table_markdown` (404 both)
```python
def render_q8_lane_decision_table_markdown(payload: Mapping[str, Any]) -> str:
    gate = payload.get("evaluation_trust_gate") if isinstance(payload.get("evaluation_trust_gate"), Mapping) else {}
    lines = [
        f"# Q8 Lane Decision Table - {payload.get('day')}",
        "",
        "## Summary",
        "",
        f"- payloads: {payload.get('payload_count')}",
        f"- candidates: {payload.get('candidate_count')}",
        f"- deduped candidates: {payload.get('deduped_candidate_count')}",
        f"- duplicates: {payload.get('duplicate_candidate_count')}",
        f"- dedupe_key: `{', '.join(list(payload.get('dedupe_key') or []))}`",
        f"- evaluated: {payload.get('evaluated_count')}",
        f"- forward observed: {payload.get('forward_outcome_available_count')} "
        f"({float(payload.get('forward_outcome_coverage') or 0.0):.1%})",
        f"- trust_gate: `{gate.get('status') or '-'}`",
        f"- promotion_allowed: `{bool(gate.get('promotion_allowed'))}`",
        f"- trust_block_reasons: `{', '.join(list(gate.get('block_reasons') or gate.get('reasons') or [])) or '-'}`",
        f"- would-enter: {payload.get('would_enter_count')}",
        f"- top reasons: {payload.get('reason_summary') or '-'}",
        "",
        "## Lane Verdicts",
        "",
        "| Lane | Verdict | Decision | n | obs | +5m | +15m | +30m | MFE5 | MAE5 | Rationale |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for row in _rows(payload.get("rows")):
        lines.append(
            "| "
            + " | ".join(
                [
                    _text(row.get("lane")) or "-",
                    _text(row.get("verdict")) or "-",
                    _text(row.get("decision")) or "-",
                    str(row.get("candidate_count") or 0),
                    str(row.get("observed_count") or 0),
                    _fmt_pct(row.get("avg_return_5m_pct")),
                    _fmt_pct(row.get("avg_return_15m_pct")),
                    _fmt_pct(row.get("avg_return_30m_pct")),
                    _fmt_pct(row.get("avg_mfe_5m_pct")),
                    _fmt_pct(row.get("avg_mae_5m_pct")),
                    _text(row.get("rationale")) or "-",
                ]
            )
            + " |"
        )
    lines += [
        "",
        "## Operating Interpretation",
        "",
        "- `TRUST_GATE_BLOCKED`: lane signal is visible, but Q8 evidence is not eligible for policy promotion.",
        "- `MISSED_OPPORTUNITY`: blocked candidates rose afterward. This is a review target, not direct permission to buy.",
        "- `GOOD_BLOCK`: blocked candidates underperformed after the block. Keep the gate under observation.",
        "- `DATA_INCOMPLETE`: sample or coverage is insufficient for a policy conclusion.",
        "",
        "## Current Action",
        "",
        "No new behavior patch is implied by this table unless the Q8 trust gate allows promotion review.",
        "",
    ]
    return "\n".join(lines)
```
**DESIGN:** Complete BODY to unique Owner, original SOURCE thin wrapper; call-time seams Mapping,_rows,_text,_fmt_pct via facade. Normal targeted original/Owner/wrapper fixture: minimal {'day':'2026-11-01','rows':[]}→Markdown heading/table; fake rows; no disk. Safe in-memory/mock only, no real IO. **RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 3 | RF-035 CLAUDE_A | `libs/reporting/q8_trusted_reaggregation.py::_iter_days` @ L21 | SOURCE_BLOB `47f5e9fcc30d699c0ea2d6d5ea7bf36c3491bfb2` → `libs/reporting/q8_trusted_day_projection.py::_iter_days` (404 both)
```python
def _iter_days(start: str, end: str) -> Iterable[str]:
    current = date.fromisoformat(str(start)[:10])
    final = date.fromisoformat(str(end)[:10])
    while current <= final:
        yield current.isoformat()
        current += timedelta(days=1)
```
**DESIGN:** Complete BODY to unique Owner, original SOURCE thin wrapper; call-time seams date,timedelta via facade; preserve yield-from wrapper. Normal targeted original/Owner/wrapper fixture: '2026-11-01'..'2026-11-02'→two dates; invalid date raises; generator yield parity. Safe in-memory/mock only, no real IO. **RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 4 | RF-035 CLAUDE_A | `libs/reporting/q8_trusted_reaggregation.py::_fmt_pct` @ L29 | SOURCE_BLOB `47f5e9fcc30d699c0ea2d6d5ea7bf36c3491bfb2` → `libs/reporting/q8_trusted_pct_projection.py::_fmt_pct` (404 both)
```python
def _fmt_pct(value: Any) -> str:
    try:
        return f"{float(value):.2%}"
    except Exception:
        return "-"
```
**DESIGN:** Complete BODY to unique Owner, original SOURCE thin wrapper; call-time seams none. Normal targeted original/Owner/wrapper fixture: 0.125→'12.50%'; invalid→'-'. Safe in-memory/mock only, no real IO. **RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 5 | RF-035 CLAUDE_A | `libs/reporting/q8_trusted_reaggregation.py::_fmt_num` @ L36 | SOURCE_BLOB `47f5e9fcc30d699c0ea2d6d5ea7bf36c3491bfb2` → `libs/reporting/q8_trusted_num_projection.py::_fmt_num` (404 both)
```python
def _fmt_num(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except Exception:
        return "0"
```
**DESIGN:** Complete BODY to unique Owner, original SOURCE thin wrapper; call-time seams none. Normal targeted original/Owner/wrapper fixture: 1234→'1,234'; invalid→'0'. Safe in-memory/mock only, no real IO. **RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 6 | RF-035 CLAUDE_A | `libs/reporting/q8_trusted_reaggregation.py::_watchlist_rows` @ L43 | SOURCE_BLOB `47f5e9fcc30d699c0ea2d6d5ea7bf36c3491bfb2` → `libs/reporting/q8_trusted_watchlist_projection.py::_watchlist_rows` (404 both)
```python
def _watchlist_rows(scorecard: Mapping[str, Any]) -> List[Dict[str, Any]]:
    return [dict(row) for row in list(scorecard.get("promotion_watchlist") or []) if isinstance(row, Mapping)]
```
**DESIGN:** Complete BODY to unique Owner, original SOURCE thin wrapper; call-time seams Mapping via facade. Normal targeted original/Owner/wrapper fixture: {'promotion_watchlist':[{'x':1},None]}→[{'x':1}] copied, missing→[]. Safe in-memory/mock only, no real IO. **RESERVE_VERIFIED, NOT ISSUED.**

**COUNTS:** A-08 REMOTE_DONE=8/8; A-09 NEW_READY=8 actual unimplemented SOURCE BODY MOVEs; A future RESERVE_VERIFIED=6/6. C03 DOC_ONLY; code G1/G2/G3=0, RF_DONE_DELTA=0.
