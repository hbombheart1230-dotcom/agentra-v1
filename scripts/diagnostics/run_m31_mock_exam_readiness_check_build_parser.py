from __future__ import annotations

import argparse


def _build_parser(*, facade: object = None) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Aggregate M30/M31 artifacts into one mock exam readiness checklist.")
    p.add_argument("--day", default="2026-02-21")
    p.add_argument("--env-path", default=".env")
    p.add_argument("--event-log-path", default="data/logs/events.jsonl")
    p.add_argument("--m30-event-log-dir", default="data/logs/milestones/m30/golive")
    p.add_argument("--m30-quality-report-dir", default="reports/milestones/m30_quality_gates")
    p.add_argument("--m30-signoff-report-dir", default="reports/milestones/m30_signoff")
    p.add_argument("--m30-policy-report-dir", default="reports/milestones/m30_post_golive")
    p.add_argument("--m30-golive-report-dir", default="reports/milestones/m30_golive")
    p.add_argument("--m31-slo-report-dir", default="reports/milestones/m31_slo_incident")
    p.add_argument("--m31-mock-exam-report-dir", default="reports/milestones/m31_mock_exam")
    p.add_argument("--report-dir", default="reports/milestones/m31_mock_exam_readiness")
    p.add_argument("--strict-session", action="store_true", help="Deprecated compatibility flag.")
    p.add_argument("--allow-offhours", action="store_true", help="Allow off-hours pass for M31-2 gate.")
    p.add_argument("--json", action="store_true")
    return p
