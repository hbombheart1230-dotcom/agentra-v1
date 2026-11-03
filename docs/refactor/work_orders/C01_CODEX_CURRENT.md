# C01 — Codex B | ORDER_ID=B-20261103-09-C03 | RF-063 DEV | B42 NEW_READY=8/8 | B41 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START — remote-first; protect prior starting order
C03 verified canonical prewrite `3b859aa4facd4d38acdad3fc62507261bf48ae42`, B remote `62f227425782fc94a440910264fdd82d1fa1acd0`, old C01 blob `5b0a58bbd498a4c809170b64787499a5b727086f`. B41 #12 6590902400 delivered all 8/8, normal `tests/test_p15_rf063_20261103_08h_mock_slo_owners.py` EXIT=0 PASS=5, C04 #36 6591335590 selected 11/11 exact paths into e6319b92, C05 #36 6591430488 physical DONE 46/93. Do not redo/recount B41 or older. If prior starting order genuinely running, finish its safe items first; no retroactive cancellation.

First shell `python -m pytest --version`; if absent `python -m pip install --user pytest`, recheck. Fetch this exact remote `integration/p1.5:docs/refactor/work_orders/C01_CODEX_CURRENT.md`, log full canonical HEAD, C01 blob, ORDER_ID and B HEAD to #12. Single execution entrypoint: no D00/RF/INDEX/SKILL re-read or self-selected RF. Refetch each pinned SOURCE/TARGET on B; if drift/target exists, item-specific VERIFIED_ALREADY/BLOCKED with SHA/FIRST_BLOCKER, continue other safe items. B branch code/test only, non-force expected-head full-root delivery if terminal Git authentication unavailable.

## DONE-FIRST / resolver closeout first blocker (read-only triage)
Whole RF-063 DEV G1 PARTIAL/G3 BLOCKED despite scoped B41 G3_REUSE. Canonical `libs/reporting/llm_artifacts.py@27aea755e3ab9a3143affbd28294e4c8c775b8ca` vs B `@06dd435f68aeae0043e43f27f0b1600fa3e61b0c` resolver/consumer drift; C04/C05 own integration and whole-RF decision. At beginning record exact read-only import/dispatch and downstream trade/CLI consumer closure FIRST_BLOCKER to #12, without modifying that file or protected consumer. C03/C04/C05 must decide authorization; no blind resolver move. RF-065 alternate source `run_phase5_validation_bundle.py` and `check_trade_report_runtime_regression.py` canonical/B drift remains unadjudicated, so no unverified switch. These eight B42 items are safe diagnostics/refactoring continuity, NOT whole RF DONE. No real .env/log/report, actual go-live, RunLab, trade/LLM/broker, Guard/Step5C/UEF, state, CI/workflow or frozen oracle changes.

## B42 — eight independently verified BODY MOVEs
All eight real SOURCE bodies canonical==B pinned SHA at issuance; all eight distinct TARGETs and new test 404 canonical+B; RF-063 B-exclusive FILE_COVERAGE. Move actual calculation body to single TARGET Owner, original same-signature/default/docstring thin wrapper with call-time `sys.modules[__name__]` (or existing `_migration_sys.modules[__name__]`) facade. Owner must not import SOURCE at module import. Preserve helper monkeypatch, argparse behavior, dict/Markdown bytes, generator laziness and error types. AST-bounded editing for multiline defs, `py_compile` before test. Per item DONE or exact SHA/FIRST_BLOCKER; keep going if one blocked.

### B42-1 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_resolve_day_artifact` | SOURCE_BLOB=`331682ba27f0db3fa471cd40ce472629175fd202` (canonical=B)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_resolve_day_artifact.py::_resolve_day_artifact` | TARGET=404 canonical+B
BODY_AND_TARGETED_NORMAL=read-only direct-day JSON then sorted prefix glob latest eligible day; fake report_dir and _read_json, missing/future/day ties, return bool tuple and path identity. Original pinned AST versus Owner+wrapper fake-only parity, exact monkeypatch/error/IO safety.

### B42-2 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_iter_jsonl` | SOURCE_BLOB=`79ffdf3de93086a5a7ebeab628297bc3845cdb53` (canonical=B)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_iter_jsonl.py::_iter_jsonl` | TARGET=404 canonical+B
BODY_AND_TARGETED_NORMAL=lazy read-only JSONL generator; tmp_path fake only, blank/malformed/non-dict lines, streaming order, exceptions, no real logs. Original pinned AST versus Owner+wrapper fake-only parity, exact monkeypatch/error/IO safety.

### B42-3 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_quality_gates_bundle.py::_build_md` | SOURCE_BLOB=`6cb8fe651fd209b5ba47d4b7861bc287be4d3724` (canonical=B)
TARGET=`scripts/diagnostics/run_m30_quality_gates_bundle_build_md.py::_build_md` | TARGET=404 canonical+B
BODY_AND_TARGETED_NORMAL=pure in-memory gate status and failures Markdown, fixed functional/resilience/safety/ops ordering, numeric formatting, exact bytes. Original pinned AST versus Owner+wrapper fake-only parity, exact monkeypatch/error/IO safety.

### B42-4 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_quality_gates_bundle.py::_component_summary` | SOURCE_BLOB=`6cb8fe651fd209b5ba47d4b7861bc287be4d3724` (canonical=B)
TARGET=`scripts/diagnostics/run_m30_quality_gates_bundle_component_summary.py::_component_summary` | TARGET=404 canonical+B
BODY_AND_TARGETED_NORMAL=pure rc/ok/failure_total conversion, dict/non-dict, malformed counts, key ordering and exceptions. Original pinned AST versus Owner+wrapper fake-only parity, exact monkeypatch/error/IO safety.

### B42-5 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_quality_gates_bundle.py::_gate_status` | SOURCE_BLOB=`6cb8fe651fd209b5ba47d4b7861bc287be4d3724` (canonical=B)
TARGET=`scripts/diagnostics/run_m30_quality_gates_bundle_gate_status.py::_gate_status` | TARGET=404 canonical+B
BODY_AND_TARGETED_NORMAL=pure component pass/fail count and original components identity, zero/nonzero rc, key order. Original pinned AST versus Owner+wrapper fake-only parity, exact monkeypatch/error/IO safety.

### B42-6 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_quality_gates_bundle.py::_build_parser` | SOURCE_BLOB=`6cb8fe651fd209b5ba47d4b7861bc287be4d3724` (canonical=B)
TARGET=`scripts/diagnostics/run_m30_quality_gates_bundle_build_parser.py::_build_parser` | TARGET=404 canonical+B
BODY_AND_TARGETED_NORMAL=argparse construction only, option defaults and help, parse fake argv; NEVER invoke main or actual quality gates. Original pinned AST versus Owner+wrapper fake-only parity, exact monkeypatch/error/IO safety.

### B42-7 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_count_by` | SOURCE_BLOB=`b9bcdba3e46d5ef4c4d1948b357d5f74ac516fe3` (canonical=B)
TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_count_by.py::_count_by` | TARGET=404 canonical+B
BODY_AND_TARGETED_NORMAL=pure item grouping counts by specified key, missing/empty/string conversion, original dict order. Original pinned AST versus Owner+wrapper fake-only parity, exact monkeypatch/error/IO safety.

### B42-8 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_build_markdown` | SOURCE_BLOB=`b9bcdba3e46d5ef4c4d1948b357d5f74ac516fe3` (canonical=B)
TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_build_markdown.py::_build_markdown` | TARGET=404 canonical+B
BODY_AND_TARGETED_NORMAL=in-memory Markdown only, signoff checklist sections/status/failures, exact UTF-8 and newline formatting, no file writes. Original pinned AST versus Owner+wrapper fake-only parity, exact monkeypatch/error/IO safety.

## VERIFIED UNASSIGNED RESERVE — B 6/6
All six distinct real SOURCE bodies canonical=B, RF-063 B-exclusive FILE_COVERAGE, TARGET 404 canonical+B, fake-only IO/effect/test verified; NOT ASSIGNED, no PASS or G1 counted. Never self-select.
1. SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_run_json@b9bcdba3e46d5ef4c4d1948b357d5f74ac516fe3` → TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_run_json.py::_run_json` (404 C+B); TEST/SAFETY=fake main_fn stdout capture, json.loads exception handling; no real subprocess or real main.
2. SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_read_json@b9bcdba3e46d5ef4c4d1948b357d5f74ac516fe3` → TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_read_json.py::_read_json` (404 C+B); TEST/SAFETY=tmp_path read-only JSON dict/missing/malformed and exception parity.
3. SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_gitignore_has_env@b9bcdba3e46d5ef4c4d1948b357d5f74ac516fe3` → TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_gitignore_has_env.py::_gitignore_has_env` (404 C+B); TEST/SAFETY=tmp_path fake .gitignore and .env line matching, no actual credentials.
4. SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_item@b9bcdba3e46d5ef4c4d1948b357d5f74ac516fe3` → TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_item.py::_item` (404 C+B); TEST/SAFETY=pure keyword-only item payload builder, defaults and dict order.
5. SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_build_parser@b9bcdba3e46d5ef4c4d1948b357d5f74ac516fe3` → TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_build_parser.py::_build_parser` (404 C+B); TEST/SAFETY=argparse options/defaults only; no main, no real signoff.
6. SOURCE=`scripts/diagnostics/run_m30_final_golive_signoff.py::_build_markdown@20c5ba5c9d94bf3d1b2fb43bee6206df18872271` → TARGET=`scripts/diagnostics/run_m30_final_golive_signoff_build_markdown.py::_build_markdown` (404 C+B); TEST/SAFETY=in-memory final signoff Markdown exact bytes; no actual go-live execution.

## TARGETED TEST / NON-FORCE DELIVERY / ACCEPTANCE
Implement new `tests/test_p15_rf063_20261103_09h_m30_m31_readonly_owners.py` (404 C+B), pinned preimage AST→Owner/wrapper parity for all eight, original signatures/defaults/keyword-only, fake-only Path/argparse/Markdown/dict/exception/monkeypatch/generator. No real .env, logs, reports, quality gates, release signoff or main. `python -m py_compile` all changed SOURCE+Owner+test EXIT0; normal `python -m pytest -q tests/test_p15_rf063_20261103_09h_m30_m31_readonly_owners.py` EXIT0 required, actual PASS count only. Prepush `git status --short` and staged full-root manifest SOURCE 4 + Owner 8 + test 1 = **13 paths**; `git diff --cached --name-only`, `git show --name-only`, no root truncation. Non-force B push or authorized non-force expected-head CAS preserving full root; re-fetch final B HEAD/tree and all 13 source/owner/test blobs. Each B42-1..8 DONE/BLOCKED with exact SOURCE before/after, Owner/test blob and FIRST_BLOCKER. Report actual START_KST/END_KST/ELAPSED_MIN, normal EXIT/PASS, remote SHA and resolver read-only closure evidence to #12. C04 alone G3 integration, C05 alone RF DONE/STATUS; no docs/RF/STATUS/CI/operations writes.
