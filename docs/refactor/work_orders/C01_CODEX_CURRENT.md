# C01 — Codex B | ORDER_ID=B-20261103-00-C03 | RF-063 DEV | B38 NEW_READY=8/8 | B37 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START / authoritative remote pins
Canonical prewrite `integration/p1.5@4a5aee47903e5377345c45fcdb0cdc1584abcce5` (C02 A48 order-only commit); B actor `work/p15-b-operator-structure-20261022@4544b306fa9dffa955e3f4bc11db3ac451e70aa6`. Previous C01 blob `8c07123ae503c2e7f6289b18c9b15f72c93c5cda`. #12 [B37 6579316310](https://github.com/hbombheart1230-dotcom/agentra/issues/12#issuecomment-6579316310) **B37-1..8 REMOTE_DONE**, B remote tree `4e5019f6a8cb7452cbb99d74da582f4290568a92`, actor normal `python -m pytest -q tests/test_p15_rf063_20261102_20h_diagnostics_pure_owners.py` **8 PASS EXIT=0**. C04 [#36 6579778546](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6579778546) integrated exact B37 SOURCE/Owner/test at `b0276b01bcbaad4131d70d6d033e2ff9ad843b75`; C05 [#36 6580657392](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6580657392) accepted scoped G3_REUSE. #12 [6580839696](https://github.com/hbombheart1230-dotcom/agentra/issues/12#issuecomment-6580839696) re-read B37 and found VERIFIED_ALREADY 8/8, new code 0. **B37 and B1–B36 MUST NOT be reimplemented/retested/recounted.** If prior starting order genuinely in progress, finish safe items first; new order does not retroactively cancel.

First shell `python -m pytest --version`; if absent `python -m pip install --user pytest`, recheck. Then **fetch latest remote** `integration/p1.5:docs/refactor/work_orders/C01_CODEX_CURRENT.md` by branch (not stale local/cached checkout) and log exact REMOTE_CANONICAL_HEAD | REMOTE_C01_BLOB_SHA | ORDER_ID in #12. Latest expected header is `B-20261103-00-C03 / B38-1..8`; if B37 or older, refetch before concluding no work. C06 #37 [6577794729](https://github.com/hbombheart1230-dotcom/agentra/issues/37#issuecomment-6577794729) stale-order defect was routed once in #36 [6577827833](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6577827833); B37 is now delivered and this is **not a new code correction**. Read this single C01, not D00/RF/INDEX/CURRENT. Agentra skill `.agents/skills/agentra-contract-guard/SKILL.md@f2fe45fd856f65f5f7b5a3b710317baf1bf9ad5d` is C03-manually-checked, non-authoritative; runtime autoload NOT_VERIFIED, not an extra gate.

## DONE-FIRST / first unmet whole RF
C05 [#36 6581557766](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6581557766): physical PENDING38 / DEV7 / PEER2 / DONE46, unresolved47. RF-030 whole G1 partial (15/16 KEEP vs RF-074 frozen oracle), G2 pending, canonical G3 smoke pending; C04/C05 own closure. RF-063 whole G1/G2 residual and G3 resolver/import/runtime parity NOT_MET; prior bounded two-edge `llm_artifacts.py` resolver map found no missing import but full runtime parity remains NOT_VERIFIED. B37 scoped G3 already accepted; B38 does not fix resolver or grant RF DONE. **No trade/LLM/resolver/effect code changes without new C03 authorization.** RF-026 cold-import G1 BLOCKED_POLICY; RF-032 validation-id/Writer/UEF HOLD. Preserve all Guard/real/paper orders/Step5C/UEF/RunLab/operations, frozen oracle, network, OS/DB writes.

## B38 — 8 individually verified pure BODY MOVE items (RF-063 exclusive)
C03 inspected actual SOURCE bodies and RF-063 FILE_COVERAGE; SOURCE Git blobs identical on canonical and B for all eight; complete nontruncated Git trees C=5736, B=4696 entries confirm each sole TARGET and `tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` absent both refs. B38-1..8 are diagnostics AST/in-memory observation/argparse construction only. B38-7 mutates only the **provided fake result dict**, not real scheduler/frozen policy. B38-8 constructs parser only, never calls main or seeds events.

**Each item:** re-fetch SOURCE exact Git blob/TARGET before editing; if changed/target exists report VERIFIED_ALREADY=0 or BLOCKED with SHA/FIRST_BLOCKER, no overwrite. Move **entire real function body** into unique Owner, leave original same-signature/default/docstring thin wrapper; use `facade=sys.modules[__name__]` (or SOURCE's existing `_migration_sys.modules[__name__]`) at call time to preserve monkeypatch helper/constants/ast/argparse/datetime/regex and exact exception/identity/ordering/formatting semantics. Owner must not import SOURCE. Preserve in-place dict mutation for B38-7. No OS/environment/DB/file/network/operational calls in tests, no CLI main. Create fake-only `tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py`, original-preimage AST vs wrapper/Owner parity for all 8, normal `python -m pytest -q tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` EXIT=0, no mandatory -O/full suite/hosted CI. Only B edits B code/tests and non-force pushes B branch. If any item blocked, continue all other independent safe items.

### B38-1 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/audit_target_tree_compat.py::_dispatch_issues` Git blob `28bb333bf7e37828cac4008c55dc0b04723de549` (canonical=B). TARGET=`scripts/diagnostics/audit_target_tree_compat_dispatch_issues.py::_dispatch_issues` (404 canonical+B).
ACTUAL_BODY=Pure AST dispatch/ABI alias audit: exact __main__ guard count, bulk runpy vs nonbulk _impl.main, import alias and example implementation binding; call facade.ast/_has_statement at use time.
TARGETED_NORMAL_CASES=Fake ast.Module one/zero/two guards, bulk/nonbulk, missing alias/import, monkeypatched _has_statement, exact issues order and exception.
TEST=`tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` exact original AST vs wrapper/Owner fake parity. On blocker record current SOURCE/TARGET/SHA/FIRST_BLOCKER; continue B38-2 or completion.

### B38-2 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/audit_windows_launchers.py::_resolve_task` Git blob `f9bf40b819f95dc1cdc10d6b64efa36c0b3cec34` (canonical=B). TARGET=`scripts/diagnostics/audit_windows_launchers_resolve_task.py::_resolve_task` (404 canonical+B).
ACTUAL_BODY=Regex-only literal task name or %TASK_PREFIX% suffix resolution; facade.re and original regex flags; no scheduler query/mutation.
TARGETED_NORMAL_CASES=Literal/prefix/no prefix/malformed task, patched re, exact tuple status/order.
TEST=`tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` exact original AST vs wrapper/Owner fake parity. On blocker record current SOURCE/TARGET/SHA/FIRST_BLOCKER; continue B38-3 or completion.

### B38-3 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/reconstruct_incident_timeline.py::_utc_day` Git blob `a24339f3f0599178c1046d13e20bbf771ac33a86` (canonical=B). TARGET=`scripts/diagnostics/reconstruct_incident_timeline_utc_day.py::_utc_day` (404 canonical+B).
ACTUAL_BODY=Pure UTC date projection via facade._to_epoch; when None use facade.datetime.now(facade.timezone.utc), otherwise datetime.fromtimestamp; preserve monkeypatch clock and formatting.
TARGETED_NORMAL_CASES=None/bad timestamp, zero/offset epoch, fake clock, patched _to_epoch/datetime, exact date and exceptions.
TEST=`tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` exact original AST vs wrapper/Owner fake parity. On blocker record current SOURCE/TARGET/SHA/FIRST_BLOCKER; continue B38-4 or completion.

### B38-4 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/query_intent_state_store.py::_summary` Git blob `4e4dc6b3d032ef516d4f9b5f04fb0503edcb70f5` (canonical=B). TARGET=`scripts/diagnostics/query_intent_state_store_summary.py::_summary` (404 canonical+B).
ACTUAL_BODY=In-memory state-row filtering, age_sec calculation, active/terminal counts, stuck executing threshold, journal_transition_total passthrough, max(1,limit) truncation; no SQLite read/write.
TARGETED_NORMAL_CASES=Empty/filter/terminal/active/stuck cutoff, negative age, limit0/1, input identity, exact dict key order/exception.
TEST=`tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` exact original AST vs wrapper/Owner fake parity. On blocker record current SOURCE/TARGET/SHA/FIRST_BLOCKER; continue B38-5 or completion.

### B38-5 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/query_intent_state_store.py::_build_parser` Git blob `4e4dc6b3d032ef516d4f9b5f04fb0503edcb70f5` (canonical=B). TARGET=`scripts/diagnostics/query_intent_state_store_build_parser.py::_build_parser` (404 canonical+B).
ACTUAL_BODY=Construct argparse.ArgumentParser only (no parse_args or DB connection), seven original flags/defaults; use facade.argparse at call time.
TARGETED_NORMAL_CASES=Fake argv parse after constructing parser, defaults/choices/flags, patched argparse, help/usage parity; never touch DB.
TEST=`tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` exact original AST vs wrapper/Owner fake parity. On blocker record current SOURCE/TARGET/SHA/FIRST_BLOCKER; continue B38-6 or completion.

### B38-6 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/check_phase_5_2_5_3_runtime_health.py::_build_parser` Git blob `e095bee3edae83c4e482680091ba906c1c50b1d7` (canonical=B). TARGET=`scripts/diagnostics/check_phase_5_2_5_3_runtime_health_build_parser.py::_build_parser` (404 canonical+B).
ACTUAL_BODY=Only construct existing runtime-health argparse parser; preserve flags/defaults and facade.argparse; do NOT call runtime inspection or main.
TARGETED_NORMAL_CASES=Parser default/flags/help fake argv, patched argparse, exact namespace; no runtime query.
TEST=`tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` exact original AST vs wrapper/Owner fake parity. On blocker record current SOURCE/TARGET/SHA/FIRST_BLOCKER; continue B38-7 or completion.

### B38-7 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/audit_windows_launchers.py::assert_mockexam_known_contract` Git blob `f9bf40b819f95dc1cdc10d6b64efa36c0b3cec34` (canonical=B). TARGET=`scripts/diagnostics/audit_windows_launchers_assert_mockexam_known_contract.py::assert_mockexam_known_contract` (404 canonical+B).
ACTUAL_BODY=In-memory result dict mutation only: compare status/registered/unregistered to facade._FROZEN_REGISTERED/_FROZEN_UNREGISTERED; append issue if mismatched, update result['ok']; never edit frozen constants or run scheduler.
TARGETED_NORMAL_CASES=Fake proven/missing/extra task sets, existing issues, identity and in-place mutation parity, patched frozen sets; exact text and exception. Frozen oracle untouched.
TEST=`tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` exact original AST vs wrapper/Owner fake parity. On blocker record current SOURCE/TARGET/SHA/FIRST_BLOCKER; continue B38-8 or completion.

### B38-8 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m29_incident_timeline_check.py::_build_parser` Git blob `780a678e8c3741847cd3db5afbb26aa4480184c7` (canonical=B). TARGET=`scripts/diagnostics/run_m29_incident_timeline_check_build_parser.py::_build_parser` (404 canonical+B).
ACTUAL_BODY=Only construct original M29-7 incident timeline argparse parser with path/day/inject-fail/json defaults; no _seed_events, _run_json, filesystem or main.
TARGETED_NORMAL_CASES=Fake argv default/custom flags, patched argparse, help/usage parity; no report or event writes.
TEST=`tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` exact original AST vs wrapper/Owner fake parity. On blocker record current SOURCE/TARGET/SHA/FIRST_BLOCKER; continue B38-9 or completion.
## VERIFIED RESERVE — B 6/6, UNASSIGNED (not B38)
C03 inspected actual pure SOURCE bodies, exact identical canonical/B Git blobs and unique TARGET 404 in both complete Git trees. RF-063 FILE_COVERAGE owns each SOURCE. These are fake-only in-memory replay projection, Markdown or parser construction; **no actual replay/restore/mock exam/guard/operational mutation**. They are NOT B38 and B may not self-select them.
1. `scripts/diagnostics/run_m29_disaster_recovery_drill.py::_replay_metrics@a8a340b97a61ce953faf3d30c0dff7ca4cb86a56` → `scripts/diagnostics/run_m29_disaster_recovery_drill_replay_metrics.py::_replay_metrics` (404 C+B); TEST_HYPOTHESIS=In-memory six replay count/notional conversions; fake dict only, no replay; UNASSIGNED.
2. `scripts/diagnostics/run_m29_disaster_recovery_drill.py::_replay_parity_ok@a8a340b97a61ce953faf3d30c0dff7ca4cb86a56` → `scripts/diagnostics/run_m29_disaster_recovery_drill_replay_parity_ok.py::_replay_parity_ok` (404 C+B); TEST_HYPOTHESIS=Pure count/notional comparison with 1e-9 tolerance, fake dict only; UNASSIGNED.
3. `scripts/diagnostics/run_m29_disaster_recovery_drill.py::_build_parser@a8a340b97a61ce953faf3d30c0dff7ca4cb86a56` → `scripts/diagnostics/run_m29_disaster_recovery_drill_build_parser.py::_build_parser` (404 C+B); TEST_HYPOTHESIS=Argparse construction only, no dataset clear/restore/replay; UNASSIGNED.
4. `scripts/diagnostics/run_m31_mock_exam_readiness_check.py::_item@721630febbfadcb62940c4cc56486cf11bf047af` → `scripts/diagnostics/run_m31_mock_exam_readiness_check_item.py::_item` (404 C+B); TEST_HYPOTHESIS=Pure checklist dict projection, fake bool/string input; UNASSIGNED.
5. `scripts/diagnostics/run_m31_mock_exam_readiness_check.py::_build_markdown@721630febbfadcb62940c4cc56486cf11bf047af` → `scripts/diagnostics/run_m31_mock_exam_readiness_check_build_markdown.py::_build_markdown` (404 C+B); TEST_HYPOTHESIS=Pure readiness Markdown from fake in-memory payload; preserve exact text, never alter Guard/operations; UNASSIGNED.
6. `scripts/diagnostics/run_m31_mock_exam_readiness_check.py::_build_parser@721630febbfadcb62940c4cc56486cf11bf047af` → `scripts/diagnostics/run_m31_mock_exam_readiness_check_build_parser.py::_build_parser` (404 C+B); TEST_HYPOTHESIS=Argparse construction only, fake argv; no mock exam execution; UNASSIGNED.
 
## ACCEPTANCE / #12
Finish B38-1..8 or item-specific BLOCKED with SOURCE/TARGET/current SHA/FIRST_BLOCKER; continue independent items. Report measured START_KST/END_KST/ELAPSED_MIN, B remote HEAD before/after, full-root tree, SOURCE before/after/Owner/test Git blobs, exact normal command EXIT/PASS, non-force push and remote re-fetch. If terminal Git authentication blocks push, only approved non-force exact-tree connector fallback preserving full root; else PUSH_BLOCKED. Count actual new BODY MOVEs only; KEEP/ALREADY=0. No changes to C02/D00/C03/C04/C05/RF/STATUS or other actor. C04 integrates selected G3, C05 alone updates RF/STATUS/DONE. C03 did not execute B code or tests.
