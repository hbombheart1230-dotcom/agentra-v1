# C02 — Claude A | RF-032 ACTIVE / A62 READY

## Authority
Canonical integration/p1.5; A branch work/p15-a-reporter-pure-20261021; report #11. Follow latest D00, C03, RF_DETAIL docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md §2–3 and original docs/refactor/plan/queue/03_PEER_REVIEW/CLAUDE_A/RF-032.md C1/135-owner checklist. ACTIVE_RF=RF-032; no RF switch. Preserve Owner, frozen oracle, Guard, Writer/UEF/Step5C and real-trading safety. Skills do not grant permissions.

## Current order
ORDER_ID: A62-RF032-OWNER-KEEP-20261104
ITEM: 1 — libs/reporting/evaluation/canonical/adapters/__init__.py
FIRST_UNMET: RF-032 G1/C1 PARTIAL — canonical adapter package initialization, import/consumer/effect boundary not classified.
RF_DETAIL: docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md §2 canonical/adapters/__init__.py KEEP candidate and §3(1) KEEP_OK; original RF-032 C1/135-owner checklist.
SOURCE_PATH=TARGET_PATH=libs/reporting/evaluation/canonical/adapters/__init__.py
SOURCE_BLOB=TARGET_BLOB_BEFORE=8b76b9f33aa42e7c4c1a460cb4985c88960d70e2 (canonical and A identical).
TARGET_BLOB_AFTER=UNCHANGED if KEEP_VERIFIED; no edits authorized.
ALLOWED: read-only source, actual imports/consumers, adapter sibling modules and existing tests. No source/target/test writes, no new extraction, no repeat pytest.
ACTION: Verify the package initialization and __all__ contract, imported adapter consumer dependencies, and whether its docstring's offline/read-only assertions match actual consumer/effect boundaries; distinguish package __init__ effects from sibling modules. Record KEEP_VERIFIED|PATH|EXACT_BLOB|Owner/import/consumer/effect evidence|reason or BLOCKED|PATH|EXACT_BLOB|exact missing contract|resolution owner. Do not assert no runtime consumers from the docstring alone.
TEST: unchanged KEEP classification needs no new normal test per RF_DETAIL §3(1); concrete defect requires evidence and separate C03 scoped order.
COMPLETION: report #11 ITEM1 verdict, exact A remote SHA/blob, measured START/END and no-code/no-test declaration; no push if unchanged. Do not repeat A61 or earlier completed KEEP checks. Continue same RF-032 §2 unclassified paths after next C03 assignment.

## Execution
C04 owns G3/integration, C05 owns RF DONE. Never edit work order or protected code. Keep current instructions only.
