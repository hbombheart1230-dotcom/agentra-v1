from typing import Any,Dict,List
def _latest_day(rows:List[Dict[str,Any]],*,facade:Any)->str:
 d=sorted({str(r.get("_day") or "") for r in rows if str(r.get("_day") or "").strip()});return str(d[-1]) if d else facade.datetime.now(facade.timezone.utc).strftime("%Y-%m-%d")
