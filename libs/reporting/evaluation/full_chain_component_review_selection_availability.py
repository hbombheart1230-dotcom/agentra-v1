"""full_chain_component_review: ``_selection_availability`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _selection_availability(models: list[dict[str, Any]], *, facade: Any) -> dict[str, Any]:
    raw_controls = 0
    strategist_snapshots = 0
    commander_snapshots = 0
    comparable_strategist = 0
    comparable_commander = 0
    missing: dict[str, int] = facade.defaultdict(int)
    for model in models:
        selection = model.get("selection") if isinstance(model.get("selection"), facade.Mapping) else {}
        raw_rows = selection.get("raw_scanner_top10")
        raw_control = bool(
            selection.get("raw_scanner_snapshot_source")
            in {"control_snapshot", "scanner_intrinsic_control_snapshot"}
            and isinstance(raw_rows, list)
            and raw_rows
        )
        strategist = bool(
            selection.get("strategist_run_id")
            and isinstance(selection.get("post_strategist_top10"), list)
            and selection.get("post_strategist_top10")
        )
        commander = bool(selection.get("commander_final_explicit"))
        raw_controls += int(raw_control)
        strategist_snapshots += int(strategist)
        commander_snapshots += int(commander)
        comparable_strategist += int(raw_control and strategist)
        comparable_commander += int(strategist and commander)
        if not raw_control:
            missing["trusted_raw_scanner_top10"] += 1
        if not strategist:
            missing["strategist_run_and_post_ranking"] += 1
        if not commander:
            missing["explicit_commander_selection_or_veto"] += 1
    return {
        "trade_model_count": len(models),
        "raw_scanner_control_count": raw_controls,
        "strategist_snapshot_count": strategist_snapshots,
        "commander_snapshot_count": commander_snapshots,
        "scanner_vs_strategist_comparable_count": comparable_strategist,
        "strategist_vs_commander_comparable_count": comparable_commander,
        "missing_fields": dict(sorted(missing.items())),
    }
