# C02 — Claude A | RF-032 ACTIVE / A61 READY

## Authority
Canonical integration/p1.5; A branch work/p15-a-reporter-pure-20261021; report #11. Follow latest D00, C03, RF_DETAIL docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md §2–3 and original docs/refactor/plan/queue/03_PEER_REVIEW/CLAUDE_A/RF-032.md C1/135-owner checklist. ACTIVE_RF=RF-032; no RF switch. Preserve Owner, frozen oracle, Guard, Writer/UEF/Step5C, real-trading safety. Skills do not grant permissions.

## Current order
ORDER_ID: A61-RF032-OWNER-KEEP-20261104
ITEM: 1 — libs/reporting/evaluation/canonical/__init__.py
FIRST_UNMET: RF-032 G1/C1 PARTIAL — unclassified canonical package facade import/consumer/effect boundary.
RF_DETAIL: docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md §2 canonical/__init__.py KEEP candidate; §3(1) KEEP_OK; original RF-032 C1 owner checklist.
SOURCE_PATH=TARGET_PATH=libs/reporting/evaluation/canonical/__init__.py
SOURCE_BLOB=TARGET_BLOB_BEFORE=23a6c6e06d09b573820ff25c1d63d122c37f49e8 (canonical and A identical).
TARGET_BLOB_AFTER=UNCHANGED if KEEP_VERIFIED; no edits authorized.
ALLOWED: read-only canonical/__init__.py, its imported canonical Owner modules, existing consumers and tests. No source/target/test writes, new extraction or repeated pytest.
ACTION: Inspect actual imported Owner modules and public exports, consumers, import cycle and package initialization effects; verify whether facade is justified KEEP and imported symbols are present. Record KEEP_VERIFIED|PATH|EXACT_BLOB|Owner/import/consumer/effect evidence|reason or BLOCKED|PATH|EXACT_BLOB|exact missing contract|resolution owner. Do not infer safety from the module docstring alone. No whole G1/G2/G3 or RF DONE claim.
TEST: unchanged KEEP classification needs no new normal test per RF_DETAIL §3(1); a concrete defect requires evidence and separate C03 scoped order.
COMPLETION: report #11 ITEM1 verdict, exact A remote SHA/blob, measured START/END, no-code/no-test declaration; no push if unchanged. Do not repeat A60/A59/A58. Continue same RF-032 §2 unclassified paths after next C03 assignment.

## Execution
C04 owns G3/integration, C05 owns RF DONE. Never edit work order or protected code. Keep current instructions only.
