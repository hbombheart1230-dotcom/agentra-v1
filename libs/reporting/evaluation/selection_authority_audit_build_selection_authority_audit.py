"""selection_authority_audit: ``build_selection_authority_audit`` body (moved verbatim from ``selection_authority_audit``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from collections import Counter
from typing import Any, Mapping, Sequence


def build_selection_authority_audit(
    models: Sequence[Mapping[str, Any]],
    *,
    facade: Any,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    counters: Counter[str] = facade.Counter()
    for model in models:
        integrity = facade._mapping(model.get("integrity"))
        defects = {str(value) for value in (integrity.get("defects") or [])}
        if "broker_day_partial_exit_duplicate" in defects:
            counters["excluded:broker_day_partial_exit_duplicate"] += 1
            continue
        if "confirmed_runtime_defect" in defects:
            counters["excluded:confirmed_runtime_defect"] += 1
            continue
        selection = facade._mapping(model.get("selection"))
        monitor = facade._mapping(model.get("monitor"))
        commander = facade._mapping(selection.get("commander_final"))
        raw_top1 = facade._symbol(selection.get("raw_scanner_top1"))
        post_top1 = facade._symbol(selection.get("scanner_top1"))
        selected = facade._symbol(selection.get("selected_symbol"))
        monitor_symbol = facade._symbol(
            monitor.get("selected_symbol")
            or facade._mapping(monitor.get("entry_context")).get("selected_symbol")
        )
        commander_candidate = facade._symbol(commander.get("candidate_symbol"))
        commander_selected = facade._symbol(commander.get("selected_symbol"))
        executed = facade._symbol(model.get("symbol"))
        raw_to_post = facade._changed(raw_top1, post_top1)
        post_to_selected = facade._changed(post_top1, selected)
        selected_to_monitor = facade._changed(selected, monitor_symbol)
        monitor_to_commander = facade._changed(monitor_symbol or selected, commander_candidate or commander_selected)
        final_to_executed = facade._changed(commander_selected or commander_candidate or selected, executed)
        row = {
            "trade_id": model.get("trade_id"),
            "symbol": executed,
            "raw_scanner_top1": raw_top1,
            "post_strategy_top1": post_top1,
            "selected_symbol": selected,
            "monitor_symbol": monitor_symbol,
            "commander_candidate_symbol": commander_candidate,
            "commander_selected_symbol": commander_selected,
            "executed_symbol": executed,
            "raw_to_post_changed": raw_to_post,
            "post_to_selected_changed": post_to_selected,
            "selected_to_monitor_changed": selected_to_monitor,
            "monitor_to_commander_changed": monitor_to_commander,
            "final_to_executed_changed": final_to_executed,
            "commander_authority_scope": str(commander.get("authority_scope") or ""),
            "commander_decision": str(commander.get("decision") or ""),
            "selection_mismatch": facade._mapping(selection.get("selection_mismatch")),
        }
        rows.append(row)
        for key in (
            "raw_to_post_changed",
            "post_to_selected_changed",
            "selected_to_monitor_changed",
            "monitor_to_commander_changed",
            "final_to_executed_changed",
        ):
            value = row[key]
            counters[f"{key}:unavailable" if value is None else f"{key}:{bool(value)}"] += 1

    return {
        "schema_version": "selection_authority_audit.v1",
        "behavior_effect": "observation_only",
        "trade_count": len(rows),
        "summary": dict(counters),
        "interpretation": {
            "commander_scope": "final approval/veto unless symbol deltas prove otherwise",
            "strategist_scope": "post-strategy scanner/ranking state, not pure LLM stock picker by default",
        },
        "rows": rows,
    }
