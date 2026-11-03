from __future__ import annotations

from typing import Any, Dict


def _build_markdown(out: Dict[str, Any], *, facade: object = None) -> str:
    items = out.get("checklist") if isinstance(out.get("checklist"), list) else []
    lines = [
        f"# M30 Release Sign-off Checklist ({out.get('day')})", "",
        f"- release_ready: **{bool(out.get('release_ready'))}**",
        f"- quality_gates_ok: **{bool(out.get('quality_gates_ok'))}**",
        f"- required_pass_total: **{int(out.get('required_pass_total') or 0)}**",
        f"- required_fail_total: **{int(out.get('required_fail_total') or 0)}**", "", "## Checklist", "",
    ]
    for it in items:
        mark = "x" if bool(it.get("passed")) else " "
        lines.append(f"- [{mark}] ({it.get('category')}) {it.get('title')} | evidence={it.get('evidence')}")
    lines += ["", "## Failures", ""]
    failures = out.get("failures") if isinstance(out.get("failures"), list) else []
    if failures:
        for msg in failures:
            lines.append(f"- {msg}")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)
