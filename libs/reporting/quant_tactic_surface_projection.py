"""quant_tactic_report projections (moved verbatim from quant_tactic_report).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_report module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, Dict, Mapping


def quant_tactic_surface(report: Mapping[str, Any] | None, *, facade: Any) -> Dict[str, Any]:
    root = facade._mapping(report)
    monitor = facade._monitor(root)
    visibility = facade._entry_visibility(root)
    symbol = facade._symbol(root)
    selection = facade._mapping(root.get("why_this_symbol_was_chosen"))
    scanner_trace = facade._mapping(selection.get("scanner_selection_trace"))
    selected_row = facade._selected_candidate_row(root, symbol)
    entry_decision = facade._mapping(
        monitor.get("entry_quant_decision")
        or root.get("entry_quant_decision")
        or facade._first_nested_mapping(root, "entry_quant_decision")
    )
    exit_decision = facade._mapping(monitor.get("exit_quant_decision") or root.get("exit_quant_decision"))
    factor_snapshot = facade._mapping(
        monitor.get("quant_factor_snapshot")
        or root.get("quant_factor_snapshot")
        or selected_row.get("quant_factor_snapshot")
    )
    factors = facade._mapping(factor_snapshot.get("factors"))
    tactic_suitability = facade._mapping(
        selection.get("tactic_suitability")
        or scanner_trace.get("tactic_suitability")
        or selected_row.get("tactic_suitability")
        or entry_decision.get("tactic_suitability")
    )
    tactic_sources = facade._tactic_sources(
        entry_decision=entry_decision,
        factor_snapshot=factor_snapshot,
        selected_row=selected_row,
        tactic_suitability=tactic_suitability,
        exit_decision=exit_decision,
    )
    tactic_id_source, tactic_id = tactic_sources[0] if tactic_sources else ("", "")
    playbook = str(entry_decision.get("playbook") or exit_decision.get("playbook") or factor_snapshot.get("playbook") or facade._playbook(root)).strip()
    if not tactic_suitability and selected_row:
        tactic_suitability = facade.score_candidate_tactic_suitability(selected_row, tactic_id=tactic_id, playbook=playbook)
    if not entry_decision:
        entry_info = facade._entry_info_from_visibility(visibility, monitor)
        if entry_info or selected_row or factor_snapshot:
            entry_decision = facade.build_entry_quant_decision(
                entry_info,
                selected=selected_row,
                factor_snapshot=factor_snapshot,
                state=root,
                tactic_id=tactic_id,
                playbook=playbook,
            )
    scanner_chart_fit = facade._mapping(selection.get("scanner_chart_fit")) or facade._mapping(scanner_trace.get("scanner_chart_fit")) or facade._scanner_chart_fit_from_row(selected_row)
    if not any((entry_decision, exit_decision, factor_snapshot, tactic_suitability, tactic_id, scanner_chart_fit)):
        return {}
    return {
        "schema_version": "quant_tactic_report_surface.v1",
        "tactic_id": tactic_id,
        "tactic_id_source": tactic_id_source,
        "tactic_id_mismatches": facade._tactic_mismatches(tactic_sources, tactic_id),
        "exit_tactic_drifts": facade._exit_tactic_drifts(tactic_sources, tactic_id),
        "playbook": playbook,
        "entry_quant_decision": entry_decision,
        "exit_quant_decision": exit_decision,
        "factor_snapshot": factor_snapshot,
        "factors": factors,
        "tactic_suitability": tactic_suitability,
        "scanner_chart_fit": scanner_chart_fit,
    }
