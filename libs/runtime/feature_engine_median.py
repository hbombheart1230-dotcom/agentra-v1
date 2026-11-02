from typing import Any, List, Optional

def _median(values: List[float], facade: Any) -> Optional[float]:
    if not values:
        return None
    arr = sorted(float(x) for x in values)
    n = len(arr)
    mid = n // 2
    if n % 2:
        return float(arr[mid])
    return float((arr[mid - 1] + arr[mid]) / 2.0)
