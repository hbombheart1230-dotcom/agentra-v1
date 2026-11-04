from __future__ import annotations

import json
from pathlib import Path

from scripts.diagnostics import check_reports_trades_health as subject


_SECTIONS = (
    "executive_summary",
    "market_context_at_entry",
    "why_this_symbol_was_chosen",
    "entry_decision",
    "holding_monitoring_story",
    "exit_decision",
    "execution_quality",
    "scanner_filters",
    "guard_approval_result",
    "reporter_evaluation",
    "errors_weaknesses_improvement_points",
    "final_operator_conclusion",
)


def _write_report(path: Path, *, complete: bool = True) -> None:
    payload = {key: {} for key in _SECTIONS}
    if not complete:
        payload.pop("final_operator_conclusion")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")


def test_ai_report_is_complete_reads_canonical_report_path(tmp_path: Path) -> None:
    _write_report(tmp_path / "reports" / "ai_trade_report.json")

    assert subject._ai_trade_report_is_complete(tmp_path) is True


def test_ai_report_is_complete_rejects_incomplete_canonical_report(tmp_path: Path) -> None:
    _write_report(tmp_path / "reports" / "ai_trade_report.json", complete=False)

    assert subject._ai_trade_report_is_complete(tmp_path) is False


def test_ai_report_is_complete_prefers_canonical_report_over_legacy(tmp_path: Path) -> None:
    _write_report(tmp_path / "reports" / "ai_trade_report.json")
    _write_report(tmp_path / "ai_trade_report" / "ai_trade_report.json", complete=False)

    assert subject._ai_trade_report_is_complete(tmp_path) is True


def test_ai_report_is_complete_keeps_legacy_fallbacks(tmp_path: Path) -> None:
    _write_report(tmp_path / "ai_trade_report" / "ai_trade_report.json")
    assert subject._ai_trade_report_is_complete(tmp_path) is True

    for path in (tmp_path / "ai_trade_report").iterdir():
        path.unlink()
    (tmp_path / "ai_trade_report").rmdir()
    _write_report(tmp_path / "trade_report.json")
    assert subject._ai_trade_report_is_complete(tmp_path) is True
