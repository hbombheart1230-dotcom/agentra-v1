from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.runtime.intent_conflict_resolver import resolve_intent_conflicts


def _build_parser() -> argparse.ArgumentParser:
    from scripts.diagnostics import m27_conflict_parser_projection as o
    return o._build_parser(facade=sys.modules[__name__])


def _default_intents(*, inject_fail: bool) -> List[Dict[str, Any]]:
    from scripts.diagnostics import m27_conflict_intents_projection as _c03_11_b7_owner
    return _c03_11_b7_owner._default_intents(inject_fail=inject_fail, facade=sys.modules[__name__])


def _default_caps(*, inject_fail: bool) -> Dict[str, float]:
    from scripts.diagnostics import m27_conflict_caps_projection as o
    return o._default_caps(inject_fail=inject_fail,facade=sys.modules[__name__])


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    inject_fail = bool(args.inject_fail)

    intents = _default_intents(inject_fail=inject_fail)
    caps = _default_caps(inject_fail=inject_fail)
    result = resolve_intent_conflicts(
        intents,
        default_symbol_max_notional=0.0,
        symbol_max_notional_map=caps,
    )

    reason_counts = result.get("blocked_reason_counts") if isinstance(result.get("blocked_reason_counts"), dict) else {}
    failures: List[str] = list(result.get("failures") or [])

    if int(result.get("approved_total") or 0) < 1:
        failures.append("approved_total < 1")
    if int(reason_counts.get("opposite_side_conflict") or 0) < 1:
        failures.append("opposite_side_conflict not observed")
    if int(reason_counts.get("symbol_notional_cap_exceeded") or 0) < 1:
        failures.append("symbol_notional_cap_exceeded not observed")

    out = {
        "ok": len(failures) == 0,
        "inject_fail": inject_fail,
        "intent_total": int(result.get("intent_total") or 0),
        "approved_total": int(result.get("approved_total") or 0),
        "blocked_total": int(result.get("blocked_total") or 0),
        "invalid_total": int(result.get("invalid_total") or 0),
        "blocked_reason_counts": reason_counts,
        "failure_total": len(failures),
        "failures": failures,
    }
    if bool(args.json):
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(
            f"ok={out['ok']} intent_total={out['intent_total']} approved_total={out['approved_total']} "
            f"blocked_total={out['blocked_total']} invalid_total={out['invalid_total']} failure_total={out['failure_total']}"
        )
        for msg in failures:
            print(msg)
    return 0 if len(failures) == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
