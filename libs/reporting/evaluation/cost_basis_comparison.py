from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping
import sys

from libs.reporting.quant_shadow_candidate_evaluation import (
    Q9_ROW_KEYS_UNUSED_BY_FULL_CHAIN,
    load_quant_shadow_candidate_payloads_for_range,
)
from libs.reporting.q9_forward_candles import (
    FORWARD_DATA_SOURCE,
    load_q9_forward_candles,
)
from libs.runtime.broker_cost_profile import load_broker_cost_profile

from .scanner_quality import (
    build_scanner_quality_review,
    extract_pre_strategist_candidate_rows,
)
from . import cost_basis_comparison_topk_rows as _a45_topk_rows
from . import cost_basis_comparison_pct as _a46_pct
from . import cost_basis_comparison_build_evaluation_cost_bases as _a46_build_evaluation_cost_bases
from . import cost_basis_comparison_render_cost_basis_comparison as _a46_render_cost_basis_comparison


DEFAULT_EVALUATION_SLIPPAGE_PCT = 0.05
LIVE_BUY_FEE_RATE = 0.00015
LIVE_SELL_FEE_RATE = 0.00015
LIVE_EQUITY_SELL_TAX_RATE_2026 = 0.002


def _pct(value: float) -> float:
    return _a46_pct._pct(value, facade=sys.modules[__name__])


def build_evaluation_cost_bases(
    profile: Mapping[str, Any] | None,
    *,
    slippage_pct: float = DEFAULT_EVALUATION_SLIPPAGE_PCT,
) -> dict[str, Any]:
    return _a46_build_evaluation_cost_bases.build_evaluation_cost_bases(profile, slippage_pct=slippage_pct, facade=sys.modules[__name__])


def _topk_rows(review: Mapping[str, Any]) -> dict[tuple[int, str], dict[str, Any]]:
    return _a45_topk_rows._topk_rows(review, facade=sys.modules[__name__])


def build_cost_basis_comparison(
    *,
    reports_root: Path,
    start: str,
    end: str,
    cost_profile_path: Path | None = None,
    slippage_pct: float = DEFAULT_EVALUATION_SLIPPAGE_PCT,
) -> dict[str, Any]:
    payloads = load_quant_shadow_candidate_payloads_for_range(
        reports_root=Path(reports_root),
        start=start,
        end=end,
        drop_q9_row_keys=Q9_ROW_KEYS_UNUSED_BY_FULL_CHAIN,  # only pre-strategist rows' forward outcomes are read
    )
    profile = load_broker_cost_profile(cost_profile_path)
    bases = build_evaluation_cost_bases(profile, slippage_pct=slippage_pct)
    pre_strategist_rows = extract_pre_strategist_candidate_rows(payloads)
    forward_candles = load_q9_forward_candles(
        pre_strategist_rows,
        allow_fresh_fetch=start[:10] == end[:10],
        run_id_prefix="q9_cost_basis_forward_recovery",
    )
    mock_cost = float(bases["mock_observed"]["round_trip_cost_pct"])
    live_cost = float(bases["live_deployment_equity"]["round_trip_cost_pct"])
    mock_review = build_scanner_quality_review(
        payloads,
        cost_pct=mock_cost,
        slippage_pct=slippage_pct,
        minute_rows_by_symbol=forward_candles,
    )
    live_review = build_scanner_quality_review(
        payloads,
        cost_pct=live_cost,
        slippage_pct=slippage_pct,
        minute_rows_by_symbol=forward_candles,
    )
    mock_rows = _topk_rows(mock_review)
    live_rows = _topk_rows(live_review)
    rows: list[dict[str, Any]] = []
    for key in sorted(mock_rows, key=lambda item: (item[1], item[0])):
        mock_row = mock_rows[key]
        live_row = live_rows.get(key, {})
        gross = mock_row.get("gross") if isinstance(mock_row.get("gross"), Mapping) else {}
        mock_net = mock_row.get("net") if isinstance(mock_row.get("net"), Mapping) else {}
        live_net = live_row.get("net") if isinstance(live_row.get("net"), Mapping) else {}
        rows.append({
            "top_k": key[0],
            "horizon": key[1],
            "window_count": int(mock_row.get("window_count") or 0),
            "observed_day_count": int(mock_row.get("observed_day_count") or 0),
            "gross": dict(gross),
            "mock_net": dict(mock_net),
            "live_net": dict(live_net),
            "expectancy_delta_live_minus_mock_pct": round(
                float(live_net.get("expectancy_pct") or 0.0)
                - float(mock_net.get("expectancy_pct") or 0.0),
                4,
            ),
        })
    return {
        "schema_version": "q9_cost_basis_comparison.v1",
        "behavior_effect": "evaluation_only",
        "cohort_scope": "all_pre_strategist_windows_with_observed_horizon",
        "forward_data_source": FORWARD_DATA_SOURCE,
        "range": {"start": start[:10], "end": end[:10]},
        "cost_bases": bases,
        "pre_strategist_universe_available": bool(
            mock_review.get("pre_strategist_universe_available")
        ),
        "rows": rows,
        "interpretation": {
            "mock_net": "Can the signal overcome Kiwoom mock-account friction?",
            "live_net": "Could the signal overcome the stated real-account equity assumptions?",
            "policy_change_authorized": False,
        },
    }


def render_cost_basis_comparison(payload: Mapping[str, Any]) -> str:
    return _a46_render_cost_basis_comparison.render_cost_basis_comparison(payload, facade=sys.modules[__name__])


def write_cost_basis_comparison(
    *,
    reports_root: Path,
    start: str,
    end: str,
    output_dir: Path,
    cost_profile_path: Path | None = None,
) -> dict[str, str]:
    payload = build_cost_basis_comparison(
        reports_root=reports_root,
        start=start,
        end=end,
        cost_profile_path=cost_profile_path,
    )
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "cost_basis_comparison.json"
    markdown_path = output_dir / "cost_basis_comparison.md"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    markdown_path.write_text(render_cost_basis_comparison(payload), encoding="utf-8")
    return {"json": str(json_path), "markdown": str(markdown_path)}


__all__ = [
    "build_cost_basis_comparison",
    "build_evaluation_cost_bases",
    "render_cost_basis_comparison",
    "write_cost_basis_comparison",
]
