from typing import Any
def _utc_day(ts:Any,*,facade:Any)->str:
 e=facade._to_epoch(ts)
 return facade.datetime.now(facade.timezone.utc).strftime("%Y-%m-%d") if e is None else facade.datetime.fromtimestamp(e,tz=facade.timezone.utc).strftime("%Y-%m-%d")
