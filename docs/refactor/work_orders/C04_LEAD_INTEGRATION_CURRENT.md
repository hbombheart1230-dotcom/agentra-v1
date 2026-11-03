# C04 — 선별 통합

매시 35분 정본 integration/p1.5의 D00와 이 파일, #11/#12/#36 신규 증거를 읽는다. 스킬은 agentra-contract-guard 및 agentra-done-verifier다.

## 실행 순서
원격 G1/G2 충족 변경을 Owner·consumer·의존성 기준으로 선별 통합한다. source/test/dependency가 동일한 유효 증거는 재사용하고 미검증 범위만 정상 fake smoke로 확인한다. 각 준비 항목을 끝까지 처리하고 #36에 RF, 전체/부분 게이트, 통합 SHA, 테스트 명령·exit, C05_READY, FIRST_BLOCKER를 남긴다.

## 현재 처리 대상
- RF-063 B44의 테스트와 manifest를 #12에서 인수해 정본 실제 소비 경로를 검증한다.
- RF-030의 테스트 tests/test_p15_rf030_20261102_02h_run_contexts.py는 정본 891de6396afd5d116c308ee32f8b6a0b94c24df2에서 14 PASS/exit 0이다. historical pin을 조회하는 테스트이므로 현재 facade/Owner/consumer를 실제로 덮는 범위를 확인한 뒤 G3 재사용을 판정한다.
- 위 테스트의 필요한 pin은 b2e48863ae8a44d7ab41090160816d504052f2e0 및 7dd8a2ad54228ca7f9e5530f07f39b324a55fdb9다.
- 같은 정본에서 tests/test_work_reporter_seed_migration.py::test_target_tree_discipline_and_no_forbidden_surface는 기준 eeb742a33b16f6271ff364a904e187b470561c7e 확보 후에도 경로 범위 위반으로 FAIL이다. frozen scope/Owner 차단과 current-consumer coverage를 구분해 C03/C05에 인계한다.

부분 테스트 통과를 whole RF G3로 승격하지 않는다. 보호 정책을 바꾸지 않는다. 같은 증거의 반복 실행·통합·보고를 피한다.

## 갱신 규칙
이 파일은 현재 지시와 미완료 항목만 유지한다. 갱신 시 본문을 교체하고 완료 주문·이전 보고·교정 이력을 누적하지 않는다. 과거 증거는 Git history와 해당 Issue에서 조회한다. 진행 중인 유효 항목은 다음 갱신에 보존한다.
