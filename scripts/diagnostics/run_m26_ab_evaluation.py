from __future__ import annotations

import argparse
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_m26_scorecard import main as scorecard_main


def _as_float(v: Any, default: float = 0.0) -> float:
    from scripts.diagnostics import m26_ab_float_projection as _b4_owner
    return _b4_owner._as_float(v, default)


def _json_path_get(obj: Dict[str, Any], path: str, default: float = 0.0) -> float:
    from scripts.diagnostics import m26_ab_path_projection as _b5_owner
    return _b5_owner._json_path_get(obj, path, default, facade=sys.modules[__name__])


def _run_scorecard_json(*, dataset_root: Path, day: str) -> Tuple[int, Dict[str, Any]]:
    from scripts.diagnostics import m26_ab_scorecard_projection as _b8_owner
    return _b8_owner._run_scorecard_json(dataset_root=dataset_root, day=day, facade=sys.modules[__name__])


def _build_parser() -> argparse.ArgumentParser:
    from scripts.diagnostics import m26_ab_parser_projection as _b6_owner
    return _b6_owner._build_parser(facade=sys.modules[__name__])


def _compare_metrics(
    *,
    a_label: str,
    b_label: str,
    a_score: Dict[str, Any],
    b_score: Dict[str, Any],
) -> Dict[str, Any]:
    from scripts.diagnostics import m26_ab_compare_projection as _b7_owner
    return _b7_owner._compare_metrics(a_label=a_label, b_label=b_label, a_score=a_score, b_score=b_score, facade=sys.modules[__name__])


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    a_root = Path(str(args.a_dataset_root).strip())
    b_root = Path(str(args.b_dataset_root).strip())
    a_label = str(args.a_label or "A").strip() or "A"
    b_label = str(args.b_label or "B").strip() or "B"
    day = str(args.day or "").strip()

    failures: List[str] = []
    a_rc, a_obj = _run_scorecard_json(dataset_root=a_root, day=day)
    b_rc, b_obj = _run_scorecard_json(dataset_root=b_root, day=day)

    if a_rc != 0:
        failures.append("a_scorecard rc != 0")
    if b_rc != 0:
        failures.append("b_scorecard rc != 0")
    if a_obj and not bool(a_obj.get("ok")):
        failures.append("a_scorecard ok != true")
    if b_obj and not bool(b_obj.get("ok")):
        failures.append("b_scorecard ok != true")

    comparison: Dict[str, Any] = {}
    if not failures:
        comparison = _compare_metrics(a_label=a_label, b_label=b_label, a_score=a_obj, b_score=b_obj)

    out = {
        "ok": len(failures) == 0,
        "day": day,
        "a": {
            "label": a_label,
            "dataset_root": str(a_root),
            "rc": int(a_rc),
            "ok": bool(a_obj.get("ok")) if isinstance(a_obj, dict) else False,
            "total_pnl_proxy": _json_path_get(a_obj if isinstance(a_obj, dict) else {}, "total_pnl_proxy", 0.0),
            "sortino_proxy": _json_path_get(a_obj if isinstance(a_obj, dict) else {}, "risk_adjusted.sortino_proxy", 0.0),
            "max_drawdown_ratio": _json_path_get(
                a_obj if isinstance(a_obj, dict) else {},
                "drawdown.max_drawdown_ratio",
                0.0,
            ),
            "win_rate": _json_path_get(a_obj if isinstance(a_obj, dict) else {}, "win_rate", 0.0),
        },
        "b": {
            "label": b_label,
            "dataset_root": str(b_root),
            "rc": int(b_rc),
            "ok": bool(b_obj.get("ok")) if isinstance(b_obj, dict) else False,
            "total_pnl_proxy": _json_path_get(b_obj if isinstance(b_obj, dict) else {}, "total_pnl_proxy", 0.0),
            "sortino_proxy": _json_path_get(b_obj if isinstance(b_obj, dict) else {}, "risk_adjusted.sortino_proxy", 0.0),
            "max_drawdown_ratio": _json_path_get(
                b_obj if isinstance(b_obj, dict) else {},
                "drawdown.max_drawdown_ratio",
                0.0,
            ),
            "win_rate": _json_path_get(b_obj if isinstance(b_obj, dict) else {}, "win_rate", 0.0),
        },
        "comparison": comparison,
        "failure_total": len(failures),
        "failures": failures,
    }

    if bool(args.json):
        print(json.dumps(out, ensure_ascii=False))
    else:
        winner = (comparison.get("winner") if isinstance(comparison, dict) else "") or "n/a"
        rec = (
            ((comparison.get("promotion_gate") or {}).get("recommended_action"))
            if isinstance(comparison, dict)
            else ""
        ) or "n/a"
        print(
            f"ok={out['ok']} winner={winner} recommended_action={rec} "
            f"a_total_pnl={out['a']['total_pnl_proxy']:.6f} b_total_pnl={out['b']['total_pnl_proxy']:.6f} "
            f"failure_total={out['failure_total']}"
        )
        for msg in list(out.get("failures") or []):
            print(msg)
    return 0 if len(failures) == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
