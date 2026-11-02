"""no_trade_attribution: ``_q11_opening`` body (moved verbatim from ``no_trade_attribution``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any


def _q11_opening(reports_root: Path, day: str, *, facade: Any) -> dict[str, Any]:
    root = reports_root / "evaluation" / "opportunity_engine_shadow" / day
    payload = facade._read_json(root / "opportunity_engine_daily_report.json")
    signals = facade._read_json(root / "opportunity_engine_signals.json")
    virtual = facade._read_json(root / "opportunity_engine_virtual_trades.json")
    summary = facade._mapping(virtual.get("summary") or payload.get("summary"))
    data_quality = facade._mapping(signals.get("data_quality"))
    return {
        "available": bool(payload or signals or virtual),
        "signal_rows": int(signals.get("signal_count") or summary.get("signal_rows") or payload.get("signal_rows") or 0),
        "probe_candidates": sum(
            1
            for row in signals.get("signals") or []
            if isinstance(row, facade.Mapping) and bool(facade._mapping(row.get("opportunity")).get("probe_candidate"))
        ),
        "probe_near_misses": int(data_quality.get("probe_near_miss_count") or 0),
        "virtual_trades": int(virtual.get("trade_count") or summary.get("trade_count") or summary.get("virtual_trades") or 0),
        "win_rate": facade._num(summary.get("win_rate") or payload.get("win_rate")),
        "avg_net_return_pct": facade._num(summary.get("average_net_return_pct") or summary.get("avg_net_return") or summary.get("avg_net_return_pct") or payload.get("avg_net_return_pct")),
        "avg_mfe_pct": facade._num(summary.get("average_mfe_pct") or summary.get("avg_mfe") or summary.get("avg_mfe_pct") or payload.get("avg_mfe_pct")),
        "avg_mae_pct": facade._num(summary.get("average_mae_pct") or summary.get("avg_mae") or summary.get("avg_mae_pct") or payload.get("avg_mae_pct")),
        "profit_factor": facade._num(summary.get("profit_factor") or payload.get("profit_factor")),
    }
