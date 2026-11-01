# C02 — Claude A | A-20261101-10 | FAST-3 EIGHT NEW VERIFIED SOURCE BODY MOVEs

**SINGLE ENTRY / PIN:** At start record CANONICAL_HEAD, ORDER_FILE_BLOB_SHA, OWNER_REMOTE_SHA and ORDER_ID=A-20261101-10. Read THIS document and named code/test only; do not read D00/RF/queue/C03/CURRENT/HANDOFF, do not self-select. Execute ALL A1–A8/B1–B8; any blocked item → next safe item. Previously pinned start order remains valid. C03 document commit is NOT G1/G2/G3 code work.

**REMOTE_DONE:** 8/8 at A 4c264f96; normal unittest 8/8 exit0, #11 6551064560. Do not reimplement completed prior order or rerun same-SHA tests. Source and Owner branch pinned for issuance: `4c264f9612d8ce82cb8d3ff3ec7844a6892e9ea0`; canonical input HEAD must be rechecked at actor start. Each item has real function body and new Owner path; each TARGET verified absent on actor and integration before publication. **NEW_READY=8**. 

**OWNER/SAFETY:** RF-035 CLAUDE_A only; actor branch `work/p15-a-reporter-pure-20261021`. Allowed SOURCE paths: `libs/reporting/q8_lane_decision_table.py`, `libs/reporting/q8_trusted_reaggregation.py`, `libs/reporting/quant_shadow_forward_outcomes.py`; allowed NEW TARGET paths only those enumerated below; NEW targeted test `tests/test_p15_rf035_20261101_10h_owners.py`. Do not modify other actor code, D00/RF/STATUS/queue/C04/C05/RunLab, real operations, Broker/Guard/Step5C/UEF, frozen oracle/CI workflow, production state, trading/network/real data or force-push. No actual order, promotion, guard, file write or subprocess; evaluate/render in memory. B audit parser may only parse fake argv; A trust policy thresholds/permissions remain byte-identical. Any safety ambiguity blocks that item, not others.

**TEST / PUSH:** Snapshot original golden and exact source blob before edit; Owner holds complete actual BODY and original SOURCE becomes a thin wrapper with call-time facade seams, unique import aliases `_c03_10_aN_owner` (avoid collision with previous orders). One new unittest per item in `tests/test_p15_rf035_20261101_10h_owners.py`. Normal command `python -m unittest tests/test_p15_rf035_20261101_10h_owners.py -v` expected exit0 **8/8** (NOT_RUN until actor executes); optional narrow existing tests, no mandatory blanket -O/full peer/hosted CI. Commit ONLY actor code/test, normal non-force push or approved expected-head lease, re-fetch actor HEAD and all changed SOURCE/Owner/test blobs; report per item, normal command/exit, exact SHA and measured START/END/ELAPSED to #11. Git auth failure=PUSH_BLOCKED not G1, continue safe work. C04 integrates, C05 G1/G2/G3/DONE/STATUS. No test/PASS is claimed by this order publication.

## A1 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::_fmt_pct` @ L116 | CURRENT_BLOB `d291b1d2b065a1e9cb31223c2f21213607235202`
**TARGET (404 on both refs VERIFIED):** `libs/reporting/q8_lane_pct_projection.py::_fmt_pct`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _fmt_pct(value: Any) -> str:
    if value in (None, ""):
        return "-"
    return f"{_float(value):.4f}%"
```
**THIN WRAPPER / PATCH:** inside SOURCE _fmt_pct, import libs.reporting.q8_lane_pct_projection as _c03_10_a1_owner; return _c03_10_a1_owner._fmt_pct(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **_float** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_a1_fmt_pct`:** None→'-'; 0.125→'0.1250%'. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #11; continue A2.

## A2 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_lane_decision_table.py::render_q8_lane_decision_table_markdown` @ L122 | CURRENT_BLOB `d291b1d2b065a1e9cb31223c2f21213607235202`
**TARGET (404 on both refs VERIFIED):** `libs/reporting/q8_lane_render_projection.py::render_q8_lane_decision_table_markdown`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
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
**THIN WRAPPER / PATCH:** inside SOURCE render_q8_lane_decision_table_markdown, import libs.reporting.q8_lane_render_projection as _c03_10_a2_owner; return _c03_10_a2_owner.render_q8_lane_decision_table_markdown(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **Mapping,_rows,_text,_fmt_pct** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_a2_render_q8_lane_decision_table_markdown`:** minimal day/rows=[] produces table and no trading permission; patched _rows. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #11; continue A3.

## A3 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_trusted_reaggregation.py::_iter_days` @ L21 | CURRENT_BLOB `47f5e9fcc30d699c0ea2d6d5ea7bf36c3491bfb2`
**TARGET (404 on both refs VERIFIED):** `libs/reporting/q8_trusted_day_projection.py::_iter_days`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _iter_days(start: str, end: str) -> Iterable[str]:
    current = date.fromisoformat(str(start)[:10])
    final = date.fromisoformat(str(end)[:10])
    while current <= final:
        yield current.isoformat()
        current += timedelta(days=1)
```
**THIN WRAPPER / PATCH:** inside SOURCE _iter_days, import libs.reporting.q8_trusted_day_projection as _c03_10_a3_owner; yield from _c03_10_a3_owner._iter_days(<original arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **date,timedelta** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_a3_iter_days`:** 2026-11-01..2026-11-02→two dates; invalid date raises; generator yield-from parity. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #11; continue A4.

## A4 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_trusted_reaggregation.py::_fmt_pct` @ L29 | CURRENT_BLOB `47f5e9fcc30d699c0ea2d6d5ea7bf36c3491bfb2`
**TARGET (404 on both refs VERIFIED):** `libs/reporting/q8_trusted_pct_projection.py::_fmt_pct`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _fmt_pct(value: Any) -> str:
    try:
        return f"{float(value):.2%}"
    except Exception:
        return "-"
```
**THIN WRAPPER / PATCH:** inside SOURCE _fmt_pct, import libs.reporting.q8_trusted_pct_projection as _c03_10_a4_owner; return _c03_10_a4_owner._fmt_pct(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **none** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_a4_fmt_pct`:** 0.125→'12.50%'; invalid→'-'. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #11; continue A5.

## A5 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_trusted_reaggregation.py::_fmt_num` @ L36 | CURRENT_BLOB `47f5e9fcc30d699c0ea2d6d5ea7bf36c3491bfb2`
**TARGET (404 on both refs VERIFIED):** `libs/reporting/q8_trusted_num_projection.py::_fmt_num`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _fmt_num(value: Any) -> str:
    try:
        return f"{int(value):,}"
    except Exception:
        return "0"
```
**THIN WRAPPER / PATCH:** inside SOURCE _fmt_num, import libs.reporting.q8_trusted_num_projection as _c03_10_a5_owner; return _c03_10_a5_owner._fmt_num(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **none** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_a5_fmt_num`:** 1234→'1,234'; invalid→'0'. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #11; continue A6.

## A6 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_trusted_reaggregation.py::_watchlist_rows` @ L43 | CURRENT_BLOB `47f5e9fcc30d699c0ea2d6d5ea7bf36c3491bfb2`
**TARGET (404 on both refs VERIFIED):** `libs/reporting/q8_trusted_watchlist_projection.py::_watchlist_rows`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _watchlist_rows(scorecard: Mapping[str, Any]) -> List[Dict[str, Any]]:
    return [dict(row) for row in list(scorecard.get("promotion_watchlist") or []) if isinstance(row, Mapping)]
```
**THIN WRAPPER / PATCH:** inside SOURCE _watchlist_rows, import libs.reporting.q8_trusted_watchlist_projection as _c03_10_a6_owner; return _c03_10_a6_owner._watchlist_rows(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **Mapping** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_a6_watchlist_rows`:** watchlist [{x:1},None]→[{x:1}] copy, absent→[]. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #11; continue A7.

## A7 | RF-035 CLAUDE_A | SOURCE `libs/reporting/q8_trusted_reaggregation.py::render_q8_trusted_reaggregation_markdown` @ L126 | CURRENT_BLOB `47f5e9fcc30d699c0ea2d6d5ea7bf36c3491bfb2`
**TARGET (404 on both refs VERIFIED):** `libs/reporting/q8_trusted_render_projection.py::render_q8_trusted_reaggregation_markdown`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def render_q8_trusted_reaggregation_markdown(payload: Mapping[str, Any]) -> str:
    date_range = payload.get("range") if isinstance(payload.get("range"), Mapping) else {}
    aggregate = payload.get("aggregate") if isinstance(payload.get("aggregate"), Mapping) else {}
    daily = list(payload.get("daily") or [])
    lines = [
        f"# Q8 Trusted Reaggregation ({date_range.get('start') or '-'} ~ {date_range.get('end') or '-'})",
        "",
        "This report is evaluation-only. It does not change trading behavior.",
        "",
        "## Summary",
        "",
        f"- raw candidates: **{_fmt_num(aggregate.get('candidate_count'))}**",
        f"- deduped candidates: **{_fmt_num(aggregate.get('deduped_candidate_count'))}**",
        f"- duplicate count/rate: **{_fmt_num(aggregate.get('duplicate_candidate_count'))} / {_fmt_pct(aggregate.get('duplicate_rate'))}**",
        f"- trusted forward: **{_fmt_num(aggregate.get('forward_outcome_available_count'))} / {_fmt_pct(aggregate.get('trusted_forward_coverage'))}**",
        f"- promotion allowed days: **{_fmt_num(aggregate.get('promotion_allowed_day_count'))}**",
        f"- cumulative trust gate: **`{aggregate.get('cumulative_trust_gate_status') or 'not_available'}`**",
        f"- cumulative promotion allowed: **`{bool(aggregate.get('cumulative_promotion_allowed'))}`**",
        f"- cumulative block reasons: **{', '.join(str(x) for x in list(aggregate.get('cumulative_trust_reasons') or [])) or '-'}**",
        "",
        "## Daily Trust Gate",
        "",
        "| Day | Raw | Deduped | Dup Rate | Trusted Forward | Trust Gate | Promotion | Reasons |",
        "|---|---:|---:|---:|---:|---|---|---|",
    ]
    for row in daily:
        reasons = ", ".join(str(x) for x in list(row.get("trust_reasons") or [])) or "-"
        lines.append(
            "| {day} | {raw} | {deduped} | {dup_rate} | {forward} ({coverage}) | `{gate}` | `{allowed}` | {reasons} |".format(
                day=row.get("day") or "-",
                raw=_fmt_num(row.get("candidate_count")),
                deduped=_fmt_num(row.get("deduped_candidate_count")),
                dup_rate=_fmt_pct(row.get("duplicate_rate")),
                forward=_fmt_num(row.get("trusted_forward_count")),
                coverage=_fmt_pct(row.get("trusted_forward_coverage")),
                gate=row.get("trust_gate_status") or "-",
                allowed=bool(row.get("promotion_allowed")),
                reasons=reasons,
            )
        )
    lines += [
        "",
        "## Promotion Watchlist",
        "",
        "| Day | Candidate | Observed | Days | +5m | +15m | MAE5 | State |",
        "|---|---|---:|---:|---:|---:|---:|---|",
    ]
    watch_count = 0
    for item in list(aggregate.get("promotion_watchlist") or []):
        if not isinstance(item, Mapping):
            continue
        watch_count += 1
        lines.append(
            "| {day} | `{name}` | {obs}/{count} | {days} | {ret5} | {ret15} | {mae5} | `{state}` |".format(
                day="cumulative",
                name=item.get("name") or "-",
                obs=_fmt_num(item.get("observed_count")),
                count=_fmt_num(item.get("candidate_count")),
                days=_fmt_num(item.get("observed_day_count")),
                ret5=f"{float(item.get('avg_return_5m_pct')):.4f}%" if item.get("avg_return_5m_pct") is not None else "-",
                ret15=f"{float(item.get('avg_return_15m_pct')):.4f}%" if item.get("avg_return_15m_pct") is not None else "-",
                mae5=f"{float(item.get('avg_mae_5m_pct')):.4f}%" if item.get("avg_mae_5m_pct") is not None else "-",
                state=item.get("review_state") or "-",
            )
        )
    for row in daily:
        for item in list(row.get("promotion_watchlist") or []):
            if not isinstance(item, Mapping):
                continue
            watch_count += 1
            lines.append(
                "| {day} | `{name}` | {obs}/{count} | {days} | {ret5} | {ret15} | {mae5} | `{state}` |".format(
                    day=row.get("day") or "-",
                    name=item.get("name") or "-",
                    obs=_fmt_num(item.get("observed_count")),
                    count=_fmt_num(item.get("candidate_count")),
                    days=_fmt_num(item.get("observed_day_count")),
                    ret5=f"{float(item.get('avg_return_5m_pct')):.4f}%" if item.get("avg_return_5m_pct") is not None else "-",
                    ret15=f"{float(item.get('avg_return_15m_pct')):.4f}%" if item.get("avg_return_15m_pct") is not None else "-",
                    mae5=f"{float(item.get('avg_mae_5m_pct')):.4f}%" if item.get("avg_mae_5m_pct") is not None else "-",
                    state=item.get("review_state") or "-",
                )
            )
    if watch_count <= 0:
        lines.append("| - | - | 0/0 | 0 | - | - | - | no_watchlist |")
    lines += [
        "",
        "## Decision Rule",
        "",
        "- PROMOTE is not allowed unless the daily trust gate has `promotion_allowed=true`.",
        f"- A day is promotion-review eligible only when trusted forward count >= {TRUSTED_FORWARD_MIN_COUNT}, "
        f"trusted coverage >= {TRUSTED_FORWARD_MIN_COVERAGE:.0%}, and duplicate rate <= {DUPLICATE_RATE_MAX:.0%}.",
        f"- Candidate-level promotion requires at least {PROMOTION_CANDIDATE_MIN_OBSERVED} trusted observations "
        f"across at least {PROMOTION_CANDIDATE_MIN_DAYS} observed days.",
        "- Cross-day or stale forward observations are excluded from trusted forward counts.",
        "- Duplicate candidates are removed before forward performance is averaged.",
    ]
    return "\n".join(lines)
```
**THIN WRAPPER / PATCH:** inside SOURCE render_q8_trusted_reaggregation_markdown, import libs.reporting.q8_trusted_render_projection as _c03_10_a7_owner; return _c03_10_a7_owner.render_q8_trusted_reaggregation_markdown(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **Mapping,_fmt_num,_fmt_pct,TRUSTED_FORWARD_MIN_COUNT,TRUSTED_FORWARD_MIN_COVERAGE,DUPLICATE_RATE_MAX,PROMOTION_CANDIDATE_MIN_OBSERVED,PROMOTION_CANDIDATE_MIN_DAYS** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_a7_render_q8_trusted_reaggregation_markdown`:** minimal payload range/aggregate/daily=[] yields heading and no_watchlist; fake one daily and one watchlist row preserve Markdown byte order. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #11; continue A8.

## A8 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_forward_outcomes.py::_normalize_rows` @ L60 | CURRENT_BLOB `f53b8f56a1c6afca60b46eb8cc18568c561504d9`
**TARGET (404 on both refs VERIFIED):** `libs/reporting/quant_forward_normalize_projection.py::_normalize_rows`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _normalize_rows(value: Any) -> list[Dict[str, Any]]:
    if isinstance(value, Mapping) and isinstance(value.get("rows"), list):
        raw_rows = value.get("rows") or []
    elif isinstance(value, list):
        raw_rows = value
    else:
        raw_rows = []
    rows: list[Dict[str, Any]] = []
    for raw in raw_rows:
        if not isinstance(raw, Mapping):
            continue
        ts = _to_int(raw.get("ts"), 0)
        close = _to_float(raw.get("close") or raw.get("price"), None)
        if ts <= 0 or close is None or close <= 0:
            continue
        high = _to_float(raw.get("high"), close) or close
        low = _to_float(raw.get("low"), close) or close
        rows.append(
            {
                "ts": ts,
                "close": float(close),
                "high": float(high),
                "low": float(low),
                "raw_ts": _text(raw.get("raw_ts") or raw.get("datetime") or raw.get("time")),
            }
        )
    rows.sort(key=lambda item: int(item["ts"]))
    return rows
```
**THIN WRAPPER / PATCH:** inside SOURCE _normalize_rows, import libs.reporting.quant_forward_normalize_projection as _c03_10_a8_owner; return _c03_10_a8_owner._normalize_rows(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **Mapping,_to_int,_to_float,_text** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_a8_normalize_rows`:** rows=[{ts:2,close:3,high:4,low:2},{ts:1,price:2},{ts:0,close:4}] => sorted ts [1,2], copies and high/low defaults; patched _to_int and exception parity. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #11; continue all other safe items and push.

## FUTURE RESERVE — RESERVE_NOT_VERIFIED 0/6 (DESIGN ONLY, NOT EXECUTABLE)
All six previously VERIFIED candidates have been promoted into this executable order and cannot be reused as future reserve. RESERVE_NOT_VERIFIED 0/6: next analyze remaining RF-035 reporting pure functions, verify SOURCE/TARGET blob and owner exclusivity before labeling VERIFIED. Do not infer safe new functions from names alone. Next C03 must independently inspect new SOURCE BODY/blob, Owner exclusivity, target 404 on both refs, effect/monkeypatch, normal fixture before issuing or marking VERIFIED.

**COUNTS:** previous REMOTE_DONE as above; NEW_READY=8 actual source BODY MOVEs, FUTURE_RESERVE_VERIFIED=0/6; C03 DOC_ONLY code G1/G2/G3=0 and RF_DONE_DELTA=0. RunLab Exited(255), RUN_SOURCE_SHA=UNKNOWN; do not touch runtime.
