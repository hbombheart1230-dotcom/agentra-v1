import ast
import json
import subprocess
from pathlib import Path

from scripts.diagnostics import check_trade_report_runtime_regression as runtime


_SHA = "0e35a4a79133e0371aa43bca4c84942868c0bba5"
_PATH = "scripts/diagnostics/check_trade_report_runtime_regression.py"


def _function_ast(source, name):
    return next(node for node in ast.parse(source).body if isinstance(node, ast.FunctionDef) and node.name == name)


def test_pinned_canonical_parser_and_main_ast_match_b_facade():
    assert subprocess.check_output(["git", "rev-parse", f"{_SHA}:{_PATH}"], text=True).strip() == "dc882aa56b5a23d9716cc8d3ec009480275cfe4d"
    canonical = subprocess.check_output(["git", "show", f"{_SHA}:{_PATH}"], text=True)
    facade = Path(runtime.__file__).read_text(encoding="utf-8")
    for name in ("_build_parser", "main"):
        assert ast.dump(_function_ast(facade, name), include_attributes=False) == ast.dump(_function_ast(canonical, name), include_attributes=False)


def test_parser_accepts_fake_only_skip_case(tmp_path):
    args = runtime._build_parser().parse_args([
        "--reports-root", str(tmp_path), "--case", "2026-04-16:TRD_X:RUN_X",
        "--skip-repair", "--skip-local-debug", "--json",
    ])
    assert args.case == ["2026-04-16:TRD_X:RUN_X"]
    assert args.skip_repair is True and args.skip_local_debug is True and args.json is True
    assert args.llm_acceptance is False


def _run_fake_main(monkeypatch, tmp_path, validation):
    emitted = []
    monkeypatch.setattr(runtime, "_resolve_trade_context", lambda *_: {"target_run_id": "RUN_X"})
    monkeypatch.setattr(runtime, "validate_trade_artifact_chain", lambda *_: validation)
    monkeypatch.setattr(runtime, "_run_python_json", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("subprocess path invoked")))
    monkeypatch.setattr(runtime, "_emit_text", emitted.append)
    exit_code = runtime.main([
        "--reports-root", str(tmp_path), "--case", "2026-04-16:TRD_X:RUN_X",
        "--skip-repair", "--skip-local-debug", "--json",
    ])
    return exit_code, json.loads(emitted[-1])


def test_main_fake_only_success_has_all_effect_paths_skipped(monkeypatch, tmp_path):
    exit_code, payload = _run_fake_main(monkeypatch, tmp_path, {"ok": True, "failures": [], "warnings": []})
    assert exit_code == 0
    assert payload["case_count"] == 1 and payload["failed_case_count"] == 0
    row = payload["rows"][0]
    assert (row["requested_target_run_id"], row["resolved_target_run_id"]) == ("RUN_X", "RUN_X")
    assert row["repair"]["skipped"] is True and row["local_debug_regen"]["skipped"] is True and row["llm_acceptance"]["skipped"] is True


def test_main_fake_only_validation_failure_is_nonzero(monkeypatch, tmp_path):
    exit_code, payload = _run_fake_main(monkeypatch, tmp_path, {"ok": False, "failures": ["fixture_failure"], "warnings": []})
    assert exit_code == 1
    assert payload["failed_case_count"] == 1
    assert payload["rows"][0]["validation"]["failures"] == ["fixture_failure"]
