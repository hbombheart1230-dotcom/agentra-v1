from typing import Any
def _build_parser(*,facade:Any):
 p=facade.argparse.ArgumentParser(description="Check intent->decision->execution audit trail completeness.");p.add_argument("--event-log-path",default="data/logs/events.jsonl");p.add_argument("--report-dir",default="reports/audit");p.add_argument("--day",default=None);p.add_argument("--require-actionable",action="store_true");p.add_argument("--json",action="store_true");return p
