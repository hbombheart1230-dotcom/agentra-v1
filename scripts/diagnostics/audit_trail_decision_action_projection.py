from typing import Any,Dict
def _extract_decision_action(row:Dict[str,Any],*,facade:Any)->str:
 p=row.get("payload") if isinstance(row.get("payload"),dict) else {};q=p.get("decision_packet") if isinstance(p.get("decision_packet"),dict) else {};i=q.get("intent") if isinstance(q.get("intent"),dict) else {};return str(i.get("action") or p.get("action") or p.get("intent") or "").strip().upper()
