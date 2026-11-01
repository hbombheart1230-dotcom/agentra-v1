from typing import Any,Dict
def _default_caps(*,inject_fail:bool,facade:Any)->Dict[str,float]:return {"005930":1_000_000.0,"000660":1_000_000.0 if inject_fail else 200.0}
