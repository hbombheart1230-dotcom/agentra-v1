# Agentra P1.6 설계 마스터 플랜 (2026-11-03)

상태: PROPOSED. P1.5 D00/RF/STATUS/FAST-3/RunLab 수정 금지. 제품 성과와 학술 검증은 동등 목표. 7에이전트 유지. README.md가 P1.6 제품·연구 아이덴티티의 정본이다.

## 문서 작성·승인 순서

| 순서 | docs/p1.6 파일 | 내용 |
|---|---|---|
| 00 | INDEX.md | 문서 정본, 결정 상태, 의존성 |
| 01 | REQUIREMENTS.md | 제품·연구 요구, 정량 수용 기준 |
| 02 | P15_REUSE_INVENTORY.md | 현행 소스/DTO/Skills/키움/docs 재사용 조사 |
| 03 | SYSTEM_ARCHITECTURE.md | 계층, 데이터 흐름, 신뢰 경계 |
| 04 | AGENT_CONTRACTS.md | 7에이전트 역할, 권한, IO |
| 05 | DATA_ARCHITECTURE.md | 글로벌·국내 데이터, 시간·출처·저장 |
| 06 | KNOWLEDGE_ARCHITECTURE.md | 관계, 가설, 신뢰도, 버전·폐기 |
| 07 | EXPERIENCE_ARCHITECTURE.md | 결정, 반론, 주문, 결과, 오류 학습 |
| 08 | SKILLS_MCP_ARCHITECTURE.md | 개발/런타임 Skills, 키움 및 외부 어댑터 |
| 09 | DECISION_EXECUTION.md | 승인, Guard, Executor, 멱등성 |
| 10 | RESEARCH_EVALUATION.md | 백테스트, 워크포워드, ablation |
| 11 | RUNTIME_OBSERVABILITY.md | 이벤트, 스케줄, 장애 복구, 감사 |
| 12 | SECURITY_OPERATIONS.md | 보안, 비밀, 권한, 배포·롤백 |
| 13 | REPOSITORY_BLUEPRINT.md | 전체 폴더 트리, 파일별 책임과 크기 |
| 14 | INTERFACE_CATALOG.md | DTO, 이벤트, API, 스키마·버전 |
| 15 | MIGRATION_PLAN.md | P1.5→P1.6 단계별 전환과 호환 |
| 16 | TEST_STRATEGY.md | unit, contract, integration, replay, safety |
| 17 | WORK_BREAKDOWN.md | 전체 Capability→Module→WP/RF, 소유·의존성 |
| 18 | ACCEPTANCE_GATES.md | 설계·구현·통합·연구 수용 기준 |

문서마다 DRAFT→REVIEWED→APPROVED→FROZEN. 13·14는 03~12를 검토하며 왕복 수정한 뒤 동시 확정한다. 17은 13~16에 근거하여 확정. 하나의 개념은 하나의 정본에서만 정의하고 다른 문서는 링크한다.

## 논리 구조

외부 글로벌/KR 데이터·키움·검증된 외부 MCP/Skills → Provider Adapter/Time/Provenance/DTO → Market Store + Knowledge & Experience Layer → 기존 7에이전트 → Supervisor/Guard → Executor/Broker → Reporter/Event Log → 검증된 지식 갱신.

Knowledge Layer는 8번째 에이전트가 아니다. Monitor 직접 주문 금지, 실거래 기본 차단, 승인 없는 주문 금지, 동일 intent 중복 금지, 지식의 자동 무검증 승격 금지.

## 모듈 설계 기준 (초안)

- Production Python 파일 권장 100~300 logical LOC, 400 LOC부터 검토, 600 LOC 초과 예외 승인. 단일 책임과 부작용 경계가 크기보다 우선.
- 함수 권장 10~50 LOC, 80 LOC 초과 분리 검토. CLI/호환 facade/generated code 예외 가능.
- 1함수 1파일 양산 금지. 순환 import 0 목표. 도메인 DTO는 외부 provider SDK에 의존하지 않는다.
- IO/DB/LLM/주문 부작용은 명시적 효과 Owner만 수행. 기존 소스·소비자·패치 seam 보존.
- 정확 파일 수·크기·DB·모델·저장 용량은 실제 repo 인벤토리와 벤치마크 이후 확정.

## 폴더 후보 (PROPOSED, 실제 생성/이동 아님)

```text
docs/p1.6/
libs/contracts/          # DTO/events/schema
libs/market_data/        # data/time/provenance
libs/knowledge/          # evidence/relations/hypotheses
libs/experience/         # decisions/outcomes/attribution
libs/capabilities/       # skills/MCP registry and permissions
libs/research/           # experiments/backtest/ablation
libs/runtime/            # existing seven-agent runtime
libs/execution/          # existing safety/approval boundary
libs/reporting/          # existing reporter/observability
integrations/providers/  # external provider adapters
integrations/mcp/        # MCP adapters
integrations/skills/     # runtime skills
tests/p16/               # contract/data/knowledge/experience/safety/research
```

기존 libs/scripts/graphs/tests 및 키움/Skills 실사 후 중복 경로를 피한다. integrations 신설도 미확정.

## 구현 순서 (Capability Wave)

W0 현행 코드·라이선스·소비자 인벤토리와 KEEP/ADAPT/REPLACE/RETIRE → W1 DTO/이벤트/시간·출처·어댑터 → W2 글로벌/KR 수집·정합·replay → W3 Knowledge 최소 수직 절편 → W4 Experience 최소 수직 절편 → W5 기존 7에이전트에 read-only Skills/MCP/지식 연결 → W6 Supervisor/Guard/Executor fake 통합 → W7 연구·제품 평가/ablation/비용 → W8 운영·관측·복구·배포 → W9 최종 안전·실험 인수.

개별 작업 단위는 Capability→Module→WP(RF형 작업 패키지)→Test Gate. 작업 ID/총수는 W0 실사 후 확정하며 P1.5 RF 숫자에 맞추지 않는다.

각 WP 필수 필드: WP_ID, CAPABILITY, SOURCE_PATH/BLOB, TARGET_PATH, OWNER, KEEP/ADAPT/REPLACE/NEW, INPUT/OUTPUT DTO, EFFECTS, CONSUMERS, DEPENDENCIES, SIZE_ESTIMATE, TESTS, ACCEPTANCE, P1.5_RF_LINK, STATUS.

P1.6 게이트 제안: G0 요구/연구, G1 architecture/contract, G2 source/target/owner, G3 code/targeted test, G4 integration/safety, G5 evaluation/release. P1.5 G1~G3와 별개.

## 당장 할 일

1. INDEX 작성, 2. REQUIREMENTS 정리, 3. 현행 GitHub 인벤토리와 P1.5 잔여 RF 재사용 대조, 4. 아키텍처·데이터·지식·경험·권한 계약, 5. 폴더·모듈·인터페이스·작업 패키지 전수 설계, 6. 구현 전 의존성·검증 기준 확정.

P1.5는 C05/C06·RunLab의 상태·안전·계약 변경만 모니터링하며 자동화가 개발/통합/종결을 계속 담당한다. P1.6 설계 문서가 기존 실행 지시보다 우선하지 않는다.
