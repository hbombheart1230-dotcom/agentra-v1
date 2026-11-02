from typing import Any, Optional

def _to_float(v: Any, facade: Any) -> Optional[float]:
    try:
        if v is None:
            return None
        return float(v)
    except Exception:
        return None
