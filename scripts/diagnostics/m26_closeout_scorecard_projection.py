from pathlib import Path
from typing import Any,Dict,Tuple
def _run_scorecard_json(*,dataset_root:Path,day:str,facade:Any)->Tuple[int,Dict[str,Any]]:
 a=["--dataset-root",str(dataset_root),"--json"]
 if day:a.extend(["--day",day])
 return facade._run_json(facade.scorecard_main,a)
