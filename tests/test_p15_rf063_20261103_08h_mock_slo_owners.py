from __future__ import annotations

import ast
import inspect
import subprocess
from pathlib import Path

import pytest

from scripts.diagnostics import run_m31_mock_investor_exam_check as mock
from scripts.diagnostics import run_m31_slo_incident_review_check as slo
from scripts.diagnostics import run_m31_mock_investor_exam_check_read_env_file as env_owner
from scripts.diagnostics import run_m31_mock_investor_exam_check_parse_kst_datetime as kst_owner
from scripts.diagnostics import run_m31_mock_investor_exam_check_utc_day as utc_owner
from scripts.diagnostics import run_m31_mock_investor_exam_check_item as item_owner
from scripts.diagnostics import run_m31_mock_investor_exam_check_build_markdown as markdown_owner
from scripts.diagnostics import run_m31_mock_investor_exam_check_build_parser as parser_owner
from scripts.diagnostics import run_m31_slo_incident_review_check_iter_jsonl as jsonl_owner
from scripts.diagnostics import run_m31_slo_incident_review_check_read_json as json_owner


MOCK_BLOB = "2a875186f0a869966b26192e5ebd72240dde69b9"
SLO_BLOB = "c3fbff8859a8bd34e9426f1058986ea45e973517"


def _preimage_body(blob: str, name: str) -> str:
    source = subprocess.run(
        ["git", "cat-file", "blob", blob], check=True, capture_output=True, text=True
    ).stdout
    function = next(
        node for node in ast.parse(source).body
        if isinstance(node, ast.FunctionDef) and node.name == name
    )
    return ast.dump(ast.Module(body=function.body, type_ignores=[]), include_attributes=False)


def test_mock_read_env_file_uses_only_fake_path_and_preserves_parsing(tmp_path: Path):
    fixture = tmp_path / "fake.env"
    fixture.write_text("# comment\nA=1 # inline\nB='x#y'\nC=\"two\"\nBROKEN\n=empty\n", encoding="utf-8")
    assert mock._read_env_file(fixture) == {"A": "1", "B": "x#y", "C": "two"}
    assert mock._read_env_file(tmp_path / "missing.env") == {}
    assert env_owner._read_env_file(fixture, facade=mock) == mock._read_env_file(fixture)


def test_mock_kst_utc_day_item_and_facade_monkeypatch():
    assert mock._parse_kst_datetime("") is None
    assert mock._parse_kst_datetime("invalid") is None
    assert mock._parse_kst_datetime("2026-02-21T00:00:00Z").isoformat().endswith("+09:00")
    assert mock._utc_day(0) == "1970-01-01"
    mock._to_epoch = lambda _value: 86_400
    assert utc_owner._utc_day("patched", facade=mock) == "1970-01-02"
    result = mock._item(item_id="x", title="X", passed=1, evidence=7)
    assert list(result) == ["id", "title", "required", "passed", "evidence"]
    assert result == {"id": "x", "title": "X", "required": True, "passed": True, "evidence": "7"}
    with pytest.raises(TypeError):
        mock._item("x", "X", True, "e")
    assert kst_owner._parse_kst_datetime("2026-02-21T00:00:00Z", facade=mock) == mock._parse_kst_datetime("2026-02-21T00:00:00Z")
    assert item_owner._item(item_id="x", title="X", passed=True, evidence="e", facade=mock)["id"] == "x"


def test_mock_markdown_and_parser_exact_output_shapes():
    payload = {"day": "2026-01-02", "ok": True, "required_pass_total": 2, "required_fail_total": 0,
               "runtime_mode": {}, "guardrails": {}, "market": {}, "events": {},
               "checklist": [{"passed": False, "title": "한글", "evidence": "왜"}], "failures": ["f"]}
    markdown = mock._build_markdown(payload)
    assert markdown.startswith("# M31-2 Mock Investor Exam Check (2026-01-02)\n")
    assert "- [ ] 한글 | evidence=왜" in markdown
    assert markdown.endswith("## Failures\n\n- f\n")
    args = mock._build_parser().parse_args(["--allow-offhours", "--strict-session", "--now-kst", "2026-02-21T09:00:00"])
    assert (args.allow_offhours, args.strict_session, args.now_kst) == (True, True, "2026-02-21T09:00:00")
    assert markdown_owner._build_markdown(payload, facade=mock) == markdown
    assert parser_owner._build_parser(facade=mock).parse_args(["--json"]).json is True


def test_slo_json_readers_are_lazy_and_only_read_fake_paths(tmp_path: Path):
    jsonl = tmp_path / "events.jsonl"
    jsonl.write_text("\nnot json\n[]\n{\"a\": 1}\n", encoding="utf-8")
    iterator = slo._iter_jsonl(jsonl)
    assert not isinstance(iterator, list)
    assert list(iterator) == [{"a": 1}]
    assert slo._iter_jsonl(tmp_path / "missing.jsonl") == []
    document = tmp_path / "document.json"
    document.write_text('{"ok": true}', encoding="utf-8")
    assert slo._read_json(document) == {"ok": True}
    document.write_text("[]", encoding="utf-8")
    assert slo._read_json(document) == {}
    document.write_text("bad", encoding="utf-8")
    assert slo._read_json(document) == {}
    assert list(jsonl_owner._iter_jsonl(jsonl, facade=slo)) == [{"a": 1}]
    assert json_owner._read_json(tmp_path / "missing.json", facade=slo) == {}


def test_all_eight_preimage_bodies_are_owned_once_and_source_is_thin():
    pairs = [
        (MOCK_BLOB, "_read_env_file", env_owner._read_env_file),
        (MOCK_BLOB, "_parse_kst_datetime", kst_owner._parse_kst_datetime),
        (MOCK_BLOB, "_utc_day", utc_owner._utc_day),
        (MOCK_BLOB, "_item", item_owner._item),
        (MOCK_BLOB, "_build_markdown", markdown_owner._build_markdown),
        (MOCK_BLOB, "_build_parser", parser_owner._build_parser),
        (SLO_BLOB, "_iter_jsonl", jsonl_owner._iter_jsonl),
        (SLO_BLOB, "_read_json", json_owner._read_json),
    ]
    source_modules = [mock, mock, mock, mock, mock, mock, slo, slo]
    for (blob, name, owner), source_module in zip(pairs, source_modules):
        owner_node = ast.parse(inspect.getsource(owner)).body[0]
        source_node = ast.parse(inspect.getsource(getattr(source_module, name))).body[0]
        assert _preimage_body(blob, name)
        assert owner_node.body
        assert len(source_node.body) == 2
        assert isinstance(source_node.body[0], (ast.ImportFrom, ast.Import))
        assert isinstance(source_node.body[1], ast.Return)
