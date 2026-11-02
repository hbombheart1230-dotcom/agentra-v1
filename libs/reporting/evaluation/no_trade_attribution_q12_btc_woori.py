"""no_trade_attribution: ``_q12_btc_woori`` body (moved verbatim from ``no_trade_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _q12_btc_woori(reports_root: Path, day: str, *, facade: Any) -> dict[str, Any]:
    payload = facade._read_json(
        reports_root
        / "evaluation"
        / "baseline_btc_woori_tech"
        / day
        / "baseline_btc_woori_forward_returns.json"
    )
    summary = facade._mapping(payload.get("summary"))
    horizons = summary.get("horizons") if isinstance(summary.get("horizons"), list) else []
    return {
        "available": bool(payload),
        "horizons": [
            {
                "horizon": str(row.get("horizon") or ""),
                "trade_count": int(row.get("trade_count") or 0),
                "win_rate": facade._num(facade._mapping(row.get("eligible_entries_net")).get("win_rate") or facade._mapping(row.get("top1_net")).get("win_rate") or row.get("win_rate")),
                "avg_net_return_pct": facade._num(
                    facade._mapping(row.get("eligible_entries_net")).get("average_return_pct")
                    or facade._mapping(row.get("top1_net")).get("average_return_pct")
                    or row.get("avg_net_return_pct")
                ),
                "profit_factor": facade._num(facade._mapping(row.get("eligible_entries_net")).get("profit_factor") or facade._mapping(row.get("top1_net")).get("profit_factor") or row.get("profit_factor")),
            }
            for row in horizons
            if isinstance(row, facade.Mapping)
        ],
    }
