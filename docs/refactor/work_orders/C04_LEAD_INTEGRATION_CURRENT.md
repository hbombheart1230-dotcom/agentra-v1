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

## 현재 상태 — 2026-11-03 08h KST / A55+B41 선별 통합

- **정본 코드 통합:** `c85879c15c3e45e092186cb2241abb64bb856c10` → `e6319b927d6340a9ebded6898048d2496d423b71` (tree `e828db83c34b848ceb385af6d4028b4126e58969`, non-force expected-head push). 24 code/test 경로만 변경: A55 SOURCE4+Owner8+test1 = 13, B41 SOURCE2+Owner8+test1 = 11. **24/24 정확 actor↔integration Git blob 일치**, SOURCE preimage 6/6 actor parent↔canonical 일치, 새 Owner/test 18경로 충돌 없음. B41 직접 import/Owner 의존성 11/11 blob 일치; A55 evaluation 디렉터리 기존 공통 경로에서 SOURCE4 이외 drift 0.
- **RF-032 A55:** actor `2d48eb29c813353eddb8a9e47de1ae5f9787fa1b`, #11 6590953654. `scanner_quality.py::pre_strategist_candidate_rows`; `scanner_alignment_root_cause.py::{build_scanner_alignment_root_cause_report,_load_day_models_and_evaluations,build_scanner_alignment_root_cause_range,_read_json}`; `no_trade_attribution.py::{build_no_trade_attribution_report,_read_json}`; `historical_prior.py::_rank_bucket` → 각 단일 Owner. Normal `python -m pytest -q tests/test_p15_rf032_20261103_08h_scanner_no_trade_historical_owners.py` **302 PASS, EXIT=0** (actor fresh clone). 선택 범위 G1/G2/G3_REUSE MET; **전체 G1 BLOCKED_POLICY** (validation-id/Writer/UEF), 03_PEER, CLOSEOUT_READY 아님.
- **RF-063 B41:** actor `62f227425782fc94a440910264fdd82d1fa1acd0`, #12 6590902400. `run_m31_mock_investor_exam_check.py::{_read_env_file,_parse_kst_datetime,_utc_day,_item,_build_markdown,_build_parser}` + `run_m31_slo_incident_review_check.py::{_iter_jsonl,_read_json}` → 각 단일 Owner. Normal `python -m pytest -q tests/test_p15_rf063_20261103_08h_mock_slo_owners.py` **5 PASS, EXIT=0**, `py_compile` EXIT0 (actor). 선택 범위 G1/G2/G3_REUSE MET; **전체 G1 PARTIAL/G3 BLOCKED** (`libs/reporting/llm_artifacts.py` resolver/consumer, canonical `27aea755` vs B `06dd435f`), 02_DEV, CLOSEOUT_READY 아님.
- **RF-030:** G1 PARTIAL (RF-074 frozen Owner), exact canonical fake-only `python -m pytest -q tests/test_p15_rf030_20261102_02h_run_contexts.py` **NOT_RUN**, G2/G3 PENDING. 로컬 터미널 GitHub DNS 실패로 private checkout 미확보; actor 테스트 PASS로 대체하지 않는다.
- **RF-026:** G1 BLOCKED_POLICY cold-import. **RF-044:** 기존 DONE, 중복 집계 금지. 마지막 C05 확인 **46/93 DONE**, **CLOSEOUT_READY=0**, 이번 신규 RF DONE=0. 통합된 두 선택 범위에 대한 정본 직접 pytest **NOT_RUN**; 정확 Git blob/의존성 동일성과 actor 정상 targeted 결과를 G3_REUSE 증거로 사용하며 정본 PASS를 주장하지 않는다.
- **Next:** (1) C03/C05 RF-074 Owner adjudication + RF-030 정본 fake smoke; (2) C03/B RF-063 resolver/consumer 정확 경계·Owner G1/G2 확보 후 C04 좁은 import parity; (3) C03/승인 안전 Owner RF-032 Writer/UEF 정책 차단 해소, C05 재판정. 모든 RF full peer/-O/full suite/hosted CI 새 게이트 금지. 실거래/운영 DB/Guard/Step5C/UEF/RunLab effect 금지. C05만 RF/STATUS/DONE 작성.
- **Agentra SKILL:** `agentra-contract-guard/SKILL.md@f2fe45fd`, `agentra-done-verifier/SKILL.md@ae742477` 수동 체크리스트 참고만, 자동 로딩 미확인.
