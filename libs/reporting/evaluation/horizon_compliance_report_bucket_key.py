"""horizon_compliance_report: ``_bucket_key`` body (moved verbatim from ``horizon_compliance_report``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from typing import Any, Mapping


def _bucket_key(evaluation: Mapping[str, Any], *, facade: Any) -> tuple[str, str]:
    horizon = facade._mapping(evaluation.get("horizon_alignment"))
    exit_quality = facade._mapping(evaluation.get("exit_quality"))
    strategy_horizon = str(horizon.get("strategy_horizon") or "unknown")
    exit_reason = str(exit_quality.get("reason") or evaluation.get("exit_reason") or "unknown")
    return strategy_horizon, exit_reason
