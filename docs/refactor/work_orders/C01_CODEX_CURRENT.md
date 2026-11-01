# C01 — Codex B | B-20261101-14-C03 | RF DONE FIRST + NEW VERIFIED 8

**ONE FILE / PIN:** Record CANONICAL_HEAD, ORDER_BLOB, B_REMOTE_HEAD, ORDER_ID at session start. Already pinned earlier B14/B13 is not retroactively cancelled; finish safe pinned tasks first. B only writes code/tests on `work/p15-b-operator-structure-20261022`. No D00/RF/queue/C03/HANDOFF reread, no autonomous RF choice. No A-owned scanner source, frozen oracle, RF/STATUS/C04/C05 or operational code writes.

**REMOTE FACTS:** Before issuance canonical `77d527122addec442f615747a2f23307913c7070`; B actor `d530c2c6f6e3c99e8522b8631b4c0cddb37351bc`. #12 6553332265: old K1/K3/K4/B1/B2/B3/B7 **7/7 REMOTE_DONE**, C04 integrated exact seven at `1456f4a188a4383e1a829f661032ba046dead6d5`. Prior C01 still named those seven and asked B to resolve RF-014 A-owned frozen SOURCE collision; **both stale/cross-owner tasks removed**. RF-014 source blobs restored by A, frozen tests cannot be modified. Do not repeat old K2/B4/B5/B6/B8 or seven new integrated bodies.

## P0 — GIT/PYTEST BOOTSTRAP
Run `git --version` and `python -m pytest --version`; if pytest missing try `python -m pip install --user pytest` or isolated venv, rerun version check. Check `git remote -v`, `git fetch origin`, remote B ref. Report exact installation/auth errors as TEST_BLOCKED or PUSH_BLOCKED, not PASS. No full peer, blanket -O, per-RF hosted CI, real execution or mandatory 30min.

## P1 — FIRST PRIORITY: RF-063/065 G2/G1 CLOSEOUT (NOT NEW MOVES)
1. RF-063 **new reproducible G2**: `tests/test_p15_rf063_20261101_13h_residual_owners.py` exact blob `5acdb6f68c5e63aaeb4dc605d4adebed5c504dc7` is integrated but #12 only supplied an abbreviated `python -c` smoke. Run **once** `python -m pytest -q tests/test_p15_rf063_20261101_13h_residual_owners.py` on pinned B HEAD, report exit and count; do not claim pass until executed. No duplicate old K2 test.
2. RF-063 K3/K4 **populated-manifest golden+exception**: add B-owned `tests/test_p15_rf063_20261101_14h_manifest_golden.py`. In `TemporaryDirectory`, fake UTC clock and all manifest component paths, capture exact original pre-MOVE behavior from recorded preimage if available, compare `run_m26_dataset_manifest_check::_seed_demo_dataset` and `run_m26_closeout_check::_prepare_candidate_dataset` through their single Owners for JSON/CSV/JSONL bytes, manifest components and candidate close=115; invalid/exception parity. If original preimage unavailable report GOLDEN_NOT_VERIFIED, never invent parity. Run this new test once normal. Never call main or real filesystem paths.
3. RF-063 old **B-04 integrated-source G3** and **B1 normal G2**: supply exact existing SHA/test command/evidence if available; do not rerun same-SHA PASS or claim whole RF G3 from seven moves. C04/C05 own acceptance.
4. RF-065 G1 first unmet: `scripts/research/run_phase5_validation_bundle.py::_render_bundle_markdown` source blob `1beb655be5e3ec31c39ea05ded8da044c8b34e84` is already thin wrapper to `scripts/research/phase5_validation_markdown.py` blob `cc37e3ddf7ee1ed5b6eee7e8d28f6bff3d6ca7cb`; KEEP/REMOTE_DONE, no re-MOVE. Read-only static evidence for representative RF-065-owned `scripts/research/__init__.py`, `daily_profitability_scorecard.py`, `run_agent_effectiveness_scorecard.py`, `run_alpha_hypothesis_competition.py`: exact unchanged blobs, CLI entry/argv/cwd/output-root, safe KEEP or explicit SAFETY_HOLD. No research main, subprocess, UEF, live writes. Report specific G1 gaps for C05, not blanket 54-file retest.

## P2 — NEW RF-063 EIGHT REAL BODY MOVES, ONLY AFTER P1
Eight SOURCE functions verified as **real bodies** on identical B/integration blobs, TARGET 404 on BOTH refs. RF-063 CODEX_B exclusive `scripts/diagnostics/`; no B/A overlap. Move each complete computation BODY to its unique TARGET Owner, retain same-signature thin SOURCE wrapper with function-local import and `facade=sys.modules[__name__]` for call-time SOURCE monkeypatch/global references (`argparse`, `json`, `_extract_decision_action`, `_extract_allowed`). No duplicate computation. For `_iter_rows` only fake TemporaryDirectory file IO; `analyze_day_rows` in-memory only. Preserve return, ordering, exceptions, facade monkeypatch and original-before-edit golden. Create B-only `tests/test_p15_rf063_20261101_14h_supply_owners.py` with one test per item, normal/negative/exception + AST thin wrapper; run `python -m pytest -q tests/test_p15_rf063_20261101_14h_supply_owners.py` once, actual exit required. If one item blocked, record exact cause and continue next. No main, allocation, portfolio Guard, real orders or production State.

### P2-1 | RF-063 CODEX_B | `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_build_parser` @ L17 | CURRENT SOURCE BLOB `e8c050b18e8a523becf28db5c6c0f22198f46f37`
**TARGET 404 B+integration:** `scripts/diagnostics/m27_budget_parser_projection.py::_build_parser`. **ACTUAL SOURCE BODY TO MOVE:**
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M27-3 portfolio budget boundary check.")
    p.add_argument("--json", action="store_true")
    p.add_argument("--inject-fail", action="store_true")
    return p
```
**WRAPPER:** original signature + local import of sole Owner, forward args and call-time facade; for `analyze_day_rows` use `facade._extract_decision_action` and `facade._extract_allowed`, for parser use `facade.argparse`, for JSONL use `facade.json.loads`. **TARGETED NORMAL expected:** [] -> json=False, inject_fail=False; --json --inject-fail -> True/True. Compare original golden vs wrapper/Owner, negative/exception and patched SOURCE seam; no IO except temp JSONL. **BLOCKED→NEXT:** P2-2.

### P2-2 | RF-063 CODEX_B | `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_profiles` @ L24 | CURRENT SOURCE BLOB `e8c050b18e8a523becf28db5c6c0f22198f46f37`
**TARGET 404 B+integration:** `scripts/diagnostics/m27_budget_profiles_projection.py::_profiles`. **ACTUAL SOURCE BODY TO MOVE:**
```python
def _profiles() -> List[Dict[str, Any]]:
    return [
        {"strategy_id": "trend", "enabled": True, "weight": 0.5},
        {"strategy_id": "mean_reversion", "enabled": True, "weight": 0.3},
        {"strategy_id": "event_driven", "enabled": True, "weight": 0.2},
    ]
```
**WRAPPER:** original signature + local import of sole Owner, forward args and call-time facade; for `analyze_day_rows` use `facade._extract_decision_action` and `facade._extract_allowed`, for parser use `facade.argparse`, for JSONL use `facade.json.loads`. **TARGETED NORMAL expected:** three weights .5/.3/.2, order trend/mean_reversion/event_driven. Compare original golden vs wrapper/Owner, negative/exception and patched SOURCE seam; no IO except temp JSONL. **BLOCKED→NEXT:** P2-3.

### P2-3 | RF-063 CODEX_B | `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_intents` @ L32 | CURRENT SOURCE BLOB `e8c050b18e8a523becf28db5c6c0f22198f46f37`
**TARGET 404 B+integration:** `scripts/diagnostics/m27_budget_intents_projection.py::_intents`. **ACTUAL SOURCE BODY TO MOVE:**
```python
def _intents(*, inject_fail: bool) -> List[Dict[str, Any]]:
    if inject_fail:
        return [
            {
                "intent_id": "i1",
                "strategy_id": "trend",
                "symbol": "005930",
                "side": "BUY",
                "requested_notional": 300,
                "priority": 9,
                "confidence": 0.9,
            },
            {
                "intent_id": "i2",
                "strategy_id": "mean_reversion",
                "symbol": "000660",
                "side": "BUY",
                "requested_notional": 200,
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
            "requested_notional": 700,
            "priority": 9,
            "confidence": 0.9,
        },
        {
            "intent_id": "i2",
            "strategy_id": "trend",
            "symbol": "005930",
            "side": "BUY",
            "requested_notional": 400,
            "priority": 3,
            "confidence": 0.3,
        },
        {
            "intent_id": "i3",
            "strategy_id": "mean_reversion",
            "symbol": "005930",
            "side": "SELL",
            "requested_notional": 300,
            "priority": 8,
            "confidence": 0.8,
        },
        {
            "intent_id": "i4",
            "strategy_id": "event_driven",
            "symbol": "000660",
            "side": "BUY",
            "requested_notional": 350,
            "priority": 9,
            "confidence": 0.9,
        },
        {
            "intent_id": "i5",
            "strategy_id": "mean_reversion",
            "symbol": "000660",
            "side": "BUY",
            "requested_notional": 300,
            "priority": 4,
            "confidence": 0.4,
        },
    ]
```
**WRAPPER:** original signature + local import of sole Owner, forward args and call-time facade; for `analyze_day_rows` use `facade._extract_decision_action` and `facade._extract_allowed`, for parser use `facade.argparse`, for JSONL use `facade.json.loads`. **TARGETED NORMAL expected:** normal 5 intents; inject_fail 2 intents, all dictionaries, independent returned list. Compare original golden vs wrapper/Owner, negative/exception and patched SOURCE seam; no IO except temp JSONL. **BLOCKED→NEXT:** P2-4.

### P2-4 | RF-063 CODEX_B | `scripts/diagnostics/run_m27_portfolio_budget_boundary_check.py::_symbol_caps` @ L104 | CURRENT SOURCE BLOB `e8c050b18e8a523becf28db5c6c0f22198f46f37`
**TARGET 404 B+integration:** `scripts/diagnostics/m27_budget_caps_projection.py::_symbol_caps`. **ACTUAL SOURCE BODY TO MOVE:**
```python
def _symbol_caps(*, inject_fail: bool) -> Dict[str, float]:
    if inject_fail:
        return {"005930": 10_000.0, "000660": 10_000.0}
    return {"005930": 10_000.0, "000660": 500.0}
```
**WRAPPER:** original signature + local import of sole Owner, forward args and call-time facade; for `analyze_day_rows` use `facade._extract_decision_action` and `facade._extract_allowed`, for parser use `facade.argparse`, for JSONL use `facade.json.loads`. **TARGETED NORMAL expected:** normal 000660=500.0; inject_fail 000660=10000.0. Compare original golden vs wrapper/Owner, negative/exception and patched SOURCE seam; no IO except temp JSONL. **BLOCKED→NEXT:** P2-5.

### P2-5 | RF-063 CODEX_B | `scripts/diagnostics/run_m27_closeout_check.py::_build_parser` @ L30 | CURRENT SOURCE BLOB `1f48a79ecff887921682f180a1a3aa9214795416`
**TARGET 404 B+integration:** `scripts/diagnostics/m27_closeout_parser_projection.py::_build_parser`. **ACTUAL SOURCE BODY TO MOVE:**
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M27 closeout check (allocation/conflict/guard/metrics/notify).")
    p.add_argument("--event-log-dir", default="data/logs/m27_closeout")
    p.add_argument("--report-dir", default="reports/m27_closeout")
    p.add_argument("--day", default="2026-02-20")
    p.add_argument("--inject-fail", action="store_true")
    p.add_argument("--no-clear", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
```
**WRAPPER:** original signature + local import of sole Owner, forward args and call-time facade; for `analyze_day_rows` use `facade._extract_decision_action` and `facade._extract_allowed`, for parser use `facade.argparse`, for JSONL use `facade.json.loads`. **TARGETED NORMAL expected:** default day=2026-02-20; --json --no-clear -> True/True. Compare original golden vs wrapper/Owner, negative/exception and patched SOURCE seam; no IO except temp JSONL. **BLOCKED→NEXT:** P2-6.

### P2-6 | RF-063 CODEX_B | `scripts/diagnostics/run_m29_closeout_check.py::_build_parser` @ L25 | CURRENT SOURCE BLOB `ac491cb4ec89ff72ed64d9466055f06f936019f3`
**TARGET 404 B+integration:** `scripts/diagnostics/m29_closeout_parser_projection.py::_build_parser`. **ACTUAL SOURCE BODY TO MOVE:**
```python
def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M29 governance closeout check (audit/archive/timeline/dr).")
    p.add_argument("--event-log-dir", default="data/logs/m29_closeout")
    p.add_argument("--report-dir", default="reports/m29_closeout")
    p.add_argument("--day", default="2026-02-21")
    p.add_argument("--inject-fail", action="store_true")
    p.add_argument("--no-clear", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
```
**WRAPPER:** original signature + local import of sole Owner, forward args and call-time facade; for `analyze_day_rows` use `facade._extract_decision_action` and `facade._extract_allowed`, for parser use `facade.argparse`, for JSONL use `facade.json.loads`. **TARGETED NORMAL expected:** default day=2026-02-21; --json --no-clear -> True/True. Compare original golden vs wrapper/Owner, negative/exception and patched SOURCE seam; no IO except temp JSONL. **BLOCKED→NEXT:** P2-7.

### P2-7 | RF-063 CODEX_B | `scripts/diagnostics/check_audit_trail_completeness.py::_iter_rows` @ L30 | CURRENT SOURCE BLOB `30da7a766711b8a242cafe003cc1de2968e61cb3`
**TARGET 404 B+integration:** `scripts/diagnostics/audit_trail_rows_projection.py::_iter_rows`. **ACTUAL SOURCE BODY TO MOVE:**
```python
def _iter_rows(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    out: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s:
                continue
            try:
                obj = json.loads(s)
            except Exception:
                continue
            if isinstance(obj, dict):
                out.append(obj)
    return out
```
**WRAPPER:** original signature + local import of sole Owner, forward args and call-time facade; for `analyze_day_rows` use `facade._extract_decision_action` and `facade._extract_allowed`, for parser use `facade.argparse`, for JSONL use `facade.json.loads`. **TARGETED NORMAL expected:** temp JSONL blank/malformed/list/{'run_id':'r1'} -> only one dict; missing path -> []. Compare original golden vs wrapper/Owner, negative/exception and patched SOURCE seam; no IO except temp JSONL. **BLOCKED→NEXT:** P2-8.

### P2-8 | RF-063 CODEX_B | `scripts/diagnostics/check_audit_trail_completeness.py::analyze_day_rows` @ L63 | CURRENT SOURCE BLOB `30da7a766711b8a242cafe003cc1de2968e61cb3`
**TARGET 404 B+integration:** `scripts/diagnostics/audit_trail_analysis_projection.py::analyze_day_rows`. **ACTUAL SOURCE BODY TO MOVE:**
```python
def analyze_day_rows(day_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_run: Dict[str, List[Dict[str, Any]]] = {}
    stage_event_total: Dict[str, int] = {
        "start": 0,
        "verdict": 0,
        "execution": 0,
        "degrade_policy_block": 0,
        "end": 0,
        "error": 0,
    }

    for row in day_rows:
        run_id = str(row.get("run_id") or "").strip()
        if run_id:
            by_run.setdefault(run_id, []).append(row)

        stage = str(row.get("stage") or "")
        event = str(row.get("event") or "")
        if stage == "execute_from_packet" and event in stage_event_total:
            stage_event_total[event] = int(stage_event_total.get(event) or 0) + 1

    actionable_run_total = 0
    execution_run_total = 0
    linked_complete_run_total = 0

    missing_start: List[str] = []
    missing_resolution: List[str] = []
    missing_execution_payload: List[str] = []
    missing_terminal: List[str] = []
    orphan_execution: List[str] = []

    for run_id, rows in by_run.items():
        has_actionable = False
        has_exec_activity = False
        has_start = False
        has_verdict = False
        has_degrade_block = False
        has_execution = False
        has_end = False
        has_error = False
        has_allowed_true = False

        for row in rows:
            stage = str(row.get("stage") or "")
            event = str(row.get("event") or "")

            if stage == "decision" and event == "trace":
                action = _extract_decision_action(row)
                if action in ("BUY", "SELL"):
                    has_actionable = True

            if stage == "execute_from_packet":
                has_exec_activity = True
                if event == "start":
                    has_start = True
                elif event == "verdict":
                    has_verdict = True
                    if _extract_allowed(row) is True:
                        has_allowed_true = True
                elif event == "degrade_policy_block":
                    has_degrade_block = True
                elif event == "execution":
                    has_execution = True
                elif event == "end":
                    has_end = True
                elif event == "error":
                    has_error = True

        if has_exec_activity:
            execution_run_total += 1
        if has_exec_activity and not has_actionable:
            orphan_execution.append(run_id)

        if not has_actionable:
            continue

        actionable_run_total += 1

        has_resolution = has_verdict or has_degrade_block or has_error
        has_terminal = has_end or has_error

        if not has_start:
            missing_start.append(run_id)
        if not has_resolution:
            missing_resolution.append(run_id)
        if has_allowed_true and not has_execution:
            missing_execution_payload.append(run_id)
        if not has_terminal:
            missing_terminal.append(run_id)

        if has_start and has_resolution and (not has_allowed_true or has_execution) and has_terminal:
            linked_complete_run_total += 1

    link_success_rate = (
        float(linked_complete_run_total) / float(actionable_run_total)
        if actionable_run_total > 0
        else 1.0
    )

    return {
        "run_total": int(len(by_run)),
        "actionable_decision_run_total": int(actionable_run_total),
        "execution_run_total": int(execution_run_total),
        "linked_complete_run_total": int(linked_complete_run_total),
        "link_success_rate": float(link_success_rate),
        "missing_execution_start_total": int(len(missing_start)),
        "missing_execution_resolution_total": int(len(missing_resolution)),
        "missing_execution_payload_total": int(len(missing_execution_payload)),
        "missing_terminal_event_total": int(len(missing_terminal)),
        "orphan_execution_run_total": int(len(orphan_execution)),
        "stage_event_total": stage_event_total,
        "anomaly_examples": {
            "missing_execution_start": missing_start[:10],
            "missing_execution_resolution": missing_resolution[:10],
            "missing_execution_payload": missing_execution_payload[:10],
            "missing_terminal_event": missing_terminal[:10],
            "orphan_execution": orphan_execution[:10],
        },
    }
```
**WRAPPER:** original signature + local import of sole Owner, forward args and call-time facade; for `analyze_day_rows` use `facade._extract_decision_action` and `facade._extract_allowed`, for parser use `facade.argparse`, for JSONL use `facade.json.loads`. **TARGETED NORMAL expected:** empty -> run_total=0, link_success_rate=1.0; one fake decision BUY + start/verdict allowed/exec/end -> actionable=1 linked_complete=1; omit end -> missing_terminal=1. Compare original golden vs wrapper/Owner, negative/exception and patched SOURCE seam; no IO except temp JSONL. **BLOCKED→NEXT:** P2-report.

## DELIVERY / SUPPLY STATUS
Push B code/tests normally (no force), re-fetch remote B HEAD and SOURCE/TARGET/test blobs; report all P1/P2 items individually with actual test commands/exits, measured START/END, G1/G2/G3 first unmet to #12. C04 alone integrates; C05 alone writes RF/STATUS/DONE. **NEW_READY=8 verified**; **FUTURE RESERVE_VERIFIED=0/6, RESERVE_NOT_VERIFIED** because former six reserves promoted; never claim six future. Old B13 seven are REMOTE_DONE, new tests NOT_RUN at issuance. RunLab Exited(255), RUN_SOURCE_SHA UNKNOWN; no real trading, Broker/Guard/Step5C/UEF/RunLab operational effects.
