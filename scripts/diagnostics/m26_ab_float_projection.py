from typing import Any
def _as_float(v: Any, default: float = 0.0) -> float:
    try: return float(v)
    except Exception: return float(default)
