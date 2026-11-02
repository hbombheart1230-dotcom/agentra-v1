"""Pure parser-construction owner for the M29 timeline check."""
from __future__ import annotations

from typing import Any


def _build_parser(*, facade: Any) -> Any:
    p = facade.argparse.ArgumentParser(description="M29-7 incident timeline reconstruction closeout check.")
    p.add_argument("--event-log-path", default="data/logs/m29_incident_timeline_events.jsonl")
    p.add_argument("--report-dir", default="reports/m29_incident_timeline")
    p.add_argument("--day", default="2026-02-21")
    p.add_argument("--inject-fail", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
