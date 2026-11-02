# C02 — Claude A | ORDER_ID=A-20261103-05-C03 | RF-032 PEER | A52 NEW_READY=8/8 | A51 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START — single remote entrypoint, preserve in-progress starting orders
Canonical PREWRITE=78b1da2e54fd1bc771bf2d5315c780c5edf98f86; A actor remote HEAD=373af1457fb8ebe11ef3ba61105d66592143ae65; previous C02 blob=ad10de597be1734a097a85bf37eef65c17fcbb9b. A51 #11 6586172610: eight real moves at A 373af145, targeted normal 215 PASS EXIT0, 10/10 staged and final blobs. C04 #36 6586601257 integrated A51 exact 10/10 at canonical 78b1da2e; C05 #36 6586889248 scoped G1/G2/G3_REUSE but RF-032 whole BLOCKED_POLICY. **Never redo/recount A51 or earlier.** If A51 genuinely began before new order became visible, finish all its safe items first; do not retroactively cancel.

First shell `python -m pytest --version`; if missing `python -m pip install --user pytest`, recheck. Fetch this C02 **directly from remote integration/p1.5** at start, record exact canonical HEAD/C02 Git blob/ORDER_ID and A HEAD in #11. This file alone is execution entrypoint; no D00/RF/INDEX/skill reread. At start re-fetch SOURCE and all TARGETs on A branch; SOURCE drift, pre-existing TARGET or ownership conflict = item-specific VERIFIED_ALREADY/BLOCKED with exact SHA; continue remaining independent safe items. A edits code/tests only on A branch.

## DONE-first gate separation / safety
C05 physical 93 unique: PENDING38/DEV7/PEER2/DONE46; unresolved47, NEW_RF_DONE=0. RF-030 PENDING G1 PARTIAL (15/16 KEEP, RF-074 frozen owner boundary), G2/G3 canonical fake-only smoke unverified; C03/C04/C05 adjudicate, **not A52**. RF-063 B40 syntax repair and resolver dependency closure belong B/C04. RF-032 whole validation-id/Writer/UEF remains G1 BLOCKED_POLICY; A52 is **only pure evaluation body migration**, cannot authorize real mode or claim RF DONE. C03 inspected other closeout candidates but no verified eight-item independent safe A BODY MOVE set there. This is a supply obligation within an unresolved A-owned RF, not a claim of whole-RF closeout; next priority remains G1/G2/G3 closeout rather than endless RF-032 targets.

## A52 — 8 distinct real SOURCE BODY MOVEs (not KEEP, not done before)
All eight SOURCE functions are in `libs/reporting/evaluation/full_chain_component_review.py` Git blob `dc1e6c5017e537057864be84b659f0803efa0a8c`, identical on canonical and A at issuance. RF-032 FILE_COVERAGE explicitly owns this SOURCE; A exclusive, B read-only. Each exact TARGET file below was independently fetched and returned 404 on **both** canonical and A. All are in-memory calculation/aggregation, no file/DB/network/trade/State writes; `_q9_decision_candidate_rows` calls `attach_forward_outcomes` through the original facade and is tested with fake patched helper only. Transfer **entire real body** into one new TARGET Owner function of same name; retain original SOURCE signature/defaults/docstring as thin import+delegate wrapper, no duplicate calculation. Use `facade=sys.modules[__name__]` at call-time; Owner must not import SOURCE. Resolve mutable SOURCE globals through facade at use-time (Mapping, defaultdict, DecisionClass, HORIZONS, constants, _number, _topk_metric, _checkpoint_return, candidate_day, performance_metrics, attach_forward_outcomes and other helpers as applicable). Preserve monkeypatch, imports, identity, order, exceptions, dict keys, float rounding and output bytes. **No touching build/write public IO functions, contracts, frozen oracle, Guard, Step5C, UEF, real effects or operations.** Do not trigger file loaders in tests.

One **new** fake-only targeted test `tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py` (404 canonical+A at issuance): compare each pinned original SOURCE AST body against final thin wrapper+Owner, including call-time monkeypatch seams; exact output, exceptions, order, identity, one-shot generator behavior. Run **normal** `python -m pytest -q tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py` once after changes, EXIT=0 on exact final A tree. No mandatory -O/full suite/hosted CI/peer.

### A52-1 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_number` | SOURCE_GIT_BLOB=`dc1e6c5017e537057864be84b659f0803efa0a8c`
TARGET=`libs/reporting/evaluation/full_chain_component_review_number.py::_number` | TARGET=404 canonical+A, A-exclusive
ACTUAL_BODY=float-or-None, preserve `value in (None, '')` membership, only TypeError/ValueError catches
MOVE=transfer full original computation to one Owner; same-signature thin SOURCE facade with use-time helper resolution; no IO/effect change.
TARGETED_NORMAL_CASES=None/empty/0/numeric string, custom comparison/float exceptions, identity/exception parity; original pinned AST vs wrapper+Owner fake parity.
TEST=`tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py`. If blocked record exact SOURCE/TARGET/SHA/FIRST_BLOCKER and continue remaining A52 items.

### A52-2 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_behavior_metric_eligible` | SOURCE_GIT_BLOB=`dc1e6c5017e537057864be84b659f0803efa0a8c`
TARGET=`libs/reporting/evaluation/full_chain_component_review_behavior_metric_eligible.py::_behavior_metric_eligible` | TARGET=404 canonical+A, A-exclusive
ACTUAL_BODY=integrity Mapping check, defect string set and BEHAVIOR_METRIC_EXCLUSION_DEFECTS intersection
MOVE=transfer full original computation to one Owner; same-signature thin SOURCE facade with use-time helper resolution; no IO/effect change.
TARGETED_NORMAL_CASES=missing/nonmapping integrity, duplicate defects, patched exclusion set at call-time; original pinned AST vs wrapper+Owner fake parity.
TEST=`tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py`. If blocked record exact SOURCE/TARGET/SHA/FIRST_BLOCKER and continue remaining A52 items.

### A52-3 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_topk_metric` | SOURCE_GIT_BLOB=`dc1e6c5017e537057864be84b659f0803efa0a8c`
TARGET=`libs/reporting/evaluation/full_chain_component_review_topk_metric.py::_topk_metric` | TARGET=404 canonical+A, A-exclusive
ACTUAL_BODY=first matching topk_forward_performance row copied to dict; int(top_k), horizon and iterator order
MOVE=transfer full original computation to one Owner; same-signature thin SOURCE facade with use-time helper resolution; no IO/effect change.
TARGETED_NORMAL_CASES=multiple rows, missing fields, malformed int, generator order and first match; original pinned AST vs wrapper+Owner fake parity.
TEST=`tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py`. If blocked record exact SOURCE/TARGET/SHA/FIRST_BLOCKER and continue remaining A52 items.

### A52-4 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_classify_root_cause` | SOURCE_GIT_BLOB=`dc1e6c5017e537057864be84b659f0803efa0a8c`
TARGET=`libs/reporting/evaluation/full_chain_component_review_classify_root_cause.py::_classify_root_cause` | TARGET=404 canonical+A, A-exclusive
ACTUAL_BODY=scanner/strategist/commander/monitor-entry/monitor-exit thresholds, ordered statuses and primary cause, exact evidence mapping
MOVE=transfer full original computation to one Owner; same-signature thin SOURCE facade with use-time helper resolution; no IO/effect change.
TARGETED_NORMAL_CASES=zero/missing samples, threshold boundaries, monkeypatched _topk_metric/_number, key order; original pinned AST vs wrapper+Owner fake parity.
TEST=`tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py`. If blocked record exact SOURCE/TARGET/SHA/FIRST_BLOCKER and continue remaining A52 items.

### A52-5 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_role_metrics` | SOURCE_GIT_BLOB=`dc1e6c5017e537057864be84b659f0803efa0a8c`
TARGET=`libs/reporting/evaluation/full_chain_component_review_role_metrics.py::_role_metrics` | TARGET=404 canonical+A, A-exclusive
ACTUAL_BODY=role/horizon filtering, checkpoint return minus cost, candidate_day set, performance_metrics merge
MOVE=transfer full original computation to one Owner; same-signature thin SOURCE facade with use-time helper resolution; no IO/effect change.
TARGETED_NORMAL_CASES=empty/zero/negative return, duplicate days, cost precision, patched helpers; original pinned AST vs wrapper+Owner fake parity.
TEST=`tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py`. If blocked record exact SOURCE/TARGET/SHA/FIRST_BLOCKER and continue remaining A52 items.

### A52-6 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_paired_role_deltas` | SOURCE_GIT_BLOB=`dc1e6c5017e537057864be84b659f0803efa0a8c`
TARGET=`libs/reporting/evaluation/full_chain_component_review_paired_role_deltas.py::_paired_role_deltas` | TARGET=404 canonical+A, A-exclusive
ACTUAL_BODY=group top_pick vs runner_up_evaluated by generated window; per-window averages and positive rate
MOVE=transfer full original computation to one Owner; same-signature thin SOURCE facade with use-time helper resolution; no IO/effect change.
TARGETED_NORMAL_CASES=missing windows, duplicate rows, generator consumption, patched _checkpoint_return/performance_metrics; original pinned AST vs wrapper+Owner fake parity.
TEST=`tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py`. If blocked record exact SOURCE/TARGET/SHA/FIRST_BLOCKER and continue remaining A52 items.

### A52-7 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_selection_availability` | SOURCE_GIT_BLOB=`dc1e6c5017e537057864be84b659f0803efa0a8c`
TARGET=`libs/reporting/evaluation/full_chain_component_review_selection_availability.py::_selection_availability` | TARGET=404 canonical+A, A-exclusive
ACTUAL_BODY=selection raw control/snapshot/comparability counters and sorted missing-field map
MOVE=transfer full original computation to one Owner; same-signature thin SOURCE facade with use-time helper resolution; no IO/effect change.
TARGETED_NORMAL_CASES=nonmapping selection, absent controls, mixed snapshots, output key and sorted order; original pinned AST vs wrapper+Owner fake parity.
TEST=`tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py`. If blocked record exact SOURCE/TARGET/SHA/FIRST_BLOCKER and continue remaining A52 items.

### A52-8 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_q9_decision_candidate_rows` | SOURCE_GIT_BLOB=`dc1e6c5017e537057864be84b659f0803efa0a8c`
TARGET=`libs/reporting/evaluation/full_chain_component_review_q9_decision_candidate_rows.py::_q9_decision_candidate_rows` | TARGET=404 canonical+A, A-exclusive
ACTUAL_BODY=flatten q9_decision_candidates preserving payload order, copy rows, default generated_at, attach_forward_outcomes call-time
MOVE=transfer full original computation to one Owner; same-signature thin SOURCE facade with use-time helper resolution; no IO/effect change.
TARGETED_NORMAL_CASES=nonmapping rows, duplicate generated_at, patched attach_forward_outcomes, no mutation/identity parity; original pinned AST vs wrapper+Owner fake parity.
TEST=`tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py`. If blocked record exact SOURCE/TARGET/SHA/FIRST_BLOCKER and continue remaining A52 items.

## VERIFIED UNASSIGNED RESERVE — A 6/6 (do NOT execute without next C03 order)
Same SOURCE `libs/reporting/evaluation/full_chain_component_review.py@dc1e6c5017e537057864be84b659f0803efa0a8c` inspected on canonical+A. Each reserve function has real unextracted calculation/string-render body; each unique TARGET 404 canonical+A at issuance, no other actor ownership. The render helper builds an in-memory Markdown string only (the separate write function is **excluded**). Future fake-only targeted AST/monkeypatch parity test is proposed, not run. These six are **not** A52 READY or new accomplishments:
1. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_q9_role_row@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_q9_role_row.py::_q9_role_row` (404 canonical+A). BODY=role selection first q9_selected or minimum int(float(rank)); original row identity; pure. IO/State=none, no live effects. FUTURE_FAKE_TEST=empty/malformed rank, tie, selected-first. UNASSIGNED.
2. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_decision_window_attribution@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_decision_window_attribution.py::_decision_window_attribution` (404 canonical+A). BODY=Q9 window/horizon in-memory attribution; helper seams and dict order; pure. IO/State=none, no live effects. FUTURE_FAKE_TEST=mock roles, no-trade, cost, missing checkpoints. UNASSIGNED.
3. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_attribution_component@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_attribution_component.py::_attribution_component` (404 canonical+A). BODY=strategist/commander attribution decision dict; thresholds and no behavior authorization. IO/State=none, no live effects. FUTURE_FAKE_TEST=empty/missing, positive/negative threshold. UNASSIGNED.
4. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_scanner_decision@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_scanner_decision.py::_scanner_decision` (404 canonical+A). BODY=top-pick/runner-up metrics materiality comparison and contract constants. IO/State=none, no live effects. FUTURE_FAKE_TEST=zero/missing metrics, threshold edges. UNASSIGNED.
5. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_unavailable_component@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_unavailable_component.py::_unavailable_component` (404 canonical+A). BODY=static unavailable decision dict and behavior_change_authorized false. IO/State=none, no live effects. FUTURE_FAKE_TEST=question, missing comparison, availability identity. UNASSIGNED.
6. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::render_full_chain_component_review@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_render.py::render_full_chain_component_review` (404 canonical+A). BODY=string-only Markdown rendering, no filesystem write or runtime effects. IO/State=none, no live effects. FUTURE_FAKE_TEST=empty/filled payload, Unicode, exact newline/byte parity. UNASSIGNED.

## C06 preventive integrity — already forwarded; do not reopen A49
#37 comment 6584273468 A49 intermediate missing SOURCE wrappers was corrected before G3. A50/A51 each reported full staged SOURCE+8 Owner+test manifest and exact final blobs. For A52 before non-force push run `git status --short`, `git diff --cached --name-only`; stage SOURCE+8 Owners+test = **10 paths**, re-stage after stash/pop; inspect `git show --name-only --format= HEAD`. Re-fetch all 10 remote paths after push. No reimplementation/retest of A49.

## DELIVERY / ACCEPTANCE / #11
A52-1..8 individually DONE with SOURCE before/after and Owner/test blobs, or BLOCKED with exact SOURCE/TARGET/SHA/FIRST_BLOCKER. One failure must not stop other safe items. Normal targeted command EXIT and observed PASS count separate; actual START_KST/END_KST/ELAPSED_MIN; A HEAD before/after; staged 10-path manifest; non-force remote SHA; refetch full-root tree and 10 blobs. Auth/push failure blocks only remote G1, not independent safe code work. No force/history rewrite. C04 alone integrates and proves G3; C05 alone RF/STATUS/DONE. No document, C01/C03/C04/C05/D00/RF/STATUS/RunLab/Guard/Step5C/UEF/operations writes.
