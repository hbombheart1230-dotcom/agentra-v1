"""cost_basis_comparison: ``build_evaluation_cost_bases`` body (moved verbatim from ``cost_basis_comparison``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def build_evaluation_cost_bases(
    profile: Mapping[str, Any] | None,
    *,
    slippage_pct: float,
    facade: Any,
) -> dict[str, Any]:
    observed = dict(profile or {})
    mock_ratio = float(
        observed.get("conservative_round_trip_cost_pct")
        or observed.get("ema_round_trip_cost_pct")
        or 0.009
    )
    live_ratio = facade.LIVE_BUY_FEE_RATE + facade.LIVE_SELL_FEE_RATE + facade.LIVE_EQUITY_SELL_TAX_RATE_2026
    return {
        "schema_version": "evaluation_cost_bases.v1",
        "primary_interpretation": "show_both_no_automatic_policy_change",
        "slippage_pct": round(float(slippage_pct), 6),
        "mock_observed": {
            "purpose": "mock_broker_pnl_and_mock_cash_truth",
            "source": str(observed.get("source") or "fallback"),
            "sample_count": int(observed.get("sample_count") or 0),
            "round_trip_cost_pct": facade._pct(mock_ratio),
            "total_drag_with_slippage_pct": round(facade._pct(mock_ratio) + float(slippage_pct), 6),
        },
        "live_deployment_equity": {
            "purpose": "real_account_strategy_evaluation",
            "source": "kiwoom_openapi_standard_equity_assumption_2026",
            "buy_fee_pct": facade._pct(facade.LIVE_BUY_FEE_RATE),
            "sell_fee_pct": facade._pct(facade.LIVE_SELL_FEE_RATE),
            "sell_tax_pct": facade._pct(facade.LIVE_EQUITY_SELL_TAX_RATE_2026),
            "round_trip_cost_pct": facade._pct(live_ratio),
            "total_drag_with_slippage_pct": round(facade._pct(live_ratio) + float(slippage_pct), 6),
            "scope": "KRX listed equities; ETF/ETN tax treatment must be resolved by instrument type",
        },
    }
