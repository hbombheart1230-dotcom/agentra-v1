# C01 — Codex B | B-20261101-06 | FAST-3 NEW EIGHT VERIFIED BODY MOVEs

**SINGLE ENTRY.** At start pin integration HEAD, C01 blob, B owner HEAD, ORDER_ID. Read only this C01 and named code/test paths, never D00/RF/queue/C03/CURRENT/HANDOFF. Execute all B1–B8; if one item BLOCKED continue remaining safe items. Previously started pinned order can finish without retroactive cancellation.

**REMOTE_DONE:** previous C01 blob 219751a5ccbc9b1829e64bff80369a584dd4b99f B-20261101-05 eight BODY MOVEs are remotely complete at B SHA a7866cbcaca6571a6e7298b055dd99adcf05283c (#12 6548598563), normal targeted 8/8 exit0, integrated exact at faded947e62e7fc4dd153fbe94d3a72d92b27c02 (#36 6548799065). Do not redo previous same-SHA tests, MOVE or KEEP. These eight new functions below retain original executable bodies on B and integration.

**OWNERSHIP/SAFETY:** RF-063 CODEX_B only. Change only the two named SOURCE scripts, eight NEW Owner projection files and NEW tests/test_p15_rf063_20261101_06h_owners.py on B branch work/p15-b-operator-structure-20261022. No other Actor, D00/RF/queue/STATUS/C04/C05, frozen CI, real Broker/Guard/Step5C/UEF/RunLab, real data/network/orders or live promotion. Test all writes/reads ONLY in TemporaryDirectory, and all run_* helpers with patched fake _run_json and fake main; never execute real scorecard, replay, closeout, promotion or CLI main. No force push.

**MOVE MECHANISM:** Before edits capture original golden from pinned SOURCE blob. Move COMPLETE executable BODY to unique new Owner with original parameters plus keyword-only facade; leave exact original SOURCE signature/annotations with ONLY thin Owner delegation. Source scripts already import sys. Owner must not import SOURCE; every listed helper/global resolves through facade.<name> at call time to preserve monkeypatch. Preserve exception/output/order/alias/copy/defaults. For seed move ALL CSV/JSONL/manifest content, not a stub. For validation preserve failure ordering and counts; parsers preserve options/defaults.

**TARGETED NORMAL G2:** Write eight distinct unittest cases test_b1_* through test_b8_* in NEW test file, compare golden original vs SOURCE wrapper vs direct Owner on positive/negative/error, call-time facade monkeypatch and AST old calculation BODY removed. Run python -m unittest tests/test_p15_rf063_20261101_06h_owners.py -v (normal exit0), fake/temp only; no compulsory full-suite/-O/peer/hosted CI. Commit only code/test on B branch, normal push and re-fetch remote B HEAD and SOURCE/TARGET/test blobs. If terminal HTTPS blocked, approved exact-tree expected-head lease may be used without force; report PUSH_BLOCKED if not delivered. Record per-item status, normal exit, actual measured START/END in #12. On divergence or safety issue BLOCKED exact SHA and continue other items; no self-selection.

## B1 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_dataset_manifest_check.py::_utc_now_iso @ L42 | CURRENT_BLOB a0afae27c395837c8e2059bb6cf22c34baed03fe
**NEW TARGET (404 B/integration):** scripts/diagnostics/m26_manifest_now_projection.py::_utc_now_iso. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
```
**SOURCE thin wrapper:** preserve exact signature; import scripts.diagnostics.m26_manifest_now_projection as _b1_owner; sole delegation: return _b1_owner._utc_now_iso(facade=sys.modules[__name__]). **CALL-TIME SEAM:** datetime,timezone; Owner uses facade.<name> for each applicable global/helper.
**NORMAL TARGETED test_b1_utc_now_iso:** fixed fake UTC clock 2026-02-17T00:00:00+00:00 -> exact ISO string. Original-golden == wrapper == direct Owner; AST original BODY removed. **BLOCKED→NEXT:** log exact failure and continue B2.

## B2 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_dataset_manifest_check.py::_write_text @ L46 | CURRENT_BLOB a0afae27c395837c8e2059bb6cf22c34baed03fe
**NEW TARGET (404 B/integration):** scripts/diagnostics/m26_manifest_write_projection.py::_write_text. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
```
**SOURCE thin wrapper:** preserve exact signature; import scripts.diagnostics.m26_manifest_write_projection as _b2_owner; sole delegation: return _b2_owner._write_text(path, content, facade=sys.modules[__name__]). **CALL-TIME SEAM:** Path methods; Owner uses facade.<name> for each applicable global/helper.
**NORMAL TARGETED test_b2_write_text:** TemporaryDirectory child path with content 'x' -> UTF-8 'x' and parent created. Original-golden == wrapper == direct Owner; AST original BODY removed. **BLOCKED→NEXT:** log exact failure and continue B3.

## B3 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_dataset_manifest_check.py::_seed_demo_dataset @ L51 | CURRENT_BLOB a0afae27c395837c8e2059bb6cf22c34baed03fe
**NEW TARGET (404 B/integration):** scripts/diagnostics/m26_manifest_seed_projection.py::_seed_demo_dataset. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
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
**SOURCE thin wrapper:** preserve exact signature; import scripts.diagnostics.m26_manifest_seed_projection as _b3_owner; sole delegation: return _b3_owner._seed_demo_dataset(root, facade=sys.modules[__name__]). **CALL-TIME SEAM:** _write_text,_utc_now_iso,json,SCHEMA_VERSION,REQUIRED_COMPONENT_FILES; Owner uses facade.<name> for each applicable global/helper.
**NORMAL TARGETED test_b3_seed_demo_dataset:** TemporaryDirectory root -> manifest.json with schema_version m26.dataset_manifest.v1 and only temp paths; fixed fake timestamp. Original-golden == wrapper == direct Owner; AST original BODY removed. **BLOCKED→NEXT:** log exact failure and continue B4.

## B4 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_dataset_manifest_check.py::_validate_dataset @ L177 | CURRENT_BLOB a0afae27c395837c8e2059bb6cf22c34baed03fe
**NEW TARGET (404 B/integration):** scripts/diagnostics/m26_manifest_validate_projection.py::_validate_dataset. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _validate_dataset(root: Path) -> Dict[str, Any]:
    manifest_path = root / "manifest.json"
    failures: List[str] = []
    missing_files: List[str] = []
    schema_version = ""
    dataset_id = ""

    manifest: Dict[str, Any] = {}
    if not manifest_path.exists():
        failures.append("missing:manifest.json")
    else:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except Exception as e:
            failures.append(f"invalid:manifest.json ({e})")

    if manifest:
        schema_version = str(manifest.get("schema_version") or "")
        dataset_id = str(manifest.get("dataset_id") or "")
        if schema_version != SCHEMA_VERSION:
            failures.append(f"invalid:schema_version (expected={SCHEMA_VERSION}, got={schema_version or 'empty'})")
        if not dataset_id:
            failures.append("invalid:dataset_id (empty)")

        components = manifest.get("components")
        if not isinstance(components, dict):
            failures.append("invalid:components (must be object)")
            components = {}
        for comp, expected in REQUIRED_COMPONENT_FILES.items():
            listed = components.get(comp)
            if not isinstance(listed, list):
                failures.append(f"missing_component:{comp}")
                listed = []
            listed_set = {str(x).replace("\\", "/") for x in listed}
            for rel in expected:
                if rel not in listed_set:
                    failures.append(f"missing_manifest_ref:{rel}")
                if not (root / rel).exists():
                    missing_files.append(rel)
    else:
        # Even when manifest is missing/invalid, report expected missing files
        for expected in REQUIRED_COMPONENT_FILES.values():
            for rel in expected:
                if not (root / rel).exists():
                    missing_files.append(rel)

    missing_files = sorted(set(missing_files))
    out = {
        "ok": len(failures) == 0 and len(missing_files) == 0,
        "dataset_root": str(root),
        "manifest_path": str(manifest_path),
        "schema_version": schema_version,
        "dataset_id": dataset_id,
        "component_total": len(REQUIRED_COMPONENT_FILES),
        "required_file_total": int(sum(len(v) for v in REQUIRED_COMPONENT_FILES.values())),
        "present_file_total": 0,
        "missing_file_total": len(missing_files),
        "missing_files": missing_files,
        "failure_total": len(failures),
        "failures": failures,
    }
    # compute present count from required total minus unique missing
    out["present_file_total"] = int(out["required_file_total"]) - int(out["missing_file_total"])
    return out
```
**SOURCE thin wrapper:** preserve exact signature; import scripts.diagnostics.m26_manifest_validate_projection as _b4_owner; sole delegation: return _b4_owner._validate_dataset(root, facade=sys.modules[__name__]). **CALL-TIME SEAM:** json,SCHEMA_VERSION,REQUIRED_COMPONENT_FILES; Owner uses facade.<name> for each applicable global/helper.
**NORMAL TARGETED test_b4_validate_dataset:** empty TemporaryDirectory -> missing:manifest.json; temp seeded dataset -> ok True and missing_file_total 0. Original-golden == wrapper == direct Owner; AST original BODY removed. **BLOCKED→NEXT:** log exact failure and continue B5.

## B5 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_dataset_manifest_check.py::_build_parser @ L243 | CURRENT_BLOB a0afae27c395837c8e2059bb6cf22c34baed03fe
**NEW TARGET (404 B/integration):** scripts/diagnostics/m26_manifest_parser_projection.py::_build_parser. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M26 fixed dataset manifest scaffold and validation gate.")
    p.add_argument("--dataset-root", default="data/eval/m26_fixed_dataset_v1")
    p.add_argument("--seed-demo", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
```
**SOURCE thin wrapper:** preserve exact signature; import scripts.diagnostics.m26_manifest_parser_projection as _b5_owner; sole delegation: return _b5_owner._build_parser(facade=sys.modules[__name__]). **CALL-TIME SEAM:** argparse; Owner uses facade.<name> for each applicable global/helper.
**NORMAL TARGETED test_b5_build_parser:** parse_args(['--seed-demo','--json']) -> seed_demo True,json True, default dataset_root. Original-golden == wrapper == direct Owner; AST original BODY removed. **BLOCKED→NEXT:** log exact failure and continue B6.

## B6 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_closeout_check.py::_build_parser @ L129 | CURRENT_BLOB 4a87f8bdf0c1af655192521ead900431ebf66bba
**NEW TARGET (404 B/integration):** scripts/diagnostics/m26_closeout_parser_projection.py::_build_parser. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M26 closeout check (dataset/replay/scorecard/A-B/promotion gate).")
    p.add_argument("--base-dataset-root", default="data/eval/m26_closeout/base")
    p.add_argument("--candidate-dataset-root", default="data/eval/m26_closeout/candidate")
    p.add_argument("--day", default="2026-02-17")
    p.add_argument("--min-delta-total-pnl-proxy", type=float, default=5.0)
    p.add_argument("--inject-gate-fail", action="store_true")
    p.add_argument("--no-clear", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
```
**SOURCE thin wrapper:** preserve exact signature; import scripts.diagnostics.m26_closeout_parser_projection as _b6_owner; sole delegation: return _b6_owner._build_parser(facade=sys.modules[__name__]). **CALL-TIME SEAM:** argparse; Owner uses facade.<name> for each applicable global/helper.
**NORMAL TARGETED test_b6_build_parser:** parse_args(['--day','2026-11-01','--json']) -> day 2026-11-01,json True,no_clear False. Original-golden == wrapper == direct Owner; AST original BODY removed. **BLOCKED→NEXT:** log exact failure and continue B7.

## B7 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_closeout_check.py::_run_manifest_json @ L33 | CURRENT_BLOB 4a87f8bdf0c1af655192521ead900431ebf66bba
**NEW TARGET (404 B/integration):** scripts/diagnostics/m26_closeout_manifest_projection.py::_run_manifest_json. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _run_manifest_json(*, dataset_root: Path, seed_demo: bool) -> Tuple[int, Dict[str, Any]]:
    argv = ["--dataset-root", str(dataset_root), "--json"]
    if seed_demo:
        argv.insert(2, "--seed-demo")
    return _run_json(manifest_main, argv)
```
**SOURCE thin wrapper:** preserve exact signature; import scripts.diagnostics.m26_closeout_manifest_projection as _b7_owner; sole delegation: return _b7_owner._run_manifest_json(dataset_root=dataset_root, seed_demo=seed_demo, facade=sys.modules[__name__]). **CALL-TIME SEAM:** _run_json,manifest_main; Owner uses facade.<name> for each applicable global/helper.
**NORMAL TARGETED test_b7_run_manifest_json:** fake _run_json captures ['--dataset-root','/tmp/fake','--seed-demo','--json'] and returns (0,{'ok':True}); no actual main. Original-golden == wrapper == direct Owner; AST original BODY removed. **BLOCKED→NEXT:** log exact failure and continue B8.

## B8 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_closeout_check.py::_run_replay_json @ L40 | CURRENT_BLOB 4a87f8bdf0c1af655192521ead900431ebf66bba
**NEW TARGET (404 B/integration):** scripts/diagnostics/m26_closeout_replay_projection.py::_run_replay_json. **MOVE COMPLETE ORIGINAL EXECUTABLE BODY** (Owner same signature plus keyword-only facade):
```python
def _run_replay_json(*, dataset_root: Path, day: str) -> Tuple[int, Dict[str, Any]]:
    argv = ["--dataset-root", str(dataset_root), "--json"]
    if day:
        argv.extend(["--day", day])
    return _run_json(replay_main, argv)
```
**SOURCE thin wrapper:** preserve exact signature; import scripts.diagnostics.m26_closeout_replay_projection as _b8_owner; sole delegation: return _b8_owner._run_replay_json(dataset_root=dataset_root, day=day, facade=sys.modules[__name__]). **CALL-TIME SEAM:** _run_json,replay_main; Owner uses facade.<name> for each applicable global/helper.
**NORMAL TARGETED test_b8_run_replay_json:** fake _run_json captures ['--dataset-root','/tmp/fake','--json','--day','2026-11-01']; empty day omits --day. Original-golden == wrapper == direct Owner; AST original BODY removed. **BLOCKED→NEXT:** log exact failure and continue B1–B8 remaining/push.

## FUTURE RESERVE — 6/6 VERIFIED DESIGN ONLY, NOT EXECUTABLE
Each distinct SOURCE BODY/blob checked on B and integration; six TARGET paths 404 on both. RF-063 only. Future C03 must recheck source/target, caller/patch seam and temp isolation before issuing new order. B must NOT implement reserves now.

### R1 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_closeout_check.py::_write_jsonl @ L22 | BLOB 4a87f8bdf0c1af655192521ead900431ebf66bba
**TARGET ABSENT B/integration:** scripts/diagnostics/m26_closeout_jsonl_projection.py::_write_jsonl. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
```
**Future normal fake/temp fixture:** TemporaryDirectory JSONL one {'x':1} row -> UTF-8 line. **Seam:** json,Path, preserve thin SOURCE wrapper and use-time facade; no real data, CLI main, promotion, orders or operational effects.

### R2 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_closeout_check.py::_run_json @ L29 | BLOB 4a87f8bdf0c1af655192521ead900431ebf66bba
**TARGET ABSENT B/integration:** scripts/diagnostics/m26_closeout_run_json_projection.py::_run_json. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def _run_json(main_fn, argv: List[str]) -> Tuple[int, Dict[str, Any]]:  # type: ignore[no-untyped-def]
    return capture_cli_json(main_fn, argv)
```
**Future normal fake/temp fixture:** fake capture_cli_json returns (0,{'ok':True}), args unchanged. **Seam:** capture_cli_json, preserve thin SOURCE wrapper and use-time facade; no real data, CLI main, promotion, orders or operational effects.

### R3 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_closeout_check.py::_run_scorecard_json @ L47 | BLOB 4a87f8bdf0c1af655192521ead900431ebf66bba
**TARGET ABSENT B/integration:** scripts/diagnostics/m26_closeout_scorecard_projection.py::_run_scorecard_json. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def _run_scorecard_json(*, dataset_root: Path, day: str) -> Tuple[int, Dict[str, Any]]:
    argv = ["--dataset-root", str(dataset_root), "--json"]
    if day:
        argv.extend(["--day", day])
    return _run_json(scorecard_main, argv)
```
**Future normal fake/temp fixture:** fake _run_json captures scorecard_main and day; no real scorecard. **Seam:** _run_json,scorecard_main, preserve thin SOURCE wrapper and use-time facade; no real data, CLI main, promotion, orders or operational effects.

### R4 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_closeout_check.py::_run_ab_eval_json @ L54 | BLOB 4a87f8bdf0c1af655192521ead900431ebf66bba
**TARGET ABSENT B/integration:** scripts/diagnostics/m26_closeout_ab_projection.py::_run_ab_eval_json. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future normal fake/temp fixture:** fake _run_json captures baseline/candidate args; no real AB. **Seam:** _run_json,ab_eval_main, preserve thin SOURCE wrapper and use-time facade; no real data, CLI main, promotion, orders or operational effects.

### R5 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_closeout_check.py::_run_gate_json @ L71 | BLOB 4a87f8bdf0c1af655192521ead900431ebf66bba
**TARGET ABSENT B/integration:** scripts/diagnostics/m26_closeout_gate_projection.py::_run_gate_json. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future normal fake/temp fixture:** fake _run_json captures min delta and day; no real gate. **Seam:** _run_json,gate_main, preserve thin SOURCE wrapper and use-time facade; no real data, CLI main, promotion, orders or operational effects.

### R6 | RF-063 CODEX_B | SOURCE scripts/diagnostics/run_m26_closeout_check.py::_prepare_candidate_dataset @ L100 | BLOB 4a87f8bdf0c1af655192521ead900431ebf66bba
**TARGET ABSENT B/integration:** scripts/diagnostics/m26_closeout_candidate_projection.py::_prepare_candidate_dataset. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future normal fake/temp fixture:** precreate market/execution in TemporaryDirectory, fake _write_jsonl, verify candidate 100→115 data, no real paths. **Seam:** _write_jsonl,Path, preserve thin SOURCE wrapper and use-time facade; no real data, CLI main, promotion, orders or operational effects.

**COUNTS:** B-05 REMOTE_DONE=8/8; B-06 NEW_READY=8; RESERVE_VERIFIED=6. C03 document-only publication, not code G1/G2/G3 or RF DONE.