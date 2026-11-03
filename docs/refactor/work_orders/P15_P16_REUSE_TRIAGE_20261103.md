# P1.5 → P1.6 즉시 실사·인계 01 (2026-11-03)

> **READ-ONLY audit**: 원격 `integration/p1.5`의 RF 원본·상세설계와 C03/C04/C05 최근 #36 판정 직접 대조. 코드 실행/pytest/통합/종결 **NOT_RUN**. 47건 전수 완료 주장 금지.
> 기준: C05 2026-11-03 09:45 KST, 93 unique / DONE46 / 미종결47(PENDING38 DEV7 PEER2). 새 RF DONE=0.
> 등급 A=안전/호환성/소비경로 필수 종결, B=최소 수정 후 종결, C=개별 승인 필요 P1.6 이관 심사. 동일 RF의 세부 과업은 A+B 혼합 가능.

## 직접 확인된 5건

| RF | 물리 단계 | 등급 | 원격에서 확인한 FIRST_UNMET | 지금 바로 넘길 Owner·안전한 다음 행동 | P1.6 관련 |
|---|---|---|---|---|---|
| RF-030 | 01_PENDING / Claude A | A (계약·검증), B (부수 구조) | 16개 소유, 15/16 KEEP; `_build_run_contexts` canonical 정확한 fake G2/G3 미검증. RF-074 frozen fixture/test 소유 경계 | **C04:** canonical 현재 SHA에서 `tests/test_p15_rf030_20261102_02h_run_contexts.py`의 git-show pinned preimage 의존성 먼저 read-only 확인. 재현 가능하면 해당 정확한 fake-only normal test exit0를 실행하고 #36에 SHA/exit/의존성 증거. **C05:** G1 KEEP 예외를 RF-074 소유권과 대조 후 G1~G3 재판정. | 보고 소비자 계약은 P1.6 재사용; 추가 함수 이동 최소 |
| RF-063 | 02_DEVELOPING / Codex B | A (resolver/consumer), B (diagnostics MOVE) | `libs/reporting/llm_artifacts.py` canonical `27aea755` vs B `06dd435f` drift, resolver→trade/LLM consumer import/dispatch closure. B42의 8 MOVE는 scoped G3_REUSE만 | **C03+B:** 실제 drift가 필요한 부분/다른 Owner 영향 read-only 판정 후 최소 안전 계약 주문. **C04:** dependency-closed fake import/consumer smoke, 정확 선별 통합. **C05:** whole RF 재판정. B43 등 진행 중인 발행 주문 소급 취소 금지. | 진단 재배치 반복보다 인터페이스 보존 우선 |
| RF-032 | 03_PEER_REVIEW / Claude A | A (Writer/UEF 경계), B (평가 분리) | `--validation-id`를 경로에 무검증 결합하여 temp 격리 재현에서 `../`·절대경로 이탈 가능; 보호된 Writer/UEF 계약 승인 미완료. A56 scoped G3_REUSE는 whole RF 해제 아님 | **C03+authorized safety Owner:** 허용 validation-id·출력 경로·하위호환 정책 결정 요청. **C05:** 승인 후 affected fake G2/G3 판정. 무단 하드닝·UEF 수정 금지. | 평가/경험 지식화에 필요하나 안전 경계 우선 |
| RF-026 | 01_PENDING (C05 09:45 판정 기준) / Codex B | A | `exit_policy→monitor_exit` 순환 import 및 RF-021 소유 안전 경계, whole-RF G1 BLOCKED_POLICY. scoped 테스트·이동만 승인 | **C03:** RF-021과 import graph/Owner를 read-only 대조해 충돌 없는 최소 변경 계약 작성. **C04:** 허가된 정확 fake import smoke 후 통합. **C05:** 안전 HOLD 해제 전 DONE 금지. | Monitor/exit 안전성은 P1.6 필수 |
| RF-065 | 02_DEVELOPING / Codex B | B (KEEP 분류), A (CLI/Writer·UEF 보호) | 54개 research 소유 경로 중 KEEP/CLI 효과 분류 미완료. `_render_bundle_markdown` 분리·targeted 3 PASS·선별 통합은 과거 scoped 수용 | **C03+B:** 기존 CLI 경계/Owner exact blob 위주 read-only KEEP 확인; 무의미한 신규 분리보다 54-owner 분류의 빠른 종료 가능성 판단. **C05:** G1~G3 충족 시 종결. UEF/Writer effect 수정 금지. | 연구 CLI는 P1.6에서도 재사용 가능, 구조 변경 최소 |

## 즉시 결론

1. **바로 종결 심사에 가장 가까운 것은 RF-030**: 새 BODY MOVE보다 canonical exact fake G2/G3 및 RF-074 frozen Owner 정합성 확인.
2. **가장 반복 낭비 위험이 큰 것은 RF-063**: B42/B43 진단 함수 이동은 전체 RF의 resolver/consumer blocker를 직접 제거하지 못함. 안전한 발행 주문은 완료하되 다음 신규 배정은 실제 차단점 해결 우선.
3. **승인 선행은 RF-032**: 관측된 경로 이탈 가능성 때문에 임의 코드 수정·승인 없는 DONE 금지.
4. **RF-026은 핵심 런타임 계약**, P1.6 이관 심사 대상으로 가볍게 돌릴 수 없음.
5. **RF-065는 구조 완벽주의 대신 정확한 KEEP 증거와 CLI 안전 경계**를 우선.

## 나머지 42건

`UNREVIEWED`. 47건 전체를 A/B/C로 판정했다고 주장하지 않는다. 다음 C03은 기존 93개 인덱스 전체를 다시 읽는 대신 **미종결 RF 원본과 최신 stage·G1/G2/G3만** 증분 실사해 `RF | STAGE | A/B/C | P1.6 재사용 근거 | FIRST_UNMET | OWNER | NEXT SAFE ACTION | 승인 필요`를 이어서 작성한다. RF별 계약을 변경하거나 P1.6 이관할 때는 홍사장 승인 필요.

## 불변 안전 규칙

D00·frozen oracle·RF-074 Owner·Guard·Supervisor/Executor·실거래/UEF/RunLab 보호. C03 배정, C04 통합, C05 RF/DONE 단독 권한 유지. 이 문서는 read-only 감사 결과와 실행 인계이며 G1/G2/G3 테스트 성공 증거가 아니다.

근거: `docs/refactor/plan/queue/{01_PENDING/CLAUDE_A/RF-030.md,02_DEVELOPING/CODEX_B/RF-063.md,03_PEER_REVIEW/CLAUDE_A/RF-032.md,02_DEVELOPING/CODEX_B/RF-065.md}`, `docs/refactor/plan/rf_details/RF-{026,030,032,063,065}_IMPLEMENTATION.md`, `docs/refactor/plan/STATUS.md`, #36 C03 6592544237 / C04 6592259700 / C05 6592301333.
