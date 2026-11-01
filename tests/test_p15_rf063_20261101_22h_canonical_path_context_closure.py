import copy
import subprocess
import types
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Dict

from scripts.diagnostics import check_trade_report_runtime_regression as runtime


_SHA = "48d7622dd24a94735bdaf75f69adf47a959fac84"
_PATH = "libs/reporting/llm_artifacts_trade_path_projection.py"
_CANONICAL_LLM_BLOB = "27aea755e3ab9a3143affbd28294e4c8c775b8ca"
_PATH_BLOB = "cf17542917ac15c34dba2e6bd9f3694cc97a13f7"
_FACADE_BLOB = "c7113fcf6e7c3313943e484fa939c48062672141"
_CONTEXT_BLOB = "433de050fa01885bf7315380a6efa5070d741ccf"
_READ_ORDER = ("entry_json", "exit_json", "hold_json", "lifecycle_bundle_json", "ai_trade_report_input_json", "ai_trade_report_json", "trade_provenance_json", "trade_health_json")


def _canonical_owner():
    assert subprocess.check_output(["git", "rev-parse", f"{_SHA}:libs/reporting/llm_artifacts.py"], text=True).strip() == _CANONICAL_LLM_BLOB
    assert subprocess.check_output(["git", "rev-parse", f"{_SHA}:{_PATH}"], text=True).strip() == _PATH_BLOB
    assert subprocess.check_output(["git", "rev-parse", "HEAD:scripts/diagnostics/check_trade_report_runtime_regression.py"], text=True).strip() == _FACADE_BLOB
    assert subprocess.check_output(["git", "rev-parse", "HEAD:scripts/diagnostics/trade_artifact_context_projection.py"], text=True).strip() == _CONTEXT_BLOB
    raw = subprocess.check_output(["git", "show", f"{_SHA}:{_PATH}"], text=True)
    module = types.ModuleType("canonical_trade_path_projection")
    module.__dict__.update({"Any": Any, "Dict": Dict, "Path": Path})
    exec(compile(raw, "canonical_trade_path_projection", "exec"), module.__dict__)
    return module


def _path_facade():
    return SimpleNamespace(
        canonical_trade_day_root=lambda root, day: Path(root) / "trades" / day,
        resolve_trade_day_root=lambda root, day: Path(root) / "trades" / day,
        find_trade_dir=lambda _root, _trade_id: None,
    )


def _resolve(monkeypatch, tmp_path, payloads):
    owner = _canonical_owner()
    paths = owner.trade_artifact_paths(tmp_path, "2026-04-16", "TRD_X", facade=_path_facade())
    fixture = {path: copy.deepcopy(payloads.get(key, {})) for key, path in paths.items()}
    original_fixture = copy.deepcopy(fixture)
    calls = []
    monkeypatch.setattr(runtime, "trade_artifact_paths", lambda root, day, trade: owner.trade_artifact_paths(root, day, trade, facade=_path_facade()))
    monkeypatch.setattr(runtime, "_read_json", lambda path: calls.append(path) or copy.deepcopy(fixture[path]))
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("subprocess invoked")))
    monkeypatch.setattr(subprocess, "Popen", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("Popen invoked")))
    monkeypatch.setattr(Path, "mkdir", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("mkdir invoked")))
    monkeypatch.setattr(Path, "write_text", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("write invoked")))
    actual = runtime._resolve_trade_context(tmp_path, "2026-04-16", "TRD_X")
    assert fixture == original_fixture
    assert calls == [paths[key] for key in _READ_ORDER]
    assert actual["trade_paths"] == paths
    return actual, paths


def test_c1_empty_root_uses_canonical_paths_and_eight_reads(monkeypatch, tmp_path):
    actual, paths = _resolve(monkeypatch, tmp_path, {})
    assert actual["trade_paths"]["trade_root"] == tmp_path / "trades" / "2026-04-16" / "TRD_X"
    assert actual["entry_run_id"] == actual["exit_run_id"] == actual["target_run_id"] == ""
    assert not list(tmp_path.iterdir())
    assert paths["entry_json"].name == "entry.json"


def test_c2_populated_payloads_match_canonical_projected_paths(monkeypatch, tmp_path):
    payloads = {
        "entry_json": {"run_id": "ENTRY1"}, "exit_json": {"run_id": "EXIT1"},
        "lifecycle_bundle_json": {"run_id": "LIFECYCLE"}, "trade_provenance_json": {"source": "fixture"},
        "trade_health_json": {"ok": True},
    }
    actual, _ = _resolve(monkeypatch, tmp_path, payloads)
    assert actual["entry_payload"] == {"run_id": "ENTRY1"}
    assert actual["exit_payload"] == {"run_id": "EXIT1"}
    assert actual["target_run_id"] == "EXIT1"
    assert actual["provenance"] == {"source": "fixture"}


def test_c3_entry_fallback_has_no_effect_or_mutation(monkeypatch, tmp_path):
    actual, _ = _resolve(monkeypatch, tmp_path, {"entry_json": {"run_id": "ENTRY1"}, "exit_json": {}})
    assert actual["entry_run_id"] == "ENTRY1"
    assert actual["exit_run_id"] == ""
    assert actual["target_run_id"] == "ENTRY1"
