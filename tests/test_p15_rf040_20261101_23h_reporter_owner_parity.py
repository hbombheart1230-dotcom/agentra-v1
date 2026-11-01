"""RF-040 A23-1: run_reporter_agent original preimage (ad718992) vs thin wrapper + single Owner.

The pinned original function is extracted by AST from ``git show`` and compiled in an isolated
namespace. Read model / separated report are pure stubs; subprocess, sockets and file writes are
guarded. Nothing is registered in ``sys.modules``.
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
from typing import Any, Dict, Optional

import pytest

PRE = "ad7189929a0a9291a100e38ca58b230562f77371"
PRE_BLOB = "00a8d240af99c14b493b50b2e989cc2e605e9968"
reporter = importlib.import_module("libs.agent.reporter")
owner = importlib.import_module("libs.agent.reporter_run_reporter_agent")
rtm = importlib.import_module("libs.reporting.trade_read_model")
fnr = importlib.import_module("libs.reporting.fact_narrative_report")


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def original_fn():
    try:
        raw = subprocess.run(["git", "show", f"{PRE}:libs/agent/reporter.py"], check=True,
                             capture_output=True).stdout
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(raw) == PRE_BLOB, "BLOCKED_PIN original blob"
    tree = ast.parse(raw.decode("utf-8"))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "run_reporter_agent")
    mod = ast.Module(body=[node], type_ignores=[])
    ns = {"Path": Path, "Optional": Optional, "Dict": Dict, "Any": Any,
          "_normalize_trade_reporter_policy": reporter._normalize_trade_reporter_policy,
          "_validate_trade_read_model": reporter._validate_trade_read_model}
    exec(compile(ast.fix_missing_locations(mod), f"<{PRE[:8]}:libs/agent/reporter.py>", "exec"), ns)
    return ns["run_reporter_agent"]


@pytest.fixture
def stubs(monkeypatch):
    st = {"model": None, "raises": None, "builds": [], "reports": [], "narrative": {"status": "dry_run"}}

    def build_trade_read_model(trade_dir):
        st["builds"].append(trade_dir)
        if st["raises"]:
            raise st["raises"]
        return copy.deepcopy(st["model"])

    def build_separated_report(*, trade_model, model=None, execution_profile=None):
        st["reports"].append({"trade_model": copy.deepcopy(trade_model), "model": model,
                              "execution_profile": execution_profile})
        return {"narrative": copy.deepcopy(st["narrative"])}

    def boom(*a, **k):
        raise AssertionError("effect attempted")

    monkeypatch.setattr(rtm, "build_trade_read_model", build_trade_read_model)
    monkeypatch.setattr(fnr, "build_separated_report", build_separated_report)
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(Path, "mkdir", boom)
    monkeypatch.setattr(Path, "write_text", boom)
    return st


def _compare(original_fn, st, policy=None):
    pol = copy.deepcopy(policy)
    a = original_fn("/tmp/fixture-trade", pol)
    a_state = (copy.deepcopy(st["builds"]), copy.deepcopy(st["reports"]))
    st["builds"].clear()
    st["reports"].clear()
    b = reporter.run_reporter_agent("/tmp/fixture-trade", pol)
    assert pol == policy
    assert a == b
    assert list(a) == list(b)  # key insertion order
    assert (st["builds"], st["reports"]) == a_state
    return b


GOOD = {"trade_id": "t1", "symbol": "005930", "facts": {"trade_id": "t1", "symbol": "005930"},
        "provenance": {"src": "x"}, "context": {"c": 1}}


def test_c1_read_model_exception_degraded(original_fn, stubs):
    stubs["raises"] = ValueError("fixture")
    out = _compare(original_fn, stubs)
    assert out["status"] == "degraded"
    assert out["narrative"]["reason"] == "trade_read_model_exception" and out["narrative"]["error"] == "fixture"
    assert stubs["reports"] == []


@pytest.mark.parametrize("model,reason", [
    ({}, "trade_read_model_missing"),
    ({"trade_id": "t"}, "trade_read_model_facts_missing"),
    ({"facts": {"a": 1}}, "trade_read_model_provenance_missing"),
])
def test_c2_invalid_read_model_skipped_no_report_call(original_fn, stubs, model, reason):
    stubs["model"] = model
    out = _compare(original_fn, stubs)
    assert out["status"] == "degraded" and out["narrative"]["status"] == "skipped"
    assert out["narrative"]["reason"] == reason and out["narrative"]["llm_call_skipped"] is True
    assert stubs["reports"] == []


def test_c3_ok_dry_run_forwarding(original_fn, stubs):
    stubs["model"] = GOOD
    stubs["narrative"] = {"status": "dry_run", "text": "n"}
    out = _compare(original_fn, stubs, policy={"model": "m1", "execution_profile": {"p": 1}})
    assert out["status"] == "ok"
    assert out["metadata"] == {"trade_id": "t1", "symbol": "005930", "trade_dir": "/tmp/fixture-trade",
                               "generated_by": "reporter_agent_v1"}
    assert len(stubs["reports"]) == 1
    assert stubs["reports"][0]["model"] == "m1" and stubs["reports"][0]["execution_profile"] == {"p": 1}


def test_c4_invalid_narrative_status_degraded(original_fn, stubs):
    stubs["model"] = GOOD
    stubs["narrative"] = {"status": "weird"}
    assert _compare(original_fn, stubs)["status"] == "degraded"


def test_c5_use_time_facade_seam(stubs, monkeypatch):
    stubs["model"] = GOOD
    seen = []
    monkeypatch.setattr(reporter, "_normalize_trade_reporter_policy",
                        lambda policy: seen.append(("n", policy)) or {"model": "FM", "execution_profile": "FP"})
    monkeypatch.setattr(reporter, "_validate_trade_read_model",
                        lambda m: seen.append(("v", None)) or {"ok": False, "reason": "seam"})
    out = reporter.run_reporter_agent("/tmp/fixture-trade", {"k": 1})
    assert seen == [("n", {"k": 1}), ("v", None)]
    assert out["narrative"]["reason"] == "seam" and stubs["reports"] == []


def test_c6_single_owner_and_thin_wrapper():
    wrapper = ast.parse(inspect.getsource(reporter.run_reporter_agent)).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.Try, ast.Dict))]
    own = inspect.getsource(owner)
    assert "import libs.agent.reporter" not in own and "from libs.agent.reporter import" not in own
    assert owner.run_reporter_agent.__module__ == "libs.agent.reporter_run_reporter_agent"
