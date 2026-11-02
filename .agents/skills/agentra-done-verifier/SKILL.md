---
name: agentra-done-verifier
description: Audit Agentra FAST-3 G1/G2/G3 evidence and count only newly closed RFs; never self-authorize DONE.
---
# Agentra DONE Verifier (pilot)

## Role boundaries
- C04 alone (or explicitly authorized integrator) integrates selected changes into `integration/p1.5`.
- C05 alone updates RF physical phase, STATUS and formal DONE.
- C06 audits independently in read-only mode.
- This skill only prepares an evidence checklist; it cannot mark a RF DONE or push to canonical by itself.

## FAST-3 acceptance
- G1 CODE_READY: current remote source/owner SHA and actually changed or valid KEEP scope verified. Local-only work is insufficient.
- G2 TEST_READY: a relevant changed-function/affected-caller normal pytest or reproducible stdlib smoke exited 0, with exact SOURCE SHA; acceptable existing CI evidence only as allowed by D00. Never invent PASS.
- G3 INTEGRATED_DONE: exact source present in canonical `integration/p1.5` (or canonical KEEP) plus relevant integrated-SHA smoke/targeted CI or valid existing passing evidence.
- C05 may count new RF_DONE_DELTA only after G1/G2/G3 met and actual 05_DONE/STATUS update. Distinguish development DONE from RunLab RUNTIME_VERIFIED.

## No double-counting
Keep independent counters: `NEW_BODY_MOVES`, `KEEP_VERIFIED_ONLY`, `LOCAL_ONLY`, `PUSH_VERIFIED`, `INTEGRATED`, `RF_DONE_DELTA`. Do not convert a new test, document commit, old DONE improvement, duplicate retry or reserved future task into fresh DONE.

## Evidence format
`RF_ID | G1 | G2 | G3 | ACTOR_REMOTE_SHA | CANONICAL_SHA | TEST_COMMAND | EXIT_CODE | PHYSICAL_PHASE | STATUS_SYNCED | RF_DONE_DELTA | FIRST_UNMET`.

No new mandatory peer review, all-mode suite, -O tests or hosted CI gates beyond canonical D00 FAST-3. If evidence is missing, report PENDING/PARTIAL/MISSING/BLOCKED, never PASS.
