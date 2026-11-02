from typing import Any, List, Mapping

def _series(candles: List[Mapping[str, Any]], key: str, facade: Any) -> List[float]:
    out: List[float] = []
    for row in candles:
        x = facade._to_float(row.get(key))
        if x is not None:
            out.append(float(x))
    return out
