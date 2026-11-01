"""operator_visibility: ``_build_trading_health_status`` body (moved verbatim from ``operator_visibility``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _build_trading_health_status(reports_root: Path, day: str, *, facade: Any) -> Dict[str, Any]:
    summary_path = facade.Path(reports_root) / "performance" / str(day or "").strip() / "summary.json"
    summary = facade._read_json(summary_path)
    sample_count = facade._safe_int(summary.get("return_sample_count"), 0)
    total_trades = facade._safe_int(summary.get("total_trades"), 0)
    win_rate = facade._safe_float(summary.get("win_rate"), 0.0)
    avg_return = facade._safe_float(summary.get("avg_return"), 0.0)
    profit_factor = facade._safe_float(summary.get("profit_factor"), 0.0)
    level = "GREEN"
    reasons: List[str] = []
    if not summary:
        level = "UNKNOWN"
        reasons.append("performance summary artifact is missing")
    elif sample_count <= 0:
        level = "UNKNOWN"
        reasons.append("no realized return samples; trading performance is not evaluable")
    elif sample_count >= 3 and (win_rate < 0.25 or avg_return <= -0.008):
        level = "RED"
        reasons.append(
            f"trade performance weak: sample={sample_count}, win_rate={win_rate:.2%}, avg_return={avg_return:.2%}"
        )
    elif avg_return < 0.0 or (sample_count >= 2 and win_rate < 0.40):
        level = "YELLOW"
        reasons.append(
            f"trade performance watch: sample={sample_count}, win_rate={win_rate:.2%}, avg_return={avg_return:.2%}"
        )
    else:
        reasons.append(
            f"trade performance acceptable: sample={sample_count}, win_rate={win_rate:.2%}, avg_return={avg_return:.2%}"
        )
    return {
        "schema_version": "trading_health_status.v1",
        "trading_health_level": level,
        "sample_count": int(sample_count),
        "total_trades": int(total_trades),
        "win_rate": float(win_rate),
        "avg_return": float(avg_return),
        "profit_factor": float(profit_factor),
        "reasoning": reasons,
        "source_path": str(summary_path),
    }
