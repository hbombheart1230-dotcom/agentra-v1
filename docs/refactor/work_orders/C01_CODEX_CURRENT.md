# C01 — Codex B

- 정본은 integration/p1.5. 이 파일을 먼저 읽는다.
- 작업 브랜치는 work/p15-b-operator-structure-20261022, 보고는 #12.
- 스킬은 agentra-rf-executor 및 agentra-contract-guard. C03의 허용 범위와 D00 보호 제약을 따른다.

## 현재 주문
ORDER_ID=B44-RF063-CONSUMER-20261104
목표는 RF-063 resolver와 실제 소비 경로의 G2 증거 또는 최소 실패 재현 확보다.

읽기 범위는 libs/reporting/ 아래 llm_artifacts.py, llm_artifacts_trade_lookup.py, llm_artifacts_path_projection.py, llm_artifacts_run_paths.py, single_trade_report.py, intraday_trade_reports.py 및 직접 import 의존성이다. 정본과 B의 관련 blob을 비교한다.
쓰기 허용은 tests/test_p15_rf063_b44_resolver_consumers.py 한 파일이다. 기존 파일이면 원격 완료 증거를 먼저 확인한다.

1. 실제 resolver 및 최소 한 실제 소비자 진입점을 tmp_path/fake/monkeypatch로 검증한다.
2. canonical root 존재, misplaced root만 존재, 양쪽 존재 우선순위, 둘 다 없음, trade-id 조회, call-time monkeypatch를 포함한다.
3. 실제 reports/logs·네트워크·운영 main·실거래 호출과 frozen 테스트 변경은 금지한다. 소스 수정이 필요하면 정확한 경로·함수·재현을 C03에 전달한다.
4. 정상 pytest 결과를 기록하고 B 브랜치에 비강제 푸시한 뒤 원격 SHA·테스트 blob을 재조회한다.
5. #12에 ORDER_ID, 항목별 결과, source/consumer/dependency manifest, 테스트 명령·exit, 원격 SHA, 실제 소요 시간을 남긴다.

모든 배정 안전 항목을 처리한다. ORDER_ID+ITEM+SOURCE_BLOB의 원격 완료 증거가 있으면 VERIFIED_ALREADY로 건너뛴다. B43은 완료됐으며 재실행하지 않는다. 새 주문이 없으면 C03에 NO_READY_ORDER를 보고한다.

## 갱신 규칙
이 파일은 현재 지시와 미완료 항목만 유지한다. 갱신 시 본문을 교체하고 완료 주문·이전 보고·교정 이력을 누적하지 않는다. 과거 증거는 Git history와 해당 Issue에서 조회한다. 진행 중인 유효 항목은 다음 갱신에 보존한다.
