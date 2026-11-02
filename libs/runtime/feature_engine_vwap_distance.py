from typing import Any, List, Mapping, Optional

def _vwap_distance(candles: List[Mapping[str, Any]], closes: List[float], vols: List[float], facade: Any) -> Optional[float]:
    if not candles or not closes: return None
    last_close=float(closes[-1])
    if last_close <= 0.0: return None
    vwap_raw=facade._to_float(candles[-1].get("vwap"))
    if vwap_raw is not None and vwap_raw > 0.0: return float((last_close / float(vwap_raw))-1.0)
    if len(closes)!=len(vols) or not vols: return None
    den=float(sum(v for v in vols if v>0.0))
    if den<=0.0: return None
    num=sum(float(c)*float(vols[i]) for i,c in enumerate(closes) if float(vols[i])>0.0)
    if num<=0.0: return None
    vwap=num/den
    return float((last_close/vwap)-1.0) if vwap>0.0 else None
