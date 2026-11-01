# C01 — Codex B | B-20261101-12 | NEW RF DONE FIRST: RF-063 EIGHT RESIDUAL SAFE MOVEs (4 CLOSEOUT K + 4 B11), NO DUPLICATE PASS

**ONE-FILE ENTRY / PIN:** At start record CANONICAL_HEAD, ORDER_FILE_BLOB_SHA, B_OWNER_REMOTE_SHA, ORDER_ID=B-20261101-12. Read THIS C01 and named code/tests only; no D00/RF/queue/C03/CURRENT/HANDOFF, no self-selection. Previous B-20261101-11 pinned order remains valid for its own in-flight start; this update is for next start. No C03 code execution. Git auth/pytest failure blocks only respective push/test, not other safe items.

**LATEST VERIFIED REMOTE:** B HEAD `744e4fe4d74ef9fd5b3dd6a750617819339c7d42` (#12 6552184419). B-11 B4 allocation parser, B5 profiles, B6 conflict parser, B8 caps = 4/8 **REMOTE_DONE**, normal 4/4 exit0, C04 integrated exact `60a51f8c6742d45b0c9c37b0be606798f6501e53`, C05 scoped accepted; these four are **NOT assigned again**. Unfinished B-11 B1–B3 archive, B7 conflict intents plus prior K1 audit markdown/K2 audit parser/K3 dataset seed/K4 candidate preparation = **8 real SOURCE BODY MOVEs still in place**, safe independent queue >=6. They are CARRYOVER/UNFINISHED, **NEW_READY=0**, not new eight successes. Do not create a second 8-item supply while eight genuine safe items remain. C03 directs exact order below; do not choose other RF.

**DIRECT CLOSEOUT PRIORITY:** RF-063 CODEX_B, physical 02_DEVELOPING, G1/G2/G3 whole-RF PARTIAL. Work **K1,K2,K3,K4 FIRST** because they are identified first G1 gaps for DONE. Then B1,B2,B3,B7. Do not repeat previously passed same SHA tests. The earlier B-04 integrated-source G3 and B1 normal G2, populated-manifest original-vs-Owner golden/exception parity remain OPEN and require exact scoped new evidence; do not assert RF DONE after partial G3. C04 selectively integrates each code chunk; C05 alone accepts G1/G2/G3 and moves RF/STATUS. No automatic full peer/-O/per-RF CI gate.

**OWNER/SAFETY:** RF-063 only, CODEX_B exclusive `scripts/diagnostics/` SOURCE paths enumerated below and eight new target modules in each item; code and `tests/test_p15_rf063_20261101_12h_residual_owners.py` only. No other actor code, D00/C03/C04/C05/RF/STATUS/queue, frozen tests, CI/security policy, or force push. Use fake argv/dicts/TemporaryDirectory only. Never run any diagnostic `main()` that can invoke live portfolio, Broker, Guard, Step5C, UEF, RunLab, operational State or real filesystem/network. No real orders/restarts/deploys. If IO is required by K3/K4, route every read/write to TemporaryDirectory and patch any facade paths. On any transitive effect/owner ambiguity SAFETY_BLOCKED for that item; continue others.

**BODY/WRAPPER:** Every item below includes its original executable BODY, exact SOURCE blob, exclusive TARGET and targeted expected inputs. Move actual BODY once to the single new Owner, replace SOURCE with same-signature thin local-import delegation via `facade=sys.modules[__name__]` when required. No duplicate implementation. Preserve use-time globals/monkeypatch, return values, exceptions, copy/mutation, parser defaults and original consumer. Compare ORIGINAL golden captured before edit with wrapper/Owner on fake fixtures; AST verify source computation removed. The K3/K4 seeded file functions may be large: preserve exact temp-only semantics and exception paths; never truncate their BODY.

**TEST / DELIVERY:** New test file `tests/test_p15_rf063_20261101_12h_residual_owners.py`, 8 individually named `test_k1_*`, `test_k2_*`, `test_k3_*`, `test_k4_*`, `test_b1_*`, `test_b2_*`, `test_b3_*`, `test_b7_*`. Normal `python -m unittest tests/test_p15_rf063_20261101_12h_residual_owners.py -v` expected 8/8 exit0 **NOT_RUN at publication**. Use exact old-vs-new golden, negative/exception, fake/temp and parser argv. Do not rerun old B4/B5/B6/B8 or previously passed tests on same SHA. If a new test fails, fix within RF-063 scope or report per-item blocker; continue remaining safe items. Commit only B-owned code/test, normal non-force push or approved expected-HEAD lease, re-fetch B HEAD and changed source/Owner/test blobs, report each item/exit/actual measured times to #12. Git push failure=PUSH_BLOCKED, no local-only G1 claim.

## CLOSEOUT-FIRST — FOUR OLDER G1 GAPS (K1–K4; NOT NEW_READY)

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

## SECOND — FOUR UNFINISHED B-11 ITEMS (B1/B2/B3/B7; NOT NEW_READY)

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

## B7 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m27_conflict_resolution_check.py::_default_intents` @ L21 | CURRENT_BLOB `f5ccbc0d12ea0cf594539482a97cf64a9ef9ad9b`
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

## FUTURE RESERVE — VERIFIED 6/6 (DESIGN ONLY; NOT EXECUTABLE)

- **R1 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_build_parser` @ L17, current blob `e8c050b18e8a523becf28db5c6c0f22198f46f37`; TARGET `scripts/diagnostics/m27_budget_parser_projection.py::_build_parser` absent on B/integration. Original actual BODY confirmed: `p = argparse.ArgumentParser(description="M27-3 portfolio budget boundary check.") p.add_argument("--json", action="store_true") p.add_argument("--inject-fail", action="store_true")` (not a wrapper). Call-time facade argparse; fake in-memory test [] -> inject_fail False, --inject-fail True. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R2 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_profiles` @ L24, current blob `e8c050b18e8a523becf28db5c6c0f22198f46f37`; TARGET `scripts/diagnostics/m27_budget_profiles_projection.py::_profiles` absent on B/integration. Original actual BODY confirmed: `return [ {"strategy_id": "trend", "enabled": True, "weight": 0.5}, {"strategy_id": "mean_reversion", "enabled": True, "weight": 0.3},` (not a wrapper). Call-time facade none; fake in-memory test 3 profiles, weights .5/.3/.2. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R3 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_intents` @ L32, current blob `e8c050b18e8a523becf28db5c6c0f22198f46f37`; TARGET `scripts/diagnostics/m27_budget_intents_projection.py::_intents` absent on B/integration. Original actual BODY confirmed: `if inject_fail: return [ {` (not a wrapper). Call-time facade none; fake in-memory test normal 5 intents, inject_fail 2 intents; in-memory only, no guard call. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R4 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_symbol_caps` @ L104, current blob `e8c050b18e8a523becf28db5c6c0f22198f46f37`; TARGET `scripts/diagnostics/m27_budget_caps_projection.py::_symbol_caps` absent on B/integration. Original actual BODY confirmed: `if inject_fail: return {"005930": 10_000.0, "000660": 10_000.0} return {"005930": 10_000.0, "000660": 500.0}` (not a wrapper). Call-time facade none; fake in-memory test normal 000660=500; inject_fail 000660=10000. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R5 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m27_closeout_check.py::_build_parser` @ L30, current blob `1f48a79ecff887921682f180a1a3aa9214795416`; TARGET `scripts/diagnostics/m27_closeout_parser_projection.py::_build_parser` absent on B/integration. Original actual BODY confirmed: `p = argparse.ArgumentParser(description="M27 closeout check (allocation/conflict/guard/metrics/notify).") p.add_argument("--event-log-dir", default="data/logs/m27_closeout") p.add_argument("--report-dir", default="reports/m27_closeout")` (not a wrapper). Call-time facade argparse; fake in-memory test parse_args([]) default event-log-dir, parse_args(['--json']) sets json=True. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.
- **R6 RF-063 CODEX_B VERIFIED:** SOURCE `scripts/diagnostics/run_m29_closeout_check.py::_build_parser` @ L25, current blob `ac491cb4ec89ff72ed64d9466055f06f936019f3`; TARGET `scripts/diagnostics/m29_closeout_parser_projection.py::_build_parser` absent on B/integration. Original actual BODY confirmed: `p = argparse.ArgumentParser(description="M29 governance closeout check (audit/archive/timeline/dr).") p.add_argument("--event-log-dir", default="data/logs/m29_closeout") p.add_argument("--report-dir", default="reports/m29_closeout")` (not a wrapper). Call-time facade argparse; fake in-memory test parse_args([]) default day=None or declared default; --json=True, fake argv only. No actual guard/allocation/main invocation. NOT EXECUTABLE until C03 revalidates and promotes.

**COUNT / FIRST_BLOCKER / NEXT:** B-11 4/8 REMOTE_DONE; eight unfinished independent safe MOVE items (K1–K4,B1–B3,B7) with SOURCE BODY not yet moved. CURRENT_READY=8, NEW_READY=0 (carryovers only), RESERVE_VERIFIED=6/6 DESIGN_ONLY; do not count old PASS. FIRST_BLOCKER for RF-063 whole-DONE = remaining G1 BODY and populated-manifest parity, then older B-04 G3/B1 normal G2; C04/C05 handle G3/DONE. If any K item cannot preserve temp IO, record SAFETY_BLOCKED and continue B1/B2/B3/B7; next C03 must replace when <6 safe items. RF-065 G1 KEEP/CLI effect and RF-044 facade are next **unassigned** B-owned closeout candidates, not actor self-selection. C03 DOC_ONLY RF_DONE_DELTA=0. RunLab Exited(255), RUN_SOURCE_SHA UNKNOWN, operational HOLD.
