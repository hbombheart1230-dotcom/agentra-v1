from typing import Any

def _to_float(v: Any, default: float = 0.0, facade: Any = None) -> float:
    try: return float(v)
    except Exception: return float(default)
