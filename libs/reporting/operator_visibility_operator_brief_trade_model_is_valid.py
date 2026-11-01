"""operator_visibility: ``_operator_brief_trade_model_is_valid`` body (moved verbatim from ``operator_visibility``).

``facade`` is the source module; module-level names resolve on it at call time (monkeypatch-compatible). Owner never imports the facade.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple


def _operator_brief_trade_model_is_valid(trade_model: Dict[str, Any], *, facade: Any) -> bool:
    if not isinstance(trade_model, dict) or not trade_model:
        return False
    facts = trade_model.get("facts") if isinstance(trade_model.get("facts"), dict) else {}
    provenance = trade_model.get("provenance") if isinstance(trade_model.get("provenance"), dict) else {}
    return bool(facts) and bool(provenance)
