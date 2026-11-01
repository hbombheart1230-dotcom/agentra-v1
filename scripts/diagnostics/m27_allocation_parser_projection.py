from typing import Any
def _build_parser(*,facade:Any):
 p=facade.argparse.ArgumentParser(description="M27-1 multi-strategy allocation policy check.");p.add_argument("--total-notional",type=float,default=1_000_000);p.add_argument("--reserve-ratio",type=float,default=.1);p.add_argument("--json",action="store_true");return p
