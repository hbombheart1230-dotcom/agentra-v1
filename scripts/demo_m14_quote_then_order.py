# scripts/demo_m15_smoke.py
from __future__ import annotations

import argparse
import inspect
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from libs.core.settings import Settings
from libs.skills.runner import CompositeSkillRunner
from libs.supervisor.two_phase import TwoPhaseSupervisor
from libs.supervisor.intent_store import IntentStore
from libs.agent.executor.executor_agent import ExecutorAgent


def _ensure_parent(p: Path) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)


def _write_jsonl(path: Path, obj: Dict[str, Any]) -> None:
    _ensure_parent(path)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _clear_file(p: Path) -> None:
    if p.exists():
        p.unlink(missing_ok=True)


def _env_bool(name: str, default: str = "false") -> bool:
    return (os.getenv(name, default) or default).strip().lower() == "true"


def _env_int(name: str, default: int) -> int:
    raw = (os.getenv(name, "") or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except Exception:
        return default


def _resolve_approval_mode() -> str:
    """
    Priority:
      1) APPROVAL_MODE if set/non-empty
      2) AUTO_APPROVE legacy if set (true->auto, false->manual)
      3) default manual
    """
    raw = os.getenv("APPROVAL_MODE")
    if raw is not None and raw.strip():
        return raw.strip().lower()

    legacy = os.getenv("AUTO_APPROVE")
    if legacy is not None and legacy.strip():
        return "auto" if legacy.strip().lower() == "true" else "manual"

    return "manual"


def _call_agent_method(agent: Any, method_name: str, **kwargs) -> Any:
    """
    Robustly call agent.<method_name>(...) even if signature differs between versions.
    It will:
      - inspect signature
      - pass only accepted kwargs
      - if it accepts no kwargs, call without args
    """
    fn = getattr(agent, method_name)
    sig = inspect.signature(fn)
    params = sig.parameters

    # If method has no parameters except self -> call with no args
    # NOTE: bound method signature does not include self in params
    if len(params) == 0:
        return fn()

    # Filter kwargs to only those accepted
    accepted = {}
    for k, v in kwargs.items():
        if k in params:
            accepted[k] = v

    return fn(**accepted)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--clear", action="store_true", help="Clear demo jsonl logs before running")
    args = ap.parse_args()

    cfg = Settings.from_env()

    kiwoom_mode = (os.getenv("KIWOOM_MODE", "mock") or "mock").strip().lower()
    approval_mode = _resolve_approval_mode()
    execution_enabled = _env_bool("EXECUTION_ENABLED", "false")

    demo_symbol = (os.getenv("DEMO_SYMBOL", "005930") or "005930").strip()
    demo_qty = _env_int("DEMO_QTY", 1)

    # If DEMO_PRICE is set (>0), we use a limit order for notional guard tests
    demo_price = _env_int("DEMO_PRICE", 0)
    if demo_price > 0:
        order_type = "limit"
        price = demo_price
    else:
        order_type = "market"
        price = None

    # For manual path regression: if DEMO_DO_APPROVE=true and decision is needs_approval, call approve()
    do_approve = _env_bool("DEMO_DO_APPROVE", "false")

    data_dir = ROOT / "data"
    intents_path = data_dir / "m15_demo_intents.jsonl"
    events_path = data_dir / "m15_demo_events.jsonl"

    if args.clear:
        _clear_file(intents_path)
        _clear_file(events_path)

    print("=== M15 Smoke Demo ===")
    print(f"KIWOOM_MODE={kiwoom_mode} EXECUTION_ENABLED={execution_enabled} APPROVAL_MODE={approval_mode}")
    print(f"AUTO_APPROVE={os.getenv('AUTO_APPROVE')}")
    print(f"DEMO_SYMBOL={demo_symbol} DEMO_QTY={demo_qty} DEMO_PRICE={demo_price} DEMO_DO_APPROVE={do_approve}")
    print(f"intents: {intents_path}")
    print(f"events : {events_path}")

    runner = CompositeSkillRunner(settings=cfg, event_log_path=str(events_path))
    supervisor = TwoPhaseSupervisor(cfg)
    store = IntentStore(str(intents_path))

    # Repo requires both intent_store and intent_store_path
    agent = ExecutorAgent(
        runner=runner,
        supervisor=supervisor,
        intent_store=store,
        intent_store_path=str(intents_path),
    )

    # ---- intent1 (buy) ----
    res1 = _call_agent_method(
        agent,
        "submit_order_intent",
        side="buy",
        symbol=demo_symbol,
        qty=demo_qty,
        order_type=order_type,
        price=price,
        rationale="m15 smoke demo/intent1",
        approval_mode=approval_mode,
        execution_enabled=execution_enabled,
    )
    print("\n[intent1/submit]", res1)
    _write_jsonl(events_path, {"tag": "intent1_submit", "result": res1})

    intent_id_1 = res1["decision"]["intent"]["intent_id"]
    status_1 = res1["decision"]["status"]

    # preview / last / list
    prev = _call_agent_method(agent, "preview", intent_id=intent_id_1)
    print("\n[preview]", prev)
    print("\n[last_intent]", _call_agent_method(agent, "last_intent"))
    print("\n[list_intents]", _call_agent_method(agent, "list_intents", limit=50))

    # manual approve regression (optional)
    if do_approve and status_1 == "needs_approval":
        appr = _call_agent_method(agent, "approve", intent_id=intent_id_1)
        print("\n[approve]", appr)
        _write_jsonl(events_path, {"tag": "intent1_approve", "result": appr})

    # reject
    rej = _call_agent_method(agent, "reject", intent_id=intent_id_1, reason="demo reject")
    print("\n[reject]", rej)

    # ---- intent2 (sell) ----
    res2 = _call_agent_method(
        agent,
        "submit_order_intent",
        side="sell",
        symbol=demo_symbol,
        qty=demo_qty,
        order_type=order_type,
        price=price,
        rationale="m15 smoke demo/intent2",
        approval_mode=approval_mode,
        execution_enabled=execution_enabled,
    )
    print("\n[intent2/submit]", res2)
    _write_jsonl(events_path, {"tag": "intent2_submit", "result": res2})

    intent_id_2 = res2["decision"]["intent"]["intent_id"]
    status_2 = res2["decision"]["status"]
    if do_approve and status_2 == "needs_approval":
        appr2 = _call_agent_method(agent, "approve", intent_id=intent_id_2)
        print("\n[intent2/approve]", appr2)
        _write_jsonl(events_path, {"tag": "intent2_approve", "result": appr2})

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
