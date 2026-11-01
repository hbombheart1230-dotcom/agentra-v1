from typing import Any
def _build_parser(*, facade: Any):
    p = facade.argparse.ArgumentParser(description="M26 A/B evaluation scaffold over scorecard outputs.")
    p.add_argument("--a-dataset-root", default="data/eval/m26_fixed_dataset_v1"); p.add_argument("--b-dataset-root", default="data/eval/m26_fixed_dataset_v1"); p.add_argument("--a-label", default="A"); p.add_argument("--b-label", default="B"); p.add_argument("--day", default=""); p.add_argument("--json", action="store_true")
    return p
