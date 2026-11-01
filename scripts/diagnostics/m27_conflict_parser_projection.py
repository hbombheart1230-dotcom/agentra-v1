from typing import Any
def _build_parser(*,facade:Any):
 p=facade.argparse.ArgumentParser(description="M27-2 intent conflict resolution policy check.");p.add_argument("--json",action="store_true");p.add_argument("--inject-fail",action="store_true");return p
