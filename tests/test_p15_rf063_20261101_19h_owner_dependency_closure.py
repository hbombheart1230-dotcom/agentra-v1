import ast
import importlib
import subprocess
from pathlib import Path

from scripts.diagnostics import check_trade_report_runtime_regression as runtime


_OWNER_MODULES = {
    "trade_artifact_validation_read_projection",
    "trade_artifact_context_projection",
    "trade_artifact_validation_evidence_projection",
    "trade_artifact_validation_cli",
    "trade_artifact_evidence_predicates",
    "trade_artifact_case_projection",
    "trade_artifact_command_text",
    "trade_artifact_command_projection",
}


def test_facade_static_owner_closure_imports_without_effects(monkeypatch):
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("subprocess invoked during import")))
    source = Path(runtime.__file__).read_text(encoding="utf-8")
    tree = ast.parse(source)
    direct = {
        alias.name.rsplit(".", 1)[-1]
        for node in tree.body if isinstance(node, ast.ImportFrom) and node.module == "scripts.diagnostics"
        for alias in node.names
    }
    lazy = {
        alias.name.rsplit(".", 1)[-1]
        for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module == "scripts.diagnostics"
        for alias in node.names
    }
    assert direct == {
        "trade_artifact_command_projection", "trade_artifact_validation_read_projection",
        "trade_artifact_context_projection", "trade_artifact_validation_evidence_projection",
        "trade_artifact_validation_cli",
    }
    assert lazy == _OWNER_MODULES
    for module in sorted(_OWNER_MODULES):
        assert importlib.import_module(f"scripts.diagnostics.{module}")


def test_validation_closure_smoke_uses_fake_context_without_subprocess(monkeypatch, tmp_path):
    keys = ("entry_json", "hold_json", "exit_json", "lifecycle_bundle_json", "ai_trade_report_input_json", "ai_trade_report_json", "ai_trade_report_md", "trade_provenance_json", "trade_health_json")
    paths = {key: tmp_path / key for key in keys}
    context = {
        "trade_paths": paths, "entry_payload": {}, "exit_payload": {}, "hold_payload": {},
        "lifecycle_bundle": {}, "story_input": {}, "report": {}, "provenance": {}, "health": {},
    }
    monkeypatch.setattr(runtime, "_resolve_trade_context", lambda *_: context)
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("subprocess invoked")))
    result = runtime.validate_trade_artifact_chain(tmp_path, "2026-04-16", "TRD_X")
    assert result["ok"] is False
    assert "missing_artifact:entry_json" in result["failures"]
