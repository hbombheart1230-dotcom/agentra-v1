# C01 — Codex B | ORDER_ID=B-20261103-08-C03 | RF-063 DEV | B41 NEW_READY=8/8 | B40 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START — latest remote only; protect starting order
C03 prewrite canonical `15207cf47e3b1b447545f5948a73eed3801f1e9d`, B remote `52a4a9b2d667b47631af0fe8ffc7d4d9534eea05`, previous C01 blob `a3c15ac68a37500ca0d0b88a614d2458fb1f38e3`. B40 [#12 6589772676](https://github.com/hbombheart1230-dotcom/agentra/issues/12#issuecomment-6589772676) all **8/8 remote DONE**, `tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` normal EXIT0/6 PASS, syntax EXIT0; C04 [#36 6590341772](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6590341772) integrated exact B40 11/11 at canonical `15207cf4`. Old malformed local `49f4c8c1` invalid, never reuse. Do not redo/recount B40 or B1-B39. Preserve any truly in-flight earlier starting order.

First shell `python -m pytest --version`; if missing `python -m pip install --user pytest`, recheck. Fetch **remote** `integration/p1.5:docs/refactor/work_orders/C01_CODEX_CURRENT.md`, log full canonical HEAD/C01 blob/ORDER_ID and B HEAD to #12. C01 is sole execution entrypoint; no D00/RF/INDEX/SKILL re-read or self-selection. Refetch each pinned B SOURCE/TARGET; if drift/target exists mark item-specific VERIFIED_ALREADY/BLOCKED with SHA/FIRST_BLOCKER, continue others. Only B code/test branch, non-force push.

## DONE-FIRST / resolver containment
C05 07:48 physical 46/93 DONE (PENDING38/DEV7/PEER2). RF-063 whole G1 residual and G3 resolver/consumer BLOCKED: canonical `libs/reporting/llm_artifacts.py@27aea755e3ab9a3143affbd28294e4c8c775b8ca` vs B `@06dd435f68aeae0043e43f27f0b1600fa3e61b0c`. B40 scoped G3_REUSE ≠ whole RF DONE. RF-065 alternative source `scripts/research/run_phase5_validation_bundle.py` canonical `1beb655b` vs B `b44edf39`, `check_trade_report_runtime_regression.py` canonical `dc882aa5` vs B `c7113fcf`; do not issue a blind RF-065 or cross-owner resolver move on mismatched preimages. C03/C04/C05 must adjudicate exact dependency-closed resolver/consumer import parity and B-04 G3; no self-selected protected changes. B41 uses the remaining independently verified read-only/pure RF-063 functions while closeout blockers are routed separately. No LLM/resolver/trade/Guard/Step5C/UEF/broker, real .env, real logs/reports, operational state, runtime, CI/workflow or frozen oracle changes.

## B41 eight independently verified SOURCE BODY MOVEs
All real bodies canonical==B at issuance, 8 distinct exclusive TARGETs and new targeted test 404 canonical+B. Transfer entire computation to single Owner and retain same-signature/default/docstring SOURCE thin wrapper, call-time facade `sys.modules[__name__]` (SLO existing `_migration_sys.modules[__name__]`), preserve helper monkeypatches/import paths, dict order, error types, generator laziness and exact Markdown bytes. Use AST-bounded editing for multiline keyword-only `_item`, `py_compile` before tests. No Owner importing SOURCE at import-time; no double body.

### 1. RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_read_env_file` | SOURCE_GIT_BLOB=`2a875186f0a869966b26192e5ebd72240dde69b9` (canonical=actor verified 08h)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_read_env_file.py::_read_env_file` | TARGET=404 canonical+actor verified
BODY=read-only Path env parser: comments, quote removal, split first '=', inline # only unquoted, key order; NEVER read real .env
TARGETED_NORMAL=tmp_path fake .env only, quoted/inline comment/empty/missing/malformed, no secrets
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 2. RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_parse_kst_datetime` | SOURCE_GIT_BLOB=`2a875186f0a869966b26192e5ebd72240dde69b9` (canonical=actor verified 08h)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_parse_kst_datetime.py::_parse_kst_datetime` | TARGET=404 canonical+actor verified
BODY=ISO Z/naive/aware conversion into KST; naive replace tzinfo KST, invalid None; preserve KST facade
TARGETED_NORMAL=empty, malformed, Z, naive, offset, boundary date, monkeypatched KST
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 3. RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_utc_day` | SOURCE_GIT_BLOB=`2a875186f0a869966b26192e5ebd72240dde69b9` (canonical=actor verified 08h)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_utc_day.py::_utc_day` | TARGET=404 canonical+actor verified
BODY=call-time _to_epoch then UTC date via datetime.fromtimestamp; None and exception propagation preserved
TARGETED_NORMAL=epoch 0, UTC boundary, invalid, patched _to_epoch and datetime
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 4. RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_item` | SOURCE_GIT_BLOB=`2a875186f0a869966b26192e5ebd72240dde69b9` (canonical=actor verified 08h)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_item.py::_item` | TARGET=404 canonical+actor verified
BODY=keyword-only five-field checklist dict id,title,required,passed,evidence; preserve multiline signature/default/order/bool/str
TARGETED_NORMAL=required omitted/default, truthy objects, positional TypeError, key order; AST-safe header
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 5. RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_build_markdown` | SOURCE_GIT_BLOB=`2a875186f0a869966b26192e5ebd72240dde69b9` (canonical=actor verified 08h)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_build_markdown.py::_build_markdown` | TARGET=404 canonical+actor verified
BODY=full in-memory mock exam Markdown from runtime_mode/guardrails/market/events/checklist; exact headings, format, newline bytes
TARGETED_NORMAL=empty/full/malformed nested payload, Unicode, failure rows, original byte parity
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 6. RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_build_parser` | SOURCE_GIT_BLOB=`2a875186f0a869966b26192e5ebd72240dde69b9` (canonical=actor verified 08h)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_build_parser.py::_build_parser` | TARGET=404 canonical+actor verified
BODY=argparse construction only; preserve defaults and --allow-offhours/--strict-session/--now-kst, no parse/main
TARGETED_NORMAL=fake argv parsing defaults/flags/help, patched argparse, no CLI main
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 7. RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_iter_jsonl` | SOURCE_GIT_BLOB=`c3fbff8859a8bd34e9426f1058986ea45e973517` (canonical=actor verified 08h)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_iter_jsonl.py::_iter_jsonl` | TARGET=404 canonical+actor verified
BODY=nested lazy generator, read-only path.open UTF-8, skip blank/bad/non-dict, return [] if missing; do NOT materialize
TARGETED_NORMAL=tmp_path only, missing/invalid/mixed JSONL, lazy iterator behavior, exact errors
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 8. RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_read_json` | SOURCE_GIT_BLOB=`c3fbff8859a8bd34e9426f1058986ea45e973517` (canonical=actor verified 08h)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_read_json.py::_read_json` | TARGET=404 canonical+actor verified
BODY=read-only Path JSON parser: missing => {}, try/except Exception => {}, dict only; no writes
TARGETED_NORMAL=tmp_path missing/invalid/list/dict, facade json, exception parity
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

## VERIFIED UNASSIGNED RESERVE — B 6/6
Each real body verified RF-063 B-exclusive FILE_COVERAGE, canonical=B SOURCE blob, six distinct TARGET 404 C+B, IO/state/fake test scope verified at 08h. UNASSIGNED, no actor discretion or G2 claim.
1. SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_resolve_day_artifact@c3fbff8859a8bd34e9426f1058986ea45e973517` → TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_resolve_day_artifact.py::_resolve_day_artifact` (404 canonical+actor). BODY/TEST=read-only direct-day then sorted glob latest eligible prior day; tmp_path + fake _read_json; exclusive Owner; unassigned, no PASS.
2. SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_iter_jsonl@2a875186f0a869966b26192e5ebd72240dde69b9` → TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_iter_jsonl.py::_iter_jsonl` (404 canonical+actor). BODY/TEST=lazy read-only JSONL generator; tmp_path only, malformed/blank/dict filter; exclusive Owner; unassigned, no PASS.
3. SOURCE=`scripts/diagnostics/run_m30_quality_gates_bundle.py::_build_md@6cb8fe651fd209b5ba47d4b7861bc287be4d3724` → TARGET=`scripts/diagnostics/run_m30_quality_gates_bundle_build_md.py::_build_md` (404 canonical+actor). BODY/TEST=in-memory gate/failure Markdown exact bytes; exclusive Owner; unassigned, no PASS.
4. SOURCE=`scripts/diagnostics/run_m30_quality_gates_bundle.py::_component_summary@6cb8fe651fd209b5ba47d4b7861bc287be4d3724` → TARGET=`scripts/diagnostics/run_m30_quality_gates_bundle_component_summary.py::_component_summary` (404 canonical+actor). BODY/TEST=pure rc/ok/failure_total dict, key order; exclusive Owner; unassigned, no PASS.
5. SOURCE=`scripts/diagnostics/run_m30_quality_gates_bundle.py::_gate_status@6cb8fe651fd209b5ba47d4b7861bc287be4d3724` → TARGET=`scripts/diagnostics/run_m30_quality_gates_bundle_gate_status.py::_gate_status` (404 canonical+actor). BODY/TEST=pure pass/fail counts and components identity; exclusive Owner; unassigned, no PASS.
6. SOURCE=`scripts/diagnostics/run_m30_quality_gates_bundle.py::_build_parser@6cb8fe651fd209b5ba47d4b7861bc287be4d3724` → TARGET=`scripts/diagnostics/run_m30_quality_gates_bundle_build_parser.py::_build_parser` (404 canonical+actor). BODY/TEST=argparse builder only; no main/real execution; exclusive Owner; unassigned, no PASS.

## TEST / PUSH / ACCEPTANCE
Implement `tests/test_p15_rf063_20261103_08h_mock_slo_owners.py` (404 C+B) pinned preimage AST→Owner/wrapper fake parity for all eight, original signatures/defaults/keyword-only/monkeypatch/identity/bytes/lazy generator and exceptions. `_read_env_file` must ONLY open tmp_path fake fixture; `_iter_jsonl`/JSON only tmp_path. `python -m py_compile` changed SOURCE+Owner EXIT0, then normal `python -m pytest -q tests/test_p15_rf063_20261103_08h_mock_slo_owners.py` **EXIT0 required**. Staged full-root manifest SOURCE 2 + Owner 8 + test 1 = **11 paths**; check status, staged names, commit names. Non-force B push or authorized non-force expected-head **full-root** exact-tree fallback (never root-only tests); re-fetch B remote HEAD/tree and 11 paths. Each B41-1..8 DONE or exact SHA/FIRST_BLOCKER; continue safe items despite failure. Report actual START_KST/END_KST/ELAPSED_MIN, normal EXIT/PASS, SOURCE before/after, Owner/test blobs, remote SHA to #12. C04 integration/G3, C05 DONE/STATUS exclusive. No docs/RF/STATUS/CI/operations writes.
