#!/usr/bin/env python3
"""Merge checked-in RF JSON shards, preserving evidence from unified ledger."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PARTS = ROOT / "docs/refactor/plan/ledger_parts"
OUT = ROOT / "docs/refactor/plan/RF_TASK_LEDGER.json"
files = sorted(PARTS.glob("RF_*.json"))
if len(files) != 9:
    raise SystemExit(f"Expected 9 RF shards, got {len(files)}")
existing = json.loads(OUT.read_text(encoding="utf-8")) if OUT.exists() else {}
prior = {t["task_id"]: t for rf in existing.get("rf", []) for t in rf["tasks"]}
rf_list = []
for file in files:
    rf_list.extend(json.loads(file.read_text(encoding="utf-8"))["rf"])
rf_list.sort(key=lambda r: r["rf_id"])
ids = [r["rf_id"] for r in rf_list]
if ids != [f"RF-{n:03d}" for n in range(1, 94)]:
    raise SystemExit("Missing, duplicate, or unexpected RF IDs")
task_ids = set()
for rf in rf_list:
    for task in rf["tasks"]:
        tid = task["task_id"]
        if tid in task_ids:
            raise SystemExit(f"Duplicate task ID: {tid}")
        task_ids.add(tid)
        old = prior.get(tid)
        if old and all(old.get(k) == task.get(k) for k in ("kind", "source", "target")):
            for key in ("implementation", "peer_review", "integration_runtime", "blocker", "evidence"):
                task[key] = old.get(key, task.get(key))
if set(prior) - task_ids:
    raise SystemExit("Existing tracked task disappeared; manual migration required")
data = {
    "schema_version": "1.0.0",
    "source_branch": "integration/p1.5",
    "completion_rule": "implementation, peer_review, integration_runtime all PASS and no blocker",
    "rf": rf_list,
}
OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"RF={len(rf_list)} tasks={len(task_ids)} merged from {len(files)} shards")
