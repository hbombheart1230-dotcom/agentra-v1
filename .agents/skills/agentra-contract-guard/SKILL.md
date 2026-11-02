---
name: agentra-contract-guard
description: Check Agentra P1.5 RF owner boundaries, compatibility, safety, and protected resources before proposing or accepting changes.
---
# Agentra Contract Guard (pilot)

## Source of authority
This skill is an aid, NOT a replacement for `docs/refactor/work_orders/D00_ENGINEERING_DELIVERY_POLICY.md`, the live C03 work orders, or the assigned actor's single C01/C02 entrypoint. Only the lead C03-C05 decides owner changes and acceptance. Never edit D00 via this skill.

## Preflight checks (on assigned paths only)
- Confirm exact canonical `integration/p1.5` and actor HEAD, file/blob SHA, SOURCE::FUNCTION and TARGET::FUNCTION, and exclusive ownership; detect cross-actor collision and stale instructions.
- Check that a real BODY MOVE removes original calculation from SOURCE, uses a single Owner and thin wrapper, preserves signature, helper monkeypatches, exception, order, formatting and runtime import semantics.
- No accidental removal of required DTO/IO fields, semantic changes to existing fields, unversioned breaking contracts, or control-flow changes from observational logging.
- Protect real execution: Monitor must not place orders; approvals do not bypass Guards; disabled execution stays blocked; repeated intent_id must not execute twice. No live credentials, effects, actual brokerage activity or runtime state/database/network access in fake tests.
- Never weaken frozen oracle, real-mode interlocks, CI security, or protected D00 contract for easier test results.

## Outcomes
Return only `SAFE_WITH_EVIDENCE`, `KEEP_VERIFIED`, or `BLOCKED_POLICY` with exact path/function/blob and first failing rule. A blocked item must not prevent completing unrelated authorized safe items. Escalate owner/policy conflicts to C03; do not auto-fix or auto-approve a contract change.

## Tool discipline
For unclear third-party library behaviors, Context7 may provide documentation, but version/installed runtime must still be checked. Superpowers debugging can aid diagnosis but cannot override owner boundaries.
