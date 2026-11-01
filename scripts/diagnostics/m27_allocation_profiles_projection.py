from typing import Any,Dict,List
def _default_profiles(*,facade:Any)->List[Dict[str,Any]]:return [{"strategy_id":"trend","enabled":True,"weight":.6,"max_notional_ratio":.7},{"strategy_id":"mean_reversion","enabled":True,"weight":.3,"max_notional_ratio":.4},{"strategy_id":"event_driven","enabled":True,"weight":.1,"max_notional_ratio":.2}]
