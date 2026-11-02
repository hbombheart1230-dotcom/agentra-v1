"""Pure stale-group aggregation owner for monitor gate diagnostics."""
from __future__ import annotations

from typing import Any, Dict, Iterable, List


def _build_stale_groups(rows: Iterable[Dict[str, Any]], *, stale_age_min: float = 3.0, facade: Any) -> List[Dict[str, Any]]:
    groups: Dict[tuple[str, str, Any], List[Dict[str, Any]]] = {}
    for row in rows:
        if not row.get("minute_source_present"):
            continue
        latest_candle_ts = row.get("latest_candle_ts")
        if latest_candle_ts in (None, ""):
            continue
        age = facade._to_float(row.get("artifact_age_minutes"))
        if age is None or age < stale_age_min:
            continue
        key = (str(row.get("symbol") or ""), str(row.get("evaluation_summary") or ""), latest_candle_ts)
        groups.setdefault(key, []).append(row)
    out: List[Dict[str, Any]] = []
    for (symbol, reason, latest_candle_ts), cases in groups.items():
        cases = sorted(cases, key=lambda row: str(row.get("ts") or ""))
        out.append(
            {
                "symbol": symbol,
                "evaluation_summary": reason,
                "latest_candle_ts": latest_candle_ts,
                "repeat_count": len(cases),
                "first_run_id": cases[0].get("run_id"),
                "last_run_id": cases[-1].get("run_id"),
                "max_artifact_age_minutes": max((facade._to_float(row.get("artifact_age_minutes")) or 0.0) for row in cases),
                "runs": [str(row.get("run_id") or "") for row in cases],
            }
        )
    out.sort(key=lambda row: (-int(row["repeat_count"]), row["symbol"], row["evaluation_summary"]))
    return out
