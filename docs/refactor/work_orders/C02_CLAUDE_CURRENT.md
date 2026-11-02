# C02 — Claude A | ORDER_ID=A-20261103-06-C03 | RF-032 PEER | A53 NEW_READY=8/8 | A52 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START — authoritative single work order
Canonical PREWRITE=`437a3f201e9cb45712ee7f52188981ef4719fd46`; actor A HEAD=`20345954d9c422bf1a15718cfb0e0e9f5e4857dc`; prior C02 blob=`3d6f0adf4cee1998c860acb2c61f329c5a9b9a64`. A52 [#11 6587485709](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6587485709) final remote 20345954, eight real BODY MOVEs, normal fresh-clone `tests/test_p15_rf032_20261103_05h_full_chain_component_owners.py` EXIT=0/PASS=248. C04 [#36 6587876887](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6587876887) exact 10/10 integration at canonical 437a3f20; C05 [#36 6588012922](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6588012922) whole RF-032 remains G1 BLOCKED_POLICY. Do NOT repeat A52 or earlier; do not count previous PASS as new G2. If an earlier starting order was actually in progress, finish its safe items first; no retroactive cancellation.

First shell: `python -m pytest --version`; if unavailable `python -m pip install --user pytest` and recheck. Fetch `integration/p1.5:docs/refactor/work_orders/C02_CLAUDE_CURRENT.md` directly from remote and report canonical HEAD, full C02 Git blob, ORDER_ID, actor HEAD in #11. C02 is sole work entrypoint; do not reread D00/RF/INDEX/skill. Before each item refetch exact A SOURCE and TARGET; if SOURCE differs or TARGET already exists, mark that item VERIFIED_ALREADY/BLOCKED with exact SHA and continue remaining safe items. Code/test edits only on A branch, non-force push.

## DONE-FIRST / safety and ownership
Latest C05 physical stages PENDING38/DEV7/PEER2/LEAD0/DONE46 (47 unresolved), NEW_RF_DONE=0. RF-030 is higher whole-RF closeout candidate but its canonical G2/G3 and RF-074 owner boundary belong C04/C05, NOT A53. RF-063 B40 and resolver closure belong B/C04; RF-032 whole validation-id/Writer/UEF G1 BLOCKED_POLICY. A53 is **only pure evaluation body extraction**, NOT whole RF DONE and does not authorize Writer, UEF, runtime, trading or behavior changes. C03 found no separately verified 8-item A closeout-safe set in another unresolved RF at this prewrite; hence 8 safe RF-032 pure items supplied under D00 continuity, while G3/DONE blockers stay explicit. RF-035/044 already DONE are not a substitute.

Two exact canonical==A SOURCE blobs verified at issuance:
- `libs/reporting/evaluation/full_chain_component_review.py@1d44c646540adffd676ea16489b6212d8bbf5e97` (RF-032, A exclusive).
- `libs/reporting/evaluation/scanner_alignment_root_cause.py@2a595f8d1025fd6bcc31033d256e7f1766c57ab0` (RF-032, A exclusive).
All eight unique TARGET paths below and test `tests/test_p15_rf032_20261103_06h_full_chain_alignment_owners.py` were independently 404 on BOTH canonical and A at issuance. Every SOURCE function below has a real still-inline computation/render body; no prior Owner/wrapper for these functions. Preserve original exact signature/defaults/docstring, source public import path, exception types/messages, ordering, byte output, identity and call-time monkeypatch. Transfer **entire actual calculation body** to exactly one new Owner module per item; SOURCE becomes thin delegate, no duplicate body. Owner takes `facade` keyword and uses source module `sys.modules[__name__]` passed at CALL time for dynamic helpers/constants; Owner never imports SOURCE. Keep existing A52 wrappers/imports intact. Tests fake/temp in memory only, never invoke build/write filesystem, live data, broker, Guard, Step5C, UEF, RunLab, operations or real trading.

One new targeted normal test for changed scope: `python -m pytest -q tests/test_p15_rf032_20261103_06h_full_chain_alignment_owners.py`, EXIT=0 on exact final A tree. For each item include original pinned SOURCE AST body vs final facade+Owner fake parity, wrapper structure (real original body removed), helper patch seam, exceptions/order/bytes. Do not require -O/full-suite/full peer/hosted CI. A blocked item must not stop the other seven.

### A53-1 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_q9_role_row@1d44c646540adffd676ea16489b6212d8bbf5e97`
TARGET=`libs/reporting/evaluation/full_chain_component_review_q9_role_row.py::_q9_role_row` (404 C+A; A exclusive).
BODY=select first truthy `q9_selected` for B_STRATEGIST_RANKED, otherwise `min(rows,key=int(float(rank or 999)),default={})`; preserve ORIGINAL row object identity, tie/invalid-rank errors. Wrapper same signature and facade call-time. TEST=empty, selected-first, equal rank, malformed rank, identity and original AST parity.

### A53-2 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_decision_window_attribution@1d44c646540adffd676ea16489b6212d8bbf5e97`
TARGET=`libs/reporting/evaluation/full_chain_component_review_decision_window_attribution.py::_decision_window_attribution` (404 C+A).
BODY=128-line in-memory Q9 decision grouping, horizon loops, strategist/refresh/commander comparisons, day sets, cost and rate rounding; `defaultdict`, `HORIZONS`, `_q9_decision_candidate_rows`, `_q9_role_row`, `_checkpoint_return`, `candidate_day` resolved through facade at use-time. No live loaders. TEST=empty/duplicate decisions, missing checkpoints, no-trade, cost/rounding, horizon order, patched helpers, AST parity.

### A53-3 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_attribution_component@1d44c646540adffd676ea16489b6212d8bbf5e97`
TARGET=`libs/reporting/evaluation/full_chain_component_review_attribution_component.py::_attribution_component` (404 C+A).
BODY=65-line strategist/commander `+30m` evidence/count/day thresholds and decision dict; preserve `_number`, `DIRECTIONAL_MIN_OBSERVATIONS`, `DIRECTIONAL_MIN_DAYS`, `DecisionClass`, dict key order and `availability` semantics via facade. TEST=empty/low/high count, exact thresholds, missing/negative delta, patched constants, AST parity.

### A53-4 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_scanner_decision@1d44c646540adffd676ea16489b6212d8bbf5e97`
TARGET=`libs/reporting/evaluation/full_chain_component_review_scanner_decision.py::_scanner_decision` (404 C+A).
BODY=54-line top_pick/runner_up 30m selection, pair count/day materiality, relative/absolute decision and dict projection; facade resolves `DIRECTIONAL_MIN_*`, `MIN_MATERIAL_RANKING_DELTA_PCT`, `MIN_POSITIVE_RANKING_DELTA_RATE`, `DecisionClass`. TEST=zero/missing/threshold boundary, patched constants, float errors, AST parity.

### A53-5 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::_unavailable_component@1d44c646540adffd676ea16489b6212d8bbf5e97`
TARGET=`libs/reporting/evaluation/full_chain_component_review_unavailable_component.py::_unavailable_component` (404 C+A).
BODY=exact insufficient-evidence decision dict with `DecisionClass.INSUFFICIENT_EVIDENCE.value`, original `availability` identity, `behavior_change_authorized=False`. TEST=missing comparison, patched DecisionClass, identity/key order and AST parity.

### A53-6 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::render_full_chain_component_review@1d44c646540adffd676ea16489b6212d8bbf5e97`
TARGET=`libs/reporting/evaluation/full_chain_component_review_render.py::render_full_chain_component_review` (404 C+A).
BODY=130-line in-memory Markdown string rendering only (NO `write_full_chain_component_review` move/call); preserve component table order, `json.dumps`/float formatting, Unicode/newlines and exact output bytes. Facade `json` and helper seams. TEST=empty/full payload, unusual unicode/float, exact newline bytes, AST parity, no Path.write_text.

### A53-7 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::classify_scanner_alignment_root_cause@2a595f8d1025fd6bcc31033d256e7f1766c57ab0`
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_classify.py::classify_scanner_alignment_root_cause` (404 C+A).
BODY=91-line in-memory root cause classification (Missing Evidence/Symbol Mapping/Candidate Filtering/Strategist Override and remaining original branches), original `_selected_rank`/`_score_gap` call-time patch seam, confidence/reasons/order. No file read or behavior patch execution. TEST=missing symbols, changed mappings, selected rank, gap, net return edge, exact reason text, AST parity.

### A53-8 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::render_scanner_alignment_root_cause_report@2a595f8d1025fd6bcc31033d256e7f1766c57ab0`
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_render.py::render_scanner_alignment_root_cause_report` (404 C+A).
BODY=54-line in-memory Markdown report renderer only; `_mapping` call-time patch seam, row filtering, percent formatting, exact text/line order; DO NOT touch writer or load range. TEST=empty/full/malformed payload, patched _mapping, Unicode, bytes/newlines and AST parity.

## VERIFIED UNASSIGNED RESERVE — A 6/6, do not execute without new C03 order
Each SOURCE body and SOURCE blob were inspected and matched canonical==A; each unique TARGET 404 on canonical+A, RF-032 A-exclusive. These are NOT A53 READY or accomplishments. Fake-only future normal targeted test required before G2; no test run yet.
1. `libs/reporting/evaluation/scanner_quality.py::build_scanner_quality_review@57f190411ed91e6318771f63ffda8f416a6eacac` → `libs/reporting/evaluation/scanner_quality_build_scanner_quality_review.py::build_scanner_quality_review` (404 C+A). In-memory quality aggregation; no direct filesystem write, but fake-patch `attach_forward_outcomes` and `performance_metrics` before calling; test missing payload/horizon/topk/order.
2. `libs/reporting/evaluation/episode_scanner_review.py::build_episode_scanner_review@0f0b5ac107f26a0aa82ff8c0b75e7a0ad65bcdfe` → `libs/reporting/evaluation/episode_scanner_review_build_episode_scanner_review.py::build_episode_scanner_review` (404 C+A). In-memory rank bucket/episode metrics, prepared_rows fake avoids external payload; test negative drag/horizon/order.
3. `libs/reporting/evaluation/episode_scanner_review.py::build_same_symbol_reentry_review@0f0b5ac107f26a0aa82ff8c0b75e7a0ad65bcdfe` → `libs/reporting/evaluation/episode_scanner_review_build_same_symbol_reentry_review.py::build_same_symbol_reentry_review` (404 C+A). Pure trade-id grouping and reentry metric summary, fake row inputs only; test malformed IDs, first/repeat, negative previous returns.
4. `libs/reporting/evaluation/no_trade_attribution.py::render_no_trade_attribution_report@7f707a446d06362bf3962318b7c88563a306bfd0` → `libs/reporting/evaluation/no_trade_attribution_render.py::render_no_trade_attribution_report` (404 C+A). In-memory string renderer, no write; test empty/full, exact Markdown bytes.
5. `libs/reporting/evaluation/no_trade_attribution.py::_baseline_samsung@7f707a446d06362bf3962318b7c88563a306bfd0` → `libs/reporting/evaluation/no_trade_attribution_baseline_samsung.py::_baseline_samsung` (404 C+A). Read-only `_read_json` call plus pure horizon projection; IO impact is existing read ONLY. Fake-patch `_read_json` with tmp fixture, never read real reports; test missing/malformed summary, first-key fallback.
6. `libs/reporting/evaluation/no_trade_attribution.py::_q12_btc_woori@7f707a446d06362bf3962318b7c88563a306bfd0` → `libs/reporting/evaluation/no_trade_attribution_q12_btc_woori.py::_q12_btc_woori` (404 C+A). Read-only `_read_json` plus horizon net metrics; IO impact is existing read ONLY. Fake-patch `_read_json` with tmp fixture, no real file reads; test eligible_entries/top1 fallback, invalid rows.

## DELIVERY / #11
A53-1..8 each DONE with SOURCE before/after, Owner/test blob, normal EXIT/PASS, or individually BLOCKED with exact SOURCE/TARGET/SHA/FIRST_BLOCKER. Continue other safe items after failure. Before push `git status --short`, `git diff --cached --name-only`: staged SOURCE **2** + new Owners **8** + test **1** = **11 paths**; inspect `git show --name-only`, re-stage SOURCE after stash/pop (A49 intermediate omission already corrected; do NOT rerun A49). Push non-force, re-fetch exact remote A HEAD/full root tree and 11 blobs; no local-only claim as G1. Report actual START_KST/END_KST/ELAPSED_MIN, before/after SHA, test command EXIT and PASS separately, changed path manifest and blockers to #11. C04 alone integrates/G3; C05 alone RF/STATUS/DONE. No docs/C01/C03/C04/C05/D00/RF/STATUS/CI/workflow/RunLab/Guard/Step5C/UEF/operations writes.
