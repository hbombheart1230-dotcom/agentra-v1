# C02 — Claude A | RF-032 ACTIVE / A60 READY

## Authority
Canonical integration/p1.5; A branch work/p15-a-reporter-pure-20261021; report #11. Follow latest D00, C03, RF_DETAIL docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md §2–3 and original docs/refactor/plan/queue/03_PEER_REVIEW/CLAUDE_A/RF-032.md C1/135-owner checklist. Preserve Owner, frozen oracle, Guard, Writer/UEF/Step5C and real-trading safety. Keep ACTIVE_RF=RF-032; do not switch RF. Skills grant no extra authority.

## Current order
ORDER_ID: A60-RF032-OWNER-KEEP-20261104
ITEM: 1 — libs/reporting/evaluation/attribution_score_window.py
FIRST_UNMET: RF-032 G1/C1 PARTIAL — unclassified owner/import/consumer/effect boundary.
RF_DETAIL: RF-032_IMPLEMENTATION.md §2 (attribution_score_window.py KEEP candidate), §3(1) KEEP_OK and original RF-032 C1 owner checklist.
SOURCE_PATH=TARGET_PATH=libs/reporting/evaluation/attribution_score_window.py
SOURCE_BLOB=TARGET_BLOB_BEFORE=7eccdfd79bca57b61f70d1bcf839729d6cbe4bdc (canonical and A remote identical, verified by C03).
TARGET_BLOB_AFTER=UNCHANGED for KEEP_VERIFIED; no code edits authorized.
ALLOWED: read-only source, existing attribution_score_window_* owner modules, existing imports/consumers and tests. No source/target/test writes, no new extraction or repeat pytest.
ACTION: Inspect real imported Owner modules, public facade delegates and call-time patch seams, consumers, JSON/filesystem reads versus writes, and any remaining inline effect logic. Verify whether source is a justified KEEP and whether delegated owners are importable without circular dependency. Report KEEP_VERIFIED|PATH|EXACT_BLOB|Owner/consumer evidence|effect boundary or BLOCKED|PATH|EXACT_BLOB|exact missing contract|resolution owner. Existing A33–A38 delegations are not new BODY MOVE. Do not claim whole G1/G2/G3 or RF DONE.
TEST: unchanged KEEP classification requires no new normal test per RF_DETAIL §3(1); concrete new defect requires exact evidence and separate C03 scope.
COMPLETION: #11 ITEM 1 verdict, exact A remote SHA/blob, real START/END, no-code/no-test declaration. No push if unchanged. Do not repeat A59/A58/A57. Continue next RF-032 §2 C1 unclassified path after C03 assignment.

## Execution
C04 owns G3/integration; C05 owns RF DONE. Report #11. Never edit this work order or protected code. Retain current instructions only.
