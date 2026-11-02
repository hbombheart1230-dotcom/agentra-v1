# C02 — Claude A | ORDER_ID=A-20261102-14-C03 | RF-032 03_PEER_REVIEW | A38 NEW_READY=8/8 | A37 REMOTE_DONE=8 | RESERVE_VERIFIED=6/6

## START — A37 completed; next A38 only
Read ONLY this C02. Canonical pre-order `integration/p1.5@650ba629cabc723bdc1e60389eb61888a4ac2b72`; A remote `work/p15-a-reporter-pure-20261021@afd8becdc6af23e10cfd0abc3bf92efa01727791`. #11 comment 6569003972 reports A37-1..8 REMOTE_DONE, normal 71 PASS EXIT=0; C04 #36 6569121647 integrated 11/11 exact SOURCE/Owner/test blobs at `650ba629`; C05 #36 6569259986 accepted selected G3_REUSE only. **Do not reissue A33–A37 or change already-started work retroactively.** All eight below are new and each TARGET was 404 on both refs before issuance. Source blobs below match canonical=A exact; recheck at actual execution HEAD.

**DONE-first selection:** RF-030 PENDING/A closeout is C04-owned exact canonical fake smoke, and changing its pinned SOURCE invalidates proof; RF-063 DEV/B requires B-04 facade/seven Owner resolver closure; RF-032 PEER/A still has independently verifiable pure/report calculations but **whole G1 BLOCKED_POLICY** validation-id path containment/Writer/UEF. A38 improves only selected scope; it cannot authorize safety clearance or RF DONE. RF-031 and RF-050 are already DONE; RF-035/044 are DONE and not resupplied. If current RF-032 safety owner denies even read-only Owner extraction, record item-specific SAFETY_BLOCKED and continue other safe items.

**Safety and method:** A branch SOURCE/Owner/targeted test code only. No D00/C/RF/STATUS, B files, C04/C05, CI/workflows/schedules, validation-id writer, UEF5/historical_recompute, Broker/Guard/Step5C/RunLab, real orders, operational State/DB, network/subprocess, actual filesystem read/write. Source module remains original public API and exact same-signature wrapper; move actual calculation into sole TARGET, no duplicate body, Owner must NOT import SOURCE. Delegate with `facade=sys.modules[__name__]` at CALL TIME to preserve monkeypatch seams, constants, helper functions, Mapping/Counter/enum/Path behavior, identity/copy semantics, key order and exception class/message. For generator functions preserve laziness; none of these eight may trigger real I/O in tests. For read-only JSON helpers fake `Path.read_text`, for ledger fake `Path.glob`, no real disk access. Existing tests/frozen oracles untouched. If drift/target exists/unsafe effect, individually report exact FIRST_BLOCKER and continue other assigned items. One PASS or short runtime is not a stop condition.

## A38 — eight mandatory actual SOURCE::function → sole TARGET Owner
All SOURCE bodies below independently inspected on both refs, substantive original computations (not already thin Owner wrappers). All eight TARGET and `tests/test_p15_rf032_20261102_14h_evaluation_pure_followup_owners.py` were independently 404 on both refs. New targeted test must capture pinned original AST before edits and compare Owner+wrapper outputs, ordered/nested identity, exceptions and call-time patched facade in distinct fake-only cases for **each of eight**. Required normal `python -m pytest -q tests/test_p15_rf032_20261102_14h_evaluation_pure_followup_owners.py` EXIT=0 on final delivered BLOB. Never count a KEEP or preexisting target as a new MOVE.

### A38-1 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/counterfactuals.py::build_selection_attribution` SOURCE_BLOB=`8429cf73588fda3cbf200aaa5c207e30a4868ba3`; TARGET=`libs/reporting/evaluation/counterfactuals_build_selection_attribution.py::build_selection_attribution` TARGET=404 canonical+A.
BODY=derive selection/raw_scanner_top1/scanner_top1 symbol comparison, availability, scanner/strategist/commander structured evidence, immutable limitations and exact nested schema/ordered keys; preserve precedence of `raw_top1.get("rank") or 1 if top1_symbol else None` and `EvidenceClass.UNAVAILABLE.value` via facade. FAKE_CASES=missing selection, non-dict top1, same/different symbols, rank 0/None, patched EvidenceClass, nested key order/identity, exceptions. No external effects.

### A38-2 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/daily_scorecard.py::build_daily_scorecard` SOURCE_BLOB=`9c09b97144ce17aeb71e56312265a11075913a1a`; TARGET=`libs/reporting/evaluation/daily_scorecard_build_daily_scorecard.py::build_daily_scorecard` TARGET=404 canonical+A.
BODY=eligible returns, Counter integrity/horizon buckets, early exit cost, strategist deltas, READY/return-based DecisionClass, performance_metrics and contract_metadata, stable nested `daily_scorecard.v1` output; all Counter, enum, performance_metrics, contract_metadata references via facade at call time. Preserve keyword-only signature/default None, shallow `start_gate` identity and all numeric/exception semantics. FAKE_CASES=empty/mixed trades, missing horizon, READY/non-READY, positive/negative/zero returns, invalid numeric, q8 gate, patched metrics/contract, exact ordered/nested payload.

### A38-3 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/artifact_inventory.py::read_json` SOURCE_BLOB=`8cf0a23641d9cf3c133a98135f5283f4d40c2e64`; TARGET=`libs/reporting/evaluation/artifact_inventory_read_json.py::read_json` TARGET=404 canonical+A.
BODY=read UTF-8 text via facade `json.loads(path.read_text(encoding="utf-8"))`, return dict only else {}, catch Exception→{}. FAKE_CASES=valid dict, list/scalar, invalid JSON, read_text raises, encoding parameter and exact exception suppression. Patch fake path object; never actual disk.

### A38-4 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/attribution_score_v0.py::_ledger_day_record` SOURCE_BLOB=`27fa361dc1da696a0dae801d1dabb75446856b74`; TARGET=`libs/reporting/evaluation/attribution_score_v0_ledger_day_record.py::_ledger_day_record` TARGET=404 canonical+A.
BODY=compose freeze_window root, sorted `*/daily_ledger.json` fake glob, facade `_read_json`, first matching day row shallow dict copy, fallback {}; preserve path string sort and first match. FAKE_CASES=missing/no match, two files out of order, duplicate days, non-dict rows, shallow nested identity, patched _read_json, fake Path glob. No real FS.

### A38-5 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/attribution_score_v0.py::_read_json` SOURCE_BLOB=`27fa361dc1da696a0dae801d1dabb75446856b74`; TARGET=`libs/reporting/evaluation/attribution_score_v0_read_json.py::_read_json` TARGET=404 canonical+A.
BODY=UTF-8 `json.loads` and Mapping-to-dict-only fallback {}, broad Exception catch. FAKE_CASES=dict/list/scalar/invalid/raised read_text, patched json, encoding and identity. Fake read only.

### A38-6 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/attribution_score_window.py::_read_json` SOURCE_BLOB=`fce6c31ec4461454e857573c0c2b0a60f2086ce7`; TARGET=`libs/reporting/evaluation/attribution_score_window_read_json.py::_read_json` TARGET=404 canonical+A.
BODY=UTF-8 `json.loads`, return dict else {}, broad Exception catch. FAKE_CASES=valid dict/non-dict/invalid/raised read_text, patch json and fake Path, identity, no actual FS.

### A38-7 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/horizon_alignment.py::_group_key` SOURCE_BLOB=`c41a0b655071a7e14b43305ddd9c26b1114bf685`; TARGET=`libs/reporting/evaluation/horizon_alignment_group_key.py::_group_key` TARGET=404 canonical+A.
BODY=facade `_lane_observation(row)`, compute five fixed dimensions `time_bucket,tactic,primary_lane,market_regime_rail,selection_role` via facade `_text`, return ordered tuple by requested dimensions. FAKE_CASES=empty/nonempty lane, permutation/subset, invalid dimension KeyError, patched helper call sequence and exact exception, no IO.

### A38-8 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/horizon_alignment.py::_profit_factor` SOURCE_BLOB=`c41a0b655071a7e14b43305ddd9c26b1114bf685`; TARGET=`libs/reporting/evaluation/horizon_alignment_profit_factor.py::_profit_factor` TARGET=404 canonical+A.
BODY=sum positive gains and negated losses; no losses returns 999.0 if gains>0 else 0.0; otherwise round(gains/losses,4). FAKE_CASES=empty, all gains/losses, mixed, zeros, negative zero, rounding tie, invalid input/NaN and exception parity. No IO.

## Six independently verified unassigned reserves — 6/6, NOT A38
All six actual original bodies were inspected at identical canonical+A SOURCE `libs/reporting/evaluation/entry_timing_attribution.py@a7559c358b7ff8e6048586ba1d42a97480ad3c79`, RF-032 Claude A-owned; sole TARGET 404 canonical+A individually. Future issuance must recheck source/target and preserve facade helper patches; fake-only tests, no network/FS/real effects:
1. `_epoch` → `libs/reporting/evaluation/entry_timing_attribution_epoch.py::_epoch`: numeric/ISO timestamp conversion with fallback 0, `datetime.fromisoformat` fake edge, float/string/invalid and exception parity.
2. `_iso` → `libs/reporting/evaluation/entry_timing_attribution_iso.py::_iso`: UTC ISO formatting, epoch<=0 blank, patched datetime/timezone seam and overflow parity.
3. `_stage_epoch` → `libs/reporting/evaluation/entry_timing_attribution_stage_epoch.py::_stage_epoch`: first positive facade._epoch among keys, order/zero fallback, patched helper.
4. `_candidate_symbol` → `libs/reporting/evaluation/entry_timing_attribution_candidate_symbol.py::_candidate_symbol`: Mapping symbol strip or empty, nested identity and Mapping seam.
5. `_candidate_rank` → `libs/reporting/evaluation/entry_timing_attribution_candidate_rank.py::_candidate_rank`: facade._num rank to int/None, bool/NaN/error parity.
6. `_row_at_or_before` → `libs/reporting/evaluation/entry_timing_attribution_row_at_or_before.py::_row_at_or_before`: last row with int(ts)<=epoch, preserve row identity, invalid timestamp exception, stable order.
Reserves are NOT assigned, NEW_READY or RF DONE. A38 completion will require fresh reserve refill next C03.

## CLOSEOUT_FIRST — C04/C05 exclusive
1. RF-030 PENDING/A G3 FIRST_UNMET: exact integrated `operator_visibility.py@bb6e97a72f94412ff9ca818dbf2a03d788dddf48` + `operator_visibility_build_run_contexts.py@db45fb0e06aee58c5d7938ad7f59801c11fb6191` + `tests/test_p15_rf030_20261102_02h_run_contexts.py@3b7c48e9b98f699f8f3def7314ef8bb2e8a07330`; C04 normal fake-only exit0 on exact canonical dependencies or equivalent proof. C05 also reconcile stale RF030 physical checklist G1 PARTIAL/G2 PENDING before DONE.
2. RF-063 DEV/B G3 BLOCKED: B-04 trade facade/seven B-only Owner closure and canonical `llm_artifacts.py` resolver; C04 narrow fake import/resolver test. No blind merge.
3. RF-032 PEER/A G1 BLOCKED_POLICY: validation-id path traversal containment/Writer/UEF safety-owner approval required; A38 pure work does not clear.
4. RF-026 PENDING/B G1 BLOCKED_POLICY cold-import `exit_policy→monitor_exit.__init__→policy_map_builder→exit_policy`; B34 and B33 report clarification cannot clear.

**#11 REPORT:** `ORDER_ID | ACTUAL_C02_BLOB | canonical SHA | A_HEAD_BEFORE→AFTER | A38-1..8 individually DONE/BLOCKED with exact FIRST_BLOCKER | SOURCE before/after blobs | 8 Owner blobs | targeted test blob | NORMAL EXIT=n PASS=n | NEW_BODY_MOVE_ACTUAL | final remote SHA/tree/full-root + exact blob refetch | measured START_KST/END_KST/ELAPSED_MIN | RESERVE_VERIFIED=6/6 unassigned | NEXT=C03_ASSIGNED_ONLY`. If push auth fails, approved non-force expected-parent exact-tree fallback only; otherwise PUSH_BLOCKED. Do not claim actor PASS from unrun tests, no force push.
