"""historical_prior: ``summarize_historical_prior`` body (moved verbatim from ``historical_prior``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def summarize_historical_prior(
    *,
    models: list[dict[str, Any]],
    evaluations: list[dict[str, Any]],
    attributions: list[dict[str, Any]],
    errors: list[dict[str, Any]],
    from_day: str,
    before_day: str,
    facade: Any,
) -> dict[str, Any]:
    eligible = [
        row for row in evaluations
        if bool((row.get("integrity") or {}).get("promotion_metric_eligible"))
    ]
    returns = [value for value in (facade._net_return(row) for row in eligible) if value is not None]
    all_returns = [value for value in (facade._net_return(row) for row in evaluations) if value is not None]
    integrity_counts = facade.Counter(str((row.get("integrity") or {}).get("status") or "unknown") for row in evaluations)
    watch_counts = facade.Counter(
        item
        for row in evaluations
        for item in list((row.get("integrity") or {}).get("watch_items") or [])
    )
    defect_counts = facade.Counter(
        item
        for row in evaluations
        for item in list((row.get("integrity") or {}).get("defects") or [])
    )
    rank_rows: list[tuple[str, float]] = []
    playbook_rows: list[tuple[str, float]] = []
    symbol_rows: list[tuple[str, float]] = []
    horizon_bucket_rows: list[tuple[str, float]] = []
    source_days = sorted({str(row.get("day") or "") for row in evaluations if str(row.get("day") or "")})
    for model, evaluation in zip(models, evaluations):
        value = facade._net_return(evaluation)
        if value is None:
            continue
        selection = model.get("selection") if isinstance(model.get("selection"), dict) else {}
        horizon = evaluation.get("horizon_alignment") if isinstance(evaluation.get("horizon_alignment"), dict) else {}
        rank_rows.append((facade._rank_bucket(selection.get("selected_rank")), value))
        playbook_rows.append((selection.get("strategist_playbook") or "unknown", value))
        symbol_rows.append((model.get("symbol") or "unknown", value))
        horizon_bucket_rows.append((horizon.get("bucket") or "unknown", value))
    comparable_attributions = [
        row for row in attributions
        if (row.get("deltas") or {}).get("strategist_delta_pct") is not None
    ]
    return {
        "schema_version": "historical_q9_prior_summary.v1",
        "behavior_effect": "read_only_historical_prior",
        "generated_at": facade.datetime.now(facade.timezone.utc).isoformat(),
        "scope": {
            "from_day": from_day,
            "before_day": before_day,
            "source": "reports/trades lifecycle_bundle artifacts",
            "official_q9_freeze_sample": False,
            "usage": "prior_evidence_only",
        },
        "coverage": {
            "source_day_count": len(source_days),
            "source_days": source_days,
            "trade_count": len(evaluations),
            "eligible_trade_count": len(eligible),
            "build_error_count": len(errors),
            "integrity_status_counts": dict(integrity_counts),
            "top_watch_items": dict(watch_counts.most_common(20)),
            "top_defects": dict(defect_counts.most_common(20)),
        },
        "performance": {
            "eligible": facade.performance_metrics(returns),
            "all_realized": facade.performance_metrics(all_returns),
        },
        "breakdowns": {
            "selected_rank_bucket": facade._group_metrics(rank_rows),
            "strategist_playbook": facade._group_metrics(playbook_rows),
            "symbol": facade._group_metrics(symbol_rows),
            "horizon_bucket": facade._group_metrics(horizon_bucket_rows),
        },
        "selection_attribution": {
            "comparison_count": len(comparable_attributions),
            "unavailable_count": len(attributions) - len(comparable_attributions),
            "note": "Historical artifacts often lack Q9-native A/B/C forward controls; use as prior only.",
        },
        "interpretation_guardrails": [
            "Do not merge these rows into the frozen Q9 five-day validation sample.",
            "Do not promote a new tactic from historical_prior alone.",
            "Use this report to decide whether Q9 freeze findings agree with older evidence.",
        ],
        "errors": errors[:50],
    }
