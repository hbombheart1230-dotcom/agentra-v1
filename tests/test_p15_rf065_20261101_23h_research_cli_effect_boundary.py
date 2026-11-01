import json
import subprocess
from pathlib import Path

from scripts.research import run_alpha_research_board as alpha
from scripts.research import run_attribution_score_range as score_range
from scripts.research import run_attribution_score_window as score_window


_PINS = {
    "scripts/research/run_alpha_research_board.py": "059026ee848adcb0c69ac88b49d17f8ae9a2fbc2",
    "scripts/research/run_attribution_score_range.py": "b7af6023c25b4c42fc7cc6aad3df4048bd69623f",
    "scripts/research/run_attribution_score_window.py": "d9f8d204ff42941a66874aff1e45a35c4f1003b9",
    "scripts/research/phase5_validation_markdown.py": "cc37e3ddf7ee1ed5b6eee7e8d28f6bff3d6ca7cb",
}


def _pin_sources():
    for path, expected in _PINS.items():
        assert subprocess.check_output(["git", "rev-parse", f"HEAD:{path}"], text=True).strip() == expected


def _guard_effects(monkeypatch):
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("subprocess invoked")))
    monkeypatch.setattr(Path, "mkdir", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("mkdir invoked")))
    monkeypatch.setattr(Path, "write_text", lambda *_a, **_kw: (_ for _ in ()).throw(AssertionError("write invoked")))


def test_alpha_cli_without_output_dir_is_fake_only(monkeypatch, capsys):
    _pin_sources()
    seen = {}
    monkeypatch.setattr(alpha, "build_alpha_research_board", lambda **kwargs: seen.update(kwargs) or {"ok": True, "day": "2026-09-29"})
    monkeypatch.setattr(alpha.sys, "argv", ["prog", "--through-day", "2026-09-29", "--reports-root", "/fake/reports"])
    _guard_effects(monkeypatch)
    assert alpha.main() == 0
    assert seen == {"reports_root": Path("/fake/reports"), "through_day": "2026-09-29"}
    assert json.loads(capsys.readouterr().out) == {"ok": True, "day": "2026-09-29"}


def test_attribution_range_cli_forwards_to_fake_writer(monkeypatch, capsys):
    _pin_sources()
    seen = {}
    monkeypatch.setattr(score_range, "write_attribution_score_range", lambda **kwargs: seen.update(kwargs) or {"ok": True, "range": "fake"})
    monkeypatch.setattr(score_range.sys, "argv", ["prog", "--start", "2026-09-01", "--end", "2026-09-03", "--include-empty-days", "--reports-root", "/fake/reports"])
    _guard_effects(monkeypatch)
    assert score_range.main() == 0
    assert seen == {"reports_root": Path("/fake/reports"), "start": "2026-09-01", "end": "2026-09-03", "include_empty_days": True}
    assert json.loads(capsys.readouterr().out) == {"ok": True, "range": "fake"}


def test_attribution_window_cli_forwards_to_fake_writer(monkeypatch, capsys):
    _pin_sources()
    seen = {}
    monkeypatch.setattr(score_window, "write_attribution_score_window", lambda **kwargs: seen.update(kwargs) or {"ok": True, "window": "fake"})
    monkeypatch.setattr(score_window.sys, "argv", ["prog", "--window-id", "fake-window", "--reports-root", "/fake/reports"])
    _guard_effects(monkeypatch)
    assert score_window.main() == 0
    assert seen == {"reports_root": Path("/fake/reports"), "window_id": "fake-window"}
    assert json.loads(capsys.readouterr().out) == {"ok": True, "window": "fake"}
