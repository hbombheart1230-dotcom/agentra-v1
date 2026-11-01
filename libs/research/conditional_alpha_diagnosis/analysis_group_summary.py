from typing import Any


def _group_summary(rows: list[dict[str, Any]], field: str, *, facade: Any) -> dict[str, Any]:
    metrics = facade.performance(row.get(field) for row in rows)
    profile = facade.evidence_profile(rows)
    values = sorted([value for row in rows if (value := facade.number(row.get(field))) is not None], reverse=True)
    without_top3 = values[3:] if len(values) > 3 else []
    positive_sum = sum(value for value in values if value > 0)
    top3_positive = sum(value for value in values[:3] if value > 0)
    return {**metrics, **profile, "positive_day_rate": facade.positive_day_rate(rows, field),
            "average_without_top3_pct": round(sum(without_top3) / len(without_top3), 4) if without_top3 else None,
            "top3_positive_profit_share": round(top3_positive / positive_sum, 4) if positive_sum else None,
            "evidence_status": facade.evidence_status(metrics, profile)}
