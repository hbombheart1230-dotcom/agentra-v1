# C01 — Codex B | B-20261101-07 REMAINING | FAST-3 SIX VERIFIED BODY MOVEs + ONE B-06 CARRYOVER

**SINGLE ENTRY.** At start pin integration HEAD, C01 blob, B owner HEAD and ORDER_ID. Read this C01 and named code/test only; never D00/RF/queue/C03/CURRENT/HANDOFF. Execute remaining carryover C1 and ALL REMAINING B1–B6; if one blocked continue every other safe item. Previously pinned start order is not retroactively cancelled.

**REMOTE_DONE:** B-20261101-07 B7 `_to_epoch` and B8 `_num_summary` are REMOTE_DONE at B `b3e12945d6101b3808aedbc9ef21f5b23f36ae6e` (#12 `6550414243`), targeted normal `python -m unittest tests/test_p15_rf063_20261101_07h_owners.py -v` 2/2 exit0, exact scoped integration `93a1a4b2e2b27b3ad4e9b853fa4baef0c6fc52b1` and C05 G1/G2/G3 scoped acceptance. DO NOT redo B7/B8 or same-SHA test. B-06 B1/B2/B5/B6/B7/B8 six prior REMOTE_DONE; B-06 B4 `_validate_dataset` also REMOTE_DONE at B `f8fbe7648174da08cc71d25fb71c28ab5c30a970`, normal 06h 7/7 exit0. **B-06 B3 `_seed_demo_dataset` is C1 carryover (NOT NEW)**. B-07 B1–B6 are six actual unimplemented BODY MOVEs; SOURCE `scripts/diagnostics/run_m26_closeout_check.py` exact B/integration blob `d0d9a1f86b4f69cb4b81fb9b707a76a73bc858f9`, all six Owner targets 404 on both refs at issuance. Do not reimplement B-06 completed items. Older B-04 G3 and B1 G2 remain C04/C05 gaps, not new work.

**OWNER/SAFETY:** RF-063 CODEX_B exclusively. Modify ONLY two named SOURCE scripts, 7 distinct NEW Owner projection files (6 B1–B6 + 1 carryover C1), existing `tests/test_p15_rf063_20261101_06h_owners.py` for missing C1 case, and NEW `tests/test_p15_rf063_20261101_07h_owners.py` for B1–B6 on B branch `work/p15-b-operator-structure-20261022`. No A branch, D00/RF/STATUS/queue/C04/C05, frozen CI, real data/operations/Broker/Guard/Step5C/UEF/RunLab/network/orders/promotion. C1 seed and B1/B6 writes ONLY in TemporaryDirectory; B2–B5 use patched fake capture/runner (NEVER real CLI main or gate). No force push.

**MOVE/TEST:** Capture original golden before editing at exact SOURCE blobs. Owner preserves complete executable BODY, original signature + keyword-only facade; SOURCE retains same signature but sole Owner delegation with call-time facade monkeypatch, no duplicate calculation. Preserve output/error/arg order, alias/copy and nested functions. Source scripts already import sys. For carryover C1 add only the one missing test to existing 06h file and run `python -m unittest tests/test_p15_rf063_20261101_06h_owners.py -v` normal exit0 (expect 8/8 after C1 addition; C2's 7/7 normal prior run is not repeated for same SHA). For remaining B1–B6 append 6 distinct unittest tests to the existing 07h file, preserving B7/B8 and their existing passing tests without rewriting them and run `python -m unittest tests/test_p15_rf063_20261101_07h_owners.py -v` normal exit0 (8/8 total: 6 new + existing B7/B8). Do not count existing 2 PASS as NEW. All fake/temp, no real CLI. Optional related scoped test; full/-O/full peer/hosted CI NOT compulsory. Commit only code/test to B branch, normal push or approved exact-tree expected-head lease without force, re-fetch B HEAD and SOURCE/Owner/test blob. Report each item and measured START/END to #12. Push failure=PUSH_BLOCKED only, continue safe work. SHA divergence→item BLOCKED with exact ref; do not overwrite.

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
## B1 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_closeout_check.py::_write_jsonl` @ L22 | CURRENT_BLOB `d0d9a1f86b4f69cb4b81fb9b707a76a73bc858f9`
**NEW TARGET (404 B/integration VERIFIED):** `scripts/diagnostics/m26_closeout_jsonl_projection.py::_write_jsonl`. MOVE **COMPLETE executable body below** into Owner with original signature + keyword-only facade; keep original SOURCE signature and replace with thin wrapper only.
```python
def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
```
**THIN WRAPPER / MONKEYPATCH:** SOURCE local import `scripts.diagnostics.m26_closeout_jsonl_projection as _b07_1_owner`, sole `return _b07_1_owner._write_jsonl(<original args forwarded>, facade=sys.modules[__name__])`; unique alias avoids collisions. Owner must not import SOURCE. Resolve listed call-time globals through facade: json,Path methods. Preserve output/exception, nested function, JSON order, CLI args and side-effect boundaries. 
**NORMAL TARGETED `test_b1__write_jsonl`:** TemporaryDirectory/execution/x.jsonl rows=[{'symbol':'005930'}] → one UTF-8 JSONL line, parent exists; empty rows→empty file. Compare original-golden vs wrapper vs direct Owner, positive/negative/exception, patched facade, AST SOURCE old BODY removed. **BLOCKED→NEXT:** record exact error/SHA, continue B2.

## B2 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_closeout_check.py::_run_json` @ L29 | CURRENT_BLOB `d0d9a1f86b4f69cb4b81fb9b707a76a73bc858f9`
**NEW TARGET (404 B/integration VERIFIED):** `scripts/diagnostics/m26_closeout_capture_projection.py::_run_json`. MOVE **COMPLETE executable body below** into Owner with original signature + keyword-only facade; keep original SOURCE signature and replace with thin wrapper only.
```python
def _run_json(main_fn, argv: List[str]) -> Tuple[int, Dict[str, Any]]:  # type: ignore[no-untyped-def]
    return capture_cli_json(main_fn, argv)
```
**THIN WRAPPER / MONKEYPATCH:** SOURCE local import `scripts.diagnostics.m26_closeout_capture_projection as _b07_2_owner`, sole `return _b07_2_owner._run_json(<original args forwarded>, facade=sys.modules[__name__])`; unique alias avoids collisions. Owner must not import SOURCE. Resolve listed call-time globals through facade: capture_cli_json. Preserve output/exception, nested function, JSON order, CLI args and side-effect boundaries. 
**NORMAL TARGETED `test_b2__run_json`:** fake capture_cli_json returns (0,{'ok':True}) and receives exact dummy main_fn, ['--json']; no real CLI. Compare original-golden vs wrapper vs direct Owner, positive/negative/exception, patched facade, AST SOURCE old BODY removed. **BLOCKED→NEXT:** record exact error/SHA, continue B3.

## B3 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_closeout_check.py::_run_scorecard_json` @ L43 | CURRENT_BLOB `d0d9a1f86b4f69cb4b81fb9b707a76a73bc858f9`
**NEW TARGET (404 B/integration VERIFIED):** `scripts/diagnostics/m26_closeout_scorecard_projection.py::_run_scorecard_json`. MOVE **COMPLETE executable body below** into Owner with original signature + keyword-only facade; keep original SOURCE signature and replace with thin wrapper only.
```python
def _run_scorecard_json(*, dataset_root: Path, day: str) -> Tuple[int, Dict[str, Any]]:
    argv = ["--dataset-root", str(dataset_root), "--json"]
    if day:
        argv.extend(["--day", day])
    return _run_json(scorecard_main, argv)
```
**THIN WRAPPER / MONKEYPATCH:** SOURCE local import `scripts.diagnostics.m26_closeout_scorecard_projection as _b07_3_owner`, sole `return _b07_3_owner._run_scorecard_json(<original args forwarded>, facade=sys.modules[__name__])`; unique alias avoids collisions. Owner must not import SOURCE. Resolve listed call-time globals through facade: _run_json,scorecard_main. Preserve output/exception, nested function, JSON order, CLI args and side-effect boundaries. 
**NORMAL TARGETED `test_b3__run_scorecard_json`:** fake _run_json receives --dataset-root and --day 2026-02-17; day='' omits --day; never run scorecard. Compare original-golden vs wrapper vs direct Owner, positive/negative/exception, patched facade, AST SOURCE old BODY removed. **BLOCKED→NEXT:** record exact error/SHA, continue B4.

## B4 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_closeout_check.py::_run_ab_eval_json` @ L50 | CURRENT_BLOB `d0d9a1f86b4f69cb4b81fb9b707a76a73bc858f9`
**NEW TARGET (404 B/integration VERIFIED):** `scripts/diagnostics/m26_closeout_ab_projection.py::_run_ab_eval_json`. MOVE **COMPLETE executable body below** into Owner with original signature + keyword-only facade; keep original SOURCE signature and replace with thin wrapper only.
```python
def _run_ab_eval_json(*, base_root: Path, candidate_root: Path, day: str) -> Tuple[int, Dict[str, Any]]:
    argv = [
        "--a-dataset-root",
        str(base_root),
        "--b-dataset-root",
        str(candidate_root),
        "--a-label",
        "baseline",
        "--b-label",
        "candidate",
        "--json",
    ]
    if day:
        argv.extend(["--day", day])
    return _run_json(ab_eval_main, argv)
```
**THIN WRAPPER / MONKEYPATCH:** SOURCE local import `scripts.diagnostics.m26_closeout_ab_projection as _b07_4_owner`, sole `return _b07_4_owner._run_ab_eval_json(<original args forwarded>, facade=sys.modules[__name__])`; unique alias avoids collisions. Owner must not import SOURCE. Resolve listed call-time globals through facade: _run_json,ab_eval_main. Preserve output/exception, nested function, JSON order, CLI args and side-effect boundaries. 
**NORMAL TARGETED `test_b4__run_ab_eval_json`:** fake _run_json captures --a-dataset-root/--b-dataset-root, baseline/candidate labels, --day; never run AB. Compare original-golden vs wrapper vs direct Owner, positive/negative/exception, patched facade, AST SOURCE old BODY removed. **BLOCKED→NEXT:** record exact error/SHA, continue B5.

## B5 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_closeout_check.py::_run_gate_json` @ L67 | CURRENT_BLOB `d0d9a1f86b4f69cb4b81fb9b707a76a73bc858f9`
**NEW TARGET (404 B/integration VERIFIED):** `scripts/diagnostics/m26_closeout_gate_projection.py::_run_gate_json`. MOVE **COMPLETE executable body below** into Owner with original signature + keyword-only facade; keep original SOURCE signature and replace with thin wrapper only.
```python
def _run_gate_json(
    *,
    base_root: Path,
    candidate_root: Path,
    day: str,
    min_delta_total_pnl_proxy: float,
) -> Tuple[int, Dict[str, Any]]:
    argv = [
        "--a-dataset-root",
        str(base_root),
        "--b-dataset-root",
        str(candidate_root),
        "--a-label",
        "baseline",
        "--b-label",
        "candidate",
        "--min-delta-total-pnl-proxy",
        str(float(min_delta_total_pnl_proxy)),
        "--min-sortino-proxy",
        "0",
        "--max-drawdown-ratio",
        "1",
        "--json",
    ]
    if day:
        argv.extend(["--day", day])
    return _run_json(gate_main, argv)
```
**THIN WRAPPER / MONKEYPATCH:** SOURCE local import `scripts.diagnostics.m26_closeout_gate_projection as _b07_5_owner`, sole `return _b07_5_owner._run_gate_json(<original args forwarded>, facade=sys.modules[__name__])`; unique alias avoids collisions. Owner must not import SOURCE. Resolve listed call-time globals through facade: _run_json,gate_main. Preserve output/exception, nested function, JSON order, CLI args and side-effect boundaries. 
**NORMAL TARGETED `test_b5__run_gate_json`:** fake _run_json captures --min-delta-total-pnl-proxy '1.5', --min-sortino-proxy '0', --max-drawdown-ratio '1'; no actual gate/promotion. Compare original-golden vs wrapper vs direct Owner, positive/negative/exception, patched facade, AST SOURCE old BODY removed. **BLOCKED→NEXT:** record exact error/SHA, continue B6.

## B6 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_closeout_check.py::_prepare_candidate_dataset` @ L96 | CURRENT_BLOB `d0d9a1f86b4f69cb4b81fb9b707a76a73bc858f9`
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

## FUTURE RESERVE — VERIFIED 6/6 (DESIGN ONLY; **NOT EXECUTABLE**; C03 MUST ISSUE A NEW ORDER FIRST)
RF-063 CODEX_B exclusively; SOURCE `scripts/diagnostics/check_audit_trail_completeness.py` actor/integration exact blob `1df9947a268f31d73639542db4a09eaac6e172b6`; all six TARGET paths independently returned 404 on BOTH actor branch and integration on 2026-11-01. These six are NOT part of the current executable order. No Actor self-selection or same-SHA retest. Each has no real-order, Broker/Guard/Step5C/UEF/RunLab effects; fake/in-memory fixtures only. Preserve original facade monkeypatch and exception behavior when C03 later issues them.

### RESERVE 1 | `scripts/diagnostics/check_audit_trail_completeness.py::_to_epoch` @ L15 | SOURCE_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6` → `scripts/diagnostics/audit_trail_epoch_projection.py::_to_epoch` (404 both)
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
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: datetime/timezone via facade. NORMAL targeted golden/Owner/wrapper test: '1970-01-01T00:00:01Z'→1; None→None; naive UTC. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 2 | `scripts/diagnostics/check_audit_trail_completeness.py::_utc_day` @ L38 | SOURCE_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6` → `scripts/diagnostics/audit_trail_utc_day_projection.py::_utc_day` (404 both)
```python
def _utc_day(ts: Any) -> str:
    epoch = _to_epoch(ts)
    if epoch is None:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return datetime.fromtimestamp(epoch, tz=timezone.utc).strftime("%Y-%m-%d")
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: _to_epoch/datetime/timezone via facade. NORMAL targeted golden/Owner/wrapper test: ts=1→'1970-01-01'; None with fake clock→fixed day. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 3 | `scripts/diagnostics/check_audit_trail_completeness.py::_extract_ts` @ L45 | SOURCE_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6` → `scripts/diagnostics/audit_trail_extract_ts_projection.py::_extract_ts` (404 both)
```python
def _extract_ts(row: Dict[str, Any]) -> Any:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    return row.get("ts") or payload.get("ts")
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: none. NORMAL targeted golden/Owner/wrapper test: {'ts':0,'payload':{'ts':42}}→42. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 4 | `scripts/diagnostics/check_audit_trail_completeness.py::_extract_decision_action` @ L68 | SOURCE_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6` → `scripts/diagnostics/audit_trail_decision_action_projection.py::_extract_decision_action` (404 both)
```python
def _extract_decision_action(row: Dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    packet = payload.get("decision_packet") if isinstance(payload.get("decision_packet"), dict) else {}
    intent = packet.get("intent") if isinstance(packet.get("intent"), dict) else {}
    action = intent.get("action") or payload.get("action") or payload.get("intent")
    return str(action or "").strip().upper()
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: none. NORMAL targeted golden/Owner/wrapper test: nested decision_packet.intent.action='buy'→'BUY'; absent→''. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 5 | `scripts/diagnostics/check_audit_trail_completeness.py::_extract_allowed` @ L76 | SOURCE_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6` → `scripts/diagnostics/audit_trail_allowed_projection.py::_extract_allowed` (404 both)
```python
def _extract_allowed(row: Dict[str, Any]) -> Optional[bool]:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    v = payload.get("allowed")
    if isinstance(v, bool):
        return v
    return None
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: none. NORMAL targeted golden/Owner/wrapper test: payload.allowed=True→True; allowed=1→None. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 6 | `scripts/diagnostics/check_audit_trail_completeness.py::_latest_day` @ L84 | SOURCE_BLOB `1df9947a268f31d73639542db4a09eaac6e172b6` → `scripts/diagnostics/audit_trail_latest_day_projection.py::_latest_day` (404 both)
```python
def _latest_day(rows: List[Dict[str, Any]]) -> str:
    days = sorted({str(r.get("_day") or "") for r in rows if str(r.get("_day") or "").strip()})
    if days:
        return str(days[-1])
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: datetime/timezone via facade. NORMAL targeted golden/Owner/wrapper test: [{'_day':'2026-10-30'},{'_day':'2026-11-01'}]→'2026-11-01'; [] with fake clock→fixed day. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

**COUNTS:** B-06 REMOTE_DONE=7/8; B-07 NEW_READY=6 plus C1 carryover (B7/B8 REMOTE_DONE 2/8); RESERVE_VERIFIED=6/6. C03 DOC_ONLY; code G1/G2/G3=0, RF_DONE_DELTA=0.
