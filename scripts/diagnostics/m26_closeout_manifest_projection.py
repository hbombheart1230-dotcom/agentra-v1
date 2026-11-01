from pathlib import Path
from typing import Any,Dict,Tuple
def _run_manifest_json(*,dataset_root:Path,seed_demo:bool,facade:Any)->Tuple[int,Dict[str,Any]]:
 argv=["--dataset-root",str(dataset_root),"--json"]
 if seed_demo: argv.insert(2,"--seed-demo")
 return facade._run_json(facade.manifest_main,argv)
