from collections import defaultdict
from typing import Any


def actual_live_cost_cross_sections(rows: list[dict[str, Any]], *, facade: Any) -> list[dict[str, Any]]:
    dimensions={"strategy_horizon":lambda r:str(r.get("strategy_horizon") or r.get("entry_horizon") or "MISSING"),"playbook":lambda r:str(r.get("playbook") or "MISSING"),"exit_reason":lambda r:facade._exit_class(r.get("exit_reason")),"holding_time":lambda r:facade._holding_bucket(r.get("holding_seconds")),"selected_rank":lambda r:str(r.get("selected_rank") if r.get("selected_rank") is not None else "MISSING"),"chart_fit":lambda r:facade._bucket(r.get("chart_fit_score"),(.35,.65),("LOW","MEDIUM","HIGH")),"scanner_score":lambda r:facade._bucket(r.get("scanner_score"),(.5,.75,1,1.25),("<0.50","0.50~0.75","0.75~1.00","1.00~1.25",">=1.25")),"risk_score":lambda r:facade._bucket(r.get("risk_score"),(.4,.7),("LOW","MEDIUM","HIGH"))}
    result=[]
    for dimension,resolver in dimensions.items():
        grouped=defaultdict(list)
        for row in rows: grouped[resolver(row)].append(row)
        for value,group in sorted(grouped.items()):
            metrics=facade.performance(row.get("actual_live_net_return_pct") for row in group); profile=facade.evidence_profile(group)
            result.append({"dimension":dimension,"value":value,**metrics,**profile,"evidence_status":facade.evidence_status(metrics,profile)})
    return result
