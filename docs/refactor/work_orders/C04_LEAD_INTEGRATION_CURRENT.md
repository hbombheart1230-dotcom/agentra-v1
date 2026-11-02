# C04 — 지팀장 · 선별 통합/CI

## 최신 우선 계약 — 구현 변경 묶음만 통합

C01/C02에서 나온 **실제 함수 이동 source+target blob**과 해당 normal targeted exit를 대조해 여러 준비 RF를 한 회차에 통합. 관련 경계 기존 PASS 증거 재사용, 변경 없는 정당한 KEEP은 새 테스트/CI dispatch 0. T00~T09 및 `rf_details/INDEX.md`의 SOURCE/TARGET Owner와 교차 RF 신규 경로 충돌 점검. 아래 이미 DONE인 RF-016/028/029 등 고정 반복 통합 지시는 신규 delta 없으면 적용 금지. 실거래/운영 효과 보호.


## FAST-3 G3 재실행 중복 방지 — C04 실제 판단 절차
- **1단계 대상 검증:** RF의 G1 원격 OWNER SOURCE SHA와 integration의 실제 파일별 Git blob을 대조하고, G2의 정확 SOURCE SHA·영향 테스트/실제 exit0 증거를 확인한다. 단순 문서 HEAD 변경으로 `SOURCE_CHANGED`를 판단하지 않는다.
- **2단계 증거 재사용:** 같은 대상 source+consumer 경계, 동일 테스트·의존성·CI 워크플로 상태에 대해 이미 성공한 정상 smoke/targeted pytest 또는 exact relevant CI 증거가 있으면 `G3_REUSE`로 수용한다. SOURCE 또는 테스트/의존성/보호 경계가 바뀌었으면 관련 범위만 재검증한다. 이전 기록의 PASS가 현재 코드에 해당하는지 불명확하면 재사용 불가, 하지만 full suite로 확대하지 않는다.
- **3단계 명시적 분기:** `KEEP_BLOB_IDENTICAL + VALID_RELEVANT_EVIDENCE` ⇒ **새 CI/pytest 실행 요청 0**, C05에 G3 증거 전달. `SOURCE_CHANGED` 또는 `TEST/DEPENDENCY/WORKFLOW_CHANGED` ⇒ 대상 변경분을 최소 통합하고 **관련 smoke/pytest 1회 또는 유효한 CI 1개** 확인. `DOCS_STATUS_ONLY` ⇒ **신규 CI dispatch 0 / smoke 반복 0**. `NO_MATCHING_EVIDENCE` ⇒ targeted smoke 1회만 실행(실행 환경 부재 시 G3 BLOCKED, 성공으로 간주 금지).
- **4단계 중복 dispatch 락:** 실제 GitHub Actions 수동 dispatch 이전 **기존 run의 head SHA, workflow/테스트 범위, conclusion을 조회**하고, 동등하게 성공한 run이나 같은 범위의 진행 중 run이 있으면 또 요청하지 않는다. 한 번 실행한 후 해당 `RF | owner blobs | integration/source SHA | relevant test list | PASS/FAIL | run_id 또는 local command | reuse/new/blocked` 근거를 #36 한 번만 보고한다. `python -O`/full hosted CI는 FAST-3 강제요건 아님.
- GitHub Actions `push` 트리거/branch protection·workflows·frozen oracle는 변경하지 않는다. 현재 `.github/workflows/p15-shared-candidate.yml`은 코드/테스트 변경 Push에서 자동 실행될 수 있으므로 이것을 삭제/비활성화한다고 주장하지 않는다. **중복 수동 실행 요청만 차단**하고 정상적인 자동 안전 CI는 유지한다.

## FAST-3 간소 통합 우선 (2026-10-29 승인)
- D00 §2 FAST-3가 아래 구 C1~C7/full independent C4/매 RF 전체 hosted normal/-O CI 요구보다 우선한다. **G1/G2 MET인 RF를 G3로 처리**한다. C05의 과거 7개 전수 수용을 기다리지 말고 실제 새로운 G1/G2 상태를 원격에서 확인한다.
- KEEP이면 해당 코드의 integration blob 동일성 확인 후 기존 정상 smoke/CI evidence 1개로 G3 제출 가능. 변경 있으면 최소 파일 선택 통합 후 **변경 경계 관련 smoke/pytest 1회** 또는 해당 integration SHA의 기존 관련 CI 성공으로 G3 제출한다. 전체 suite, -O 반복, 반대 전체 peer, 새 hosted CI 매번 강제하지 않는다.
- RF-016/028/029 및 RF-051/054/058은 DONE이므로 동일 SHA 재검증·재통합 금지. 새 C01/C02 G1/G2 실제 SOURCE와 RF Owner를 우선하고, 통합 결과 없으면 G3를 꾸며내지 않고 BLOCKED(scope/명령/NEXT). #36에는 신규 근거만 제출.
- mock/paper 실행은 모의 모드·계정이 확인된 환경에서만, 실제 런검증은 별도 단계. 실계좌 real mode는 무승인 실행 금지.

**입력:** [Issue #11 Claude A](https://github.com/hbombheart1230-dotcom/agentra/issues/11) · [Issue #12 Codex B](https://github.com/hbombheart1230-dotcom/agentra/issues/12) · [Issue #32 RunLab](https://github.com/hbombheart1230-dotcom/agentra/issues/32)의 **새 댓글 delta만** → C05가 실제 `04_LEAD_ACCEPTANCE`로 이동한 RF. [D00](D00_ENGINEERING_DELIVERY_POLICY.md) 준수. [#36](https://github.com/hbombheart1230-dotcom/agentra/issues/36)은 결과 출력 전용. 오래된 A/B HANDOFF 재독·갱신 금지.

## 현재 상태 — 2026-11-02 18h KST / 미종결 RF 우선

- **정본 통합 기준:** `4fdce6eac9c1681d80a74b6f40fb43cf86081443` (tree `51046944cc82f76e873a2cfeff9e50c649664b01`); #11 A42 `c845ba697cd5be3002a85e436f67e43592e851ed`, #12 B35-6 `4ffc847994952f9d7c8f7553b7c4ff76d2a72602`. C03 CLOSEOUT_CANDIDATES #36 [6573212384](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6573212384). 정확 SOURCE/Owner/test blob 및 G2 exit0 확인한 범위만 최소 통합.
- **RF-032 A42 신규 선택 통합:** `libs/reporting/evaluation/loss_decomposition.py`에서 `_to_float,_parse_ts,_iter_days,_checkpoint_return,_rank_bucket,_candidate_rows,_group_forward,_realized_trade_summary` 8개를 대응 단일 Owner 8개로 이동한 actor 소스/Owner/test 10개 경로. SOURCE preimage canonical=actor-parent `87544f1ad77e164389fce354c02680d70b98f7f7`; after `bbe3777bbf339812766aed8816818939ce788242`. 정상 G2 `python -m pytest -q tests/test_p15_rf032_20261102_18h_loss_decomposition_owners.py` actor **180 PASS EXIT0**. 선택 G3_REUSE MET(정확 10 blob), **whole G1 BLOCKED_POLICY** validation-id/Writer/UEF 보호 승인 대기.
- **RF-063 B35-6 신규 선택 통합:** `scripts/diagnostics/benchmark_operator_visibility_memory.py::_target_day_events_for_run` → `benchmark_operator_visibility_memory__target_day_events_for_run.py`, test `tests/test_p15_rf026_20261102_15h_feature_regime_observability_owners.py` 갱신, 3경로. SOURCE preimage canonical=actor-parent `345752dc4665d7b54630684141ac0adf484ecca7`; after `fe87c11dabf1f5221ebed48dfd4e925e48229ae7`. 정상 G2 `python -m pytest -q tests/test_p15_rf026_20261102_15h_feature_regime_observability_owners.py` actor **3 PASS EXIT0**. FILE_COVERAGE `b46bcb1f29ed3c0a133b059d690173c195c81bf9`가 이 SOURCE를 **RF-063**으로 배정; 과거 B35-5 `_filler_row` 선택 통합의 RF-026 표기는 RF-063으로 정정(코드/증거 재실행 없음). 선택 G3_REUSE MET, **whole RF-063 G3 BLOCKED** B-04 facade/seven Owners 및 `llm_artifacts.py` resolver 의존성.
- **RF-030 CLOSEOUT 최우선:** 정본 `operator_visibility.py@bb6e97a72f94412ff9ca818dbf2a03d788dddf48`, `operator_visibility_build_run_contexts.py@db45fb0e06aee58c5d7938ad7f59801c11fb6191`, `tests/test_p15_rf030_20261102_02h_run_contexts.py@3b7c48e9b98f699f8f3def7314ef8bb2e8a07330`. 정본 fake-only normal targeted smoke EXIT0 또는 dependency-identical 과거 증거 전 **G3 PENDING**. C03/C05 whole G1/G2 별도 조정 필요.
- **기타 whole HOLD:** RF-026 RF021/026 cold-import G1 BLOCKED_POLICY, RF-032 validation-id/Writer/UEF G1 BLOCKED_POLICY, RF-065 protected Writer/UEF HOLD, RF-044 이미 DONE. A42 pure/B35 synthetic 선택 MET가 whole RF DONE을 뜻하지 않는다.
- **실행 한계:** C04 정본 직접 pytest NOT_RUN (container GitHub DNS 실패); 180+3 PASS는 정확 actor SHA의 정상 결과이지 정본 직접 실행이 아니다. 변경된 SOURCE/Owner/test와 기존 의존성 경계의 정확 blob에 한해 G3_REUSE. 수동 CI 0, 실거래/운영 effect 0. 마지막 C05 DONE 46/93, CLOSEOUT_READY 0.
- **Next:** RF-030 exact fake-only smoke/증거, RF-063 B-04 import+resolver 최소 종결, 신규 A/B G1/G2만 다음 선택 통합. 원격 신규 코드/test 증거 없으면 중복 통합·CI·문서 커밋 0.
