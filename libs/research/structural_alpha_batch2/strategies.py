from __future__ import annotations

import sys
from typing import Any, Callable, Mapping

from libs.research.structural_alpha.features import (
    entry_bar,
    relative_strength_features,
)
from libs.research.structural_alpha.strategies import _episode

from . import strategy_episode_projection as _a24_owner
from .contracts import EPISODE_GAP_SEC, MARKET_PROXY_SYMBOLS
from .features import (
    market_return_15m,
    oversold_reversal_features,
    trend_pullback_features,
)


FeatureBuilder = Callable[..., dict[str, Any]]


def _timestamps(
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
) -> dict[str, list[int]]:
    return {
        symbol: [int(row.get("ts") or 0) for row in rows]
        for symbol, rows in minute_rows_by_symbol.items()
    }


def _build_local_episodes(
    windows: list[Mapping[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
    strategy_id: str,
    feature_builder: FeatureBuilder,
    eligible: Callable[[Mapping[str, Any]], bool],
    selection_key: Callable[[Mapping[str, Any]], tuple[Any, ...]],
) -> list[dict[str, Any]]:
    return _a24_owner._build_local_episodes(windows, minute_rows_by_symbol=minute_rows_by_symbol, strategy_id=strategy_id, feature_builder=feature_builder, eligible=eligible, selection_key=selection_key, facade=sys.modules[__name__])


def build_market_shock_reversal_episodes(
    windows: list[Mapping[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    return _a24_owner.build_market_shock_reversal_episodes(windows, minute_rows_by_symbol=minute_rows_by_symbol, facade=sys.modules[__name__])


def build_oversold_reversal_episodes(
    windows: list[Mapping[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    return _build_local_episodes(
        windows,
        minute_rows_by_symbol=minute_rows_by_symbol,
        strategy_id="H8_OVERSOLD_MEAN_REVERSION",
        feature_builder=oversold_reversal_features,
        eligible=lambda row: bool(
            row.get("oversold_ok")
            and row.get("reversal_ok")
            and row.get("volume_ok")
        ),
        selection_key=lambda row: (
            -float(row["rsi_14"]),
            float(row["rebound_1m_pct"]),
            str(row["symbol"]),
        ),
    )


def build_trend_pullback_episodes(
    windows: list[Mapping[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
) -> list[dict[str, Any]]:
    return _build_local_episodes(
        windows,
        minute_rows_by_symbol=minute_rows_by_symbol,
        strategy_id="H9_TREND_PULLBACK_RESUMPTION",
        feature_builder=trend_pullback_features,
        eligible=lambda row: bool(
            row.get("trend_ok")
            and row.get("pullback_reclaim_ok")
            and row.get("resume_ok")
        ),
        selection_key=lambda row: (
            float(row["trend_spread_pct"]),
            str(row["symbol"]),
        ),
    )
