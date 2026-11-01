"""RF-037 structural_alpha_batch2: episode projection Owner (bodies moved verbatim from ``strategies``).

``facade`` is the ``strategies`` module; ``_timestamps``, ``EPISODE_GAP_SEC``, ``MARKET_PROXY_SYMBOLS``,
``entry_bar``, ``_episode``, ``market_return_15m`` and ``relative_strength_features`` are resolved on it at call
time, so caller monkeypatching keeps working. This module never imports ``strategies``. Pure, no IO.
"""
from __future__ import annotations

from typing import Any, Callable, Mapping

FeatureBuilder = Callable[..., dict[str, Any]]


def _build_local_episodes(
    windows: list[Mapping[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
    strategy_id: str,
    feature_builder: FeatureBuilder,
    eligible: Callable[[Mapping[str, Any]], bool],
    selection_key: Callable[[Mapping[str, Any]], tuple[Any, ...]],
    facade: Any,
) -> list[dict[str, Any]]:
    episodes: list[dict[str, Any]] = []
    last_epoch = 0
    timestamps = facade._timestamps(minute_rows_by_symbol)
    for window in windows:
        epoch = int(window.get("decision_epoch") or 0)
        day = str(window.get("day") or "")
        if last_epoch and epoch - last_epoch < facade.EPISODE_GAP_SEC:
            continue
        candidates: list[dict[str, Any]] = []
        for candidate in window.get("candidates") or []:
            symbol = str(candidate.get("symbol") or "")
            features = feature_builder(
                minute_rows_by_symbol.get(symbol) or [],
                decision_epoch=epoch,
                day=day,
                timestamps=timestamps.get(symbol),
            )
            row = {"symbol": symbol, **features}
            if features.get("available") and eligible(row):
                candidates.append(row)
        if not candidates:
            continue
        selected = max(candidates, key=selection_key)
        symbol = str(selected["symbol"])
        bar = facade.entry_bar(
            minute_rows_by_symbol.get(symbol) or [],
            decision_epoch=epoch,
            day=day,
            timestamps=timestamps.get(symbol),
        )
        if not bar:
            continue
        episodes.append(
            facade._episode(
                strategy_id=strategy_id,
                window=window,
                symbol=symbol,
                bar=bar,
                features=selected,
                index=len(episodes) + 1,
            )
        )
        last_epoch = epoch
    return episodes


def build_market_shock_reversal_episodes(
    windows: list[Mapping[str, Any]],
    *,
    minute_rows_by_symbol: Mapping[str, list[Mapping[str, Any]]],
    facade: Any,
) -> list[dict[str, Any]]:
    episodes: list[dict[str, Any]] = []
    last_epoch = 0
    timestamps = facade._timestamps(minute_rows_by_symbol)
    for window in windows:
        epoch = int(window.get("decision_epoch") or 0)
        day = str(window.get("day") or "")
        if last_epoch and epoch - last_epoch < facade.EPISODE_GAP_SEC:
            continue
        market_returns = [
            value
            for symbol in facade.MARKET_PROXY_SYMBOLS
            if (
                value := facade.market_return_15m(
                    minute_rows_by_symbol.get(symbol) or [],
                    decision_epoch=epoch,
                    day=day,
                    timestamps=timestamps.get(symbol),
                )
            )
            is not None
        ]
        if not market_returns:
            continue
        market_return = sum(market_returns) / len(market_returns)
        if market_return > -0.75:
            continue
        candidates: list[dict[str, Any]] = []
        for candidate in window.get("candidates") or []:
            symbol = str(candidate.get("symbol") or "")
            features = facade.relative_strength_features(
                minute_rows_by_symbol.get(symbol) or [],
                decision_epoch=epoch,
                day=day,
                timestamps=timestamps.get(symbol),
            )
            candidate_return = float(features.get("return_5m_pct") or 0.0)
            volume_ratio = float(features.get("volume_ratio") or 0.0)
            if (
                features.get("available")
                and candidate_return > 0.0
                and features.get("above_vwap")
                and volume_ratio >= 1.2
            ):
                candidates.append(
                    {
                        "symbol": symbol,
                        **features,
                        "market_return_15m_pct": round(market_return, 6),
                        "relative_strength_pct": round(
                            candidate_return - market_return,
                            6,
                        ),
                    }
                )
        if not candidates:
            continue
        selected = max(
            candidates,
            key=lambda row: (
                float(row["relative_strength_pct"]),
                str(row["symbol"]),
            ),
        )
        symbol = str(selected["symbol"])
        bar = facade.entry_bar(
            minute_rows_by_symbol.get(symbol) or [],
            decision_epoch=epoch,
            day=day,
            timestamps=timestamps.get(symbol),
        )
        if not bar:
            continue
        episodes.append(
            facade._episode(
                strategy_id="H7_MARKET_SHOCK_RELATIVE_STRENGTH_REVERSAL",
                window=window,
                symbol=symbol,
                bar=bar,
                features=selected,
                index=len(episodes) + 1,
            )
        )
        last_epoch = epoch
    return episodes
