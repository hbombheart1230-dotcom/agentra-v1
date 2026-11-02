"""entry_timing_attribution: ``_label`` body (moved verbatim from ``entry_timing_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence


def _label(
    *,
    scanner_to_entry_delay_sec: int | None,
    pre_entry_move_pct: float | None,
    forward: Mapping[str, Any],
    strategy_horizon: str = "",
    facade: Any,
) -> tuple[str, list[str]]:
    cp5 = facade._checkpoint(forward, "+5m")
    cp15 = facade._checkpoint(forward, "+15m")
    cp30 = facade._checkpoint(forward, "+30m")
    ret5 = facade._num(cp5.get("return_pct"))
    mfe5 = facade._num(cp5.get("mfe_pct"))
    mae5 = facade._num(cp5.get("mae_pct"))
    ret15 = facade._num(cp15.get("return_pct"))
    normalized_horizon = str(strategy_horizon or "").strip().lower()
    if normalized_horizon in {"swing", "overnight", "position", "1-2day", "1_2day"}:
        return "INSUFFICIENT_EVIDENCE", ["strategy_horizon_exceeds_entry_timing_observation_window"]
    if normalized_horizon == "intraday":
        ret30 = facade._num(cp30.get("return_pct"))
        mfe15 = facade._num(cp15.get("mfe_pct"))
        mae15 = facade._num(cp15.get("mae_pct"))
        if ret15 is None or ret30 is None or mfe15 is None or mae15 is None:
            return "INSUFFICIENT_EVIDENCE", ["missing_intraday_forward_quality"]
        reasons: list[str] = []
        if pre_entry_move_pct is not None and pre_entry_move_pct >= 0.35 and ret15 <= 0.0 and ret30 <= 0.0:
            return "ENTRY_TOO_LATE", ["pre_entry_move>=0.35pct_then_intraday_forward_weak"]
        if mae15 <= -0.75 and ret15 < 0.0 and (pre_entry_move_pct is None or pre_entry_move_pct < 0.20):
            return "ENTRY_TOO_EARLY", ["intraday_adverse_move_without_prior_alpha"]
        if ret15 > 0.0 or ret30 > 0.0 or mfe15 >= 0.70:
            return "ENTRY_APPROPRIATE", ["favorable_intraday_forward_response"]
        return "INSUFFICIENT_EVIDENCE", ["intraday_forward_weak_but_not_classifiable"]
    if ret5 is None or mfe5 is None or mae5 is None:
        return "INSUFFICIENT_EVIDENCE", ["missing_5m_forward_quality"]
    reasons: list[str] = []
    if scanner_to_entry_delay_sec is not None and scanner_to_entry_delay_sec >= 180:
        reasons.append("scanner_to_entry_delay>=180s")
    if pre_entry_move_pct is not None and pre_entry_move_pct >= 0.35 and (ret5 <= 0.0 or (ret15 is not None and ret15 <= 0.0)):
        reasons.append("pre_entry_move>=0.35pct_then_forward_weak")
        return "ENTRY_TOO_LATE", reasons
    if mae5 <= -0.55 and ret5 < 0.0 and (pre_entry_move_pct is None or pre_entry_move_pct < 0.20):
        reasons.append("immediate_adverse_move_without_prior_alpha")
        return "ENTRY_TOO_EARLY", reasons
    if ret5 > 0.0 or (ret15 is not None and ret15 > 0.0) or mfe5 >= 0.50:
        reasons.append("favorable_forward_response")
        return "ENTRY_APPROPRIATE", reasons
    reasons.append("forward_weak_but_not_classifiable")
    return "INSUFFICIENT_EVIDENCE", reasons
