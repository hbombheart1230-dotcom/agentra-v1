# Supervisor and Executor modularization — P1.6 design draft

Status: PROPOSED. This document is planning only and does not change P1.5 execution behavior.

## Verified source inventory (integration/p1.5)
| Path | Blob prefix | Design observation |
|---|---|---|
| libs/risk/supervisor.py | cb7deb0b | Deterministic risk policy and AllowResult |
| libs/supervisor/two_phase.py | de930281 | OrderIntent, Decision, TwoPhaseSupervisor |
| libs/agent/executor.py | 6f5c8ac8 | AgentExecutor public wrapper |
| libs/agent/executor/agent_executor.py | 3135159a | Similar AgentExecutor wrapper, duplication candidate |
| libs/execution/executors/real_executor.py | eb0a0953 | Broker HTTP execution and safety boundary |
| graphs/nodes/execute_from_packet.py | 1a10af59 | Execution orchestration and lifecycle |
| graphs/nodes/executor_node.py | 832c6a30 | Pending-only graph stub; not an order sender |

Supervisor graph entrypoint remains unverified.

## Design
Supervisor: separate intent normalization, pure risk assessment, approval decision, evidence projection, and compatibility facade.

Executor: separate approved-intent adaptation, idempotency, broker mapping, order lifecycle, external effect boundary, execution evidence, and compatibility facade.

Keep existing package ownership first. Reduce duplicate implementations and oversized orchestration; do not create one-function-per-file modules. File size guideline: 100–300 logical lines; review above 400; exception review above 600.

## Work packages
| ID | Scope | Dependency |
|---|---|---|
| SUP-01 | Map current Supervisor entrypoints, consumers and tests | P1.5 baseline |
| SUP-02 | Design risk and approval state contracts | SUP-01 |
| SUP-03 | Design evidence and compatibility facade | SUP-02 |
| EXE-01 | Map both AgentExecutor implementations and consumers | P1.5 baseline |
| EXE-02 | Design intent, idempotency and lifecycle contracts | EXE-01, SUP-02 |
| EXE-03 | Separate broker adapter from effect owner | EXE-02 |
| EXE-04 | Slim execute_from_packet orchestration | EXE-02, EXE-03 |
| SX-01 | Contract and safety regression suite | SUP-03, EXE-04 |

## Non-negotiable invariants
Existing approvals, broker write restrictions, fail-closed behavior, order deduplication and public contracts must not be weakened. All code changes require current-source consumer analysis, regression tests, and the relevant P1.5 ownership approvals. The duplicated AgentExecutor wrappers are candidates for consolidation, not approved deletions.

Final paths, sizes and tests will be reconciled against the completed P1.5 canonical commit before freezing the P1.6 blueprint.
