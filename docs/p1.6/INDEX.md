# P1.6 설계 정본 인덱스

상태: DRAFT · 2026-11-03. P1.5 실행과 분리. 이 문서는 파일 존재·정본·승인 상태만 관리하며 내용 중복을 금지한다.

## 현재 확인된 문서
| 문서 | 역할 | 상태 |
|---|---|---|
| [README.md](README.md) | 제품/연구 아이덴티티, 7에이전트, 지식/경험 방향 | 방향 초안 |
| [00_MASTER_PLAN.md](00_MASTER_PLAN.md) | 00~18 작성 순서, 모듈/개발 Wave 제안 | PROPOSED |
| [INDEX.md](INDEX.md) | 정본 라우팅 및 승인 기록 | DRAFT |
| [REQUIREMENTS.md](REQUIREMENTS.md) | 요구사항 ID, 우선순위, 수용 증거 | DRAFT |

미작성 예정: P15_REUSE_INVENTORY, SYSTEM_ARCHITECTURE, AGENT_CONTRACTS, DATA_ARCHITECTURE, KNOWLEDGE_ARCHITECTURE, EXPERIENCE_ARCHITECTURE, SKILLS_MCP_ARCHITECTURE, DECISION_EXECUTION, RESEARCH_EVALUATION, RUNTIME_OBSERVABILITY, SECURITY_OPERATIONS, REPOSITORY_BLUEPRINT, INTERFACE_CATALOG, MIGRATION_PLAN, TEST_STRATEGY, WORK_BREAKDOWN, ACCEPTANCE_GATES. 상세 순서는 [00_MASTER_PLAN](00_MASTER_PLAN.md)을 따른다.

## 확정 정책과 가설 구분
- CONFIRMED: 원격 소스·테스트·계약에서 직접 검증.
- DIRECTED: 홍사장님이 방향을 결정했으나 세부 계약/실험 미확정.
- PROPOSED: 지팀장 설계 제안.
- HYPOTHESIS: 검증 전 시장/연구 가설.
- BLOCKED: P1.5 완료 SHA 또는 승인·증거가 필요.
- FROZEN: 승인 후 변경 관리 대상. 현재 P1.6 문서는 FROZEN 아님.

## 동결 전 체크포인트
D0 요구사항, D1 현행 코드/소비자/키움/Skills 인벤토리, D2 논리 아키텍처/안전, D3 데이터·지식·경험·연구 계약, D4 정확 폴더·파일/DTO/WP, D5 P1.5 최종 SHA 기준 재대조. 각 단계의 승인·미결정·변경 영향을 기록한다.

P1.5 D00/C01~C06/RunLab은 별도 정본. P1.6 문서는 해당 계약을 변경하거나 RF DONE을 선언하지 않는다.
