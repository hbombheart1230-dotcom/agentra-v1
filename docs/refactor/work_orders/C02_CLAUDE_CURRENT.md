# C02 — Claude A | ORDER_ID=A-20261103-03-C03 | RF-032 PEER | A50 NEW_READY=8/8 | A49 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START — exact remote pins and starting-order preservation
Canonical prewrite `8fe92ce5f9dc3c9bb131a59b7b75d87150bdf59d`; A actor HEAD `74fe2120932e1dcdc367e2769558be3b1d406c77`. Previous C02 blob `a1f11a1487d4366c75e59d9ec20bdffc07bbe714`. A49 [#11 6583712787](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6583712787) final A HEAD delivered 8/8 with normal fresh-clone EXIT=0 PASS184; C04 [#36 6584029322](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6584029322) integrated exact **final** A49 at canonical `8fe92ce5`. Intermediate incomplete `828469ee` was not integrated. A1–A49 already delivered; no reimplementation/retest/recount. If genuinely still working on a prior starting order, finish its safe items before switching; no retroactive cancellation.

First shell `python -m pytest --version`; if unavailable run `python -m pip install --user pytest`, then recheck. Fetch latest **remote** `integration/p1.5:docs/refactor/work_orders/C02_CLAUDE_CURRENT.md` by branch (not cached checkout), log full REMOTE_CANONICAL_HEAD, C02_BLOB_SHA, ORDER_ID in #11. This C02 is the only execution entrypoint; no D00/RF/INDEX reread. Refetch A HEAD, each SOURCE/TARGET at start; if SHA drift, target exists, or ownership overlap, record exact VERIFIED_ALREADY/BLOCKED per item and continue safe items.

## C06 #37 6584273468 — one-time preventive fix, NOT a new A49 code defect
Audit [#37 6584273468](https://github.com/hbombheart1230-dotcom/agentra/issues/37#issuecomment-6584273468) confirmed A49 intermediate push `828469ee` omitted two SOURCE wrappers due to stash/pop unstaging; A self-corrected in non-force final `74fe2120`, canonical exact integration `8fe92ce5` and scoped G1/G2/G3_REUSE accepted. **Do not rerun A49 or recreate it.** For A50 and future orders: immediately before commit run `git status --short` and `git diff --cached --name-only`, compare staged paths against **all SOURCE files + eight exclusive Owner files + targeted test**; after any stash/pop, explicitly re-stage missing SOURCE wrappers. If any missing, fix staging before commit/push. After commit inspect `git show --name-only --format= HEAD` manifest; if any SOURCE/Owner/test missing, correct via non-force follow-up before integration, never claim incomplete commit as G1. After final push refetch exact remote source/Owner/test blobs. In #11 report PREPUSH_STAGED_MANIFEST=COMPLETE/INCOMPLETE, missing paths if any, and FINAL_REMOTE_SHA. This is prevention only, not a new G2/G3 gate or request for repeated tests.

## DONE-FIRST boundary
Latest C05 [#36 6584047694](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6584047694): physical DONE46/93, unresolved47; RF-030 G1 partial/G2 pending/G3 canonical fake smoke pending, C04 owns exact canonical smoke. RF-032 **whole G1 BLOCKED_POLICY** validation-id/Writer/UEF, even though A49 scoped G3_REUSE accepted. A50 is in-memory reporting only and does NOT authorize Writer/UEF, frozen RF-074 oracle, broker, Guard, Step5C, real trading or runtime changes. C05 alone can close RF. C03 will prioritize a different unfinished A-owned RF when a safe owner/consumer scope is validated; A must not self-select.

## A50 — eight individually verified independent pure BODY MOVE items
All SOURCE are `libs/reporting/evaluation/scanner_alignment_root_cause.py@561fbdced4acd99e6c7acb9153e99b0280a977a4` identical on canonical and A at issuance. Eight unique TARGET Owner files are 404 on both complete nontruncated Git trees; RF-032 FILE_COVERAGE and A/B exclusivity checked. Transfer **entire actual body** to single Owner function, keep SOURCE same-signature/default/docstring thin wrapper. Call-time `facade=sys.modules[__name__]` for SOURCE helpers, Mapping and constants; Owner must not import SOURCE. Preserve output identity, exception order, rounding, Markdown strings, monkeypatch and return key ordering. No IO, network, real mode, operational file access or changes to external consumers. Use original A preimage AST and fake-only test `tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` for all eight; normal pytest exit0 once. A49 wrappers in same SOURCE are existing and must not be rewritten or recounted.

### A50-1 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_symbol` | SOURCE_GIT_BLOB=`561fbdced4acd99e6c7acb9153e99b0280a977a4` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_symbol.py::_symbol` | TARGET=404 canonical+A, exclusive Owner
ACTUAL_BODY=Mapping `.get('symbol')` or scalar; str(...).strip, preserve falsy fallback and original type errors
MOVE=full real body → Owner; original signature thin SOURCE wrapper with dynamic facade; no consumer/effect edits.
TARGETED_NORMAL_CASES=dict, None, empty, unicode, custom str
TEST=`tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` original preimage AST parity against wrapper+Owner, fake-only; on drift/collision report item-specific SHA/FIRST_BLOCKER and continue.

### A50-2 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_selected_rank` | SOURCE_GIT_BLOB=`561fbdced4acd99e6c7acb9153e99b0280a977a4` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_selected_rank.py::_selected_rank` | TARGET=404 canonical+A, exclusive Owner
ACTUAL_BODY=Dynamic SOURCE `_mapping`/`_num` for selected_rank and selected_candidate.rank fallback; preserve int conversion and None
MOVE=full real body → Owner; original signature thin SOURCE wrapper with dynamic facade; no consumer/effect edits.
TARGETED_NORMAL_CASES=nested/empty, rank=0, invalid, monkeypatch _mapping/_num
TEST=`tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` original preimage AST parity against wrapper+Owner, fake-only; on drift/collision report item-specific SHA/FIRST_BLOCKER and continue.

### A50-3 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_score_gap` | SOURCE_GIT_BLOB=`561fbdced4acd99e6c7acb9153e99b0280a977a4` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_score_gap.py::_score_gap` | TARGET=404 canonical+A, exclusive Owner
ACTUAL_BODY=Dynamic `_mapping`/`_num` for top1 vs selected score, return 6-decimal rounded difference or None
MOVE=full real body → Owner; original signature thin SOURCE wrapper with dynamic facade; no consumer/effect edits.
TARGETED_NORMAL_CASES=missing/negative/zero, rounding boundary, patched helpers
TEST=`tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` original preimage AST parity against wrapper+Owner, fake-only; on drift/collision report item-specific SHA/FIRST_BLOCKER and continue.

### A50-4 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_outcome_return` | SOURCE_GIT_BLOB=`561fbdced4acd99e6c7acb9153e99b0280a977a4` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_outcome_return.py::_outcome_return` | TARGET=404 canonical+A, exclusive Owner
ACTUAL_BODY=Evaluation realized_outcome.net_return_pct, fallback model.outcome; dynamic mapping/num and missing None
MOVE=full real body → Owner; original signature thin SOURCE wrapper with dynamic facade; no consumer/effect edits.
TARGETED_NORMAL_CASES=nested/fallback/zero, invalid, patched facade
TEST=`tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` original preimage AST parity against wrapper+Owner, fake-only; on drift/collision report item-specific SHA/FIRST_BLOCKER and continue.

### A50-5 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_impact_score` | SOURCE_GIT_BLOB=`561fbdced4acd99e6c7acb9153e99b0280a977a4` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_impact_score.py::_impact_score` | TARGET=404 canonical+A, exclusive Owner
ACTUAL_BODY=Sum negative return values only and round to 4 decimals; preserve original iterable and numeric errors
MOVE=full real body → Owner; original signature thin SOURCE wrapper with dynamic facade; no consumer/effect edits.
TARGETED_NORMAL_CASES=empty, positive, negatives, rounding, custom numeric exceptions
TEST=`tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` original preimage AST parity against wrapper+Owner, fake-only; on drift/collision report item-specific SHA/FIRST_BLOCKER and continue.

### A50-6 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_diagnostic_kind` | SOURCE_GIT_BLOB=`561fbdced4acd99e6c7acb9153e99b0280a977a4` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_diagnostic_kind.py::_diagnostic_kind` | TARGET=404 canonical+A, exclusive Owner
ACTUAL_BODY=Membership in call-time OUTCOME_CONDITIONED_CAUSES or EVIDENCE_GAP_CAUSES, else structural
MOVE=full real body → Owner; original signature thin SOURCE wrapper with dynamic facade; no consumer/effect edits.
TARGETED_NORMAL_CASES=known/unknown, patched constants, custom equality
TEST=`tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` original preimage AST parity against wrapper+Owner, fake-only; on drift/collision report item-specific SHA/FIRST_BLOCKER and continue.

### A50-7 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_largest_cause` | SOURCE_GIT_BLOB=`561fbdced4acd99e6c7acb9153e99b0280a977a4` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_largest_cause.py::_largest_cause` | TARGET=404 canonical+A, exclusive Owner
ACTUAL_BODY=Filter trade_count >0 and excluded root_cause; max by (count, abs negative_impact_pct), return copied dict or {}
MOVE=full real body → Owner; original signature thin SOURCE wrapper with dynamic facade; no consumer/effect edits.
TARGETED_NORMAL_CASES=empty, ties, excluded, invalid numerics, order, input identity
TEST=`tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` original preimage AST parity against wrapper+Owner, fake-only; on drift/collision report item-specific SHA/FIRST_BLOCKER and continue.

### A50-8 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_patch_candidate` | SOURCE_GIT_BLOB=`561fbdced4acd99e6c7acb9153e99b0280a977a4` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_patch_candidate.py::_patch_candidate` | TARGET=404 canonical+A, exclusive Owner
ACTUAL_BODY=Exact seven-way root-cause string to diagnostic recommendation; no action or trading behavior patch
MOVE=full real body → Owner; original signature thin SOURCE wrapper with dynamic facade; no consumer/effect edits.
TARGETED_NORMAL_CASES=all branches, unknown/None, exact string/Unicode output
TEST=`tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` original preimage AST parity against wrapper+Owner, fake-only; on drift/collision report item-specific SHA/FIRST_BLOCKER and continue.

## VERIFIED RESERVE — A 6/6 (UNASSIGNED, not Actor discretion)
Actual bodies read, RF-032 FILE_COVERAGE and exact canonical=A SOURCE `libs/reporting/evaluation/episode_scanner_review.py@5bd42ffafd07612290dc4138e149d2e627590d60`; all six exclusive targets 404 on canonical+A full trees. In-memory only, no effect or IO; fake-only parity with patched facade helpers. Do NOT execute until next C03 order.
1. RF-032 SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_number@5bd42ffafd07612290dc4138e149d2e627590d60` → TARGET=`libs/reporting/evaluation/episode_scanner_review_number.py::_number` (404 C+A); BODY=TypeError/ValueError only float-or-None, preserve value in (None,'') check; IO/State=none, fake normal parity hypothesis; UNASSIGNED.
2. RF-032 SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_mapping@5bd42ffafd07612290dc4138e149d2e627590d60` → TARGET=`libs/reporting/evaluation/episode_scanner_review_mapping.py::_mapping` (404 C+A); BODY=Mapping identity-or-empty, no copy; IO/State=none, fake normal parity hypothesis; UNASSIGNED.
3. RF-032 SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_checkpoint_return@5bd42ffafd07612290dc4138e149d2e627590d60` → TARGET=`libs/reporting/evaluation/episode_scanner_review_checkpoint_return.py::_checkpoint_return` (404 C+A); BODY=Nested shadow_forward_outcome.checkpoints status observed and dynamic `_mapping/_number`; IO/State=none, fake normal parity hypothesis; UNASSIGNED.
4. RF-032 SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_epoch@5bd42ffafd07612290dc4138e149d2e627590d60` → TARGET=`libs/reporting/evaluation/episode_scanner_review_epoch.py::_epoch` (404 C+A); BODY=shadow_forward_base.baseline_epoch int-or-zero with dynamic helpers; IO/State=none, fake normal parity hypothesis; UNASSIGNED.
5. RF-032 SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_setup_key@5bd42ffafd07612290dc4138e149d2e627590d60` → TARGET=`libs/reporting/evaluation/episode_scanner_review_setup_key.py::_setup_key` (404 C+A); BODY=entry_lane_observation subtype_v2/subtype/primary_lane/reason/unknown fallback; IO/State=none, fake normal parity hypothesis; UNASSIGNED.
6. RF-032 SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_day@5bd42ffafd07612290dc4138e149d2e627590d60` → TARGET=`libs/reporting/evaluation/episode_scanner_review_day.py::_day` (404 C+A); BODY=call-time `candidate_day(row)` fallback row.day, strip hyphens and require 8 digits; IO/State=none, fake normal parity hypothesis; UNASSIGNED.

## ACCEPTANCE / #11
Execute A50-1..8 or report exact per-item SOURCE/TARGET/current SHA/FIRST_BLOCKER. Do not stop after first PASS or early push. Normal targeted `python -m pytest -q tests/test_p15_rf032_20261103_03h_scanner_alignment_owners.py` EXIT=0, record observed PASS count and actual START_KST/END_KST/ELAPSED_MIN, A HEAD before/after, prepush staged manifest, SOURCE pre/post + eight Owner + test Git blobs, non-force remote SHA and final refetch. Git authentication failure blocks only push; continue safe items and report PUSH_BLOCKED. Do not force push/history rewrite. C04 owns selective integration/G3, C05 RF/STATUS/DONE; no C01/C03/C04/C05/D00/RF/STATUS writes.
