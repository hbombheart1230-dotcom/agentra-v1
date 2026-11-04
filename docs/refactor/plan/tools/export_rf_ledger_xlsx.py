#!/usr/bin/env python3
"""Generate the Agentra RF dashboard from the canonical JSON ledger."""
import json
from collections import Counter
import re
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

root = Path(__file__).resolve().parents[4]
source = root / "docs/refactor/plan/RF_TASK_LEDGER.json"
output = root / "docs/refactor/plan/RF_TASK_LEDGER.xlsx"
data = json.loads(source.read_text(encoding="utf-8"))
rf_list = data["rf"]
status_doc = (root / "docs/refactor/plan/STATUS.md").read_text(encoding="utf-8")
# Queue location is RF-level status, not task-level PASS evidence.
queue_state = {}
for state, num in re.findall(r"queue/(0[1-5]_[A-Z_]+)/(?:[A-Z_]+/)?RF-(\\d{3})\\.md", status_doc):
    queue_state[f"RF-{num}"] = state
assert len(rf_list) == 93
wb = Workbook.create()
detail = wb.worksheets.add("세부 작업")
summary = wb.worksheets.add("RF별 요약")
guide = wb.worksheets.add("판정 기준")
headers = ["RF 번호","작업 ID","작업 유형","원본·작업 항목","목표","담당","구현",
           "독립 검증","통합·런 검증","차단 사유","증거","설계 문서"]
detail_rows = [headers]
summary_rows = [["RF 번호","RF 상태","전체 작업","완료","진행","차단","미확인","완료율","담당","설계 문서"]]
ids = set()
for rf in rf_list:
    counts = Counter()
    for t in rf["tasks"]:
        tid = t["task_id"]
        assert tid not in ids, f"duplicate task ID: {tid}"
        ids.add(tid)
        impl,peer,runtime = [t.get(k,"UNKNOWN") for k in ("implementation","peer_review","integration_runtime")]
        blocker = t.get("blocker")
        done = impl == peer == runtime == "PASS" and not blocker
        if done:
            counts["완료"] += 1
        elif blocker or "BLOCKED" in (impl,peer,runtime):
            counts["차단"] += 1
        elif "IN_PROGRESS" in (impl,peer,runtime):
            counts["진행"] += 1
        else:
            counts["미확인"] += 1
        detail_rows.append([rf["rf_id"],tid,t["kind"],t["source"],t.get("target") or "",
                            rf.get("owner") or "",impl,peer,runtime,str(blocker or ""),
                            json.dumps(t.get("evidence",[]),ensure_ascii=False),
                            rf.get("design_document") or ""])
    total = len(rf["tasks"])
    summary_rows.append([rf["rf_id"],queue_state.get(rf["rf_id"],"STATUS_UNVERIFIED"),total,counts["완료"],counts["진행"],counts["차단"],
                         counts["미확인"],counts["완료"]/total if total else 0,
                         rf.get("owner") or "",rf.get("design_document") or ""])
detail.get_range(f"A1:L{len(detail_rows)}").values = detail_rows
summary.get_range("A1:J94").values = summary_rows
guide.get_range("A1:B7").values = [
    ["항목","설명"],
    ["정본","docs/refactor/plan/RF_TASK_LEDGER.json"],
    ["총 RF",str(len(rf_list))],
    ["세부 작업 수",str(len(ids))],
    ["완료","구현·독립 검증·통합 런 검증 모두 PASS, 차단 사유 없음"],
    ["UNKNOWN","작업별 증거 미확인. RF 전체 DONE과는 별개"],
    ["KEEP_IF","파일 단위 유지/검증 항목. 실제 코드 이동 건수와 구분"],
]
for sheet,range_name in ((detail,"A1:L1"),(summary,"A1:J1"),(guide,"A1:B1")):
    sheet.get_range(range_name).format.fill = "#17324D"
    sheet.get_range(range_name).format.font.color = "#FFFFFF"
    sheet.get_range(range_name).format.font.bold = True
    sheet.freeze_panes.freeze_rows(1)
for col,width in {"A":16,"B":22,"C":18,"D":68,"E":65,"F":17,"G":18,
                  "H":18,"I":19,"J":28,"K":42,"L":66}.items():
    detail.get_range(f"{col}:{col}").format.column_width = width
for col,width in {"A":16,"B":17,"C":15,"D":15,"E":15,"F":15,"G":16,"H":18,"I":18,"J":70}.items():
    summary.get_range(f"{col}:{col}").format.column_width = width
summary.get_range("H2:H94").set_number_format("0.0%")
guide.get_range("A:A").format.column_width = 23
guide.get_range("B:B").format.column_width = 90
SpreadsheetFile.export_xlsx(wb).save(str(output))
assert output.is_file() and output.stat().st_size > 1000
print(f"Excel generated: {output}, RF={len(rf_list)}, tasks={len(ids)}")
