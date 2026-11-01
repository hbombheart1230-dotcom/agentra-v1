"""RF-039 A25-9: original (d58cc171 preimage, blob 8b79cb43) vs thin ``analysis`` wrappers + 8 Owners.

The eight original function ASTs are extracted from ``git show`` and compiled together in one isolated namespace
whose module-level dependencies are the same objects (or the same overrides) used by the live ``analysis`` module.
Pure computation only: socket/subprocess/Path writes are guarded. Nothing is registered in ``sys.modules``.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import importlib
import inspect
import socket
import subprocess
from collections import Counter, defaultdict
from pathlib import Path
from statistics import median

import pytest

PRE = "d58cc171353ed3f6f1092d05d1d476ea80ddf48a"
PATH = "libs/research/existing_evidence_mining/analysis.py"
PRE_BLOB = "8b79cb4376757d738f02f26ad5aeca84a1c024a3"
NAMES = ["blocked_opportunity_analysis", "actual_trade_analysis", "summarize_rows", "discovery_cohorts",
         "score_component_diagnostics", "grouped_horizon_summary", "split_summary", "simulate_path_policies"]
analysis = importlib.import_module("libs.research.existing_evidence_mining.analysis")
OWNERS = {n: importlib.import_module(f"libs.research.existing_evidence_mining.analysis_{n}") for n in NAMES}
H = analysis.HORIZONS


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
    nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in NAMES]
    assert sorted(n.name for n in nodes) == sorted(NAMES)
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


def _ns(orig_nodes, overrides, under_test):
    ns = {"Any": object, "Iterable": object, "Mapping": dict, "defaultdict": defaultdict, "Counter": Counter,
          "median": median, "performance_metrics": analysis.performance_metrics, "HORIZONS": analysis.HORIZONS,
          "LIVE_COST_PCT": analysis.LIVE_COST_PCT, "PATH_POLICIES": analysis.PATH_POLICIES,
          "PRIMARY_HORIZON": analysis.PRIMARY_HORIZON, "_observed_return": analysis._observed_return}
    ns.update(overrides)
    mod = ast.Module(body=copy.deepcopy(orig_nodes), type_ignores=[])
    exec(compile(ast.fix_missing_locations(mod), f"<{PRE[:8]}:{PATH}>", "exec"), ns)
    for k, v in overrides.items():  # dependency overrides replace the compiled original binding
        if k != under_test:
            ns[k] = v
    return ns


def check(orig_nodes, monkeypatch, name, args=(), kwargs=None, overrides=None):
    kwargs = kwargs or {}
    overrides = overrides or {}
    ns = _ns(orig_nodes, overrides, name)
    for k, v in overrides.items():
        monkeypatch.setattr(analysis, k, v)
    got = {}
    for label, fn in (("orig", ns[name]), ("new", getattr(analysis, name))):
        a, k = copy.deepcopy((args, kwargs))
        try:
            got[label] = ("ok", repr(fn(*a, **k)))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert (a, k) == (args, kwargs), f"{label} mutated its input"
    assert got["orig"] == got["new"], got  # repr equality also pins dict insertion order
    return eval(got["new"][1]) if got["new"][0] == "ok" else got["new"]


def cp(net, gross=None, mfe=0.5, mae=-0.2, status="observed"):
    return {"status": status, "live_net_return_pct": net, "gross_return_pct": net if gross is None else gross,
            "mfe_pct": mfe, "mae_pct": mae}


def row(day="2026-07-09", symbol="A", net=0.4, h="+30m", **extra):
    base = {"day": day, "symbol": symbol, "checkpoints": {h: cp(net)}}
    base.update(extra)
    return base


# ---------------- A25-3 summarize_rows ----------------
@pytest.mark.parametrize("rows", [
    [],
    [{"day": "d", "checkpoints": {"+30m": cp(1.0, status="pending")}}],
    [row(net=0.0)],
    [row(net=0.5, day="2026-07-09", symbol="A"), row(net=-0.2, day="2026-07-09", symbol="B"),
     row(net=1.2, day="2026-07-13", symbol="A"), row(net=0.3333333, day="2026-07-13", symbol="C"), {"day": "x"}],
])
def test_summarize_rows(orig_nodes, monkeypatch, guards, rows):
    check(orig_nodes, monkeypatch, "summarize_rows", (rows, "+30m"))


def test_summarize_rows_facade_seams(orig_nodes, monkeypatch, guards):
    calls = []

    def fake_metrics(values):
        calls.append(list(values))
        return {"fake": True}

    out = check(orig_nodes, monkeypatch, "summarize_rows", ([row(net=1.0)], "+30m"),
                overrides={"performance_metrics": fake_metrics, "_observed_return": lambda r, h: 7.0})
    assert out["metrics"] == {"fake": True} and calls[-2] == [7.0] and calls[-1] == [1.0]


# ---------------- A25-6 grouped_horizon_summary / A25-7 split_summary ----------------
@pytest.mark.parametrize("episodes", [
    [],
    [row(lane="x"), row(lane=["x", "y", "x"]), row(lane=None), row(lane=""), row()],
])
def test_grouped_horizon_summary(orig_nodes, monkeypatch, guards, episodes):
    out = check(orig_nodes, monkeypatch, "grouped_horizon_summary", (episodes,), {"field": "lane"})
    assert list(out) == sorted(out)


def test_grouped_horizon_summary_fake_summarizer(orig_nodes, monkeypatch, guards):
    seen = []
    out = check(orig_nodes, monkeypatch, "grouped_horizon_summary", ([row(lane="a")],), {"field": "lane"},
                overrides={"summarize_rows": lambda rows, horizon: seen.append(horizon) or {"h": horizon}})
    assert list(out["a"]) == list(H) and seen[-len(H):] == list(H)


@pytest.mark.parametrize("days", [
    [],
    ["2026-07-09", "2026-07-10", "2026-07-11", "2026-07-13", "2026-07-14"],
    ["", "2026-07-12"],
])
def test_split_summary(orig_nodes, monkeypatch, guards, days):
    eps = [row(day=d, lane="a") for d in days] + [{"lane": "z"}]
    for cal, retro in (("2026-07-10", "2026-07-13"), ("2026-07-13", "2026-07-10")):  # also overlapping
        check(orig_nodes, monkeypatch, "split_summary", (eps,),
              {"field": "lane", "calibration_end": cal, "retrospective_start": retro})


def test_split_summary_use_time_patch(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "split_summary", ([row(day="2026-07-09")],),
                {"field": "lane", "calibration_end": "2026-07-10", "retrospective_start": "2026-07-13"},
                overrides={"grouped_horizon_summary": lambda eps, *, field: {"n": len(eps), "f": field}})
    assert out == {"calibration": {"n": 1, "f": "lane"}, "retrospective": {"n": 0, "f": "lane"}}


# ---------------- A25-4 discovery_cohorts ----------------
def test_discovery_cohorts(orig_nodes, monkeypatch, guards):
    eps = [row(day=d, time_bucket="open_0_20m", rank_bucket=r, net=n)
           for d, r, n in (("2026-07-09", "rank1", 0.3), ("2026-07-10", "rank2_3", -0.1),
                           ("2026-07-11", "rank1", 0.2), ("2026-07-13", "rank1", 0.9),
                           ("2026-07-14", "rank2_3", 0.0))]
    eps.append(row(time_bucket="later", rank_bucket="rank1"))
    out = check(orig_nodes, monkeypatch, "discovery_cohorts", (eps,))
    assert list(out) == ["opening_all", "opening_rank1", "opening_rank2_3"]
    assert list(out["opening_all"]) == ["overall", "calibration", "retrospective"]
    assert check(orig_nodes, monkeypatch, "discovery_cohorts", ([],))["opening_all"]["overall"]["+5m"]["population_count"] == 0


# ---------------- A25-5 score_component_diagnostics ----------------
def _score_eps(values, key="alpha"):
    return [row(net=0.1 * i, score_breakdown={key: v}) for i, v in enumerate(values)]


@pytest.mark.parametrize("values,included", [
    (list(range(29)), False),
    (list(range(30)), True),
    ([0] * 14 + [1] * 16, False),  # 14/16 split
    ([0] * 15 + [1] * 15, False),  # only 2 distinct values
    ([0] * 10 + [1] * 5 + [2] * 15, True),
])
def test_score_component_diagnostics(orig_nodes, monkeypatch, guards, values, included):
    out = check(orig_nodes, monkeypatch, "score_component_diagnostics", (_score_eps(values),))
    assert ("alpha" in out) is included


def test_score_component_malformed_and_unobserved(orig_nodes, monkeypatch, guards):
    eps = _score_eps(list(range(30))) + [row(net=1.0, score_breakdown={"alpha": "bad", "beta": 1})]
    eps.append({"checkpoints": {"+30m": cp(1.0, status="pending")}, "score_breakdown": {"alpha": 5}})
    out = check(orig_nodes, monkeypatch, "score_component_diagnostics", (eps,))
    assert list(out) == ["alpha"]


def test_score_component_use_time_median(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "score_component_diagnostics", (_score_eps(list(range(30))),),
                overrides={"median": lambda vs: 20.0})
    assert out.get("alpha", {}).get("median") in (None, 20.0)


# ---------------- A25-1 blocked_opportunity_analysis ----------------
def _sample(**kw):
    s = {"symbol": "A", "q16_day": "2026-07-09", "opportunity_disposition": "blocked", "reason": "r1",
         "primary_failure_axis": "ax", "entry_lane": "strict", "entry_quant_cost_floor_state": "ok"}
    s.update(kw)
    return s


def test_blocked_empty_and_malformed_shadow(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "blocked_opportunity_analysis", ([],))
    assert out["sample_count"] == 0 and out["by_disposition"] == {}
    samples = [_sample(shadow_forward_outcome="bad"), _sample(shadow_forward_outcome={"checkpoints": 3}),
               _sample(checkpoints="bad")]
    check(orig_nodes, monkeypatch, "blocked_opportunity_analysis", (samples,))


def test_blocked_direct_vs_shadow_precedence_and_groups(orig_nodes, monkeypatch, guards):
    obs = lambda g: {"status": "observed", "gross_return_pct": g, "mfe_pct": 1.0, "mae_pct": -0.5}  # noqa: E731
    samples = [
        _sample(checkpoints={"+5m": obs(1.0)}, shadow_forward_outcome={"checkpoints": {"+5m": obs(9.0)}}),
        _sample(shadow_forward_outcome={"checkpoints": {"+5m": obs(-1.0), "+15m": {"status": "pending"}}},
                reason="r2", opportunity_disposition="allowed", entry_lane=None),
        _sample(checkpoints={"+5m": {"status": "observed", "return_pct": 0.5}}, symbol="B",
                q16_day="2026-07-10", primary_failure_axis=None),
    ]
    out = check(orig_nodes, monkeypatch, "blocked_opportunity_analysis", (samples,))
    assert list(out) == ["sample_count", "by_disposition", "by_reason", "by_primary_failure_axis",
                         "by_entry_lane", "by_cost_floor_state"]
    assert "missing" in out["by_entry_lane"] and "missing" in out["by_primary_failure_axis"]
    assert list(out["by_reason"]["r1"]) == list(H[:-1])
    assert out["by_reason"]["r1"]["+5m"]["observed_count"] == 2


def test_blocked_use_time_constants(orig_nodes, monkeypatch, guards):
    obs = {"status": "observed", "gross_return_pct": 1.0}
    out = check(orig_nodes, monkeypatch, "blocked_opportunity_analysis", ([_sample(checkpoints={"+5m": obs})],),
                overrides={"LIVE_COST_PCT": 0.5, "performance_metrics": lambda v: {"v": list(v)}})
    assert out["by_reason"]["r1"]["+5m"]["net_metrics"] == {"v": [0.5]}


# ---------------- A25-2 actual_trade_analysis ----------------
def _trade(net, hold, rank=1, eligible=True, early=False, violation=False, horizon="intraday"):
    return {"realized_outcome": {"net_return_pct": net, "holding_seconds": hold},
            "integrity": {"promotion_metric_eligible": eligible},
            "horizon_alignment": {"exited_before_min_hold": early, "horizon_violation_candidate": violation,
                                  "strategy_horizon": horizon},
            "selection_context": {"selected_rank": rank}}


def test_actual_trade_empty_and_skips(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "actual_trade_analysis", ([],))
    assert out["trade_count"] == 0 and out["average_holding_seconds"] is None
    check(orig_nodes, monkeypatch, "actual_trade_analysis", ([{"realized_outcome": {"net_return_pct": None}}, {}],))


def test_actual_trade_thresholds_ranks_and_flags(orig_nodes, monkeypatch, guards):
    holds = [59, 60, 299, 300, 1799, 1800, None]
    rows = [_trade(0.1 * i - 0.2, h, rank=(i % 3), eligible=bool(i % 2), early=(i % 4 == 0),
                   violation=(i % 5 == 0), horizon=("swing" if i % 2 else "intraday"))
            for i, h in enumerate(holds)]
    rows.append({"realized_outcome": {"net_return_pct": 0.3}, "horizon_alignment": "bad", "integrity": 5})
    out = check(orig_nodes, monkeypatch, "actual_trade_analysis", (rows,))
    assert list(out["by_hold_bucket"]) == sorted(out["by_hold_bucket"])
    assert set(out["by_hold_bucket"]) == {"under_60s", "60_300s", "300_1800s", "1800s_plus"}
    assert list(out["by_selected_rank"]) == sorted(out["by_selected_rank"])
    assert out["trade_count"] == 8


# ---------------- A25-8 simulate_path_policies ----------------
POL = [{"policy_id": "p", "target_pct": 1.0, "stop_pct": 0.5, "max_minutes": 30}]


def _ep(**kw):
    e = {"symbol": "A", "day": "2026-07-09", "baseline_epoch": 1000, "baseline_price": 100.0}
    e.update(kw)
    return e


def _bar(ts, low, high, close=100.0, raw_ts=""):
    return {"ts": ts, "low": low, "high": high, "close": close, "raw_ts": raw_ts}


@pytest.mark.parametrize("episodes,rows", [
    ([], {}),
    ([_ep(baseline_price=0.0)], {"A": [_bar(1000, 99, 101)]}),
    ([_ep()], {"A": []}),
    ([_ep()], {"A": [_bar(999, 50, 150), _bar(1000 + 1801, 50, 150)]}),  # both outside the 30m window
    ([_ep()], {"A": [_bar(1000 + 1800, 99.9, 100.1, 100.4)]}),  # window edge included, time exit
    ([_ep()], {"A": [_bar(1000, 99.0, 102.0)]}),  # same bar: stop before target
    ([_ep()], {"A": [_bar(1000, 99.8, 102.0)]}),  # target
    ([_ep(), _ep(day="2026-07-10")], {"A": [_bar(1000, 99.9, 100.2, raw_ts="20260709093000")]}),  # date filter
])
def test_simulate_path_policies(orig_nodes, monkeypatch, guards, episodes, rows):
    out = check(orig_nodes, monkeypatch, "simulate_path_policies", (episodes,), {"minute_rows_by_symbol": rows})
    for payload in out.values():
        assert payload["conservative_same_bar_rule"] == "stop_before_target"


def test_simulate_path_policies_fake_policy_and_priority(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "simulate_path_policies", ([_ep()],),
                {"minute_rows_by_symbol": {"A": [_bar(1000, 99.0, 102.0)]}},
                overrides={"PATH_POLICIES": POL, "LIVE_COST_PCT": 0.0,
                           "performance_metrics": lambda v: {"v": [round(x, 6) for x in v]}})
    assert list(out) == ["p"] and out["p"]["exit_reasons"] == {"stop": 1} and out["p"]["metrics"] == {"v": [-0.5]}


# ---------------- structure ----------------
@pytest.mark.parametrize("name", NAMES)
def test_wrapper_thin_and_owner_holds_body(name):
    wrapper = ast.parse(inspect.getsource(getattr(analysis, name))).body[0]
    assert len(wrapper.body) == 1 and isinstance(wrapper.body[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.DictComp))]
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(list(ast.walk(node))) > 25
    assert owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name])
    assert "from .analysis " not in src and "import analysis" not in src.replace("analysis_", "")
