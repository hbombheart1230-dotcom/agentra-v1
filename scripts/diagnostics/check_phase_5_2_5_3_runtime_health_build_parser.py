"""Pure parser-construction owner for runtime health diagnostics."""
from __future__ import annotations

from typing import Any


def _build_parser(*, facade: Any) -> Any:
    parser = facade.argparse.ArgumentParser(
        description="Inspect phase 5-2 ~ 5-3 runtime surfaces from canonical monitor artifacts and monitor event payloads."
    )
    parser.add_argument("--reports-root", default="reports")
    parser.add_argument("--event-log-path", default="data/logs/events.jsonl")
    parser.add_argument("--date", default="", help="Canonical day (YYYY-MM-DD). Defaults to latest canonical day.")
    parser.add_argument("--run-id", action="append", default=[], help="Specific run_id(s) to inspect. May be repeated.")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--only-buy", action="store_true", help="Print only recent BUY run table after aggregation.")
    parser.add_argument("--reason", default="", help="Filter compact run view by exact legacy/final reason.")
    parser.add_argument("--show-reclaim-near-ready", action="store_true", help="Print reclaim WAIT table with near-ready fields.")
    parser.add_argument("--show-policy-summary", action="store_true", help="Print only compact policy surface quality summary.")
    parser.add_argument("--show-chart-structure-summary", action="store_true", help="Print only compact chart structure decision hint summary.")
    parser.add_argument("--json", action="store_true")
    return parser
