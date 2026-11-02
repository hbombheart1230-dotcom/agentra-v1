from typing import Any
def _to_float(value: Any, *, facade: Any) -> float:
    try: return float(value)
    except Exception: return 0.0
