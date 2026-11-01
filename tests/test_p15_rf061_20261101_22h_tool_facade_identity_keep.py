"""RF-061 A22-1: ToolFacade three-owner identity + pure policy/DTO helpers, fake-only.

No ToolFacade construction, no CLI main, no order/approval/Step5C/supervisor call.
"""
from __future__ import annotations

import copy
import importlib
import subprocess

import pytest

PINS = {
    "libs/tools/__init__.py": "6fd24c349bb8780c9cb80c91983e4fef3b252eb1",
    "libs/tools/tool_facade.py": "7eaebf76311197000ea4cdb388a2543be0dfbce6",
    "libs/tools/tool_schema.py": "7facdcb0da8156ac39956d7755f516e3e8088721",
    "scripts/approval_cli.py": "c2f0af420300fe3614c6b1d21a068d8553c807fa",
}

tools = importlib.import_module("libs.tools")
live = importlib.import_module("libs.tools.tool_facade")
legacy = importlib.import_module("libs.tools.tool_schema")
cli = importlib.import_module("scripts.approval_cli")


@pytest.mark.parametrize("path", sorted(PINS))
def test_i0_source_blob_pins(path):
    out = subprocess.run(["git", "hash-object", path], check=True, capture_output=True, text=True).stdout.strip()
    assert out == PINS[path]


def test_i1_public_identity():
    assert tools.ToolFacade is live.ToolFacade
    assert cli.ToolFacade is live.ToolFacade
    assert legacy.ToolFacade is not live.ToolFacade


@pytest.fixture
def clean_env(monkeypatch):
    for k in ("APPROVAL_MODE", "AUTO_APPROVE", "EXECUTION_ENABLED", "KIWOOM_MODE"):
        monkeypatch.delenv(k, raising=False)
    return monkeypatch


def test_i2_policy_helpers(clean_env):
    mp = clean_env
    assert live._approval_mode() == "manual"
    assert live._execution_enabled() is False
    assert live._mode() == "real"
    mp.setenv("APPROVAL_MODE", "auto")
    assert live._approval_mode() == "auto"
    mp.setenv("APPROVAL_MODE", "manual")
    mp.setenv("AUTO_APPROVE", "true")
    assert live._approval_mode() == "manual"  # APPROVAL_MODE wins
    mp.delenv("APPROVAL_MODE")
    assert live._approval_mode() == "auto"  # legacy boolean
    mp.setenv("AUTO_APPROVE", "manual")
    assert live._approval_mode() == "manual"
    mp.setenv("AUTO_APPROVE", "false")
    assert live._approval_mode() == "manual"
    mp.setenv("EXECUTION_ENABLED", " On ")
    assert live._execution_enabled() is True
    mp.setenv("EXECUTION_ENABLED", "no")
    assert live._execution_enabled() is False
    mp.setenv("KIWOOM_MODE", " MOCK ")
    assert live._mode() == "mock"


def test_i3_unwrap_and_summarize_pure():
    raw = {"intent_id": "i1", "action": "BUY"}
    wrapped = {"ts": 1, "intent_id": "i1", "intent": raw}
    assert live._unwrap_intent(raw) is raw
    assert live._unwrap_intent(wrapped) is raw
    assert live._unwrap_intent("x") is None
    assert live._unwrap_intent(None) is None

    intent = {"intent_id": "i1", "action": "BUY", "symbol": "005930", "qty": 3,
              "order_type": "limit", "price": 70000, "created_epoch": 9, "extra": "dropped"}
    snap = copy.deepcopy(intent)
    facade = live.ToolFacade.__new__(live.ToolFacade)
    out = live.ToolFacade._summarize_intent(facade, intent)
    assert out == {"intent_id": "i1", "action": "BUY", "symbol": "005930", "qty": 3,
                   "order_type": "limit", "price": 70000, "rationale": "", "created_epoch": 9}
    assert intent == snap
    assert live.ToolFacade._summarize_intent(facade, {"intent": snap})["intent_id"] == "i1"
    assert live.ToolFacade._summarize_intent(facade, "bad")["intent_id"] is None
