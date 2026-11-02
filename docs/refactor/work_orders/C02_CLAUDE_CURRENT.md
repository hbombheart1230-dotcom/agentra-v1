# C02 — Claude A | ORDER_ID=A-20261103-08-C03 | RF-032 PEER | A55 NEW_READY=8/8 | A54 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START — latest remote only; preserve already-started order
C03 prewrite canonical `15207cf47e3b1b447545f5948a73eed3801f1e9d`, A remote `7d1dcb8b55ea98b52fc4bcbdacf4aaaa0d9eeca1`, previous C02 blob `f40ed5f2ebc9cc7e368d3fc92b263da01b2adb99`. A54 [#11 6589870708](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6589870708) **8/8 remote DONE**, normal `tests/test_p15_rf032_20261103_07h_quality_episode_no_trade_owners.py` EXIT0/152 PASS, actor SHA above; C04 [#36 6590341772](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6590341772) integrated 12/12 exact A54 paths at canonical `15207cf4`; C05 [#36 6590478122](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6590478122) still 46/93 DONE, RF-032 whole G1 BLOCKED_POLICY. A54 and older A tasks MUST NOT be repeated/recounted. If an older starting order genuinely in flight, finish its safe items first; do not retroactively cancel.

First shell `python -m pytest --version`; if missing `python -m pip install --user pytest`, recheck. Fetch **remote** `integration/p1.5:docs/refactor/work_orders/C02_CLAUDE_CURRENT.md`, log full canonical HEAD/C02 blob/ORDER_ID and A HEAD to #11. This C02 is sole execution entrypoint: no D00/RF/INDEX/SKILL re-read and no self-selected RF. Refetch each SOURCE and TARGET on A before editing; if preimage SHA changed or target exists, record item-specific evidence and continue independent items. Code/test only on A branch, non-force push.

## DONE-FIRST / why this scope
Physical PENDING38/DEV7/PEER2/DONE46, 47 unresolved (C05 07:48). RF-030 G1 PARTIAL RF-074 frozen owner and canonical G2/G3 fake smoke are C04/C05, and A operator_visibility.py actor `ec196b5f` differs canonical `bb6e97a7`: no safe RF-030 blind reassignment. RF-032 validation-id/Writer/UEF G1 BLOCKED_POLICY cannot be changed by A55; these read-only/in-memory BODY MOVEs are continuity supply, **NOT whole RF DONE**. No protected Writer/UEF/Guard/Step5C, broker/trade, live network, runtime state/DB, operational reports or frozen oracle/CI modifications. For existing read-only loaders, only fake patch or tmp_path tests; never production reports. Keep signatures, defaults, docstrings, imports, dict order, identity, exceptions, output bytes, monkeypatch seams.

## A55 eight independently verified SOURCE::function → single TARGET Owner
At issuance all SOURCE real bodies exist, canonical==A exact pinned blobs; all eight TARGETs and test path are 404 canonical+A. Use AST-bounded signature/body editing, not regex for multiline headers. SOURCE thin wrapper delegates to new Owner using call-time `sys.modules[__name__]` facade (Owner may take keyword-only facade); dynamically resolve helpers/globals/typing names through facade where monkeypatchable. Owner must not import SOURCE at module import. No extra G2/-O/full suite/peer/hosted CI gate.

### 1. RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_quality.py::pre_strategist_candidate_rows` | SOURCE_GIT_BLOB=`26a5eedd4adb46308a715256a791bd6f1a0c4d05` (canonical=actor verified 08h)
TARGET=`libs/reporting/evaluation/scanner_quality_pre_strategist_candidate_rows.py::pre_strategist_candidate_rows` | TARGET=404 canonical+actor verified
BODY=actual extract_pre_strategist_candidate_rows then attach_forward_outcomes; preserve optional keyword-only minute_rows_by_symbol and identity/call-time helper seam
TARGETED_NORMAL=empty/duplicate payload, None vs supplied minute map, fake attach/extract, exceptions
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 2. RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::build_scanner_alignment_root_cause_report` | SOURCE_GIT_BLOB=`b46c7569ab1cd3730193642d1e93f80f9035590d` (canonical=actor verified 08h)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_build_scanner_alignment_root_cause_report.py::build_scanner_alignment_root_cause_report` | TARGET=404 canonical+actor verified
BODY=real model/evaluation trade-id join, row root-cause classification, counts, impact and output ordering; all helpers dynamically through SOURCE facade
TARGETED_NORMAL=empty/duplicate trade IDs, missing model/evaluation, patched classify/metric, key and exception parity
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 3. RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_load_day_models_and_evaluations` | SOURCE_GIT_BLOB=`b46c7569ab1cd3730193642d1e93f80f9035590d` (canonical=actor verified 08h)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_load_day_models_and_evaluations.py::_load_day_models_and_evaluations` | TARGET=404 canonical+actor verified
BODY=read-only sorted trade dirs; _read_json model/evaluation, skip falsy payloads, return ordered pair; preserve Path.iterdir semantics
TARGETED_NORMAL=tmp_path fake directories only, missing day, malformed JSON via patched _read_json, sorting, no production IO
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 4. RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::build_scanner_alignment_root_cause_range` | SOURCE_GIT_BLOB=`b46c7569ab1cd3730193642d1e93f80f9035590d` (canonical=actor verified 08h)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_build_scanner_alignment_root_cause_range.py::build_scanner_alignment_root_cause_range` | TARGET=404 canonical+actor verified
BODY=real inclusive date iteration, daily selection/model/evaluation assembly, aggregate/root-cause summary and date error semantics
TARGETED_NORMAL=fake _read_json/_load_day_models_and_evaluations/build_scanner_alignment_root_cause_report; empty/reversed/invalid dates, exact dict order
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 5. RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/no_trade_attribution.py::build_no_trade_attribution_report` | SOURCE_GIT_BLOB=`59126f3b2695c52b3b5339f4488e5946c3f278ab` (canonical=actor verified 08h)
TARGET=`libs/reporting/evaluation/no_trade_attribution_build_no_trade_attribution_report.py::build_no_trade_attribution_report` | TARGET=404 canonical+actor verified
BODY=real NOOP/approve/buy/commander/monitor/scanner counter aggregation with read-only q9/q11/q12/baseline helper calls; preserve Counter insertion order
TARGETED_NORMAL=fake all report loaders; empty windows, approve+noop, buy, positive shadow, malformed row and key/exception parity
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 6. RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/no_trade_attribution.py::_read_json` | SOURCE_GIT_BLOB=`59126f3b2695c52b3b5339f4488e5946c3f278ab` (canonical=actor verified 08h)
TARGET=`libs/reporting/evaluation/no_trade_attribution_read_json.py::_read_json` | TARGET=404 canonical+actor verified
BODY=real path.read_text UTF-8 + json.loads; return dict only; catch any Exception and return {}; no writes
TARGETED_NORMAL=tmp_path only: missing/invalid/array/object/UTF-8; facade.json monkeypatch and exception parity
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 7. RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_read_json` | SOURCE_GIT_BLOB=`b46c7569ab1cd3730193642d1e93f80f9035590d` (canonical=actor verified 08h)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_read_json.py::_read_json` | TARGET=404 canonical+actor verified
BODY=real UTF-8 json.loads read-only dict projection; any Exception => {}; separate Owner from no_trade _read_json
TARGETED_NORMAL=tmp_path only: missing/invalid/non-dict/valid, patched json, no production paths
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

### 8. RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/historical_prior.py::_rank_bucket` | SOURCE_GIT_BLOB=`6adbc1e96e1fd160c5efcd9e7e7704c300c32c20` (canonical=actor verified 08h)
TARGET=`libs/reporting/evaluation/historical_prior_rank_bucket.py::_rank_bucket` | TARGET=404 canonical+actor verified
BODY=real int(float(value)) conversion with only TypeError/ValueError caught; <=1, <=3, <=10, rank11_plus, unknown; do not catch OverflowError
TARGETED_NORMAL=None/nonnumeric/negative/1/3/10/11/nan/inf, exact exception and bucket parity
MOVE=move actual entire computation body into exactly one Owner; original same-signature/default/docstring thin wrapper with call-time facade and original import compatibility; no duplicated calculation. If drift/collision, exact item BLOCKED/VERIFIED_ALREADY and continue others.

## VERIFIED UNASSIGNED RESERVE — A 6/6
All six actual bodies and canonical=A SOURCE SHA, RF-032 A-exclusive FILE_COVERAGE, distinct TARGET 404 on canonical+A, fake-only IO/state/test hypothesis checked at 08h. UNASSIGNED; do not execute without next C03 order.
1. SOURCE=`libs/reporting/evaluation/full_chain_component_review.py::build_full_chain_component_review@7706d3567dc27286b3c63e6344193401e28a944b` → TARGET=`libs/reporting/evaluation/full_chain_component_review_build_full_chain_component_review.py::build_full_chain_component_review` (404 canonical+actor). BODY/TEST=large read-only evaluation; fake all loaders/cost profile/os.getenv, no real filesystem/env, no writer; exclusive Owner; unassigned, no PASS.
2. SOURCE=`libs/reporting/evaluation/historical_prior.py::_day_from_trade_dir@6adbc1e96e1fd160c5efcd9e7e7704c300c32c20` → TARGET=`libs/reporting/evaluation/historical_prior_day_from_trade_dir.py::_day_from_trade_dir` (404 canonical+actor). BODY/TEST=Path.parts trades/day extraction, fake Path only; exclusive Owner; unassigned, no PASS.
3. SOURCE=`libs/reporting/evaluation/historical_prior.py::_net_return@6adbc1e96e1fd160c5efcd9e7e7704c300c32c20` → TARGET=`libs/reporting/evaluation/historical_prior_net_return.py::_net_return` (404 canonical+actor). BODY/TEST=realized_outcome.net_return_pct float; catch only TypeError/ValueError; exclusive Owner; unassigned, no PASS.
4. SOURCE=`libs/reporting/evaluation/historical_prior.py::_group_metrics@6adbc1e96e1fd160c5efcd9e7e7704c300c32c20` → TARGET=`libs/reporting/evaluation/historical_prior_group_metrics.py::_group_metrics` (404 canonical+actor). BODY/TEST=group float tuples, sorted keys, call-time performance_metrics; pure; exclusive Owner; unassigned, no PASS.
5. SOURCE=`libs/reporting/evaluation/historical_prior.py::summarize_historical_prior@6adbc1e96e1fd160c5efcd9e7e7704c300c32c20` → TARGET=`libs/reporting/evaluation/historical_prior_summarize_historical_prior.py::summarize_historical_prior` (404 canonical+actor). BODY/TEST=90-line in-memory eligible/returns/integrity counters; fake lists only; exclusive Owner; unassigned, no PASS.
6. SOURCE=`libs/reporting/evaluation/historical_prior.py::render_historical_prior_markdown@6adbc1e96e1fd160c5efcd9e7e7704c300c32c20` → TARGET=`libs/reporting/evaluation/historical_prior_render_historical_prior_markdown.py::render_historical_prior_markdown` (404 canonical+actor). BODY/TEST=61-line in-memory Markdown exact UTF-8/newlines; no writes; exclusive Owner; unassigned, no PASS.

## TARGETED TEST / DELIVERY / ACCEPTANCE
Implement `tests/test_p15_rf032_20261103_08h_scanner_no_trade_historical_owners.py` (new, 404 C+A) with original pinned preimage AST→Owner/wrapper parity for **all 8**, input/return/error/monkeypatch/format/identity/IO safety, fake/tmp_path only. Before pytest `python -m py_compile` all changed SOURCE+Owner files EXIT0. Normal `python -m pytest -q tests/test_p15_rf032_20261103_08h_scanner_no_trade_historical_owners.py` **EXIT0 required**, PASS count observed, not invented. Prepush `git status --short` + staged manifest must include SOURCE 4 + Owner 8 + test 1 = **13 paths**, especially after stash/pop; verify `git diff --cached --name-only` and `git show --name-only`. Non-force A push; refetch A remote HEAD/full-root tree and all 13 blobs. Per A55-1..8 report DONE with before/after SOURCE, Owner/test blob or BLOCKED exact SHA/FIRST_BLOCKER; continue other safe items. Actual START_KST/END_KST/ELAPSED_MIN, normal EXIT/PASS, final SHA to #11. No C/RF/STATUS/docs edits. C04 alone G3 integration, C05 alone RF DONE/STATUS.
