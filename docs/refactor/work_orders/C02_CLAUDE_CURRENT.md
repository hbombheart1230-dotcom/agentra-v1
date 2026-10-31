# C02 — Claude A | A-20261101-08 | FAST-3 EIGHT NEW VERIFIED BODY MOVEs

**SINGLE ENTRY / PIN:** At start pin `integration/p1.5` HEAD, this C02 blob, A branch HEAD, ORDER_ID. Execute ALL A1–A8. Read this C02 and named code/test only; no D00/RF/queue/C03/CURRENT/HANDOFF. Earlier start-pinned order remains valid; do not redo prior completed functions.

**REMOTE_DONE:** A-20261101-07 8/8 at A remote `58dd2993872d251dffc74aa3b06e6c5cb12889e4`, #11 comment `6549882523`, normal targeted unittest 8/8 exit0. Exact A code/test integrated at `341f6c4306b5d9383a5c7c3938553ba196f92703`, C05 accepted narrow G1/G2/G3 (RF-035 previously DONE, no new RF DONE). All A-07 same-SHA tests/KEEP are excluded from this order.

**OWNER/SAFETY:** RF-035 CLAUDE_A only; SOURCE `libs/reporting/quant_shadow_forward_outcomes.py` actor/integration current blob `b28078090a76181ba503c1251c6fc607ac63abaa` (identical checked). Only change this SOURCE, eight new `libs/reporting/quant_forward_*_projection.py` Owner files named below, and NEW `tests/test_p15_rf035_20261101_08h_forward_owners.py` on `work/p15-a-reporter-pure-20261021`. This is evaluation/read-model math only; no state JSON reads, market data/network, real trading, promotion, Broker/Guard/Step5C/UEF/RunLab, runtime/CI/frozen oracle or other-owner files. Never run `load_minute_rows_from_state`, `attach_forward_outcomes` with default state, real CLI or actual report dirs. Use in-memory rows, fake datetime and temp-only if needed. No force push.

**IMPLEMENTATION CONTRACT:** Capture golden from original pinned SOURCE before editing. For each item copy the **complete original executable body** shown below to the new Owner function with original args plus keyword-only `facade`; replace only references to patchable SOURCE globals with the listed `facade.<name>` lookups. Owner imports safe typing/datetime only as required, **never imports SOURCE**. Keep original SOURCE function name/signature/annotations as a **single-return thin wrapper** with unique local import `from libs.reporting import <target module> as _a08_N_owner` inside function, `return _a08_N_owner.<function>(<original arguments>, facade=sys.modules[__name__])`. Add `import sys` in SOURCE (absent at pinned blob). For patched source globals, resolution must happen at call time through facade; preserve datetime/KST semantics, output/error order, default handling, alias/copy. No duplicate computation in SOURCE. Keep all other functions including `load_minute_rows_from_state`, `attach_forward_outcomes`, `_normalize_rows` unchanged.

**TEST/PUSH:** Write 8 independent stdlib unittest methods `test_a1_*` through `test_a8_*` in NEW file; each compare original-golden vs SOURCE wrapper vs direct Owner using same fake facade; positive, negative, exception/patch seam as applicable. AST asserts original SOURCE body removed, Owner has actual computation, no cyclic import. `python -m unittest tests/test_p15_rf035_20261101_08h_forward_owners.py -v` normal exit0 required; optional narrow existing forward outcome test, no blanket -O/full peer/hosted CI. Commit ONLY A code/test, normal non-force push, re-fetch A branch HEAD and SOURCE/Owner/test Git blobs; #11 report per-item status, exact normal command/exit, remote SHA, measured START_KST/END_KST/ELAPSED_MIN (never estimate). If any item SHA/owner differs or safety issue arises, mark that item BLOCKED and continue all other safe items. Git auth failure is PUSH_BLOCKED, not code G1. C04 owns selective integration; C05 owns G1/G2/G3/STATUS/DONE.

## A1 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_forward_outcomes.py::_to_float` @ L19 | CURRENT_BLOB `b28078090a76181ba503c1251c6fc607ac63abaa`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/quant_forward_float_projection.py::_to_float`. MOVE **EXACT executable BODY** below into Owner, including try/except and ordering; SOURCE retains thin wrapper only.
```python
def _to_float(value: Any, default: float | None = None) -> float | None:
    try:
        if value in (None, ""):
            return default
        return float(value)
    except Exception:
        return default
```
**WRAPPER/CALL-TIME PATCH:** SOURCE local import alias `_a08_1_owner`; original signature unchanged; return `_a08_1_owner._to_float(value, default, facade=sys.modules[__name__])`. Owner's call-time globals: none (stdlib float). No SOURCE import in Owner. Test original-vs-wrapper-vs-Owner and preserve TypeError/exception behavior.
**NORMAL TARGETED `test_a1_to_float`:** '1.25'→1.25; None with default=2.0→2.0; 'bad'→default; exception parity. In-memory fake fixture, no operational IO; verify AST old SOURCE computation removed. **BLOCKED→NEXT:** record exact SHA/error, continue A2.

## A2 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_forward_outcomes.py::_to_int` @ L28 | CURRENT_BLOB `b28078090a76181ba503c1251c6fc607ac63abaa`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/quant_forward_int_projection.py::_to_int`. MOVE **EXACT executable BODY** below into Owner, including try/except and ordering; SOURCE retains thin wrapper only.
```python
def _to_int(value: Any, default: int = 0) -> int:
    try:
        if value in (None, ""):
            return int(default)
        return int(float(value))
    except Exception:
        return int(default)
```
**WRAPPER/CALL-TIME PATCH:** SOURCE local import alias `_a08_2_owner`; original signature unchanged; return `_a08_2_owner._to_int(value, default, facade=sys.modules[__name__])`. Owner's call-time globals: none (stdlib int/float). No SOURCE import in Owner. Test original-vs-wrapper-vs-Owner and preserve TypeError/exception behavior.
**NORMAL TARGETED `test_a2_to_int`:** '2.9'→2; None default=7→7; 'bad' default=7→7. In-memory fake fixture, no operational IO; verify AST old SOURCE computation removed. **BLOCKED→NEXT:** record exact SHA/error, continue A3.

## A3 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_forward_outcomes.py::_text` @ L37 | CURRENT_BLOB `b28078090a76181ba503c1251c6fc607ac63abaa`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/quant_forward_text_projection.py::_text`. MOVE **EXACT executable BODY** below into Owner, including try/except and ordering; SOURCE retains thin wrapper only.
```python
def _text(value: Any) -> str:
    return str(value or "").strip()
```
**WRAPPER/CALL-TIME PATCH:** SOURCE local import alias `_a08_3_owner`; original signature unchanged; return `_a08_3_owner._text(value, facade=sys.modules[__name__])`. Owner's call-time globals: none. No SOURCE import in Owner. Test original-vs-wrapper-vs-Owner and preserve TypeError/exception behavior.
**NORMAL TARGETED `test_a3_text`:** '  ABC  '→'ABC'; None→''; odd __str__ exception parity. In-memory fake fixture, no operational IO; verify AST old SOURCE computation removed. **BLOCKED→NEXT:** record exact SHA/error, continue A4.

## A4 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_forward_outcomes.py::_parse_epoch` @ L41 | CURRENT_BLOB `b28078090a76181ba503c1251c6fc607ac63abaa`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/quant_forward_epoch_projection.py::_parse_epoch`. MOVE **EXACT executable BODY** below into Owner, including try/except and ordering; SOURCE retains thin wrapper only.
```python
def _parse_epoch(value: Any) -> int:
    if value in (None, ""):
        return 0
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value or "").strip()
    if not text:
        return 0
    try:
        return int(float(text))
    except Exception:
        pass
    try:
        return int(datetime.fromisoformat(text.replace("Z", "+00:00")).timestamp())
    except Exception:
        return 0
```
**WRAPPER/CALL-TIME PATCH:** SOURCE local import alias `_a08_4_owner`; original signature unchanged; return `_a08_4_owner._parse_epoch(value, facade=sys.modules[__name__])`. Owner's call-time globals: datetime: use facade.datetime in Owner. No SOURCE import in Owner. Test original-vs-wrapper-vs-Owner and preserve TypeError/exception behavior.
**NORMAL TARGETED `test_a4_parse_epoch`:** '1970-01-01T00:00:01Z'→1; '1'→1; invalid→0; patched datetime seam. In-memory fake fixture, no operational IO; verify AST old SOURCE computation removed. **BLOCKED→NEXT:** record exact SHA/error, continue A5.

## A5 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_forward_outcomes.py::_parse_raw_ts_epoch` @ L59 | CURRENT_BLOB `b28078090a76181ba503c1251c6fc607ac63abaa`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/quant_forward_raw_epoch_projection.py::_parse_raw_ts_epoch`. MOVE **EXACT executable BODY** below into Owner, including try/except and ordering; SOURCE retains thin wrapper only.
```python
def _parse_raw_ts_epoch(value: Any) -> int:
    text = _text(value)
    if len(text) >= 14 and text[:14].isdigit():
        try:
            return int(datetime.strptime(text[:14], "%Y%m%d%H%M%S").replace(tzinfo=KST).timestamp())
        except Exception:
            return 0
    return _parse_epoch(text)
```
**WRAPPER/CALL-TIME PATCH:** SOURCE local import alias `_a08_5_owner`; original signature unchanged; return `_a08_5_owner._parse_raw_ts_epoch(value, facade=sys.modules[__name__])`. Owner's call-time globals: _text,datetime,KST,_parse_epoch: facade._text/facade.datetime/facade.KST/facade._parse_epoch. No SOURCE import in Owner. Test original-vs-wrapper-vs-Owner and preserve TypeError/exception behavior.
**NORMAL TARGETED `test_a5_parse_raw_ts_epoch`:** '19700101090001'→1; '1970-01-01T00:00:01Z'→1; invalid→0; patched facade._parse_epoch seam. In-memory fake fixture, no operational IO; verify AST old SOURCE computation removed. **BLOCKED→NEXT:** record exact SHA/error, continue A6.

## A6 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_forward_outcomes.py::_kst_day_from_epoch` @ L69 | CURRENT_BLOB `b28078090a76181ba503c1251c6fc607ac63abaa`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/quant_forward_kst_day_projection.py::_kst_day_from_epoch`. MOVE **EXACT executable BODY** below into Owner, including try/except and ordering; SOURCE retains thin wrapper only.
```python
def _kst_day_from_epoch(value: Any) -> str:
    epoch = _to_int(value, 0)
    if epoch <= 0:
        return ""
    try:
        return datetime.fromtimestamp(epoch, tz=KST).strftime("%Y%m%d")
    except Exception:
        return ""
```
**WRAPPER/CALL-TIME PATCH:** SOURCE local import alias `_a08_6_owner`; original signature unchanged; return `_a08_6_owner._kst_day_from_epoch(value, facade=sys.modules[__name__])`. Owner's call-time globals: _to_int,datetime,KST via facade. No SOURCE import in Owner. Test original-vs-wrapper-vs-Owner and preserve TypeError/exception behavior.
**NORMAL TARGETED `test_a6_kst_day_from_epoch`:** 1→'19700101'; 0→''; invalid→''; patched _to_int seam. In-memory fake fixture, no operational IO; verify AST old SOURCE computation removed. **BLOCKED→NEXT:** record exact SHA/error, continue A7.

## A7 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_forward_outcomes.py::_row_day` @ L79 | CURRENT_BLOB `b28078090a76181ba503c1251c6fc607ac63abaa`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/quant_forward_row_day_projection.py::_row_day`. MOVE **EXACT executable BODY** below into Owner, including try/except and ordering; SOURCE retains thin wrapper only.
```python
def _row_day(row: Mapping[str, Any]) -> str:
    raw_ts = _text(row.get("raw_ts"))
    if len(raw_ts) >= 8 and raw_ts[:8].isdigit():
        return raw_ts[:8]
    return _kst_day_from_epoch(row.get("ts"))
```
**WRAPPER/CALL-TIME PATCH:** SOURCE local import alias `_a08_7_owner`; original signature unchanged; return `_a08_7_owner._row_day(row, facade=sys.modules[__name__])`. Owner's call-time globals: _text,_kst_day_from_epoch via facade. No SOURCE import in Owner. Test original-vs-wrapper-vs-Owner and preserve TypeError/exception behavior.
**NORMAL TARGETED `test_a7_row_day`:** {'raw_ts':'20261101120000'}→'20261101'; {'ts':1}→'19700101'; patched _kst_day_from_epoch seam. In-memory fake fixture, no operational IO; verify AST old SOURCE computation removed. **BLOCKED→NEXT:** record exact SHA/error, continue A8.

## A8 | RF-035 CLAUDE_A | SOURCE `libs/reporting/quant_shadow_forward_outcomes.py::_kst_time_tuple` @ L86 | CURRENT_BLOB `b28078090a76181ba503c1251c6fc607ac63abaa`
**NEW TARGET (404 A/integration VERIFIED):** `libs/reporting/quant_forward_kst_time_projection.py::_kst_time_tuple`. MOVE **EXACT executable BODY** below into Owner, including try/except and ordering; SOURCE retains thin wrapper only.
```python
def _kst_time_tuple(row: Mapping[str, Any]) -> tuple[int, int]:
    epoch = _parse_raw_ts_epoch(row.get("raw_ts")) or _to_int(row.get("ts"), 0)
    if epoch <= 0:
        return (0, 0)
    dt = datetime.fromtimestamp(epoch, tz=KST)
    return (dt.hour, dt.minute)
```
**WRAPPER/CALL-TIME PATCH:** SOURCE local import alias `_a08_8_owner`; original signature unchanged; return `_a08_8_owner._kst_time_tuple(row, facade=sys.modules[__name__])`. Owner's call-time globals: _parse_raw_ts_epoch,_to_int,datetime,KST via facade. No SOURCE import in Owner. Test original-vs-wrapper-vs-Owner and preserve TypeError/exception behavior.
**NORMAL TARGETED `test_a8_kst_time_tuple`:** {'ts':1}→(9,0); {'ts':0}→(0,0); patched _parse_raw_ts_epoch seam. In-memory fake fixture, no operational IO; verify AST old SOURCE computation removed. **BLOCKED→NEXT:** record exact SHA/error, continue A1–A8 remaining and push.

## FUTURE RESERVE — VERIFIED 6/6 (DESIGN ONLY; **NOT EXECUTABLE**; C03 MUST ISSUE A NEW ORDER FIRST)
RF-035 CLAUDE_A exclusively; SOURCE `libs/reporting/q8_lane_decision_table.py` actor/integration exact blob `d997eef97b2a2077c1be638948e4355503d7c018`; all six TARGET paths independently returned 404 on BOTH actor branch and integration on 2026-11-01. These six are NOT part of the current executable order. No Actor self-selection or same-SHA retest. Each has no real-order, Broker/Guard/Step5C/UEF/RunLab effects; fake/in-memory fixtures only. Preserve original facade monkeypatch and exception behavior when C03 later issues them.

### RESERVE 1 | `libs/reporting/q8_lane_decision_table.py::_text` @ L14 | SOURCE_BLOB `d997eef97b2a2077c1be638948e4355503d7c018` → `libs/reporting/q8_lane_text_projection.py::_text` (404 both)
```python
def _text(value: Any) -> str:
    return str(value or "").strip()
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: none. NORMAL targeted golden/Owner/wrapper test: ' A '→'A', None→''. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 2 | `libs/reporting/q8_lane_decision_table.py::_float` @ L18 | SOURCE_BLOB `d997eef97b2a2077c1be638948e4355503d7c018` → `libs/reporting/q8_lane_float_projection.py::_float` (404 both)
```python
def _float(value: Any, default: float = 0.0) -> float:
    try:
        if value in (None, ""):
            return float(default)
        return float(value)
    except Exception:
        return float(default)
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: none. NORMAL targeted golden/Owner/wrapper test: '1.5'→1.5, bad default=3→3. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 3 | `libs/reporting/q8_lane_decision_table.py::_int` @ L27 | SOURCE_BLOB `d997eef97b2a2077c1be638948e4355503d7c018` → `libs/reporting/q8_lane_int_projection.py::_int` (404 both)
```python
def _int(value: Any, default: int = 0) -> int:
    try:
        if value in (None, ""):
            return int(default)
        return int(float(value))
    except Exception:
        return int(default)
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: none. NORMAL targeted golden/Owner/wrapper test: '2.9'→2, bad default=4→4. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 4 | `libs/reporting/q8_lane_decision_table.py::_rows` @ L36 | SOURCE_BLOB `d997eef97b2a2077c1be638948e4355503d7c018` → `libs/reporting/q8_lane_rows_projection.py::_rows` (404 both)
```python
def _rows(value: Any) -> List[Dict[str, Any]]:
    return [dict(row) for row in list(value or []) if isinstance(row, Mapping)]
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: Mapping via facade.Mapping. NORMAL targeted golden/Owner/wrapper test: [{'x':1},None]→[{'x':1}] copy-not-alias. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 5 | `libs/reporting/q8_lane_decision_table.py::_forward_rows` @ L40 | SOURCE_BLOB `d997eef97b2a2077c1be638948e4355503d7c018` → `libs/reporting/q8_lane_forward_rows_projection.py::_forward_rows` (404 both)
```python
def _forward_rows(evaluation: Mapping[str, Any]) -> List[Dict[str, Any]]:
    forward = evaluation.get("entry_lane_forward_outcomes")
    if not isinstance(forward, Mapping):
        return []
    return _rows(forward.get("by_primary_lane"))
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: Mapping and _rows via facade. NORMAL targeted golden/Owner/wrapper test: {'entry_lane_forward_outcomes':{'by_primary_lane':[{'name':'x'}]}}→one row; missing→[]. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

### RESERVE 6 | `libs/reporting/q8_lane_decision_table.py::_counts_by_name` @ L47 | SOURCE_BLOB `d997eef97b2a2077c1be638948e4355503d7c018` → `libs/reporting/q8_lane_counts_projection.py::_counts_by_name` (404 both)
```python
def _counts_by_name(rows: Iterable[Mapping[str, Any]]) -> Dict[str, int]:
    out: Dict[str, int] = {}
    for row in rows:
        name = _text(row.get("name"))
        if name:
            out[name] = _int(row.get("count"))
    return out
```
**DESIGN:** Entire BODY to unique Owner, SOURCE thin facade wrapper; monkeypatch seams: _text and _int via facade. NORMAL targeted golden/Owner/wrapper test: [{'name':'A','count':2},{'name':'B','count':'3'}]→{'A':2,'B':3}. No real IO, no state changes; clock via fake if applicable. **STATUS=RESERVE_VERIFIED, NOT ISSUED.**

**COUNTS:** A-07 REMOTE_DONE=8/8; A-08 NEW_READY=8; RESERVE_VERIFIED=6/6. C03 DOC_ONLY; code G1/G2/G3=0, RF_DONE_DELTA=0.
