"""quant_tactic_report projections (moved verbatim from quant_tactic_report).

Module globals and helpers are resolved on ``facade`` (the quant_tactic_report module) at call time; this module never imports it.
"""
from __future__ import annotations

from typing import Any, List, Mapping


def _tactic_sources(
    *,
    entry_decision: Mapping[str, Any],
    factor_snapshot: Mapping[str, Any],
    selected_row: Mapping[str, Any],
    tactic_suitability: Mapping[str, Any],
    exit_decision: Mapping[str, Any],
    facade: Any,
) -> List[tuple[str, str]]:
    selected_factor = facade._mapping(selected_row.get("quant_factor_snapshot"))
    rows = (
        ("entry_quant_decision", entry_decision.get("tactic_id")),
        ("factor_snapshot", factor_snapshot.get("tactic_id")),
        ("selected_quant_factor_snapshot", selected_factor.get("tactic_id")),
        ("selected_candidate", selected_row.get("tactical_strategy")),
        ("tactic_suitability", tactic_suitability.get("tactic_id")),
        ("exit_quant_decision", exit_decision.get("tactic_id")),
    )
    return [(source, tactic_id) for source, value in rows if (tactic_id := facade._tactic_value(value))]
