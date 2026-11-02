from typing import Any
def _to_int(value: Any, *, facade: Any) -> int:
    try: return int(float(value))
    except Exception: return 0
