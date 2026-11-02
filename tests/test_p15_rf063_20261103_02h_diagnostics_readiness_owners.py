from __future__ import annotations

import ast
import inspect
import subprocess

from scripts.diagnostics import run_m29_disaster_recovery_drill as drill
from scripts.diagnostics import run_m31_mock_exam_readiness_check as readiness
from scripts.diagnostics import run_m31_slo_incident_review_check as slo
from scripts.diagnostics import run_m29_disaster_recovery_drill_replay_metrics as metrics_owner
from scripts.diagnostics import run_m29_disaster_recovery_drill_replay_parity_ok as parity_owner
from scripts.diagnostics import run_m29_disaster_recovery_drill_build_parser as drill_parser_owner
from scripts.diagnostics import run_m31_mock_exam_readiness_check_item as item_owner
from scripts.diagnostics import run_m31_mock_exam_readiness_check_build_markdown as markdown_owner
from scripts.diagnostics import run_m31_mock_exam_readiness_check_build_parser as readiness_parser_owner
from scripts.diagnostics import run_m31_slo_incident_review_check_severity_from_level as severity_owner
from scripts.diagnostics import run_m31_slo_incident_review_check_ownership_from_level as ownership_owner


def _body(func):
    return ast.dump(ast.parse(inspect.getsource(func)).body[0], include_attributes=False)


def _preimage_body(blob: str, name: str) -> str:
    source = subprocess.run(
        ["git", "cat-file", "blob", blob], check=True, capture_output=True, text=True
    ).stdout
    node = next(x for x in ast.parse(source).body if isinstance(x, ast.FunctionDef) and x.name == name)
    return ast.dump(ast.Module(body=node.body, type_ignores=[]), include_attributes=False)


def test_replay_helpers_fake_inputs_and_parity_boundary():
    obj = {"replayed_intent_total": "2", "fill_notional_total": "1.5"}
    assert drill._replay_metrics(obj) == metrics_owner._replay_metrics(obj)
    assert drill._replay_metrics({}) == {"replayed_intent_total": 0, "executed_intent_total": 0, "blocked_intent_total": 0, "pending_intent_total": 0, "fill_qty_total": 0, "fill_notional_total": 0.0}
    assert drill._replay_parity_ok({"fill_notional_total": 1}, {"fill_notional_total": 1 + 1e-10}) == (True, [])
    assert drill._replay_parity_ok({"executed_intent_total": 1}, {"executed_intent_total": 2}) == (False, ["parity_mismatch:executed_intent_total"])


def test_parser_facades_keep_defaults_and_flags():
    d = drill._build_parser().parse_args(["--inject-fail", "--json"])
    r = readiness._build_parser().parse_args(["--strict-session", "--allow-offhours"])
    assert (d.day, d.inject_fail, d.json) == ("2026-02-21", True, True)
    assert (r.day, r.strict_session, r.allow_offhours) == ("2026-02-21", True, True)


def test_readiness_item_and_markdown_are_in_memory_only():
    assert readiness._item(item_id="x", title="T", passed=0, evidence=12, required="") == {"id": "x", "title": "T", "required": False, "passed": False, "evidence": "12"}
    out = {"day": "2026-02-21", "ok": True, "required_pass_total": 1, "required_fail_total": 0, "stage_checks": {}, "runtime_profile": {}, "guardrails": {}, "checklist": [], "missing_prerequisites": []}
    assert readiness._build_markdown(out) == markdown_owner._build_markdown(out)
    assert readiness._build_markdown(out).endswith("- (none)\n")


def test_slo_level_facades_preserve_normalization():
    assert [slo._severity_from_level(x) for x in (" INCIDENT ", "watch", None, "other")] == ["SEV-1", "SEV-2", "SEV-3", "SEV-3"]
    assert [slo._ownership_from_level(x) for x in (" INCIDENT ", "watch", None, "other")] == ["primary_and_secondary_oncall", "primary_oncall", "none", "none"]


def test_owner_bodies_are_the_original_calculation_bodies_and_do_not_import_sources():
    pairs = [
        (metrics_owner._replay_metrics, ("replayed_intent_total", "fill_notional_total")),
        (parity_owner._replay_parity_ok, ("parity_mismatch:", "fill_notional_total")),
        (drill_parser_owner._build_parser, ("--working-dataset-root", "--json")),
        (item_owner._item, ("required", "evidence")),
        (markdown_owner._build_markdown, ("## Stage Checks", "## Missing Prerequisites")),
        (readiness_parser_owner._build_parser, ("--strict-session", "--allow-offhours")),
        (severity_owner._severity_from_level, ("incident", "SEV-1")),
        (ownership_owner._ownership_from_level, ("incident", "primary_and_secondary_oncall")),
    ]
    for owner, fragments in pairs:
        source = inspect.getsource(owner)
        assert "run_m29_disaster_recovery_drill import" not in source
        assert "run_m31_mock_exam_readiness_check import" not in source
        assert "run_m31_slo_incident_review_check import" not in source
        assert all(fragment in source for fragment in fragments)
        assert _body(owner)


def test_owner_ast_bodies_match_the_original_preimage_for_all_eight_moves():
    drill_blob = "a8a340b97a61ce953faf3d30c0dff7ca4cb86a56"
    readiness_blob = "721630febbfadcb62940c4cc56486cf11bf047af"
    slo_blob = "e70a3e791dcc3381a848b1e44a93b5234214a2eb"
    expected = [
        (drill_blob, "scripts/diagnostics/run_m29_disaster_recovery_drill.py", "_replay_metrics", metrics_owner._replay_metrics),
        (drill_blob, "scripts/diagnostics/run_m29_disaster_recovery_drill.py", "_replay_parity_ok", parity_owner._replay_parity_ok),
        (drill_blob, "scripts/diagnostics/run_m29_disaster_recovery_drill.py", "_build_parser", drill_parser_owner._build_parser),
        (readiness_blob, "scripts/diagnostics/run_m31_mock_exam_readiness_check.py", "_item", item_owner._item),
        (readiness_blob, "scripts/diagnostics/run_m31_mock_exam_readiness_check.py", "_build_markdown", markdown_owner._build_markdown),
        (readiness_blob, "scripts/diagnostics/run_m31_mock_exam_readiness_check.py", "_build_parser", readiness_parser_owner._build_parser),
        (slo_blob, "scripts/diagnostics/run_m31_slo_incident_review_check.py", "_severity_from_level", severity_owner._severity_from_level),
        (slo_blob, "scripts/diagnostics/run_m31_slo_incident_review_check.py", "_ownership_from_level", ownership_owner._ownership_from_level),
    ]
    for blob, path, name, owner in expected:
        owner_body = ast.parse(inspect.getsource(owner)).body[0].body
        assert _preimage_body(blob, name) == ast.dump(
            ast.Module(body=owner_body, type_ignores=[]), include_attributes=False
        )
