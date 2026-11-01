from typing import Any, Optional


def _parse_day(value: str, *, facade: Any) -> Optional[Any]:
    s = str(value or "").strip()
    if not s:
        return None
    try:
        return facade.datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None
