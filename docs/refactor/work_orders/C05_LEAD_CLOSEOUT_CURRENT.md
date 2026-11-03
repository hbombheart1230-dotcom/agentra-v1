# C05 — RF 종결

## 최우선 작업 기준
홍사장 지시: 담당별 진행 중 RF를 유지하고 상세 계획의 남은 항목을 끝까지 처리한다. 매회 DONE 쉬운 RF를 다시 찾거나 단일 HOLD 때문에 RF를 바꾸지 않는다. 기존 DONE-FIRST의 배정 해석보다 이 원칙이 우선한다.
범위·순서·완료 조건은 정본 `docs/refactor/plan/rf_details/RF-XXX_IMPLEMENTATION.md`와 해당 RF 원본 체크리스트를 따른다. 이슈는 완료 증거일 뿐 계획을 대체하지 않는다.
막힌 항목은 원인·해소 담당을 기록하고 같은 RF의 독립 항목을 계속한다. 전체 잔여 항목이 실제 차단된 경우에만 C03이 근거·복귀 조건을 남겨 다음 RF를 배정한다. 개발을 완료해 C04/C05로 인계한 경우 개발자는 다음 RF를 진행할 수 있다.
D00 Owner·안전·frozen 계약과 실제 G1/G2/G3 요건은 유지한다. 완료 작업 재실행 금지.

매시 45분 정본 integration/p1.5의 D00와 이 파일, C04의 #36 최신 증거를 읽는다. 스킬은 agentra-done-verifier 및 agentra-contract-guard다.

## 실행 순서
1. 동일 정본 SHA의 RF 물리 큐와 STATUS 및 신규 G1/G2/G3 증거를 대조한다.
2. 전체 게이트를 충족한 모든 RF를 05_DONE으로 이동하고 STATUS 및 필요한 패치노트를 갱신한다. 원격 반영과 누락·중복 없는 집계를 확인한다.
3. 미충족 RF에는 FIRST_UNMET, 담당, 정확한 해소 조건을 남겨 C03으로 인계한다.
4. #36에 NEW_DONE_RF_IDS, DONE_BEFORE/AFTER, 원격 SHA, G3_READY_BUT_NOT_DONE, NEXT_OWNER를 보고한다.

## 현재 판정 대상
RF-030은 C04의 현재 소비 경로 및 RF-074 frozen scope 판정이 필요하다. RF-063은 resolver/consumer 전체 증거가 필요하다. RF-026/032/065의 Owner·보호 정책 HOLD는 근거 없이 해제하지 않는다. RF-009는 기존 DONE이므로 신규 실적에서 제외한다.

부분 G3, BODY MOVE, 문서 커밋과 기존 DONE을 신규 RF 종결로 계산하지 않는다. 모든 수용 가능한 RF를 같은 회차에 처리한다.

## 갱신 규칙
이 파일은 현재 지시와 미완료 항목만 유지한다. 갱신 시 본문을 교체하고 완료 주문·이전 보고·교정 이력을 누적하지 않는다. 과거 증거는 Git history와 해당 Issue에서 조회한다. 진행 중인 유효 항목은 다음 갱신에 보존한다.
