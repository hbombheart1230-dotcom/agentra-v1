"""RF-015 A16-1: REAL ``monitor_node(state)`` caller consumes the Monitor Owner helpers.

The two Owner helpers are wrapped with recording delegates that call the ORIGINAL
functions. All reachable effect boundaries are faked; tmp_path / in-memory only.
"""
from __future__ import annotations

import copy
import importlib

import pytest

monitor_module = importlib.import_module("graphs.nodes.monitor_node")


@pytest.fixture
def harness(monkeypatch, tmp_path):
    monkeypatch.setenv("USE_EXIT_POLICY", "false")
    h = {
        "chain_calls": [], "chain_returns": [],
        "trans_calls": [], "trans_returns": [],
        "events": [], "effects": [],
    }
    orig_chain = monitor_module.cycle_detail_blocked_rules_reason_chain
    orig_trans = monitor_module.build_state_transition_event_payload

    def chain(*args, **kwargs):
        h["chain_calls"].append((args, kwargs))
        r = orig_chain(*args, **kwargs)
        h["chain_returns"].append(r)
        return r

    def trans(*args, **kwargs):
        h["trans_calls"].append((args, kwargs))
        r = orig_trans(*args, **kwargs)
        h["trans_returns"].append(r)
        return r

    def emit(state, *, name, payload, level="info", symbol=""):
        h["events"].append((name, copy.deepcopy(payload)))

    def effect(label, ret=None):
        def _f(*a, **k):
            h["effects"].append(label)
            return ret
        return _f

    previous = {"posture": "WATCH", "reason": "candidate", "active_exit_axis": "stop"}
    monkeypatch.setattr(monitor_module, "cycle_detail_blocked_rules_reason_chain", chain)
    monkeypatch.setattr(monitor_module, "build_state_transition_event_payload", trans)
    monkeypatch.setattr(monitor_module, "_emit_monitor_event", emit)
    monkeypatch.setattr(monitor_module, "record_raw_input", effect("record_raw_input"))
    monkeypatch.setattr(monitor_module, "record_decision_bridge", effect("record_decision_bridge"))
    monkeypatch.setattr(monitor_module, "append_decision_trace", lambda state, *a, **k: state)
    monkeypatch.setattr(monitor_module, "_log_monitor_summary", effect("log_summary"))
    monkeypatch.setattr(monitor_module, "write_monitor_artifact", effect("write_artifact"))
    monkeypatch.setattr(monitor_module, "_save_current_monitor_state", effect("save_state"))
    monkeypatch.setattr(monitor_module, "_persist_overnight_decision", effect("persist_overnight"))
    monkeypatch.setattr(monitor_module, "_persist_eod_carry_decisions_for_open_positions",
                        effect("persist_eod_carry", {}))
    monkeypatch.setattr(monitor_module, "save_quant_shadow_candidates_for_state", effect("shadow", {}))
    monkeypatch.setattr(monitor_module, "_load_previous_monitor_state",
                        lambda state, symbol: dict(previous))
    h["previous"] = previous
    return h


def _state(tmp_path):
    return {
        "plan": {"thesis": "test"},
        "selected": {"symbol": "005930", "price": 71000.0,
                     "features": {"engine_volatility20": 0.02}},
        "portfolio_snapshot": {"cash": 2_000_000.0, "positions": []},
        "policy": {"use_exit_policy": False},
        "reports_root": str(tmp_path / "reports"),
    }


def test_m1_caller_consumes_blocked_rules_reason_chain(harness, tmp_path):
    state = _state(tmp_path)
    out = monitor_module.monitor_node(state)

    assert len(harness["chain_calls"]) == 1
    blocked, reason, triggered = harness["chain_returns"][0]
    assert out["monitor_evaluation"]["triggered_rules"] == triggered
    assert out["monitor_action_decision"]["decision_reason_chain"] == reason
    assert out["monitor_evaluation"]["blocked_rules"] == list(dict.fromkeys(blocked))[:8]


def test_m2_caller_consumes_state_transition_payload(harness, tmp_path):
    out = monitor_module.monitor_node(_state(tmp_path))

    assert len(harness["trans_calls"]) == 1
    payload = harness["trans_returns"][0]
    emitted = [p for n, p in harness["events"] if n == "state_transition"]
    assert emitted == [payload]
    assert "monitor_state_transition" in out
    trace = payload["trigger_delta"]
    assert out["monitor"]["entry_transition_trace"] == out["monitor_output"]["entry_transition_trace"]
    assert trace["became_ready_this_cycle"] == bool(out["monitor"]["entry_transition_trace"].get("became_ready_this_cycle"))
    assert payload["previous_posture"] == "WATCH" and payload["previous_reason"] == "candidate"
    assert payload["state_changed"] == bool(
        payload["previous_posture"] != payload["current_posture"]
        or payload["previous_reason"] != payload["current_reason"]
    )
    assert trace["previous_active_exit_axis"] == "stop"


def test_m3_no_live_effect_and_no_actual_intent(harness, tmp_path):
    out = monitor_module.monitor_node(_state(tmp_path))
    intents = out.get("intents") or []
    assert not [i for i in intents if str((i or {}).get("side") or "").upper() in ("BUY", "SELL")], intents
    assert "persist_overnight" not in harness["effects"]
    assert len(harness["chain_calls"]) == 1 and len(harness["trans_calls"]) == 1
