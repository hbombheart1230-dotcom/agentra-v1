from typing import Any


def _build_parser(*, facade: Any) -> Any:
    p = facade.argparse.ArgumentParser(description="M27 closeout check (allocation/conflict/guard/metrics/notify).")
    p.add_argument("--event-log-dir", default="data/logs/m27_closeout")
    p.add_argument("--report-dir", default="reports/m27_closeout")
    p.add_argument("--day", default="2026-02-20")
    p.add_argument("--inject-fail", action="store_true")
    p.add_argument("--no-clear", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
