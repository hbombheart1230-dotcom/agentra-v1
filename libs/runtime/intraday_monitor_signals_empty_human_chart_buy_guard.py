from __future__ import annotations
from typing import Any, Dict

def _empty_human_chart_buy_guard(*, facade: Any) -> Dict[str, Any]:
    return {"schema_version":"human_chart_buy_guard.v1","available":False,"applied":False,"mode":"none","authority":"hard_buy_block","thresholds":{"min_entry_chart_score":0.25,"max_exit_risk_score":0.40,"min_late_entry_chart_score":0.50,"near_upper_prev_close_distance_pct":0.29,"no_reward_room_score":0.05,"no_reward_room_pct":0.012},"observed":{},"blocking_features":[],"notes":[]}
