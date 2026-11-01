from typing import Any, Dict, List


def _intents(*, inject_fail: bool, facade: Any) -> List[Dict[str, Any]]:
    if inject_fail:
        return [{"intent_id":"i1","strategy_id":"trend","symbol":"005930","side":"BUY","requested_notional":300,"priority":9,"confidence":0.9}, {"intent_id":"i2","strategy_id":"mean_reversion","symbol":"000660","side":"BUY","requested_notional":200,"priority":8,"confidence":0.8}]
    return [{"intent_id":"i1","strategy_id":"trend","symbol":"005930","side":"BUY","requested_notional":700,"priority":9,"confidence":0.9}, {"intent_id":"i2","strategy_id":"trend","symbol":"005930","side":"BUY","requested_notional":400,"priority":3,"confidence":0.3}, {"intent_id":"i3","strategy_id":"mean_reversion","symbol":"005930","side":"SELL","requested_notional":300,"priority":8,"confidence":0.8}, {"intent_id":"i4","strategy_id":"event_driven","symbol":"000660","side":"BUY","requested_notional":350,"priority":9,"confidence":0.9}, {"intent_id":"i5","strategy_id":"mean_reversion","symbol":"000660","side":"BUY","requested_notional":300,"priority":4,"confidence":0.4}]
