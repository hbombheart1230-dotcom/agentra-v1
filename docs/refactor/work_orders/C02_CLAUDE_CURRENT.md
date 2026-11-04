# C02 — Claude A | RF-032 ACTIVE / A64 READY

## Authority
Canonical integration/p1.5; A branch work/p15-a-reporter-pure-20261021; report #11. Read latest D00, C03_LEAD_TRIAGE_CURRENT.md, docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md §2–3, and docs/refactor/plan/queue/03_PEER_REVIEW/CLAUDE_A/RF-032.md C1/135-owner checklist. ACTIVE_RF=RF-032. Preserve Owner, frozen, UEF, Guard, Writer, Step5C and no-live-operation boundaries.

## Current order
ORDER_ID: A64-RF032-FORWARD-ADAPTER-20261104
ITEM: 1
FIRST_UNMET: RF-032 C1/G1 PARTIAL — forward measurement adapter's Owner/import/consumer/effect classification.
RF_DETAIL: docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md §2 entry libs/reporting/evaluation/canonical/adapters/forward_measurement_adapter.py (KEEP candidate) and §3(1) KEEP / §3(2) verified MOVE. Original RF-032 C1/135-owner checklist.
SOURCE_PATH=TARGET_PATH=libs/reporting/evaluation/canonical/adapters/forward_measurement_adapter.py
SOURCE_BLOB=TARGET_BLOB_BEFORE=67b6e4ea51b43b7dc548e233035069bc127e69cd (canonical and A identical).
TARGET_BLOB_AFTER=UNCHANGED for read-only classification.
ALLOWED: read-only source, actual dependencies, consumers and existing tests; no modifications or repeated pytest.
ACTION: Inspect actual def/class boundaries, imports, consumers, IO/effects, frozen engine delegation and monkeypatch seams. Return KEEP_VERIFIED|PATH|BLOB|specific Owner/consumer/effect evidence or TARGET_GAP|PATH|BLOB|real function/line span|existing Owner candidate|test needed for separate C03 order. If blocked give exact rule and resolution owner. No KEEP solely from module docstring.
TEST: unchanged read-only KEEP classification needs no new tests (§3(1)); code change requires separate authorized order and one normal targeted test.
COMPLETION: report #11 with exact blob, A remote SHA, measured time and verdict; no push for unchanged source. A63 already completed and must not be repeated. Continue RF-032 next item.

## Execution
C04 owns G3 and C05 whole RF DONE. Work order holds current instruction only.
