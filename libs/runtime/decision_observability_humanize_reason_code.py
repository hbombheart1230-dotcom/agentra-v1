from typing import Any
def _humanize_reason_code(value: Any, *, facade: Any) -> str:
    text=str(value or "").strip()
    return text.replace("_"," ") if text else ""
