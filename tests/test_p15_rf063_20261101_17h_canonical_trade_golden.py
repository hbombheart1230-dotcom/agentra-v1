import ast
import subprocess
import types
from pathlib import Path
from typing import Any, Dict, List, Optional

import pytest

from scripts.diagnostics import check_trade_report_runtime_regression as runtime


_SHA = "42bcb938c869e95f72c6ac69bed57eff88b6a1dd"
_PATH = "scripts/diagnostics/check_trade_report_runtime_regression.py"
_NAMES = ("entry_json", "hold_json", "exit_json", "lifecycle_bundle_json", "ai_trade_report_input_json", "ai_trade_report_json", "ai_trade_report_md")


def _golden():
    assert subprocess.check_output(["git", "rev-parse", f"{_SHA}:{_PATH}"], text=True).strip() == "dc882aa56b5a23d9716cc8d3ec009480275cfe4d"
    raw = subprocess.check_output(["git", "show", f"{_SHA}:{_PATH}"], text=True)
    wanted = {"_safe_int", "_is_closed_trade", "_is_empty_placeholder", "_has_substantive_entry_evidence", "_has_substantive_exit_evidence", "_section_provenance_all_fallback", "_parse_case", "_normalize_cases", "validate_trade_artifact_chain"}
    nodes = [n for n in ast.parse(raw).body if isinstance(n, ast.FunctionDef) and n.name in wanted]
    module = types.ModuleType("canonical_trade_golden")
    module.__dict__.update({"Any": Any, "Dict": Dict, "List": List, "Optional": Optional, "Path": Path, "DEFAULT_GOLDEN_CASES": runtime.DEFAULT_GOLDEN_CASES})
    exec(compile(ast.fix_missing_locations(ast.Module(body=nodes, type_ignores=[])), "canonical_trade_golden", "exec"), module.__dict__)
    return module


def _ctx(root: Path, *, touched=False, status="closed", malformed=False):
    paths = {name: root / name for name in _NAMES}
    if touched:
        for path in paths.values(): path.write_text("x")
    rank = "NaN" if malformed else 1
    return {"trade_paths":paths, "entry_payload":{"run_id":"run-buy","ts":"2026-04-16T00:07:45+00:00","action":"BUY","symbol":"000660","qty":1,"reason_human":"selected"}, "exit_payload":{} if status == "open" else {"run_id":"run-sell","ts":"2026-04-16T00:08:47+00:00","action":"SELL","symbol":"000660","reason_human":"peak"}, "hold_payload":{"hold_duration":"1.0m","hold_duration_sec":62}, "lifecycle_bundle":{"trade_lifecycle_status":status,"linked_run_ids":["run-buy","run-sell"],"lifecycle_completeness":"partial","same_day_reporter_linkage":{"status":"missing","reporter_analysis_json_path":"","reporter_analysis_md_path":""}}, "story_input":{"symbol":"000660","selected_symbol":"000660","selected_rank":rank,"candidate_count":0 if malformed else 5,"status":"closed","action":"SELL","scanner_selection_trace":{"selected_rank":0,"candidate_count":0}}, "report":{"generation":{"status":"ok"},"section_provenance":{"market_context_at_entry":{"source":"canonical"}}}, "provenance":{"lifecycle_status":status}, "health":{}}


@pytest.mark.parametrize("touched,status,malformed", [(False,"closed",False), (True,"closed",False), (True,"open",False), (True,"closed",True)])
def test_canonical_full_result_matches_b_facade(monkeypatch, tmp_path, touched, status, malformed):
    golden = _golden(); context = _ctx(tmp_path, touched=touched, status=status, malformed=malformed)
    monkeypatch.setattr(golden, "_resolve_trade_context", lambda *_: context, raising=False)
    monkeypatch.setattr(runtime, "_resolve_trade_context", lambda *_: context)
    monkeypatch.setattr(runtime, "_run_python_json", lambda *_a, **_k: pytest.fail("runtime subprocess called"))
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_k: pytest.fail("subprocess.run called"))
    expected = golden.validate_trade_artifact_chain(tmp_path, "2026-04-16", "t")
    actual = runtime.validate_trade_artifact_chain(tmp_path, "2026-04-16", "t")
    assert actual == expected
    if not touched: assert actual["failures"][:7] == [f"missing_artifact:{name}" for name in _NAMES]
    if status == "open": assert actual["failures"] == ["story_input_status_conflicts_with_authoritative_status", "story_input_action_conflicts_with_open_trade"]
    if malformed: assert actual["failures"][-2:] == ["closed_trade_selected_rank_zero", "closed_trade_candidate_count_zero"]
