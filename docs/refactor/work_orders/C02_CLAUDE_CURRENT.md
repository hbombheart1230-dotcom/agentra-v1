# C02 — Claude A | ORDER_ID=A-20261103-00-C03 | RF-032 PEER | A48 NEW_READY=8/8 | A47 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START / authoritative remote pins
Canonical prewrite `integration/p1.5@1edf8dfc4d1eb82a5512709977d3e3cc52392dc3`; A actor `work/p15-a-reporter-pure-20261021@128bad7750e7e0dc472303755337d16cd38f4d60`. Previous C02 blob `08c19421ad663fa918284626330036678a14a07b`. #11 [A47 6580939923](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6580939923): A47-1..8 delivered at exact A remote SHA, normal targeted **278 PASS EXIT=0**; C04 [#36 6581135940](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6581135940) integrated A47 exact 12/12 at canonical `1edf8dfc`, scoped G3_REUSE MET. **A47 and A1–A46 are DONE/ALREADY, not new work.** If an earlier starting order was genuinely in progress, finish its safe items first, never retroactively cancel.

First shell `python -m pytest --version`; if absent `python -m pip install --user pytest`, recheck. Fetch this **single latest remote C02** from `integration/p1.5`, log canonical HEAD/C02 blob/ORDER_ID in #11; no D00/RF/INDEX/CURRENT reread. Skill `.agents/skills/agentra-contract-guard/SKILL.md@f2fe45fd856f65f5f7b5a3b710317baf1bf9ad5d` was manually read by C03 as **non-authoritative** safety checklist; automatic loading NOT_VERIFIED, do not treat it as a new gate.

## DONE-FIRST / protected boundaries
Physical queue as C05 [#36 6581557766](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6581557766): PENDING38 / DEV7 / PEER2 / DONE46, unresolved47, NEW_DONE0. **RF-030** first missing G1 partial (15/16 KEEP vs frozen RF-074 oracle), G2 pending, canonical G3 fake smoke pending; C04 canonical smoke, C05 physical DONE only. **RF-063** whole G1/G2 residual and G3 resolver/runtime closure remains; B37 now completed/integrated and must not be repeated. **RF-032** validation-id/Writer/UEF whole G1 BLOCKED_POLICY; A48 is scoped observation-only BODY MOVE, NOT RF DONE. Never change frozen oracle, policy/Guard, real/paper orders, Step5C, UEF, RunLab, live network, OS/DB/operational state.

## A48 — 8 new, individually authorized SOURCE::function → exclusive TARGET Owner BODY MOVEs
Preflight C03 inspected actual SOURCE bodies on identical canonical/A Git blobs and complete nontruncated Git trees (C=5736, A=5311 entries); all eight unique TARGET paths and `tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` were 404 on both refs. RF-032 FILE_COVERAGE covers all three SOURCE modules; no cross-actor paths. The two scanner aggregators only **read already materialized fake rows**, never call pre_strategist_candidate_rows/build_scanner_quality_review or attach forward outcomes.

**Every item:** re-fetch exact SOURCE blob and target on actor branch before editing; if SHA drift or TARGET already exists, mark VERIFIED_ALREADY=0 or BLOCKED with exact current SHA/FIRST_BLOCKER, do not overwrite. Move the **real entire calculation body** to one TARGET Owner; original public SOURCE keeps exact signature/defaults/docstring and a thin wrapper. Use `facade=sys.modules[__name__]` at call time to preserve SOURCE helper/constant/Mapping/Counter/monkeypatch seams, but Owner must never import SOURCE; retain original exception order, identity, generator consumption, dict ordering, Markdown bytes and import timing. For SOURCE-defined default binding, preserve wrapper signature and pass bound default explicitly to Owner. Only A edits A code/test and non-force pushes A branch. One fake-only normal targeted `python -m pytest -q tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` EXIT=0; at least one distinct original-preimage AST vs new wrapper+Owner parity case for each of eight. No mandatory -O/full-suite/hosted CI. If one item blocked continue all other safe items; no retesting A47.

### A48-1 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_quality.py::build_scanner_topk_forward_performance` Git blob `13abc5dd46c0f6912fe263fd1dfd3dbbf3fd3df5` (canonical=A at issuance). TARGET=`libs/reporting/evaluation/scanner_quality_build_scanner_topk_forward_performance.py::build_scanner_topk_forward_performance` (404 canonical+A). 
ACTUAL_BODY=In-memory decision_id grouping, SCANNER_HORIZONS×TOP_K_VALUES rank sort, observed checkpoint average, gross/net drag, candidate_day distinct-day counts, performance_metrics and ordered schema; call SOURCE facade._number/_checkpoint_return/candidate_day/performance_metrics/constants at use time.
TARGETED_NORMAL_CASES=Empty and duplicate decision IDs, rank=0 vs missing, ties, missing checkpoints, zero/negative returns, multiple horizons/top-K, patched helpers/constants, ordered rows and exception parity.
TEST=`tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` (original AST parity, monkeypatch/ordering/exception). On blocker record current SOURCE/TARGET/blob/FIRST_BLOCKER; continue A48-2 or completion.

### A48-2 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_quality.py::build_scanner_source_performance` Git blob `13abc5dd46c0f6912fe263fd1dfd3dbbf3fd3df5` (canonical=A at issuance). TARGET=`libs/reporting/evaluation/scanner_quality_build_scanner_source_performance.py::build_scanner_source_performance` (404 canonical+A). 
ACTUAL_BODY=In-memory source/horizon buckets, unknown fallback, per-source cost/slippage drag, candidate_day sets, sorted buckets and performance_metrics; call facade._checkpoint_return/candidate_day/performance_metrics/SCANNER_HORIZONS at use time.
TARGETED_NORMAL_CASES=Unknown/duplicate sources, no observed return, zero cost, horizon ordering, patched helpers, sorted row/schema and exception parity.
TEST=`tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` (original AST parity, monkeypatch/ordering/exception). On blocker record current SOURCE/TARGET/blob/FIRST_BLOCKER; continue A48-3 or completion.

### A48-3 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/selection_authority_audit.py::_mapping` Git blob `7f139a43a46a53c947c033d19a2eea4fff36ac7c` (canonical=A at issuance). TARGET=`libs/reporting/evaluation/selection_authority_audit_mapping.py::_mapping` (404 canonical+A). 
ACTUAL_BODY=Return input Mapping by identity else new empty dict; facade.Mapping dynamic lookup.
TARGETED_NORMAL_CASES=Dict/subclass identity, None/nonmapping, patched Mapping, exception parity.
TEST=`tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` (original AST parity, monkeypatch/ordering/exception). On blocker record current SOURCE/TARGET/blob/FIRST_BLOCKER; continue A48-4 or completion.

### A48-4 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/selection_authority_audit.py::_symbol` Git blob `7f139a43a46a53c947c033d19a2eea4fff36ac7c` (canonical=A at issuance). TARGET=`libs/reporting/evaluation/selection_authority_audit_symbol.py::_symbol` (404 canonical+A). 
ACTUAL_BODY=Mapping symbol extraction or scalar string; falsy fallback and strip; facade.Mapping dynamic lookup.
TARGETED_NORMAL_CASES=Mapping symbol empty/nonempty, scalar/None/whitespace, patched Mapping, exact string.
TEST=`tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` (original AST parity, monkeypatch/ordering/exception). On blocker record current SOURCE/TARGET/blob/FIRST_BLOCKER; continue A48-5 or completion.

### A48-5 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/selection_authority_audit.py::_changed` Git blob `7f139a43a46a53c947c033d19a2eea4fff36ac7c` (canonical=A at issuance). TARGET=`libs/reporting/evaluation/selection_authority_audit_changed.py::_changed` (404 canonical+A). 
ACTUAL_BODY=Tri-state comparison: None when either side falsy; otherwise a != b; preserve types/exceptions.
TARGETED_NORMAL_CASES=Empty/None, equal/different, custom __eq__, exact bool/None.
TEST=`tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` (original AST parity, monkeypatch/ordering/exception). On blocker record current SOURCE/TARGET/blob/FIRST_BLOCKER; continue A48-6 or completion.

### A48-6 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/selection_authority_audit.py::build_selection_authority_audit` Git blob `7f139a43a46a53c947c033d19a2eea4fff36ac7c` (canonical=A at issuance). TARGET=`libs/reporting/evaluation/selection_authority_audit_build_selection_authority_audit.py::build_selection_authority_audit` (404 canonical+A). 
ACTUAL_BODY=Read-only model selection/monitor/commander projection; skip two defect classes, _mapping/_symbol/_changed use-time, Counter order, exact observation_only interpretation and row schema; no selection/approval decision changes.
TARGETED_NORMAL_CASES=Excluded defect combinations, absent nested fields, mismatch tri-state, commander fallback precedence, Counter counts and ordering, monkeypatched helpers, exact output.
TEST=`tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` (original AST parity, monkeypatch/ordering/exception). On blocker record current SOURCE/TARGET/blob/FIRST_BLOCKER; continue A48-7 or completion.

### A48-7 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/selection_authority_audit.py::render_selection_authority_audit` Git blob `7f139a43a46a53c947c033d19a2eea4fff36ac7c` (canonical=A at issuance). TARGET=`libs/reporting/evaluation/selection_authority_audit_render_selection_authority_audit.py::render_selection_authority_audit` (404 canonical+A). 
ACTUAL_BODY=Pure Markdown construction: summary sorted keys, no rows placeholder, fixed table columns, skip non-Mapping rows, trailing newline; use facade._mapping/Mapping.
TARGETED_NORMAL_CASES=Empty/ordered summary, nonmapping rows, false/zero display fallback, patched Mapping/_mapping, exact UTF-8 Markdown bytes.
TEST=`tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` (original AST parity, monkeypatch/ordering/exception). On blocker record current SOURCE/TARGET/blob/FIRST_BLOCKER; continue A48-8 or completion.

### A48-8 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/feedback_effectiveness.py::build_feedback_effectiveness` Git blob `f12cec33f28a492c41e306dbede6c8c4540eb4a0` (canonical=A at issuance). TARGET=`libs/reporting/evaluation/feedback_effectiveness_build_feedback_effectiveness.py::build_feedback_effectiveness` (404 canonical+A). 
ACTUAL_BODY=In-memory q9 feedback identity dedupe, adoption candidate count, provenance fallback trade records, rate rounding and schema. Preserve facade.CONTRACT_VERSION/DecisionClass and no causal-claim assertion; no runtime feedback writes.
TARGETED_NORMAL_CASES=Empty models/windows, duplicate feedback_id+decision_id, adopted/unadopted, trade provenance fallback, record order, patched constants, exact schema and exceptions.
TEST=`tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` (original AST parity, monkeypatch/ordering/exception). On blocker record current SOURCE/TARGET/blob/FIRST_BLOCKER; continue A48-9 or completion.
## VERIFIED RESERVE — A 6/6, UNASSIGNED (not actor discretion)
All six SOURCE function bodies inspected; canonical=A exact blob and unique TARGET 404 in both complete Git trees; RF-032 FILE_COVERAGE owns each SOURCE. Fake-only, in-memory; no IO/state/order/UEF. These are NOT A48 and are NOT authorized to execute until C03 explicitly assigns.
1. `libs/reporting/evaluation/no_trade_attribution.py::_mapping@967aca16db2926cc00b0a7761d1534cf4b84540b` → `libs/reporting/evaluation/no_trade_attribution_mapping.py::_mapping` (404 C+A); TEST_HYPOTHESIS=Mapping identity or {}, fake dict/subclass/None; no IO; UNASSIGNED.
2. `libs/reporting/evaluation/no_trade_attribution.py::_num@967aca16db2926cc00b0a7761d1534cf4b84540b` → `libs/reporting/evaluation/no_trade_attribution_num.py::_num` (404 C+A); TEST_HYPOTHESIS=float parse with only TypeError/ValueError catch, fake custom __float__; UNASSIGNED.
3. `libs/reporting/evaluation/no_trade_attribution.py::_pct@967aca16db2926cc00b0a7761d1534cf4b84540b` → `libs/reporting/evaluation/no_trade_attribution_pct.py::_pct` (404 C+A); TEST_HYPOTHESIS=_num use-time and 4-decimal pct formatting, fake invalid/zero; UNASSIGNED.
4. `libs/reporting/evaluation/no_trade_attribution.py::_top@967aca16db2926cc00b0a7761d1534cf4b84540b` → `libs/reporting/evaluation/no_trade_attribution_top.py::_top` (404 C+A); TEST_HYPOTHESIS=Counter.most_common stable top limit and falsy-key filter, fake Counter; UNASSIGNED.
5. `libs/reporting/evaluation/no_trade_attribution.py::_q9_window_view@967aca16db2926cc00b0a7761d1534cf4b84540b` → `libs/reporting/evaluation/no_trade_attribution_q9_window_view.py::_q9_window_view` (404 C+A); TEST_HYPOTHESIS=In-memory reduced scanner/strategist/commander Mapping projection; no report IO; UNASSIGNED.
6. `libs/reporting/evaluation/scanner_alignment_root_cause.py::_mapping@8774bea29dd8ebd83283b28c5109e5fc6210fd1a` → `libs/reporting/evaluation/scanner_alignment_root_cause_mapping.py::_mapping` (404 C+A); TEST_HYPOTHESIS=Mapping identity-or-empty; fake dict/subclass/None; no IO; UNASSIGNED.
 
## ACCEPTANCE / #11
Finish A48-1..8 or item-specific BLOCKED with SOURCE/TARGET/current SHA/FIRST_BLOCKER; keep processing independent safe items. Report measured START_KST/END_KST/ELAPSED_MIN, remote A HEAD before/after, full-root tree, SOURCE before/after/Owner/test Git blobs, normal command/EXIT/PASS, non-force push and remote re-fetch. New BODY_MOVE only for actually moved functions; KEEP/ALREADY=0. C04 alone integrates selected code/G3; C05 alone updates RF/STATUS/DONE. C03 did not execute A code or tests.
