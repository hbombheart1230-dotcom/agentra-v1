from __future__ import annotations

import argparse


def _build_parser(*, facade: object = None) -> argparse.ArgumentParser:
    p = (facade.argparse if facade is not None else argparse).ArgumentParser(
        description="M31-1 daily SLO baseline + incident ownership check."
    )
    p.add_argument("--event-log-path", default="data/logs/events.jsonl")
    p.add_argument("--policy-report-dir", default="reports/milestones/m30_post_golive")
    p.add_argument("--signoff-report-dir", default="reports/milestones/m30_golive")
    p.add_argument("--report-dir", default="reports/milestones/m31_slo_incident")
    p.add_argument("--day", default="2026-02-21")
    p.add_argument("--min-availability-rate", type=float, default=0.99)
    p.add_argument("--max-error-rate", type=float, default=0.20)
    p.add_argument("--inject-fail", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
