"""RF-030 A26-8: ``operator_visibility._build_run_contexts`` original vs thin wrapper + Owner.

Pins: A preimage ``b2e48863`` blob 8444ae44, canonical ``7dd8a2ad`` blob 26c71139; the original function AST must be
IDENTICAL across both before any parity claim. The original is compiled in a copy of the live module namespace (same
helper objects); dependency overrides apply to both sides. Pure aggregation over supplied rows; guards for IO.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import inspect
import socket
import subprocess
from pathlib import Path

import pytest

A_PRE = "b2e48863ae8a44d7ab41090160816d504052f2e0"
A_BLOB = "8444ae44328ccface4c18c3a74d87a83979cd54b"
CANON = "7dd8a2ad54228ca7f9e5530f07f39b324a55fdb9"
CANON_BLOB = "26c71139e363632e914dff16e690ef2d209277c6"
PATH = "libs/reporting/operator_visibility.py"
NAME = "_build_run_contexts"
ov = importlib.import_module("libs.reporting.operator_visibility")
owner = importlib.import_module("libs.reporting.operator_visibility_build_run_contexts")


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


def _show(commit):
    return subprocess.run(["git", "show", f"{commit}:{PATH}"], check=True, capture_output=True).stdout


def _fn(raw):
    tree = ast.parse(raw.decode("utf-8"))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == NAME]
    assert len(nodes) == 1
    return nodes[0]


@pytest.fixture(scope="module")
def orig_node():
    try:
        a_raw, c_raw = _show(A_PRE), _show(CANON)
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(a_raw) == A_BLOB, "BLOCKED_PIN actor blob"
    assert _sha(c_raw) == CANON_BLOB, "BLOCKED_PIN canonical blob"
    a_node, c_node = _fn(a_raw), _fn(c_raw)
    assert ast.dump(a_node, include_attributes=False) == ast.dump(c_node, include_attributes=False), \
        "HOLD RF030: original function differs between actor and canonical"
    return a_node


def test_original_function_identical_actor_vs_canonical(orig_node):
    a_src = ast.get_source_segment(_show(A_PRE).decode(), orig_node)
    c_src = ast.get_source_segment(_show(CANON).decode(), _fn(_show(CANON)))
    assert a_src == c_src and len(a_src.splitlines()) >= 320


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(Path, "mkdir", boom)
    monkeypatch.setattr(Path, "write_text", boom)
    monkeypatch.setattr(Path, "read_text", boom)


def ev(run_id, stage, event, payload=None, epoch=0, **extra):
    row = {"run_id": run_id, "stage": stage, "event": event, "payload": payload if payload is not None else {}, "_epoch": epoch}
    row.update(extra)
    return row


def check(orig_node, monkeypatch, rows, overrides=None):
    overrides = overrides or {}
    ns = dict(vars(ov))
    mod = ast.Module(body=[copy.deepcopy(orig_node)], type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), f"<{A_PRE[:8]}:{PATH}>", "exec"), ns)
    for k, v in overrides.items():
        ns[k] = v
        monkeypatch.setattr(ov, k, v)
    got = {}
    for label, fn in (("orig", ns[NAME]), ("new", getattr(ov, NAME))):
        data = copy.deepcopy(rows)
        pulled = []

        def gen():
            for r in data:
                pulled.append(1)
                yield r  # one-shot iterator: not a list
        try:
            got[label] = ("ok", repr(fn(gen())), len(pulled))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert data == rows, f"{label} mutated input rows"
    assert got["orig"] == got["new"], got
    return eval(got["new"][1]) if got["new"][0] == "ok" else got["new"]


def test_empty_and_skipped_rows(orig_node, monkeypatch, guards):
    assert check(orig_node, monkeypatch, []) == []
    assert check(orig_node, monkeypatch, [{"stage": "x"}, {"run_id": "  "}, ev("", "a", "b")]) == []


FULL_RUN = [
    ev("r1", "strategist_llm", "result", {"intent_action": "buy", "intent_reason": "momentum"}, 100),
    ev("r1", "strategist", "policy_resolution", {"policy": "p"}, 101),
    ev("r1", "decision", "trace", {
        "decision_packet": {"intent": {"action": "buy", "symbol": "005930", "qty": "3", "reason": "why"},
                            "why": {"technical": {"rsi": 55}, "news": {"symbol_sentiment_status": "BAD", "global_sentiment_status": "ok"},
                                    "policy": {"p": 1}}, "invalidation": {"k": 1}},
        "trace": {"llm_context": {"technical": {"x": 1}}}}, 102),
    ev("r1", "decision_trace", "strategic_frame", {"payload": {"key_events": ["e1"]}}, 103),
    ev("r1", "scanner", "candidate_selection_reason", {"a": 1}, 104),
    ev("r1", "scanner", "selection_output", {"b": 2}, 105),
    ev("r1", "monitor", "entry_decision_detail", {"no_trade_surface": {"dominant_blocker": "spread", "decision_outcome": "wait",
                                                                      "near_ready_flag": 1, "distance_to_ready": {"spread": 0.1},
                                                                      "no_trade_reason_summary": "blocked by spread"},
                                                  "scanner_monitor_handoff": {"scanner_selected_symbol": "000660"}}, 106),
    ev("r1", "commander_router", "route", {"m": 1, "route_observability": {"obs": 2}}, 107),
    ev("r1", "execute_from_packet", "verdict", {"allowed": True}, 108),
    ev("r1", "execute_from_packet", "execution", {"order": {"action": "buy", "symbol": "005930", "qty": 3}, "payload": {"broker_code": "0"}}, 109),
    ev("r1", "commander_router", "intervention", {"type": "pause"}, 110),
    ev("r1", "commander_router", "intervention", {}, 111),
    ev("r1", "commander_router", "transition", {"transition": "COOLDOWN"}, 112),
    ev("r1", "anything", "error", {}, 113),
]


def test_full_event_stream(orig_node, monkeypatch, guards):
    out = check(orig_node, monkeypatch, FULL_RUN)
    assert len(out) == 1
    ctx = out[0]
    assert ctx["first_epoch"] == 100 and ctx["last_epoch"] == 113
    assert ctx["operator_intervention"] == ["pause", "operator_intervention"]
    assert ctx["risk_flags"] == ["cooldown_transition", "error:anything", "symbol_sentiment_bad"]
    assert (ctx["execution_status"], ctx["action"], ctx["symbol"]) == ("EXECUTED_OK", "BUY", "005930")
    assert ctx["final_outcome"] == "order accepted"


def test_out_of_order_duplicates_and_story_sort(orig_node, monkeypatch, guards):
    rows = [ev("late", "decision", "trace", {"decision_packet": {"intent": {"action": "sell", "symbol": "a", "qty": 1}}}, 500),
            ev("early", "decision", "trace", {"decision_packet": {"intent": {"action": "hold"}}}, 50),
            ev("late", "strategist_llm", "result", {"intent_action": "buy"}, 20),
            ev("dup", "execute_from_packet", "verdict", {"allowed": False, "reason": "risk_limit"}, 70),
            ev("dup", "execute_from_packet", "verdict", {"allowed": False}, 60),
            ev("early", "execute_from_packet", "execution", {"order": {"action": "sell", "symbol": "z", "qty": "2"},
                                                             "payload": {"broker_code": "-1"}}, 55),
            ev("noop", "strategist_llm", "result", {"intent_action": "noop"}, 0)]
    out = check(orig_node, monkeypatch, rows)
    assert [c["first_epoch"] for c in out] == sorted(c["first_epoch"] for c in out)
    statuses = {c["run_id"] if "run_id" in c else i: c["execution_status"] for i, c in enumerate(out)}
    assert "BLOCKED" in statuses.values() and "NOOP" in statuses.values()


@pytest.mark.parametrize("code", [None, "0", 0, "1", "-1", "weird", ""])
def test_broker_success_and_failure_codes(orig_node, monkeypatch, guards, code):
    rows = [ev("b", "execute_from_packet", "execution", {"order": {"action": "buy", "symbol": "s", "qty": 1},
                                                         "payload": {"broker_code": code}}, 1)]
    out = check(orig_node, monkeypatch, rows)
    assert out[0]["execution_status"] in {"EXECUTED_OK", "EXECUTED_FAIL", "EXECUTED"}


def test_guard_and_no_trade_surface_branches(orig_node, monkeypatch, guards):
    rows = [ev("g", "execute_from_packet", "verdict", {"allowed": False, "reason": "NO_CANDIDATE"}, 5),
            ev("n", "monitor", "entry_decision_detail", {"no_trade_surface": {"no_trade_reason_code": "NO_CANDIDATE"}}, 6),
            ev("c", "decision_trace", "candidate_selection", {"payload": {"selected_symbol": "x", "selected_candidate": {"why": "w", "score_total": 1},
                                                              "score_breakdown_summary": {"a": 1}, "playbook": "p"}}, 7),
            ev("e", "decision_trace", "entry_exit_decision", {"payload": {"selected_symbol": "y", "exit_reason": "tp", "thresholds": {"t": 1},
                                                              "min_hold_blocked": True, "sell_cooldown_blocked": True}}, 8),
            ev("m", "decision_trace", "bogus", {}, 9)]
    out = check(orig_node, monkeypatch, rows)
    flags = [f for c in out for f in c["risk_flags"]]
    assert "guard_block" in flags and "min_hold_blocked" in flags and "sell_cooldown_blocked" in flags


def test_use_time_helper_monkeypatch(orig_node, monkeypatch, guards):
    calls = []

    def fake_humanize(value):
        calls.append(value)
        return f"H[{value}]"

    out = check(orig_node, monkeypatch, [ev("h", "execute_from_packet", "verdict", {"allowed": False, "reason": "r"}, 1)],
                overrides={"_humanize_reason": fake_humanize,
                           "_normalize_reason_code": lambda raw, **kw: f"N[{raw}]"})
    assert out[0]["key_reason_raw"] == "N[unspecified]" and out[0]["key_reason"] == "H[N[unspecified]]"
    assert out[0]["guard_reason_human"] == "H[r]" and "r" in calls and "N[unspecified]" in calls


def test_wrapper_thin_and_owner_holds_body():
    wrapper = ast.parse(inspect.getsource(getattr(ov, NAME))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp))]
    fn = getattr(owner, NAME)
    assert len(inspect.getsource(fn).splitlines()) >= 300 and fn.__module__ == owner.__name__
    assert "operator_visibility import" not in inspect.getsource(owner).replace("operator_visibility_build", "")
