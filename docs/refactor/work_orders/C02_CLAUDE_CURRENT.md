# C02 — Claude A | A-20261101-15-C03 | RF-015 PEER → FAST-3 CLOSEOUT | SUPPLY_GAP

**START PIN:** Record `CANONICAL_HEAD`, `C02_ORDER_BLOB`, `A_REMOTE_HEAD`, `ORDER_ID` before changes. Previously started safe orders remain valid until finished. Execute this one order; no D00/RF/queue/C03/HANDOFF exploration, no autonomous RF selection. A owns only A-branch code/tests on `work/p15-a-reporter-pure-20261021`; C03 alone edits C02. C04 integrates; C05 alone changes RF/STATUS/DONE.

**REMOTE FACTS VERIFIED AT ISSUANCE:** canonical `881ad95edcbf1e10318fdc133d79225bd5da1a56`; A HEAD `2d0113858d5984a4206083f4405489b690e61d47`. A14-R1 real Scanner consumer normal 4 PASS and A14-R2 RF-050 KEEP research are REMOTE_DONE, integrated at `d4546683ddf89cac7a6a2290c4280ddc845e241a`. **RF-014 is now C05 physical 05_DONE (33/93)**, so do NOT rerun A14, move pinned Scanner sources, or relabel RF-014 as unfinished. RF-035 is also DONE. Next unfinished A priority is **RF-015 / 03_PEER_REVIEW**; 19 Monitor Owner files are already located in `libs/agents/monitor/`. Existing A 19/19 cold-import and historic tests are evidence to reuse, not blanket rerun.

## A15-1 | RF-015 CLAUDE_A — NEW bounded pure Monitor consumer contract G2

**READ-ONLY PRODUCTION SOURCES (identical canonical+A blobs):**
- `libs/agents/monitor/projections/cycle_detail_projection_exit_decision_detail.py::cycle_detail_blocked_rules_reason_chain`, blob `fe67e0012d72ec08ce66fcc89c53de517cec0e1b`, current body constructs three lists (blocked, reason, triggered) from exit/entry/state; `facade` parameter is accepted but not used by this helper.
- `libs/agents/monitor/events/cycle_event_payloads.py::build_state_transition_event_payload`, blob `633f9afbb422c6970cb1597aecb5e24b358d5481`, pure transition dictionary body.
- `graphs/nodes/monitor_node.py` and shared State/Broker/Guard are READ ONLY, never execute the live node. Do not refactor these existing single-Owner bodies without a proven defect.

**NEW A-OWNED TEST FILE ONLY:** `tests/test_p15_rf015_20261101_15h_monitor_keep_consumer.py`. Use pytest and in-memory dicts; do not call `monitor_node` or event writers. Case M1: call `cycle_detail_blocked_rules_reason_chain(exit_info,entry_info,state,facade=SimpleNamespace())` with:
`exit_info={'triggered':True,'reason':'take_profit','sell_guard_blocked':True,'sell_guard_reason':'no_fill','monitor_reason':'risk'}`;
`entry_info={'triggered':True,'pattern':'breakout','guard_blocked':True,'guard_reason':'cooldown','failed_checks':['spread','',None],'reason':'entry_wait'}`;
`state={'monitor_output':{'entry_exit_reason':'NOOP'}}`.
Expect exact tuple `(['cooldown','no_fill','spread'],['risk','take_profit','entry_wait','NOOP'],['take_profit','entry:breakout'])`. Empty input dicts yield three empty lists; inputs remain deep-equal before/after; no order/fill/intent or file/network call.
Case M2: call `build_state_transition_event_payload` with `current_posture='WAIT'`, `current_reason='no_signal'`, `previous_posture='WATCH'`, `previous_reason='candidate'`, `state_changed=True`, `previous_monitor_state={'active_exit_axis':'stop'}`, `exit_info={'active_exit_axis':'','triggered':False}`, `entry_info={'triggered':True,'pattern':'breakout'}`, `entry_transition_trace={'became_ready_this_cycle':True,'last_blocking_axis':'spread','transition_readiness_score':0.8}`. Expect previous/current posture, state_changed=True, `trigger_delta.previous_active_exit_axis='stop'`, `current_active_exit_axis=''`, `entry_triggered=True`, `became_ready_this_cycle=True`, `transition_readiness_score=0.8`. Use exact original signature, do not assume a return wrapper.
Case M3: use fake monkeypatch on any imported real writer/HTTP entry to raise if touched, but only if the patch point is actually imported by this test; do not claim a call-counter PASS for an unbound patch. The two pure functions must not invoke IO. Add an import/consumer reference assertion only if it is a real imported symbol, not a fabricated runtime path.

**NORMAL targeted:** `python -m pytest -q tests/test_p15_rf015_20261101_15h_monitor_keep_consumer.py`, expected 2-3 tests exit0, NOT_RUN at issuance. If current actual signature/return differs, record exact mismatch and stop only the affected case; do not weaken oracle to hide a failure. Preserve pre-existing 11 historical FAIL as baseline evidence, not a mandatory full suite/peer rerun. No production code edit unless C03 supplies a separately verified bounded defect.

## A15-2 | RF-015 G1/KEEP / C05 handoff, read-only

Confirm current unchanged SOURCE blobs above and single Owner responsibility: Monitor projections build data only, orchestrator retains State/event/order effects. Use existing cold-import 19/19 evidence at unchanged blobs, not same-SHA rerun. Return `KEEP_VERIFIED|SOURCE::FUNCTION|BLOB|reason` for two helpers, exact newly tested file SHA, normal exit and A remote push. If the consumer path is not demonstrated by these pure helpers, label `CONSUMER_PARTIAL` and state the precise missing caller seam; do NOT claim whole RF-015 DONE. C04 selects only new test and exact SOURCE; C05 decides G1/G2/G3 and physical stage. RF-050 is PEER candidate only after RF-015, no repeat A14 read-only research.

## SUPPLY_GAP / RESERVE / DELIVERY

**A NEW_READY=0/8; RESERVE_VERIFIED=0/6 (RESERVE_NOT_VERIFIED), SUPPLY_GAP.** These tests/KEEP are **not** BODY MOVE. RF-014 and RF-035 already DONE; RF-031 previous bodies and RF-050 policy slot already split; the 19 Monitor functions inspected here are existing single-Owner projection bodies, not verified new 404 TARGET moves. C03 has NOT verified eight new safe A-owned SOURCE→TARGET bodies with owner, effect and original golden; inventing targets would harm RF DONE priority. NEXT C03: audit unfinished A RF-015/050/031/032/033/034 for genuine necessary new Owner moves, with full SOURCE/blob/TARGET 404/IO/test proof before supply.

A writes ONLY the new test on its branch, runs normal targeted once, normal pushes/re-fetches, and comments #11 `ORDER_ID | SOURCE_BLOBS | TEST_BLOB | NORMAL_COMMAND/EXIT | A_REMOTE_SHA/PUSH_BLOCKED | G1/G2/G3_FIRST_UNMET | NEXT | measured START/END`. If pytest unavailable, stdlib smoke is acceptable when executable and reproducible; report TEST_BLOCKED separately from PUSH_BLOCKED. Do not run live/real/Broker/Guard/Step5C/UEF/RunLab, alter frozen oracle or change other owners' files.
