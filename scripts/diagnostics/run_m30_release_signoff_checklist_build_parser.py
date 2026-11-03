from __future__ import annotations
import argparse
def _build_parser(*, facade: object = None) -> argparse.ArgumentParser:
    p=(facade.argparse if facade is not None else argparse).ArgumentParser(description="M30-2 release sign-off checklist generator.")
    p.add_argument("--quality-gates-json-path",default=""); p.add_argument("--event-log-dir",default="data/logs/milestones/m30/quality_gates"); p.add_argument("--quality-report-dir",default="reports/milestones/m30_quality_gates"); p.add_argument("--report-dir",default="reports/milestones/m30_signoff"); p.add_argument("--day",default="2026-02-21"); p.add_argument("--inject-fail",action="store_true"); p.add_argument("--no-run-quality-gates",action="store_true"); p.add_argument("--json",action="store_true")
    return p
