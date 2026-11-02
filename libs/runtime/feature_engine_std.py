from typing import Any, List, Optional

def _std(values: List[float], facade: Any) -> Optional[float]:
    if len(values) < 2:
        return None
    mean = float(sum(values) / float(len(values)))
    var = float(sum((x - mean) ** 2 for x in values) / float(len(values)))
    return float(facade.sqrt(var))
