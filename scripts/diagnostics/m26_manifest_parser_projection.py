from typing import Any
def _build_parser(*,facade:Any):
 p=facade.argparse.ArgumentParser(description="M26 fixed dataset manifest scaffold and validation gate.");p.add_argument("--dataset-root",default="data/eval/m26_fixed_dataset_v1");p.add_argument("--seed-demo",action="store_true");p.add_argument("--json",action="store_true");return p
