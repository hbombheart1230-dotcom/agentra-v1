# C02 — Claude A | P1.5 컷라인 마무리 (RF-032, RF-021)

## Authority
Canonical integration/p1.5. 컷라인 정본: docs/refactor/p1_6/P15_CUTLINE_PROPOSAL_20261105.md (오너 결정 5건 확정, 2026-11-05). D00의 보호 경계(Owner, frozen, UEF, Guard, Writer, Step5C, 실거래·브로커 금지)는 그대로 유지한다. 이 지시서는 2026-11-05에 Claude가 오너 위임으로 직접 개정했다.

## Current order
ORDER_ID: A65-CUTLINE-FINISH-20261105
SCOPE: P1.5에서 끝낼 RF는 RF-032 / RF-021 / RF-045 세 개뿐이다. 이 중 Claude A 담당은 RF-032(7 MOVE, 피어 리뷰 대기)와 RF-021(1 MOVE)이다. RF-045는 C01(Codex B).
ITEM 1: RF-032 — 정정(2026-11-05 Codex B 피어 검토): 원장의 RF-032 MOVE_BODY 7개는 모두 libs/reporting/evaluation/uef5/historical_recompute.py의 함수(_prepare_secondary_and_cost 등)이며 타겟이 아직 없다. UEF는 보호 경계라 오너 승인 없이 건드리지 않는다. A가 integration에 반영한 _rank_row·_candidate_rows 분리(506de8d2, 테스트 204 통과)는 원장에 없는 별도 이동으로 기록만 한다. 오너 결정(2026-11-05): 7개 UEF 이동은 P1.6으로 이관. A는 RF-032에서 더 할 일 없음.
ITEM 2: RF-021 — Codex B 독립 검토 결과 KEEP_VERIFIED(exit_policy_chart_projection.py::exit_chart_out, blob e7f5c2b4, 안전 보호 영역이며 분리 불필요). 코드 변경 없음. C05 종결 판정만 남음.
DEFERRED(하지 않는다): RF-010, 011, 012, 022, 026, 030, 042, 048, 049 및 KEEP-only RF 전부는 P1.6으로 이관됨. 새 RF를 시작하지 않는다.
KNOWN_BASELINE_FAILURES: 컷라인 문서 동결 조건 2-1에 기록된 기존 실패(262건: decision_observability_dedupe_non_empty import, RF93 work orders 부재 등)는 이 작업의 책임이 아니다. 새 실패를 만들지 않는 것만 증명한다(작업 전후 실패 집합 비교).
TEST: 변경한 경계마다 normal과 `python -O` 각 1회, 기준선과 실패 집합 비교.
COMPLETION: Issue #11에 실제 종료 코드와 SHA를 보고. 푸시 실패는 있는 그대로 기록한다.

## Execution
HANDOFF/STATUS/CSV/patchnotes/RF 문서는 수정하지 않는다. main, 새 브랜치/PR/worktree 금지. 예약 작업은 만들지 않는다.
