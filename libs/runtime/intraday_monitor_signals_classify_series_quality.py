from __future__ import annotations
from typing import Any, Dict, Mapping, Sequence

def _classify_series_quality(candles: Sequence[Mapping[str, Any]], *, timeframe_minutes: int, facade: Any) -> Dict[str, Any]:
    spacing_seconds=facade._infer_spacing_seconds(candles)
    if spacing_seconds is None: return {"intraday_compatible":True,"inferred_spacing_seconds":None,"inferred_spacing_minutes":None,"series_class":"unknown","compatibility_reason":"timestamp_missing"}
    spacing_minutes=spacing_seconds/60.0; maximum=max(1800.0,float(max(1,timeframe_minutes))*60.0*6.0); compatible=spacing_seconds<=maximum
    if compatible: series_class="intraday"
    elif spacing_seconds>=12*3600: series_class="daily_or_higher"
    else: series_class="higher_timeframe"
    return {"intraday_compatible":compatible,"inferred_spacing_seconds":round(spacing_seconds,3),"inferred_spacing_minutes":round(spacing_minutes,3),"series_class":series_class,"compatibility_reason":"intraday_spacing_detected" if compatible else "non_intraday_spacing_detected"}
