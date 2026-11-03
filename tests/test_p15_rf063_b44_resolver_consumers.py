from __future__ import annotations

from pathlib import Path

from libs.reporting import llm_artifacts
from libs.reporting import single_trade_report


DAY = "2026-11-04"
TRADE_ID = "TRD_20261104_005930_01"


def _trade_marker(root: Path, name: str = TRADE_ID) -> Path:
    trade_root = root / name
    trade_root.mkdir(parents=True)
    (trade_root / "lifecycle_bundle.json").write_text("{}", encoding="utf-8")
    return trade_root


def _state() -> dict:
    return {
        "day": DAY,
        "run_id": "b44-run",
        "ts": f"{DAY}T01:23:45+00:00",
        "applied_policy": {"reporter": {"trade_report": {"enabled": True, "generate_on_open": False}}},
        "execution": {
            "ok": True,
            "reason": "fake execution only",
            "order": {"action": "SELL", "symbol": "005930", "qty": 1},
            "payload": {"order_id": "B44-FAKE", "filled_qty": 1, "avg_fill_price": 1},
        },
        "monitor_output": {"decision": "SELL", "decision_summary": "fake", "position_age_seconds": 0},
        "scanner_output": {"selected": {"symbol": "005930", "why": "fake"}},
        "strategist_output": {},
        "commander_decision": {},
    }


def _fake_report(story_input: dict, **_kwargs: object) -> dict:
    return {
        "trade_id": story_input["trade_id"],
        "generation": {"status": "ok"},
        "ai_trade_report_status": "ok",
        "llm_response_artifact": {"status": "ok", "llm_status": "ok", "model_info": {}},
    }


def test_resolver_prefers_canonical_then_legacy_then_canonical_absent(tmp_path: Path) -> None:
    reports_root = tmp_path / "reports"
    canonical = _trade_marker(reports_root / "trades" / DAY)
    legacy = _trade_marker(tmp_path / DAY, "TRD_20261104_000660_02")

    assert llm_artifacts.resolve_trade_day_root(reports_root, DAY) == canonical.parent
    assert llm_artifacts.find_trade_dir(canonical.parent, TRADE_ID) == canonical

    # Remove only the canonical marker so the legacy root becomes the resolver fallback.
    for path in sorted(canonical.rglob("*"), reverse=True):
        path.unlink() if path.is_file() else path.rmdir()
    canonical.rmdir()
    canonical.parent.rmdir()
    assert llm_artifacts.resolve_trade_day_root(reports_root, DAY) == legacy.parent

    for path in sorted(legacy.rglob("*"), reverse=True):
        path.unlink() if path.is_file() else path.rmdir()
    legacy.rmdir()
    assert llm_artifacts.resolve_trade_day_root(reports_root, DAY) == reports_root / "trades" / DAY


def test_resolver_uses_call_time_fallback_dependency(tmp_path: Path, monkeypatch) -> None:
    reports_root = tmp_path / "reports"
    replacement = _trade_marker(tmp_path / "replacement")

    monkeypatch.setattr(llm_artifacts, "misplaced_trade_day_root", lambda *_args: replacement.parent)

    assert llm_artifacts.resolve_trade_day_root(reports_root, DAY) == replacement.parent


def test_single_trade_report_uses_real_path_consumer_with_fake_only_inputs(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(single_trade_report, "build_ai_trade_report", _fake_report)
    monkeypatch.setattr(single_trade_report, "render_trade_report_markdown", lambda _report: "# fake")
    monkeypatch.setattr("subprocess.Popen", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("no subprocess")))
    monkeypatch.setattr("subprocess.run", lambda *_args, **_kwargs: (_ for _ in ()).throw(AssertionError("no subprocess")))

    out = single_trade_report.generate_single_trade_report(TRADE_ID, state=_state(), root=tmp_path)

    expected = tmp_path / "reports" / "trades" / DAY / TRADE_ID
    assert out["ok"] is True
    assert Path(out["report_path"]).parent.parent == expected
    assert (expected / "reports" / "ai_trade_report.json").exists()
