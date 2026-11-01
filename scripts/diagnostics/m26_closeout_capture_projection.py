from typing import Any,Dict,List,Tuple
def _run_json(main_fn,argv:List[str],*,facade:Any)->Tuple[int,Dict[str,Any]]:return facade.capture_cli_json(main_fn,argv)
