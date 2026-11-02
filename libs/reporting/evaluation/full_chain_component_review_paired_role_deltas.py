"""full_chain_component_review: ``_paired_role_deltas`` body (moved verbatim from ``full_chain_component_review``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any


def _paired_role_deltas(
    candidates: list[dict[str, Any]],
    *,
    horizon: str,
    facade: Any,
) -> dict[str, Any]:
    windows: dict[str, dict[str, list[float]]] = facade.defaultdict(lambda: facade.defaultdict(list))
    window_days: dict[str, str] = {}
    for row in candidates:
        role = str(row.get("shadow_role") or "")
        if role not in {"top_pick", "runner_up_evaluated"}:
            continue
        value = facade._checkpoint_return(row, horizon)
        if value is None:
            continue
        window = str(row.get("_payload_generated_at") or "")
        if not window:
            continue
        windows[window][role].append(value)
        window_days[window] = facade.candidate_day(row) or ""
    deltas: list[float] = []
    days: set[str] = set()
    for window, roles in windows.items():
        top = roles.get("top_pick") or []
        runner = roles.get("runner_up_evaluated") or []
        if not top or not runner:
            continue
        deltas.append((sum(top) / len(top)) - (sum(runner) / len(runner)))
        if window_days.get(window):
            days.add(window_days[window])
    return {
        "horizon": horizon,
        "comparison": "top_pick_minus_runner_up_evaluated",
        "evidence_class": "TRUSTED_SHADOW",
        "paired_window_count": len(deltas),
        "observed_day_count": len(days),
        "average_delta_pct": round(sum(deltas) / len(deltas), 4) if deltas else None,
        "positive_delta_rate": round(sum(value > 0 for value in deltas) / len(deltas), 4) if deltas else None,
        "delta_distribution": facade.performance_metrics(deltas),
    }
