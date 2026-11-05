# C01 — Codex B | P1.5 컷라인 마무리 (RF-045, RF-032 피어)

## Authority
Canonical integration/p1.5. 컷라인 정본: docs/refactor/p1_6/P15_CUTLINE_PROPOSAL_20261105.md (오너 결정 5건 확정, 2026-11-05). D00 보호 경계(Owner, frozen, UEF, Guard, Writer, Step5C, 실거래·브로커 금지) 유지. 이 지시서는 2026-11-05에 Claude가 오너 위임으로 직접 개정했다. RF-063은 컷라인에서 제외(P1.6 이관)되어 더 이상 활성이 아니다.

## Current order
ORDER_ID: B47-CUTLINE-FINISH-20261105
ITEM 1: RF-045 — 남은 MOVE_BODY 3개를 원장(docs/refactor/plan/RF_TASK_LEDGER.jsonl)의 RF-045 행에서 찾아 처리. B 브랜치의 http_client·log_maintenance 수정은 이미 integration에 반영됨(d5450594).
ITEM 2: RF-032 독립 피어 리뷰(READ-ONLY) — Claude A의 RF-032 결과를 source/target blob, 반환 키, 경고·오류 순서, effect 경계 기준으로 검토해 PASS 또는 TARGET_GAP을 판정.
DEFERRED(하지 않는다): B의 폴더 구조(brief_parts/, read_models/, agent_output_parts/)는 채택하지 않으며 P1.6에서 가드 테스트와 함께 다룬다. commander/__init__.py, run_m30_final_golive_signoff.py, shared_role_contracts.py의 B 버전도 같은 이유로 보류. 새 RF 시작 금지.
KNOWN_BASELINE_FAILURES: 컷라인 문서 동결 조건 2-1의 기존 실패는 책임 밖. 새 실패가 없음을 작업 전후 실패 집합 비교로 증명한다.
TEST: 변경 경계마다 normal과 `python -O` 각 1회.
COMPLETION: Issue #12에 실제 종료 코드와 SHA 보고.

## Execution
문서/RF/STATUS 수정 금지. main, 새 브랜치/PR/worktree 금지. 예약 작업은 만들지 않는다.
