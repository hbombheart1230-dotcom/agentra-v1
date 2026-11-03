# C02 — Claude A

- 정본은 integration/p1.5. 이 파일을 먼저 읽는다.
- 작업 브랜치는 work/p15-a-reporter-pure-20261021, 보고는 #11.
- 스킬은 agentra-rf-executor 및 agentra-contract-guard. C03의 허용 범위와 D00 보호 제약을 따른다.

## 현재 상태
NEW_READY=0. A57-1/2는 최신 #11 및 원격 blob으로 VERIFIED_ALREADY 여부를 확인한다. 완료 증거가 있으면 재실행하지 않는다. C03는 RF-032 정책 HOLD와 독립적인 미완료 후보를 검토해 다음 구체 주문을 발행한다.

## 실행 규칙
C03가 발행한 ORDER_ID, 허용 경로, source/target blob, 테스트, 완료 조건에 따라 모든 안전 항목을 수행한다. 막힌 항목은 FIRST_BLOCKER를 기록하고 다른 항목을 계속한다. 임의 작업 선택 및 다른 Owner 소스 수정은 금지한다.
코드·테스트만 A 브랜치에 비강제 푸시하고 원격 SHA를 재조회한다. #11에 항목별 결과, 정상 테스트 명령·exit, 원격 SHA, 실제 소요 시간을 보고한다. 신규 주문이 없으면 NO_READY_ORDER를 C03에 전달한다.

## 갱신 규칙
이 파일은 현재 지시와 미완료 항목만 유지한다. 갱신 시 본문을 교체하고 완료 주문·이전 보고·교정 이력을 누적하지 않는다. 과거 증거는 Git history와 해당 Issue에서 조회한다. 진행 중인 유효 항목은 다음 갱신에 보존한다.
