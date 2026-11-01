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

## 현재 상태 — 2026-11-01 16:35 KST / 미종결 RF 최소 G3
- BASE: canonical `c26ec32be1b5257cae7a7f24239b39a704998b3c`; C03 #36 [6554728491](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6554728491) CLOSEOUT_CANDIDATES RF-015/033/063, RF-065 protected HOLD. C05 last #36 [6554589080](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6554589080): 33/93 DONE, RF-014/044/050 already DONE; no repeat.
- RF-015 A16 [#11 6554836030](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6554836030), actor `3765a2b62e058982039ed8ff88f689053c5ba3a3`: KEEP exact unchanged `graphs/nodes/monitor_node.py` `ea5e5890`, Monitor Owners `fe67e001`/`633f9afb`. Select only `tests/test_p15_rf015_20261101_16h_real_monitor_consumer.py` blob `9cf7cb9e4796b395fe305b72b6fc2198dae96362`; actor normal `python -m pytest -q tests/test_p15_rf015_20261101_16h_real_monitor_consumer.py` exit0 3 PASS. Fake/temp real monitor_node State/event caller seam, no live effects; scoped G3 MET by exact-source reuse. C05 whole RF G1 scope/acceptance review, no automatic DONE.
- RF-033 A16 same actor: KEEP exact unchanged `libs/reporting/baseline_btc_woori_tech/comparison.py` `9d5f01d3`, `forward_returns.py` `8d2904c6`, `libs/reporting/baseline_samsung_hynix/forward_returns.py` `9648a639`. Select only `tests/test_p15_rf033_20261101_16h_baseline_pure_consumer.py` blob `c4d177487da0c1c81becb3c6459c5510ebb83ca1`; actor normal `python -m pytest -q tests/test_p15_rf033_20261101_16h_baseline_pure_consumer.py` exit0 4 PASS. Pure helpers only, no network/writer. Scoped G3 MET, 45-path whole RF PENDING.
- RF-063 B16 [#12 6554800499](https://github.com/hbombheart1230-dotcom/agentra/issues/12#issuecomment-6554800499), actor `c535e28240454398dac86489bff7aae7ee81a451`: B trade source `c7113fcf` != integration `dc882aa5`, B-only seven Owner modules not integrated. New test `71c1b850` normal 3 PASS compares B facade vs B Owner only, not canonical original-vs-Owner. Dead private duplicate removal is not a BODY MOVE. G3 HOLD for trade source and B test until canonical golden/affected-function parity, no broad import. Earlier RF-063 scoped G3 remains; whole RF PENDING.
- RF-065 previous scoped fake CLI G3 MET; protected research writer/IO/UEF ownership G1 PARTIAL/SAFETY_HOLD. No new B16 code G3 candidate.
- THIS C04: two A16 targeted test blobs only, zero BODY MOVE; unchanged A↔integration source 6/6 exact; actor normal 3/3+4/4 PASS reused. Direct pytest/CI dispatch 0, no same-SHA rerun; whole CLOSEOUT_READY=0 pending C05. #36 new delta report exact remote integration SHA, blobs and first unmet. No RF/STATUS/DONE or C01-C03/C05 writes, no protected effects.
