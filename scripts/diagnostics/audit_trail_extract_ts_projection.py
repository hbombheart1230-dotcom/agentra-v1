from typing import Any,Dict
def _extract_ts(row:Dict[str,Any],*,facade:Any)->Any:
 p=row.get("payload") if isinstance(row.get("payload"),dict) else {};return row.get("ts") or p.get("ts")
