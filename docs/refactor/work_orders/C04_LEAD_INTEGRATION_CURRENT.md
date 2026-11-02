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

## 현재 상태 — 2026-11-02 16h KST / 신규 DONE 우선

- **정본 통합 기준:** `60f5ac222215b56501c6c97743fe55395001b3fc`. #11 A39 `f58b41a85dd92e3954b6accf910e01f0c224a399` / A40 `8c26d830cc774e80fe4a46a945286b00d20bd9c7`; #12 B35 partial `87a59cee7423f16c98538c64511efa60b96fa383`.
- **RF-032 선택 통합:** A39 8개 + A40 8개 `entry_timing_attribution.py` 실제 계산 본문 → sole Owners 16개, 원본은 call-time facade. 정상 G2 `python -m pytest -q tests/test_p15_rf032_20261102_15h_entry_timing_owners.py` **126 PASS EXIT0** 및 `python -m pytest -q tests/test_p15_rf032_20261102_16h_entry_timing_followup_owners.py` **234 PASS EXIT0** (A actor 보고). 선택 source/Owner/test 19개 Git blob 동일, 핵심 dependencies `quant_shadow_forward_outcomes.py`, `evaluation/metrics.py`, `evaluation/__init__.py` actor↔정본 기존 동일. **선택 G3_REUSE MET, 전체 G1 BLOCKED_POLICY** validation-id/Writer/UEF 안전 Owner 승인 대기.
- **RF-026 선택 통합:** B35-2/3 `regime._to_float/classify_regime_v2`, B35-7/8 `decision_observability._reclaim_evidence_explanation/_blocker_family` 4개 Owner 이동. 정상 G2 `python -m pytest -q tests/test_p15_rf026_20261102_15h_feature_regime_observability_owners.py` **1 PASS EXIT0** (B actor 보고), source/Owner/test 7개 blob 동일; `decision_observability_to_float.py`, `libs/runtime/__init__.py` actor↔정본 기존 동일. **선택 G3_REUSE MET, 전체 G1 BLOCKED_POLICY** RF-021/026 cold-import. B35-1/4/5/6 미완료, 무증거 통합 금지.
- **RF-030 최우선 종결:** `operator_visibility.py@bb6e97a72f94412ff9ca818dbf2a03d788dddf48`, `operator_visibility_build_run_contexts.py@db45fb0e06aee58c5d7938ad7f59801c11fb6191`, `tests/test_p15_rf030_20261102_02h_run_contexts.py@3b7c48e9b98f699f8f3def7314ef8bb2e8a07330`. 정본 fake-only normal smoke EXIT0 또는 동일 의존성의 과거 성공 증거 전 **G3 PENDING**. C05는 whole G1/G2 별도 판정.
- **RF-063 G3 BLOCKED:** B-04 facade/seven Owner + `llm_artifacts.py` resolver 의존성. RF-065 Writer/UEF HOLD. RF-044 이미 DONE이며 재집계 금지.
- **실행 한계:** C04 정본 직접 pytest NOT_RUN (private checkout GitHub DNS 실패). actor PASS를 정본 직접 실행 PASS로 표시하지 않는다. G3_REUSE는 정확 소스/Owner/테스트 및 직접 의존성 blob 동일성에 한정한다. 수동 CI 0, 실거래·운영 효과 0. 마지막 C05 DONE 46/93, CLOSEOUT_READY 0.
- **Next:** RF-030 exact fake-only G3 및 C05 whole G1/G2 reconcile; RF-063 facade/resolver 좁은 smoke; B35 나머지는 신규 원격 G1/G2 도착 시에만 통합. 새 증거 없으면 반복 통합·CI·문서 커밋 0.
