from pathlib import Path
from typing import Any,Dict,Tuple
def _run_gate_json(*,base_root:Path,candidate_root:Path,day:str,min_delta_total_pnl_proxy:float,facade:Any)->Tuple[int,Dict[str,Any]]:
 a=["--a-dataset-root",str(base_root),"--b-dataset-root",str(candidate_root),"--a-label","baseline","--b-label","candidate","--min-delta-total-pnl-proxy",str(float(min_delta_total_pnl_proxy)),"--min-sortino-proxy","0","--max-drawdown-ratio","1","--json"]
 if day:a.extend(["--day",day])
 return facade._run_json(facade.gate_main,a)
