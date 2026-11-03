# Agentra P1.6 요구사항과 수용 기준

상태: DRAFT / 홍사장 방향 반영, 상세 목표 미승인 · 2026-11-03
정본: 제품/연구 정체성은 [README](README.md), 작성 순서는 [00_MASTER_PLAN](00_MASTER_PLAN.md). 아래 ID는 설계 추적용이며 구현 완료를 의미하지 않는다.

## A. 제품·에이전트
| ID | 요구사항 | 우선 | 수용 기준(초안) |
|---|---|---|---|
| PR-01 | Commander, Strategist, Scanner, Monitor, Supervisor, Executor, Reporter 7역할 유지 | MUST | 기존 P1.5 경계/소비자와 계약 매핑 |
| PR-02 | 국내 주식시장에 글로벌 데이터와 관계·경험 지식을 활용 | MUST | 시점 보존 데이터→가설→판단 end-to-end replay |
| PR-03 | 실제 수익성과 학술 검증을 동등하게 평가 | MUST | 비용 반영 성과 지표와 별도 연구 지표·베이스라인 |
| PR-04 | 기존 Skills/키움/DTO/P1.5 자산 우선 재사용 | MUST | 소스 SHA·소비자 기반 KEEP/ADAPT/REPLACE/NEW 근거 |
| PR-05 | 외부 MCP/Skills는 교체 가능한 권한 제한 어댑터 | MUST | 무단 주문 경로 없음, failure isolation |
| PR-06 | 설명 가능한 결정과 감사·재현성 | MUST | run_id/intent_id/evidence version 연결 |

## B. 데이터·지식·경험
| ID | 요구사항 | 우선 | 수용 기준(초안) |
|---|---|---|---|
| DK-01 | KR/US 시차·DST·휴장·관측가능 시점 처리 | MUST | as-of 재생 시 미래 정보 접근 차단 테스트 |
| DK-02 | 출처·수집시점·유효시점·수정 이력·라이선스 추적 | MUST | lineage와 수정 버전 재현 |
| DK-03 | 지식 가설에 증거·반증·신뢰도·국면·만료 기록 | MUST | 검증/감쇠/폐기 가능, 검증 전 가설 분리 |
| DK-04 | 판단·반론·거절·주문·결과·예측오차 경험 연결 | MUST | decision→outcome 추적과 사후평가 |
| DK-05 | 지식 갱신은 검증 게이트 통과 후만 허용 | MUST | 결과 누출·무검증 승격 방지 |

## C. 실행 안전·운영
| ID | 요구사항 | 우선 | 수용 기준(초안) |
|---|---|---|---|
| SF-01 | Monitor 직접 주문 금지, Supervisor/Guard/Executor 경계 유지 | MUST | 권한 부정·우회 테스트 |
| SF-02 | 실거래 기본 차단, 승인 기반 주문, 멱등성 | MUST | fake order/veto/retry/duplicate 테스트 |
| SF-03 | 오류·중단·복구 후 감사 추적 보존 | MUST | replay와 상태 복원 |
| SF-04 | 기존 P1.5 계약을 승인 없이 완화하지 않음 | MUST | baseline SHA와 차이/승인 기록 |
| SF-05 | 개인정보·비밀·브로커 자격증명 격리 | MUST | 로그/도구 응답의 비밀 노출 방지 테스트 |

## D. 연구
| ID | 요구사항 | 우선 | 수용 기준(초안) |
|---|---|---|---|
| RS-01 | 글로벌→한국시장 선행 관계는 검증 전 가설 | MUST | 시장 국면/시간차/거래 가능 시점별 검증 |
| RS-02 | 국내-only vs 글로벌 추가 vs 관계 지식 vs 경험 지식 ablation | MUST | 동일 기간·종목·비용·정보 시점 비교 |
| RS-03 | walk-forward, 데이터 누출 방지, 비용·슬리피지 반영 | MUST | 재현 가능한 실험 manifest/seed/data version |
| RS-04 | 수익·위험·통계적 불확실성·실패를 함께 보고 | MUST | 지표/신뢰구간/실패 사례 보고 |
| RS-05 | 논문 신규성은 선행연구와 실험 후 판단 | MUST | 검증되지 않은 신규성 주장 금지 |

## E. 아키텍처·개발 품질
| ID | 요구사항 | 우선 | 수용 기준(초안) |
|---|---|---|---|
| AR-01 | 단일 Owner, DTO와 효과 경계, 의존성 방향 | MUST | import/consumer map, 순환 import 방지 |
| AR-02 | 기존 코드 중복 재개발 방지 | MUST | inventory 기반 build-vs-integrate 결정 |
| AR-03 | 폴더·모듈·파일 크기와 전체 WP/RF 개발 순서를 사전 설계 | MUST | path/size estimate/dependency/acceptance 추적 |
| AR-04 | P1.5 목표 기준선으로 조건부 설계, 최종 SHA에서 동결 | MUST | baseline reconciliation PASS |
| AR-05 | 기능과 안전 계약별 자동 테스트·독립 검증 | MUST | unit/contract/integration/safety/research gate |

## 아직 정해야 할 수치·선택 (TBD)
- 실거래/모의거래 범위와 명시적 승인 경계, 투자 대상 종목군·빈도·운영 시간.
- 성과 목표(수익률, 최대낙폭, 지연, 가용성), 비용·슬리피지, 데이터 제공자와 라이선스.
- 저장소 엔진·보존 기간·용량, 모델·추론 예산, MCP/Skills 제공자.
- 연구 데이터 기간, 베이스라인, 표본 크기와 통계적 검정 방법.
- 실제 파일 경로·모듈 LOC·작업 패키지 수는 현행 소스 인벤토리 및 P1.5 최종 SHA 재대조 뒤 확정.

## 다음 단계
1. 현행 P1.5 실제 repo의 7 agents/DTO/Skills/키움 API·소비자·테스트 인벤토리 작성.
2. 요구 ID를 시스템/데이터/지식/경험/실행 설계 문서에 매핑.
3. 모든 TBD를 ADR로 결정하고 홍사장 승인 후 DRAFT→REVIEWED→FROZEN.

P1.5 자동화와 RunLab은 별도 진행. 이 문서는 실행 주문이 아니다.
