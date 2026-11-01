"""RF-037 A24-3: original (0d21ec48 preimage) vs thin ``strategies`` wrappers + ``strategy_episode_projection`` Owner.

Original decision bodies are extracted by AST from ``git show`` and compiled in an isolated namespace using the
same pure fakes that are patched onto the live ``strategies`` module. No IO/network; nothing enters ``sys.modules``.
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

PRE = "0d21ec48a82399ed41d3b3cfdd1d350dd8991076"
PATH = "libs/research/structural_alpha_batch2/strategies.py"
PRE_BLOB = "9da94362b140665b8a621b93b02ef4f5d6dfccb5"
strat = importlib.import_module("libs.research.structural_alpha_batch2.strategies")
owner = importlib.import_module("libs.research.structural_alpha_batch2.strategy_episode_projection")
GAP = strat.EPISODE_GAP_SEC
PROXY = strat.MARKET_PROXY_SYMBOLS


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


class Env:
    """Recording pure fakes shared by the original namespace and the live module."""

    def __init__(self):
        self.log = []

    def entry_bar(self, rows, *, decision_epoch, day, timestamps):
        self.log.append(("entry_bar", len(rows), decision_epoch, day, timestamps))
        return {"ts": decision_epoch, "price": 10.0} if rows else None

    def _episode(self, *, strategy_id, window, symbol, bar, features, index):
        self.log.append(("_episode", strategy_id, symbol, index))
        return {"strategy_id": strategy_id, "symbol": symbol, "index": index, "bar": bar,
                "epoch": window.get("decision_epoch"), "feature_keys": list(features)}

    def market_return_15m(self, rows, *, decision_epoch, day, timestamps):
        self.log.append(("market_return_15m", decision_epoch))
        return rows[0].get("mret") if rows else None

    def relative_strength_features(self, rows, *, decision_epoch, day, timestamps):
        self.log.append(("rsf", decision_epoch))
        return dict(rows[0].get("rs") or {}) if rows else {"available": False}


@pytest.fixture(scope="module")
def originals():
    try:
        raw = subprocess.run(["git", "show", f"{PRE}:{PATH}"], check=True, capture_output=True).stdout
    except subprocess.CalledProcessError as exc:
        pytest.fail(f"BLOCKED_PIN: {exc.stderr!r}")
    assert _sha(raw) == PRE_BLOB, "BLOCKED_PIN original blob"
    tree = ast.parse(raw.decode("utf-8"))
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef)
             and n.name in ("_build_local_episodes", "build_market_shock_reversal_episodes")]
    assert len(nodes) == 2
    return nodes


def _orig_ns(originals, env):
    ns = {"Any": object, "Callable": object, "Mapping": object, "FeatureBuilder": object,
          "EPISODE_GAP_SEC": GAP, "MARKET_PROXY_SYMBOLS": PROXY,
          "_timestamps": strat._timestamps, "entry_bar": env.entry_bar, "_episode": env._episode,
          "market_return_15m": env.market_return_15m, "relative_strength_features": env.relative_strength_features}
    mod = ast.Module(body=copy.deepcopy(originals), type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), f"<{PRE[:8]}:{PATH}>", "exec"), ns)
    return ns


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(Path, "mkdir", boom)
    monkeypatch.setattr(Path, "write_text", boom)


def _live(monkeypatch, env):
    monkeypatch.setattr(strat, "entry_bar", env.entry_bar)
    monkeypatch.setattr(strat, "_episode", env._episode)
    monkeypatch.setattr(strat, "market_return_15m", env.market_return_15m)
    monkeypatch.setattr(strat, "relative_strength_features", env.relative_strength_features)


def _run_both(originals, monkeypatch, name, *args, **kwargs):
    env_o, env_n = Env(), Env()
    ns = _orig_ns(originals, env_o)
    _live(monkeypatch, env_n)
    a_args, b_args = copy.deepcopy((args, kwargs)), copy.deepcopy((args, kwargs))
    got = {}
    for label, fn, (aa, kk) in (("orig", ns[name], a_args), ("new", getattr(strat, name), b_args)):
        try:
            got[label] = ("ok", fn(*aa, **kk))
        except Exception as exc:  # compare class + message
            got[label] = ("err", type(exc), str(exc))
        assert (aa, kk) == (args, kwargs), f"{label} mutated input"
    assert got["orig"] == got["new"]
    assert env_o.log == env_n.log
    return got["new"], env_n


def _rows(**kw):
    return [dict(kw)]


def _fb(table):
    def feature_builder(rows, *, decision_epoch, day, timestamps):
        if not rows:
            return {"available": False}
        return dict(table[rows[0]["sym"]])
    return feature_builder


def _local_kwargs(table, windows_syms, **extra):
    rows = {s: _rows(sym=s) for s in table}
    return dict(minute_rows_by_symbol=rows, strategy_id="S_TEST", feature_builder=_fb(table),
                eligible=lambda r: r.get("ok", True), selection_key=lambda r: (r["score"], r["symbol"]), **extra)


def test_l1_local_empty_and_no_candidate(originals, monkeypatch, guards):
    kw = _local_kwargs({"A": {"available": True, "score": 1.0}}, None)
    out, _ = _run_both(originals, monkeypatch, "_build_local_episodes", [], **kw)
    assert out == ("ok", [])
    kw["eligible"] = lambda r: False
    out, _ = _run_both(originals, monkeypatch, "_build_local_episodes",
                       [{"decision_epoch": 100, "day": "d", "candidates": [{"symbol": "A"}]}], **kw)
    assert out == ("ok", [])


def test_l2_local_tie_and_gap_suppression(originals, monkeypatch, guards):
    table = {"A": {"available": True, "score": 2.0}, "B": {"available": True, "score": 2.0},
             "C": {"available": False, "score": 9.0}}
    cands = [{"symbol": s} for s in ("A", "B", "C")]
    windows = [{"decision_epoch": 1000, "day": "d", "candidates": cands},
               {"decision_epoch": 1000 + GAP - 1, "day": "d", "candidates": cands},
               {"decision_epoch": 1000 + GAP, "day": "d", "candidates": cands}]
    out, env = _run_both(originals, monkeypatch, "_build_local_episodes", windows, **_local_kwargs(table, None))
    status, eps = out
    assert status == "ok" and [e["index"] for e in eps] == [1, 2]
    assert [e["symbol"] for e in eps] == ["B", "B"]  # tie on score -> larger symbol
    assert [e["epoch"] for e in eps] == [1000, 1000 + GAP]
    assert list(eps[0]) == ["strategy_id", "symbol", "index", "bar", "epoch", "feature_keys"]


def test_l3_local_missing_bar_and_error(originals, monkeypatch, guards):
    table = {"A": {"available": True, "score": 1.0}}
    kw = _local_kwargs(table, None)
    kw["minute_rows_by_symbol"] = {"A": []}
    kw["feature_builder"] = lambda rows, **k: {"available": True, "score": 1.0}
    out, _ = _run_both(originals, monkeypatch, "_build_local_episodes",
                       [{"decision_epoch": 5, "day": "d", "candidates": [{"symbol": "A"}]}], **kw)
    assert out == ("ok", [])

    def bad(rows, **k):
        raise ValueError("boom")
    kw["feature_builder"] = bad
    out, _ = _run_both(originals, monkeypatch, "_build_local_episodes",
                       [{"decision_epoch": 5, "day": "d", "candidates": [{"symbol": "A"}]}], **kw)
    assert out[0] == "err" and out[1] is ValueError and out[2] == "boom"


def _market_rows(mret, rs_by_symbol):
    rows = {PROXY[0]: [{"mret": mret}], PROXY[1]: [{"mret": mret}]}
    for sym, rs in rs_by_symbol.items():
        rows[sym] = [{"rs": rs}]
    return rows


GOOD = {"available": True, "return_5m_pct": 1.0, "volume_ratio": 1.5, "above_vwap": True}


def test_m1_m2_no_proxy_or_not_negative_enough(originals, monkeypatch, guards):
    w = [{"decision_epoch": 1, "day": "d", "candidates": [{"symbol": "X"}]}]
    out, _ = _run_both(originals, monkeypatch, "build_market_shock_reversal_episodes", w,
                       minute_rows_by_symbol={"X": [{"rs": GOOD}]})
    assert out == ("ok", [])
    out, _ = _run_both(originals, monkeypatch, "build_market_shock_reversal_episodes", w,
                       minute_rows_by_symbol=_market_rows(-0.7, {"X": GOOD}))
    assert out == ("ok", [])
    # boundary: -0.75 is NOT skipped (condition is `> -0.75`), so an episode is produced on both sides
    out, _ = _run_both(originals, monkeypatch, "build_market_shock_reversal_episodes", w,
                       minute_rows_by_symbol=_market_rows(-0.75, {"X": GOOD}))
    assert out[0] == "ok" and len(out[1]) == 1


def test_m3_negative_proxy_valid_candidates_and_tie(originals, monkeypatch, guards):
    w = [{"decision_epoch": 1, "day": "d", "candidates": [{"symbol": s} for s in ("X", "Y", "Z", "W")]}]
    rows = _market_rows(-1.0, {"X": GOOD, "Y": GOOD,
                               "Z": dict(GOOD, volume_ratio=1.0),
                               "W": dict(GOOD, above_vwap=False)})
    out, env = _run_both(originals, monkeypatch, "build_market_shock_reversal_episodes", w,
                         minute_rows_by_symbol=rows)
    status, eps = out
    assert status == "ok" and len(eps) == 1
    assert eps[0]["symbol"] == "Y"  # tie on relative strength -> larger symbol
    assert eps[0]["strategy_id"] == "H7_MARKET_SHOCK_RELATIVE_STRENGTH_REVERSAL"
    assert eps[0]["feature_keys"][-2:] == ["market_return_15m_pct", "relative_strength_pct"]
    order = [c[0] for c in env.log]
    assert order.index("market_return_15m") < order.index("rsf") < order.index("entry_bar") < order.index("_episode")


def test_m4_market_missing_bar(originals, monkeypatch, guards):
    w = [{"decision_epoch": 1, "day": "d", "candidates": [{"symbol": "X"}]}]
    rows = _market_rows(-1.0, {})
    rows["X"] = [{"rs": GOOD}]
    # entry_bar fake returns None when rows empty; make X rows non-empty but force None via patched fake below
    env_o, env_n = Env(), Env()
    for env in (env_o, env_n):
        env.entry_bar = (lambda e: (lambda rows, **k: (e.log.append(("entry_bar", None)) or None)))(env)
    ns = _orig_ns(originals, env_o)
    _live(monkeypatch, env_n)
    a = ns["build_market_shock_reversal_episodes"](copy.deepcopy(w), minute_rows_by_symbol=copy.deepcopy(rows))
    b = strat.build_market_shock_reversal_episodes(copy.deepcopy(w), minute_rows_by_symbol=copy.deepcopy(rows))
    assert a == b == [] and env_o.log == env_n.log


def test_s1_use_time_seams(monkeypatch, guards):
    env = Env()
    _live(monkeypatch, env)
    calls = []
    monkeypatch.setattr(strat, "EPISODE_GAP_SEC", 5)
    monkeypatch.setattr(strat, "_timestamps", lambda rows: calls.append("ts") or {})
    kw = _local_kwargs({"A": {"available": True, "score": 1.0}}, None)
    w = [{"decision_epoch": 100, "day": "d", "candidates": [{"symbol": "A"}]},
         {"decision_epoch": 106, "day": "d", "candidates": [{"symbol": "A"}]}]
    eps = strat._build_local_episodes(w, **kw)
    assert calls == ["ts"] and len(eps) == 2  # gap read from facade at call time (5s)


def test_s2_thin_wrappers_single_owner():
    for fn in (strat._build_local_episodes, strat.build_market_shock_reversal_episodes):
        node = ast.parse(inspect.getsource(fn)).body[0]
        assert len(node.body) == 1 and isinstance(node.body[0], ast.Return)
        assert not [n for n in ast.walk(node) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp))]
    own = inspect.getsource(owner)
    assert "from .strategies" not in own and "import strategies" not in own
    assert owner._build_local_episodes.__module__ == owner.__name__
