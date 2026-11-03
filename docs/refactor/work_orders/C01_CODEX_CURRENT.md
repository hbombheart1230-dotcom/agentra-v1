# C01 — Codex B | READY

정본 integration/p1.5. 실행 브랜치 work/p15-b-operator-structure-20261022. 결과 #12.
매회 최신 D00와 agentra-rf-executor/agentra-contract-guard를 적용한다. frozen oracle·Owner·실거래·Guard·Writer·UEF·Step5C 보호.

## 현재 주문
ORDER_ID: B45-RF063-CANONICAL-REPORT-20261104
ITEM: 1
RF: RF-063
FIRST_UNMET: G1/G2 — diagnostics 보고서 완성도 판정의 현재 저장 경로 누락
SOURCE_SHA: canonical 7b8529d646a145da35c1f6c7484edd04677fd977 / B 5448bb9fe47041e25420a900f4894c521b1f2556
SOURCE_BLOB: aedf88d610e2a3965d5c0aa500dca11f22ff61da
TARGET_BLOB_BEFORE: aedf88d610e2a3965d5c0aa500dca11f22ff61da
허용 수정: scripts/diagnostics/reports_trades_health_read_projection.py::_ai_trade_report_is_complete, 신규 tests/test_p15_rf063_b45_canonical_report.py.
신규 테스트 TARGET_BLOB_BEFORE=ABSENT(실행 직전 확인); 결과 TARGET_BLOB은 실제 커밋 후 기록.

## 수행
1. 현재 source blob과 B HEAD를 재확인한다. 해당 소스 변경 또는 동일 주문 완료 시 기존 결과를 대조해 중복 수정하지 않는다.
2. 실제 결함: 위 함수는 ai_trade_report/ai_trade_report.json, trade_report.json만 조회한다. 생산 경로 reports/ai_trade_report.json이 빠졌다. 12개 필수 dict section이 있는 동일 payload에 대해 canonical 경로만 있으면 False, legacy 경로면 True를 지팀장이 temp-only로 재현했다.
3. 새 테스트에 canonical-only 완전/불완전 JSON, canonical과 legacy 공존 시 canonical 우선, 두 legacy fallback을 고정한다. 기존 테스트는 변경하지 않는다. canonical 우선순위는 libs/reporting/llm_artifacts.py::trade_artifact_paths의 ai_trade_report_json 계약으로 확인한다.
4. 신규 테스트의 실패를 확인하고 _artifact_path 후보 맨 앞에 reports/ai_trade_report.json을 추가하는 최소 수정만 한다. 필수 section·예외 처리·기존 fallback 계약은 유지한다. libs/reporting 소스/Owner를 복사하거나 수정하지 않는다.
5. 정상 python -m pytest -q tests/test_p15_rf063_b45_canonical_report.py tests/test_check_reports_trades_health.py tests/test_p15_rf063_07h_b5_ai_trade_report_is_complete_owner.py 를 1회 검증한다. 회귀 발생 시 원인을 수정한 뒤 필요한 범위만 재실행한다. 운영 root·LLM·network·subprocess 없이 tmp fixture만 사용한다.
6. B 기존 브랜치에 source+신규 테스트만 커밋·원격 전달하고 source/test blob을 재조회한다. #12에 ORDER_ID/ITEM/SOURCE_BLOB, 전후 실패/PASS, 명령·exit, 원격 SHA, C04 인계 경로를 보고한다.

## 완료·인계
C04는 B45 두 파일만 Owner·의존성을 확인해 선별 통합하고 정확한 정본 SHA에서 scoped G3를 판정한다. whole RF DONE은 C05만 판정한다. B44 완료 테스트는 재시험하지 않는다. 한 항목 완료를 RF-063 전체 완료로 보고하지 않는다.
현재 주문만 본문 교체 유지. 이력 누적 금지.
