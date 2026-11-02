---
name: agentra-rf-executor
description: Execute assigned Agentra P1.5 RF code changes with targeted tests, remote SHA proof, and no premature stop. Use only when the active actor's C01/C02 order explicitly authorizes implementation.
---
# Agentra RF Executor (pilot)

## Authority and entrypoint
- The active Codex B reads only `docs/refactor/work_orders/C01_CODEX_CURRENT.md` first; Claude A reads only `C02_CLAUDE_CURRENT.md`. This skill is supplementary guidance, never a new task source.
- An actor must not modify D00, CURRENT, C01-C06, RF docs, queue, STATUS, patchnotes, workflows, or the other actor's files. Only own-branch source and code tests, and comments on the actor's own Issue.
- Do not select unassigned items, broaden file scope, or alter any broker, live-trading, Guard, Supervisor, Executor, Step5C, UEF, frozen oracle, runtime state, network, or operational database surfaces.
- If this skill conflicts with the canonical D00 or current C01/C02 order, STOP the conflicting action and follow the canonical contract.

## Execution checklist
1. Snapshot the order ID, all item IDs, allowed source/target paths, actor branch, and initial remote SHA. Do not invalidate an in-progress start order on mid-run update.
2. At start run `python -m pytest --version`; if missing, follow the explicit C01/C02 environment fallback. Do not treat missing pytest as license to skip other safe work.
3. For each assigned item: refetch exact remote SOURCE and TARGET blobs; check the order's ownership and prior completion. Already-done source/target is VERIFIED_ALREADY, not a new BODY MOVE.
4. For an actual move, preserve original signature, call-time facade helper resolution, monkeypatch compatibility, output, error and ordering parity. Owner holds the one calculation body; SOURCE becomes a thin wrapper, never dual implementation.
5. Use relevant fake-only targeted regression cases. Test-driven development may start with a focused failing test; do not repeatedly execute unchanged suites. Run the one normal targeted pytest/smoke with exit 0 required by G2; do not introduce blanket -O, full-suite, hosted-CI, or mandatory peer requirements.
6. Continue through ALL assigned safe items. Each must finish DONE, VERIFIED_ALREADY, or a specific BLOCKED with FIRST_BLOCKER; no stopping at first PASS/commit/push failure.
7. Commit and non-force push ONLY the actor branch. Refetch remote full SHA, tree, modified blobs and test file after push. Local-only commit is not PUSH_VERIFIED and is not G1.
8. Report exact START_KST, END_KST, measured elapsed, per-item status, test command + exit code, remote SHA, actual NEW_BODY_MOVES, blockers and next assigned point to actor Issue (#12 B / #11 A).

## Superpowers / Context7
- Use Superpowers systematic debugging when a reproducible failure exists, TDD for actual changed behavior, and verification-before-completion for evidence integrity, only if available in this execution environment.
- Use Context7 only when an external library API is material and local installed documentation is insufficient. Never introduce a dependency or network call inside a fake-only test merely to invoke Context7.
- Plugin connectivity in ChatGPT does not imply availability inside Codex/Claude/automation processes. If unavailable, apply the checklist directly; do not claim plugin execution.

## Exit evidence
`ORDER_ID | ITEM | SOURCE_BLOB | TARGET_BLOB | TEST_COMMAND | TEST_EXIT | PUSH_VERIFIED | REMOTE_SHA | FIRST_BLOCKER | NEW_BODY_MOVES`.
Never equate a successful test, MOVE, or integration to C05's RF_DONE_DELTA.
