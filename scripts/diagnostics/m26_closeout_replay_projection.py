from pathlib import Path
from typing import Any,Dict,Tuple
def _run_replay_json(*,dataset_root:Path,day:str,facade:Any)->Tuple[int,Dict[str,Any]]:
 argv=["--dataset-root",str(dataset_root),"--json"]
 if day: argv.extend(["--day",day])
 return facade._run_json(facade.replay_main,argv)
