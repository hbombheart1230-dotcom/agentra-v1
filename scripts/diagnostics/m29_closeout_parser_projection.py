from typing import Any


def _build_parser(*, facade: Any) -> Any:
    p = facade.argparse.ArgumentParser(description="M29 governance closeout check (audit/archive/timeline/dr).")
    p.add_argument("--event-log-dir", default="data/logs/m29_closeout")
    p.add_argument("--report-dir", default="reports/m29_closeout")
    p.add_argument("--day", default="2026-02-21")
    p.add_argument("--inject-fail", action="store_true")
    p.add_argument("--no-clear", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
