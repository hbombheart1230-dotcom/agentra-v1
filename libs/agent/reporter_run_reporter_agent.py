"""Reporter agent: ``run_reporter_agent`` entrypoint body (moved verbatim from ``libs.agent.reporter``).

Single decision-body Owner. ``facade`` is the ``libs.agent.reporter`` module; ``_normalize_trade_reporter_policy`` and
``_validate_trade_read_model`` are resolved on it at call time (monkeypatch-compatible). This module never imports the
facade. The read-model and separated-report imports stay lazy inside the function, exactly as before.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Optional


def run_reporter_agent(trade_dir: str, policy: Optional[Dict[str, Any]] = None, *, facade: Any) -> Dict[str, Any]:
    from libs.reporting.trade_read_model import build_trade_read_model
    from libs.reporting.fact_narrative_report import build_separated_report

    trade_root = Path(str(trade_dir))
    cfg = facade._normalize_trade_reporter_policy(policy)

    try:
        trade_model = build_trade_read_model(str(trade_root))
    except Exception as exc:
        return {
            "metadata": {
                "trade_id": "",
                "symbol": "",
                "trade_dir": str(trade_root),
                "generated_by": "reporter_agent_v1",
            },
            "facts": {},
            "provenance": {},
            "narrative": {
                "status": "error",
                "source": "llm",
                "based_on": "fact_payload",
                "reason": "trade_read_model_exception",
                "error": str(exc),
            },
            "status": "degraded",
        }

    validation = facade._validate_trade_read_model(trade_model)
    if not bool(validation.get("ok")):
        return {
            "metadata": {
                "trade_id": str(trade_model.get("trade_id") or ""),
                "symbol": str(trade_model.get("symbol") or ""),
                "trade_dir": str(trade_root),
                "generated_by": "reporter_agent_v1",
            },
            "facts": dict(trade_model.get("facts") or {}),
            "provenance": dict(trade_model.get("provenance") or {}),
            "context": dict(trade_model.get("context") or {}),
            "narrative": {
                "status": "skipped",
                "source": "llm",
                "based_on": "fact_payload",
                "reason": str(validation.get("reason") or "invalid_trade_read_model"),
                "llm_call_skipped": True,
            },
            "status": "degraded",
        }

    separated = build_separated_report(
        trade_model=trade_model,
        model=cfg["model"] or None,
        execution_profile=cfg["execution_profile"] or None,
    )
    narrative = separated.get("narrative") if isinstance(separated.get("narrative"), dict) else {}
    facts = trade_model.get("facts") if isinstance(trade_model.get("facts"), dict) else {}
    provenance = trade_model.get("provenance") if isinstance(trade_model.get("provenance"), dict) else {}
    context = trade_model.get("context") if isinstance(trade_model.get("context"), dict) else {}

    return {
        "metadata": {
            "trade_id": str(facts.get("trade_id") or trade_model.get("trade_id") or ""),
            "symbol": str(facts.get("symbol") or trade_model.get("symbol") or ""),
            "trade_dir": str(trade_root),
            "generated_by": "reporter_agent_v1",
        },
        "facts": dict(facts),
        "provenance": dict(provenance),
        "context": dict(context),
        "narrative": dict(narrative),
        "status": "ok" if str(narrative.get("status") or "").strip().lower() in {"ok", "dry_run", "skipped"} else "degraded",
    }
