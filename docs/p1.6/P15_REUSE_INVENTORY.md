# P1.6 — P1.5 재사용 인벤토리 (실사 1차)

상태: PARTIAL / READ-ONLY SOURCE AUDIT · 2026-11-03
기준: GitHub `integration/p1.5`에서 직접 조회한 파일 blob. **최종 P1.5 완료 기준선 아님**. 코드 실행, pytest, import graph 전수 조사 NOT_RUN. 7 agent/키움/Skills 전체 조사 완료 아님.

## 판정 체계
- KEEP: 현재 공개 경계/구현을 보존하는 것이 우선. 변경 없이 P1.6에 적용된다는 보장은 아님.
- ADAPT: 기존 구현을 재사용하면서 새 계약/어댑터 연결 필요.
- REPLACE: 소스·소비자·테스트 근거와 승인 후에만 교체.
- NEW: 기존 동일 책임 구현이 없음을 전수 확인한 뒤 신설. 지금은 PROPOSED.
- UNVERIFIED: 경로/구현/소비자/현재 동작 검증 미완료.

## 실제 소스 확인

| 영역 | 실제 확인 경로 / blob | 직접 확인한 내용 | P1.6 초기 판정 | 다음 검증 |
|---|---|---|---|---|
| Strategist graph | `graphs/nodes/strategist_node.py` / `1b2a7c07` | 역할 주석: 전략 프레이밍, Scanner/Monitor handoff, 직접 주문 금지. LLM router, global sentiment, news, evidence ledger, runtime Strategist modules, canonical artifact import | KEEP + ADAPT | 공개 node/State DTO, import/side-effect, tests |
| Strategist memory | `libs/runtime/strategist/context/memory.py` / `33be9482` | 순수 projection, `facade` 주입으로 기존 monkeypatch/use-time lookup 보존; memory disable/ambiguous playbook 처리 | KEEP + ADAPT | P1.6 Experience/Knowledge read-model 연계; 검증되지 않은 기억 승격 금지 |
| Global market | `libs/market/global_sentiment.py` / `8523d4ca` | DRY_RUN, mock, optional yfinance, US indices/VIX/DXY/10Y normalized signal 근거 | ADAPT | timestamp/as-of, licensing, provider reliability, KR/US calendar, no-lookahead |
| Agent outputs | `libs/contracts/agent_outputs.py` / `ccfc2b89` | 다수 agent output/decision observability 모듈을 가져오는 공개 projection 계층 | KEEP + ADAPT | DTO producer/consumer/version, schema·order parity |
| Output values | `libs/contracts/agent_output_values.py` / `76e489f8` | `agent_outputs.py`에서 분리한 pure value normalization, re-export 호환 주석 | KEEP | 테스트 및 실제 import consumers |
| Monitor policy | `libs/runtime/monitor_policy.py` / `f98d0b95` | dataclass 기반 policy 및 feature 상태·값 normalization | KEEP + ADAPT | Monitor→Supervisor→Guard 계약, no direct order |
| Monitor exit | `libs/runtime/monitor_exit/exit_policy_chart_projection.py` / `e7f5c2b4` | pure projection, facade use-time lookup, side effects original orchestrator 유지 주석 | KEEP + ADAPT | RF-021/026 import cycle, ownership, safe exit parity |
| Evidence ledger | `libs/research/evidence_ledger.py` / `91f141a2` | JSONL append evidence, write lock, runtime path isolation, run_id/agent/stage 기록 | ADAPT | append schema, event time/provenance, durability, write permissions |
| Kiwoom package | `libs/kiwoom/__init__.py` / `e69de29b` | 패키지 파일 존재(빈 파일)만 확인 | UNVERIFIED | API catalog, discovery, planning, broker request, MCP protocol 구현 경로 찾기 |
| Skills | `libs/runtime/skill_map.py`, `libs/runtime/composite_skills.py` 경로 조회 실패 | **해당 경로의 존재를 확인하지 못함**; Skills 미구현 판정 아님 | UNVERIFIED | 실제 경로 탐색, registry/skill_map/composite_skills, 호출·권한·테스트 |

## 설계 문서에서 확보한 보조 근거 (현재 코드 확인과 구분)
- `docs/refactor/plan/rf_details/RF-008_IMPLEMENTATION.md`: Strategist graph에서 `libs/runtime/strategist/llm/`, `context/`로 분리 계획, facade와 LLM/State 효과 보존. **설계 기록이지 현재 모든 이동 완료 증거 아님**.
- `RF-018_IMPLEMENTATION.md`: Strategist context/LLM 소유 경계와 47 경로의 계획.
- `RF-044_IMPLEMENTATION.md`: agent_outputs/agent_output_parts 및 Commander/Scanner/Monitor/Strategist output projection 계획.
- `RF-021_IMPLEMENTATION.md`: monitor_exit 32개 경로 Owner 설계; RF-026과 cross-owner import 위험.
- `RF-070_IMPLEMENTATION.md`: scripts root CLI entry 유지 및 효과 분리 계획.
- `docs/refactor/work_orders/P15_P16_REUSE_TRIAGE_20261103.md`: RF-030/063/032/026/065 미종결 차단점. P1.6 설계의 제약 입력이지 P1.5 완료 판정 아님.

## 현재 가능한 구조적 결정

1. `graphs/nodes/`는 7에이전트의 public orchestration seam 후보. 기존 entrypoint 유지 후 Knowledge/Experience **읽기 전용** 인터페이스 주입을 우선 검토.
2. `libs/contracts/`를 기존 DTO/projection 호환성 기준선으로 삼고 새 `libs/contracts`를 중복 신설하지 않는다.
3. `libs/runtime/strategist/`, `libs/runtime/monitor_exit/`를 기존 Owner 후보로 우선 재사용; 1함수1파일 추가 분할을 성과로 삼지 않는다.
4. `libs/market/`의 글로벌 시그널과 `libs/research/evidence_ledger.py`를 새 시간/지식/경험 계층의 **adapter 연결 후보**로 선정. 데이터 라이선스·시간 정합성·쓰기 권한 검증 전 확정 금지.
5. Skills/키움 MCP 실제 구현 위치와 전체 소비자는 **UNVERIFIED**. 신규 플랫폼을 먼저 만들지 않는다.

## 다음 증분 실사 순서

1. GitHub repo tree에서 Skills, 키움 REST discovery/catalog/planning/request, 7 graph nodes, DTO·events의 실제 경로와 blob 목록 추출.
2. 공개 함수·입출력/소비자/side effects와 tests를 단위별 대조, KEEP/ADAPT/REPLACE/NEW 재판정.
3. 실제 tree 기준 `REPOSITORY_BLUEPRINT` 파일별 target/size/Owner 초안.
4. P1.5 최종 canonical SHA 확정 시 다시 diff하여 FROZEN 승인.

**인수 기준:** 경로·blob·실제 함수·consumer·테스트·권한 근거 없는 '재사용 확정' 금지. P1.5 D00/C01~C06/RF/STATUS 및 RunLab 변경 없음.
