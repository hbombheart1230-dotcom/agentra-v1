from pathlib import Path
from typing import Any,Dict,Tuple
def _run_ab_eval_json(*,base_root:Path,candidate_root:Path,day:str,facade:Any)->Tuple[int,Dict[str,Any]]:
 a=["--a-dataset-root",str(base_root),"--b-dataset-root",str(candidate_root),"--a-label","baseline","--b-label","candidate","--json"]
 if day:a.extend(["--day",day])
 return facade._run_json(facade.ab_eval_main,a)
