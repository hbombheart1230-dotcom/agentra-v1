# C01 — Codex B | RF-063 ACTIVE / B46 READY (READ-ONLY CONTRACT RECONCILIATION)

## Authority
Canonical integration/p1.5; B branch work/p15-b-operator-structure-20261022; report #12. Read D00, C03_LEAD_TRIAGE_CURRENT.md, docs/refactor/plan/rf_details/RF-063_IMPLEMENTATION.md opening “실물 함수 분석” and §2–3, and docs/refactor/plan/queue/02_DEVELOPING/CODEX_B/RF-063.md C1/76-owner checklist. ACTIVE_RF=RF-063; no RF switch. Preserve Owner, frozen oracle, Guard/Writer/UEF/Step5C and no-live-operation boundaries.

## Current order
ORDER_ID: B46-RF063-VALIDATION-OWNER-RECONCILIATION-20261104
ITEM: 1
FIRST_UNMET: RF-063 C1/G1 PARTIAL — validate_trade_artifact_chain projection Owner/consumer contract and existing B implementation equivalence not yet established.
RF_DETAIL: RF-063_IMPLEMENTATION.md opening “실물 함수 분석” validate_trade_artifact_chain calculation-only evidence projection; §2 check_trade_report_runtime_regression.py; §3 owner/CLI classification; original RF-063 C1/76-owner checklist.
SOURCE_PATH=scripts/diagnostics/check_trade_report_runtime_regression.py
SOURCE_BLOB_CANONICAL=dc882aa56b5a23d9716cc8d3ec009480275cfe4d
SOURCE_BLOB_B=c7113fcf6e7c3313943e484fa939c48062672141
PLANNED_TARGET=scripts/diagnostics/trade_artifact_validation_projection.py; TARGET_BLOB_BEFORE=ABSENT on canonical and B. DO NOT CREATE.
EXISTING_B_OWNER=scripts/diagnostics/trade_artifact_validation_evidence_projection.py; BLOB=9fd7c104efc5b0497bdb7f9b0b6a4642386b3974
DEPENDENCIES_B: trade_artifact_validation_read_projection.py blob c573e644ab9f81377ecba906ad283170807c6ee7; trade_artifact_validation_cli.py blob 1fd6fefbca7d1a04373c626f3f02ae4a4fb2d8f6.
ALLOWED: read-only exact source/Owner/consumer/import and existing test inspection, no source/test changes or repeat pytest.
ACTION: Trace the exact calculation-only body in canonical to B evidence projection, compare return keys, warning/error ordering, effect boundary and public facade/CLI consumer imports. Inventory the seven B-only transitive projection dependencies and whether a minimal non-overwriting selective integration is safe. Report KEEP_EXISTING_OWNER with exact blob and C04 file/test manifest if equivalent, or TARGET_GAP with exact function/line/contract mismatch and a minimal allowed source/target/test proposal for C03. Do not overwrite canonical facade or create duplicate Owner. If blocked provide per-path evidence, rule and resolution owner; continue independent RF-063 C1 candidates.
TEST: NOT_RUN for unchanged read-only inspection; subsequent C03 code order requires one scoped normal targeted pytest. Existing B45 9 PASS and canonical 13 PASS are completed, do not repeat.
COMPLETION: #12 evidence with B remote SHA, exact blobs, actual import/consumer paths, verdict and measured time. C04 owns selective integration/G3, C05 whole RF DONE. No code push for read-only order.

## Execution
On a later exact code order verify source/target blob before edit, one normal scoped test, non-force push and refetch. No edits to this work order by B. Current instructions only.
