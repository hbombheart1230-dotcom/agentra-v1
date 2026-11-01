"""RF-025 A27-7/8: controlled_mock_lanes coordinator ``_pending_buy_symbols`` / ``_intent``, original vs wrapper + Owner.

Pure projections over supplied dicts. No order/ledger/Step5C/Guard execution, no live entrypoint; IO guarded.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import inspect
import socket
import subprocess
from pathlib import Path

import pytest

PRE = "8ea0702dcc322caae176c0eab9d7349a1fbeed20"
PATH = "libs/runtime/controlled_mock_lanes/coordinator.py"
PRE_BLOB = "19d95a08c39dda4a9136a1ff1d4608169eb6e53e"
NAMES = ["_pending_buy_symbols", "_intent"]
coord = importlib.import_module("libs.runtime.controlled_mock_lanes.coordinator")
OWNERS = {n: importlib.import_module(f"libs.runtime.controlled_mock_lanes.coordinator_{n.lstrip('_')}") for n in NAMES}


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    try:
        raw = subprocess.run(["git", "show", f"{PRE}:{PATH}"], check=True, capture_output=True).stdout
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(raw) == PRE_BLOB, "BLOCKED_PIN original blob"
    tree = ast.parse(raw.decode("utf-8"))
    nodes = {n.name: n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in NAMES}
    assert sorted(nodes) == sorted(NAMES)
    return nodes


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(Path, "mkdir", boom)
    monkeypatch.setattr(Path, "write_text", boom)
    # protected effect entrypoints must never run
    for fn in ("inject_controlled_mock_lane_intent", "finalize_controlled_mock_lane_submission"):
        if hasattr(coord, fn):
            monkeypatch.setattr(coord, fn, boom)
    for fn in ("record_accepted_submission", "record_attempt", "record_evaluations"):
        monkeypatch.setattr(coord, fn, boom)


def check(orig_nodes, monkeypatch, name, *args, overrides=None):
    ns = dict(vars(coord))
    mod = ast.Module(body=[copy.deepcopy(orig_nodes[name])], type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), f"<{PRE[:8]}:{PATH}>", "exec"), ns)
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(coord, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[name]), ("new", getattr(coord, name))):
        a = copy.deepcopy(args)
        try:
            values[label] = fn(*a)
            got[label] = ("ok", repr(values[label]))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert repr(a) == repr(args), f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


# ---- A27-7 _pending_buy_symbols ----
def order(**kw):
    base = {"symbol": "005930", "side": "BUY", "qty": 3}
    base.update(kw)
    return base


STATES = [
    {},
    {"account_orders": [order()]},
    {"account_orders": {"o1": order(symbol="A005930"), "o2": order(symbol="000660", side="SELL")}},
    {"portfolio_snapshot": {"orders": [order(action="buy", side="")]}},
    {"persisted_state": {"pending_unfilled_orders": [order(ord_dvsn_name="현금매수", side="", qty=0, unfilled_qty=2)]}},
    {"account_orders": [order(qty=0), order(symbol="", stk_cd="035420"), order(symbol=None, code="051910", remaining_qty="4")]},
    {"account_orders": [order(rmn_qty="0", qty=5)]},
    {"account_orders": ["bad", None, 5, order(symbol="  ")], "portfolio_snapshot": "bad", "persisted_state": []},
    {"account_orders": [order(side="매도")], "portfolio_snapshot": {"orders": [order(side="Buy", symbol="b1")]},
     "persisted_state": {"pending_unfilled_orders": {"x": order(symbol="b2"), "y": order(symbol="b1")}}},
    {"account_orders": [order(qty="abc")]},
    {"account_orders": None, "portfolio_snapshot": {"orders": None}},
]


@pytest.mark.parametrize("state", STATES)
def test_pending_buy_symbols(orig_nodes, monkeypatch, guards, state):
    check(orig_nodes, monkeypatch, "_pending_buy_symbols", state)


def test_pending_buy_symbols_values(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_pending_buy_symbols", STATES[8])
    assert out == {"B1", "B2"}
    assert check(orig_nodes, monkeypatch, "_pending_buy_symbols", {}) == set()


def test_pending_buy_symbols_helper_patch(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_pending_buy_symbols", {"account_orders": [order()]},
                overrides={"normalize_symbol": lambda v: f"N:{v}", "_int": lambda v, default=0: 9})
    assert out == {"N:005930"}


# ---- A27-8 _intent ----
CANDS = [
    {"lane_id": "q12", "symbol": "005930", "price": 71000.0},
    {"lane_id": "q10_index", "symbol": "A000660", "price": None, "horizon": "overnight_probe", "extra": {"n": 1}},
    {},
    {"lane_id": "  ", "symbol": "", "horizon": "scalp"},
]


@pytest.mark.parametrize("candidate", CANDS)
def test_intent(orig_nodes, monkeypatch, guards, candidate):
    check(orig_nodes, monkeypatch, "_intent", candidate)


def test_intent_shape_and_key_order(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_intent", CANDS[0])
    assert list(out) == ["symbol", "side", "qty", "price", "risk_score", "confidence", "thesis", "meta"]
    assert out["side"] == "BUY" and out["qty"] == coord.DEFAULT_ORDER_QTY and out["thesis"].endswith("q12")
    assert list(out["meta"]) == ["entry_signal_source", "entry_lane", "entry_reason", "controlled_mock_lane",
                                 "position_strategy_snapshot", "price", "current_price", "order_price_source"]
    lane = out["meta"]["controlled_mock_lane"]
    assert lane["schema_version"] == coord.SCHEMA_VERSION and lane["daily_limit"] == 1
    assert lane["submission_state"] == "PENDING_BROKER_RESULT" and out["meta"]["entry_lane"] == "controlled_mock:q12"


def test_intent_strategy_snapshot_patch(orig_nodes, monkeypatch, guards):
    seen = []
    out = check(orig_nodes, monkeypatch, "_intent", CANDS[1],
                overrides={"_strategy_snapshot": lambda c: seen.append(dict(c)) or {"patched": True},
                           "normalize_symbol": lambda v: "NORM"})
    assert out["meta"]["position_strategy_snapshot"] == {"patched": True} and out["symbol"] == "NORM" and seen


@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(coord, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.Dict))]
    owner_fn = getattr(OWNERS[name], name)
    assert len(list(ast.walk(ast.parse(inspect.getsource(owner_fn)).body[0]))) > 30
    assert owner_fn.__module__ == OWNERS[name].__name__
    assert "coordinator import" not in inspect.getsource(OWNERS[name])
