from typing import Any
def _normalize_decision_outcome(value: Any, *, fallback: str="WAIT", facade: Any) -> str:
    text=str(value or "").strip().upper()
    return text if text in facade._DECISION_OUTCOMES else fallback
