import json
from pathlib import Path

from scripts.diagnostics import check_audit_trail_completeness as audit
from scripts.diagnostics import check_log_archive_integrity as archive
from scripts.diagnostics import run_m26_closeout_check as closeout
from scripts.diagnostics import run_m26_dataset_manifest_check as manifest
from scripts.diagnostics import run_m27_conflict_resolution_check as conflict


def test_k1_markdown_wrapper_and_owner():
    text = audit._build_markdown(day="2026-02-17", out={"ok": True, "stage_event_total": {}})
    assert "Audit Trail Completeness" in text and "Failures" in text


def test_k3_seed_demo_wrapper_and_owner(tmp_path: Path):
    path = manifest._seed_demo_dataset(tmp_path)
    payload = json.loads(path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == manifest.SCHEMA_VERSION
    assert (tmp_path / "execution" / "fills.jsonl").exists()


def test_k4_candidate_dataset_wrapper_and_owner(tmp_path: Path):
    for child in ("execution", "market"):
        (tmp_path / child).mkdir()
    closeout._prepare_candidate_dataset(tmp_path, day="2026-02-17")
    assert '"action": "SELL"' in (tmp_path / "execution" / "intents.jsonl").read_text()


def test_b1_archive_day_wrapper_and_owner():
    assert str(archive._parse_day("2026-02-17")) == "2026-02-17"


def test_b2_archive_markdown_wrapper_and_owner():
    assert "Log Archive Integrity" in archive._markdown({"day": "2026-02-17", "ok": True})


def test_b3_archive_parser_wrapper_and_owner():
    assert archive._build_parser().parse_args(["--json"]).json is True


def test_b7_conflict_intents_wrapper_and_owner():
    assert len(conflict._default_intents(inject_fail=False)) == 4
    assert len(conflict._default_intents(inject_fail=True)) == 2
