import ast
import subprocess
import sys
import types
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from scripts.diagnostics import check_trade_report_runtime_regression as runtime


_SHA = "0e35a4a79133e0371aa43bca4c84942868c0bba5"
_PATH = "scripts/diagnostics/check_trade_report_runtime_regression.py"
_NAMES = {"_safe_int", "_is_closed_trade", "_is_empty_placeholder", "_has_substantive_entry_evidence", "_has_substantive_exit_evidence", "_section_provenance_all_fallback", "_command_to_text", "_build_bundle_repair_command", "_build_report_regen_command"}


def _golden():
    assert subprocess.check_output(["git", "rev-parse", f"{_SHA}:{_PATH}"], text=True).strip() == "dc882aa56b5a23d9716cc8d3ec009480275cfe4d"
    raw = subprocess.check_output(["git", "show", f"{_SHA}:{_PATH}"], text=True)
    nodes = [node for node in ast.parse(raw).body if isinstance(node, ast.FunctionDef) and node.name in _NAMES]
    module = types.ModuleType("canonical_predicate_command_golden")
    module.__dict__.update({"Any": Any, "Dict": Dict, "List": List, "Optional": Optional, "ROOT": runtime.ROOT, "sys": sys})
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])), "canonical_predicate_command_golden", "exec"), module.__dict__)
    return module


@pytest.mark.parametrize("value, default", [(None, 9), ("", 9), ("4.9", 0), ("bad", 7), (float("inf"), 8)])
def test_safe_int_canonical_matches_facade(value, default):
    golden = _golden()
    assert runtime._safe_int(value, default) == golden._safe_int(value, default)


@pytest.mark.parametrize("lifecycle, exit_payload", [({"status": "open"}, {"run_id": "x"}), ({"status": "closed"}, {}), ({"status": ""}, {}), ({}, {"run_id": "x"})])
def test_closed_trade_canonical_matches_facade(lifecycle, exit_payload):
    golden = _golden()
    assert runtime._is_closed_trade(lifecycle, exit_payload) == golden._is_closed_trade(lifecycle, exit_payload)


def test_closed_trade_honors_call_time_exit_evidence_monkeypatch(monkeypatch):
    golden = _golden()
    sentinel = lambda payload: bool(payload.get("sentinel"))
    monkeypatch.setattr(golden, "_has_substantive_exit_evidence", sentinel)
    monkeypatch.setattr(runtime, "_has_substantive_exit_evidence", sentinel)
    assert golden._is_closed_trade({}, {"sentinel": True}) is True
    assert runtime._is_closed_trade({}, {"sentinel": True}) is True


@pytest.mark.parametrize("value", [None, False, 0, {"nested": ["", 0, False]}, {"nested": "value"}])
def test_empty_placeholder_canonical_matches_facade(value):
    golden = _golden()
    assert runtime._is_empty_placeholder(value) == golden._is_empty_placeholder(value)


@pytest.mark.parametrize("entry, exit", [({"run_id": "entry"}, {}), ({"execution_context": {"order_id": "o"}}, {}), ({}, {"run_id": "exit"}), ({}, {"monitor_context": {"trigger_type": "take_profit"}})])
def test_evidence_predicates_canonical_match_facade(entry, exit):
    golden = _golden()
    assert runtime._has_substantive_entry_evidence(entry) == golden._has_substantive_entry_evidence(entry)
    assert runtime._has_substantive_exit_evidence(exit) == golden._has_substantive_exit_evidence(exit)


@pytest.mark.parametrize("report", [{"section_provenance": {"a": {"source": "fallback"}, "b": {"source": "missing"}}}, {"section_provenance": {"a": {"source": "fallback"}, "b": {"source": "canonical"}}}])
def test_section_provenance_canonical_matches_facade(report):
    golden = _golden()
    assert runtime._section_provenance_all_fallback(report) == golden._section_provenance_all_fallback(report)


def test_command_constructors_canonical_match_facade(monkeypatch, tmp_path):
    golden = _golden()
    monkeypatch.setattr(runtime, "ROOT", tmp_path)
    golden.ROOT = tmp_path
    bundle = dict(day="2026-04-16", target_run_id="run-x", role="test", max_runs=2, event_log_path="e", evidence_log_path="v", report_dir="r", reports_root="tmp")
    regen = dict(day="2026-04-16", trade_id="trade-x", reports_root="tmp")
    assert runtime._command_to_text(["python", "--x", 3]) == golden._command_to_text(["python", "--x", 3])
    assert runtime._build_bundle_repair_command(**bundle) == golden._build_bundle_repair_command(**bundle)
    for local_debug, with_llm, timeout in [(True, False, None), (False, True, 5)]:
        assert runtime._build_report_regen_command(**regen, local_debug=local_debug, with_llm=with_llm, hard_timeout_sec=timeout) == golden._build_report_regen_command(**regen, local_debug=local_debug, with_llm=with_llm, hard_timeout_sec=timeout)
