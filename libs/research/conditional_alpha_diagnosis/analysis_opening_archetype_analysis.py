from collections import Counter, defaultdict
from typing import Any


def opening_archetype_analysis(rows: list[dict[str, Any]], *, facade: Any) -> dict[str, Any]:
    grouped=defaultdict(list)
    for row in rows: grouped[facade._archetype(row)].append(row)
    result={}
    for name,group in sorted(grouped.items()):
        values=sorted([v for row in group if (v:=facade.number(row.get("net_return_30m_pct"))) is not None],reverse=True); metrics=facade.performance(values)
        result[name]={**metrics,"strong_30m_count":sum(v>=2 for v in values),"average_without_top1_pct":round(sum(values[1:])/len(values[1:]),4) if len(values)>1 else None,"average_without_top3_pct":round(sum(values[3:])/len(values[3:]),4) if len(values)>3 else None,"playbooks":dict(sorted(Counter(str(r.get("playbook") or "MISSING") for r in group).items())),"scenarios":dict(sorted(Counter(str(r.get("strategist_scenario") or "MISSING") for r in group).items())),"scanner_score_average":facade._mean(group,"scanner_score"),"risk_score_average":facade._mean(group,"risk_score"),"confidence_average":facade._mean(group,"confidence"),"opening_gap_average_pct":facade._mean(group,"opening_gap_pct"),"entry_extension_average_pct":facade._mean(group,"entry_vs_prior_close_pct"),"opening_relative_volume_average":facade._mean(group,"opening_relative_volume"),"kospi_average_pct":facade._mean(group,"kospi_pct")}
    return result
