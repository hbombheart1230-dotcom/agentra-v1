# C01 — Codex B | B-20261101-05 | FAST-3 NEW 8 VERIFIED SOURCE BODY MOVEs

**SINGLE ENTRY, NO SELF-SELECTION.** Start pin CANONICAL_HEAD (integration/p1.5), this C01 blob, B remote HEAD and ORDER_ID. Read ONLY this C01 and named code/test paths; do not read D00/RF/queue/C03/CURRENT/HANDOFF. Execute ALL B1–B8 safely in order, continue after a blocked item. An actor already running a previous pinned order may finish that order; do not retroactively cancel it.

**C03 REMOTE DONE DELTA:** #12 comment 6547974300 confirms B-20261101-04-DELIVERY B2–B8 were transferred from local 4ca5ee9674faf524c763f171c4391da84a80abba to B remote `f5e497ef0b635732000fe86a87b844372d263900`; seven Owner files and thin SOURCE wrappers re-fetched, previous normal unittest 7/7 exit0 retained. Old C01 blob `ca0c2503fd8957f08b02d29334ca8e1e2f33c695` is exhausted 7/7 REMOTE_DONE. B1 earlier _to_epoch was also moved. DO NOT repeat B1–B8 old work or prior same-SHA tests. This is a wholly NEW eight-item order.

**OWNERSHIP & ISOLATION:** RF-063, CODEX_B only; SOURCE paths in `scripts/diagnostics`, unique TARGETs below verified absent on B branch and integration. RF-063 source coverage explicitly includes both scripts. No edits outside the listed SOURCE files, eight new TARGETs, and NEW `tests/test_p15_rf063_20261101_05h_metrics_ab_owners.py`. Preserve all older tests, CLI signatures, public imports, call-time SOURCE monkeypatches, output order, exceptions and defaults. Never modify other Actor, D00/RF/STATUS/queue/C04/C05, CI/frozen oracle, Broker/Guard/Step5C/UEF/RunLab, live network, real data or real orders. No force push.

**MOVE MECHANISM:** Move complete ORIGINAL executable body below into a unique new Owner function (not a copy), replace SOURCE body with only the shown Owner delegation. Keep original SOURCE function signature and annotations; use local import inside wrapper or module-level unique alias, avoid cycles. For facade-dependent Owner, add keyword-only `facade`, resolve every SOURCE global/helper at call time through facade (not a snapshot), do not import SOURCE from Owner. `sys` is already imported in both SOURCE files. Preserve `_compare_metrics` promotion recommendation as *data-only*; NEVER apply/promote. B8 test must monkeypatch SOURCE `scorecard_main` to a pure fake before any call; never run real scorecard or main.

**G2/DELIVERY:** Before editing, capture exact original source bodies from pinned blobs below for golden parity. Write eight distinct `test_b1_* ... test_b8_*` unittest cases in NEW test file: compare original-golden vs SOURCE wrapper vs direct Owner on positive/negative/exception and patched SOURCE seam; AST verify no duplicate calculation remains in SOURCE. Run `python -m py_compile scripts/diagnostics/check_metrics_schema_v1.py scripts/diagnostics/run_m26_ab_evaluation.py scripts/diagnostics/*_projection.py` (scope only newly changed Owner files if wildcard matches others) and `python -m unittest tests/test_p15_rf063_20261101_05h_metrics_ab_owners.py -v` normal exit0; relevant existing tests only when affected. Commit ONLY code and NEW test on B branch, normal push (or authorized exact-tree GitHub route with expected remote HEAD lease, never force), re-fetch B HEAD and SOURCE/TARGET/test blob parity. If HTTPS credential push fails, mark PUSH_BLOCKED and continue all independent safe items; local-only is NOT REMOTE_DONE. Report #12 `ORDER_ID | CANONICAL_HEAD | ORDER_BLOB | B_REMOTE_BEFORE→AFTER | per-item MOVE/TEST/PUSH | NORMAL_EXIT | SOURCE/TARGET/TEST_BLOBS | FIRST_BLOCKER | NEXT | measured START/END`. -O/full peer/per-RF hosted CI are NOT mandatory. C04 G3 and C05 RF DONE are separate.

## B1 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_metrics_schema_v1.py::_is_dict` @ L21 | CURRENT_BLOB `586466c6162d818d1ae60644ec7dd0d988beef63`
**NEW TARGET (404 actor/integration):** `scripts/diagnostics/metrics_schema_dict_projection.py::_is_dict`. **MOVE COMPLETE EXECUTABLE BODY EXACTLY:**
```python
def _is_dict(v: Any) -> bool:
    return isinstance(v, dict)
```
**SOURCE thin wrapper:** keep signature, import `scripts.diagnostics.metrics_schema_dict_projection` as `_b1_owner`; replace old body with sole `return _b1_owner._is_dict(v)`. **CALLER/MONKEYPATCH:** pure isinstance; original negative/exception/identity behavior unchanged.
**NORMAL TARGETED `test_b1_is_dict`:** {}→True; []→False. Assert original-golden == wrapper == direct Owner and AST thin delegation. **BLOCKED→NEXT:** record exact error and continue B2.

## B2 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_metrics_schema_v1.py::_is_list` @ L25 | CURRENT_BLOB `586466c6162d818d1ae60644ec7dd0d988beef63`
**NEW TARGET (404 actor/integration):** `scripts/diagnostics/metrics_schema_list_projection.py::_is_list`. **MOVE COMPLETE EXECUTABLE BODY EXACTLY:**
```python
def _is_list(v: Any) -> bool:
    return isinstance(v, list)
```
**SOURCE thin wrapper:** keep signature, import `scripts.diagnostics.metrics_schema_list_projection` as `_b2_owner`; replace old body with sole `return _b2_owner._is_list(v)`. **CALLER/MONKEYPATCH:** pure isinstance; original negative/exception/identity behavior unchanged.
**NORMAL TARGETED `test_b2_is_list`:** []→True; {}→False. Assert original-golden == wrapper == direct Owner and AST thin delegation. **BLOCKED→NEXT:** record exact error and continue B3.

## B3 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/check_metrics_schema_v1.py::_build_parser` @ L34 | CURRENT_BLOB `586466c6162d818d1ae60644ec7dd0d988beef63`
**NEW TARGET (404 actor/integration):** `scripts/diagnostics/metrics_schema_parser_projection.py::_build_parser`. **MOVE COMPLETE EXECUTABLE BODY EXACTLY:**
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Validate frozen metrics schema v1.")
    p.add_argument("--event-log-path", default="data/logs/events.jsonl")
    p.add_argument("--report-dir", default="reports/metrics")
    p.add_argument("--day", default=None)
    p.add_argument("--json", action="store_true")
    return p
```
**SOURCE thin wrapper:** keep signature, import `scripts.diagnostics.metrics_schema_parser_projection` as `_b3_owner`; replace old body with sole `return _b3_owner._build_parser(facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade.argparse; parser construction only, never main; original negative/exception/identity behavior unchanged.
**NORMAL TARGETED `test_b3_build_parser`:** parse_args(['--day','2026-11-01','--json'])→day='2026-11-01',json=True. Assert original-golden == wrapper == direct Owner and AST thin delegation. **BLOCKED→NEXT:** record exact error and continue B4.

## B4 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_ab_evaluation.py::_as_float` @ L18 | CURRENT_BLOB `864f845cd2e6644c134372745590ecafeabc70ee`
**NEW TARGET (404 actor/integration):** `scripts/diagnostics/m26_ab_float_projection.py::_as_float`. **MOVE COMPLETE EXECUTABLE BODY EXACTLY:**
```python
def _as_float(v: Any, default: float = 0.0) -> float:
    try:
        return float(v)
    except Exception:
        return float(default)
```
**SOURCE thin wrapper:** keep signature, import `scripts.diagnostics.m26_ab_float_projection` as `_b4_owner`; replace old body with sole `return _b4_owner._as_float(v, default)`. **CALLER/MONKEYPATCH:** pure float fallback; original negative/exception/identity behavior unchanged.
**NORMAL TARGETED `test_b4_as_float`:** '2.5'→2.5; ('bad',3.0)→3.0. Assert original-golden == wrapper == direct Owner and AST thin delegation. **BLOCKED→NEXT:** record exact error and continue B5.

## B5 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_ab_evaluation.py::_json_path_get` @ L25 | CURRENT_BLOB `864f845cd2e6644c134372745590ecafeabc70ee`
**NEW TARGET (404 actor/integration):** `scripts/diagnostics/m26_ab_path_projection.py::_json_path_get`. **MOVE COMPLETE EXECUTABLE BODY EXACTLY:**
```python
def _json_path_get(obj: Dict[str, Any], path: str, default: float = 0.0) -> float:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict):
            return float(default)
        cur = cur.get(part)
    return _as_float(cur, default)
```
**SOURCE thin wrapper:** keep signature, import `scripts.diagnostics.m26_ab_path_projection` as `_b5_owner`; replace old body with sole `return _b5_owner._json_path_get(obj, path, default, facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade._as_float at call-time; original negative/exception/identity behavior unchanged.
**NORMAL TARGETED `test_b5_json_path_get`:** ({'a':{'b':2}},'a.b')→2.0; missing default=3→3.0. Assert original-golden == wrapper == direct Owner and AST thin delegation. **BLOCKED→NEXT:** record exact error and continue B6.

## B6 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_ab_evaluation.py::_build_parser` @ L50 | CURRENT_BLOB `864f845cd2e6644c134372745590ecafeabc70ee`
**NEW TARGET (404 actor/integration):** `scripts/diagnostics/m26_ab_parser_projection.py::_build_parser`. **MOVE COMPLETE EXECUTABLE BODY EXACTLY:**
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M26 A/B evaluation scaffold over scorecard outputs.")
    p.add_argument("--a-dataset-root", default="data/eval/m26_fixed_dataset_v1")
    p.add_argument("--b-dataset-root", default="data/eval/m26_fixed_dataset_v1")
    p.add_argument("--a-label", default="A")
    p.add_argument("--b-label", default="B")
    p.add_argument("--day", default="")
    p.add_argument("--json", action="store_true")
    return p
```
**SOURCE thin wrapper:** keep signature, import `scripts.diagnostics.m26_ab_parser_projection` as `_b6_owner`; replace old body with sole `return _b6_owner._build_parser(facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade.argparse, no main; original negative/exception/identity behavior unchanged.
**NORMAL TARGETED `test_b6_build_parser`:** parse_args(['--a-label','X','--json'])→a_label='X',json=True. Assert original-golden == wrapper == direct Owner and AST thin delegation. **BLOCKED→NEXT:** record exact error and continue B7.

## B7 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_ab_evaluation.py::_compare_metrics` @ L61 | CURRENT_BLOB `864f845cd2e6644c134372745590ecafeabc70ee`
**NEW TARGET (404 actor/integration):** `scripts/diagnostics/m26_ab_compare_projection.py::_compare_metrics`. **MOVE COMPLETE EXECUTABLE BODY EXACTLY:**
```python
def _compare_metrics(
    *,
    a_label: str,
    b_label: str,
    a_score: Dict[str, Any],
    b_score: Dict[str, Any],
) -> Dict[str, Any]:
    metric_rules: List[Tuple[str, str]] = [
        ("total_pnl_proxy", "higher"),
        ("risk_adjusted.sortino_proxy", "higher"),
        ("risk_adjusted.sharpe_proxy", "higher"),
        ("drawdown.max_drawdown_ratio", "lower"),
        ("win_rate", "higher"),
    ]
    eps = 1e-12
    points: Dict[str, int] = {a_label: 0, b_label: 0}
    results: List[Dict[str, Any]] = []

    for metric, direction in metric_rules:
        a_val = _json_path_get(a_score, metric, 0.0)
        b_val = _json_path_get(b_score, metric, 0.0)
        winner = "tie"
        if direction == "higher":
            if b_val > a_val + eps:
                winner = b_label
                points[b_label] += 1
            elif a_val > b_val + eps:
                winner = a_label
                points[a_label] += 1
        else:
            if b_val + eps < a_val:
                winner = b_label
                points[b_label] += 1
            elif a_val + eps < b_val:
                winner = a_label
                points[a_label] += 1

        results.append(
            {
                "metric": metric,
                "direction": direction,
                "a_value": float(a_val),
                "b_value": float(b_val),
                "delta_b_minus_a": float(b_val - a_val),
                "winner": winner,
            }
        )

    if points[b_label] > points[a_label]:
        winner = b_label
    elif points[a_label] > points[b_label]:
        winner = a_label
    else:
        winner = "tie"

    # Conservative promotion gate:
    # winner must keep drawdown no worse and improve or match PnL + Sortino.
    a_pnl = _json_path_get(a_score, "total_pnl_proxy", 0.0)
    b_pnl = _json_path_get(b_score, "total_pnl_proxy", 0.0)
    a_sortino = _json_path_get(a_score, "risk_adjusted.sortino_proxy", 0.0)
    b_sortino = _json_path_get(b_score, "risk_adjusted.sortino_proxy", 0.0)
    a_dd = _json_path_get(a_score, "drawdown.max_drawdown_ratio", 0.0)
    b_dd = _json_path_get(b_score, "drawdown.max_drawdown_ratio", 0.0)

    recommended = "hold"
    reasons: List[str] = []
    if winner == b_label:
        if (b_pnl >= a_pnl) and (b_sortino >= a_sortino) and (b_dd <= a_dd):
            recommended = f"promote_{b_label}"
            reasons.append("b beats or matches A on pnl/sortino and keeps drawdown no worse")
        else:
            recommended = f"no_promote_{b_label}"
            reasons.append("b wins points but fails conservative promotion gate")
    elif winner == a_label:
        if (a_pnl >= b_pnl) and (a_sortino >= b_sortino) and (a_dd <= b_dd):
            recommended = f"promote_{a_label}"
            reasons.append("a beats or matches B on pnl/sortino and keeps drawdown no worse")
        else:
            recommended = f"no_promote_{a_label}"
            reasons.append("a wins points but fails conservative promotion gate")
    else:
        reasons.append("tie result")

    return {
        "metric_results": results,
        "points": points,
        "winner": winner,
        "promotion_gate": {
            "recommended_action": recommended,
            "reasons": reasons,
        },
    }
```
**SOURCE thin wrapper:** keep signature, import `scripts.diagnostics.m26_ab_compare_projection` as `_b7_owner`; replace old body with sole `return _b7_owner._compare_metrics(a_label=a_label,b_label=b_label,a_score=a_score,b_score=b_score,facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade._json_path_get at invocation; output advisory only, no promotion execution; original negative/exception/identity behavior unchanged.
**NORMAL TARGETED `test_b7_compare_metrics`:** a metrics pnl10/sortino1/sharpe1/dd0.2/win0.4 vs b 12/2/2/0.1/0.6→winner='B',points B=5,recommended_action='promote_B'; identical→tie/hold. Assert original-golden == wrapper == direct Owner and AST thin delegation. **BLOCKED→NEXT:** record exact error and continue B8.

## B8 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_ab_evaluation.py::_run_scorecard_json` @ L34 | CURRENT_BLOB `864f845cd2e6644c134372745590ecafeabc70ee`
**NEW TARGET (404 actor/integration):** `scripts/diagnostics/m26_ab_scorecard_projection.py::_run_scorecard_json`. **MOVE COMPLETE EXECUTABLE BODY EXACTLY:**
```python
def _run_scorecard_json(*, dataset_root: Path, day: str) -> Tuple[int, Dict[str, Any]]:
    argv = ["--dataset-root", str(dataset_root), "--json"]
    if day:
        argv.extend(["--day", day])
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = scorecard_main(argv)
    out = buf.getvalue().strip()
    if not out:
        return int(rc), {}
    try:
        return int(rc), json.loads(out)
    except Exception:
        return int(rc), {}
```
**SOURCE thin wrapper:** keep signature, import `scripts.diagnostics.m26_ab_scorecard_projection` as `_b8_owner`; replace old body with sole `return _b8_owner._run_scorecard_json(dataset_root=dataset_root,day=day,facade=sys.modules[__name__])`. **CALLER/MONKEYPATCH:** facade.io.StringIO/redirect_stdout/scorecard_main/json; fake scorecard only, NEVER real scorecard/main or real dataset; original negative/exception/identity behavior unchanged.
**NORMAL TARGETED `test_b8_run_scorecard_json`:** patch SOURCE scorecard_main to fake printing '{"ok":true}' and returning 0→(0,{'ok':True}); fake invalid JSON→(0,{}). Assert original-golden == wrapper == direct Owner and AST thin delegation. **BLOCKED→NEXT:** record exact error and continue B1–B8 remaining / push.

## FUTURE RESERVE — 6/6 VERIFIED DESIGN ONLY, NOT EXECUTABLE IN THIS ORDER
Each distinct SOURCE was read on current B and integration with matching blob; unique TARGET files checked absent in BOTH directories. RF-063 owns these scripts/diagnostics paths. Reserve work requires fresh C03 reissue and source/target/caller check; NEVER implement it now. All file effects strictly TemporaryDirectory/fake only; never run main or actual data.

### R1 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_dataset_manifest_check.py::_utc_now_iso` @ L42 | BLOB `a0afae27c395837c8e2059bb6cf22c34baed03fe`
**TARGET ABSENT actor/integration:** `scripts/diagnostics/m26_manifest_now_projection.py::_utc_now_iso`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
```
**Future targeted normal fixture:** patch SOURCE datetime/timezone clock to fixed UTC; deterministic ISO output. **Isolation/compat:** clock only, no filesystem; thin SOURCE wrapper, use-time facade globals/patch parity, no duplicated BODY, no live effect.

### R2 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_dataset_manifest_check.py::_write_text` @ L46 | BLOB `a0afae27c395837c8e2059bb6cf22c34baed03fe`
**TARGET ABSENT actor/integration:** `scripts/diagnostics/m26_manifest_write_projection.py::_write_text`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
```
**Future targeted normal fixture:** TemporaryDirectory child path, content='x'→UTF-8 x and parent created. **Isolation/compat:** TEMP-ONLY IO; no real dataset path; thin SOURCE wrapper, use-time facade globals/patch parity, no duplicated BODY, no live effect.

### R3 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_dataset_manifest_check.py::_seed_demo_dataset` @ L51 | BLOB `a0afae27c395837c8e2059bb6cf22c34baed03fe`
**TARGET ABSENT actor/integration:** `scripts/diagnostics/m26_manifest_seed_projection.py::_seed_demo_dataset`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future targeted normal fixture:** TemporaryDirectory root→manifest.json schema_version m26.dataset_manifest.v1, all generated files confined to temp. **Isolation/compat:** TEMP-ONLY seed; no real data, no main; thin SOURCE wrapper, use-time facade globals/patch parity, no duplicated BODY, no live effect.

### R4 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_dataset_manifest_check.py::_validate_dataset` @ L177 | BLOB `a0afae27c395837c8e2059bb6cf22c34baed03fe`
**TARGET ABSENT actor/integration:** `scripts/diagnostics/m26_manifest_validate_projection.py::_validate_dataset`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future targeted normal fixture:** empty TemporaryDirectory→missing:manifest.json; seeded fake dataset→ok=True. **Isolation/compat:** read-only TEMP fixture, preserve file-order/errors; thin SOURCE wrapper, use-time facade globals/patch parity, no duplicated BODY, no live effect.

### R5 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_dataset_manifest_check.py::_build_parser` @ L243 | BLOB `a0afae27c395837c8e2059bb6cf22c34baed03fe`
**TARGET ABSENT actor/integration:** `scripts/diagnostics/m26_manifest_parser_projection.py::_build_parser`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M26 fixed dataset manifest scaffold and validation gate.")
    p.add_argument("--dataset-root", default="data/eval/m26_fixed_dataset_v1")
    p.add_argument("--seed-demo", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
```
**Future targeted normal fixture:** parse_args(['--seed-demo','--json'])→seed_demo=True,json=True. **Isolation/compat:** parser only; never seed via main; thin SOURCE wrapper, use-time facade globals/patch parity, no duplicated BODY, no live effect.

### R6 | RF-063 CODEX_B | SOURCE `scripts/diagnostics/run_m26_closeout_check.py::_build_parser` @ L129 | BLOB `4a87f8bdf0c1af655192521ead900431ebf66bba`
**TARGET ABSENT actor/integration:** `scripts/diagnostics/m26_closeout_parser_projection.py::_build_parser`. **ACTUAL VERIFIED BODY (DESIGN ONLY):**
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
**Future targeted normal fixture:** parse_args(['--day','2026-11-01','--json'])→day='2026-11-01',json=True. **Isolation/compat:** parser only; never execute destructive closeout/main; thin SOURCE wrapper, use-time facade globals/patch parity, no duplicated BODY, no live effect.

**COUNTS:** old C01 7/7 REMOTE_DONE, NEW_READY=8, RESERVE_VERIFIED=6. C03 publication is a document-only assignment, not G1/G2/G3 code development or RF DONE. If source/target changed since this snapshot, BLOCKED precisely and continue other safe items; do not silently reassign.
