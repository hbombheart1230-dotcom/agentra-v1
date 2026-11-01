from typing import Any, Dict, List


def _profiles(*, facade: Any) -> List[Dict[str, Any]]:
    return [{"strategy_id": "trend", "enabled": True, "weight": 0.5}, {"strategy_id": "mean_reversion", "enabled": True, "weight": 0.3}, {"strategy_id": "event_driven", "enabled": True, "weight": 0.2}]
