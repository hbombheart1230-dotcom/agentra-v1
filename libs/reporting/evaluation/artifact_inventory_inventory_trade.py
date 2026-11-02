"""artifact_inventory: ``inventory_trade`` body (moved verbatim from ``artifact_inventory``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping


def inventory_trade(trade_dir: Path, *, facade: Any) -> dict[str, Any]:
    paths: Iterable[tuple[str, facade.Path, bool]] = (
        ("lifecycle_bundle", trade_dir / "lifecycle_bundle.json", True),
        ("entry", trade_dir / "entry.json", True),
        ("exit", trade_dir / "exit.json", False),
        ("scanner_evidence", trade_dir / "evidence" / "scanner_evidence.json", True),
        ("strategist_evidence", trade_dir / "evidence" / "strategist_evidence.json", True),
        ("commander_evidence", trade_dir / "evidence" / "commander_evidence.json", True),
        ("monitor_evidence", trade_dir / "evidence" / "monitor_evidence.json", True),
        ("ai_trade_summary", trade_dir / "reports" / "ai_trade_summary.json", False),
        ("post_exit_shadow", trade_dir / "reports" / "post_exit_shadow_recap.json", False),
    )
    artifacts = {name: facade._record(path, required=required) for name, path, required in paths}
    missing_required = [name for name, row in artifacts.items() if row["required"] and not row["exists"]]
    return {
        "trade_dir": str(trade_dir),
        "trade_id": trade_dir.name,
        "artifacts": artifacts,
        "missing_required": missing_required,
        "complete": not missing_required,
    }
