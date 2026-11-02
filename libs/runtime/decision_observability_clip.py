from typing import Any
def _clip(value: Any, *, max_len: int=200, facade: Any) -> str:
    text=str(value or "").strip()
    return text if len(text)<=max_len else text[:max(0,max_len-3)]+"..."
