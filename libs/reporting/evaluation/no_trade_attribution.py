from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping
import sys

from libs.reporting.json_array_stream import iter_json_array
from libs.reporting.evaluation.artifact_inventory import (
    is_regular_session_evaluation_row,
    is_synthetic_evaluation_row,
)
from . import no_trade_attribution_mapping as _a49_no__mapping
from . import no_trade_attribution_num as _a49_no__num
from . import no_trade_attribution_pct as _a49_no__pct
from . import no_trade_attribution_top as _a49_no__top
from . import no_trade_attribution_q9_window_view as _a49_no__q9_window_view
from . import no_trade_attribution_render as _a54_nt_render
from . import no_trade_attribution_baseline_samsung as _a54_nt_baseline_samsung
from . import no_trade_attribution_q12_btc_woori as _a54_nt_q12_btc_woori
from . import no_trade_attribution_q9_windows as _a54_nt_q9_windows
from . import no_trade_attribution_q11_opening as _a54_nt_q11_opening


def _read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        return payload if isinstance(payload, dict) else {}
    except Exception:
        return {}


def _mapping(value: Any) -> Mapping[str, Any]:
    return _a49_no__mapping._mapping(value, facade=sys.modules[__name__])


def _num(value: Any) -> float | None:
    return _a49_no__num._num(value, facade=sys.modules[__name__])


def _pct(value: Any) -> str:
    return _a49_no__pct._pct(value, facade=sys.modules[__name__])


def _top(counter: Counter[str], limit: int = 10) -> list[dict[str, Any]]:
    return _a49_no__top._top(counter, limit, facade=sys.modules[__name__])


def _q9_window_view(row: Mapping[str, Any]) -> dict[str, Any]:
    """The only parts of a q9 window `build_no_trade_attribution_report` reads (non-mappings read as {})."""
    return _a49_no__q9_window_view._q9_window_view(row, facade=sys.modules[__name__])


def _q9_windows(reports_root: Path, day: str) -> list[dict[str, Any]]:
    return _a54_nt_q9_windows._q9_windows(reports_root, day, facade=sys.modules[__name__])


def _baseline_samsung(reports_root: Path, day: str) -> dict[str, Any]:
    return _a54_nt_baseline_samsung._baseline_samsung(reports_root, day, facade=sys.modules[__name__])


def _q11_opening(reports_root: Path, day: str) -> dict[str, Any]:
    return _a54_nt_q11_opening._q11_opening(reports_root, day, facade=sys.modules[__name__])


def _q12_btc_woori(reports_root: Path, day: str) -> dict[str, Any]:
    return _a54_nt_q12_btc_woori._q12_btc_woori(reports_root, day, facade=sys.modules[__name__])


def build_no_trade_attribution_report(
    *,
    day: str,
    reports_root: Path,
    trade_count: int,
) -> dict[str, Any]:
    reports_root = Path(reports_root)
    windows = _q9_windows(reports_root, day)
    commander_decisions: Counter[str] = Counter()
    commander_reasons: Counter[str] = Counter()
    commander_details: Counter[str] = Counter()
    monitor_intents: Counter[str] = Counter()
    monitor_noop_reasons: Counter[str] = Counter()
    scanner_top1: Counter[str] = Counter()
    strategist_selected: Counter[str] = Counter()
    commander_selected: Counter[str] = Counter()
    approve_noop = 0
    approve_buy = 0
    for window in windows:
        scanner = _mapping(window.get("scanner_control"))
        strategist = _mapping(window.get("strategist_selection"))
        commander = _mapping(window.get("commander_final"))
        if scanner.get("top1_symbol"):
            scanner_top1[str(scanner.get("top1_symbol"))] += 1
        if strategist.get("selected_symbol"):
            strategist_selected[str(strategist.get("selected_symbol"))] += 1
        if commander.get("selected_symbol"):
            commander_selected[str(commander.get("selected_symbol"))] += 1
        decision = str(commander.get("decision") or "")
        intent = str(commander.get("monitor_intent") or "")
        commander_decisions[decision] += 1
        commander_reasons[str(commander.get("reason") or "")] += 1
        detail = str(commander.get("detail") or "")
        if detail:
            commander_details[detail[:160]] += 1
        monitor_intents[intent] += 1
        monitor_observation = _mapping(commander.get("monitor_observation"))
        monitor_reason = str(
            commander.get("monitor_reason")
            or monitor_observation.get("reason")
            or ""
        )
        if intent == "NOOP" and monitor_reason:
            monitor_noop_reasons[monitor_reason] += 1
        if decision == "approve" and intent == "NOOP":
            approve_noop += 1
        if decision == "approve" and intent == "BUY":
            approve_buy += 1

    q11 = _q11_opening(reports_root, day)
    no_trade_class = "NOT_NO_TRADE_DAY"
    primary_issue = ""
    if trade_count <= 0:
        if not windows:
            no_trade_class = "MISSING_Q9_EVIDENCE"
            primary_issue = "q9_windows_missing"
        elif approve_noop > 0:
            q11_avg_net = _num(q11.get("avg_net_return_pct"))
            if int(q11.get("virtual_trades") or 0) > 0 and (
                q11_avg_net is not None and q11_avg_net > 0
            ):
                no_trade_class = "POSSIBLE_OVER_FILTERING"
                primary_issue = "positive_net_shadow_blocked_after_commander_approval"
            else:
                no_trade_class = "FILTERING_REVIEW_REQUIRED"
                primary_issue = (
                    "commander_approved_monitor_noop_requires_forward_review"
                )
        elif commander_decisions.get("reject", 0) > 0:
            no_trade_class = "UPSTREAM_REJECTED"
            primary_issue = "commander_rejected_candidates"
        else:
            no_trade_class = "NO_ACTIONABLE_CANDIDATE"
            primary_issue = "no_commander_approved_candidate"

    shadow_opportunity = "UNAVAILABLE"
    if q11.get("available"):
        virtual_trades = int(q11.get("virtual_trades") or 0)
        avg_net = _num(q11.get("avg_net_return_pct"))
        avg_mfe = _num(q11.get("avg_mfe_pct"))
        if virtual_trades <= 0:
            shadow_opportunity = "NO_SHADOW_TRADES"
        elif avg_net is not None and avg_net > 0:
            shadow_opportunity = "POSITIVE_NET_SHADOW"
        elif avg_mfe is not None and avg_mfe > 0:
            shadow_opportunity = "MFE_ONLY_SHADOW"
        else:
            shadow_opportunity = "NEGATIVE_SHADOW"

    return {
        "schema_version": "no_trade_attribution_report.v1",
        "behavior_effect": "observation_only",
        "day": day,
        "trade_count": int(trade_count),
        "q9_window_count": int(len(windows)),
        "no_trade_class": no_trade_class,
        "primary_issue": primary_issue,
        "commander_approve_monitor_noop_count": int(approve_noop),
        "commander_approve_monitor_buy_count": int(approve_buy),
        "commander_decisions": _top(commander_decisions),
        "commander_reasons": _top(commander_reasons),
        "commander_details": _top(commander_details),
        "monitor_intents": _top(monitor_intents),
        "monitor_noop_reasons": _top(monitor_noop_reasons),
        "scanner_top1": _top(scanner_top1),
        "strategist_selected": _top(strategist_selected),
        "commander_selected": _top(commander_selected),
        "shadow_opportunity_status": shadow_opportunity,
        "q10_samsung_hynix": _baseline_samsung(reports_root, day),
        "q11_opening_opportunity": q11,
        "q12_btc_woori": _q12_btc_woori(reports_root, day),
        "interpretation": {
            "scope": "Explains no-trade or sparse-trade days without changing execution behavior.",
            "q13_q14_boundary": "If trade_count is zero, Q13/Q14 trade attribution remains insufficient; use this report for over-filtering and missed-opportunity validation.",
        },
    }


def render_no_trade_attribution_report(payload: Mapping[str, Any]) -> str:
    return _a54_nt_render.render_no_trade_attribution_report(payload, facade=sys.modules[__name__])
