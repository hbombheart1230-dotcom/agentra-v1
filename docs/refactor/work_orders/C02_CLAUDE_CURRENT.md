# C02 — Claude A | ORDER_ID=A-20261103-04-C03 | RF-032 PEER | A51 NEW_READY=8/8 | A50 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START — remote exact pins, starting-order preservation
Canonical PREWRITE=`4751dd928cd12c84c95485b66a8a6f199a6d6188`; actor A remote HEAD=`d891f7a4caa2980aa11b9acb45b408170b9cc793`; previous C02 blob=`d69f6f38f8e26657db23bcaa43dc9428cf926330`. A50 [#11 6584947389](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6584947389) delivered eight actual BODY MOVEs at A `d891f7a4`, normal targeted 215 PASS EXIT0, full staged manifest 10/10; C04 [#36 6585230784](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6585230784) selected exact 10/10 blobs at code integration `6cc3ae11`, final canonical `4751dd92`. **Do not rerun/recount A50**. If a prior starting order is genuinely in progress, finish safe items before switching; no retroactive cancellation.

First shell `python -m pytest --version`; if unavailable `python -m pip install --user pytest`, then recheck. Fetch latest **remote** `integration/p1.5:docs/refactor/work_orders/C02_CLAUDE_CURRENT.md` by branch; log full canonical HEAD, C02 blob and ORDER_ID in #11. This file alone is execution entrypoint: no D00/RF/INDEX reread, no self-selected RF. At start refetch A HEAD and exact SOURCE/TARGET; drift, pre-existing target or ownership collision = item-specific VERIFIED_ALREADY/BLOCKED with actual SHA; continue other safe items.

## DONE-FIRST gate separation
C05 [#36 6585332331](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6585332331) physical DONE46/93, unresolved47; **RF-030 PENDING** has G1 partial (RF-074 frozen owner boundary), G2/G3 exact canonical fake smoke pending, owned by C03/C04/C05, **not A51**. **RF-032 whole G1 BLOCKED_POLICY** validation-id/Writer/UEF. A51 is safe in-memory evaluation BODY MOVE only, cannot clear Writer/UEF or authorize real effects. C03 verified RF-031/RF-050 already DONE; other unresolved A RF lack a verified 8-item safe ready set in this run. A51 uses independently verified RF-032 pure scope without pretending RF DONE; C03 will switch to a closeout-ready unresolved A RF when exact safe Owner/source evidence is ready.

## A51 — eight independent real BODY MOVE items
SOURCE for all eight = `libs/reporting/evaluation/episode_scanner_review.py@5bd42ffafd07612290dc4138e149d2e627590d60` exact canonical==A HEAD at issue. RF-032 FILE_COVERAGE and source bodies independently inspected. All eight TARGET Owner files individually 404 on canonical and A at issuance; A/B cross-owner overlap zero. Move entire original calculation body into one new Owner function of same name under `libs/reporting/evaluation/`; leave same-signature/default/docstring thin SOURCE wrapper delegating to Owner with `facade=sys.modules[__name__]` (import sys if absent). Owner must **not import SOURCE**; resolve original SOURCE globals/helpers through facade at call-time, including `Mapping, defaultdict, SCANNER_HORIZONS, candidate_day, _mapping, _number, _checkpoint_return, _epoch, _setup_key, _day, _rank_bucket` where used. Preserve byte/order/identity/exceptions/monkeypatch. No IO, network, real-mode, report writing or protected Writer/UEF/Guard/Step5C. Test each item using original pinned A preimage AST vs final wrapper+Owner in-memory fake parity in **one new targeted test** `tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py` (404 canonical+A at issuance); normal `python -m pytest -q tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py` EXIT0 required on final A tree. No -O/full suite/hosted CI gate.

### A51-1 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_number` | SOURCE_BLOB=`5bd42ffafd07612290dc4138e149d2e627590d60`
TARGET=`libs/reporting/evaluation/episode_scanner_review_number.py::_number` | TARGET=404 canonical+A at issuance, exclusive A Owner
ACTUAL_BODY=float-or-None; preserve membership check value in (None, '') and TypeError/ValueError-only catch
MOVE=full calculation into Owner, SOURCE exact-signature thin facade wrapper; no other consumer/effect changes.
TARGETED_NORMAL_CASES=None, empty, 0, numeric string, custom __eq__/__float__ exception; fake original AST output/exception/identity/monkeypatch parity; TEST=`tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py`. If blocked, report item SHA/FIRST_BLOCKER and continue.

### A51-2 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_mapping` | SOURCE_BLOB=`5bd42ffafd07612290dc4138e149d2e627590d60`
TARGET=`libs/reporting/evaluation/episode_scanner_review_mapping.py::_mapping` | TARGET=404 canonical+A at issuance, exclusive A Owner
ACTUAL_BODY=Mapping identity or empty dict; no copying; preserve isinstance semantics
MOVE=full calculation into Owner, SOURCE exact-signature thin facade wrapper; no other consumer/effect changes.
TARGETED_NORMAL_CASES=dict, mapping proxy, nonmapping, input identity; fake original AST output/exception/identity/monkeypatch parity; TEST=`tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py`. If blocked, report item SHA/FIRST_BLOCKER and continue.

### A51-3 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_checkpoint_return` | SOURCE_BLOB=`5bd42ffafd07612290dc4138e149d2e627590d60`
TARGET=`libs/reporting/evaluation/episode_scanner_review_checkpoint_return.py::_checkpoint_return` | TARGET=404 canonical+A at issuance, exclusive A Owner
ACTUAL_BODY=shadow_forward_outcome.checkpoints[horizon] observed-only; call-time facade._mapping and facade._number
MOVE=full calculation into Owner, SOURCE exact-signature thin facade wrapper; no other consumer/effect changes.
TARGETED_NORMAL_CASES=observed/nonobserved, nested absent, malformed return, monkeypatch helpers; fake original AST output/exception/identity/monkeypatch parity; TEST=`tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py`. If blocked, report item SHA/FIRST_BLOCKER and continue.

### A51-4 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_epoch` | SOURCE_BLOB=`5bd42ffafd07612290dc4138e149d2e627590d60`
TARGET=`libs/reporting/evaluation/episode_scanner_review_epoch.py::_epoch` | TARGET=404 canonical+A at issuance, exclusive A Owner
ACTUAL_BODY=shadow_forward_base.baseline_epoch via facade._mapping/_number then int(value or 0)
MOVE=full calculation into Owner, SOURCE exact-signature thin facade wrapper; no other consumer/effect changes.
TARGETED_NORMAL_CASES=zero, negative, None, float truncation, patched helpers; fake original AST output/exception/identity/monkeypatch parity; TEST=`tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py`. If blocked, report item SHA/FIRST_BLOCKER and continue.

### A51-5 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_setup_key` | SOURCE_BLOB=`5bd42ffafd07612290dc4138e149d2e627590d60`
TARGET=`libs/reporting/evaluation/episode_scanner_review_setup_key.py::_setup_key` | TARGET=404 canonical+A at issuance, exclusive A Owner
ACTUAL_BODY=entry_lane_observation subtype_v2/subtype/primary_lane/reason/unknown fallback; exact str conversion
MOVE=full calculation into Owner, SOURCE exact-signature thin facade wrapper; no other consumer/effect changes.
TARGETED_NORMAL_CASES=empty/zero/unicode, fallback precedence, custom string; fake original AST output/exception/identity/monkeypatch parity; TEST=`tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py`. If blocked, report item SHA/FIRST_BLOCKER and continue.

### A51-6 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_day` | SOURCE_BLOB=`5bd42ffafd07612290dc4138e149d2e627590d60`
TARGET=`libs/reporting/evaluation/episode_scanner_review_day.py::_day` | TARGET=404 canonical+A at issuance, exclusive A Owner
ACTUAL_BODY=facade.candidate_day(row) fallback row.day; strip hyphens; require eight digits
MOVE=full calculation into Owner, SOURCE exact-signature thin facade wrapper; no other consumer/effect changes.
TARGETED_NORMAL_CASES=valid/invalid day, unicode digits, patched candidate_day, exception parity; fake original AST output/exception/identity/monkeypatch parity; TEST=`tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py`. If blocked, report item SHA/FIRST_BLOCKER and continue.

### A51-7 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_rank_bucket` | SOURCE_BLOB=`5bd42ffafd07612290dc4138e149d2e627590d60`
TARGET=`libs/reporting/evaluation/episode_scanner_review_rank_bucket.py::_rank_bucket` | TARGET=404 canonical+A at issuance, exclusive A Owner
ACTUAL_BODY=rank==1, 2..3, >=4, otherwise unknown; preserve comparison/TypeError behavior
MOVE=full calculation into Owner, SOURCE exact-signature thin facade wrapper; no other consumer/effect changes.
TARGETED_NORMAL_CASES=negative/zero/1/2/3/4, non-int exception; fake original AST output/exception/identity/monkeypatch parity; TEST=`tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py`. If blocked, report item SHA/FIRST_BLOCKER and continue.

### A51-8 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/episode_scanner_review.py::_episode_representatives` | SOURCE_BLOB=`5bd42ffafd07612290dc4138e149d2e627590d60`
TARGET=`libs/reporting/evaluation/episode_scanner_review_episode_representatives.py::_episode_representatives` | TARGET=404 canonical+A at issuance, exclusive A Owner
ACTUAL_BODY=group by day/symbol/setup; sorted candidate epoch/rank; gap-based episode indexing; score_breakdown, sources, horizons returns, exact episode_id/output order and one-shot consumption; call-time facade helper lookups
MOVE=full calculation into Owner, SOURCE exact-signature thin facade wrapper; no other consumer/effect changes.
TARGETED_NORMAL_CASES=duplicate episode, boundary gap, zero epoch, invalid rank, monkeypatch facade helpers, generator, ordering; fake original AST output/exception/identity/monkeypatch parity; TEST=`tests/test_p15_rf032_20261103_04h_episode_scanner_owners.py`. If blocked, report item SHA/FIRST_BLOCKER and continue.
## VERIFIED RESERVE — A 6/6, UNASSIGNED (not actor discretion)
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py@dc1e6c5017e537057864be84b659f0803efa0a8c` canonical==A; RF-032 FILE_COVERAGE; six actual pure function bodies inspected. Each distinct TARGET 404 on both canonical and A, no IO/State/real trading. Targeted future fake-only AST parity needed; **not assigned in A51**, do not execute without next C03 order.
1. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_number@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_number.py::_number` (404 canonical+A); BODY=float-or-None, TypeError/ValueError only, no IO; preserve use-time globals, exact signature/exception/order, fake-only normal test proposed; UNASSIGNED.
2. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_behavior_metric_eligible@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_behavior_metric_eligible.py::_behavior_metric_eligible` (404 canonical+A); BODY=defect set intersection with BEHAVIOR_METRIC_EXCLUSION_DEFECTS; no IO; preserve use-time globals, exact signature/exception/order, fake-only normal test proposed; UNASSIGNED.
3. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_topk_metric@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_topk_metric.py::_topk_metric` (404 canonical+A); BODY=topk rows top_k/horizon first-match copy; no IO; preserve use-time globals, exact signature/exception/order, fake-only normal test proposed; UNASSIGNED.
4. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_classify_root_cause@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_classify_root_cause.py::_classify_root_cause` (404 canonical+A); BODY=in-memory scanner/attribution/entry/exit thresholds and ordered status/evidence; no IO; preserve use-time globals, exact signature/exception/order, fake-only normal test proposed; UNASSIGNED.
5. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_role_metrics@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_role_metrics.py::_role_metrics` (404 canonical+A); BODY=shadow role/horizon filtered cost-adjusted metrics, candidate_day and performance_metrics call-time; no IO; preserve use-time globals, exact signature/exception/order, fake-only normal test proposed; UNASSIGNED.
6. RF-032 SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_paired_role_deltas@dc1e6c5017e537057864be84b659f0803efa0a8c` → TARGET=`libs/reporting/evaluation/full_chain_component_review_paired_role_deltas.py::_paired_role_deltas` (404 canonical+A); BODY=window-role grouping and average/positive delta metrics; no IO; preserve use-time globals, exact signature/exception/order, fake-only normal test proposed; UNASSIGNED.

## C06 prevention already forwarded — do not repeat A49
[#37 6584273468](https://github.com/hbombheart1230-dotcom/agentra/issues/37#issuecomment-6584273468) A49 intermediate omitted SOURCE wrappers, self-corrected final A49; no reimplementation/retest. A50 reported PREPUSH_STAGED_MANIFEST COMPLETE 10/10 and final remote 10/10 [#11 6584947389](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6584947389). For A51, before commit run `git status --short` and `git diff --cached --name-only` to confirm SOURCE+8 Owner+test all staged; re-stage after stash/pop; inspect `git show --name-only --format= HEAD` and final remote blobs after non-force push. Report PREPUSH_STAGED_MANIFEST and final SHA in #11. No new completion gate beyond integrity, G1/G2/G3 unchanged.

## ACCEPTANCE / #11
A51-1..8 each DONE with SOURCE before/after+Owner/test blobs or BLOCKED with actual SOURCE/TARGET/SHA/FIRST_BLOCKER; one failure does not stop independent safe items. Normal targeted EXIT=0 and observed PASS count on exact final A tree, START_KST/END_KST/ELAPSED_MIN actual, A HEAD before/after, staged 10-path manifest, non-force remote SHA, final refetch all 10 paths. Push/auth failure blocks only remote G1, not other safe items. No force/history rewrite. C04 only selected integration/G3, C05 only RF/STATUS/DONE. A edits code/tests on A branch only, no C01/C03/C04/C05/D00/RF/STATUS/operations.
