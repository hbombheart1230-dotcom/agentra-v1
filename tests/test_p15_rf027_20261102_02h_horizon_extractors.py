"""RF-027 A26-1..5: original (b2e48863 preimage, blob 8336d03f) vs thin wrappers + 5 Owners.

The five original functions are AST-extracted from ``git show`` and compiled in a copy of the live module namespace
(so helper bindings are identical); dependency overrides are applied to both sides. Socket/subprocess/Path writes guarded.
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

PRE = "b2e48863ae8a44d7ab41090160816d504052f2e0"
PATH = "libs/runtime/strategy_horizon_feedback.py"
PRE_BLOB = "8336d03f41ea7157b6ab207f3829215464078a9a"
NAMES = ["_epoch_seconds", "extract_commander_horizon_policy", "extract_commander_horizon_policy_from_state",
         "extract_strategy_horizon_feedback", "extract_strategy_horizon_feedback_from_state"]
sfb = importlib.import_module("libs.runtime.strategy_horizon_feedback")
OWNERS = {n: importlib.import_module(f"libs.runtime.strategy_horizon_feedback_{n.lstrip('_')}") for n in NAMES}


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    try:
        raw = subprocess.run(["git", "show", f"{PRE}:{PATH}"], check=True, capture_output=True).stdout
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(raw) == PRE_BLOB, "BLOCKED_PIN original blob"
    tree = ast.parse(raw.decode("utf-8"))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in NAMES]
    assert sorted(n.name for n in nodes) == sorted(NAMES)
    return nodes


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(Path, "mkdir", boom)
    monkeypatch.setattr(Path, "write_text", boom)


def check(orig_nodes, monkeypatch, name, *args, overrides=None):
    overrides = overrides or {}
    ns = dict(vars(sfb))
    mod = ast.Module(body=copy.deepcopy(orig_nodes), type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), f"<{PRE[:8]}:{PATH}>", "exec"), ns)
    for k, v in overrides.items():
        if k != name:
            ns[k] = v
        monkeypatch.setattr(sfb, k, v)
    got = {}
    for label, fn in (("orig", ns[name]), ("new", getattr(sfb, name))):
        a = copy.deepcopy(args)
        try:
            got[label] = ("ok", repr(fn(*a)))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert a == args, f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return eval(got["new"][1]) if got["new"][0] == "ok" else got["new"]


# ---- A26-1 _epoch_seconds ----
@pytest.mark.parametrize("value", [None, "", "  ", 0, 1700000000, 1700000000.5, 10_000_000_001, 20_000_000_000_000,
                                   "1700000000", "1700000000123", "20260416093000", "2026041609300",
                                   "2026-04-16T09:30:00Z", "2026-04-16T09:30:00+09:00", "2026-04-16T09:30:00",
                                   "not-a-date", "20269999999999", object.__name__])
def test_epoch_seconds(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_epoch_seconds", value)


def test_epoch_seconds_values(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_epoch_seconds", 10_000_000_001) == 10_000_000.001
    assert check(orig_nodes, monkeypatch, "_epoch_seconds", "20260416093000") == check(
        orig_nodes, monkeypatch, "_epoch_seconds", "2026-04-16T09:30:00Z")
    assert check(orig_nodes, monkeypatch, "_epoch_seconds", "bad") is None


# ---- A26-2 extract_commander_horizon_policy ----
CH = {"owner": "commander", "strategy_horizon": "intraday"}
CS = {"schema_version": "commander_horizon_policy.v1", "x": 1}
SURFACES = [
    None, {}, "bad", {"commander_horizon_policy": CH}, {"horizon_policy": CS},
    {"horizon_policy": {"owner": "other"}},
    {"applied_policy": {"horizon": CH}}, {"applied_policy": {"commander_horizon_policy": CS}},
    {"strategy_policy": {"commander_horizon_policy": CH}},
    {"monitor_policy": {"applied_policy": {"horizon": CS}}},
    {"commander_context": {"strategy_policy": {"horizon_policy": CH}}},
    {"commander_context_ref": {"commander_horizon_policy": CS}},
    {"strategy_policy": {"x": 1}, "monitor_policy": {"horizon_policy": CH}, "commander_context": {"commander_horizon_policy": CS}},
    {"commander_horizon_policy": [1], "applied_policy": 5, "strategy_policy": "s"},
]


@pytest.mark.parametrize("surface", SURFACES)
def test_extract_commander_horizon_policy(orig_nodes, monkeypatch, guards, surface):
    check(orig_nodes, monkeypatch, "extract_commander_horizon_policy", surface)


def test_extract_commander_priority_and_recursion_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "extract_commander_horizon_policy",
                {"strategy_policy": {"commander_horizon_policy": CH}, "monitor_policy": {"horizon_policy": CS}})
    assert out == CH
    seen = []
    # recursive calls go through the facade name at call time
    check(orig_nodes, monkeypatch, "extract_commander_horizon_policy_from_state", {"strategy_policy": {"a": 1}},
          overrides={"extract_commander_horizon_policy": lambda s: seen.append(s) or {}})
    assert seen, "facade extractor was not consulted"


# ---- A26-3 extract_commander_horizon_policy_from_state ----
@pytest.mark.parametrize("state", [
    None, {}, "bad", {"commander_horizon_policy": CH},
    *[{k: {"commander_horizon_policy": CH}} for k in
      ("commander_decision", "strategist_output", "strategy_policy", "entry_strategy_context", "monitor_policy", "applied_policy")],
    {"commander_decision": {"horizon_policy": CS}, "applied_policy": {"commander_horizon_policy": CH}},
    {"strategist_output": "bad"},
])
def test_extract_commander_horizon_policy_from_state(orig_nodes, monkeypatch, guards, state):
    check(orig_nodes, monkeypatch, "extract_commander_horizon_policy_from_state", state)


def test_from_state_patched_extractor(orig_nodes, monkeypatch, guards):
    calls = []

    def fake(surface):
        calls.append(sorted(surface) if isinstance(surface, dict) else surface)
        return {"fake": True} if surface.get("applied_policy") is not None else {}

    out = check(orig_nodes, monkeypatch, "extract_commander_horizon_policy_from_state",
                {"commander_decision": {"a": 1}, "applied_policy": {"applied_policy": {}}},
                overrides={"extract_commander_horizon_policy": fake})
    assert out == {"fake": True}


# ---- A26-4 extract_strategy_horizon_feedback ----
FB = {"strategy_horizon": "intraday", "marker": 1}


@pytest.mark.parametrize("surface", [
    None, {}, "bad", {"strategy_horizon_feedback": FB},
    {"strategy_policy": {"monitor_policy": {"strategy_horizon_feedback": FB}}},
    {"monitor_policy": {"strategy_horizon_feedback": FB}},
    {"monitor_policy": {"x": 1}},
    {"strategy_horizon": "scalp"}, {"strategy_horizon": "swing_unknown", "playbook": "pb", "risk_tone": "hi"},
    {"strategy_horizon": "1_2day_swing", "expected_hold_window": {"min_sec": 1}, "exit_guidance": {"g": 1},
     "invalidation_conditions": ["x"], "monitor_handoff": {"h": 1}, "monitor_guidance": "mg", "trade_aggressiveness": "ta"},
    {"strategy_horizon": ""},
])
def test_extract_strategy_horizon_feedback(orig_nodes, monkeypatch, guards, surface):
    check(orig_nodes, monkeypatch, "extract_strategy_horizon_feedback", surface)


def test_strategy_feedback_builder_kwargs(orig_nodes, monkeypatch, guards):
    seen = []

    def fake_build(raw=None, **kw):
        seen.append((copy.deepcopy(raw), kw))
        return {"built": kw.get("source")}

    out = check(orig_nodes, monkeypatch, "extract_strategy_horizon_feedback",
                {"strategy_horizon": "scalp", "playbook": "p"}, overrides={"build_strategy_horizon_feedback": fake_build})
    assert out == {"built": "extracted_surface"} and seen[-1][1]["playbook"] == "p"


# ---- A26-5 extract_strategy_horizon_feedback_from_state ----
@pytest.mark.parametrize("state", [
    None, {}, "bad",
    {"strategist_output": {"strategy_horizon_feedback": FB}},
    {"strategist_output": {"x": 1}, "strategy_policy": {"strategy_horizon_feedback": FB}},
    {"entry_strategy_context": {"strategy_horizon_feedback": FB}},
    {"strategist_output": "bad", "playbook": "pb", "monitor_guidance": "mg", "trade_aggressiveness": "ta", "risk_tone": "rt"},
])
def test_extract_strategy_horizon_feedback_from_state(orig_nodes, monkeypatch, guards, state):
    check(orig_nodes, monkeypatch, "extract_strategy_horizon_feedback_from_state", state)


def test_from_state_default_builder_kwargs(orig_nodes, monkeypatch, guards):
    seen = []
    out = check(orig_nodes, monkeypatch, "extract_strategy_horizon_feedback_from_state",
                {"playbook": "pb"},
                overrides={"build_strategy_horizon_feedback": lambda raw=None, **kw: seen.append(kw) or {"src": kw["source"]}})
    assert out == {"src": "state_default"} and seen[-1]["playbook"] == "pb"


@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(sfb, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp))]
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(list(ast.walk(node))) > 20 and owner_fn.__module__ == OWNERS[name].__name__
    assert "import strategy_horizon_feedback " not in inspect.getsource(OWNERS[name]).replace("strategy_horizon_feedback_", "")
