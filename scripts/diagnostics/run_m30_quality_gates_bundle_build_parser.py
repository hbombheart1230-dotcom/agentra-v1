from __future__ import annotations

import argparse


def _build_parser(*, facade: object = None) -> argparse.ArgumentParser:
    p = (facade.argparse if facade is not None else argparse).ArgumentParser(description="M30-1 quality gates bundle (functional/resilience/safety/ops).")
    p.add_argument("--event-log-dir", default="data/logs/milestones/m30/quality_gates")
    p.add_argument("--report-dir", default="reports/milestones/m30_quality_gates")
    p.add_argument("--day", default="2026-02-21")
    p.add_argument("--m23-day", default="", help="Optional explicit day for m23 closeout; default uses script latest-day behavior.")
    p.add_argument("--m26-day", default="2026-02-17", help="Replay evaluation day for m26 closeout (dataset-seeded default).")
    p.add_argument("--inject-fail", action="store_true")
    p.add_argument("--no-clear", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
