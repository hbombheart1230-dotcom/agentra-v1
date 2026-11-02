"""no_trade_attribution: ``_baseline_samsung`` body (moved verbatim from ``no_trade_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _baseline_samsung(reports_root: Path, day: str, *, facade: Any) -> dict[str, Any]:
    payload = facade._read_json(
        reports_root
        / "evaluation"
        / "baseline_samsung_hynix"
        / day
        / "baseline_samsung_hynix_forward_returns.json"
    )
    summary = facade._mapping(payload.get("summary"))
    rows = summary.get("horizons") if isinstance(summary.get("horizons"), list) else []
    return {
        "available": bool(payload),
        "horizons": [
            {
                "horizon": str(row.get("horizon") or ""),
                "trade_count": int(row.get("top1_observation_count") or row.get("trade_count") or 0),
                "win_rate": facade._num(facade._mapping(row.get("top1_net")).get("win_rate") or row.get("top1_win_rate") or row.get("win_rate")),
                "avg_net_return_pct": facade._num(
                    facade._mapping(row.get("top1_net")).get("average_return_pct")
                    or row.get("top1_avg_net_return_pct")
                    or row.get("avg_net_return_pct")
                ),
                "profit_factor": facade._num(facade._mapping(row.get("top1_net")).get("profit_factor") or row.get("top1_profit_factor") or row.get("profit_factor")),
            }
            for row in rows
            if isinstance(row, facade.Mapping)
        ],
    }
