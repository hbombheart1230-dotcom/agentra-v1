# C02 — Claude A | P1.5 컷라인 마무리 (RF-032, RF-021)

## Authority
Canonical integration/p1.5. 컷라인 정본: docs/refactor/p1_6/P15_CUTLINE_PROPOSAL_20261105.md (오너 결정 5건 확정, 2026-11-05). D00의 보호 경계(Owner, frozen, UEF, Guard, Writer, Step5C, 실거래·브로커 금지)는 그대로 유지한다. 이 지시서는 2026-11-05에 Claude가 오너 위임으로 직접 개정했다.

## Current order
ORDER_ID: A65-CUTLINE-FINISH-20261105
SCOPE: P1.5에서 끝낼 RF는 RF-032 / RF-021 / RF-045 세 개뿐이다. 이 중 Claude A 담당은 RF-032(7 MOVE, 피어 리뷰 대기)와 RF-021(1 MOVE)이다. RF-045는 C01(Codex B).
ITEM 1: RF-032 — A 브랜치의 cumulative_improvement_review 분리 소스는 integration에 이미 반영됨(506de8d2). 남은 것은 7개 MOVE_BODY가 integration 기준으로 BASE parity, normal·`python -O` 테스트 통과, 독립 피어 PASS(실제 종료 코드)를 갖췄는지 확인하고 부족분만 채우는 것.
ITEM 2: RF-021 — 남은 MOVE_BODY 1개를 원장(docs/refactor/plan/RF_TASK_LEDGER.jsonl)의 RF-021 행에서 찾아 처리.
DEFERRED(하지 않는다): RF-010, 011, 012, 022, 026, 030, 042, 048, 049 및 KEEP-only RF 전부는 P1.6으로 이관됨. 새 RF를 시작하지 않는다.
KNOWN_BASELINE_FAILURES: 컷라인 문서 동결 조건 2-1에 기록된 기존 실패(262건: decision_observability_dedupe_non_empty import, RF93 work orders 부재 등)는 이 작업의 책임이 아니다. 새 실패를 만들지 않는 것만 증명한다(작업 전후 실패 집합 비교).
TEST: 변경한 경계마다 normal과 `python -O` 각 1회, 기준선과 실패 집합 비교.
COMPLETION: Issue #11에 실제 종료 코드와 SHA를 보고. 푸시 실패는 있는 그대로 기록한다.

## Execution
HANDOFF/STATUS/CSV/patchnotes/RF 문서는 수정하지 않는다. main, 새 브랜치/PR/worktree 금지. 예약 작업은 만들지 않는다.
