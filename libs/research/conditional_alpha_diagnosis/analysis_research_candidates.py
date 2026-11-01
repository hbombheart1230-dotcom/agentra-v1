from typing import Any


def research_candidates(cross_sections: list[dict[str, Any]], *, facade: Any) -> list[dict[str, Any]]:
    candidates = []
    for row in cross_sections:
        number = facade.number
        if (not row.get("point_in_time_eligible") or row.get("value") == "MISSING" or row.get("evidence_status") != "SCREENABLE"
                or number(row.get("average_pct")) is None or number(row.get("average_pct")) <= 0
                or number(row.get("profit_factor")) is None or number(row.get("profit_factor")) <= 1
                or number(row.get("positive_day_rate")) is None or number(row.get("positive_day_rate")) < .5
                or number(row.get("average_without_top3_pct")) is None or number(row.get("average_without_top3_pct")) <= 0
                or (number(row.get("largest_day_share")) and number(row.get("largest_day_share")) > .4)
                or (number(row.get("largest_symbol_share")) and number(row.get("largest_symbol_share")) > .4)):
            continue
        candidates.append(dict(row))
    return sorted(candidates, key=lambda row: (facade.number(row.get("average_pct")) or -999, int(row.get("count") or 0)), reverse=True)
