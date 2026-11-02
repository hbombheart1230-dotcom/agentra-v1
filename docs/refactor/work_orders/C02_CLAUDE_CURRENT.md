# C02 — Claude A | ORDER_ID=A-20261102-21-C03 | RF-032 PEER | A45 NEW_READY=8/8 | A44 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START — exact remote pins and in-flight protection
Canonical baseline `integration/p1.5@6915f64dd56b6e8fa2771fd4fa4252b79b8feb2b`, A actor `work/p15-a-reporter-pure-20261021@aa2f2ab1ff9efc12e577e11182e9cf480d151c01`; prior C02 blob `18b4dcf4e7addba719e6936e572e4fa31b04acce`. #11 [A44 6576018106](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6576018106): A44-1..8 all remote DONE, targeted normal **234 PASS EXIT0**. C04 [6576114228](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6576114228) integrated exact A44 source/8 Owners/test at canonical `6915f64d`; C05 [6576285635](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6576285635) whole RF-032 G1 BLOCKED_POLICY, **NOT DONE**. Do not repeat A44 or earlier A33–A43; these are not NEW_BODY_MOVE. If an earlier order was already started, finish its safe items before reading this next-start order; do not retroactively cancel it. First run `python -m pytest --version`, install `python -m pip install --user pytest` if missing, recheck, then execute assigned work.

## DONE-first / bounded non-code closeout evidence
Physical canonical 93 RF = PENDING38 / DEV7 / PEER2 / DONE46, unresolved47. **RF-030** physical G1 PARTIAL/G2 PENDING; C04 canonical G3 fake smoke not established. A actor `operator_visibility.py@ec196b5fe6ec3acff9e09178d0d8f7662badeb83` differs from canonical `bb6e97a72f94412ff9ca818dbf2a03d788dddf48`, so A-only PASS cannot satisfy canonical G3. C04 alone handles canonical `python -m pytest -q tests/test_p15_rf030_20261102_02h_run_contexts.py` EXIT0 / dependency-identical proof; C05 whole G1/G2/G3 adjudication. RF-030 historical RF-074 frozen-oracle restriction remains; do not edit forbidden operator source or oracle. RF-032 validation-id/Writer/UEF safety HOLD remains; do not change protected effects or claim DONE based on A45. RF-063 resolver/import closure belongs B/C04.

## A45 — eight NEW verified safe SOURCE::function → sole TARGET Owner
Each listed SOURCE was fetched on **both** canonical and A HEAD above with **identical Git blob**, actual function body inspected. Every listed sole TARGET basename was absent in both complete `libs/reporting/evaluation/` directory listings; new targeted test `tests/test_p15_rf032_20261102_21h_reporting_pure_owners.py` explicitly GitHub **404 on both**. All SOURCEs belong RF-032 FILE_COVERAGE; no B overlap. These are in-memory report calculations/projections/Markdown; never read/write operating state, trade, broker, Guard, Step5C, UEF, RunLab, frozen oracle, or live network.

For each item: re-fetch SOURCE and target at start; if changed, record exact new blob and stop **that item only** pending conflict analysis, continue other safe items. Move **actual entire computation** into exactly one Owner module/function (no copy-only), leave SOURCE with exact-signature thin wrapper that resolves dynamic helpers/monkeypatch via `facade=sys.modules[__name__]` at **call time**, with no Owner→SOURCE import. Preserve generator/evaluation timing, output types/keys/order, exceptions/messages and IO=none. For each item test original pre-move AST function vs new facade/Owner under fake inputs and patched globals, verify source wrapper is thin and Owner holds sole body. Do not change existing fixture/oracle. New targeted test command **`python -m pytest -q tests/test_p15_rf032_20261102_21h_reporting_pure_owners.py`**, require normal EXIT=0 and real PASS count; only A owns code/test commit and non-force push to its own branch. If item blocked, log SOURCE/TARGET/current blob/FIRST_BLOCKER, then continue next safe item.

### A45-1 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/loss_decomposition.py::_entry_timing_summary` @ `bbe3777bbf339812766aed8816818939ce788242` L70 (63 source lines); TARGET=`libs/reporting/evaluation/loss_decomposition_entry_timing_summary.py::_entry_timing_summary` (absent canonical+A at issuance).
ACTUAL_BODY=same-symbol baseline candidate time sorting; entry epoch/price ratio, median/mean, matched days/examples; preserve defaultdict/Mapping/_to_float/_parse_ts/median call-time facade and dict key order.
TARGETED_NORMAL_CASES=empty/no match, 15min boundary, invalid baseline, patched _to_float/_parse_ts, sorting/tie and exception parity. AST original-body vs final facade/Owner output, exception, type, call order and monkeypatch parity; targeted test above normal EXIT0. On blocker record SOURCE/TARGET/blob/FIRST_BLOCKER and continue A45-2.

### A45-2 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/loss_decomposition.py::_exit_hold_summary` @ `bbe3777bbf339812766aed8816818939ce788242` L133 (49 source lines); TARGET=`libs/reporting/evaluation/loss_decomposition_exit_hold_summary.py::_exit_hold_summary` (absent canonical+A at issuance).
ACTUAL_BODY=post-exit +5/+15/+30/+60m observed checkpoint aggregation, improvements, counts/examples; preserve Mapping/_to_float/defaultdict call-time facade and iteration order.
TARGETED_NORMAL_CASES=missing/invalid checkpoint, observed/unobserved, zero/negative improvement, patched _to_float, key/order parity. AST original-body vs final facade/Owner output, exception, type, call order and monkeypatch parity; targeted test above normal EXIT0. On blocker record SOURCE/TARGET/blob/FIRST_BLOCKER and continue A45-3.

### A45-3 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/loss_decomposition.py::_diagnosis` @ `bbe3777bbf339812766aed8816818939ce788242` L182 (69 source lines); TARGET=`libs/reporting/evaluation/loss_decomposition_diagnosis.py::_diagnosis` (absent canonical+A at issuance).
ACTUAL_BODY=six ordered diagnostic finding rows and exact stage/status/string interpolation; pure in-memory; preserve Mapping call-time facade.
TARGETED_NORMAL_CASES=empty shadow, missing buckets, optional metrics, output stage order, exact strings and exceptions. AST original-body vs final facade/Owner output, exception, type, call order and monkeypatch parity; targeted test above normal EXIT0. On blocker record SOURCE/TARGET/blob/FIRST_BLOCKER and continue A45-4.

### A45-4 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/loss_decomposition.py::_next_action` @ `bbe3777bbf339812766aed8816818939ce788242` L251 (43 source lines); TARGET=`libs/reporting/evaluation/loss_decomposition_next_action.py::_next_action` (absent canonical+A at issuance).
ACTUAL_BODY=in-memory recommendation/evidence projection only (behavior_change_authorized remains False); preserve _to_float facade lookup and no runtime action.
TARGETED_NORMAL_CASES=missing top_pick, missing +5m, patched _to_float, fixed False flag, key order. AST original-body vs final facade/Owner output, exception, type, call order and monkeypatch parity; targeted test above normal EXIT0. On blocker record SOURCE/TARGET/blob/FIRST_BLOCKER and continue A45-5.

### A45-5 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/loss_decomposition.py::render_loss_decomposition` @ `bbe3777bbf339812766aed8816818939ce788242` L360 (98 source lines); TARGET=`libs/reporting/evaluation/loss_decomposition_render_loss_decomposition.py::render_loss_decomposition` (absent canonical+A at issuance).
ACTUAL_BODY=Markdown-only string renderer, exact table row order/formatting/trailing newline; no disk write, preserve original signature.
TARGETED_NORMAL_CASES=empty/mixed payload, formatting/escaping, missing nested keys, exact byte-for-byte Markdown/exception parity. AST original-body vs final facade/Owner output, exception, type, call order and monkeypatch parity; targeted test above normal EXIT0. On blocker record SOURCE/TARGET/blob/FIRST_BLOCKER and continue A45-6.

### A45-6 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/evaluation_lens_report.py::_candidate_rows` @ `c58aac7eac505f4e0a847261fd4e0ab02995c9ae` L99 (13 source lines); TARGET=`libs/reporting/evaluation/evaluation_lens_report_candidate_rows.py::_candidate_rows` (absent canonical+A at issuance).
ACTUAL_BODY=copy Mapping candidate rows, setdefault generated timestamp, attach_forward_outcomes at call time through facade; preserve iterable consumption and original row order.
TARGETED_NORMAL_CASES=non-Mapping rows, existing timestamp, generator once, patched attach_forward_outcomes, input mutation/exception parity. AST original-body vs final facade/Owner output, exception, type, call order and monkeypatch parity; targeted test above normal EXIT0. On blocker record SOURCE/TARGET/blob/FIRST_BLOCKER and continue A45-7.

### A45-7 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/evaluation_lens_report.py::_q9_candidate_rows` @ `c58aac7eac505f4e0a847261fd4e0ab02995c9ae` L112 (13 source lines); TARGET=`libs/reporting/evaluation/evaluation_lens_report_q9_candidate_rows.py::_q9_candidate_rows` (absent canonical+A at issuance).
ACTUAL_BODY=copy Mapping q9_decision_candidates rows, setdefault generated timestamp, call-time attach_forward_outcomes; preserve output order.
TARGETED_NORMAL_CASES=missing q9 list, invalid rows, existing timestamp, generator, monkeypatch attach_forward_outcomes parity. AST original-body vs final facade/Owner output, exception, type, call order and monkeypatch parity; targeted test above normal EXIT0. On blocker record SOURCE/TARGET/blob/FIRST_BLOCKER and continue A45-8.

### A45-8 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/cost_basis_comparison.py::_topk_rows` @ `d6ceae367fead768c76155bb775987e92e2bbdde` L69 (10 source lines); TARGET=`libs/reporting/evaluation/cost_basis_comparison_topk_rows.py::_topk_rows` (absent canonical+A at issuance).
ACTUAL_BODY=pure topk_forward_performance rows → (int(top_k), str(horizon)) keyed dict; preserve Mapping lookup, duplicate-key last-wins and conversion exceptions.
TARGETED_NORMAL_CASES=missing/non-Mapping topk, duplicate keys, malformed top_k ValueError, key order, patched Mapping seam. AST original-body vs final facade/Owner output, exception, type, call order and monkeypatch parity; targeted test above normal EXIT0. On blocker record SOURCE/TARGET/blob/FIRST_BLOCKER and continue A45-completion.

## VERIFIED RESERVE — A 6/6, NOT ASSIGNED, NOT CODE DONE
All below SOURCE blobs canonical=A at issuance, original bodies inspected, sole TARGET filenames absent from both complete evaluation directory listings. RF-032 owns these sources. Reserve is **not** permission for A to self-select or implement.
1. `horizon_compliance_report.py::_mapping@e4d6325a8f7def0ad682188000a84b89be00c6e1` L9 → `horizon_compliance_report_mapping.py::_mapping`: 4-line Mapping-only in-memory projection, fake non-Mapping/dict parity, no effects.
2. `horizon_compliance_report.py::_num@e4d6325a8f7def0ad682188000a84b89be00c6e1` L13 → `horizon_compliance_report_num.py::_num`: 9-line float/None conversion with TypeError/ValueError, fake invalid inputs.
3. `horizon_compliance_report.py::_bucket_key@e4d6325a8f7def0ad682188000a84b89be00c6e1` L22 → `horizon_compliance_report_bucket_key.py::_bucket_key`: 8-line tuple grouping, dynamic _mapping seam, fake missing horizon/exit.
4. `horizon_compliance_report.py::render_horizon_compliance_report@e4d6325a8f7def0ad682188000a84b89be00c6e1` L140 → `horizon_compliance_report_render_horizon_compliance_report.py::render_horizon_compliance_report`: 43-line in-memory Markdown, exact newline/order, fake payload.
5. `cost_basis_comparison.py::_pct@d6ceae367fead768c76155bb775987e92e2bbdde` L29 → `cost_basis_comparison_pct.py::_pct`: 4-line float×100 rounded, fake NaN/float/exception.
6. `cost_basis_comparison.py::render_cost_basis_comparison@d6ceae367fead768c76155bb775987e92e2bbdde` L157 → `cost_basis_comparison_render_cost_basis_comparison.py::render_cost_basis_comparison`: 52-line pure Markdown formatting, no output write, fake byte parity.

## ACCEPTANCE / #11
Execute **all** A45-1..8, or individually explain BLOCKED. Report actual START_KST/END_KST/ELAPSED_MIN (not inferred from issue time), each SOURCE pre/post blob, sole TARGET blob, test blob, normal command EXIT/PASS, branch before/after remote HEAD/tree, non-force push/refetch and exact per-item DONE/BLOCKED. Distinguish new BODY_MOVEs from KEEP/already moved. If no code changes or pytest/push unavailable, report actual evidence; do not invent PASS. Do not edit Markdown/RF/STATUS/other branches. C04 alone integrates, C05 alone adjudicates G1/G2/G3 and DONE.
