# C02 — Claude A | RF-032 ACTIVE / A63 READY

## Authority
Canonical integration/p1.5; A branch work/p15-a-reporter-pure-20261021; report #11. Follow latest D00, C03, RF_DETAIL docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md §2–3 and original docs/refactor/plan/queue/03_PEER_REVIEW/CLAUDE_A/RF-032.md C1/135-owner checklist. ACTIVE_RF=RF-032; do not switch RF. D00 Owner/frozen/Guard/Writer/UEF/Step5C and live-trading protections remain binding. Skills do not expand authority.

## Current order
ORDER_ID: A63-RF032-ADAPTER-BOUNDARY-20261104
ITEM: 1 — libs/reporting/evaluation/canonical/adapters/already_net_shadow_adapter.py
FIRST_UNMET: RF-032 G1/C1 PARTIAL — large adapter's real function/effect/consumer boundaries not yet classified.
RF_DETAIL: docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md §2 entry already_net_shadow_adapter.py ("긴 파일: 함수 분리 필요성 1회 판단, 실제 이름 확보 전 무작위 MOVE 금지") and §3(1) KEEP or §3(2) verified MOVE; original RF-032 C1/135-owner checklist.
SOURCE_PATH=TARGET_PATH=libs/reporting/evaluation/canonical/adapters/already_net_shadow_adapter.py
SOURCE_BLOB=TARGET_BLOB_BEFORE=be23986b0fb9b111e290357a81b356c521c1d4cf (canonical and A identical).
TARGET_BLOB_AFTER=UNCHANGED for read-only classification. No source/target/test edits authorized by this order.
ALLOWED: read-only source and actual imported dependencies, consumers, existing tests; no protected UEF internals modification, new module, or repeat pytest.
ACTION: Inspect actual def/class boundaries, call-time imports and consumers, effects and patch seams; decide whether the existing 26,125-byte module has justified single responsibility. Report KEEP_VERIFIED|PATH|EXACT_BLOB|specific reason and import/consumer/effect evidence, or TARGET_GAP|PATH|EXACT_BLOB|actual function name and source span|candidate existing Owner|effect boundary|required scoped test and C03 authorization, or BLOCKED with exact safety rule and resolution owner. Do not mark KEEP solely from module name or size; do not invent a MOVE or alter frozen tests.
TEST: no new test for unchanged read-only classification per RF_DETAIL §3(1); any identified extraction requires a separate scoped C03 code order and normal targeted test.
COMPLETION: #11 ITEM1 verdict, A remote SHA/blob, measured START/END, no-code/no-test statement; no push if unchanged. Do not repeat A62 or earlier verified items. Continue RF-032 on next C03 assignment.

## Execution
C04 owns G3/integration and C05 owns RF DONE. Do not edit work orders or protected code. Current instructions only.
