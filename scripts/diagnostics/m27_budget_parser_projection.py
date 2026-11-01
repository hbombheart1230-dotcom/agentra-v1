from typing import Any


def _build_parser(*, facade: Any) -> Any:
    p = facade.argparse.ArgumentParser(description="M27-3 portfolio budget boundary check.")
    p.add_argument("--json", action="store_true")
    p.add_argument("--inject-fail", action="store_true")
    return p
