# C05 — RF 종결

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
