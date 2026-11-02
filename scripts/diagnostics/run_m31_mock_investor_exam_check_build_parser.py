from __future__ import annotations

import argparse


def _build_parser(*, facade: object = None) -> argparse.ArgumentParser:
    p = (facade.argparse if facade is not None else argparse).ArgumentParser(description="M31-2 mock investor exam protocol gate check.")
    p.add_argument("--env-path", default=".env")
    p.add_argument("--event-log-path", default="data/logs/events.jsonl")
    p.add_argument("--report-dir", default="reports/milestones/m31_mock_exam")
    p.add_argument("--day", default="2026-02-21")
    p.add_argument("--allow-offhours", action="store_true", help="Allow off-hours check pass (default is hard session gate).")
    p.add_argument("--strict-session", action="store_true", help="Deprecated compatibility flag (session gate is hard by default).")
    p.add_argument("--now-kst", default=None, help="Optional ISO datetime override for deterministic session checks.")
    p.add_argument("--inject-fail", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
