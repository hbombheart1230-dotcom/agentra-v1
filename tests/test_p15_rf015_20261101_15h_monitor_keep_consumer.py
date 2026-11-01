"""RF-015 A15-1: pure Monitor projection helpers, in-memory dict contract tests.

No monitor_node, no event writers, no IO/network, no orders.
"""
from __future__ import annotations

import copy
from types import SimpleNamespace

from libs.agents.monitor.events.cycle_event_payloads import build_state_transition_event_payload
from libs.agents.monitor.projections.cycle_detail_projection_exit_decision_detail import (
    cycle_detail_blocked_rules_reason_chain,
)


def test_m1_blocked_rules_reason_chain_exact_tuple():
    exit_info = {"triggered": True, "reason": "take_profit", "sell_guard_blocked": True,
                 "sell_guard_reason": "no_fill", "monitor_reason": "risk"}
    entry_info = {"triggered": True, "pattern": "breakout", "guard_blocked": True,
                  "guard_reason": "cooldown", "failed_checks": ["spread", "", None],
                  "reason": "entry_wait"}
    state = {"monitor_output": {"entry_exit_reason": "NOOP"}}
    snap = copy.deepcopy((exit_info, entry_info, state))

    out = cycle_detail_blocked_rules_reason_chain(exit_info, entry_info, state, facade=SimpleNamespace())

    assert out == (["cooldown", "no_fill", "spread"],
                   ["risk", "take_profit", "entry_wait", "NOOP"],
                   ["take_profit", "entry:breakout"])
    assert (exit_info, entry_info, state) == snap
    for key in ("orders", "fills", "intents"):
        assert key not in state


def test_m1_empty_inputs_yield_three_empty_lists():
    assert cycle_detail_blocked_rules_reason_chain({}, {}, {}, facade=SimpleNamespace()) == ([], [], [])


def test_m2_state_transition_payload():
    exit_info = {"active_exit_axis": "", "triggered": False}
    entry_info = {"triggered": True, "pattern": "breakout"}
    trace = {"became_ready_this_cycle": True, "last_blocking_axis": "spread",
             "transition_readiness_score": 0.8}
    prev = {"active_exit_axis": "stop"}
    snap = copy.deepcopy((exit_info, entry_info, trace, prev))

    out = build_state_transition_event_payload(
        current_posture="WAIT", current_reason="no_signal", entry_info=entry_info,
        entry_transition_trace=trace, exit_info=exit_info, previous_monitor_state=prev,
        previous_posture="WATCH", previous_reason="candidate", state_changed=True)

    assert out["previous_posture"] == "WATCH" and out["current_posture"] == "WAIT"
    assert out["previous_reason"] == "candidate" and out["current_reason"] == "no_signal"
    assert out["state_changed"] is True
    td = out["trigger_delta"]
    assert td["previous_active_exit_axis"] == "stop"
    assert td["current_active_exit_axis"] == ""
    assert td["exit_triggered"] is False
    assert td["entry_triggered"] is True
    assert td["entry_pattern"] == "breakout"
    assert td["became_ready_this_cycle"] is True
    assert td["last_blocking_axis"] == "spread"
    assert td["transition_readiness_score"] == 0.8
    assert (exit_info, entry_info, trace, prev) == snap
