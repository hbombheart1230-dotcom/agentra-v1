"""episode_scanner_review: ``build_episode_scanner_review`` body (moved verbatim from ``episode_scanner_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence


def build_episode_scanner_review(
    payloads: list[dict[str, Any]],
    *,
    mock_drag_pct: float,
    live_drag_pct: float,
    episode_gap_sec: int = 900,
    prepared_rows: Sequence[Mapping[str, Any]] | None = None,
    facade: Any,
) -> dict[str, Any]:
    rows = (
        [dict(row) for row in prepared_rows]
        if prepared_rows is not None
        else facade.pre_strategist_candidate_rows(payloads)
    )
    episodes = facade._episode_representatives(rows, episode_gap_sec=episode_gap_sec)
    output: list[dict[str, Any]] = []
    for bucket in facade.RANK_BUCKETS:
        bucket_rows = [row for row in episodes if row["rank_bucket"] == bucket]
        for horizon in facade.SCANNER_HORIZONS:
            gross = [
                float(row["returns"][horizon])
                for row in bucket_rows
                if row["returns"].get(horizon) is not None
            ]
            output.append(
                {
                    "rank_bucket": bucket,
                    "horizon": horizon,
                    "episode_count": len(bucket_rows),
                    "observed_count": len(gross),
                    "observed_day_count": len(
                        {
                            row["day"]
                            for row in bucket_rows
                            if row["returns"].get(horizon) is not None
                        }
                    ),
                    "gross": facade.performance_metrics(gross),
                    "live_net": facade.performance_metrics(
                        [value - float(live_drag_pct) for value in gross]
                    ),
                    "mock_net": facade.performance_metrics(
                        [value - float(mock_drag_pct) for value in gross]
                    ),
                }
            )

    observed_30m_episodes = [
        row for row in episodes if row["returns"].get("+30m") is not None
    ]
    component_covered = [
        row for row in observed_30m_episodes if row.get("score_breakdown")
    ]
    component_values: dict[str, list[tuple[float, float, str]]] = facade.defaultdict(list)
    for row in component_covered:
        outcome = float(row["returns"]["+30m"])
        for key, raw in row["score_breakdown"].items():
            value = facade._number(raw)
            if value is not None:
                component_values[str(key)].append((value, outcome, row["day"]))

    component_rows: list[dict[str, Any]] = []
    for component, values in component_values.items():
        xs = [value for value, _, _ in values]
        ys = [outcome for _, outcome, _ in values]
        x_mean = sum(xs) / len(xs)
        y_mean = sum(ys) / len(ys)
        covariance = sum(
            (value - x_mean) * (outcome - y_mean)
            for value, outcome, _ in values
        )
        x_scale = facade.sqrt(sum((value - x_mean) ** 2 for value in xs))
        y_scale = facade.sqrt(sum((outcome - y_mean) ** 2 for outcome in ys))
        correlation = covariance / (x_scale * y_scale) if x_scale and y_scale else None
        component_rows.append(
            {
                "component": component,
                "observed_count": len(values),
                "observed_day_count": len({day for _, _, day in values}),
                "avg_score_contribution": round(x_mean, 6),
                "avg_gross_return_30m_pct": round(y_mean, 4),
                "avg_live_net_return_30m_pct": round(
                    y_mean - float(live_drag_pct), 4
                ),
                "score_return_correlation": (
                    round(correlation, 4) if correlation is not None else None
                ),
            }
        )
    component_rows.sort(
        key=lambda row: (
            int(row["observed_count"]),
            abs(float(row["score_return_correlation"] or 0.0)),
        ),
        reverse=True,
    )
    component_coverage = (
        len(component_covered) / len(observed_30m_episodes)
        if observed_30m_episodes
        else 0.0
    )
    rank1_30m = next(
        (
            row
            for row in output
            if row["rank_bucket"] == "rank1" and row["horizon"] == "+30m"
        ),
        {},
    )
    rank23_30m = next(
        (
            row
            for row in output
            if row["rank_bucket"] == "rank2_3" and row["horizon"] == "+30m"
        ),
        {},
    )
    rank1_value = facade._number(facade._mapping(rank1_30m.get("gross")).get("expectancy_pct"))
    rank23_value = facade._number(facade._mapping(rank23_30m.get("gross")).get("expectancy_pct"))
    return {
        "schema_version": "episode_scanner_review.v1",
        "behavior_effect": "evaluation_only",
        "episode_gap_sec": int(episode_gap_sec),
        "raw_candidate_row_count": len(rows),
        "episode_count": len(episodes),
        "compression_ratio": round(len(episodes) / len(rows), 4) if rows else 0.0,
        "cost_drag_pct": {
            "mock": round(float(mock_drag_pct), 6),
            "live": round(float(live_drag_pct), 6),
        },
        "rank_horizon_rows": output,
        "score_component_review": {
            "status": (
                "READY"
                if len(component_covered) >= 20 and component_coverage >= 0.70
                else "NOT_READY_MISSING_SCORE_COMPONENT_ARTIFACT"
            ),
            "forward_observed_episode_count": len(observed_30m_episodes),
            "component_covered_episode_count": len(component_covered),
            "coverage": round(component_coverage, 4),
            "rows": component_rows,
        },
        "rank1_minus_rank2_3_gross_30m_pct": (
            round(rank1_value - rank23_value, 4)
            if rank1_value is not None and rank23_value is not None
            else None
        ),
        "episodes": episodes,
        "limitations": [
            "An episode is the first observation after a 15-minute same-symbol/setup gap.",
            "Episodes reduce serial duplication but are not randomized independent trades.",
            "This report does not change Scanner ranking or execution.",
        ],
    }
