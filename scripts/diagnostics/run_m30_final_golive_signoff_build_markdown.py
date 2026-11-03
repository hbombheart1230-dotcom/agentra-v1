from __future__ import annotations
from typing import Any, Dict
def _build_markdown(out: Dict[str, Any], *, facade: object = None) -> str:
    a=out.get("m30_1_quality_gates") if isinstance(out.get("m30_1_quality_gates"),dict) else {}; b=out.get("m30_2_signoff") if isinstance(out.get("m30_2_signoff"),dict) else {}; c=out.get("m30_3_policy") if isinstance(out.get("m30_3_policy"),dict) else {}
    lines=[f"# M30 Final Go-live Signoff ({out.get('day')})","",f"- approved: **{bool(out.get('approved'))}**",f"- go_live_decision: **{out.get('go_live_decision')}**",f"- failure_total: **{int(out.get('failure_total') or 0)}**","","## Stage Status","",f"- m30_1_quality_gates: rc={int(a.get('rc') or 0)} ok={bool(a.get('ok'))}",f"- m30_2_release_signoff: rc={int(b.get('rc') or 0)} release_ready={bool(b.get('release_ready'))}",f"- m30_3_post_golive_policy: rc={int(c.get('rc') or 0)} escalation_level={c.get('escalation_level')}","","## Failures",""]
    failures=out.get("failures") if isinstance(out.get("failures"),list) else []
    lines += [f"- {msg}" for msg in failures] or ["- (none)"]; lines.append("")
    return "\n".join(lines)
