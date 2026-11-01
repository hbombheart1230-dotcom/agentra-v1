from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.run_m26_ab_evaluation import main as ab_eval_main
from scripts.run_m26_dataset_manifest_check import main as manifest_main
from scripts.run_m26_promotion_gate_check import main as gate_main
from scripts.run_m26_replay_runner import main as replay_main
from scripts.run_m26_scorecard import main as scorecard_main
from libs.diagnostics.cli_capture import capture_cli_json


def _write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    from scripts.diagnostics import m26_closeout_jsonl_projection as _b07_1_owner
    return _b07_1_owner._write_jsonl(path, rows, facade=sys.modules[__name__])


def _run_json(main_fn, argv: List[str]) -> Tuple[int, Dict[str, Any]]:  # type: ignore[no-untyped-def]
    from scripts.diagnostics import m26_closeout_capture_projection as _b07_2_owner
    return _b07_2_owner._run_json(main_fn, argv, facade=sys.modules[__name__])


def _run_manifest_json(*, dataset_root: Path, seed_demo: bool) -> Tuple[int, Dict[str, Any]]:
    from scripts.diagnostics import m26_closeout_manifest_projection as _b7_owner
    return _b7_owner._run_manifest_json(dataset_root=dataset_root, seed_demo=seed_demo, facade=sys.modules[__name__])


def _run_replay_json(*, dataset_root: Path, day: str) -> Tuple[int, Dict[str, Any]]:
    from scripts.diagnostics import m26_closeout_replay_projection as _b8_owner
    return _b8_owner._run_replay_json(dataset_root=dataset_root, day=day, facade=sys.modules[__name__])


def _run_scorecard_json(*, dataset_root: Path, day: str) -> Tuple[int, Dict[str, Any]]:
    from scripts.diagnostics import m26_closeout_scorecard_projection as _b07_3_owner
    return _b07_3_owner._run_scorecard_json(dataset_root=dataset_root,day=day,facade=sys.modules[__name__])


def _run_ab_eval_json(*, base_root: Path, candidate_root: Path, day: str) -> Tuple[int, Dict[str, Any]]:
    from scripts.diagnostics import m26_closeout_ab_projection as _b07_4_owner
    return _b07_4_owner._run_ab_eval_json(base_root=base_root,candidate_root=candidate_root,day=day,facade=sys.modules[__name__])


def _run_gate_json(
    *,
    base_root: Path,
    candidate_root: Path,
    day: str,
    min_delta_total_pnl_proxy: float,
) -> Tuple[int, Dict[str, Any]]:
    from scripts.diagnostics import m26_closeout_gate_projection as _b07_5_owner
    return _b07_5_owner._run_gate_json(base_root=base_root,candidate_root=candidate_root,day=day,min_delta_total_pnl_proxy=min_delta_total_pnl_proxy,facade=sys.modules[__name__])


def _prepare_candidate_dataset(candidate_root: Path, *, day: str) -> None:
    from scripts.diagnostics import m26_closeout_candidate_projection as _c03_11_k4_owner
    return _c03_11_k4_owner._prepare_candidate_dataset(candidate_root, day=day, facade=sys.modules[__name__])


def _build_parser() -> argparse.ArgumentParser:
    from scripts.diagnostics import m26_closeout_parser_projection as _b6_owner
    return _b6_owner._build_parser(facade=sys.modules[__name__])


def main(argv: Optional[List[str]] = None) -> int:
    args = _build_parser().parse_args(argv)
    base_root = Path(str(args.base_dataset_root).strip())
    candidate_root = Path(str(args.candidate_dataset_root).strip())
    day = str(args.day or "2026-02-17").strip()

    if not bool(args.no_clear):
        if base_root.exists():
            shutil.rmtree(base_root, ignore_errors=True)
        if candidate_root.exists():
            shutil.rmtree(candidate_root, ignore_errors=True)

    base_root.mkdir(parents=True, exist_ok=True)
    candidate_root.mkdir(parents=True, exist_ok=True)

    m1_rc, m1_base = _run_manifest_json(dataset_root=base_root, seed_demo=True)
    m1c_rc, m1_candidate = _run_manifest_json(dataset_root=candidate_root, seed_demo=True)

    if not bool(args.inject_gate_fail):
        _prepare_candidate_dataset(candidate_root, day=day)

    m2_base_rc, m2_base = _run_replay_json(dataset_root=base_root, day=day)
    m2_candidate_rc, m2_candidate = _run_replay_json(dataset_root=candidate_root, day=day)

    m3_base_rc, m3_base = _run_scorecard_json(dataset_root=base_root, day=day)
    m3_candidate_rc, m3_candidate = _run_scorecard_json(dataset_root=candidate_root, day=day)

    m4_rc, m4 = _run_ab_eval_json(base_root=base_root, candidate_root=candidate_root, day=day)

    min_delta = float(args.min_delta_total_pnl_proxy)
    if bool(args.inject_gate_fail):
        min_delta = max(min_delta, 9999.0)
    m5_rc, m5 = _run_gate_json(
        base_root=base_root,
        candidate_root=candidate_root,
        day=day,
        min_delta_total_pnl_proxy=min_delta,
    )

    failures: List[str] = []
    checks = [
        ("m26_1_base", m1_rc, m1_base),
        ("m26_1_candidate", m1c_rc, m1_candidate),
        ("m26_2_base", m2_base_rc, m2_base),
        ("m26_2_candidate", m2_candidate_rc, m2_candidate),
        ("m26_3_base", m3_base_rc, m3_base),
        ("m26_3_candidate", m3_candidate_rc, m3_candidate),
        ("m26_4_ab", m4_rc, m4),
        ("m26_5_gate", m5_rc, m5),
    ]
    for name, rc, obj in checks:
        if int(rc) != 0:
            failures.append(f"{name} rc != 0")
        if obj and not bool(obj.get("ok")):
            failures.append(f"{name} ok != true")

    if isinstance(m4.get("comparison"), dict):
        winner = str((m4.get("comparison") or {}).get("winner") or "")
        if winner and winner != "candidate":
            failures.append("m26_4 winner != candidate")
    if isinstance(m5, dict):
        action = str(m5.get("recommended_action") or "")
        if action and action != "promote_candidate":
            failures.append("m26_5 recommended_action != promote_candidate")

    out = {
        "ok": len(failures) == 0,
        "day": day,
        "base_dataset_root": str(base_root),
        "candidate_dataset_root": str(candidate_root),
        "m26_1_manifest": {
            "base": {"rc": int(m1_rc), "ok": bool(m1_base.get("ok")) if isinstance(m1_base, dict) else False},
            "candidate": {"rc": int(m1c_rc), "ok": bool(m1_candidate.get("ok")) if isinstance(m1_candidate, dict) else False},
        },
        "m26_2_replay": {
            "base": {
                "rc": int(m2_base_rc),
                "ok": bool(m2_base.get("ok")) if isinstance(m2_base, dict) else False,
                "replayed_intent_total": int(m2_base.get("replayed_intent_total") or 0) if isinstance(m2_base, dict) else 0,
            },
            "candidate": {
                "rc": int(m2_candidate_rc),
                "ok": bool(m2_candidate.get("ok")) if isinstance(m2_candidate, dict) else False,
                "replayed_intent_total": int(m2_candidate.get("replayed_intent_total") or 0) if isinstance(m2_candidate, dict) else 0,
            },
        },
        "m26_3_scorecard": {
            "base": {
                "rc": int(m3_base_rc),
                "ok": bool(m3_base.get("ok")) if isinstance(m3_base, dict) else False,
                "total_pnl_proxy": float(m3_base.get("total_pnl_proxy") or 0.0) if isinstance(m3_base, dict) else 0.0,
            },
            "candidate": {
                "rc": int(m3_candidate_rc),
                "ok": bool(m3_candidate.get("ok")) if isinstance(m3_candidate, dict) else False,
                "total_pnl_proxy": float(m3_candidate.get("total_pnl_proxy") or 0.0) if isinstance(m3_candidate, dict) else 0.0,
            },
        },
        "m26_4_ab": {
            "rc": int(m4_rc),
            "ok": bool(m4.get("ok")) if isinstance(m4, dict) else False,
            "winner": str((m4.get("comparison") or {}).get("winner") or "") if isinstance(m4, dict) else "",
            "recommended_action": str(
                (((m4.get("comparison") or {}).get("promotion_gate") or {}).get("recommended_action") or "")
            )
            if isinstance(m4, dict)
            else "",
        },
        "m26_5_gate": {
            "rc": int(m5_rc),
            "ok": bool(m5.get("ok")) if isinstance(m5, dict) else False,
            "recommended_action": str(m5.get("recommended_action") or "") if isinstance(m5, dict) else "",
            "delta_total_pnl_proxy": float(((m5.get("values") or {}).get("delta_total_pnl_proxy") or 0.0))
            if isinstance(m5, dict)
            else 0.0,
        },
        "failures": failures,
    }

    if bool(args.json):
        print(json.dumps(out, ensure_ascii=False))
    else:
        print(
            f"ok={out['ok']} day={day} "
            f"ab_winner={out['m26_4_ab']['winner'] or 'n/a'} "
            f"gate_action={out['m26_5_gate']['recommended_action'] or 'n/a'} "
            f"delta_total_pnl_proxy={out['m26_5_gate']['delta_total_pnl_proxy']:.6f} "
            f"failure_total={len(failures)}"
        )
        for msg in failures:
            print(msg)

    return 0 if len(failures) == 0 else 3


if __name__ == "__main__":
    raise SystemExit(main())
