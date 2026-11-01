# C01 — Codex B | B-20261101-11 | FAST-3 8 NEW VERIFIED BODY MOVEs + 4 UNFINISHED CARRYOVERS

**SINGLE ENTRY / PIN:** At start pin CANONICAL_HEAD, ORDER_FILE_BLOB_SHA, OWNER_REMOTE_SHA, ORDER_ID=B-20261101-11. Read THIS document and named code/test only. Do not read D00/RF/queue/C03/CURRENT/HANDOFF or self-select. Complete ALL NEW B1–B8 plus CARRYOVER K1–K4 (or per-item evidence BLOCKED); one PASS/first commit/short time is not stop. Pinned old start order remains valid. C03 DOC_ONLY does not count as code G1/G2/G3.

**REMOTE_DONE:** Previous B-10 B1–B6 = 6/8 REMOTE_DONE at B HEAD `cf39d797b581ebd4712eee194805a7c640146779`, normal 6/6 exit0, #12 6551645639. Old B7 `_build_markdown`, B8 `_build_parser`, older C1 `_seed_demo_dataset` and B-07 B6 `_prepare_candidate_dataset` remain source BODY, CARRYOVER 4, not new. No old PASS reruns on same SHA; only missing targeted cases. NEW_READY=8 separately. Current B HEAD `cf39d797b581ebd4712eee194805a7c640146779`; canonical HEAD must be refreshed by actor at start.

**RF/OWNER/SAFETY:** RF-063 CODEX_B exclusive. Only `scripts/diagnostics/check_log_archive_integrity.py`, `run_m27_allocation_policy_check.py`, `run_m27_conflict_resolution_check.py`, `check_audit_trail_completeness.py`, `run_m26_dataset_manifest_check.py`, `run_m26_closeout_check.py` (all under scripts/diagnostics), their named new target projection files, and `tests/test_p15_rf063_20261101_11h_diagnostic_owners.py` plus carryover 06h/07h/10h test files writable. These functions are diagnostic formatting, fake M27 fixture construction, CLI argument parsers, and isolated temporary fixture writers. NEVER execute actual trading/portfolio guard/broker/Step5C/UEF, RunLab, live filesystem or network; no real orders or real state. Do not alter D00/RF/STATUS/queue/C04/C05/other actor, frozen tests, CI workflows, live configuration, real policy semantics or force-push. All tests fake argv/dicts/TemporaryDirectory; no `main()` that invokes guard/allocation or writes operational reports.

**BODY/WRAPPER:** For each B1–B8 move complete exact original executable BODY below to one new target Owner (add required stdlib/typing imports); original SOURCE keeps same signature and only a local-import thin delegation to unique alias `_c03_11_bN_owner`, with `facade=sys.modules[__name__]` for call-time global/monkeypatch parity. Add `import sys` in SOURCE only if missing. Owner accepts keyword-only `facade`, resolves listed SOURCE globals at call time (e.g. `facade.argparse`, `facade.datetime`); no Owner→SOURCE import or duplicate calculation. Preserve argv flags, defaults, exceptions, return/copy/order and facade monkeypatch. Capture original golden before edit, AST confirm BODY removed, original vs wrapper vs Owner on fake inputs.

**TEST/PUSH:** Add 8 independent `unittest` cases to `tests/test_p15_rf063_20261101_11h_diagnostic_owners.py`; normal `python -m unittest tests/test_p15_rf063_20261101_11h_diagnostic_owners.py -v` expected exit0/8 tests (NOT_RUN at publication). Missing carryover tests in `tests/test_p15_rf063_20261101_10h_audit_owners.py` (B7/B8), `tests/test_p15_rf063_20261101_06h_owners.py` (K3), `tests/test_p15_rf063_20261101_07h_owners.py` (K4); do not count old PASS as new. Commit only allowed actor code/test, normal non-force push or approved expected-HEAD lease, re-fetch B HEAD and SOURCE/TARGET/test blobs, report each item, normal exit and measured START/END/ELAPSED to #12. Git auth failure=PUSH_BLOCKED only; continue safe local work. C04 integrates and C05 G1/G2/G3/STATUS; no C03 code achievement.

## B1 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_log_archive_integrity.py::_parse_day` @ L38 | CURRENT_BLOB `d1f0b80eb488188d70e30a78f227a1f289f1d2f5`
**TARGET (404 both refs VERIFIED):** `scripts/diagnostics/archive_integrity_day_projection.py::_parse_day`; actual original BODY to move, not KEEP or copy:
```python
def _parse_day(value: str) -> Optional[date]:
    s = str(value or "").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None
```
**THIN WRAPPER/PATCH:** `_parse_day(...)` delegates via `_c03_11_b1_owner._parse_day(..., facade=sys.modules[__name__])`; Owner call-time globals: datetime. Do not call original CLI main; preserve source import and caller monkeypatch. No production effects.
**TARGETED `test_b1__parse_day`:** '2026-11-01' -> date(2026,11,1); bad/empty -> None; patched SOURCE.datetime.strptime reaches Owner. Compare original golden, wrapper and Owner with normal/negative/exception and AST check. **BLOCKED→NEXT:** record exact SHA/error to #12, continue B2.

## B2 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_log_archive_integrity.py::_markdown` @ L48 | CURRENT_BLOB `d1f0b80eb488188d70e30a78f227a1f289f1d2f5`
**TARGET (404 both refs VERIFIED):** `scripts/diagnostics/archive_integrity_markdown_projection.py::_markdown`; actual original BODY to move, not KEEP or copy:
```python
def _markdown(out: Dict[str, Any]) -> str:
    lines = [
        f"# Log Archive Integrity ({out.get('day')})",
        "",
        f"- ok: **{bool(out.get('ok'))}**",
        f"- archive_dir: `{out.get('archive_dir')}`",
        f"- manifest_path: `{out.get('manifest_path')}`",
        f"- file_total: **{int(out.get('file_total') or 0)}**",
        f"- verified_total: **{int(out.get('verified_total') or 0)}**",
        "",
        "## Integrity Totals",
        "",
        f"- missing_file_total: {int(out.get('missing_file_total') or 0)}",
        f"- hash_mismatch_total: {int(out.get('hash_mismatch_total') or 0)}",
        f"- bytes_mismatch_total: {int(out.get('bytes_mismatch_total') or 0)}",
        f"- line_count_mismatch_total: {int(out.get('line_count_mismatch_total') or 0)}",
        "",
        "## Retention",
        "",
        f"- retention_days: {int(out.get('retention_days') or 0)}",
        f"- stale_archive_total: {int(out.get('stale_archive_total') or 0)}",
    ]
    stale = out.get("stale_archive_days") if isinstance(out.get("stale_archive_days"), list) else []
    if stale:
        lines.append(f"- stale_archive_days: {', '.join(str(x) for x in stale)}")
    else:
        lines.append("- stale_archive_days: (none)")
    lines += ["", "## Failures", ""]
    failures = out.get("failures") if isinstance(out.get("failures"), list) else []
    if failures:
        for msg in failures:
            lines.append(f"- {msg}")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)
```
**THIN WRAPPER/PATCH:** `_markdown(...)` delegates via `_c03_11_b2_owner._markdown(..., facade=sys.modules[__name__])`; Owner call-time globals: none. Do not call original CLI main; preserve source import and caller monkeypatch. No production effects.
**TARGETED `test_b2__markdown`:** {'day':'2026-11-01','ok':True,'file_total':0,'failures':[]} -> heading '# Log Archive Integrity (2026-11-01)', '(none)' failures and terminal newline; stale days deterministic. Compare original golden, wrapper and Owner with normal/negative/exception and AST check. **BLOCKED→NEXT:** record exact SHA/error to #12, continue B3.

## B3 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_log_archive_integrity.py::_build_parser` @ L86 | CURRENT_BLOB `d1f0b80eb488188d70e30a78f227a1f289f1d2f5`
**TARGET (404 both refs VERIFIED):** `scripts/diagnostics/archive_integrity_parser_projection.py::_build_parser`; actual original BODY to move, not KEEP or copy:
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Check archive manifest/hash integrity and retention policy.")
    p.add_argument("--archive-dir", default="data/logs/archive")
    p.add_argument("--report-dir", default="reports/archive_integrity")
    p.add_argument("--day", default=None)
    p.add_argument("--retention-days", type=int, default=30)
    p.add_argument("--allow-stale", action="store_true", help="Do not fail on stale archive days.")
    p.add_argument("--json", action="store_true")
    return p
```
**THIN WRAPPER/PATCH:** `_build_parser(...)` delegates via `_c03_11_b3_owner._build_parser(..., facade=sys.modules[__name__])`; Owner call-time globals: argparse. Do not call original CLI main; preserve source import and caller monkeypatch. No production effects.
**TARGETED `test_b3__build_parser`:** parse_args([]) -> retention_days=30, archive_dir='data/logs/archive'; --retention-days 7 --json -> 7,True. Compare original golden, wrapper and Owner with normal/negative/exception and AST check. **BLOCKED→NEXT:** record exact SHA/error to #12, continue B4.

## B4 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m27_allocation_policy_check.py::_build_parser` @ L16 | CURRENT_BLOB `bb39094be47fb5da438b65a1107ffa260b761407`
**TARGET (404 both refs VERIFIED):** `scripts/diagnostics/m27_allocation_parser_projection.py::_build_parser`; actual original BODY to move, not KEEP or copy:
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M27-1 multi-strategy allocation policy check.")
    p.add_argument("--total-notional", type=float, default=1_000_000)
    p.add_argument("--reserve-ratio", type=float, default=0.1)
    p.add_argument("--json", action="store_true")
    return p
```
**THIN WRAPPER/PATCH:** `_build_parser(...)` delegates via `_c03_11_b4_owner._build_parser(..., facade=sys.modules[__name__])`; Owner call-time globals: argparse. Do not call original CLI main; preserve source import and caller monkeypatch. No production effects.
**TARGETED `test_b4__build_parser`:** parse_args([]) -> total_notional=1000000, reserve_ratio=.1; --total-notional 200 --json -> 200,True. Compare original golden, wrapper and Owner with normal/negative/exception and AST check. **BLOCKED→NEXT:** record exact SHA/error to #12, continue B5.

## B5 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m27_allocation_policy_check.py::_default_profiles` @ L24 | CURRENT_BLOB `bb39094be47fb5da438b65a1107ffa260b761407`
**TARGET (404 both refs VERIFIED):** `scripts/diagnostics/m27_allocation_profiles_projection.py::_default_profiles`; actual original BODY to move, not KEEP or copy:
```python
def _default_profiles() -> List[Dict[str, Any]]:
    return [
        {"strategy_id": "trend", "enabled": True, "weight": 0.6, "max_notional_ratio": 0.7},
        {"strategy_id": "mean_reversion", "enabled": True, "weight": 0.3, "max_notional_ratio": 0.4},
        {"strategy_id": "event_driven", "enabled": True, "weight": 0.1, "max_notional_ratio": 0.2},
    ]
```
**THIN WRAPPER/PATCH:** `_default_profiles(...)` delegates via `_c03_11_b5_owner._default_profiles(..., facade=sys.modules[__name__])`; Owner call-time globals: none. Do not call original CLI main; preserve source import and caller monkeypatch. No production effects.
**TARGETED `test_b5__default_profiles`:** 3 rows, strategy_id trend/mean_reversion/event_driven, weights .6/.3/.1, max ratios .7/.4/.2; returned list is fresh. Compare original golden, wrapper and Owner with normal/negative/exception and AST check. **BLOCKED→NEXT:** record exact SHA/error to #12, continue B6.

## B6 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m27_conflict_resolution_check.py::_build_parser` @ L16 | CURRENT_BLOB `3d550fe979019be37f15dbe968ca2ccd35348f13`
**TARGET (404 both refs VERIFIED):** `scripts/diagnostics/m27_conflict_parser_projection.py::_build_parser`; actual original BODY to move, not KEEP or copy:
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M27-2 intent conflict resolution policy check.")
    p.add_argument("--json", action="store_true")
    p.add_argument("--inject-fail", action="store_true")
    return p
```
**THIN WRAPPER/PATCH:** `_build_parser(...)` delegates via `_c03_11_b6_owner._build_parser(..., facade=sys.modules[__name__])`; Owner call-time globals: argparse. Do not call original CLI main; preserve source import and caller monkeypatch. No production effects.
**TARGETED `test_b6__build_parser`:** parse_args([]) -> inject_fail False; --inject-fail --json -> both True. Compare original golden, wrapper and Owner with normal/negative/exception and AST check. **BLOCKED→NEXT:** record exact SHA/error to #12, continue B7.

## B7 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m27_conflict_resolution_check.py::_default_intents` @ L23 | CURRENT_BLOB `3d550fe979019be37f15dbe968ca2ccd35348f13`
**TARGET (404 both refs VERIFIED):** `scripts/diagnostics/m27_conflict_intents_projection.py::_default_intents`; actual original BODY to move, not KEEP or copy:
```python
def _default_intents(*, inject_fail: bool) -> List[Dict[str, Any]]:
    if inject_fail:
        # no opposite-side conflict and no cap overflow on purpose.
        return [
            {
                "intent_id": "i1",
                "strategy_id": "trend",
                "symbol": "005930",
                "side": "BUY",
                "qty": 1,
                "price": 100,
                "priority": 9,
                "confidence": 0.9,
            },
            {
                "intent_id": "i2",
                "strategy_id": "mean_reversion",
                "symbol": "000660",
                "side": "BUY",
                "qty": 1,
                "price": 100,
                "priority": 8,
                "confidence": 0.8,
            },
        ]

    return [
        {
            "intent_id": "i1",
            "strategy_id": "trend",
            "symbol": "005930",
            "side": "BUY",
            "qty": 1,
            "price": 100,
            "priority": 9,
            "confidence": 0.9,
        },
        {
            "intent_id": "i2",
            "strategy_id": "mean_reversion",
            "symbol": "005930",
            "side": "SELL",
            "qty": 1,
            "price": 100,
            "priority": 3,
            "confidence": 0.4,
        },
        {
            "intent_id": "i3",
            "strategy_id": "event_driven",
            "symbol": "000660",
            "side": "BUY",
            "qty": 4,
            "price": 40,
            "priority": 8,
            "confidence": 0.8,
        },
        {
            "intent_id": "i4",
            "strategy_id": "trend",
            "symbol": "000660",
            "side": "BUY",
            "qty": 3,
            "price": 40,
            "priority": 2,
            "confidence": 0.4,
        },
    ]
```
**THIN WRAPPER/PATCH:** `_default_intents(...)` delegates via `_c03_11_b7_owner._default_intents(..., facade=sys.modules[__name__])`; Owner call-time globals: none. Do not call original CLI main; preserve source import and caller monkeypatch. No production effects.
**TARGETED `test_b7__default_intents`:** inject_fail=False -> 4 intents including opposing BUY/SELL on 005930; True -> 2 BUY intents on distinct symbols; fresh list. Compare original golden, wrapper and Owner with normal/negative/exception and AST check. **BLOCKED→NEXT:** record exact SHA/error to #12, continue B8.

## B8 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m27_conflict_resolution_check.py::_default_caps` @ L93 | CURRENT_BLOB `3d550fe979019be37f15dbe968ca2ccd35348f13`
**TARGET (404 both refs VERIFIED):** `scripts/diagnostics/m27_conflict_caps_projection.py::_default_caps`; actual original BODY to move, not KEEP or copy:
```python
def _default_caps(*, inject_fail: bool) -> Dict[str, float]:
    if inject_fail:
        return {"005930": 1_000_000.0, "000660": 1_000_000.0}
    return {"005930": 1_000_000.0, "000660": 200.0}
```
**THIN WRAPPER/PATCH:** `_default_caps(...)` delegates via `_c03_11_b8_owner._default_caps(..., facade=sys.modules[__name__])`; Owner call-time globals: none. Do not call original CLI main; preserve source import and caller monkeypatch. No production effects.
**TARGETED `test_b8__default_caps`:** inject_fail=False -> {'005930':1000000.,'000660':200.}; True -> 000660:1000000.. Compare original golden, wrapper and Owner with normal/negative/exception and AST check. **BLOCKED→NEXT:** record exact SHA/error to #12, continue all remaining carryovers.

## CARRYOVER — 4 ACTUAL UNFINISHED BODY MOVEs (NOT NEW_READY; MUST COMPLETE)

### K1 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_build_markdown` @ L184 | CURRENT_BLOB `fa531aebeeb1ff6d72905bc1b50be96721b94d4e`
**TARGET (404 both refs):** `scripts/diagnostics/audit_trail_markdown_projection.py::_build_markdown`; previous order pending, not new. Move COMPLETE actual body below, original thin wrapper with call-time facade and no duplicate body:
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
**WRAPPER/PATCH:** SOURCE original signature; unique alias `_c03_11_k1_owner` local import, sole Owner delegation with `facade=sys.modules[__name__]`; Owner call-time globals none; preserve errors, outputs, mutation, order, effects in isolated temp ONLY.
**NORMAL TARGETED:** add missing `test_k1__build_markdown` in `tests/test_p15_rf063_20261101_10h_audit_owners.py`: day=2026-11-01,out={ok:True,events:0} -> header, no failures, terminal newline; fake in-memory. Golden original vs wrapper/Owner, AST check; run that exact file via `python -m unittest tests/test_p15_rf063_20261101_10h_audit_owners.py -v` expecting full original+new suite exit0, no stale PASS reuse. **BLOCKED→NEXT:** exact reason to #12; continue next safe carryover/new item.

### K2 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_build_parser` @ L237 | CURRENT_BLOB `fa531aebeeb1ff6d72905bc1b50be96721b94d4e`
**TARGET (404 both refs):** `scripts/diagnostics/audit_trail_parser_projection.py::_build_parser`; previous order pending, not new. Move COMPLETE actual body below, original thin wrapper with call-time facade and no duplicate body:
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
**WRAPPER/PATCH:** SOURCE original signature; unique alias `_c03_11_k2_owner` local import, sole Owner delegation with `facade=sys.modules[__name__]`; Owner call-time globals argparse; preserve errors, outputs, mutation, order, effects in isolated temp ONLY.
**NORMAL TARGETED:** add missing `test_k2__build_parser` in `tests/test_p15_rf063_20261101_10h_audit_owners.py`: parse_args([]) -> event_log_path='data/logs/events.jsonl'; --day 2026-11-01 --json -> expected fields. Golden original vs wrapper/Owner, AST check; run that exact file via `python -m unittest tests/test_p15_rf063_20261101_10h_audit_owners.py -v` expecting full original+new suite exit0, no stale PASS reuse. **BLOCKED→NEXT:** exact reason to #12; continue next safe carryover/new item.

### K3 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_dataset_manifest_check.py::_seed_demo_dataset` @ L52 | CURRENT_BLOB `c039f3df0b2427e901f07219990c63da70d7b95e`
**TARGET (404 both refs):** `scripts/diagnostics/m26_manifest_seed_projection.py::_seed_demo_dataset`; previous order pending, not new. Move COMPLETE actual body below, original thin wrapper with call-time facade and no duplicate body:
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
**WRAPPER/PATCH:** SOURCE original signature; unique alias `_c03_11_k3_owner` local import, sole Owner delegation with `facade=sys.modules[__name__]`; Owner call-time globals _write_text,_utc_now_iso,json,SCHEMA_VERSION,REQUIRED_COMPONENT_FILES; preserve errors, outputs, mutation, order, effects in isolated temp ONLY.
**NORMAL TARGETED:** add missing `test_k3__seed_demo_dataset` in `tests/test_p15_rf063_20261101_06h_owners.py`: TemporaryDirectory -> manifest.json, all original CSV/JSONL bytes and 12 component paths; fake _utc_now_iso, no real files. Golden original vs wrapper/Owner, AST check; run that exact file via `python -m unittest tests/test_p15_rf063_20261101_06h_owners.py -v` expecting full original+new suite exit0, no stale PASS reuse. **BLOCKED→NEXT:** exact reason to #12; continue next safe carryover/new item.

### K4 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_closeout_check.py::_prepare_candidate_dataset` @ L63 | CURRENT_BLOB `f9f4ff9c200cf895c8105eb8207723bc13bba1e8`
**TARGET (404 both refs):** `scripts/diagnostics/m26_closeout_candidate_projection.py::_prepare_candidate_dataset`; previous order pending, not new. Move COMPLETE actual body below, original thin wrapper with call-time facade and no duplicate body:
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
**WRAPPER/PATCH:** SOURCE original signature; unique alias `_c03_11_k4_owner` local import, sole Owner delegation with `facade=sys.modules[__name__]`; Owner call-time globals _write_jsonl; preserve errors, outputs, mutation, order, effects in isolated temp ONLY.
**NORMAL TARGETED:** add missing `test_k4__prepare_candidate_dataset` in `tests/test_p15_rf063_20261101_07h_owners.py`: TemporaryDirectory with market/ and execution/ precreated; fake _write_jsonl; candidate market close=115 vs open=100. Golden original vs wrapper/Owner, AST check; run that exact file via `python -m unittest tests/test_p15_rf063_20261101_07h_owners.py -v` expecting full original+new suite exit0, no stale PASS reuse. **BLOCKED→NEXT:** exact reason to #12; continue next safe carryover/new item.

## FUTURE RESERVE — VERIFIED 6/6 (DESIGN ONLY; NOT EXECUTABLE)

- **R1 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_build_parser` @ L17, current blob `e8c050b18e8a523becf28db5c6c0f22198f46f37`; TARGET `scripts/diagnostics/m27_budget_parser_projection.py::_build_parser` absent on B/integration. Original actual BODY confirmed: `p = argparse.ArgumentParser(description="M27-3 portfolio budget boundary check.") p.add_argument("--json", action="store_true") p.add_argument("--inject-fail", action="store_true")` (not a wrapper). Call-time facade argparse; fake in-memory test [] -> inject_fail False, --inject-fail True. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R2 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_profiles` @ L24, current blob `e8c050b18e8a523becf28db5c6c0f22198f46f37`; TARGET `scripts/diagnostics/m27_budget_profiles_projection.py::_profiles` absent on B/integration. Original actual BODY confirmed: `return [ {"strategy_id": "trend", "enabled": True, "weight": 0.5}, {"strategy_id": "mean_reversion", "enabled": True, "weight": 0.3},` (not a wrapper). Call-time facade none; fake in-memory test 3 profiles, weights .5/.3/.2. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R3 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_intents` @ L32, current blob `e8c050b18e8a523becf28db5c6c0f22198f46f37`; TARGET `scripts/diagnostics/m27_budget_intents_projection.py::_intents` absent on B/integration. Original actual BODY confirmed: `if inject_fail: return [ {` (not a wrapper). Call-time facade none; fake in-memory test normal 5 intents, inject_fail 2 intents; in-memory only, no guard call. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R4 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_symbol_caps` @ L104, current blob `e8c050b18e8a523becf28db5c6c0f22198f46f37`; TARGET `scripts/diagnostics/m27_budget_caps_projection.py::_symbol_caps` absent on B/integration. Original actual BODY confirmed: `if inject_fail: return {"005930": 10_000.0, "000660": 10_000.0} return {"005930": 10_000.0, "000660": 500.0}` (not a wrapper). Call-time facade none; fake in-memory test normal 000660=500; inject_fail 000660=10000. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R5 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_closeout_check.py::_build_parser` @ L30, current blob `1f48a79ecff887921682f180a1a3aa9214795416`; TARGET `scripts/diagnostics/m27_closeout_parser_projection.py::_build_parser` absent on B/integration. Original actual BODY confirmed: `p = argparse.ArgumentParser(description="M27 closeout check (allocation/conflict/guard/metrics/notify).") p.add_argument("--event-log-dir", default="data/logs/m27_closeout") p.add_argument("--report-dir", default="reports/m27_closeout")` (not a wrapper). Call-time facade argparse; fake in-memory test parse_args([]) default event-log-dir, parse_args(['--json']) sets json=True. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R6 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m29_closeout_check.py::_build_parser` @ L25, current blob `ac491cb4ec89ff72ed64d9466055f06f936019f3`; TARGET `scripts/diagnostics/m29_closeout_parser_projection.py::_build_parser` absent on B/integration. Original actual BODY confirmed: `p = argparse.ArgumentParser(description="M29 governance closeout check (audit/archive/timeline/dr).") p.add_argument("--event-log-dir", default="data/logs/m29_closeout") p.add_argument("--report-dir", default="reports/m29_closeout")` (not a wrapper). Call-time facade argparse; fake in-memory test parse_args([]) default day=None or declared default; --json=True, fake argv only. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.

**COUNTS:** previous B-10 REMOTE_DONE=6/8, CARRYOVER_PENDING=4 (old B7/B8 and older C1/B6); NEW_READY=8 actual independent SOURCE BODY MOVEs; FUTURE_RESERVE_VERIFIED=6/6; actor tests NOT_RUN at issuance, C03 DOC_ONLY code G1/G2/G3=0 and RF_DONE_DELTA=0. RunLab Exited(255), RUN_SOURCE_SHA=UNKNOWN, no runtime action.
