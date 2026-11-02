"""no_trade_attribution: ``_q9_window_view`` body (moved verbatim from ``no_trade_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _q9_window_view(row: Mapping[str, Any], *, facade: Any) -> dict[str, Any]:
    """The only parts of a q9 window `build_no_trade_attribution_report` reads (non-mappings read as {})."""
    view: dict[str, Any] = {}
    scanner = row.get("scanner_control")
    if isinstance(scanner, facade.Mapping):
        view["scanner_control"] = {"top1_symbol": scanner.get("top1_symbol")}
    strategist = row.get("strategist_selection")
    if isinstance(strategist, facade.Mapping):
        view["strategist_selection"] = {"selected_symbol": strategist.get("selected_symbol")}
    commander = row.get("commander_final")
    if isinstance(commander, facade.Mapping):
        observation = commander.get("monitor_observation")
        view["commander_final"] = {
            key: commander.get(key)
            for key in ("selected_symbol", "decision", "monitor_intent", "reason", "detail", "monitor_reason")
        }
        if isinstance(observation, facade.Mapping):
            view["commander_final"]["monitor_observation"] = {"reason": observation.get("reason")}
    return view
