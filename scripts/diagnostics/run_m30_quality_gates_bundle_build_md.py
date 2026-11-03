from __future__ import annotations

from typing import Any, Dict


def _build_md(out: Dict[str, Any], *, facade: object = None) -> str:
    gates = out.get("gates") if isinstance(out.get("gates"), dict) else {}
    lines = [
        f"# M30 Quality Gates Bundle ({out.get('day')})", "",
        f"- ok: **{bool(out.get('ok'))}**",
        f"- failure_total: **{int(out.get('failure_total') or 0)}**",
        f"- report_json_path: `{out.get('report_json_path')}`", "", "## Gate Status", "",
    ]
    for name in ("functional", "resilience", "safety", "ops"):
        g = gates.get(name) if isinstance(gates.get(name), dict) else {}
        lines.append(f"- {name}: ok={bool(g.get('ok'))} pass_total={int(g.get('pass_total') or 0)} fail_total={int(g.get('fail_total') or 0)}")
    lines += ["", "## Failures", ""]
    failures = out.get("failures") if isinstance(out.get("failures"), list) else []
    if failures:
        for msg in failures:
            lines.append(f"- {msg}")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)
