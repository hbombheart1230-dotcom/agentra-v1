"""Pure parser-construction owner for intent state diagnostics."""
from __future__ import annotations

from typing import Any


def _build_parser(*, facade: Any) -> Any:
    p = facade.argparse.ArgumentParser(description="Query SQLite intent state/journal summary for operations.")
    p.add_argument("--state-db-path", default="")
    p.add_argument("--intent-log-path", default="data/logs/intents.jsonl")
    p.add_argument("--state", default="", help="Filter by current state (e.g. executing, failed, executed).")
    p.add_argument("--limit", type=int, default=20)
    p.add_argument("--stuck-executing-sec", type=int, default=0)
    p.add_argument("--require-no-stuck", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
