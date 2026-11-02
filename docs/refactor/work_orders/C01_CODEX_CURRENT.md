# C01 — Codex B | ORDER_ID=B-20261103-02-C03 | RF-063 DEV | B39 NEW_READY=8/8 | B38 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START / authoritative remote pins
C03 verified B38 [#12 6582211672](https://github.com/hbombheart1230-dotcom/agentra/issues/12#issuecomment-6582211672) B remote `0ea7c49be412401ea087c031a8af9dc07d7ce654`, 8/8 BODY MOVEs, normal `python -m pytest -q tests/test_p15_rf063_20261103_00h_diagnostics_pure_owners.py` EXIT=0/PASS=10; C04 [#36 6582622282](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6582622282) integrated B38 15/15 exact blobs at `08ecb864`. **B38 and B1-B37 are already delivered; no repeat/retest/recount.** Previous C01 blob `ff9d41dcd66a0724053d60438debbbe8ce93cd5f`. Protect any genuinely in-progress starting order; no retroactive cancellation.

First shell `python -m pytest --version`; if missing `python -m pip install --user pytest`, recheck. Fetch **latest remote** `integration/p1.5:docs/refactor/work_orders/C01_CODEX_CURRENT.md` by branch, not stale checkout; report exact REMOTE_CANONICAL_HEAD, C01_BLOB_SHA, ORDER_ID in #12. If B38 or older, refetch before concluding no work. Read this single C01, not D00/RF/INDEX. All SOURCE and TARGET pins independently checked on complete nontruncated Git trees: canonical `08ecb864acce08d92aad03b31be82a1b968f3425` tree `e4f010ef9a83bede487255a913c401fa975188d0` (5754 entries), A `87548b34d58308bc3686842bdd42ec0d10f767e7` tree `7bc2d5eff1dec1bfcd01e390308d004fcf88957e` (5320), B `0ea7c49be412401ea087c031a8af9dc07d7ce654` tree `cb71b1174adacb654cc5d3561ca084c6e847f3dc` (4705). Both new targeted tests absent on respective actor and canonical. RF-032 and RF-063 FILE_COVERAGE owner paths verified against their RF implementation inventories. C03 reviewed actual bodies, no source/target cross-actor overlap. Skill `.agents/skills/agentra-contract-guard/SKILL.md@f2fe45fd856f65f5f7b5a3b710317baf1bf9ad5d` used manually as non-authoritative checklist; auto-load NOT_VERIFIED, no new gate.

## DONE-FIRST — RF-063 resolver first unmet / bounded precheck
Latest C05 [#36 6582764054](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6582764054): DONE46/93, unresolved47; RF-063 whole G1/G2 residual, G3 **BLOCKED** on `libs/reporting/llm_artifacts.py` resolver/import/consumer runtime parity. Canonical `llm_artifacts.py@27aea755e3ab9a3143affbd28294e4c8c775b8ca` uses split `_lookup_owner` etc; B actor `llm_artifacts.py@06dd435f68aeae0043e43f27f0b1600fa3e61b0c` is divergent old monolith. **Before B39 changes**, perform read-only exact-source dependency map for `resolve_trade_day_root`, `iter_trade_day_roots`, `list_misplaced_trade_day_roots` and direct consumers; report first specific missing import/behavior parity, source/Owner blobs, fake/temp test hypothesis, and whether C04 must select a complete closure. This precheck is NOT a new BODY MOVE/G1/G2/G3 and does not authorize changing resolver/trade/LLM/effect code, real paths or running live consumers. If no safe closure, report `FIRST_BLOCKER=CANONICAL_B_ACTOR_SOURCE_DIVERGENCE` and continue all eight B39 independent items. C04 alone integrates safe closure and verifies G3; C05 alone DONE. RF-030 canonical fake smoke belongs C04; RF-026 cold-import policy HOLD, RF-032 Writer/UEF HOLD. No extra CI/-O/full peer gate.

## B39 — eight individually verified independent pure BODY MOVE items
Before each item refetch SOURCE/TARGET on B; SHA drift or target present => exact BLOCKED/VERIFIED_ALREADY with evidence, continue others. Move **entire real calculation body** to one unique Owner; SOURCE same-signature/default/docstring thin wrapper. Call-time `facade=sys.modules[__name__]` for SOURCE helper/argparse/Mapping/monkeypatch; Owner must not import SOURCE. Preserve original exception, return schema, order, identity and CLI parser defaults. Do not call `main`, replay/restore/clear, broker, Guard, scheduler, database or live network. One fake-only normal `python -m pytest -q tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py` EXIT=0 with original-preimage AST parity for all eight, no -O/full-suite/hosted CI requirement.

### B39-1 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m29_disaster_recovery_drill.py::_replay_metrics` | SOURCE_GIT_BLOB=`a8a340b97a61ce953faf3d30c0dff7ca4cb86a56` (canonical=actor at issuance)
TARGET=`scripts/diagnostics/run_m29_disaster_recovery_drill_replay_metrics.py::_replay_metrics` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Return six-key in-memory dict: replayed/executed/blocked/pending intent totals and fill_qty_total int; fill_notional_total float; preserve key order.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=empty/None/zero/string numerics/bad conversion exception; no replay/restore.
TEST=`tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### B39-2 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m29_disaster_recovery_drill.py::_replay_parity_ok` | SOURCE_GIT_BLOB=`a8a340b97a61ce953faf3d30c0dff7ca4cb86a56` (canonical=actor at issuance)
TARGET=`scripts/diagnostics/run_m29_disaster_recovery_drill_replay_parity_ok.py::_replay_parity_ok` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Compare five integer counters in fixed order and fill_notional_total float tolerance >1e-9; return (not failures, failures list).
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=equal/multiple mismatches/order/1e-9 boundary, invalid number exception; no replay.
TEST=`tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### B39-3 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m29_disaster_recovery_drill.py::_build_parser` | SOURCE_GIT_BLOB=`a8a340b97a61ce953faf3d30c0dff7ca4cb86a56` (canonical=actor at issuance)
TARGET=`scripts/diagnostics/run_m29_disaster_recovery_drill_build_parser.py::_build_parser` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Construct original argparse parser with working/archive/restored/report paths, day, inject-fail/no-clear/json flags; no parse_args/main.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=default/flag/usage/help parity via fake argv, patched argparse, no file mutation.
TEST=`tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### B39-4 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_exam_readiness_check.py::_item` | SOURCE_GIT_BLOB=`721630febbfadcb62940c4cc56486cf11bf047af` (canonical=actor at issuance)
TARGET=`scripts/diagnostics/run_m31_mock_exam_readiness_check_item.py::_item` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Return ordered id/title/required/passed/evidence dict with bool(required/passed) and str(evidence); keyword-only signature.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=required default, falsy/custom bool/string, key order, exception parity.
TEST=`tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### B39-5 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_exam_readiness_check.py::_build_markdown` | SOURCE_GIT_BLOB=`721630febbfadcb62940c4cc56486cf11bf047af` (canonical=actor at issuance)
TARGET=`scripts/diagnostics/run_m31_mock_exam_readiness_check_build_markdown.py::_build_markdown` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Render read-only Markdown from supplied in-memory stage_checks/runtime_profile/guardrails/checklist/missing_prerequisites; exact headings, checkboxes, numeric format, newline bytes.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=empty/full/malformed nested dict, missing rows, exact UTF-8 Markdown, no writes.
TEST=`tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### B39-6 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_mock_exam_readiness_check.py::_build_parser` | SOURCE_GIT_BLOB=`721630febbfadcb62940c4cc56486cf11bf047af` (canonical=actor at issuance)
TARGET=`scripts/diagnostics/run_m31_mock_exam_readiness_check_build_parser.py::_build_parser` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Construct original argparse with day/env/event-log/m30/m31 dirs, strict-session/allow-offhours and report options; no parse_args/main.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=defaults/flags/help/usage exact, patched argparse, no mock exam execution.
TEST=`tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### B39-7 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_severity_from_level` | SOURCE_GIT_BLOB=`e70a3e791dcc3381a848b1e44a93b5234214a2eb` (canonical=actor at issuance)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_severity_from_level.py::_severity_from_level` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=str(level or '').strip().lower(); incident->SEV-1, watch->SEV-2, else SEV-3.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=case/whitespace/None/custom str, exception parity.
TEST=`tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### B39-8 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m31_slo_incident_review_check.py::_ownership_from_level` | SOURCE_GIT_BLOB=`e70a3e791dcc3381a848b1e44a93b5234214a2eb` (canonical=actor at issuance)
TARGET=`scripts/diagnostics/run_m31_slo_incident_review_check_ownership_from_level.py::_ownership_from_level` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=str(level or '').strip().lower(); incident->primary_and_secondary_oncall, watch->primary_oncall, else none.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=case/whitespace/None/custom str, exception parity.
TEST=`tests/test_p15_rf063_20261103_02h_diagnostics_readiness_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

## VERIFIED RESERVE — B 6/6 (UNASSIGNED)
Actual bodies read; canonical=B exact SOURCE blob and exclusive TARGET 404 in both complete Git trees; pure in-memory or parser-only, no actual execution. Do not self-select.
1. RF-063 `scripts/diagnostics/run_m31_slo_incident_review_check.py::_to_epoch@e70a3e791dcc3381a848b1e44a93b5234214a2eb` → `scripts/diagnostics/run_m31_slo_incident_review_check_to_epoch.py::_to_epoch` (404 C+B); BODY=epoch numeric/ISO UTC conversion; no clock/IO; fake-only parity; UNASSIGNED.
2. RF-063 `scripts/diagnostics/run_m31_slo_incident_review_check.py::_utc_day@e70a3e791dcc3381a848b1e44a93b5234214a2eb` → `scripts/diagnostics/run_m31_slo_incident_review_check_utc_day.py::_utc_day` (404 C+B); BODY=call-time _to_epoch and UTC date format; fake-only parity; UNASSIGNED.
3. RF-063 `scripts/diagnostics/run_m31_slo_incident_review_check.py::_item@e70a3e791dcc3381a848b1e44a93b5234214a2eb` → `scripts/diagnostics/run_m31_slo_incident_review_check_item.py::_item` (404 C+B); BODY=keyword-only checklist dict projection; fake-only parity; UNASSIGNED.
4. RF-063 `scripts/diagnostics/run_m31_slo_incident_review_check.py::_build_markdown@e70a3e791dcc3381a848b1e44a93b5234214a2eb` → `scripts/diagnostics/run_m31_slo_incident_review_check_build_markdown.py::_build_markdown` (404 C+B); BODY=in-memory SLO/incident Markdown byte parity; fake-only parity; UNASSIGNED.
5. RF-063 `scripts/diagnostics/run_m31_slo_incident_review_check.py::_build_parser@e70a3e791dcc3381a848b1e44a93b5234214a2eb` → `scripts/diagnostics/run_m31_slo_incident_review_check_build_parser.py::_build_parser` (404 C+B); BODY=argparse construction only, no parse/main; fake-only parity; UNASSIGNED.
6. RF-063 `scripts/diagnostics/run_m31_mock_investor_exam_check.py::_env_bool@e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f` → `scripts/diagnostics/run_m31_mock_investor_exam_check_env_bool.py::_env_bool` (404 C+B); BODY=provided env dict bool parsing, no actual env read; fake-only parity; UNASSIGNED.

## ACCEPTANCE / #12
Finish B39-1..8 or item-specific SOURCE/TARGET/current SHA/FIRST_BLOCKER; preserve completed B38. Report measured START_KST/END_KST/ELAPSED_MIN, B HEAD before/after, full-root tree, all SOURCE pre/post/Owner/test blobs, normal command EXIT/PASS, non-force push and remote refetch. Terminal Git auth failure permits only approved **non-force expected-head exact-tree full-root** connector delivery, never a root-only-tests tree, force or history rewrite; otherwise PUSH_BLOCKED. B39 diagnostics-only cannot be called resolver G3. Code/test B branch only, no C02/D00/C03/C04/C05/RF/STATUS edits.