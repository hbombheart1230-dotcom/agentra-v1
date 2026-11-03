# C04 — 지팀장 · 선별 통합/CI

## 2026-11-04 단일 운영 지침
이 절은 아래 과거 회차의 실행·수량·대기 지시를 대체한다. D00의 최신 DONE-FIRST 및 보호·Owner 계약을 따른다. 아래 기록의 코드 경로와 테스트 명령은 증거 조회에만 사용하며 완료 주문을 재발행하지 않는다.
매회 integration/p1.5 최신 HEAD와 관련 작업서 blob을 고정한다. 같은 ORDER_ID+ITEM+SOURCE_BLOB에 원격 완료 증거가 있으면 VERIFIED_ALREADY로 건너뛴다. 변경 또는 증거 누락 범위만 테스트한다. 각 항목을 완료/기완료/정확한 차단으로 판정하고 실행 가능한 나머지 항목을 끝까지 처리한다.
문서 변경, 함수 이동 수, 부분 테스트 PASS를 전체 RF DONE으로 집계하지 않는다. 8~10개 공급 및 예비 6개 강제 기준은 폐기한다. 정책 차단 한 건 때문에 독립적인 안전 작업을 중단하지 않는다.
모델 원복·PR #40/#41 정리는 PC 담당 결과를 조회하여 중복 수행을 방지한다. 실제 원격 반영과 검증 없이 완료로 판단하지 않는다.

C04는 매시 35분 D00와 이 파일 및 #11/#12/#36 최신 증거를 읽는다. A/B의 원격 G1/G2 충족 변경을 선별 통합하고 영향받는 실제 소비 경로를 검증한다. 같은 source/test/dependency의 유효 증거를 재사용한다. 원격 통합 SHA와 G3 증거를 #36에 C05_READY로 전달한다. 부분 수용은 whole RF와 구분한다.

## 스킬 적용
실행자는 agentra-rf-executor와 agentra-contract-guard, 통합·종결·감사는 agentra-done-verifier를 역할 범위에서 적용한다. 자동 로딩을 확인할 수 없으면 정본 .agents/skills의 지침을 직접 적용한다. 스킬은 신규 권한·작업·검증 게이트를 추가하지 않는다.

## 과거 주문 및 증거 — 아래 지시는 실행하지 않음

# C04 — 지팀장 · 선별 통합/CI

## 2026-11-03 역할별 Agentra 스킬 적용
`agentra-contract-guard`로 source/target/consumer 소유권·보호 경계를 점검하고 `agentra-done-verifier`로 G3의 exact canonical SHA·smoke/CI 증거를 확인한다. scoped G3와 whole RF G3를 구분한다.

---

## 2026-11-03 홍사장 긴급 교정 — G3 실제 종결 우선
매회 먼저 G1/G2가 이미 충족되고 G3만 남은 미종결 RF를 찾아, exact integrated source/test/consumer 경계의 최소 정상 fake smoke 또는 유효 증거 재사용으로 C05에 전달한다. RF-030의 exact integrated smoke를 우선 판정한다. RF-063 resolver→trade/LLM consumer drift는 단순 diagnostics BODY MOVE 통합으로 해결된 것처럼 보고하지 말고 canonical/B SHA, owner, import/dispatch closure 및 필요한 안전한 최소 통합을 명시한다. RF-032/065 정책 HOLD는 우회하지 않는다. G3_REUSE는 **해당 변경 범위**만 의미하며 whole-RF G3로 승격하려면 전체 FIRST_UNMET 해소가 필요하다. 매회 `RF | WHOLE_GATE_CLOSED? | INTEGRATION_SHA | EXACT_TEST/EXIT | C05_READY | FIRST_BLOCKER`만 새 증거로 #36 보고. 기존 성공 CI 중복 dispatch 0; 실제 안전 자동 CI 유지. D00/보호 정책 불변.

---

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

## 현재 상태 — 2026-11-03 09h KST / A56+B42 선별 통합

- **정본 코드 통합:** `50ffbb2b311f25964c7188161710473ecfa329d3` → `11f8ee2d074dd21e98ea3725ce0d6cca540435f0` (tree `6ac993ac64abf8198eaa235dffbc3f3c2fb98812`; non-force expected-head CAS 성공). **25 code/test 경로만 변경**: A56 SOURCE3+Owner8+test1=12; B42 SOURCE4+Owner8+test1=13. SOURCE preimage 7/7 actor-parent↔canonical 일치, 새 Owner/test 18개 모두 canonical 사전 부재, 통합 후 **25/25 정확 actor↔integration blob MATCH**, A/B 교차 파일 충돌 0. RF/STATUS/DONE/타 C문서/보호 workflow 변경 0.
- **RF-032 A56:** #11 comment 6591917312; actor `a0149439392300f94876e553e11d99fec053d1d5`. `full_chain_component_review.py::build_full_chain_component_review`; `historical_prior.py::{_day_from_trade_dir,_net_return,_group_metrics,summarize_historical_prior,render_historical_prior_markdown,iter_historical_trade_dirs}`; `loss_decomposition.py::_load_trade_models` 각각 단일 Owner 이동. Normal `python -m pytest -q tests/test_p15_rf032_20261103_09h_historical_full_chain_owners.py` **117 PASS/exit0** (actor remote fresh-clone). 선택 범위 G1/G2/G3_REUSE MET, **전체 RF G1 BLOCKED_POLICY** (validation-id/Writer/UEF), 03_PEER, CLOSEOUT_READY 아님. Evaluation 디렉터리 공통 327개 blob actor↔integration 일치.
- **RF-063 B42:** #12 comment 6591950111; actor `abd03cbf09ed4b8e19eea53765babf4c6e7497f1`. `run_m31_slo_incident_review_check.py::_resolve_day_artifact`, `run_m31_mock_investor_exam_check.py::_iter_jsonl`, `run_m30_quality_gates_bundle.py::{_build_md,_component_summary,_gate_status,_build_parser}`, `run_m30_release_signoff_checklist.py::{_count_by,_build_markdown}` 각각 단일 Owner 이동. Normal `python -m pytest -q tests/test_p15_rf063_20261103_09h_m30_m31_readonly_owners.py` **5 PASS/exit0**, py_compile exit0 (actor report). 선택 범위 G1/G2/G3_REUSE MET, **전체 G1 PARTIAL/G3 BLOCKED**: `libs/reporting/llm_artifacts.py` canonical blob `27aea755` vs B `06dd435f`, resolver→trade/LLM consumer closure 불충족. Diagnostics 공통 230개 중 228개 일치, 2개 기존 비선택 drift(`check_trade_report_runtime_regression.py`, `run_m26_scorecard.py`)는 미통합·미승인. Whole-RF smoke PASS 주장 금지.
- **RF-030:** G1 PARTIAL (RF-074 frozen test Owner), exact canonical fake `python -m pytest -q tests/test_p15_rf030_20261102_02h_run_contexts.py` **NOT_RUN**, G2/G3 PENDING. 터미널 `git ls-remote` GitHub DNS EXIT128; private checkout 미확보. 동일 SOURCE/deps의 기존 성공 증거도 아직 검증되지 않음. 허위 PASS/새 full CI 금지.
- **RF-026:** G1 BLOCKED_POLICY cold-import. **RF-044:** 기존 DONE, 중복 집계 금지. 마지막 C05 검증 **46/93 DONE** (2026-11-03 08:45), 이번 **NEW_RF_DONE=0 / CLOSEOUT_READY=0**. 정본 직접 pytest NOT_RUN, 선택 G3는 정확 blob과 actor normal G2의 재사용 근거로만 판정. SKILL 2개는 GitHub 수동 참고, 자동 로딩 미확인.
- **NEXT DONE-FIRST:** (1) C03/C05 RF-074 Owner 판정 + C04 RF-030 정확 canonical fake smoke/기존 증거; (2) C03/B RF-063 resolver/consumer 정확 G1/G2 승인 후 C04 최소 fake import/CLI parity; (3) C03/승인 안전 Owner RF-032 validation-id/Writer/UEF 계약 해소 후 C05 재판정. Full peer/-O/full suite/hosted CI 추가 게이트 금지. 실거래/운영 DB/Guard/Step5C/UEF/RunLab effect 금지. C05만 RF/STATUS/DONE 작성.
