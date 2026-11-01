import json
import sys
from pathlib import Path

import pytest

from scripts.research import daily_profitability_scorecard as daily
from scripts.research import run_agent_effectiveness_scorecard as effectiveness


_DAILY = {
    "total_trades": 2,
    "closed_trades": 1,
    "loss_trades": 0,
    "lifecycle_linkage_missing_count": 0,
    "holding_evidence_thin_count": 0,
    "execution_fields_missing_count": 0,
    "top_recurring_diagnostic_weakness": "none",
}


def test_daily_cli_uses_fake_consumer_only(monkeypatch, capsys, tmp_path: Path):
    calls = []

    def fake(root: Path, day: str):
        calls.append((root, day))
        return _DAILY

    monkeypatch.setattr(daily, "build_daily_profitability_scorecard", fake)
    assert daily.main(["--date", "2026-11-01", "--reports-root", str(tmp_path), "--json"]) == 0
    assert calls == [(tmp_path, "2026-11-01")]
    assert json.loads(capsys.readouterr().out) == _DAILY
    assert list(tmp_path.iterdir()) == []


def test_daily_missing_date_does_not_call_fake(monkeypatch):
    monkeypatch.setattr(daily, "build_daily_profitability_scorecard", lambda *_: pytest.fail("writer called"))
    with pytest.raises(SystemExit) as exc:
        daily.main(["--json"])
    assert exc.value.code == 2


def test_effectiveness_same_day_uses_single_fake_writer(monkeypatch, capsys, tmp_path: Path):
    calls = []

    def fake_main(**kwargs):
        calls.append(("main", kwargs))
        return {"ok": True}

    def fake_single(**kwargs):
        calls.append(("single", kwargs))
        return {"review": "single"}

    monkeypatch.setattr(effectiveness, "write_agent_effectiveness_scorecard", fake_main)
    monkeypatch.setattr(effectiveness, "write_stage2_authority_review", fake_single)
    monkeypatch.setattr(effectiveness, "write_stage2_authority_review_sharded", lambda **_: pytest.fail("sharded called"))
    monkeypatch.setattr(sys, "argv", ["cmd", "--start", "2026-11-01", "--end", "2026-11-01", "--reports-root", str(tmp_path), "--output-dir", str(tmp_path / "out")])
    assert effectiveness.main() == 0
    assert [name for name, _ in calls] == ["main", "single"]
    assert calls[0][1] == {"reports_root": tmp_path, "start": "2026-11-01", "end": "2026-11-01", "output_dir": tmp_path / "out"}
    assert "strategist_stage2_authority_review" in json.loads(capsys.readouterr().out)
    assert list(tmp_path.iterdir()) == []


def test_effectiveness_multi_day_and_missing_end_are_fake_only(monkeypatch, tmp_path: Path):
    calls = []
    monkeypatch.setattr(effectiveness, "write_agent_effectiveness_scorecard", lambda **kwargs: calls.append(("main", kwargs)) or {})
    monkeypatch.setattr(effectiveness, "write_stage2_authority_review", lambda **_: pytest.fail("single called"))
    monkeypatch.setattr(effectiveness, "write_stage2_authority_review_sharded", lambda **kwargs: calls.append(("sharded", kwargs)) or {})
    monkeypatch.setattr(sys, "argv", ["cmd", "--start", "2026-11-01", "--end", "2026-11-02", "--reports-root", str(tmp_path), "--output-dir", str(tmp_path / "out")])
    assert effectiveness.main() == 0
    assert [name for name, _ in calls] == ["main", "sharded"]
    monkeypatch.setattr(sys, "argv", ["cmd", "--start", "2026-11-01"])
    with pytest.raises(SystemExit) as exc:
        effectiveness.main()
    assert exc.value.code == 2
