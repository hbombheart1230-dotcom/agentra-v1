from typing import Any, Dict, List


def _default_intents(*, inject_fail: bool, facade: Any) -> List[Dict[str, Any]]:
    if inject_fail:
        return [{"intent_id": "i1", "strategy_id": "trend", "symbol": "005930", "side": "BUY", "qty": 1, "price": 100, "priority": 9, "confidence": 0.9}, {"intent_id": "i2", "strategy_id": "mean_reversion", "symbol": "000660", "side": "BUY", "qty": 1, "price": 100, "priority": 8, "confidence": 0.8}]
    return [{"intent_id": "i1", "strategy_id": "trend", "symbol": "005930", "side": "BUY", "qty": 1, "price": 100, "priority": 9, "confidence": 0.9}, {"intent_id": "i2", "strategy_id": "mean_reversion", "symbol": "005930", "side": "SELL", "qty": 1, "price": 100, "priority": 3, "confidence": 0.4}, {"intent_id": "i3", "strategy_id": "event_driven", "symbol": "000660", "side": "BUY", "qty": 4, "price": 40, "priority": 8, "confidence": 0.8}, {"intent_id": "i4", "strategy_id": "trend", "symbol": "000660", "side": "BUY", "qty": 3, "price": 40, "priority": 2, "confidence": 0.4}]
