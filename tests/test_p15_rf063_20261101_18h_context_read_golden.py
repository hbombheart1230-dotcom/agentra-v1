import ast
import json
import subprocess
import types
from pathlib import Path
from typing import Any, Dict

import pytest

from scripts.diagnostics import check_trade_report_runtime_regression as runtime


_SHA = "0e35a4a79133e0371aa43bca4c84942868c0bba5"
_PATH = "scripts/diagnostics/check_trade_report_runtime_regression.py"
_KEYS = (
    "entry_json", "exit_json", "hold_json", "lifecycle_bundle_json",
    "ai_trade_report_input_json", "ai_trade_report_json", "trade_provenance_json", "trade_health_json",
)


def _golden():
    assert subprocess.check_output(["git", "rev-parse", f"{_SHA}:{_PATH}"], text=True).strip() == "dc882aa56b5a23d9716cc8d3ec009480275cfe4d"
    raw = subprocess.check_output(["git", "show", f"{_SHA}:{_PATH}"], text=True)
    nodes = [node for node in ast.parse(raw).body if isinstance(node, ast.FunctionDef) and node.name in {"_read_json", "_resolve_trade_context"}]
    module = types.ModuleType("canonical_context_read_golden")
    module.__dict__.update({"Any": Any, "Dict": Dict, "Path": Path, "json": json})
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])), "canonical_context_read_golden", "exec"), module.__dict__)
    return module


@pytest.mark.parametrize("contents, expected", [(None, {}), ('{"run_id": "r"}', {"run_id": "r"}), ("[]", {}), ("{broken", {})])
def test_read_json_canonical_matches_facade(tmp_path, contents, expected):
    golden = _golden()
    path = tmp_path / "payload.json"
    if contents is not None:
        path.write_text(contents, encoding="utf-8")
    assert golden._read_json(path) == expected
    assert runtime._read_json(path) == expected


@pytest.mark.parametrize(
    "payloads, expected_ids",
    [
        ({"entry_json": {"run_id": "entry"}, "exit_json": {"run_id": "exit"}}, ("entry", "exit", "exit")),
        ({"entry_json": {}, "exit_json": {}, "lifecycle_bundle_json": {"lifecycle": {"entry": {"run_id": "life-entry"}, "exit": {"run_id": "life-exit"}}}}, ("life-entry", "life-exit", "life-exit")),
        ({"entry_json": {}, "exit_json": {}, "lifecycle_bundle_json": {"run_id": "bundle"}}, ("", "bundle", "bundle")),
        ({}, ("", "", "")),
    ],
)
def test_context_canonical_matches_facade_and_reads_eight_paths(monkeypatch, tmp_path, payloads, expected_ids):
    golden = _golden()
    paths = {key: tmp_path / key for key in _KEYS}
    expected_payloads = {key: payloads.get(key, {}) for key in _KEYS}
    canonical_reads, facade_reads = [], []
    monkeypatch.setattr(golden, "trade_artifact_paths", lambda *_: paths, raising=False)
    monkeypatch.setattr(runtime, "trade_artifact_paths", lambda *_: paths)
    monkeypatch.setattr(golden, "_read_json", lambda path: canonical_reads.append(path) or expected_payloads[next(key for key, value in paths.items() if value == path)], raising=False)
    monkeypatch.setattr(runtime, "_read_json", lambda path: facade_reads.append(path) or expected_payloads[next(key for key, value in paths.items() if value == path)])
    expected = golden._resolve_trade_context(tmp_path, "2026-04-16", "trade")
    actual = runtime._resolve_trade_context(tmp_path, "2026-04-16", "trade")
    assert actual == expected
    assert (actual["entry_run_id"], actual["exit_run_id"], actual["target_run_id"]) == expected_ids
    assert canonical_reads == [paths[key] for key in _KEYS]
    assert facade_reads == [paths[key] for key in _KEYS]
