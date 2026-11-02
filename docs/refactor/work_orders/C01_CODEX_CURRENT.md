# C01 — Codex B | ORDER_ID=B-20261103-03-C03 | RF-063 DEV | B40 NEW_READY=8/8 | B39 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START — exact remote and starting-order protection
Canonical prewrite `8fe92ce5f9dc3c9bb131a59b7b75d87150bdf59d`; B actor HEAD `60577211d953da14a2ed6b272582564da22a661e`. Previous C01 blob `241bd03c9993628659e96a36f1289f67e54f2103`. B39-1..8 [#12 6583531867](https://github.com/hbombheart1230-dotcom/agentra/issues/12#issuecomment-6583531867) remote DONE8/8, normal `tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py` EXIT=0 PASS=6; C04 [#36 6584029322](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6584029322) integrated exact B39 at `8fe92ce5`; do not redo B1–B39 or count them again. If B39 genuinely in progress at start, finish its safe items first; no retroactive cancellation.

First shell `python -m pytest --version`; if unavailable run `python -m pip install --user pytest` then recheck. Fetch latest **remote branch** `integration/p1.5:docs/refactor/work_orders/C01_CODEX_CURRENT.md`, not stale local checkout; report full REMOTE_CANONICAL_HEAD, C01_BLOB_SHA, ORDER_ID in #12. This C01 alone is the execution entrypoint; do not reread D00/RF/INDEX. At start refetch B HEAD and each SOURCE/TARGET; drift or target exists means item-specific VERIFIED_ALREADY/BLOCKED with exact SHA, continue other safe items.

## DONE-FIRST — RF closeout blockers, do not conflate diagnostics with DONE
Latest C05 [#36 6584047694](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6584047694) physically verified DONE46/93, PENDING38/DEV7/PEER2, unresolved47. RF-030 exact canonical G3 fake smoke belongs C04, RF-032 Writer/UEF validation-id BLOCKED_POLICY; do not touch. RF-063 whole G1/G2 residual and G3 resolver/consumer parity BLOCKED: canonical `libs/reporting/llm_artifacts.py@27aea755e3ab9a3143affbd28294e4c8c775b8ca` vs B actor `@06dd435f68aeae0043e43f27f0b1600fa3e61b0c`; B39 [#12 6583531867] identified consumer import divergence. C04 must review complete safe resolver closure, not blindly cherry-pick a test. B40 does **not** authorize resolver/trade/LLM, broker, Guard, Step5C, UEF, real mode or operations changes. Do not treat B40 as RF-063 DONE. After B40, C03 will prioritize other unresolved B RF (e.g. RF-065) once source/owner/IO safe scope is independently validated; B must not self-select.

## B40 REMOTE_MISSING / syntax-safe continuation — C03 2026-11-03 04h, preserve ALL B40-1..8
[#12 6584755739](https://github.com/hbombheart1230-dotcom/agentra/issues/12#issuecomment-6584755739) confirms B40 local-only commit `49f4c8c1` contains a malformed multiline keyword-only `_item` wrapper: `SyntaxError: '(' was never closed` at `scripts/diagnostics/run_m31_slo_incident_review_check.py:90`. Normal targeted EXIT=1/PASS=0; **B remote HEAD remains `60577211d953da14a2ed6b272582564da22a661e`, all eight B40 remain UNDELIVERED**. This is not a C06 #37 finding and not a new B41 assignment. Keep the already-started B40 order; do not cancel, repeat B39, or count local `49f4c8c1` as G1.
- **FIRST ACTION:** inspect local `git status --short` and preserve unrelated work; use exact remote B HEAD `60577211...` as the clean SOURCE preimage (do not force-push or blindly reset unrelated work). Discard/repair only the malformed B40 local transformation. Re-read the exact remote SOURCE `scripts/diagnostics/run_m31_slo_incident_review_check.py@7a1ad49ba5941aa661a974a4b6690bade41275eb` and `run_m31_mock_investor_exam_check.py@e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f`; ensure all eight B40 targets remain absent on B before modifying.
- **B40-3 exact repair:** SOURCE `run_m31_slo_incident_review_check.py::_item` has the **multiline keyword-only signature** `def _item(*, item_id: str, title: str, passed: bool, evidence: str, required: bool = True) -> Dict[str, Any]`. Preserve this exact callable signature, defaults, `__name__` monkeypatch seam and dict insertion order. Replace only its calculation body with an import-and-delegate wrapper using `from scripts.diagnostics.run_m31_slo_incident_review_check_item import _item as owner` and `return owner(item_id=item_id, title=title, passed=passed, evidence=evidence, required=required, facade=_migration_sys.modules[__name__])`; Owner has real original five-key dict calculation and accepts keyword-only `facade`. Do **not** regex-cut at the first newline of a function header. Use `ast.parse` or manually bounded signature/body edits for **all** B40 wrappers.
- Before running pytest, `python -m py_compile scripts/diagnostics/run_m31_slo_incident_review_check.py scripts/diagnostics/run_m31_mock_investor_exam_check.py` EXIT0, then `python -m pytest -q tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` **normal EXIT0 required** on exact B40 final tree; fake-only, no CLI main, real env, market or operational writes. Compile is an early syntax check, not an extra RF DONE gate. Test must include keyword-only required/default, missing positional argument TypeError, dict key order and source/Owner original-AST parity.
- **All B40-1..8** remain assigned. For each record DONE with SOURCE before/after + exclusive Owner/test blobs or BLOCKED with exact SOURCE/TARGET/current SHA/FIRST_BLOCKER; continue independent safe items after a blocked one. Verify full staged SOURCE 2 + Owner 8 + targeted test 1 path manifest, `git show --name-only`, normal exit, non-force remote B push or authorized full-root expected-head route, then refetch remote B HEAD/root tree and 11 paths. Report real times and final evidence in **#12**. Do not invent PASS, G3 or RF DONE.
- **Closeout separation:** RF-063 whole G3 remains blocked by `libs/reporting/llm_artifacts.py` canonical `27aea755` vs B `06dd435f` and resolver/consumer parity. B40 diagnostics cannot clear that. C04 alone selects safe integration, C05 alone RF DONE.

## B40 — eight independent real SOURCE BODY MOVEs (all assigned)
Owner paths are unique, within RF-063 `scripts/diagnostics/`, absent on both canonical and B complete nontruncated Git trees at issuance; both SOURCE blobs canonical==B. Each item: move full original calculation body to one Owner function with same name, keep original signature/default/docstring thin wrapper in SOURCE; call-time `facade=sys.modules[__name__]` (SLO uses `_migration_sys.modules[__name__]`) for monkeypatchable helpers, constants, argparse/datetime. Owner must not import SOURCE; no double body. Preserve original return keys/order/identity/exceptions/CLI defaults. No `main`, no real env read, no runtime tick, no network/filesystem/DB/real order; only fake in-memory tests and argparse construction.

### B40-1 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_to_epoch` | SOURCE_GIT_BLOB=`7a1ad49ba5941aa661a974a4b6690bade41275eb` (canonical=B at issuance)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_to_epoch.py::_to_epoch` | TARGET=404 canonical+B, single exclusive Owner
ACTUAL_BODY=Return None for missing/blank; numeric int; float-string; ISO/Z datetime UTC; same exception suppression and timezone behavior
MOVE=transfer entire real body to Owner; SOURCE same-signature wrapper with dynamic facade; no effect/consumer edits.
TARGETED_NORMAL_CASES=None, floats, ISO naive/aware/Z, invalid dates, custom str
TEST=`tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` original preimage AST vs final Owner/wrapper on fake inputs; verify output, exception, key/byte order and monkeypatch. If SHA drift or collision, item-specific FIRST_BLOCKER and continue.

### B40-2 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_utc_day` | SOURCE_GIT_BLOB=`7a1ad49ba5941aa661a974a4b6690bade41275eb` (canonical=B at issuance)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_utc_day.py::_utc_day` | TARGET=404 canonical+B, single exclusive Owner
ACTUAL_BODY=Use SOURCE facade._to_epoch dynamically, UTC date formatting; preserve None and boundary behavior
MOVE=transfer entire real body to Owner; SOURCE same-signature wrapper with dynamic facade; no effect/consumer edits.
TARGETED_NORMAL_CASES=epoch=0, midnight, cross-day, monkeypatched _to_epoch, invalid
TEST=`tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` original preimage AST vs final Owner/wrapper on fake inputs; verify output, exception, key/byte order and monkeypatch. If SHA drift or collision, item-specific FIRST_BLOCKER and continue.

### B40-3 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_item` | SOURCE_GIT_BLOB=`7a1ad49ba5941aa661a974a4b6690bade41275eb` (canonical=B at issuance)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_item.py::_item` | TARGET=404 canonical+B, single exclusive Owner
ACTUAL_BODY=Return original five-key checklist dict from keyword-only arguments with bool conversion, key order
MOVE=transfer entire real body to Owner; SOURCE same-signature wrapper with dynamic facade; no effect/consumer edits.
TARGETED_NORMAL_CASES=all required/default False, truthy custom objects, keyword-only TypeError
TEST=`tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` original preimage AST vs final Owner/wrapper on fake inputs; verify output, exception, key/byte order and monkeypatch. If SHA drift or collision, item-specific FIRST_BLOCKER and continue.

### B40-4 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_build_markdown` | SOURCE_GIT_BLOB=`7a1ad49ba5941aa661a974a4b6690bade41275eb` (canonical=B at issuance)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_build_markdown.py::_build_markdown` | TARGET=404 canonical+B, single exclusive Owner
ACTUAL_BODY=Original in-memory SLO/incident/policy/checklist/failures Markdown; preserve exact headings, checkboxes, percentages, newline bytes
MOVE=transfer entire real body to Owner; SOURCE same-signature wrapper with dynamic facade; no effect/consumer edits.
TARGETED_NORMAL_CASES=empty/full nested data, failures, invalid numeric exception, UTF-8 byte equality
TEST=`tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` original preimage AST vs final Owner/wrapper on fake inputs; verify output, exception, key/byte order and monkeypatch. If SHA drift or collision, item-specific FIRST_BLOCKER and continue.

### B40-5 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_build_parser` | SOURCE_GIT_BLOB=`7a1ad49ba5941aa661a974a4b6690bade41275eb` (canonical=B at issuance)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_build_parser.py::_build_parser` | TARGET=404 canonical+B, single exclusive Owner
ACTUAL_BODY=Original argparse builder only, no parse_args/main; retain defaults, types, flags and help text
MOVE=transfer entire real body to Owner; SOURCE same-signature wrapper with dynamic facade; no effect/consumer edits.
TARGETED_NORMAL_CASES=default args, --inject-fail, --json, --day, patched argparse, --help
TEST=`tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` original preimage AST vs final Owner/wrapper on fake inputs; verify output, exception, key/byte order and monkeypatch. If SHA drift or collision, item-specific FIRST_BLOCKER and continue.

### B40-6 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_env_bool` | SOURCE_GIT_BLOB=`e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` (canonical=B at issuance)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_env_bool.py::_env_bool` | TARGET=404 canonical+B, single exclusive Owner
ACTUAL_BODY=Read only supplied mapping key; lower/strip; true tokens 1/true/yes/y/on; preserve bool(default) for blank
MOVE=transfer entire real body to Owner; SOURCE same-signature wrapper with dynamic facade; no effect/consumer edits.
TARGETED_NORMAL_CASES=missing/default, whitespace/case, true/false tokens, custom mapping exception
TEST=`tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` original preimage AST vs final Owner/wrapper on fake inputs; verify output, exception, key/byte order and monkeypatch. If SHA drift or collision, item-specific FIRST_BLOCKER and continue.

### B40-7 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_to_float` | SOURCE_GIT_BLOB=`e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` (canonical=B at issuance)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_to_float.py::_to_float` | TARGET=404 canonical+B, single exclusive Owner
ACTUAL_BODY=Try float(value); on any Exception return float(default); preserve both exception points
MOVE=transfer entire real body to Owner; SOURCE same-signature wrapper with dynamic facade; no effect/consumer edits.
TARGETED_NORMAL_CASES=None, invalid, zero, custom __float__, default conversion failure
TEST=`tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` original preimage AST vs final Owner/wrapper on fake inputs; verify output, exception, key/byte order and monkeypatch. If SHA drift or collision, item-specific FIRST_BLOCKER and continue.

### B40-8 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_to_epoch` | SOURCE_GIT_BLOB=`e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` (canonical=B at issuance)
TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_to_epoch.py::_to_epoch` | TARGET=404 canonical+B, single exclusive Owner
ACTUAL_BODY=Numeric/string epoch or ISO datetime/Z, naive timezone UTC, invalid returns None; preserve exception handling
MOVE=transfer entire real body to Owner; SOURCE same-signature wrapper with dynamic facade; no effect/consumer edits.
TARGETED_NORMAL_CASES=None/blank, fractional, ISO offset, invalid, boundary UTC
TEST=`tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` original preimage AST vs final Owner/wrapper on fake inputs; verify output, exception, key/byte order and monkeypatch. If SHA drift or collision, item-specific FIRST_BLOCKER and continue.

## VERIFIED RESERVE — B 6/6 (UNASSIGNED; not Actor discretion)
Verified actual bodies, canonical=B source blob `e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f`, exact RF-063 FILE_COVERAGE, six distinct target 404 canonical+B at issuance. These are NOT B40; do not execute unless next C03 order. Each requires fake/temp targeted parity; no real operations.
1. RF-063 SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_read_env_file@e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` → TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_read_env_file.py::_read_env_file` (404 C+B); BODY=Read-only local env parser, comments/quotes/first '=', **temp fake Path only**; never open real `.env` or secrets; IO/State=none except _read_env_file read-only tmp fixture; fake normal test hypothesis; UNASSIGNED.
2. RF-063 SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_parse_kst_datetime@e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` → TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_parse_kst_datetime.py::_parse_kst_datetime` (404 C+B); BODY=ISO Z/naive/aware KST conversion, invalid None; no clock reads; IO/State=none except _read_env_file read-only tmp fixture; fake normal test hypothesis; UNASSIGNED.
3. RF-063 SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_utc_day@e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` → TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_utc_day.py::_utc_day` (404 C+B); BODY=Call-time `_to_epoch` and UTC YYYY-MM-DD, in-memory; IO/State=none except _read_env_file read-only tmp fixture; fake normal test hypothesis; UNASSIGNED.
4. RF-063 SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_item@e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` → TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_item.py::_item` (404 C+B); BODY=Five-key keyword-only checklist dict projection, key/exception parity; IO/State=none except _read_env_file read-only tmp fixture; fake normal test hypothesis; UNASSIGNED.
5. RF-063 SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_build_markdown@e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` → TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_build_markdown.py::_build_markdown` (404 C+B); BODY=In-memory mock investor Markdown, exact headings/checkboxes/bytes; IO/State=none except _read_env_file read-only tmp fixture; fake normal test hypothesis; UNASSIGNED.
6. RF-063 SOURCE=`scripts/diagnostics/run_m31_mock_investor_exam_check.py::_build_parser@e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` → TARGET=`scripts/diagnostics/run_m31_mock_investor_exam_check_build_parser.py::_build_parser` (404 C+B); BODY=Argparse builder only, no parse/main/market/graph invocation; IO/State=none except _read_env_file read-only tmp fixture; fake normal test hypothesis; UNASSIGNED.

## TEST / DELIVERY / ACCEPTANCE
Normal targeted: `python -m pytest -q tests/test_p15_rf063_20261103_03h_slo_mock_owners.py` must exit 0 on exact final B tree; test all 8 with original pinned preimage AST, including facade patched helper behavior. Record observed EXIT and PASS count separately. Before commit/push verify full staged SOURCE+8 Owner+test manifest, preserve full-root tree; no root-only-tests Git tree. Non-force B push or approved non-force expected-head full-root exact-tree fallback; re-fetch B HEAD/tree and all SOURCE/Owner/test blobs. If push blocked, report PUSH_BLOCKED, never claim remote G1. Each B40-1..8 DONE or exact SOURCE/TARGET/current SHA/FIRST_BLOCKER; continue safe items despite one failure. Report actual START_KST/END_KST/ELAPSED_MIN, HEAD before/after, normal command EXIT/PASS, changed blobs, non-force remote delivery to #12. C04 owns integration/G3; C05 alone RF/STATUS/DONE. No C02/C03/C04/C05/D00/RF/STATUS docs writes; no protected effects.
