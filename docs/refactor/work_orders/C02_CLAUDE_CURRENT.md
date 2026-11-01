# C02 — Claude A | A-20261101-11 | FAST-3 8 NEW SOURCE BODY MOVEs

**SINGLE ENTRY / PIN:** At start pin CANONICAL_HEAD, ORDER_FILE_BLOB_SHA, OWNER_REMOTE_SHA and ORDER_ID=A-20261101-11. Read only THIS document plus named code/test files. Do not read D00/RF/queue/C03/CURRENT/HANDOFF, self-select, modify other actor paths, or repeat old PASS. Execute all A1–A8; blocked item → next safe item. A-10 was 8/8 REMOTE_DONE at 9eb7ed3f27e8b362407196d13c6b5c035c50d8f3, normal 8/8 exit0, #11 comment 6551673840; no old item is assigned here.

**RF/OWNER/REMOTE BASIS:** RF-035, CLAUDE_A exclusive; SOURCE `libs/reporting/live_execution_event_evidence.py` blob `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c` verified same on integration and actor; A branch `work/p15-a-reporter-pure-20261021` HEAD `9eb7ed3f27e8b362407196d13c6b5c035c50d8f3`. All 8 target paths and 6 future reserve targets are absent on BOTH integration and A branch at issuance (directory membership check). Only SOURCE, the enumerated new Owner modules, and `tests/test_p15_rf035_20261101_11h_event_owners.py` are writable for this order. No C01/C03/D00/RF/STATUS/C04/C05/other-actor edits.

**SAFETY:** These are in-memory reporting evidence projections ONLY, not trading, live orders, Broker/Guard/Step5C/UEF, RunLab, deployment, filesystem/network writes, policy thresholds, or real data. Do not call actual runtime pipeline. SOURCE must retain same signature as thin facade; move entire original executable BODY to one new Owner, no duplicate calculation, no Owner→SOURCE import. Owner imports required typing/types and accepts extra keyword-only `facade` to resolve monkeypatch-sensitive globals at call time. Source wrapper imports new module inside function with unique alias `_c03_11_aN_owner`, delegates `return owner.fn(..., facade=sys.modules[__name__])`; import sys in SOURCE. Preserve positional/keyword/default, mutation/copy/iterator, order, exceptions, and monkeypatch behavior. For each test, capture original function golden BEFORE editing, compare wrapper/Owner with original and AST confirm source BODY removed.

**TEST/DELIVERY:** Add 8 independently named `unittest` tests to `tests/test_p15_rf035_20261101_11h_event_owners.py` using fake dicts and patched facade globals only. `python -m unittest tests/test_p15_rf035_20261101_11h_event_owners.py -v` expected exit0/8 tests (NOT_RUN until actor). Commit only allowed code/test, normal non-force push or approved expected-HEAD lease, re-fetch actor HEAD, source/Owner/test blob SHAs, and report exact commands/exits, each A1–A8, measured START_KST/END_KST/ELAPSED_MIN to #11. Git auth failure=PUSH_BLOCKED (not G1), pytest absence does not prevent stdlib unittest; continue other safe items. C04 integrates and C05 decides G1/G2/G3; this C03 document commit is DOC_ONLY, not a code MOVE.

## A1 | RF-035 CLAUDE_A | SOURCE `libs/reporting/live_execution_event_evidence.py::row_event_name` @ L11 | CURRENT_BLOB `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`
**TARGET (404 both refs):** `libs/reporting/live_event_name_projection.py::row_event_name`. Move entire original computation (below) into target; original becomes thin wrapper only. No double body, no Owner import of SOURCE.
```python
def row_event_name(row: Dict[str, Any]) -> str:
    text = str(row.get("event_name") or "").strip()
    if text:
        return text
    stage = str(row.get("stage") or "").strip()
    event = str(row.get("event") or "").strip()
    return ".".join(part for part in (stage, event) if part)
```
**WRAPPER / CALL-TIME PATCH:** `row_event_name(...)` delegates via `_c03_11_a1_owner.row_event_name(..., facade=sys.modules[__name__])`; Owner resolves no module globals through facade when used, with original argument binding and error parity. Preserve source module import/use-time patch seams; no caller changes.
**TARGETED `test_a1_row_event_name`:** row={'event_name':' scanner.hit '} -> 'scanner.hit'; {'stage':'scanner','event':'hit'} -> 'scanner.hit'; empty -> ''. Original golden vs thin wrapper vs Owner; positive/negative and exception/patch parity; AST ensures original computation gone. Fake/in-memory only. **BLOCKED→NEXT:** record first exact error/SHA to #11 and continue A2.

## A2 | RF-035 CLAUDE_A | SOURCE `libs/reporting/live_execution_event_evidence.py::event_row_symbol` @ L20 | CURRENT_BLOB `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`
**TARGET (404 both refs):** `libs/reporting/live_event_symbol_projection.py::event_row_symbol`. Move entire original computation (below) into target; original becomes thin wrapper only. No double body, no Owner import of SOURCE.
```python
def event_row_symbol(row: Dict[str, Any]) -> str:
    payload = row.get("payload") if isinstance(row.get("payload"), dict) else {}
    return normalize_symbol(
        row.get("symbol")
        or payload.get("symbol")
        or payload.get("selected_symbol")
        or payload.get("position_symbol")
        or "",
        allow_test_symbols=True,
    )
```
**WRAPPER / CALL-TIME PATCH:** `event_row_symbol(...)` delegates via `_c03_11_a2_owner.event_row_symbol(..., facade=sys.modules[__name__])`; Owner resolves `normalize_symbol` through facade when used, with original argument binding and error parity. Preserve source module import/use-time patch seams; no caller changes.
**TARGETED `test_a2_event_row_symbol`:** row={'symbol':'005930'} -> normalize_symbol('005930',allow_test_symbols=True); payload.selected_symbol fallback; monkeypatch SOURCE.normalize_symbol to fake to prove call-time. Original golden vs thin wrapper vs Owner; positive/negative and exception/patch parity; AST ensures original computation gone. Fake/in-memory only. **BLOCKED→NEXT:** record first exact error/SHA to #11 and continue A3.

## A3 | RF-035 CLAUDE_A | SOURCE `libs/reporting/live_execution_event_evidence.py::event_row_name` @ L32 | CURRENT_BLOB `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`
**TARGET (404 both refs):** `libs/reporting/live_event_row_name_projection.py::event_row_name`. Move entire original computation (below) into target; original becomes thin wrapper only. No double body, no Owner import of SOURCE.
```python
def event_row_name(row: Dict[str, Any]) -> str:
    return str(row.get("event_name") or row.get("name") or row.get("event") or "").strip()
```
**WRAPPER / CALL-TIME PATCH:** `event_row_name(...)` delegates via `_c03_11_a3_owner.event_row_name(..., facade=sys.modules[__name__])`; Owner resolves no module globals through facade when used, with original argument binding and error parity. Preserve source module import/use-time patch seams; no caller changes.
**TARGETED `test_a3_event_row_name`:** row={'name':'fallback'} -> 'fallback'; {'event_name':'x'} -> 'x'; absent -> ''. Original golden vs thin wrapper vs Owner; positive/negative and exception/patch parity; AST ensures original computation gone. Fake/in-memory only. **BLOCKED→NEXT:** record first exact error/SHA to #11 and continue A4.

## A4 | RF-035 CLAUDE_A | SOURCE `libs/reporting/live_execution_event_evidence.py::merge_rows_by_identity` @ L36 | CURRENT_BLOB `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`
**TARGET (404 both refs):** `libs/reporting/live_event_identity_merge_projection.py::merge_rows_by_identity`. Move entire original computation (below) into target; original becomes thin wrapper only. No double body, no Owner import of SOURCE.
```python
def merge_rows_by_identity(*collections: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    seen: set[tuple[str, str, str, str]] = set()
    for rows in collections:
        for row in list(rows or []):
            if not isinstance(row, dict):
                continue
            key = (
                str(row.get("ts") or row.get("timestamp") or ""),
                str(row.get("run_id") or ""),
                event_row_name(row),
                event_row_symbol(row),
            )
            if key in seen:
                continue
            seen.add(key)
            out.append(row)
    return out
```
**WRAPPER / CALL-TIME PATCH:** `merge_rows_by_identity(...)` delegates via `_c03_11_a4_owner.merge_rows_by_identity(..., facade=sys.modules[__name__])`; Owner resolves `event_row_name`, `event_row_symbol` through facade when used, with original argument binding and error parity. Preserve source module import/use-time patch seams; no caller changes.
**TARGETED `test_a4_merge_rows_by_identity`:** two equal (ts,run_id,event name,symbol) dicts -> first object retained, order preserved, duplicate removed; non-dict ignored; monkeypatch SOURCE.event_row_name/event_row_symbol. Original golden vs thin wrapper vs Owner; positive/negative and exception/patch parity; AST ensures original computation gone. Fake/in-memory only. **BLOCKED→NEXT:** record first exact error/SHA to #11 and continue A5.

## A5 | RF-035 CLAUDE_A | SOURCE `libs/reporting/live_execution_event_evidence.py::filter_canonical_events` @ L56 | CURRENT_BLOB `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`
**TARGET (404 both refs):** `libs/reporting/live_event_canonical_filter_projection.py::filter_canonical_events`. Move entire original computation (below) into target; original becomes thin wrapper only. No double body, no Owner import of SOURCE.
```python
def filter_canonical_events(
    rows: List[Dict[str, Any]],
    *,
    run_ids: List[str],
    agent: str,
    event_names: List[str],
) -> List[Dict[str, Any]]:
    run_set = {str(item or "").strip() for item in list(run_ids or []) if str(item or "").strip()}
    names = {str(item or "").strip() for item in list(event_names or []) if str(item or "").strip()}
    out: List[Dict[str, Any]] = []
    for row in rows:
        if run_set and str(row.get("run_id") or "").strip() not in run_set:
            continue
        row_agent = str(row.get("agent") or row.get("stage") or "").strip().lower()
        if row_agent != str(agent or "").strip().lower():
            continue
        if names and row_event_name(row) not in names:
            continue
        out.append(
            {
                "ts": str(row.get("ts") or ""),
                "event_name": row_event_name(row),
                "level": str(row.get("level") or "info"),
                "run_id": str(row.get("run_id") or ""),
                "trade_id": str(row.get("trade_id") or ""),
                "session_id": str(row.get("session_id") or ""),
                "cycle_id": str(row.get("cycle_id") or ""),
                "agent": str(row.get("agent") or row.get("stage") or ""),
                "phase": str(row.get("phase") or ""),
                "symbol": str(row.get("symbol") or ""),
                "payload": dict(row.get("payload") or {}) if isinstance(row.get("payload"), dict) else {},
            }
        )
    out.sort(key=lambda item: to_epoch(item.get("ts")) or 0)
    return out
```
**WRAPPER / CALL-TIME PATCH:** `filter_canonical_events(...)` delegates via `_c03_11_a5_owner.filter_canonical_events(..., facade=sys.modules[__name__])`; Owner resolves `row_event_name`, `to_epoch` through facade when used, with original argument binding and error parity. Preserve source module import/use-time patch seams; no caller changes.
**TARGETED `test_a5_filter_canonical_events`:** rows with agent=strategist/run_id=r1, timestamp 2 and 1, event_names=['strategist.decision_frame'] -> chronological ts 1,2; wrong agent/run excluded; payload copied; patch SOURCE.to_epoch. Original golden vs thin wrapper vs Owner; positive/negative and exception/patch parity; AST ensures original computation gone. Fake/in-memory only. **BLOCKED→NEXT:** record first exact error/SHA to #11 and continue A6.

## A6 | RF-035 CLAUDE_A | SOURCE `libs/reporting/live_execution_event_evidence.py::resolve_strategist_source_run_ids` @ L93 | CURRENT_BLOB `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`
**TARGET (404 both refs):** `libs/reporting/live_event_strategist_source_ids_projection.py::resolve_strategist_source_run_ids`. Move entire original computation (below) into target; original becomes thin wrapper only. No double body, no Owner import of SOURCE.
```python
def resolve_strategist_source_run_ids(
    *,
    event_rows: List[Dict[str, Any]],
    lifecycle: Dict[str, Any],
) -> Tuple[List[str], Dict[str, str]]:
    lifecycle_run_ids = [str(x or "").strip() for x in list(lifecycle.get("run_ids_all") or []) if str(x or "").strip()]
    if not lifecycle_run_ids:
        return [], {}

    strategist_event_names = {
        "strategist.market_context_snapshot",
        "strategist.global_sentiment_breakdown",
        "strategist.news_evidence_ranked",
        "strategist.decision_frame",
        "strategist.llm_response_saved",
    }
    strategist_run_ids = {
        str(row.get("run_id") or "").strip()
        for row in event_rows
        if str(row.get("run_id") or "").strip() in set(lifecycle_run_ids)
        and str(row.get("agent") or row.get("stage") or "").strip().lower() == "strategist"
        and row_event_name(row) in strategist_event_names
    }

    strategist_frame_rows = [
        row
        for row in event_rows
        if str(row.get("agent") or row.get("stage") or "").strip().lower() == "strategist"
        and row_event_name(row) == "strategist.decision_frame"
    ]
    strategist_frame_rows.sort(key=lambda row: to_epoch(row.get("ts")) or 0)

    linked_cached_frames: Dict[str, str] = {}
    for run_id in lifecycle_run_ids:
        if run_id in strategist_run_ids:
            continue
        fast_path_rows = [
            row
            for row in event_rows
            if str(row.get("run_id") or "").strip() == run_id
            and row_event_name(row) == "commander_router.fast_path"
        ]
        if not fast_path_rows:
            continue
        fast_path = fast_path_rows[-1]
        payload = fast_path.get("payload") if isinstance(fast_path.get("payload"), dict) else {}
        if str(payload.get("path") or "").strip() != "integrated_chain_cached_frame":
            continue
        target_ts = to_epoch(fast_path.get("ts")) or 0
        reuse_sec = max(30, safe_int(payload.get("reuse_sec"), 180))
        candidate_rows = [
            row
            for row in strategist_frame_rows
            if str(row.get("run_id") or "").strip() != run_id
            and (to_epoch(row.get("ts")) or 0) <= target_ts
            and target_ts - (to_epoch(row.get("ts")) or 0) <= reuse_sec + 30
        ]
        if not candidate_rows:
            continue
        source_run_id = str(candidate_rows[-1].get("run_id") or "").strip()
        if not source_run_id:
            continue
        strategist_run_ids.add(source_run_id)
        linked_cached_frames[run_id] = source_run_id

    return sorted(strategist_run_ids), linked_cached_frames
```
**WRAPPER / CALL-TIME PATCH:** `resolve_strategist_source_run_ids(...)` delegates via `_c03_11_a6_owner.resolve_strategist_source_run_ids(..., facade=sys.modules[__name__])`; Owner resolves `row_event_name`, `to_epoch`, `safe_int` through facade when used, with original argument binding and error parity. Preserve source module import/use-time patch seams; no caller changes.
**TARGETED `test_a6_resolve_strategist_source_run_ids`:** lifecycle={'run_ids_all':['r1']} + direct strategist decision_frame run r1 -> (['r1'],{}); cached commander fast_path r1 at ts=200 with strategist frame r0 at ts=190 and reuse_sec=180 -> (['r0'],{'r1':'r0'}); patch SOURCE.safe_int/to_epoch. Original golden vs thin wrapper vs Owner; positive/negative and exception/patch parity; AST ensures original computation gone. Fake/in-memory only. **BLOCKED→NEXT:** record first exact error/SHA to #11 and continue A7.

## A7 | RF-035 CLAUDE_A | SOURCE `libs/reporting/live_execution_event_evidence.py::expand_targeted_run_ids_with_cached_strategist_sources` @ L161 | CURRENT_BLOB `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`
**TARGET (404 both refs):** `libs/reporting/live_event_expand_run_ids_projection.py::expand_targeted_run_ids_with_cached_strategist_sources`. Move entire original computation (below) into target; original becomes thin wrapper only. No double body, no Owner import of SOURCE.
```python
def expand_targeted_run_ids_with_cached_strategist_sources(
    *,
    event_rows: List[Dict[str, Any]],
    targeted_run_ids: Iterable[str],
) -> Set[str]:
    out: Set[str] = {
        str(run_id or "").strip()
        for run_id in list(targeted_run_ids or [])
        if str(run_id or "").strip()
    }
    if not out:
        return out

    strategist_frame_rows = [
        row
        for row in list(event_rows or [])
        if str(row.get("agent") or row.get("stage") or "").strip().lower() == "strategist"
        and row_event_name(row) == "strategist.decision_frame"
    ]
    strategist_frame_rows.sort(key=lambda row: to_epoch(row.get("ts")) or 0)
    if not strategist_frame_rows:
        return out

    fast_path_rows = [
        row
        for row in list(event_rows or [])
        if str(row.get("run_id") or "").strip() in out
        and row_event_name(row) == "commander_router.fast_path"
    ]
    for fast_path in fast_path_rows:
        payload = fast_path.get("payload") if isinstance(fast_path.get("payload"), dict) else {}
        if str(payload.get("path") or "").strip() != "integrated_chain_cached_frame":
            continue
        target_run_id = str(fast_path.get("run_id") or "").strip()
        target_ts = to_epoch(fast_path.get("ts")) or 0
        reuse_sec = max(30, safe_int(payload.get("reuse_sec"), 180))
        candidate_rows = [
            row
            for row in strategist_frame_rows
            if str(row.get("run_id") or "").strip() != target_run_id
            and (to_epoch(row.get("ts")) or 0) <= target_ts
            and target_ts - (to_epoch(row.get("ts")) or 0) <= reuse_sec + 30
        ]
        if not candidate_rows:
            continue
        source_run_id = str(candidate_rows[-1].get("run_id") or "").strip()
        if source_run_id:
            out.add(source_run_id)
    return out
```
**WRAPPER / CALL-TIME PATCH:** `expand_targeted_run_ids_with_cached_strategist_sources(...)` delegates via `_c03_11_a7_owner.expand_targeted_run_ids_with_cached_strategist_sources(..., facade=sys.modules[__name__])`; Owner resolves `row_event_name`, `to_epoch`, `safe_int` through facade when used, with original argument binding and error parity. Preserve source module import/use-time patch seams; no caller changes.
**TARGETED `test_a7_expand_targeted_run_ids_with_cached_strategist_sources`:** targeted_run_ids=['r1'], commander fast_path r1 ts=200 and strategist frame r0 ts=190 -> {'r1','r0'}; absent/expired cached frame -> {'r1'}; no clock or disk. Original golden vs thin wrapper vs Owner; positive/negative and exception/patch parity; AST ensures original computation gone. Fake/in-memory only. **BLOCKED→NEXT:** record first exact error/SHA to #11 and continue A8.

## A8 | RF-035 CLAUDE_A | SOURCE `libs/reporting/live_execution_event_evidence.py::latest_event_payload` @ L212 | CURRENT_BLOB `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`
**TARGET (404 both refs):** `libs/reporting/live_event_latest_payload_projection.py::latest_event_payload`. Move entire original computation (below) into target; original becomes thin wrapper only. No double body, no Owner import of SOURCE.
```python
def latest_event_payload(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not rows:
        return {}
    payload = rows[-1].get("payload") if isinstance(rows[-1], dict) else {}
    return dict(payload or {}) if isinstance(payload, dict) else {}
```
**WRAPPER / CALL-TIME PATCH:** `latest_event_payload(...)` delegates via `_c03_11_a8_owner.latest_event_payload(..., facade=sys.modules[__name__])`; Owner resolves no module globals through facade when used, with original argument binding and error parity. Preserve source module import/use-time patch seams; no caller changes.
**TARGETED `test_a8_latest_event_payload`:** [{'payload':{'a':1}}] -> {'a':1} new dict, [] -> {}, last non-dict -> {}; original vs facade vs Owner parity. Original golden vs thin wrapper vs Owner; positive/negative and exception/patch parity; AST ensures original computation gone. Fake/in-memory only. **BLOCKED→NEXT:** record first exact error/SHA to #11 and continue all other safe items and push.

## FUTURE RESERVE — VERIFIED 6/6 (DESIGN ONLY; NOT EXECUTABLE, NO SELF-SELECTION)

- **R1 RF-035 CLAUDE_A VERIFIED:** SOURCE `libs/reporting/live_execution_event_evidence.py::headline_count` @ L219 blob `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`; TARGET `libs/reporting/live_event_headline_count_projection.py::headline_count` absent both refs. BODY: `total = 0 for row in list(news_rows or []): if not isinstance(row, dict):` (full original BODY confirmed, not a wrapper); facade seams safe_int; in-memory/no IO, test [{'headline_count':2},{'headline_count':'3'},{}] -> 5; invalid dict skipped. Reserve only; next C03 must revalidate source/target before promotion.
- **R2 RF-035 CLAUDE_A VERIFIED:** SOURCE `libs/reporting/live_execution_event_evidence.py::hydrate_strategist_payload_from_evidence` @ L228 blob `af7cc5dd91e9c8325542ddb63eba7c03d5a41e8c`; TARGET `libs/reporting/live_event_hydrate_projection.py::hydrate_strategist_payload_from_evidence` absent both refs. BODY: `strategist_payload: Dict[str, Any], strategist_evidence: Dict[str, Any], ) -> Dict[str, Any]:` (full original BODY confirmed, not a wrapper); facade seams latest_event_payload,safe_float,safe_int,headline_count; in-memory/no IO, test empty evidence preserves supplied payload; fake market_context/decision_frame populates missing keys only, never overwrites existing. Reserve only; next C03 must revalidate source/target before promotion.
- **R3 RF-035 CLAUDE_A VERIFIED:** SOURCE `libs/reporting/live_execution_report_context.py::null_if_empty` @ L10 blob `52f877f641d552e34e529c95182035a0d1c013ff`; TARGET `libs/reporting/live_report_null_projection.py::null_if_empty` absent both refs. BODY: `if value in (None, ""): return None if isinstance(value, str):` (full original BODY confirmed, not a wrapper); facade seams none; in-memory/no IO, test '  ' -> None; ' hi ' -> 'hi'; 0 -> 0. Reserve only; next C03 must revalidate source/target before promotion.
- **R4 RF-035 CLAUDE_A VERIFIED:** SOURCE `libs/reporting/live_execution_report_context.py::build_failure_classification` @ L19 blob `52f877f641d552e34e529c95182035a0d1c013ff`; TARGET `libs/reporting/live_report_failure_projection.py::build_failure_classification` absent both refs. BODY: `*, lifecycle: Dict[str, Any], diagnostics: Dict[str, Any],` (full original BODY confirmed, not a wrapper); facade seams none; in-memory/no IO, test empty lifecycle -> entry_failure True; closed without exit -> exit_failure True; reporter missing -> reporting_failure True. Reserve only; next C03 must revalidate source/target before promotion.
- **R5 RF-035 CLAUDE_A VERIFIED:** SOURCE `libs/reporting/live_execution_report_context.py::to_epoch` @ L51 blob `52f877f641d552e34e529c95182035a0d1c013ff`; TARGET `libs/reporting/live_report_epoch_projection.py::to_epoch` absent both refs. BODY: `if ts is None: return None if isinstance(ts, (int, float)):` (full original BODY confirmed, not a wrapper); facade seams datetime,timezone; in-memory/no IO, test 1970-01-01T00:00:01Z -> 1; invalid -> None; naive UTC parity. Reserve only; next C03 must revalidate source/target before promotion.
- **R6 RF-035 CLAUDE_A VERIFIED:** SOURCE `libs/reporting/live_execution_report_context.py::utc_day` @ L73 blob `52f877f641d552e34e529c95182035a0d1c013ff`; TARGET `libs/reporting/live_report_utc_day_projection.py::utc_day` absent both refs. BODY: `epoch = to_epoch(ts) if epoch is None: return ""` (full original BODY confirmed, not a wrapper); facade seams to_epoch,datetime,timezone; in-memory/no IO, test epoch 1 -> 1970-01-01; invalid -> ''. Reserve only; next C03 must revalidate source/target before promotion.

**COUNTS:** A-10 REMOTE_DONE=8/8; NEW_READY=8 real SOURCE BODY MOVEs; FUTURE_RESERVE_VERIFIED=6/6; actor implementation/testing NOT_RUN at issuance; C03 DOC_ONLY G1/G2/G3=0, RF_DONE_DELTA=0. RunLab Exited(255), RUN_SOURCE_SHA=UNKNOWN; no runtime action.
