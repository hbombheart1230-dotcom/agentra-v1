from collections import defaultdict
from typing import Any, Mapping


def horizon_reversals(horizon_rows: list[dict[str, Any]], contexts: Mapping[str, Mapping[str, Any]], *, facade: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    result=[]; scenario_names=sorted({str(name) for row in horizon_rows for name in (row.get("scenario_returns") or {}) if str(name) != "actual_exit"}); grouped_values=defaultdict(list)
    for row in horizon_rows:
        trade_id=str(row.get("trade_id") or ""); context=dict(contexts.get(trade_id) or {}); actual=facade._scenario_value(row,"actual_exit"); broker=facade.number(row.get("broker_realized_net_return_pct")); scenarios=[]
        for scenario in scenario_names:
            alternative=facade._scenario_value(row,scenario)
            if alternative is None or actual is None: continue
            delta=round(alternative-actual,4); grouped_values[scenario].append(delta); scenarios.append({"scenario":scenario,"return_pct":alternative,"delta_vs_actual_pct":delta})
        best=max(scenarios,key=lambda item:item["return_pct"],default=None)
        result.append({**context,"trade_id":trade_id,"day":row.get("day") or context.get("day"),"symbol":row.get("symbol") or context.get("symbol"),"entry_horizon":row.get("entry_horizon") or context.get("strategy_horizon"),"holding_seconds":row.get("holding_seconds") or context.get("holding_seconds"),"exit_reason":row.get("exit_reason") or context.get("exit_reason"),"broker_realized_net_return_pct":broker,"actual_live_net_return_pct":actual,"alternatives":scenarios,"best_alternative":best,"loss_to_win":bool(actual is not None and actual<=0 and best and best["return_pct"]>0),"winner_giveback_risk":bool(actual is not None and actual>0 and best and best["return_pct"]<=0)})
    return result,{scenario:facade.performance(values) for scenario,values in grouped_values.items()}
