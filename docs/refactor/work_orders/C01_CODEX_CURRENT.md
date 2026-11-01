# C01 — Codex B | B-20261101-10 | FAST-3 EIGHT NEW VERIFIED SOURCE BODY MOVEs + TWO PRIOR CARRYOVERS

**SINGLE ENTRY / PIN:** At start record CANONICAL_HEAD, ORDER_FILE_BLOB_SHA, OWNER_REMOTE_SHA and ORDER_ID=B-20261101-10. Read THIS document and named code/test only; do not read D00/RF/queue/C03/CURRENT/HANDOFF, do not self-select. Execute ALL A1–A8/B1–B8; any blocked item → next safe item. Previously pinned start order remains valid. C03 document commit is NOT G1/G2/G3 code work.

**REMOTE_DONE:** B1–B5 plus earlier B7/B8 REMOTE_DONE, #12 6551023443; B6 and B-06 C1 remain CARRYOVER (not new). Do not reimplement completed prior order or rerun same-SHA tests. Source and Owner branch pinned for issuance: `b09c9670b3886019ff4ef91b4b133bd5e2afffd9`; canonical input HEAD must be rechecked at actor start. Each item has real function body and new Owner path; each TARGET verified absent on actor and integration before publication. **NEW_READY=8**. Two carryovers are additional obligations, not counted as NEW_READY.

**OWNER/SAFETY:** RF-063 CODEX_B only; actor branch `work/p15-b-operator-structure-20261022`. Allowed SOURCE paths: `scripts/diagnostics/check_audit_trail_completeness.py`; allowed NEW TARGET paths only those enumerated below; NEW targeted test `tests/test_p15_rf063_20261101_10h_audit_owners.py`, plus carryover-specific existing 06h/07h tests and two original SOURCE scripts only. Do not modify other actor code, D00/RF/STATUS/queue/C04/C05/RunLab, real operations, Broker/Guard/Step5C/UEF, frozen oracle/CI workflow, production state, trading/network/real data or force-push. No actual order, promotion, guard, file write or subprocess; evaluate/render in memory. B audit parser may only parse fake argv; A trust policy thresholds/permissions remain byte-identical. Any safety ambiguity blocks that item, not others.

**TEST / PUSH:** Snapshot original golden and exact source blob before edit; Owner holds complete actual BODY and original SOURCE becomes a thin wrapper with call-time facade seams, unique import aliases `_c03_10_bN_owner` (avoid collision with previous orders). One new unittest per item in `tests/test_p15_rf063_20261101_10h_audit_owners.py`. Normal command `python -m unittest tests/test_p15_rf063_20261101_10h_audit_owners.py -v` expected exit0 **8/8** (NOT_RUN until actor executes); optional narrow existing tests, no mandatory blanket -O/full peer/hosted CI. Commit ONLY actor code/test, normal non-force push or approved expected-head lease, re-fetch actor HEAD and all changed SOURCE/Owner/test blobs; report per item, normal command/exit, exact SHA and measured START/END/ELAPSED to #12. Git auth failure=PUSH_BLOCKED not G1, continue safe work. C04 integrates, C05 G1/G2/G3/DONE/STATUS. No test/PASS is claimed by this order publication.

**CARRYOVER NORMAL TESTS:** C1 must add its missing test to `tests/test_p15_rf063_20261101_06h_owners.py` and run normal exit0 8/8 (7 existing already previously passed). B6 must add missing test to `tests/test_p15_rf063_20261101_07h_owners.py` and run normal exit0 8/8 (7 existing already passed). Do not count prior 7 PASS as new. Use TemporaryDirectory only for C1/B6. Source B6 changed to current B blob `f9f4ff9c200cf895c8105eb8207723bc13bba1e8`; C1 current blob `c039f3df0b2427e901f07219990c63da70d7b95e`. Both targets confirmed 404 B/integration. Their exact original bodies and wrappers remain below, **CARRYOVER not new**.

## B1 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_to_epoch` @ L15 | CURRENT_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6`
**TARGET (404 on both refs VERIFIED):** `scripts/diagnostics/audit_trail_epoch_projection.py::_to_epoch`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _to_epoch(ts: Any) -> Optional[int]:
    if ts is None:
        return None
    if isinstance(ts, (int, float)):
        return int(ts)
    s = str(ts).strip()
    if not s:
        return None
    try:
        return int(float(s))
    except Exception:
        pass
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())
    except Exception:
        return None
```
**THIN WRAPPER / PATCH:** inside SOURCE _to_epoch, import scripts.diagnostics.audit_trail_epoch_projection as _c03_10_b1_owner; return _c03_10_b1_owner._to_epoch(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **datetime,timezone** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_b1_to_epoch`:** 1970-01-01T00:00:01Z→1; None→None; naive UTC and invalid. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #12; continue B2.

## B2 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_utc_day` @ L38 | CURRENT_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6`
**TARGET (404 on both refs VERIFIED):** `scripts/diagnostics/audit_trail_utc_day_projection.py::_utc_day`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _utc_day(ts: Any) -> str:
    epoch = _to_epoch(ts)
    if epoch is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%d")
```
**THIN WRAPPER / PATCH:** inside SOURCE _utc_day, import scripts.diagnostics.audit_trail_utc_day_projection as _c03_10_b2_owner; return _c03_10_b2_owner._utc_day(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **_to_epoch,datetime,timezone** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_b2_utc_day`:** ts=1→'1970-01-01'; None with fake datetime.now→fixed day. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #12; continue B3.

## B3 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_extract_ts` @ L45 | CURRENT_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6`
**TARGET (404 on both refs VERIFIED):** `scripts/diagnostics/audit_trail_extract_ts_projection.py::_extract_ts`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _extract_ts(row: Dict[str, Any]) -> Any:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    return row.get("ts") or payload.get("ts")
```
**THIN WRAPPER / PATCH:** inside SOURCE _extract_ts, import scripts.diagnostics.audit_trail_extract_ts_projection as _c03_10_b3_owner; return _c03_10_b3_owner._extract_ts(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **none** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_b3_extract_ts`:** {ts:0,payload:{ts:42}}→42; absent→None. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #12; continue B4.

## B4 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_extract_decision_action` @ L68 | CURRENT_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6`
**TARGET (404 on both refs VERIFIED):** `scripts/diagnostics/audit_trail_decision_action_projection.py::_extract_decision_action`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _extract_decision_action(row: Dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    packet = payload.get("decision_packet") if isinstance(payload.get("decision_packet"), dict) else {}
    intent = packet.get("intent") if isinstance(packet.get("intent"), dict) else {}
    action = intent.get("action") or payload.get("action") or payload.get("intent")
    return str(action or "").strip().upper()
```
**THIN WRAPPER / PATCH:** inside SOURCE _extract_decision_action, import scripts.diagnostics.audit_trail_decision_action_projection as _c03_10_b4_owner; return _c03_10_b4_owner._extract_decision_action(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **none** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_b4_extract_decision_action`:** nested intent.action='buy'→'BUY'; absent→''. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #12; continue B5.

## B5 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_extract_allowed` @ L76 | CURRENT_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6`
**TARGET (404 on both refs VERIFIED):** `scripts/diagnostics/audit_trail_allowed_projection.py::_extract_allowed`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _extract_allowed(row: Dict[str, Any]) -> Optional[bool]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    v = payload.get("allowed")
    if isinstance(v, bool):
        return v
    return None
```
**THIN WRAPPER / PATCH:** inside SOURCE _extract_allowed, import scripts.diagnostics.audit_trail_allowed_projection as _c03_10_b5_owner; return _c03_10_b5_owner._extract_allowed(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **none** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_b5_extract_allowed`:** payload.allowed=True→True; allowed=1→None. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #12; continue B6.

## B6 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_latest_day` @ L84 | CURRENT_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6`
**TARGET (404 on both refs VERIFIED):** `scripts/diagnostics/audit_trail_latest_day_projection.py::_latest_day`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _latest_day(rows: List[Dict[str, Any]]) -> str:
    days = sorted({str(r.get("_day") or "") for r in rows if str(r.get("_day") or "").strip()})
    if days:
        return str(days[-1])
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")
```
**THIN WRAPPER / PATCH:** inside SOURCE _latest_day, import scripts.diagnostics.audit_trail_latest_day_projection as _c03_10_b6_owner; return _c03_10_b6_owner._latest_day(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **datetime,timezone** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_b6_latest_day`:** days 2026-10-30 and 2026-11-01→2026-11-01; [] with fake datetime.now→fixed day. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #12; continue B7.

## B7 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_build_markdown` @ L212 | CURRENT_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6`
**TARGET (404 on both refs VERIFIED):** `scripts/diagnostics/audit_trail_markdown_projection.py::_build_markdown`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _build_markdown(*, day: str, out: Dict[str, Any]) -> str:
    anomalies = out.get("anomaly_examples") if isinstance(out.get("anomaly_examples"), dict) else {}
    stage_event_total = out.get("stage_event_total") if isinstance(out.get("stage_event_total"), dict) else {}
    lines = [
        f"# Audit Trail Completeness ({day})",
        "",
        f"- ok: **{bool(out.get('ok'))}**",
        f"- events: **{int(out.get('events') or 0)}**",
        f"- runs: **{int(out.get('run_total') or 0)}**",
        f"- actionable_decision_run_total: **{int(out.get('actionable_decision_run_total') or 0)}**",
        f"- linked_complete_run_total: **{int(out.get('linked_complete_run_total') or 0)}**",
        f"- link_success_rate: **{float(out.get('link_success_rate') or 0.0):.2%}**",
        "",
        "## Anomaly Totals",
        "",
        f"- missing_execution_start_total: {int(out.get('missing_execution_start_total') or 0)}",
        f"- missing_execution_resolution_total: {int(out.get('missing_execution_resolution_total') or 0)}",
        f"- missing_execution_payload_total: {int(out.get('missing_execution_payload_total') or 0)}",
        f"- missing_terminal_event_total: {int(out.get('missing_terminal_event_total') or 0)}",
        f"- orphan_execution_run_total: {int(out.get('orphan_execution_run_total') or 0)}",
        "",
        "## execute_from_packet stage_event_total",
        "",
    ]

    for k in ("start", "verdict", "execution", "degrade_policy_block", "end", "error"):
        lines.append(f"- {k}: {int(stage_event_total.get(k) or 0)}")

    lines += ["", "## Anomaly Examples", ""]
    for key in (
        "missing_execution_start",
        "missing_execution_resolution",
        "missing_execution_payload",
        "missing_terminal_event",
        "orphan_execution",
    ):
        vals = anomalies.get(key) if isinstance(anomalies.get(key), list) else []
        if vals:
            lines.append(f"- {key}: {', '.join(str(x) for x in vals)}")
        else:
            lines.append(f"- {key}: (none)")

    failures = out.get("failures") if isinstance(out.get("failures"), list) else []
    lines += ["", "## Failures", ""]
    if failures:
        for x in failures:
            lines.append(f"- {x}")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)
```
**THIN WRAPPER / PATCH:** inside SOURCE _build_markdown, import scripts.diagnostics.audit_trail_markdown_projection as _c03_10_b7_owner; return _c03_10_b7_owner._build_markdown(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **none** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_b7_build_markdown`:** day=2026-11-01,out={ok:true,events:0} => heading, no anomalies/failures, terminal newline; anomalies/stage_event_total deterministic ordering. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #12; continue B8.

## B8 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_build_parser` @ L265 | CURRENT_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6`
**TARGET (404 on both refs VERIFIED):** `scripts/diagnostics/audit_trail_parser_projection.py::_build_parser`. MOVE EXACT ORIGINAL executable BODY (below) to this new Owner; remove original computation and leave same-signature thin facade wrapper. No duplicate body, no Owner→SOURCE import.
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Check intent->decision->execution audit trail completeness.")
    p.add_argument("--event-log-path", default="data/logs/events.jsonl")
    p.add_argument("--report-dir", default="reports/audit")
    p.add_argument("--day", default=None)
    p.add_argument("--require-actionable", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
```
**THIN WRAPPER / PATCH:** inside SOURCE _build_parser, import scripts.diagnostics.audit_trail_parser_projection as _c03_10_b8_owner; return _c03_10_b8_owner._build_parser(<original positional/keyword arguments>, facade=sys.modules[__name__]). Owner accepts additional keyword-only `facade` and resolves call-time globals **argparse** through `facade` (where `none`, no source-global seam). Owner must preserve original signature semantics, default args, output/error ordering, iterator behavior, copy/alias, and caller monkeypatch behavior. If a function requires globals, do not silently snapshot them at import. Import sys in SOURCE only if absent. No changes to public callers.
**NORMAL TARGETED `test_b8_build_parser`:** parse_args([]) yields event_log_path=data/logs/events.jsonl and report_dir=reports/audit; --day 2026-11-01 --json yields expected fields; patched argparse.ArgumentParser reaches Owner. Capture original golden before editing; compare original vs wrapper vs direct Owner, positive/negative/exception; patch facade globals where applicable. AST check SOURCE has no old computation and TARGET has actual BODY; no cyclic imports. Use only in-memory/fake/temp fixture, never live effects. **BLOCKED→NEXT:** exact SHA/error to #12; continue all other safe items and push.

## CARRYOVER — TWO UNFINISHED PRIOR MOVEs, NOT NEW
## CARRYOVER — ONE UNFINISHED B-06 BODY MOVE (NOT NEW; C2 REMOTE_DONE)
### C1 (B-06 B3 REMAINING, NOT NEW) | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_dataset_manifest_check.py::_seed_demo_dataset` @ L52 | CURRENT_BLOB `c039f3df0b2427e901f07219990c63da70d7b95e`
**TARGET STILL 404 B/integration:** `scripts/diagnostics/m26_manifest_seed_projection.py::_seed_demo_dataset`. Move entire actual body, not stub:
```python
def _seed_demo_dataset(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)

    csv_seed = "ts,symbol,open,high,low,close,volume\n2026-02-17T00:00:00+00:00,005930,70000,70500,69900,70300,120000\n"
    _write_text(root / "market" / "ohlcv_1m.csv", csv_seed)
    _write_text(root / "market" / "ohlcv_5m.csv", csv_seed)
    _write_text(root / "market" / "ohlcv_1d.csv", csv_seed)
    _write_text(
        root / "market" / "corporate_actions.csv",
        "symbol,action,effective_date,ratio\n005930,split,2026-01-15,1.0\n",
    )

    _write_text(
        root / "execution" / "intents.jsonl",
        json.dumps(
            {
                "ts": "2026-02-17T00:01:00+00:00",
                "intent_id": "demo-intent-1",
                "symbol": "005930",
                "action": "BUY",
                "qty": 1,
            },
            ensure_ascii=False,
        )
        + "\n",
    )
    _write_text(
        root / "execution" / "order_status.jsonl",
        json.dumps(
            {
                "ts": "2026-02-17T00:01:05+00:00",
                "intent_id": "demo-intent-1",
                "status": "filled",
            },
            ensure_ascii=False,
        )
        + "\n",
    )
    _write_text(
        root / "execution" / "fills.jsonl",
        json.dumps(
            {
                "ts": "2026-02-17T00:01:05+00:00",
                "intent_id": "demo-intent-1",
                "fill_price": 70300,
                "fill_qty": 1,
            },
            ensure_ascii=False,
        )
        + "\n",
    )

    _write_text(
        root / "microstructure" / "top_of_book.jsonl",
        json.dumps(
            {
                "ts": "2026-02-17T00:00:30+00:00",
                "symbol": "005930",
                "bid": 70200,
                "ask": 70300,
            },
            ensure_ascii=False,
        )
        + "\n",
    )

    _write_text(
        root / "features" / "scanner_monitor_features.jsonl",
        json.dumps(
            {
                "ts": "2026-02-17T00:00:40+00:00",
                "symbol": "005930",
                "features": {"rsi14": 55.2, "ma20_gap": 0.01},
            },
            ensure_ascii=False,
        )
        + "\n",
    )

    _write_text(
        root / "news" / "headlines.jsonl",
        json.dumps(
            {
                "ts": "2026-02-17T00:00:50+00:00",
                "symbol": "005930",
                "title": "demo headline",
            },
            ensure_ascii=False,
        )
        + "\n",
    )
    _write_text(
        root / "news" / "sentiment_by_symbol.jsonl",
        json.dumps(
            {
                "ts": "2026-02-17T00:00:55+00:00",
                "symbol": "005930",
                "sentiment": 0.15,
            },
            ensure_ascii=False,
        )
        + "\n",
    )
    _write_text(
        root / "news" / "sentiment_daily.jsonl",
        json.dumps(
            {
                "ts": "2026-02-17T00:00:59+00:00",
                "market_sentiment": 0.08,
            },
            ensure_ascii=False,
        )
        + "\n",
    )

    manifest: Dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "dataset_id": "m26-fixed-demo-v1",
        "generated_at": _utc_now_iso(),
        "components": {k: list(v) for k, v in REQUIRED_COMPONENT_FILES.items()},
    }
    manifest_path = root / "manifest.json"
    _write_text(manifest_path, json.dumps(manifest, ensure_ascii=False, indent=2))
    return manifest_path
```
**WRAPPER:** original SOURCE signature, unique alias `_b06_c1_owner`, import `scripts.diagnostics.m26_manifest_seed_projection`, sole Owner delegation with `facade=sys.modules[__name__]`. Owner call-time seams: _write_text,_utc_now_iso,json,SCHEMA_VERSION,REQUIRED_COMPONENT_FILES; no real datasets. **NORMAL `test_b3__seed_demo_dataset` in EXISTING `tests/test_p15_rf063_20261101_06h_owners.py`:** Temp root→manifest.json schema_version m26.dataset_manifest.v1 and 12 expected components; fake timestamp; preserve all original CSV/JSONL bytes and file paths; golden vs wrapper vs Owner, AST old BODY removed. BLOCKED→continue B1–B8.

## B-07 REMAINING — SIX INDEPENDENT VERIFIED SOURCE BODY MOVEs (B7/B8 REMOTE_DONE)

## B6 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_closeout_check.py::_prepare_candidate_dataset` @ L96 | CURRENT_BLOB `f9f4ff9c200cf895c8105eb8207723bc13bba1e8`
**NEW TARGET (404 B/integration VERIFIED):** `scripts/diagnostics/m26_closeout_candidate_projection.py::_prepare_candidate_dataset`. MOVE **COMPLETE executable body below** into Owner with original signature + keyword-only facade; keep original SOURCE signature and replace with thin wrapper only.
```python
def _prepare_candidate_dataset(candidate_root: Path, *, day: str) -> None:
    # Overwrite candidate timeline so candidate clearly outperforms baseline on realized PnL.
    _write_jsonl(
        candidate_root / "execution" / "intents.jsonl",
        [
            {"ts": f"{day}T00:01:00+00:00", "intent_id": "c-intent-1", "symbol": "005930", "action": "BUY", "qty": 1},
            {"ts": f"{day}T00:02:00+00:00", "intent_id": "c-intent-2", "symbol": "005930", "action": "SELL", "qty": 1},
        ],
    )
    _write_jsonl(
        candidate_root / "execution" / "order_status.jsonl",
        [
            {"ts": f"{day}T00:01:05+00:00", "intent_id": "c-intent-1", "status": "filled"},
            {"ts": f"{day}T00:02:05+00:00", "intent_id": "c-intent-2", "status": "filled"},
        ],
    )
    _write_jsonl(
        candidate_root / "execution" / "fills.jsonl",
        [
            {"ts": f"{day}T00:01:05+00:00", "intent_id": "c-intent-1", "fill_price": 100, "fill_qty": 1},
            {"ts": f"{day}T00:02:05+00:00", "intent_id": "c-intent-2", "fill_price": 115, "fill_qty": 1},
        ],
    )
    (candidate_root / "market" / "ohlcv_1d.csv").write_text(
        f"ts,symbol,open,high,low,close,volume\n{day}T00:00:00+00:00,005930,100,116,99,115,1000\n",
        encoding="utf-8",
    )
```
**THIN WRAPPER / MONKEYPATCH:** SOURCE local import `scripts.diagnostics.m26_closeout_candidate_projection as _b07_6_owner`, sole `return _b07_6_owner._prepare_candidate_dataset(<original args forwarded>, facade=sys.modules[__name__])`; unique alias avoids collisions. Owner must not import SOURCE. Resolve listed call-time globals through facade: _write_jsonl,Path methods. Preserve output/exception, nested function, JSON order, CLI args and side-effect boundaries. 
**NORMAL TARGETED `test_b6__prepare_candidate_dataset`:** TemporaryDirectory precreate execution/ and market/; fake _write_jsonl captures 3 file groups; market/ohlcv_1d.csv close=115 vs open=100, no operational path. Compare original-golden vs wrapper vs direct Owner, positive/negative/exception, patched facade, AST SOURCE old BODY removed. **BLOCKED→NEXT:** record exact error/SHA; continue remaining safe B1–B6 and C1.



## FUTURE RESERVE — RESERVE_NOT_VERIFIED 0/6 (DESIGN ONLY, NOT EXECUTABLE)
All six previously VERIFIED candidates have been promoted into this executable order and cannot be reused as future reserve. RESERVE_NOT_VERIFIED 0/6: next analyze RF-063 audit analyzer/read-model pure subfunctions and separate diagnostic sources; validate source and target on both refs before VERIFIED. Do not infer safe new functions from names alone. Next C03 must independently inspect new SOURCE BODY/blob, Owner exclusivity, target 404 on both refs, effect/monkeypatch, normal fixture before issuing or marking VERIFIED.

**COUNTS:** previous REMOTE_DONE as above; NEW_READY=8 actual source BODY MOVEs, FUTURE_RESERVE_VERIFIED=0/6; C03 DOC_ONLY code G1/G2/G3=0 and RF_DONE_DELTA=0. RunLab Exited(255), RUN_SOURCE_SHA=UNKNOWN; do not touch runtime.
