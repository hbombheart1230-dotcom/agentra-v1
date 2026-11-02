"""episode_scanner_review: ``_episode_representatives`` body (moved verbatim from ``episode_scanner_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence


def _episode_representatives(
    rows: Sequence[Mapping[str, Any]],
    *,
    episode_gap_sec: int,
    facade: Any,
) -> list[dict[str, Any]]:
    grouped: dict[tuple[str, str, str], list[Mapping[str, Any]]] = facade.defaultdict(list)
    for row in rows:
        day = facade._day(row)
        symbol = str(row.get("symbol") or "")
        if not day or not symbol:
            continue
        grouped[(day, symbol, facade._setup_key(row))].append(row)

    episodes: list[dict[str, Any]] = []
    for (day, symbol, setup), candidates in sorted(grouped.items()):
        previous_epoch: int | None = None
        episode_index = 0
        for row in sorted(candidates, key=lambda item: (facade._epoch(item), int(facade._number(item.get("rank")) or 999))):
            current_epoch = facade._epoch(row)
            if (
                previous_epoch is None
                or current_epoch <= 0
                or previous_epoch <= 0
                or current_epoch - previous_epoch > episode_gap_sec
            ):
                episode_index += 1
                rank = int(facade._number(row.get("rank")) or 0)
                episodes.append(
                    {
                        "episode_id": f"{day}:{symbol}:{setup}:{episode_index}",
                        "day": day,
                        "symbol": symbol,
                        "setup": setup,
                        "baseline_epoch": current_epoch or None,
                        "rank": rank or None,
                        "rank_bucket": facade._rank_bucket(rank),
                        "score_breakdown": dict(
                            facade._mapping(row.get("score_breakdown"))
                        ),
                        "sources": [
                            str(value)
                            for value in row.get("q9_candidate_sources")
                            or row.get("sources")
                            or []
                            if str(value)
                        ],
                        "returns": {
                            horizon: facade._checkpoint_return(row, horizon)
                            for horizon in facade.SCANNER_HORIZONS
                        },
                    }
                )
            previous_epoch = current_epoch
    return episodes
