from __future__ import annotations

import ast
import inspect
import subprocess

import pytest

from scripts.diagnostics import run_m31_slo_incident_review_check as slo
from scripts.diagnostics import run_m31_mock_investor_exam_check as mock
from scripts.diagnostics import run_m31_slo_incident_review_check_to_epoch as slo_epoch
from scripts.diagnostics import run_m31_slo_incident_review_check_utc_day as slo_day
from scripts.diagnostics import run_m31_slo_incident_review_check_item as slo_item
from scripts.diagnostics import run_m31_slo_incident_review_check_build_markdown as slo_markdown
from scripts.diagnostics import run_m31_slo_incident_review_check_build_parser as slo_parser
from scripts.diagnostics import run_m31_mock_investor_exam_check_env_bool as mock_bool
from scripts.diagnostics import run_m31_mock_investor_exam_check_to_float as mock_float
from scripts.diagnostics import run_m31_mock_investor_exam_check_to_epoch as mock_epoch


SLO_BLOB = "7a1ad49ba5941aa661a974a4b6690bade41275eb"
MOCK_BLOB = "e4e7e5c56a044fe10ff85c9d273a9d77ff03d88f"


def _original_function(blob: str, name: str) -> ast.FunctionDef:
    text = subprocess.run(
        ["git", "cat-file", "blob", blob], check=True, capture_output=True, text=True
    ).stdout
    return next(n for n in ast.parse(text).body if isinstance(n, ast.FunctionDef) and n.name == name)


def _normalized_body(node: ast.FunctionDef) -> str:
    body = ast.Module(body=node.body, type_ignores=[])
    aliases = {
        "facade._to_epoch": "_to_epoch",
        "facade.datetime": "datetime",
        "facade.timezone": "timezone",
        "facade.argparse": "argparse",
        "dt_type": "datetime",
        "tz": "timezone",
    }

    class NormalizeFacade(ast.NodeTransformer):
        def visit_Name(self, item):
            alias = aliases.get(item.id)
            if alias:
                return ast.copy_location(ast.Name(id=alias, ctx=item.ctx), item)
            return item

        def visit_Assign(self, item):
            value = self.visit(item.value)
            if len(item.targets) == 1 and isinstance(item.targets[0], ast.Name):
                target = item.targets[0].id
                expected = aliases.get(target)
                if expected and isinstance(value, ast.Name) and value.id == expected:
                    return None
            item.targets = [self.visit(target) for target in item.targets]
            item.value = value
            item.type_comment = None
            return item

        def visit_Attribute(self, item):
            value = self.generic_visit(item)
            key = ast.unparse(value)
            if key in aliases:
                return ast.copy_location(ast.Name(id=aliases[key], ctx=ast.Load()), value)
            return value

        def visit_IfExp(self, item):
            value = self.generic_visit(item)
            if ast.dump(value.body, include_attributes=False) == ast.dump(
                value.orelse, include_attributes=False
            ):
                return value.body
            return value

    return ast.dump(NormalizeFacade().visit(body), include_attributes=False)


def test_slo_epoch_utc_day_and_call_time_facade(monkeypatch):
    assert slo._to_epoch(None) is None
    assert slo._to_epoch(12.9) == 12
    assert slo._to_epoch("12.9") == 12
    assert slo._to_epoch("1970-01-01T00:00:00Z") == 0
    assert slo._to_epoch("not-a-date") is None
    assert slo._utc_day(0) == "1970-01-01"
    monkeypatch.setattr(slo, "_to_epoch", lambda _value: 86_400)
    assert slo_day._utc_day("patched", facade=slo) == "1970-01-02"


def test_slo_item_keyword_only_defaults_type_error_and_key_order():
    result = slo._item(item_id="x", title="X", passed=1, evidence=7)
    assert list(result) == ["id", "title", "required", "passed", "evidence"]
    assert result == {"id": "x", "title": "X", "required": True, "passed": True, "evidence": "7"}
    assert slo._item(item_id="x", title="X", passed=0, evidence="e", required=False)["required"] is False
    with pytest.raises(TypeError):
        slo._item("x", "X", True, "e")


def test_slo_markdown_and_parser_fake_inputs():
    payload = {"day": "2026-01-02", "ok": True, "required_pass_total": 2, "required_fail_total": 0,
               "slo": {"run_total": 2, "success_run_total": 2, "availability_rate": 1.0, "event_total": 3, "error_total": 0, "error_rate": 0.0},
               "incident": {"cooldown_transition_total": 1, "intervention_total": 0},
               "policy": {"escalation_level": "normal", "severity": "SEV-3", "ownership": "none"},
               "checklist": [{"passed": True, "title": "ready", "evidence": "fake"}], "failures": []}
    markdown = slo._build_markdown(payload)
    assert markdown.startswith("# M31-1 SLO and Incident Review Check (2026-01-02)\n")
    assert "availability_rate: **100.00%**" in markdown
    assert "- [x] ready | evidence=fake" in markdown
    assert markdown.endswith("## Failures\n\n- (none)\n")
    args = slo._build_parser().parse_args(["--day", "2026-03-04", "--inject-fail", "--json"])
    assert (args.day, args.inject_fail, args.json) == ("2026-03-04", True, True)


def test_mock_exam_helpers_defaults_custom_values_and_datetime():
    assert mock._env_bool({}, "x") is False
    assert mock._env_bool({}, "x", True) is True
    assert mock._env_bool({"x": " YES "}, "x") is True
    assert mock._env_bool({"x": "false"}, "x") is False
    assert mock._to_float("bad", 2) == 2.0
    assert mock._to_float("0") == 0.0
    assert mock._to_epoch("1970-01-01T00:00:00Z") == 0
    assert mock._to_epoch("1970-01-01T00:00:00") == 0
    assert mock._to_epoch("not-a-date") is None


def test_original_preimage_ast_bodies_match_all_eight_owners():
    pairs = [
        (SLO_BLOB, "_to_epoch", slo_epoch._to_epoch),
        (SLO_BLOB, "_utc_day", slo_day._utc_day),
        (SLO_BLOB, "_item", slo_item._item),
        (SLO_BLOB, "_build_markdown", slo_markdown._build_markdown),
        (SLO_BLOB, "_build_parser", slo_parser._build_parser),
        (MOCK_BLOB, "_env_bool", mock_bool._env_bool),
        (MOCK_BLOB, "_to_float", mock_float._to_float),
        (MOCK_BLOB, "_to_epoch", mock_epoch._to_epoch),
    ]
    for blob, name, owner in pairs:
        original = _original_function(blob, name)
        current_owner = ast.parse(inspect.getsource(owner)).body[0]
        assert _normalized_body(original) == _normalized_body(current_owner)


def test_source_facades_keep_original_signatures_and_delegate_to_owners():
    assert str(inspect.signature(slo._item)) == "(*, item_id: 'str', title: 'str', passed: 'bool', evidence: 'str', required: 'bool' = True) -> 'Dict[str, Any]'"
    assert str(inspect.signature(slo._to_epoch)) == "(ts: 'Any') -> 'Optional[int]'"
    assert str(inspect.signature(mock._env_bool)) == "(env: 'Dict[str, str]', key: 'str', default: 'bool' = False) -> 'bool'"
