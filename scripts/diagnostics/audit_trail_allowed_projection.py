from typing import Any,Dict,Optional
def _extract_allowed(row:Dict[str,Any],*,facade:Any)->Optional[bool]:
 p=row.get("payload") if isinstance(row.get("payload"),dict) else {};v=p.get("allowed");return v if isinstance(v,bool) else None
