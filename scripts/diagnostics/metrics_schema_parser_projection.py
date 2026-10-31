from typing import Any
def _build_parser(*, facade: Any):
    p = facade.argparse.ArgumentParser(description="Validate frozen metrics schema v1.")
    p.add_argument("--event-log-path", default="data/logs/events.jsonl"); p.add_argument("--report-dir", default="reports/metrics"); p.add_argument("--day", default=None); p.add_argument("--json", action="store_true")
    return p
