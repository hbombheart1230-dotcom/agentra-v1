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

## 현재 상태 — 2026-11-01 12:35 KST / RF-063 K2 +1 최소 통합, RF-014 안전 HOLD
- INPUT: #12 [6552680980](https://github.com/hbombheart1230-dotcom/agentra/issues/12#issuecomment-6552680980), B actor `c2a20380ab4e5db2407e6160a08c100b0bb21b78` (K2 1/8 residual); #11 [6552900089](https://github.com/hbombheart1230-dotcom/agentra/issues/11#issuecomment-6552900089), A actor `0bce5e386fa5e70e79c2d98d958d4e5d3bf2d089` (RF-014 8 moves + C0 smoke); C03 #36 [6552627480](https://github.com/hbombheart1230-dotcom/agentra/issues/36#issuecomment-6552627480) CLOSEOUT_CANDIDATES RF-014/065/063, supply doc only.
- RF-063 B K2: SOURCE `scripts/diagnostics/check_audit_trail_completeness.py::_build_parser` preimage `fa531aebeeb1ff6d72905bc1b50be96721b94d4e` → wrapper blob `699a1c5ad1e0ae59d4817e4a2b9ed651c5e85917`; exclusive OWNER `scripts/diagnostics/audit_trail_parser_projection.py::_build_parser` blob `db2a3a9312eabc30cefde0a6b7387439f126b48f`; targeted test `tests/test_p15_rf063_20261101_10h_audit_owners.py` blob `1d8b7e606d04e5db897e5b7418687e917d6f8722`. Actor normal `python -m unittest tests/test_p15_rf063_20261101_10h_audit_owners.py -v`, exit0 7/7 reported (#12; 1 new K2). G3 scoped REUSE after exact blob comparison, whole RF-063 PENDING; K1/K3/K4/B1–B3/B7 and older B-04/B1/manifest evidence remain.
- RF-014 A: actor `python -m unittest tests/test_p15_rf014_20261101_12h_projection_owners.py tests/test_p15_rf014_scanner_repeat_risk_noop_20261101_12h.py`, exit0 11/11 reported, but widened baseline comparison found 4 NEW failures in `tests/test_p171_v3055_scanner_projection_migration.py` (3 pinned SOURCE blob and 1 exact-one-body). This historical invariant conflicts with the proposed move. **HOLD actor A batch**, no source/test integration or historical guard rewrite without C03/C05 contract decision; RF-009 consumer NOOP seam also not verified. Other RF continue.
- C04 selected B only: 3 code/test paths, 1 C04-only instruction; no RF/STATUS/C01–C03/C05 writes. G3 scoped MET RF-063 K2; RF-014 BLOCKED/HOLD; RF-065 no new code G2; CLOSEOUT_READY none. Direct pytest=0, manual CI=0, full suite/-O=0, automatic push CI conclusion separately verify. No already-DONE RF duplicate.
- NEXT: C05 accept RF-063 K2 narrow G3 only, RF-063 DEV and RF-014 PEER remain; C03 authorize correct resolution of RF-014 historical pinned invariants and RF-009 consumer seam without relaxing safety, B finish RF-063 residual K1/K3/K4/B1–B3/B7; do not count partial G3 as RF DONE. No real orders, DB, Broker/Guard/Step5C/UEF/RunLab effects.
