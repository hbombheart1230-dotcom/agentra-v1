# C02 — Claude A | ORDER_ID=A-20261103-02-C03 | RF-032 PEER | A49 NEW_READY=8/8 | A48 REMOTE_DONE=8/8 | RESERVE_VERIFIED=6/6

## START / authoritative remote pins
C03 verified A48 [#11 6582478489](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6582478489) remote A `87548b34d58308bc3686842bdd42ec0d10f767e7`, 8/8 BODY MOVEs, normal `python -m pytest -q tests/test_p15_rf032_20261103_00h_authority_feedback_pure_owners.py` EXIT=0/PASS=147; C04 [#36 6582622282](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6582622282) integrated exact A48 12/12 blobs at `08ecb864`. **A48 and A1-A47 must not be reimplemented/retested/recounted.** Previous C02 blob `4c7fc3eb064f84b7e848e3fd1761ca4b2b81856e`. If a starting order is genuinely underway, finish safe items before switching; this new order does not retroactively cancel.

First shell `python -m pytest --version`; if missing `python -m pip install --user pytest`, recheck. Fetch **latest remote** `integration/p1.5:docs/refactor/work_orders/C02_CLAUDE_CURRENT.md` by branch, not cached checkout; report exact REMOTE_CANONICAL_HEAD, C02_BLOB_SHA, ORDER_ID in #11. Read only this C02 as work instruction, not D00/RF/INDEX. All SOURCE and TARGET pins independently checked on complete nontruncated Git trees: canonical `08ecb864acce08d92aad03b31be82a1b968f3425` tree `e4f010ef9a83bede487255a913c401fa975188d0` (5754 entries), A `87548b34d58308bc3686842bdd42ec0d10f767e7` tree `7bc2d5eff1dec1bfcd01e390308d004fcf88957e` (5320), B `0ea7c49be412401ea087c031a8af9dc07d7ce654` tree `cb71b1174adacb654cc5d3561ca084c6e847f3dc` (4705). Both new targeted tests absent on respective actor and canonical. RF-032 and RF-063 FILE_COVERAGE owner paths verified against their RF implementation inventories. C03 reviewed actual bodies, no source/target cross-actor overlap. Skill `.agents/skills/agentra-contract-guard/SKILL.md@f2fe45fd856f65f5f7b5a3b710317baf1bf9ad5d` used manually as non-authoritative checklist; auto-load NOT_VERIFIED, no new gate.

## DONE-FIRST / whole RF gate and safe boundary
Latest C05 [#36 6582764054](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6582764054): PENDING38 / DEV7 / PEER2 / DONE46, unresolved47. RF-030 G1 partial/G2 pending/G3 canonical fake smoke pending; RF-063 resolver/consumer closure not met; RF-032 whole G1 **BLOCKED_POLICY** validation-id/Writer/UEF despite scoped A48 G3_REUSE. C04 owns canonical RF-030 smoke and integration, C05 alone RF DONE/STATUS. A49 is bounded in-memory RF-032 work, not whole RF DONE; do not modify frozen oracle, RF-074, protected Writer/UEF/Guard, real/paper orders, live network, OS/DB, RunLab or operational state. Other RF closeout work lacks validated A-safe actor/canonical dependency-identical assignment; C03 retains triage, A must not self-select.

## A49 — eight individually verified independent pure BODY MOVE items
Before each item re-fetch exact SOURCE/TARGET Git blob on A; if changed, target already present or cross-owner overlap, report item-specific BLOCKED/VERIFIED_ALREADY and continue other safe items. Move actual complete body to one Owner, SOURCE same-signature thin wrapper; preserve call-time SOURCE helper/Mapping/Counter facade seams. Owner may accept `facade=sys.modules[__name__]` passed by wrapper but **must not import SOURCE**. Preserve source defaults/docstring, exception order, return identity, dict/Markdown byte order. No IO or external services in tests. One new fake-only targeted normal `python -m pytest -q tests/test_p15_rf032_20261103_02h_no_trade_alignment_owners.py` EXIT=0 with original-preimage AST vs new Owner/wrapper parity for **all eight**; no mandatory -O/full suite/hosted CI.

### A49-1 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/no_trade_attribution.py::_mapping` | SOURCE_GIT_BLOB=`967aca16db2926cc00b0a7761d1534cf4b84540b` (canonical=actor at issuance)
TARGET=`libs/reporting/evaluation/no_trade_attribution_mapping.py::_mapping` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Mapping identity-or-empty: if isinstance(value, Mapping) return same object, else {}; preserve facade.Mapping use-time.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=dict/subclass identity, None/string, monkeypatch Mapping, exception/identity.
TEST=`tests/test_p15_rf032_20261103_02h_no_trade_alignment_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### A49-2 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/no_trade_attribution.py::_num` | SOURCE_GIT_BLOB=`967aca16db2926cc00b0a7761d1534cf4b84540b` (canonical=actor at issuance)
TARGET=`libs/reporting/evaluation/no_trade_attribution_num.py::_num` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=None or empty string => None; float(value), catching TypeError/ValueError only; do not catch RuntimeError.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=None/empty/zero/custom float, invalid string, propagated RuntimeError.
TEST=`tests/test_p15_rf032_20261103_02h_no_trade_alignment_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### A49-3 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/no_trade_attribution.py::_pct` | SOURCE_GIT_BLOB=`967aca16db2926cc00b0a7761d1534cf4b84540b` (canonical=actor at issuance)
TARGET=`libs/reporting/evaluation/no_trade_attribution_pct.py::_pct` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Call facade._num(value) at use time; None => '-', otherwise format 4 decimals with %.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=negative/zero/invalid, patched _num, exact 4-decimal bytes.
TEST=`tests/test_p15_rf032_20261103_02h_no_trade_alignment_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### A49-4 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/no_trade_attribution.py::_top` | SOURCE_GIT_BLOB=`967aca16db2926cc00b0a7761d1534cf4b84540b` (canonical=actor at issuance)
TARGET=`libs/reporting/evaluation/no_trade_attribution_top.py::_top` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Counter.most_common(limit) preserving tie order, filter falsy key, cast counts int and keys name.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=tie/empty key/limit 0/negative/Counter subclass and exact row ordering.
TEST=`tests/test_p15_rf032_20261103_02h_no_trade_alignment_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### A49-5 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/no_trade_attribution.py::_q9_window_view` | SOURCE_GIT_BLOB=`967aca16db2926cc00b0a7761d1534cf4b84540b` (canonical=actor at issuance)
TARGET=`libs/reporting/evaluation/no_trade_attribution_q9_window_view.py::_q9_window_view` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Read only row scanner_control.top1_symbol, strategist_selection.selected_symbol, commander_final selected_symbol/decision/monitor_intent/reason/detail/monitor_reason and nested monitor_observation.reason; omit nonmapping groups, preserve key order and docstring.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=empty/nested/nonmapping/partial rows, patched Mapping, input unchanged, exact projection schema.
TEST=`tests/test_p15_rf032_20261103_02h_no_trade_alignment_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### A49-6 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_mapping` | SOURCE_GIT_BLOB=`8774bea29dd8ebd83283b28c5109e5fc6210fd1a` (canonical=actor at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_mapping.py::_mapping` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=Mapping identity-or-empty; no copy of Mapping; dynamic facade.Mapping.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=dict/subclass identity, None/scalar, patched Mapping.
TEST=`tests/test_p15_rf032_20261103_02h_no_trade_alignment_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### A49-7 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_rows` | SOURCE_GIT_BLOB=`8774bea29dd8ebd83283b28c5109e5fc6210fd1a` (canonical=actor at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_rows.py::_rows` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=List comprehension over (value or []), retaining only Mapping rows in original order and identity; preserve single iteration and generator behavior.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=None/empty/mixed/generator, Mapping subclass, input identity, exception parity.
TEST=`tests/test_p15_rf032_20261103_02h_no_trade_alignment_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

### A49-8 | RF-032 | NEW_BODY_MOVE
SOURCE=`libs/reporting/evaluation/scanner_alignment_root_cause.py::_num` | SOURCE_GIT_BLOB=`8774bea29dd8ebd83283b28c5109e5fc6210fd1a` (canonical=actor at issuance)
TARGET=`libs/reporting/evaluation/scanner_alignment_root_cause_num.py::_num` | TARGET=404 on canonical and actor (verified nontruncated tree)
ACTUAL_BODY=None or '' => None; float conversion; catch TypeError/ValueError only.
MOVE=Transfer entire real calculation body into this single exclusive Owner; SOURCE original signature/default/docstring becomes thin call-time facade wrapper. Owner must not import SOURCE; preserve monkeypatch, exception, formatting, ordering, identity and caller behavior. Do not modify operational call sites.
TARGETED_NORMAL_CASES=0/negative/invalid/custom float, RuntimeError propagation, original AST parity.
TEST=`tests/test_p15_rf032_20261103_02h_no_trade_alignment_owners.py`; compare original preimage AST vs wrapper/Owner on fake in-memory inputs. If drift/target collision, report exact SHA/FIRST_BLOCKER and continue next assigned item.

## VERIFIED RESERVE — A 6/6 (UNASSIGNED, not actor discretion)
Actual bodies read; exact SOURCE blob canonical=A and unique TARGET 404 in both complete Git trees; in-memory only; not part of A49. Do not execute unless future C03 order.
1. RF-032 `libs/reporting/evaluation/scanner_alignment_root_cause.py::_symbol@8774bea29dd8ebd83283b28c5109e5fc6210fd1a` → `libs/reporting/evaluation/scanner_alignment_root_cause_symbol.py::_symbol` (404 C+A); BODY=Mapping symbol or scalar -> str(...).strip(), preserve falsy fallback; fake-only parity; UNASSIGNED.
2. RF-032 `libs/reporting/evaluation/scanner_alignment_root_cause.py::_selected_rank@8774bea29dd8ebd83283b28c5109e5fc6210fd1a` → `libs/reporting/evaluation/scanner_alignment_root_cause_selected_rank.py::_selected_rank` (404 C+A); BODY=nested selection selected_rank/selected_candidate.rank, _mapping/_num facade dynamic; fake-only parity; UNASSIGNED.
3. RF-032 `libs/reporting/evaluation/scanner_alignment_root_cause.py::_score_gap@8774bea29dd8ebd83283b28c5109e5fc6210fd1a` → `libs/reporting/evaluation/scanner_alignment_root_cause_score_gap.py::_score_gap` (404 C+A); BODY=top1 vs selected score, 6-decimal rounding, missing returns None; fake-only parity; UNASSIGNED.
4. RF-032 `libs/reporting/evaluation/scanner_alignment_root_cause.py::_outcome_return@8774bea29dd8ebd83283b28c5109e5fc6210fd1a` → `libs/reporting/evaluation/scanner_alignment_root_cause_outcome_return.py::_outcome_return` (404 C+A); BODY=evaluation.realized_outcome.net_return_pct fallback model.outcome; fake-only parity; UNASSIGNED.
5. RF-032 `libs/reporting/evaluation/scanner_alignment_root_cause.py::_impact_score@8774bea29dd8ebd83283b28c5109e5fc6210fd1a` → `libs/reporting/evaluation/scanner_alignment_root_cause_impact_score.py::_impact_score` (404 C+A); BODY=sum negative return values and round to 4 decimals; fake-only parity; UNASSIGNED.
6. RF-032 `libs/reporting/evaluation/scanner_alignment_root_cause.py::_diagnostic_kind@8774bea29dd8ebd83283b28c5109e5fc6210fd1a` → `libs/reporting/evaluation/scanner_alignment_root_cause_diagnostic_kind.py::_diagnostic_kind` (404 C+A); BODY=OUTCOME_CONDITIONED_CAUSES/EVIDENCE_GAP_CAUSES dynamic lookup; fake-only parity; UNASSIGNED.

## ACCEPTANCE / #11
Complete A49-1..8 or each exact SOURCE/TARGET/SHA FIRST_BLOCKER; do not stop after first PASS or short runtime. Report measured START_KST/END_KST/ELAPSED_MIN, remote A HEAD before/after, full-root tree, all SOURCE pre/post/Owner/test blobs, normal command EXIT/PASS, non-force push and remote refetch. KEEP/ALREADY=0 new moves. If push blocked, report PUSH_BLOCKED and keep safe code work; never force. C04 selects integration/G3, C05 RF/STATUS/DONE. No D00/C01/C03/C04/C05/RF/STATUS edits.