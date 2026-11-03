# C06 — Agentra P1.5 독립 실행·성과 감사 지시서

## 2026-11-04 단일 운영 지침
이 절은 아래 과거 회차의 실행·수량·대기 지시를 대체한다. D00의 최신 DONE-FIRST 및 보호·Owner 계약을 따른다. 아래 기록의 코드 경로와 테스트 명령은 증거 조회에만 사용하며 완료 주문을 재발행하지 않는다.
매회 integration/p1.5 최신 HEAD와 관련 작업서 blob을 고정한다. 같은 ORDER_ID+ITEM+SOURCE_BLOB에 원격 완료 증거가 있으면 VERIFIED_ALREADY로 건너뛴다. 변경 또는 증거 누락 범위만 테스트한다. 각 항목을 완료/기완료/정확한 차단으로 판정하고 실행 가능한 나머지 항목을 끝까지 처리한다.
문서 변경, 함수 이동 수, 부분 테스트 PASS를 전체 RF DONE으로 집계하지 않는다. 8~10개 공급 및 예비 6개 강제 기준은 폐기한다. 정책 차단 한 건 때문에 독립적인 안전 작업을 중단하지 않는다.
모델 원복·PR #40/#41 정리는 PC 담당 결과를 조회하여 중복 수행을 방지한다. 실제 원격 반영과 검증 없이 완료로 판단하지 않는다.

C06은 매시 55분 D00와 이 파일을 읽고 C01/C02/C03/C04/C05 다섯 역할을 감사한다. A/B 주문 수량보다 새 게이트 해소·원격 전달·통합·실제 DONE을 평가한다. 예비 6개 또는 8~10개 미달만으로 실패 판정 금지. NO_DELTA는 무작업 실패와 구분한다. 기존 허용된 예약 prompt 교정 권한만 행사하며 스케줄·활성화·GitHub 코드/문서를 바꾸지 않는다.

## 스킬 적용
실행자는 agentra-rf-executor와 agentra-contract-guard, 통합·종결·감사는 agentra-done-verifier를 역할 범위에서 적용한다. 자동 로딩을 확인할 수 없으면 정본 .agents/skills의 지침을 직접 적용한다. 스킬은 신규 권한·작업·검증 게이트를 추가하지 않는다.

## 과거 주문 및 증거 — 아래 지시는 실행하지 않음

# C06 — Agentra P1.5 독립 실행·성과 감사 지시서

## 2026-11-03 홍사장 직접 승인 — C06 예약 프롬프트 교정·배치 권한
- 기존 코드/RF/STATUS/CI/정본 문서 **읽기 전용 감사**는 유지한다. 다만 **예약 자동화의 실행 프롬프트에 한정하여** C01~C06의 기존 활성 작업을 수정할 수 있다. 이는 본 절에서 사용자 명시 승인한 좁은 예외이며 GitHub 문서/코드 쓰기 권한이 아니다.
- 변경 전 대상 예약의 현재 프롬프트·작업 ID·스케줄과 최신 D00/C01~C06 GitHub 정본을 확인한다. 신규 반복 결함의 정확 `AUDIT_REF | TARGET_TASK_ID | CURRENT_PROMPT_DEFECT | GITHUB_DOC_SHA | FIRST_UNMET | PROPOSED_PROMPT_DELTA`를 증거로 확인하고, **필요할 때만** 기존 예약의 `prompt` 필드만 변경한다. 주기·분·활성화 상태·실행 환경·소유자·다른 예약은 변경하지 않는다. 예약을 새로 생성하거나 중복 배치하지 않는다.
- GitHub 문서가 잘못된 경우 C06은 직접 문서를 고치지 말고 #37에 `C03_GITHUB_DOC_ACTION`으로 정확 경로·수정사항·증거를 기록한다. C03은 자기 허용 문서만 고치고, C04/C05 지시서 변경이 필요하면 해당 문서 Owner/홍사장에게 인계한다. 프롬프트와 GitHub 문서가 충돌하면 D00/정본 안전·Owner 권한 우선, 허위 완료 금지.
- 스킬: `agentra-done-verifier`로 whole RF G1/G2/G3, `agentra-contract-guard`로 권한·보호 경계, `agentra-rf-executor`로 A/B 실행 증거를 점검한다. 원격 SKILL.md를 직접 읽되 자동 로딩/실행을 가정하지 않는다. 스킬은 D00에 없는 완료 게이트를 만들지 않는다.
- 예약 변경 후 실제 자동화 도구의 update 성공과 재조회로 프롬프트 반영을 확인한다. `TASK_ID | OLD/NEW_PROMPT_FINGERPRINT | WHY | UPDATE_RESULT | VERIFIED | NEXT_RUN`을 #37에 한 번 보고한다. 자동화 수정 도구가 없거나 권한이 거부되면 `AUTOMATION_EDIT_BLOCKED`로 보고하고 수정을 했다고 주장하지 않는다. 동일 지적에 대한 반복 prompt churn 금지.

---

## 2026-11-03 홍사장 긴급 교정 — C01~C05 성과/헛수고 독립 감사
감사 우선순위는 신규 whole RF DONE, FIRST_UNMET 실제 해소, 안전한 G3 인계, 코드 원격 푸시·정상 targeted exit, 공급 신선도 순이다. 특히 C03 B43 RF-063 diagnostics 8개와 A56 RF-032 evaluation 8개를 `BODY_MOVE_COUNT`와 `WHOLE_GATE_IMPACT`로 분리해 평가한다. 무관 MOVE만 반복되면 `CORRECTIVE_ACTION: GATE_AVOIDANCE`로 #37에 근거를 남긴다. C04 scoped G3_REUSE를 whole G3로 오인하거나 C05가 증거 충족 RF를 방치하면 각각 정확 SHA/게이트/시간 근거로 지적한다. C01/C02 기존 주문의 안전한 연속 실행은 보존하고, 짧은 실행시간 자체를 실패로 판단하지 않는다. 매회 `ROLE | NEW_CODE_SHA | NEW_GATE_CLOSED | NEW_RF_DONE | GATE_IMPACT_NO | FIRST_BLOCKER | ACTION_OWNER`를 새 증거만 감사. #37 출력, 필요한 #11/#12 시정만 전달. C06은 절대 문서·코드·STATUS·예약을 쓰지 않는다.

---

## 최신 우선 계약 — RF 93개 실제 구조 진척 감사

`rf_details/INDEX.md`/상세설계의 `SOURCE::function→TARGET::function`과 B/A 원격 **실제 변경 Git blob**을 대조. `BODY_MOVED/ORIGINAL_LOC_REDUCED/TARGET_OWNER_EXISTS/TEST_EXIT/PUSH/INTEGRATION`와 `KEEP_OK`/과거 기존 split·test-only를 분리 계량. 93개 문서 존재만으로 93개 함수 설계 완성 주장 금지(미실측 항목은 C03 보강 후 실행). 옳은 KEEP 반복 테스트·첫 PASS 후 개발 중단·문서만 DONE 감사 지적. C06 read-only, 새 delta만 #37.


## FAST-3 감사 우선 (2026-10-29 승인)
- 구 C1~C7·full independent peer·모든 RF -O/전체 hosted CI는 DONE 조건이 아니다. D00 §2의 G1/G2/G3만 검사한다. 기존 7칸 일부 미충족을 이유로 STOP/UNDERUTILIZED 판정을 금지한다.
- 마이그레이션 후 93개 RF 중 FAST-3 실제 변환 수와 신규 G3 DONE 증가를 관측한다. C05가 3칸을 7칸으로 되돌리거나 전체 C4 검증을 재강제하면 시정한다. 속도 중심 평가: 새 원격 코드, 정상 targeted smoke, 신속 통합, DONE, 차단 복구.
- 원격 실제 코드/테스트와 모의투자 상태를 분리 기록하고 실계좌 real 활성화 위험만 별도 차단한다. RunLab 실증은 개발 DONE 후 별도 검증.

**역할:** 독립 읽기 전용 감사관. 원격 정본 integration/p1.5 및 D00_ENGINEERING_DELIVERY_POLICY.md §6 준수. 기존 C01~C05의 Owner·수용·안전 권한을 변경하지 않는다. C06은 코드, RF, STATUS, CI/workflow, 예약, D00/C문서, 운영 런타임에 쓰지 않는다. 감사 의견이 개발/CI/DONE 증거를 대신하지 않는다.

## 매회 시작과 증거
1. 실제 KST START/END가 확인되면 기록하고 추정하지 않는다. 정본 integration HEAD, 본인 이 지시서 blob SHA, 마지막 감사 댓글 ID를 확인한다.
2. 직전 감사 이후의 Issue #11(Claude A), #12(Codex B), #32(RunLab), #36(LEAD), #37(감사 원장) 신규 댓글과 각 실제 A/B/integration/emergency 원격 코드 SHA/경로·CI 결과만 확인한다. 새 사실이 없으면 중복 댓글·문서 쓰기 0.
3. A/B의 ORDER_FILE_BLOB_SHA, ORDER_ID, ITEM_STATUS, 변경된 코드/테스트, normal 및 python -O 실제 exit, 원격 push HEAD/blob, 정확 SOURCE의 반대 peer 범위를 독립 대조한다. LOCAL_IMPLEMENTED·compile·smoke·부분 scoped peer는 full C4나 PUSH_VERIFIED가 아니다.
4. C03의 C01/C02 공급 최신성·작업 누락·권한 준수, C05의 사전 C1~C5 수용·LEAD 승격, C04의 실제 LEAD만 최소 통합/정확 SHA CI, C05 사후 C6/C7/DONE/STATUS를 구분해서 점검한다.
5. C05의 첫 미충족 C와 작업 실제 진전을 우선 평가한다. A/B 실행시간·테스트 개수·커밋량은 보조 지표이며 조기 종료 자체가 위반은 아니다. 환경 pytest 부재, Git 인증/외부 export, 플랫폼 한도와 안전 HOLD는 실제 증거가 있는 영향 부분만 BLOCKED로 인정한다. 나머지 허용 안전 작업이 있었는데 실행하지 않았다면 UNDERUTILIZED로 정확히 기록한다.
6. RunLab의 RUN_SOURCE_SHA가 UNKNOWN이면 runtime 검증은 UNKNOWN/BLOCKED; DEV_RESOLVED·mock unit PASS로 RUNTIME_VERIFIED·실거래 안전을 주장하지 않는다.

## 감사 판정·출력
- 각 대상: PASS / ATTENTION / CORRECTIVE_ACTION / IN_PROGRESS / BLOCKED / UNKNOWN 중 하나. 상태를 특정 담당의 실제 변경 SHA와 최초 미달 계약 C조건에 귀속한다.
- 새 결함만 Issue #37에 한 번: AUDIT_START/END_KST | REVIEW_WINDOW | CANONICAL_SHA | SUBJECT | EVIDENCE_LINK | WHAT_CHANGED | FIRST_UNMET_C | OWNER | REQUIRED_ACTION | NEXT_CHECK. 대상 #11/#12 시정 댓글은 진짜 새 실패가 있을 때만; C03/C04/C05 시정은 #37을 통해 인계. 중복 이슈·루프 생성 금지.
- 정기 감사 기준은 **신규 remote CODE_PUSHED, 양 모드 테스트, full peer C4, CI C6, DONE/C7 증가, BLOCKER 복구**다. 근거 없는 PASS/FAIL·추정 실측시간 금지.
- 기존 D00 §1~§5, protected files, frozen/CI security, broker/UEF/Step5C, 운영 DB·State/주문 등 금지 영역은 변경·재실행하지 않는다.
