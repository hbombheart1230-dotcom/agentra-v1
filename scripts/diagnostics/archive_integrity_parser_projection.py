from typing import Any


def _build_parser(*, facade: Any) -> Any:
    p = facade.argparse.ArgumentParser(description="Check archive manifest/hash integrity and retention policy.")
    p.add_argument("--archive-dir", default="data/logs/archive")
    p.add_argument("--report-dir", default="reports/archive_integrity")
    p.add_argument("--day", default=None)
    p.add_argument("--retention-days", type=int, default=30)
    p.add_argument("--allow-stale", action="store_true", help="Do not fail on stale archive days.")
    p.add_argument("--json", action="store_true")
    return p
