# C04 — 선별 통합

## 최우선 작업 기준
홍사장 지시: 담당별 진행 중 RF를 유지하고 상세 계획의 남은 항목을 끝까지 처리한다. 매회 DONE 쉬운 RF를 다시 찾거나 단일 HOLD 때문에 RF를 바꾸지 않는다. 기존 DONE-FIRST의 배정 해석보다 이 원칙이 우선한다.
범위·순서·완료 조건은 정본 `docs/refactor/plan/rf_details/RF-XXX_IMPLEMENTATION.md`와 해당 RF 원본 체크리스트를 따른다. 이슈는 완료 증거일 뿐 계획을 대체하지 않는다.
막힌 항목은 원인·해소 담당을 기록하고 같은 RF의 독립 항목을 계속한다. 전체 잔여 항목이 실제 차단된 경우에만 C03이 근거·복귀 조건을 남겨 다음 RF를 배정한다. 개발을 완료해 C04/C05로 인계한 경우 개발자는 다음 RF를 진행할 수 있다.
D00 Owner·안전·frozen 계약과 실제 G1/G2/G3 요건은 유지한다. 완료 작업 재실행 금지.

매시 35분 정본 integration/p1.5의 D00와 이 파일, #11/#12/#36 신규 증거를 읽는다. 스킬은 agentra-contract-guard 및 agentra-done-verifier다.

## 실행 순서
원격 G1/G2 충족 변경을 Owner·consumer·의존성 기준으로 선별 통합한다. source/test/dependency가 동일한 유효 증거는 재사용하고 미검증 범위만 정상 fake smoke로 확인한다. 각 준비 항목을 끝까지 처리하고 #36에 RF, 전체/부분 게이트, 통합 SHA, 테스트 명령·exit, C05_READY, FIRST_BLOCKER를 남긴다.

## 현재 처리 대상
- RF-063 B45 scoped G3: 정본 980bad1566f3b3ea8915ee49f9a83d0600a7122f에서 python -m pytest -q tests/test_p15_rf063_b45_canonical_report.py tests/test_check_reports_trades_health.py tests/test_p15_rf063_07h_b5_ai_trade_report_is_complete_owner.py tests/test_check_trade_report_runtime_regression.py → 지팀장 직접 EXIT=0, 13 PASS. 같은 source/test/dependency면 재사용한다. 전체 RF 및 CLI 동등성은 미검증. 다음은 기존 trade_evidence와 projection 5파일 의존성의 실제 비교·최소 소비 경로 검증이며 B45 재시험으로 대체하지 않는다.
- RF-030의 테스트 tests/test_p15_rf030_20261102_02h_run_contexts.py는 정본 891de6396afd5d116c308ee32f8b6a0b94c24df2에서 14 PASS/exit 0이다. historical pin을 조회하는 테스트이므로 현재 facade/Owner/consumer를 실제로 덮는 범위를 확인한 뒤 G3 재사용을 판정한다.
- 위 테스트의 필요한 pin은 b2e48863ae8a44d7ab41090160816d504052f2e0 및 7dd8a2ad54228ca7f9e5530f07f39b324a55fdb9다.
- 같은 정본에서 tests/test_work_reporter_seed_migration.py::test_target_tree_discipline_and_no_forbidden_surface는 기준 eeb742a33b16f6271ff364a904e187b470561c7e 확보 후에도 경로 범위 위반으로 FAIL이다. frozen scope/Owner 차단과 current-consumer coverage를 구분해 C03/C05에 인계한다.

부분 테스트 통과를 whole RF G3로 승격하지 않는다. 보호 정책을 바꾸지 않는다. 같은 증거의 반복 실행·통합·보고를 피한다.

## 갱신 규칙
이 파일은 현재 지시와 미완료 항목만 유지한다. 갱신 시 본문을 교체하고 완료 주문·이전 보고·교정 이력을 누적하지 않는다. 과거 증거는 Git history와 해당 Issue에서 조회한다. 진행 중인 유효 항목은 다음 갱신에 보존한다.
