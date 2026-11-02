from __future__ import annotations

import argparse


def _build_parser(*, facade: object = None) -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="M29-8 disaster recovery drill (restore + replay validation).")
    p.add_argument("--working-dataset-root", default="data/recovery/m29_working_dataset")
    p.add_argument("--archive-dir", default="data/logs/m29_dr_archive")
    p.add_argument("--restored-dataset-root", default="data/recovery/m29_restored_dataset")
    p.add_argument("--report-dir", default="reports/m29_disaster_recovery")
    p.add_argument("--day", default="2026-02-21")
    p.add_argument("--inject-fail", action="store_true")
    p.add_argument("--no-clear", action="store_true")
    p.add_argument("--json", action="store_true")
    return p
