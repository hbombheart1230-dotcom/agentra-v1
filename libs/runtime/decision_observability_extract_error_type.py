from typing import Any
def _extract_error_type(value: Any, *, facade: Any) -> str:
    text=str(value or "").strip()
    if not text:return ""
    for item in ("TimeoutError","ValueError","RuntimeError","TypeError","ConnectionError"):
        if item in text:return item
    if ":" in text:return text.split(":",1)[0].strip()
    if "(" in text:return text.split("(",1)[0].strip()
    return text[:40]
