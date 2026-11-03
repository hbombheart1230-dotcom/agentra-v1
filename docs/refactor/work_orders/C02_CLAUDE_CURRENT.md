# C02 — Claude A | ORDER_ID=A-20261103-09-C03 | RF-032 PEER | A56 NEW_READY=8/8 | A55 REMOTE_DONE=8/8 | RESERVE_NOT_VERIFIED=0/6

## 2026-11-03 20:00 C03 evidence correction — reserve count only (not a new order)
A56-1..8 were completed at A remote `a0149439392300f94876e553e11d99fec053d1d5` per #11 6593666681. Preserve ORDER_ID and all existing item instructions; do not repeat them. The six `cumulative_improvement_review` reserve candidates were not independently reverified against current SOURCE blob, exclusive Owner, TARGET 404, IO/caller safety and targeted normal test, so **RESERVE_VERIFIED=0/6; RESERVE_NOT_VERIFIED** until C03 validates each. They are not assigned and Claude A must not self-select or execute them. This header correction has **GATE_IMPACT=NO**, **NEW_BODY_MOVES=0**, **RF_DONE_DELTA=0**; it is not G1/G2/G3 evidence. Future C03 must issue a separately verified next single order. Existing A49 prepush staged SOURCE+Owner+test manifest safeguard remains mandatory; no A49 re-test.

## 2026-11-03 역할별 Agentra 스킬 적용
`agentra-rf-executor` 실행 체크리스트를 적용하고 `agentra-contract-guard`로 변경 대상의 Owner/안전 경계를 확인한다. 스킬은 본 C02 주문 밖 신규 과제를 허용하지 않으며, 자동 로딩이 확인되지 않으면 `.agents/skills/<skill-name>/SKILL.md`를 참고 자료로만 사용한다.

---

## 2026-11-03 LEAD CORRECTION — A execution accountability (D00 subordinate)
Complete any already-started A56 safe items without retroactive cancellation. For every item explicitly report whether it resolves the RF's whole FIRST_UNMET gate (`GATE_IMPACT=YES/NO`). RF-032 evaluation-only BODY MOVEs do not lift validation-id/Writer/UEF policy HOLD and are not whole RF DONE. Preserve frozen oracles and all safety boundaries; if an item is unsafe, already implemented, or has drift, report exact blocker and continue remaining safe items. Post verified actor remote SHA and targeted exit to #11; do not self-assign, repeat old PASS, or claim G3/DONE.

---

## START — protect in-flight work, remote preflight
C03 verified canonical `3b859aa4facd4d38acdad3fc62507261bf48ae42`, A branch `2d48eb29c813353eddb8a9e47de1ae5f9787fa1b`, old C02 blob `927850ca3ef04a54f4a60c63c785eb83c879fc42`. A55 #11 6590953654 delivered 8/8 at A remote 2d48eb29, normal targeted EXIT=0 PASS=302, C04 #36 6591335590 selected exact 13/13 at integration e6319b92, C05 #36 6591430488 physical DONE 46/93; do not redo/recount A55 or older. If a prior starting order is genuinely in progress, finish its safe items first.

First shell `python -m pytest --version`; if absent `python -m pip install --user pytest`, recheck. Fetch this exact file from remote `integration/p1.5`, report full canonical HEAD, C02 blob, ORDER_ID, A HEAD to #11. This file is sole execution entrypoint; do NOT reread D00/RF/INDEX/SKILL or self-select RF. Before edits refetch each pinned SOURCE and each TARGET on A; if SHA drift, existing TARGET, or ownership collision, item-specific VERIFIED_ALREADY/BLOCKED with exact SHA/FIRST_BLOCKER and continue the remaining safe items. Code/tests only on A branch; non-force push. C03's new order never retroactively cancels a previously started order.

## DONE-FIRST boundaries
RF-030 PENDING G1 PARTIAL (15/16 KEEP, RF-074 test/frozen Owner read-only KEEP), canonical fake smoke G2/G3 pending C04/C05. RF-032 whole G1 BLOCKED_POLICY validation-id/Writer/UEF authorization, not lifted by this read-only work. A `operator_visibility.py` preimage differs canonical; do NOT change it or RF-074 test/frozen oracle. No protected Writer/UEF/Guard/Step5C, broker/trade, real env/network, operational files/DB/state, frozen test/CI edits. All current A56 targets verified 404 on canonical+A, SOURCE canonical==A at issuance, RF-032 A-exclusive FILE_COVERAGE. These eight are real BODY MOVEs, not RF DONE.

## A56 — eight independently verified BODY MOVEs
For every item: move the **entire real computation body** to exactly one TARGET Owner; retain original SOURCE public/private signature, defaults, keyword-only parameters and docstring as thin wrapper delegating with call-time `sys.modules[__name__]` facade. New Owner may accept keyword-only facade; do not import SOURCE at Owner module import time. Preserve dynamic helper monkeypatch, identity, generator laziness, order, exceptions, JSON/Markdown bytes, and old callers. AST-bounded edits, no duplicate body. Each item must be DONE or evidence-backed BLOCKED; continue other safe items after a failure.

### A56-1 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::build_full_chain_component_review` | SOURCE_BLOB=`7706d3567dc27286b3c63e6344193401e28a944b` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/full_chain_component_review_build_full_chain_component_review.py::build_full_chain_component_review` | TARGET=404 canonical+A
BODY_AND_TARGETED_NORMAL=read-only evaluation aggregation; fake shadow/model/cost/profile/env/entry/exit helpers; preserve ordered component decisions, thresholds, dict keys and no real filesystem/env access. Verify original preimage versus wrapper+Owner using fake-only parity, including errors/monkeypatch and no protected effects.

### A56-2 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/historical_prior.py::_day_from_trade_dir` | SOURCE_BLOB=`a9a223da81e5c29088004d8d5db0c391f8cf4373` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/historical_prior_day_from_trade_dir.py::_day_from_trade_dir` | TARGET=404 canonical+A
BODY_AND_TARGETED_NORMAL=Path.parts scan for first trades/day; fake paths, empty/multiple trades segments, exact fallback. Verify original preimage versus wrapper+Owner using fake-only parity, including errors/monkeypatch and no protected effects.

### A56-3 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/historical_prior.py::_net_return` | SOURCE_BLOB=`a9a223da81e5c29088004d8d5db0c391f8cf4373` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/historical_prior_net_return.py::_net_return` | TARGET=404 canonical+A
BODY_AND_TARGETED_NORMAL=realized_outcome.net_return_pct float; only TypeError/ValueError caught; None, missing, 0, malformed, inf parity. Verify original preimage versus wrapper+Owner using fake-only parity, including errors/monkeypatch and no protected effects.

### A56-4 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/historical_prior.py::_group_metrics` | SOURCE_BLOB=`a9a223da81e5c29088004d8d5db0c391f8cf4373` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/historical_prior_group_metrics.py::_group_metrics` | TARGET=404 canonical+A
BODY_AND_TARGETED_NORMAL=defaultdict grouping, unknown fallback, sorted key iteration, call-time performance_metrics; fake iterable, key order and exception parity. Verify original preimage versus wrapper+Owner using fake-only parity, including errors/monkeypatch and no protected effects.

### A56-5 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/historical_prior.py::summarize_historical_prior` | SOURCE_BLOB=`a9a223da81e5c29088004d8d5db0c391f8cf4373` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/historical_prior_summarize_historical_prior.py::summarize_historical_prior` | TARGET=404 canonical+A
BODY_AND_TARGETED_NORMAL=in-memory eligible returns/integrity counters and 4 breakdowns, datetime.now seam, generated_at, error slice 50, Q9 frozen guardrails; fake rows only. Verify original preimage versus wrapper+Owner using fake-only parity, including errors/monkeypatch and no protected effects.

### A56-6 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/historical_prior.py::render_historical_prior_markdown` | SOURCE_BLOB=`a9a223da81e5c29088004d8d5db0c391f8cf4373` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/historical_prior_render_historical_prior_markdown.py::render_historical_prior_markdown` | TARGET=404 canonical+A
BODY_AND_TARGETED_NORMAL=Markdown only; missing coverage/performance, nonempty breakdowns, numeric formatting, exact UTF-8/newline bytes. Verify original preimage versus wrapper+Owner using fake-only parity, including errors/monkeypatch and no protected effects.

### A56-7 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/historical_prior.py::iter_historical_trade_dirs` | SOURCE_BLOB=`a9a223da81e5c29088004d8d5db0c391f8cf4373` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/historical_prior_iter_historical_trade_dirs.py::iter_historical_trade_dirs` | TARGET=404 canonical+A
BODY_AND_TARGETED_NORMAL=read-only Path rglob of lifecycle_bundle.json and date bounds; fake Path only, sorted dedup parents, no actual report IO. Verify original preimage versus wrapper+Owner using fake-only parity, including errors/monkeypatch and no protected effects.

### A56-8 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/loss_decomposition.py::_load_trade_models` | SOURCE_BLOB=`09352162fa51641be30763bf9719a126da5ba3bf` (canonical=A at issuance)
TARGET=`libs/reporting/evaluation/loss_decomposition_load_trade_models.py::_load_trade_models` | TARGET=404 canonical+A
BODY_AND_TARGETED_NORMAL=read-only day iteration, iter_trade_dirs/build_q9_trade_read_model call-time seams; fake day/path/model objects, order and error parity. Verify original preimage versus wrapper+Owner using fake-only parity, including errors/monkeypatch and no protected effects.

## VERIFIED UNASSIGNED RESERVE — A 6/6
All six distinct real SOURCE bodies canonical=A at blob `a2f64696546cb729afd7c5b89d9d1c1e06edeac7`, RF-032 exclusive file, TARGET 404 on canonical+A, read-only/fake-only tests; not authorized to execute until next C03 order. Do not count as G1/G2.
1. SOURCE=`libs/reporting/evaluation/cumulative_improvement_review.py::_read_json@a2f64696546cb729afd7c5b89d9d1c1e06edeac7` → TARGET=`libs/reporting/evaluation/cumulative_improvement_review_read_json.py::_read_json` (404 C+A); TEST/SAFETY=read_text UTF-8-sig and dict-only JSON; fake Path and json; no live IO.
2. SOURCE=`libs/reporting/evaluation/cumulative_improvement_review.py::_strategist_weighting_review@a2f64696546cb729afd7c5b89d9d1c1e06edeac7` → TARGET=`libs/reporting/evaluation/cumulative_improvement_review_strategist_weighting_review.py::_strategist_weighting_review` (404 C+A); TEST/SAFETY=read-only sorted baseline day dirs and horizon A/B deltas; fake dirs and _read_json; no live IO.
3. SOURCE=`libs/reporting/evaluation/cumulative_improvement_review.py::_rank_row@a2f64696546cb729afd7c5b89d9d1c1e06edeac7` → TARGET=`libs/reporting/evaluation/cumulative_improvement_review_rank_row.py::_rank_row` (404 C+A); TEST/SAFETY=in-memory rank/horizon next match, first-match and Mapping identity; no live IO.
4. SOURCE=`libs/reporting/evaluation/cumulative_improvement_review.py::_candidate_rows@a2f64696546cb729afd7c5b89d9d1c1e06edeac7` → TARGET=`libs/reporting/evaluation/cumulative_improvement_review_candidate_rows.py::_candidate_rows` (404 C+A); TEST/SAFETY=in-memory episode/reentry/post-reclaim/strategist aggregation; fake _rank_row; no live IO.
5. SOURCE=`libs/reporting/evaluation/cumulative_improvement_review.py::build_cumulative_improvement_review@a2f64696546cb729afd7c5b89d9d1c1e06edeac7` → TARGET=`libs/reporting/evaluation/cumulative_improvement_review_build_cumulative_improvement_review.py::build_cumulative_improvement_review` (404 C+A); TEST/SAFETY=evaluation-only aggregation; fake cost profile/loader/forward outcomes, no production IO; no live IO.
6. SOURCE=`libs/reporting/evaluation/cumulative_improvement_review.py::render_cumulative_improvement_review@a2f64696546cb729afd7c5b89d9d1c1e06edeac7` → TARGET=`libs/reporting/evaluation/cumulative_improvement_review_render_cumulative_improvement_review.py::render_cumulative_improvement_review` (404 C+A); TEST/SAFETY=in-memory Markdown exact bytes, missing fields and formatting; no live IO.

## TEST / DELIVERY / ACCEPTANCE
New test `tests/test_p15_rf032_20261103_09h_historical_full_chain_owners.py` was 404 canonical+A. Implement pinned preimage AST-to-Owner/wrapper fake parity for all eight, with read-only fake Paths, patched external loaders/profile/env, exact signatures/defaults/keyword-only, call-time monkeypatch, return identity, output ordering, exceptions, Markdown bytes, and no real IO. `python -m py_compile` changed SOURCE+Owner+test EXIT0, then `python -m pytest -q tests/test_p15_rf032_20261103_09h_historical_full_chain_owners.py` normal EXIT0 required; report actual PASS count, no invented tests. Prepush `git status --short`, staged manifest SOURCE 3 + Owner 8 + test 1 = **12 paths**, `git diff --cached --name-only` and commit path names; after stash/pop recheck. Non-force A push; re-fetch final remote full-root tree and all 12 blobs. Report per A56-1..8 DONE/BLOCKED, SOURCE before/after, Owner/test SHA, normal command EXIT/PASS, actual START_KST/END_KST/ELAPSED_MIN, A remote SHA to #11. C04 only integration/G3; C05 only RF/STATUS/DONE. No docs/RF/STATUS/CI/operations writes.
