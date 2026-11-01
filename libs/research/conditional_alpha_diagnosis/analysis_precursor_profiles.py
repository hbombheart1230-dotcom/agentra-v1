from collections import Counter
from typing import Any


def precursor_profiles(rows: list[dict[str, Any]], *, facade: Any) -> dict[str, Any]:
    def observed_return(row, default):
        value=facade.number(row.get("net_return_30m_pct")); return default if value is None else value
    cohorts={"STRONG_30M":[r for r in rows if observed_return(r,-999)>=2],"MODEST_WIN_30M":[r for r in rows if 0<observed_return(r,-999)<2],"NON_POSITIVE_30M":[r for r in rows if observed_return(r,999)<=0]}
    fields=("scanner_score","risk_score","confidence","rank1_rank2_gap","rank1_prev5m_observations","opening_gap_pct","entry_vs_prior_close_pct","open_to_entry_pct","precompleted_return_1m_pct","opening_relative_volume","scanner_chart_fit_score","scanner_macro_chart_fit_score","kospi_pct","kosdaq_pct","krx_night_futures_pct","nasdaq_pct","vix_level")
    output={}
    for name,group in cohorts.items():
        numeric={}
        for field in fields:
            values=[v for row in group if (v:=facade.number(row.get(field))) is not None]; numeric[field]={"count":len(values),"average":round(sum(values)/len(values),4) if values else None}
        output[name]={"count":len(group),"numeric":numeric,"playbooks":dict(sorted(Counter(str(r.get("playbook") or "MISSING") for r in group).items())),"scenarios":dict(sorted(Counter(str(r.get("strategist_scenario") or "MISSING") for r in group).items())),"sources":dict(sorted(Counter(str(r.get("source_class") or "MISSING") for r in group).items()))}
    return output
