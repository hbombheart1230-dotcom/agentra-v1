import copy
import subprocess
import types
from pathlib import Path

import pytest

from scripts.diagnostics import check_trade_report_runtime_regression as runtime


_SHA = "66e0cf267090e9bde6b66fa8c70d977ed80a05f0"
_PATH = "scripts/diagnostics/check_trade_report_runtime_regression.py"
_SOURCE_BLOB = "dc882aa56b5a23d9716cc8d3ec009480275cfe4d"
_FACADE_BLOB = "c7113fcf6e7c3313943e484fa939c48062672141"
_OWNER_BLOB = "9fd7c104efc5b0497bdb7f9b0b6a4642386b3974"
_ARTIFACT_KEYS = ("entry_json", "hold_json", "exit_json", "lifecycle_bundle_json", "ai_trade_report_input_json", "ai_trade_report_json", "ai_trade_report_md")


def _original_probe():
    assert subprocess.check_output(["git", "rev-parse", f"{_SHA}:{_PATH}"], text=True).strip() == _SOURCE_BLOB
    assert subprocess.check_output(["git", "rev-parse", f"HEAD:{_PATH}"], text=True).strip() == _FACADE_BLOB
    assert subprocess.check_output(["git", "rev-parse", "HEAD:scripts/diagnostics/trade_artifact_validation_evidence_projection.py"], text=True).strip() == _OWNER_BLOB
    raw = subprocess.check_output(["git", "show", f"{_SHA}:{_PATH}"], text=True)
    module = types.ModuleType("scripts.diagnostics._canonical_trade_validation_probe")
    module.__package__ = "scripts.diagnostics"
    module.__file__ = _PATH
    exec(compile(raw, _PATH, "exec"), module.__dict__)
    return module


def _context(tmp_path, **overrides):
    ctx = {
        "trade_paths": {key: tmp_path / key for key in _ARTIFACT_KEYS},
        "entry_payload": {}, "exit_payload": {}, "hold_payload": {},
        "lifecycle_bundle": {}, "story_input": {}, "report": {}, "provenance": {}, "health": {},
    }
    ctx.update(overrides)
    return ctx


def _compare(monkeypatch, tmp_path, ctx):
    original = _original_probe()
    seed = copy.deepcopy(ctx)
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("subprocess invoked")))
    monkeypatch.setattr(subprocess, "Popen", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("Popen invoked")))
    monkeypatch.setattr(original, "_resolve_trade_context", lambda *_: copy.deepcopy(ctx))
    monkeypatch.setattr(runtime, "_resolve_trade_context", lambda *_: copy.deepcopy(ctx))
    expected = original.validate_trade_artifact_chain(tmp_path, "2026-04-16", "TRD_X")
    actual = runtime.validate_trade_artifact_chain(tmp_path, "2026-04-16", "TRD_X")
    assert ctx == seed
    assert actual == expected
    return actual


def test_v1_absent_artifacts_original_and_owner_match(monkeypatch, tmp_path):
    actual = _compare(monkeypatch, tmp_path, _context(tmp_path))
    assert actual["ok"] is False
    assert actual["failures"] == [f"missing_artifact:{key}" for key in _ARTIFACT_KEYS]


def test_v2_closed_partial_original_and_owner_match(monkeypatch, tmp_path):
    actual = _compare(monkeypatch, tmp_path, _context(
        tmp_path,
        provenance={"lifecycle_status": "closed"},
        lifecycle_bundle={"linked_run_ids": []},
        entry_payload={"scanner_context": {"selected_symbol": "TRD_X"}},
        exit_payload={"reason_human": "fixture exit"},
        hold_payload={"hold_duration_sec": 0},
        story_input={"selected_rank": 0, "candidate_count": 0},
        health={"lifecycle_completeness": "partial"},
    ))
    assert actual["closed_trade"] is True
    assert "closed_trade_missing_exit_run_id" in actual["failures"]
    assert "closed_trade_selected_rank_zero" in actual["failures"]


def test_v3_open_conflict_original_and_owner_match(monkeypatch, tmp_path):
    actual = _compare(monkeypatch, tmp_path, _context(
        tmp_path,
        provenance={"lifecycle_status": "open"},
        story_input={"status": "closed", "action": "SELL", "selected_symbol": "OTHER", "symbol": "TRD_X"},
    ))
    assert "story_input_status_conflicts_with_authoritative_status" in actual["failures"]
    assert "story_input_action_conflicts_with_open_trade" in actual["failures"]
