#!/usr/bin/env python3
"""Export the canonical RF JSON ledger to an Excel dashboard using artifact_tool."""
import json
from pathlib import Path
from artifact_tool import Workbook, SpreadsheetFile

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "docs/refactor/plan/RF_TASK_LEDGER.json"
TARGET = ROOT / "docs/refactor/plan/RF_TASK_LEDGER.xlsx"
ledger = json.loads(SOURCE.read_text(encoding="utf-8"))
rf_list = ledger["rf"]
assert len(rf_list) == 93, "Expected 93 RF entries"
rows = []
for rf in rf_list:
    for t in rf["tasks"]:
        rows.append([
            rf["rf_id"], t["task_id"], t["kind"], t["source"], t.get("target") or "",
            rf.get("owner") or "", t.get("implementation") or "UNKNOWN",
            t.get("peer_review") or "UNKNOWN",
            t.get("integration_runtime") or "UNKNOWN",
            t.get("blocker") or "",
            "; ".join(str(x) for x in t.get("evidence", [])),
            rf.get("design_document") or "",
        ])
assert len(rows) == len({r[1] for r in rows}), "Duplicate task IDs"
wb = Workbook.create()
detail = wb.worksheets.add("세부 작업")
summary = wb.worksheets.add("RF별 요약")
guide = wb.worksheets.add("판정 기준")
headers = ["RF 번호","작업 ID","작업 유형","원본/작업 항목","목표","담당",
           "구현","독립 검증","통합·런 검증","차단 사유","증거","설계 문서"]
detail.get_range(f"A1:L{len(rows)+1}").values = [headers] + rows
detail.get_range("A1:L1").format = {"fill":"#16324F","font":{"bold":True,"color":"#FFFFFF"}}
detail.freeze_panes.freeze_rows(1)
for col, width in {"A":14,"B":23,"C":17,"D":70,"E":65,"F":17,
                   "G":17,"H":17,"I":19,"J":30,"K":45,"L":68}.items():
    detail.get_range(f"{col}:{col}").format.column_width = width
detail.tables.add(f"A1:L{len(rows)+1}",True,"RFTaskDetails")
sum_headers = ["RF 번호","전체 작업","완료","진행","차단","미확인","완료율","담당","설계 문서"]
summary.get_range("A1:I1").values = [sum_headers]
summary.get_range("A1:I1").format = {"fill":"#16324F","font":{"bold":True,"color":"#FFFFFF"}}
summary.freeze_panes.freeze_rows(1)
for col,width in {"A":15,"B":16,"C":15,"D":15,"E":15,"F":15,"G":16,"H":18,"I":70}.items():
    summary.get_range(f"{col}:{col}").format.column_width = width
last = len(rows)+1
for i,rf in enumerate(rf_list,2):
    summary.get_range(f"A{i}:I{i}").values = [[
        rf["rf_id"],
        f'=COUNTIF(\'세부 작업\'!$A$2:$A${last},A{i})'.replace("\\$","$"),
        f'=COUNTIFS(\'세부 작업\'!$A$2:$A${last},A{i},\'세부 작업\'!$G$2:$G${last},"PASS",\'세부 작업\'!$H$2:$H${last},"PASS",\'세부 작업\'!$I$2:$I${last},"PASS",\'세부 작업\'!$J$2:$J${last},"")'.replace("\\$","$"),
        f'=COUNTIFS(\'세부 작업\'!$A$2:$A${last},A{i},\'세부 작업\'!$G$2:$G${last},"IN_PROGRESS")+COUNTIFS(\'세부 작업\'!$A$2:$A${last},A{i},\'세부 작업\'!$H$2:$H${last},"IN_PROGRESS")+COUNTIFS(\'세부 작업\'!$A$2:$A${last},A{i},\'세부 작업\'!$I$2:$I${last},"IN_PROGRESS")'.replace("\\$","$"),
        f'=COUNTIFS(\'세부 작업\'!$A$2:$A${last},A{i},\'세부 작업\'!$J$2:$J${last},"?*")'.replace("\\$","$"),
        f'=B{i}-C{i}-D{i}-E{i}',
        f'=IFERROR(C{i}/B{i},0)',
        rf.get("owner") or "",
        rf.get("design_document") or "",
    ]]
summary.tables.add("A1:I94",True,"RFTaskSummary")
guide.get_range("A1:B7").values = [
    ["항목","정의"],
    ["정본","docs/refactor/plan/RF_TASK_LEDGER.json"],
    ["작업 수",str(len(rows))],
    ["완료","구현·독립 검증·통합런 검증 모두 PASS, 차단 사유 없음"],
    ["UNKNOWN","미착수나 완료가 아닌 증거 미확인"],
    ["KEEP_IF","실제 KEEP_OK 근거와 증거 확인 전에는 완료 아님"],
    ["주의","설계 작업 목록이며 실제 구현 완료를 의미하지 않음"],
]
guide.get_range("A1:B1").format = {"fill":"#16324F","font":{"bold":True,"color":"#FFFFFF"}}
guide.get_range("A:A").format.column_width=23
guide.get_range("B:B").format.column_width=90
SpreadsheetFile.export_xlsx(wb).save(str(TARGET))
print(f"Exported {TARGET}: RF={len(rf_list)} tasks={len(rows)}")
