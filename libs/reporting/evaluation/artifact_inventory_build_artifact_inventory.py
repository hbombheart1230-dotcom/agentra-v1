"""artifact_inventory: ``build_artifact_inventory`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def build_artifact_inventory(reports_root: Path, day: str, *, facade: Any) -> dict[str, Any]:
    trades = [facade.inventory_trade(path) for path in facade.iter_trade_dirs(reports_root, day)]
    daily_root = facade.Path(reports_root) / "operator_summary" / "daily" / day
    daily = {
        name: facade._record(daily_root / filename, required=required)
        for name, filename, required in (
            ("daily_summary", "daily_summary.json", True),
            ("operator_summary", "operator_summary.json", False),
            ("q8_shadow_blocker_review", "q8_shadow_blocker_review.json", True),
            ("closeout_maintenance", "closeout_maintenance.json", False),
            ("q9_decision_windows", "q9_decision_windows.json", False),
        )
    }
    daily["q9_vs_samsung_hynix_comparison"] = facade._record(
        facade.Path(reports_root)
        / "evaluation"
        / "baseline_samsung_hynix"
        / day
        / "q9_vs_samsung_hynix_daily_comparison.json",
        required=False,
    )
    daily["q9_decision_windows"] = facade._q9_daily_diagnostics(
        reports_root,
        day,
        daily["q9_decision_windows"],
    )
    required_count = sum(
        1 for trade in trades for row in trade["artifacts"].values() if row["required"]
    ) + sum(1 for row in daily.values() if row["required"])
    present_required_count = sum(
        1 for trade in trades for row in trade["artifacts"].values() if row["required"] and row["exists"]
    ) + sum(1 for row in daily.values() if row["required"] and row["exists"])
    return {
        "schema_version": "artifact_inventory.v1",
        "day": day,
        "trade_count": len(trades),
        "required_artifact_count": required_count,
        "present_required_artifact_count": present_required_count,
        "required_coverage": round(present_required_count / required_count, 4) if required_count else 0.0,
        "trades": trades,
        "daily_artifacts": daily,
    }
