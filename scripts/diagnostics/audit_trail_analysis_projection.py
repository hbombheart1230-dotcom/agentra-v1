from typing import Any, Dict, List


def analyze_day_rows(day_rows: List[Dict[str, Any]], *, facade: Any) -> Dict[str, Any]:
    by_run: Dict[str, List[Dict[str, Any]]] = {}
    stage_event_total = {k: 0 for k in ("start", "verdict", "execution", "degrade_policy_block", "end", "error")}
    for row in day_rows:
        run_id = str(row.get("run_id") or "").strip()
        if run_id:
            by_run.setdefault(run_id, []).append(row)
        stage, event = str(row.get("stage") or ""), str(row.get("event") or "")
        if stage == "execute_from_packet" and event in stage_event_total:
            stage_event_total[event] = int(stage_event_total[event]) + 1
    actionable_run_total = execution_run_total = linked_complete_run_total = 0
    missing_start: List[str] = []; missing_resolution: List[str] = []; missing_execution_payload: List[str] = []; missing_terminal: List[str] = []; orphan_execution: List[str] = []
    for run_id, rows in by_run.items():
        actionable = activity = start = verdict = degrade = execution = end = error = allowed = False
        for row in rows:
            stage, event = str(row.get("stage") or ""), str(row.get("event") or "")
            if stage == "decision" and event == "trace" and facade._extract_decision_action(row) in ("BUY", "SELL"):
                actionable = True
            if stage == "execute_from_packet":
                activity = True
                if event == "start": start = True
                elif event == "verdict":
                    verdict = True
                    if facade._extract_allowed(row) is True: allowed = True
                elif event == "degrade_policy_block": degrade = True
                elif event == "execution": execution = True
                elif event == "end": end = True
                elif event == "error": error = True
        if activity: execution_run_total += 1
        if activity and not actionable: orphan_execution.append(run_id)
        if not actionable: continue
        actionable_run_total += 1
        resolution, terminal = verdict or degrade or error, end or error
        if not start: missing_start.append(run_id)
        if not resolution: missing_resolution.append(run_id)
        if allowed and not execution: missing_execution_payload.append(run_id)
        if not terminal: missing_terminal.append(run_id)
        if start and resolution and (not allowed or execution) and terminal: linked_complete_run_total += 1
    link_success_rate = float(linked_complete_run_total) / float(actionable_run_total) if actionable_run_total else 1.0
    return {"run_total": int(len(by_run)), "actionable_decision_run_total": int(actionable_run_total), "execution_run_total": int(execution_run_total), "linked_complete_run_total": int(linked_complete_run_total), "link_success_rate": float(link_success_rate), "missing_execution_start_total": int(len(missing_start)), "missing_execution_resolution_total": int(len(missing_resolution)), "missing_execution_payload_total": int(len(missing_execution_payload)), "missing_terminal_event_total": int(len(missing_terminal)), "orphan_execution_run_total": int(len(orphan_execution)), "stage_event_total": stage_event_total, "anomaly_examples": {"missing_execution_start": missing_start[:10], "missing_execution_resolution": missing_resolution[:10], "missing_execution_payload": missing_execution_payload[:10], "missing_terminal_event": missing_terminal[:10], "orphan_execution": orphan_execution[:10]}}
