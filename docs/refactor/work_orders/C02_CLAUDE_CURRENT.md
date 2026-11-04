# C02 — Claude A

## 최우선 작업 기준
홍사장 지시: 담당별 진행 중 RF를 유지하고 상세 계획의 남은 항목을 끝까지 처리한다. 매회 DONE 쉬운 RF를 다시 찾거나 단일 HOLD 때문에 RF를 바꾸지 않는다. 기존 DONE-FIRST의 배정 해석보다 이 원칙이 우선한다.
범위·순서·완료 조건은 정본 `docs/refactor/plan/rf_details/RF-XXX_IMPLEMENTATION.md`와 해당 RF 원본 체크리스트를 따른다. 이슈는 완료 증거일 뿐 계획을 대체하지 않는다.
막힌 항목은 원인·해소 담당을 기록하고 같은 RF의 독립 항목을 계속한다. 전체 잔여 항목이 실제 차단된 경우에만 C03이 근거·복귀 조건을 남겨 다음 RF를 배정한다. 개발을 완료해 C04/C05로 인계한 경우 개발자는 다음 RF를 진행할 수 있다.
D00 Owner·안전·frozen 계약과 실제 G1/G2/G3 요건은 유지한다. 완료 작업 재실행 금지.

- 정본은 integration/p1.5. 이 파일을 먼저 읽는다.
- 작업 브랜치는 work/p15-a-reporter-pure-20261021, 보고는 #11.
- 스킬은 agentra-rf-executor 및 agentra-contract-guard. C03의 허용 범위와 D00 보호 제약을 따른다.

## 현재 상태
ACTIVE_RF: RF-032 (Claude A 독점; 다른 RF 전환 금지)
READY_ORDER: 없음 — 임의 코드 변경 금지.
FIRST_UNMET: whole G1 validation-id / Writer / UEF 정책 승인 HOLD. 해소 담당: 승인권자; C03은 승인 없이 정책 변경·whole DONE 선언 금지.
NEXT_ITEM (후보 실사, 주문 아님): `docs/refactor/plan/rf_details/RF-032_IMPLEMENTATION.md` §1 `_secondary_identity` / `_pipeline_q12_calc1` 등 원본 함수별 MOVE_BODY 계획과 §2 미완료 SOURCE 목록을 실제 A 원격 코드·기존 #11 완료 manifest와 대조한다. `libs/reporting/evaluation/uef5/historical_recompute.py` canonical/A blob `719101c37fcac1fe83dd5461b906e42dd5cdf24e`; 목표 `historical_recompute_secondary_identity.py`, `historical_recompute_pipeline_q12_calc1.py`는 두 브랜치 모두 현재 ABSENT. 다만 UEF5 보호 경계로 인해 이 두 목표가 비어 있다는 사실만으로 구현 승인하지 않는다. C03이 보호 계약·monkeypatch seam·Owner·정상 fake 테스트를 먼저 검증한 후 정확한 ORDER_ID/ITEM/SOURCE/TARGET blob을 발행한다.
COMPLETED_ALREADY: A57-1/2는 #11 원격 A `77bdbf6d0834c493ff884be5c260a6b8120d2037`에서 완료; 재발행·반복 테스트 금지.
BLOCKED_SCOPE: 위 UEF5 함수 이동은 보호 경계 안전성 미확정(C03 검증 필요); validation-id/Writer/UEF 정책은 승인권자 결정 필요. 이 두 차단을 다른 독립 RF-032 항목의 자동 차단으로 확대하지 않는다.

## 실행 규칙
C03가 발행한 ORDER_ID, 허용 경로, source/target blob, 테스트, 완료 조건에 따라 모든 안전 항목을 수행한다. 막힌 항목은 FIRST_BLOCKER를 기록하고 다른 항목을 계속한다. 임의 작업 선택 및 다른 Owner 소스 수정은 금지한다.
코드·테스트만 A 브랜치에 비강제 푸시하고 원격 SHA를 재조회한다. #11에 항목별 결과, 정상 테스트 명령·exit, 원격 SHA, 실제 소요 시간을 보고한다. 신규 주문이 없으면 NO_READY_ORDER를 C03에 전달한다.

## 갱신 규칙
이 파일은 현재 지시와 미완료 항목만 유지한다. 갱신 시 본문을 교체하고 완료 주문·이전 보고·교정 이력을 누적하지 않는다. 과거 증거는 Git history와 해당 Issue에서 조회한다. 진행 중인 유효 항목은 다음 갱신에 보존한다.
