from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.runtime.portfolio_allocation import allocate_portfolio_budget
from libs.runtime.portfolio_budget_guard import apply_portfolio_budget_guard


def _build_parser() -> argparse.ArgumentParser:
    from scripts.diagnostics import m27_budget_parser_projection as owner
    return owner._build_parser(facade=sys.modules[__name__])


def _profiles() -> List[Dict[str, Any]]:
    from scripts.diagnostics import m27_budget_profiles_projection as owner
    return owner._profiles(facade=sys.modules[__name__])


def _intents(*, inject_fail: bool) -> List[Dict[str, Any]]:
    from scripts.diagnostics import m27_budget_intents_projection as owner
    return owner._intents(inject_fail=inject_fail, facade=sys.modules[__name__])


def _symbol_caps(*, inject_fail: bool) -> Dict[str, float]:
    from scripts.diagnostics import m27_budget_caps_projection as owner
    return owner._symbol_caps(inject_fail=inject_fail, facade=sys.modules[__name__])


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    inject_fail = bool(args.inject_fail)

    allocation = allocate_portfolio_budget(
        _profiles(),
        total_notional=2000.0,
        reserve_ratio=0.0,
    )

    out_guard = apply_portfolio_budget_guard(
        _intents(inject_fail=inject_fail),
        allocation_result=allocation,
        symbol_max_notional_map=_symbol_caps(inject_fail=inject_fail),
    )

    failures: List[str] = list(out_guard.get("failures") or [])
    reason_counts = (
        out_guard.get("blocked_reason_counts") if isinstance(out_guard.get("blocked_reason_counts"), dict) else {}
    )

    if not bool(allocation.get("ok")):
        failures.append("allocation ok != true")
    if int(out_guard.get("approved_total") or 0) < 1:
        failures.append("approved_total < 1")
    if int(reason_counts.get("strategy_budget_exceeded") or 0) < 1:
        failures.append("strategy_budget_exceeded not observed")
    if int(reason_counts.get("opposite_side_conflict") or 0) < 1:
        failures.append("opposite_side_conflict not observed")
    if int(reason_counts.get("symbol_notional_cap_exceeded") or 0) < 1:
        failures.append("symbol_notional_cap_exceeded not observed")

    out = {
        "ok": len(failures) == 0,
        "inject_fail": inject_fail,
        "allocation": {
            "ok": bool(allocation.get("ok")),
            "active_strategy_total": int(allocation.get("active_strategy_total") or 0),
            "allocation_total": float(allocation.get("allocation_total") or 0.0),
            "allocations": allocation.get("allocations") or [],
        },
        "guard": {
            "ok": bool(out_guard.get("ok")),
            "intent_total": int(out_guard.get("intent_total") or 0),
            "budget_screened_total": int(out_guard.get("budget_screened_total") or 0),
            "approved_total": int(out_guard.get("approved_total") or 0),
            "blocked_total": int(out_guard.get("blocked_total") or 0),
            "blocked_reason_counts": reason_counts,
            "strategy_budget": out_guard.get("strategy_budget") or {},
        },
        "failure_total": len(failures),
        "failures": failures,
    }

    if bool(args.json):
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(
            f"ok={out['ok']} intent_total={out['guard']['intent_total']} "
            f"approved_total={out['guard']['approved_total']} blocked_total={out['guard']['blocked_total']} "
            f"failure_total={out['failure_total']}"
        )
        for msg in failures:
            print(msg)

    return 0 if len(failures) == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
