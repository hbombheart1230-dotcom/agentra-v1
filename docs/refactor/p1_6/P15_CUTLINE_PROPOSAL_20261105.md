# P1.5 컷라인 제안 (2026-11-05) — 중단·정리 후 P1.6 전환

> **상태: PROPOSAL / 미승인 / 미커밋.** 이 문서는 결정이 아니라 제안이다. D00·CURRENT·STATUS·RF 대장은 지팀장만 수정하므로, 승인되면 지팀장이 해당 문서에 반영한다. 코드·브랜치·런타임은 이 문서로 바뀌지 않는다.

## 1. 한 줄 요약

1.5를 "끝까지" 밀지 않고, **이미 끝난 RF를 동결하고 진행 중인 3개 RF만 마무리**한 뒤 나머지는 P1.6 인벤토리로 넘긴다. Docker 제거는 1.5와 섞지 않고 P1.6 첫 가지치기 항목으로 별도 진행한다.

## 2. 근거 수치

`docs/refactor/plan/RF_TASK_LEDGER.jsonl` (origin/integration/p1.5 `aa80c42b`) 기준.

| 구분 | RF | MOVE_BODY | KEEP_IF |
|---|---|---|---|
| 05_DONE | 43 (+3 미분류) | 120 | 293 |
| 03_PEER_REVIEW | 2 | 7 | 7 |
| 02_DEVELOPING | 7 | 4 | 344 |
| 01_PENDING | 38 | 44 | 2,165 |
| 합계 | 90 (+3 미분류) | 175 | 2,809 |

- 작업 2,984개 중 코드를 실제로 옮기는 `MOVE_BODY`는 175개(6%)다. 나머지는 "그대로 둬도 되는지" 확인하는 `KEEP_IF`다.
- 완료되지 않은 47개 RF 중 **35개는 MOVE_BODY가 0개**(KEEP_IF만 2,516개)이고, 12개 RF에만 MOVE_BODY 55개가 남아 있다.
- **RF-028/029/037 분류 완료 (2026-11-05)**: 세 RF 모두 설계 문서에 실측 함수 이동이 없고(소스=타겟, 85+38+21=144개 파일) 이력도 KEEP_NOOP이라 KEEP_IF 144행으로 원장에 추가했다. 원장은 **3,128행 / 93개 RF**로 STATUS와 일치한다(MOVE_BODY 175 변동 없음).
- **불일치 해소 (2026-11-05)**: 지팀장 대조로 STATUS(RF 93개·DONE 46개)가 맞고, 원장이 15개 RF를 빠뜨린 것으로 확인됐다. 오너 권한 지시로 Codex가 12개 RF(행 817개, 모두 KEEP_IF)를 원장에 추가했다. **RF-028, RF-029, RF-037은 문서만으로 KEEP/MOVE를 판정할 수 없어 아직 원장에 없다**(모두 DONE). 따라서 원장은 90개 RF이고 3개가 남아 있다.

## 3. 컷라인

### IN — 동결 (손대지 않음)
- 05_DONE RF 전부(STATUS 기준 46개, 원장 43개 + 미분류 3개). 재개발 금지.

### FINISH — 1.5 안에서 마무리 (3개 RF, MOVE_BODY 11개)
| RF | 단계 | MOVE | 담당(원장) | 비고 |
|---|---|---|---|---|
| RF-032 | 03_PEER_REVIEW | 7 | Claude A | **정정(Codex B 피어 검토 2026-11-05)**: 원장 MOVE 7개는 `cumulative_improvement_review`가 아니라 `uef5/historical_recompute.py`(UEF 보호 영역) 함수이며 타겟 미생성. A의 분리 2건은 원장 밖 별도 이동 |
| RF-021 | 02_DEVELOPING | 1 | Claude A | |
| RF-045 | 02_DEVELOPING | 3 | Codex B | **KEEP_VERIFIED (2026-11-05)**: 3개 함수는 event_logger.py 내부 전용이고 비공개 헬퍼에 묶여 있어 분리하면 순환 import나 헬퍼 복제가 생긴다. 코드 변경 없음. B의 log_maintenance·http_client 수정은 반영 완료 |

### DEFER-A — 1.6 인벤토리로 이관 (MOVE-only 9개 RF, MOVE_BODY 44개)
RF-010, 011, 012, 022, 026, 030, 042, 048, 049 (모두 01_PENDING). 실제 코드 이동이라 가치는 있으나 1.5 완료 조건에서 뺀다. 1.6 Gate C에서 CONSOLIDATE 후보로 재평가한다. **승인 시 FINISH로 올릴 수 있는 항목이다.**

### DEFER-B — 완료 조건에서 제외 (KEEP-only 35개 RF, KEEP_IF 2,516개)
"유지해도 됨" 확인 작업. 1.6 Feature Disposition Ledger의 증거로 쓰고 1.5 완료율 계산에서 뺀다. 새로 원장에 들어온 RF-072~078(대기, 담당 없음)은 모두 KEEP_IF만 있어 여기에 속한다.

## 4. A·B 브랜치 처리

원본은 보존 태그 `archive/p15-20261105/*`(로컬)에 있다. 분류 결과: `classify.json`(스크래치).

**가져올 것 (구조 무관, integration이 분기 후 건드리지 않은 파일)**
- A 11개: `libs/llm/model_catalog_store.py`, `libs/market/global_sentiment.py`, `libs/market/korea_bond_yields.py`, `libs/performance/strategy_memory.py`, `libs/reporting/baseline_samsung_hynix/forward_validation/{cumulative,shadow_comparison}.py`, `.../q9_comparison.py`, `libs/reporting/evaluation/cumulative_improvement_review.py`, `libs/reporting/opening_rank1_shadow/latent_forward.py`, `libs/reporting/quant_trade_diagnosis/writer.py`, `libs/runtime/monitor_exit/policy_map_builder.py`
- A 신규 소스 2개: `cumulative_improvement_review_candidate_rows.py`, `..._rank_row.py` (RF-032)
- B 14개: `libs/agents/commander/__init__.py`, `libs/core/{http_client,log_maintenance}.py`, `scripts/diagnostics/run_m30_final_golive_signoff.py`, `scripts/examples/demo_m22_*.py`, `scripts/maintenance/run_log_maintenance.py`, `scripts/refactor/shared_role_contracts.py`, `scripts/research/run_integrated_trade_validation.py` 및 관련 테스트
- 가져오는 방식은 통째 병합이 아니라 파일 단위 선별이며, 각 묶음마다 normal과 `python -O` 테스트를 돌린다.

**보류**
- A의 `intraday_report_*_projection.py` 5개(양쪽 수정, 브랜치가 약 1시간 최신): 테스트로 정답을 가려야 한다.
- B의 폴더 구조(`brief_parts/`, `read_models/`, `agent_output_parts/`): 이번에 채택하지 않는다. 채택 시 p153·p159 가드 테스트 33개가 깨진다(2026-11-05 확인). 1.6에서 구조를 확정할 때 가드와 함께 다룬다.
- A의 RF 번호 없는 `test_p15_*` 60개, B의 31개: 새 커버리지인지 중복인지 분류 후 결정.

**버림**: 두 브랜치의 `CURRENT.md`, patch_notes, `HANDOFF_*`, work_orders 증거 문서(정본은 integration).

**오너 결정 (2026-11-05)**: RF-032의 UEF 이동 7개(RF-032-0001~0007)는 **P1.6으로 이관**한다. RF-032는 A의 분리 2건(`_rank_row`, `_candidate_rows`) 반영으로 1.5 범위를 마친 것으로 기록하고, 7개는 1.6 Gate C에서 UEF 승인과 함께 다룬다. 따라서 1.5 마무리 대상은 RF-021(KEEP_VERIFIED)과 RF-045뿐이다.

## 5. 동결 조건 (P1.6 Gate A 입력)

1. FINISH 3개 RF가 `05_DONE`이 된다 (G1 BASE parity, G2 normal·`-O` 테스트, 독립 피어 `PASS`와 실제 종료 코드).
2. 기존 실패 2건을 해결하거나 사유와 함께 기록한다: `test_p159_current_owner_contract_gates.py::test_t3_changed_paths_contain_no_authority_surface`와 p153의 1건.
2-1. 기존 실패 추가 기록 (2026-11-05, A 파일 가져오기 중 확인): `tests/test_decision_trace_ledger.py::test_decision_trace_ledger_collects_strategist_scanner_monitor`는 `libs/runtime/decision_observability.py:29`에서 `libs.runtime`의 `decision_observability_dedupe_non_empty`를 import하지 못해 실패한다. A 변경을 빼고 돌려도 동일하게 실패하므로 A와 무관한 기존 실패이며, Gate A 전에 해결하거나 사유를 남긴다. **범위 확대**: A 관련 테스트 131개 파일을 돌린 결과 normal·`-O` 모두 실패 257 + 오류 5(동일 집합)였고, A 변경 없는 HEAD에서도 정확히 같은 262건이 나왔다(A가 새로 만든 실패 0건). 원인은 주로 `decision_observability_dedupe_non_empty` import 실패(140건)와 `RF93 missing work orders`(77건, work_orders 증거 문서 부재)다.
2-2. 기존 실패 원인 분석 (2026-11-05): 262건 중 140건은 `libs/runtime/decision_observability.py`가 import하는 소유 모듈 2개(`decision_observability_dedupe_non_empty`, `..._extract_failed_names`)가 integration에서 빠져 있던 것이 원인이었다(커밋 `37216b33`에서 누락, B 브랜치에만 존재). 두 파일을 복원해(`a75d037b`, 원래 함수 본문과 동일 확인) **262 → 122건(새 실패 0)**. 남은 122건의 분류:
   - 93건: B 시기의 계약 테스트(`test_p15_commander_pure_v1_admission` 64, `test_p15_b_versioned_contract` 19, `test_shared_role_contracts` 10)가 옛 큐 경로(`docs/refactor/plan/{pending,verification,done}/RF-*.md`, 현재는 `plan/queue/<단계>/<소유자>/`)와 clone에 없는 SHA(`54bebe5e…`)를 고정한다. 코드 결함이 아니라 낡은 테스트다. P1.6 Gate A에서 갱신 또는 폐기.
   - 29건: UEF 계열 10건(`test_uef2a_forward_policy_contract` 8, `test_uef5_1_clean_evidence_registry` 2, 보호 영역이라 오너 승인 전 수정 금지), `test_work_monitor_m9_offline` 6, `test_p15_rf033_20261101_21h_original_owner_parity` 5(BLOCKED_PIN `reaction_reader.py`), `test_llm_model_policy` 3, `test_p164_t4c_extraction_gates` 2, `test_work_reporter_seed_migration` 1. 개별 원인 미분석.
3. 전체 회귀(normal·`-O`)가 통과한다. 이번에 확인한 범위는 가드 테스트 3개 파일뿐이다.
4. RunLab 이슈 #32(SELL 제출 불일치, OCI 출처 UNKNOWN)는 코드 DONE과 별개로 `OPEN/RUNTIME_PENDING`이다. 동결 문서에 미해결로 명시한다.
5. 기준 SHA와 태그를 기록하고, 오너가 승인한다.

## 6. 운영 정리 (지팀장 조치 필요)

- 문서·RF·STATUS·patch_notes 수정은 지팀장 한 곳으로 유지하고, 에이전트가 문서에 직접 쓰지 않게 한다.
- 컷라인 승인 후 C01~C06 지시를 FINISH 3개 RF 기준으로 좁힌다. 예약 작업을 새로 만들지는 않는다.
- 상태 변경은 이벤트 로그 원장(append-only)과 단일 쓰기 도구로 일원화하는 안을 별도 제안한다.

## 7. P1.6 진입 순서

1. Gate A: 위 동결 조건 충족, 기준 SHA 확정.
2. Gate B: 정체성·역할 경계 확정(MASTER_PLAN 기준).
3. Gate C: Feature Disposition Ledger. **첫 항목으로 Docker 제거**.
   - 현재 실거래 정본 런타임이 Docker다(P1.3, 10/2). 제거는 정리가 아니라 런타임 변경이다.
   - 호출 관계 증거를 남기고 대상은 `runtime_mode.py`, 시작·감시 스크립트, `scripts/docker_healthcheck.py`, `deploy/`, `tests/deploy`와 관련 테스트다.
   - 별도 오너 승인과 RunLab 검증이 필요하며 롤백은 `deploy/trading/rollback-to-host.ps1`로 한다.
4. Gate D: 오케스트레이션 비교 시 TradingAgents(Apache-2.0)를 참고한다. 후보는 결정 로그와 사후 반성 메모리, 2단계 모델 구성, 체크포인트 재개, 알파 채점 백테스트다. 데이터 소스(Yahoo·SEC)와 실행부는 가져오지 않는다.

## 8. 오너 결정 (2026-11-05, 오너가 추천안 일임)

1. DEFER-A 9개 RF는 **1.6으로 이관**한다. 1.5 마무리는 RF-032, 021, 045 세 개.
2. 원장과 STATUS 불일치는 **원장 누락으로 확정**, 12개 RF 보완 완료(3개는 미분류로 잔여).
3. 보존 태그 `archive/p15-20261105/*` 5개는 **원격에 올렸다**.
4. B 폴더 구조는 **1.6에서 가드 테스트와 함께 다시 다룬다**.
5. Docker 제거는 **1.6 Gate C 인벤토리 이후**에 하고, 그때 별도 오너 승인과 RunLab 검증을 받는다.

## 9. 남은 일

- ~~RF-028, 029, 037 분류~~ 완료(위 2절). 지팀장은 KEEP_IF 판정만 확인하면 된다.
- ~~원격 푸시~~ 완료. ~~CURRENT·C01·C02 개정~~ 완료(D00·C03~C06은 손대지 않음).

**오너 결정 (2026-11-05)**: 기존 실패 122건(낡은 B 계약 테스트 93, 개별 미분석 29 중 UEF 10 포함)은 **P1.6 Gate A로 이관**한다. 1.5에서는 더 고치지 않는다.

동결 전 남은 것:
1. 전체 회귀(normal·`-O`) 1회 실행해 실패 집합을 122건 기준선으로 고정(지금까지는 부분 실행만 함).
2. 지팀장: RF-021·RF-045를 KEEP_VERIFIED로, RF-032를 "A 2건 반영 / UEF 7건 1.6 이관"으로 원장·STATUS에 반영. 에이전트는 상태값을 바꾸지 않았다.
3. 동결 문서에 RunLab 이슈 #32를 `OPEN/RUNTIME_PENDING`으로 명시.
4. 기준 SHA와 태그 확정, 오너 승인.

보류한 브랜치 잔여물(1.6 입력): A의 `intraday_report_*_projection.py` 5개(양쪽 수정), 번호 없는 `test_p15_*` 약 90개, B의 3개 파일(commander `__init__`, `run_m30_final_golive_signoff`, `shared_role_contracts`)과 B 폴더 구조.

이 PC 밖/오너 확인: GPT·Codex 앱 쪽 예약 작업이 남아 있는지, 실패한 Codex MCP 등록 정리(`claude mcp remove codex`).
