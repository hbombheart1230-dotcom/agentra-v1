from typing import Any,Optional
def _to_epoch(ts:Any,*,facade:Any)->Optional[int]:
 if ts is None:return None
 if isinstance(ts,(int,float)):return int(ts)
 s=str(ts).strip()
 if not s:return None
 try:return int(float(s))
 except Exception:pass
 if s.endswith("Z"):s=s[:-1]+"+00:00"
 try:
  d=facade.datetime.fromisoformat(s)
  if d.tzinfo is None:d=d.replace(tzinfo=facade.timezone.utc)
  return int(d.timestamp())
 except Exception:return None
