from __future__ import annotations

from typing import Any, Dict


def _build_markdown(out: Dict[str, Any], *, facade: object = None) -> str:
    mode = out.get("runtime_mode") if isinstance(out.get("runtime_mode"), dict) else {}
    guards = out.get("guardrails") if isinstance(out.get("guardrails"), dict) else {}
    market = out.get("market") if isinstance(out.get("market"), dict) else {}
    events = out.get("events") if isinstance(out.get("events"), dict) else {}
    checklist = out.get("checklist") if isinstance(out.get("checklist"), list) else []
    lines = [
        f"# M31-2 Mock Investor Exam Check ({out.get('day')})", "",
        f"- ok: **{bool(out.get('ok'))}**",
        f"- required_pass_total: **{int(out.get('required_pass_total') or 0)}**",
        f"- required_fail_total: **{int(out.get('required_fail_total') or 0)}**", "",
        "## Runtime Mode", "",
        f"- RUNTIME_PROFILE: **{mode.get('RUNTIME_PROFILE')}**",
        f"- KIWOOM_MODE: **{mode.get('KIWOOM_MODE')}**",
        f"- APPROVAL_MODE: **{mode.get('APPROVAL_MODE')}**",
        f"- EXECUTION_ENABLED: **{bool(mode.get('EXECUTION_ENABLED'))}**",
        f"- ALLOW_REAL_EXECUTION: **{bool(mode.get('ALLOW_REAL_EXECUTION'))}**", "",
        "## Guardrails", "",
        f"- SYMBOL_ALLOWLIST size: **{int(guards.get('allowlist_size') or 0)}**",
        "- SYMBOL_ALLOWLIST policy: **optional operational guard (recommended but not mandatory)**",
        f"- max_notional_key: **{guards.get('max_notional_key')}**",
        f"- max_notional: **{float(guards.get('max_notional') or 0.0):.2f}**",
        f"- daily_loss_limit: **{float(guards.get('daily_loss_limit') or 0.0):.6f}**", "",
        "## Market Contract", "",
        f"- now_kst: **{market.get('now_kst')}**",
        f"- market_open_now: **{bool(market.get('market_open_now'))}**",
        f"- open_contract_ok: **{bool(market.get('open_contract_ok'))}**",
        f"- closed_contract_ok: **{bool(market.get('closed_contract_ok'))}**", "",
        "## Session Evidence", "",
        f"- event_total: **{int(events.get('event_total') or 0)}**",
        f"- verdict_total: **{int(events.get('verdict_total') or 0)}**",
        f"- execution_total: **{int(events.get('execution_total') or 0)}**",
        f"- error_total: **{int(events.get('error_total') or 0)}**", "",
        "## Checklist", "",
    ]
    for item in checklist:
        mark = "x" if bool(item.get("passed")) else " "
        lines.append(f"- [{mark}] {item.get('title')} | evidence={item.get('evidence')}")
    failures = out.get("failures") if isinstance(out.get("failures"), list) else []
    lines += ["", "## Failures", ""]
    if failures:
        for msg in failures:
            lines.append(f"- {msg}")
    else:
        lines.append("- (none)")
    lines.append("")
    return "\n".join(lines)
