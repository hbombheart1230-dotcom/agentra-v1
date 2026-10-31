from typing import Any
def _utc_now_iso(*, facade: Any) -> str: return facade.datetime.now(facade.timezone.utc).isoformat()
