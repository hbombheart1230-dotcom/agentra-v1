> **현재 우선 결정:** [P1.5 중단·권한 해제·P1.6 이관](P15_STOP_AND_HANDOFF_20261105.md). 미완료 이관은 검증 PASS가 아니다.

# Agentra P1.6 — Canonical Document Home

> **STATUS: DESIGN CONSOLIDATION / NOT STARTED / NO RUNTIME AUTHORIZATION (2026-10-30).**
> Canonical branch: integration/p1.5. P1.5 is stopped; unresolved work transfers to P1.6. See P15_STOP_AND_HANDOFF_20261105.md.

## Read only these three active documents

1. **[README.md](README.md)** — entrypoint, authority, document map and P1.5 continuity.
2. **[MASTER_PLAN.md](MASTER_PLAN.md)** — product identity, seven-department responsibilities, target architecture, scope and pruning decisions.
3. **[VALIDATION_AND_HANDOFF.md](VALIDATION_AND_HANDOFF.md)** — P1.5-to-P1.6 handoff, evidence gates, candidate framework benchmark, independent verification and operational restrictions.

No implementation packet, agent, scheduler, dependency, settings file, or P1.6 runtime is authorized by opening this folder. Do not open the archived 2026-10-12 packets as current work instructions.

## Current authority and execution continuity

P1.5 신규 개발과 C01~C06 반복 지시는 종료되었다. 잔여 작업은 P1.6으로 이관하며 지팀장 전용 쓰기·승인 제한은 폐지한다. 운영 런타임 안전 제한은 유지한다.
P1.5 신규 개발과 C01~C06 반복 지시는 종료되었다. 잔여 작업은 P1.6으로 이관하며 지팀장 전용 쓰기·승인 제한은 폐지한다. 운영 런타임 안전 제한은 유지한다.
- The older [P1.5/P1.6 master plan](../p1_5_p1_6_master_plan.md) is historical roadmap context. Its narrow P1.6 orchestration-only scope is superseded **for future design planning in this folder** by the user's 2026-10-30 direction; its frozen P1.5 execution/safety gates and later P2–P8 phase boundaries remain intact.
- Earlier [Architecture V2](../../architecture/architecture_v2.md) and [Q100 design](../../research/q100_research_and_learning_roadmap.md) are reference designs, not deployed proof and not competing P1.6 entrypoints. Exact current implementation must be verified at P1.5 freeze.

## Identity snapshot — direction agreed, formal freeze pending

Agentra targets an **AI-led, short-horizon quant trading desk**: scalping/intraday and 2–3 day swing; approximately three concurrent holdings (design target, not a live limit change). Seven specialist departments research autonomously; Commander makes portfolio investment decisions, while Supervisor/guards and Executor keep independent safety/side-effect authority. No long-term portfolio investment objective.

P1.6 first **decides what the system is and what to remove**, then conditionally assesses custom orchestration vs LangGraph vs pydantic-graph. It also defines future seams for model routing, bounded adaptive policy, Q/UEF/Q100 experience retrieval and an out-of-band AI Engineering Lab; it does **not** prematurely implement P2–P8 capabilities.

## Archived old planning material

The five original 2026-10-12 documents are preserved **byte-identically** under [archive/2026-10-12_orchestration_only/](archive/2026-10-12_orchestration_only/):

- CODE_AUDIT.md — historical source inspection on old, unfrozen branch SHAs.
- IMPLEMENTATION_BLUEPRINT.md — old graph-engine-only file/function proposal.
- STATE_ROUTING_AND_ENGINE_DESIGN.md — old graph state/retry sketches.
- BUILD_PACKETS_AND_TEST_MATRIX.md — old, inactive WO-16.0–16.6 work packets.
- BENCHMARK_AND_GATES.md — old framework parity/benchmark gate proposal.

**All five are reference-only.** Their obsolete branch, SHA, Claude-implementation/Codex-audit assignments and implementation-only assumptions must not become live orders. Benchmarks and old interface examples require fresh verification after P1.5 closes. Preserve history and links; do not duplicate the five documents into new active counterparts.

## Change control

현재 권한·이관 정책은 P15_STOP_AND_HANDOFF_20261105.md를 따른다. 과거 문서 통합 범위 제한은 현재 담당자의 쓰기를 제한하지 않는다.
