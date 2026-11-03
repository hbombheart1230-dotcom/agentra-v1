from __future__ import annotations

from pathlib import Path

import pytest

from scripts.diagnostics import run_m30_quality_gates_bundle as quality
from scripts.diagnostics import run_m30_release_signoff_checklist as signoff
from scripts.diagnostics import run_m31_mock_investor_exam_check as mock
from scripts.diagnostics import run_m31_slo_incident_review_check as slo
from scripts.diagnostics import run_m31_slo_incident_review_check_resolve_day_artifact as resolve_owner
from scripts.diagnostics import run_m31_mock_investor_exam_check_iter_jsonl as mock_jsonl_owner
from scripts.diagnostics import run_m30_quality_gates_bundle_build_md as quality_md_owner
from scripts.diagnostics import run_m30_quality_gates_bundle_component_summary as component_owner
from scripts.diagnostics import run_m30_quality_gates_bundle_gate_status as gate_owner
from scripts.diagnostics import run_m30_quality_gates_bundle_build_parser as quality_parser_owner
from scripts.diagnostics import run_m30_release_signoff_checklist_count_by as count_owner
from scripts.diagnostics import run_m30_release_signoff_checklist_build_markdown as signoff_md_owner


def test_resolve_day_artifact_uses_fake_report_dir_and_facade_reader(tmp_path: Path, monkeypatch):
    direct = tmp_path / "policy_2026-02-21.json"
    direct.write_text("{}", encoding="utf-8")
    prior = tmp_path / "policy_2026-02-20.json"
    prior.write_text("{}", encoding="utf-8")
    future = tmp_path / "policy_2026-02-22.json"
    future.write_text("{}", encoding="utf-8")

    def fake_reader(path: Path):
        return {"path": path.name} if path.name != direct.name else {}

    monkeypatch.setattr(slo, "_read_json", fake_reader)
    path, obj, fallback = slo._resolve_day_artifact(tmp_path, "policy", "2026-02-21")
    assert (path, obj, fallback) == (prior, {"path": "policy_2026-02-20.json"}, True)
    assert resolve_owner._resolve_day_artifact(tmp_path, "policy", "2026-02-21", facade=slo) == (prior, {"path": "policy_2026-02-20.json"}, True)


def test_mock_jsonl_is_lazy_and_filters_fake_fixture(tmp_path: Path):
    fixture = tmp_path / "events.jsonl"
    fixture.write_text("\ninvalid\n[]\n{\"row\": 1}\n{\"row\": 2}\n", encoding="utf-8")
    rows = mock._iter_jsonl(fixture)
    assert not isinstance(rows, list)
    assert list(rows) == [{"row": 1}, {"row": 2}]
    assert mock._iter_jsonl(tmp_path / "missing.jsonl") == []
    assert list(mock_jsonl_owner._iter_jsonl(fixture, facade=mock)) == [{"row": 1}, {"row": 2}]


def test_quality_helpers_preserve_markdown_component_and_gate_shape():
    payload = {"day": "2026-02-21", "ok": True, "failure_total": 0, "report_json_path": "fake.json",
               "gates": {"functional": {"ok": True, "pass_total": 1, "fail_total": 0}}, "failures": []}
    markdown = quality._build_md(payload)
    assert markdown.startswith("# M30 Quality Gates Bundle (2026-02-21)\n")
    assert "- functional: ok=True pass_total=1 fail_total=0" in markdown
    assert markdown.endswith("## Failures\n\n- (none)\n")
    assert quality._component_summary(2, {"ok": 1, "failures": ["a"]}) == {"rc": 2, "ok": True, "failure_total": 1}
    components = {"a": {"ok": True, "rc": 0}, "b": {"ok": False, "rc": 1}}
    assert quality._gate_status(components) == {"ok": False, "pass_total": 1, "fail_total": 1, "components": components}
    assert quality_md_owner._build_md(payload, facade=quality) == markdown
    assert component_owner._component_summary(2, {"ok": 1, "failures": ["a"]}, facade=quality)["failure_total"] == 1
    assert gate_owner._gate_status(components, facade=quality)["components"] is components


def test_quality_parser_and_signoff_helpers_are_in_memory_only():
    args = quality._build_parser().parse_args(["--day", "2026-03-04", "--inject-fail", "--json"])
    assert (args.day, args.inject_fail, args.json) == ("2026-03-04", True, True)
    assert quality_parser_owner._build_parser(facade=quality).parse_args(["--no-clear"]).no_clear is True
    items = [{"category": "ops"}, {"category": "ops"}, {"category": ""}, {"category": "security"}]
    assert signoff._count_by(items, "category") == {"ops": 2, "security": 1}
    payload = {"day": "2026-02-21", "release_ready": True, "quality_gates_ok": True,
               "required_pass_total": 1, "required_fail_total": 0,
               "checklist": [{"passed": True, "category": "ops", "title": "ready", "evidence": "fake"}], "failures": []}
    markdown = signoff._build_markdown(payload)
    assert "- [x] (ops) ready | evidence=fake" in markdown
    assert markdown.endswith("## Failures\n\n- (none)\n")
    assert count_owner._count_by(items, "category", facade=signoff) == {"ops": 2, "security": 1}
    assert signoff_md_owner._build_markdown(payload, facade=signoff) == markdown


def test_keyword_and_source_facade_contracts():
    assert quality._build_md({"gates": {}}) == quality_md_owner._build_md({"gates": {}}, facade=quality)
    with pytest.raises(TypeError):
        signoff._count_by()
