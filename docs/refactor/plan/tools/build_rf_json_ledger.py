#!/usr/bin/env python3
"""Generate evidence-conservative Agentra RF JSON ledger from tracked design documents.

Usage: python docs/refactor/plan/tools/build_rf_json_ledger.py
       python docs/refactor/plan/tools/build_rf_json_ledger.py --check
Only modifies docs/refactor/plan/RF_TASK_LEDGER.json. Preserves task status/evidence
from existing ledger; does not infer implementation completion from design/queue DONE.
"""
from __future__ import annotations
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
DETAILS = ROOT / "docs/refactor/plan/rf_details"
OUTPUT = ROOT / "docs/refactor/plan/RF_TASK_LEDGER.json"
RF_RE = re.compile(r"RF-(\d{3})_IMPLEMENTATION\.md$")
PATH_RE = re.compile(r"`([^`]+)`")
VALID = {"UNKNOWN", "NOT_STARTED", "IN_PROGRESS", "PASS", "BLOCKED", "NOT_APPLICABLE"}

def parse(path):
    raw = path.read_text(encoding="utf-8")
    owner_match = re.search(r"(?:구현 담당|소유)[^:\n]*[:：]\s*\*?\*?(Codex B|Claude A)", raw)
    queue_match = re.search(r"queue/(0\d_[A-Z_]+)/[^/]+/RF-\d{3}\.md", raw)
    section = 0
    tasks = []
    seen = set()
    for line in raw.splitlines():
        h = re.match(r"^## ([1-4])\.", line)
        if h:
            section = int(h.group(1))
            continue
        if not line.startswith("|") or re.match(r"^\|\s*:?-+", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if section == 1 and len(cells) >= 3:
            found = PATH_RE.findall(cells[0])
            if not found or "::" not in found[0]:
                continue
            source = found[0]
            target_match = PATH_RE.findall(cells[2])
            target = target_match[0] if target_match else None
            kind = "MOVE_BODY"
        elif section == 3 and len(cells) >= 3:
            found = PATH_RE.findall(cells[0])
            if not found or found[0] == "SOURCE_PATH":
                continue
            source = found[0].split(" → ")[0]
            target = found[0].split(" → ")[-1] if " → " in found[0] else (
                PATH_RE.findall(cells[1])[0] if PATH_RE.findall(cells[1]) else source)
            kind = "KEEP_IF"
        else:
            continue
        key = (kind, source, target)
        if key not in seen:
            seen.add(key)
            tasks.append({"kind": kind, "source": source, "target": target})
    return {"owner": owner_match.group(1) if owner_match else None,
            "queue_at_design": queue_match.group(1) if queue_match else None,
            "tasks": tasks}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="validate without writing")
    args = ap.parse_args()
    files = sorted(p for p in DETAILS.glob("RF-*_IMPLEMENTATION.md") if RF_RE.fullmatch(p.name))
    if not files:
        sys.exit("ERROR: no RF implementation documents found")
    old = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else {}
    previous = {(t["task_id"]): t for rf in old.get("rf", []) for t in rf.get("tasks", [])}
    data = {"schema_version": "1.0.0",
            "source_branch": "integration/p1.5",
            "source_dir": "docs/refactor/plan/rf_details",
            "completion_rule": "PASS in implementation, peer_review, and integration_runtime with no blocker",
            "rf": []}
    ids = set()
    for path in files:
        rf_id = path.name[:6]
        parsed = parse(path)
        tasks = []
        for i, item in enumerate(parsed["tasks"], 1):
            task_id = f"{rf_id}-{i:04d}"
            ids.add(task_id)
            prior = previous.get(task_id, {})
            # Never copy evidence if a regenerated ordinal now points to a different task.
            same = all(prior.get(k) == item[k] for k in ("kind", "source", "target"))
            status = {k: prior.get(k, "UNKNOWN") if same else "UNKNOWN"
                      for k in ("implementation", "peer_review", "integration_runtime")}
            if any(v not in VALID for v in status.values()):
                sys.exit(f"ERROR: invalid status in {task_id}")
            tasks.append({"task_id": task_id, **item, **status,
                          "blocker": prior.get("blocker") if same else None,
                          "evidence": prior.get("evidence", []) if same else []})
        data["rf"].append({"rf_id": rf_id, "owner": parsed["owner"],
                           "queue_at_design": parsed["queue_at_design"],
                           "design_document": str(path.relative_to(ROOT)).replace("\\", "/"),
                           "tasks": tasks})
    stale = sorted(set(previous) - ids)
    if stale:
        sys.exit("ERROR: previously tracked task IDs missing; manual migration required: " + ", ".join(stale[:15]))
    total = sum(len(x["tasks"]) for x in data["rf"])
    print(f"RF={len(files)} tasks={total} empty_RF={sum(not x['tasks'] for x in data['rf'])}")
    if args.check:
        return
    OUTPUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if __name__ == "__main__":
    main()
