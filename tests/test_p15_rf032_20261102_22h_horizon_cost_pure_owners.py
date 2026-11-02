"""RF-032 A46-1..8: eight ``horizon_compliance_report`` / ``cost_basis_comparison`` bodies, original vs thin wrappers + Owners.

Original = A preimage b16ef691 (SOURCE blobs e4d6325a / 69d0ec29 == canonical 5765ba80). Each original function is compiled from
``git show`` into a copy of the live module namespace and compared with the final wrapper + Owner (output repr,
exception type/message, input immutability). Fake objects only: attach/dedupe/performance helpers are faked, no real
file reads/writes, sockets, subprocess or UEF/validation-id writer.
"""
from __future__ import annotations

import ast
import builtins
import copy
import hashlib
import importlib
import inspect
import socket
import subprocess
from pathlib import Path

import pytest

A_PRE = "b16ef691b7e9721789b101003fea6d98f75a45dc"
CANON = "5765ba80521819a468aaca540bb2132e7228bdbd"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_mapping": ("horizon_compliance_report", "e4d6325a8f7def0ad682188000a84b89be00c6e1", "horizon_compliance_report_mapping"),
    "_num": ("horizon_compliance_report", "e4d6325a8f7def0ad682188000a84b89be00c6e1", "horizon_compliance_report_num"),
    "_bucket_key": ("horizon_compliance_report", "e4d6325a8f7def0ad682188000a84b89be00c6e1", "horizon_compliance_report_bucket_key"),
    "build_horizon_compliance_report": ("horizon_compliance_report", "e4d6325a8f7def0ad682188000a84b89be00c6e1", "horizon_compliance_report_build_horizon_compliance_report"),
    "render_horizon_compliance_report": ("horizon_compliance_report", "e4d6325a8f7def0ad682188000a84b89be00c6e1", "horizon_compliance_report_render_horizon_compliance_report"),
    "_pct": ("cost_basis_comparison", "69d0ec298f9f0afcfb7db39f7e86723f1e9918c0", "cost_basis_comparison_pct"),
    "build_evaluation_cost_bases": ("cost_basis_comparison", "69d0ec298f9f0afcfb7db39f7e86723f1e9918c0", "cost_basis_comparison_build_evaluation_cost_bases"),
    "render_cost_basis_comparison": ("cost_basis_comparison", "69d0ec298f9f0afcfb7db39f7e86723f1e9918c0", "cost_basis_comparison_render_cost_basis_comparison"),
}
MODS = {s: importlib.import_module(f"libs.reporting.evaluation.{s}") for s in {v[0] for v in SPEC.values()}}
OWNERS = {n: importlib.import_module(f"libs.reporting.evaluation.{v[2]}") for n, v in SPEC.items()}
NAN = float("nan")


def _sha(raw: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + bytes([0]) + raw).hexdigest()


@pytest.fixture(scope="module")
def orig_nodes():
    out = {}
    for stem, blob in {(v[0], v[1]) for v in SPEC.values()}:
        raws = {}
        for label, rev in (("A", A_PRE), ("canonical", CANON)):
            try:
                raws[label] = subprocess.run(["git", "show", f"{rev}:{EV}{stem}.py"], check=True, capture_output=True).stdout
            except subprocess.CalledProcessError as exc:
                pytest.fail(f"BLOCKED_PIN {stem} {label}: {exc.stderr!r}")
            assert _sha(raws[label]) == blob, f"BLOCKED_PIN {stem} {label} blob"
        tree = ast.parse(raws["A"].decode("utf-8"))
        for n, v in SPEC.items():
            if v[0] == stem:
                out[n] = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == n][-1]
    assert sorted(out) == sorted(SPEC)
    return out


@pytest.fixture
def guards(monkeypatch):
    def boom(*a, **k):
        raise AssertionError("real filesystem/effect attempted")
    monkeypatch.setattr(subprocess, "run", boom)
    monkeypatch.setattr(subprocess, "Popen", boom)
    monkeypatch.setattr(socket.socket, "connect", boom)
    for attr in ("read_text", "read_bytes", "write_text", "write_bytes", "mkdir", "touch", "unlink", "rename", "replace",
                 "exists", "is_dir", "is_file", "rglob", "glob", "iterdir"):
        monkeypatch.setattr(Path, attr, boom)
    real_open = builtins.open

    def guarded_open(file, mode="r", *a, **k):
        if any(c in str(mode) for c in "wax+") or str(file).replace("\\", "/").startswith(("/rep", "/fake")):
            raise AssertionError("open attempted")
        return real_open(file, mode, *a, **k)
    monkeypatch.setattr(builtins, "open", guarded_open)


def check(orig_nodes, monkeypatch, name, *args, overrides=None, **kwargs):
    mod = MODS[SPEC[name][0]]
    ns = dict(vars(mod))
    tree = ast.Module(body=[copy.deepcopy(orig_nodes[name])], type_ignores=[])
    exec(compile(ast.fix_missing_locations(tree), f"<{A_PRE[:8]}:{name}>", "exec"), ns)
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(mod, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[name]), ("new", getattr(mod, name))):
        a, k = copy.deepcopy((args, kwargs))
        try:
            values[label] = fn(*a, **k)
            got[label] = ("ok", repr(values[label]))
        except Exception as exc:
            got[label] = ("err", type(exc).__name__, str(exc))
        assert repr((a, k)) == repr((args, kwargs)), f"{label} mutated input"
    assert got["orig"] == got["new"], got
    return values["new"] if got["new"][0] == "ok" else got["new"]


import collections

HC = MODS["horizon_compliance_report"]
CB = MODS["cost_basis_comparison"]


class _Str:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"_Str({self.text!r})"

    def __str__(self):
        return self.text


class _Num:
    def __repr__(self):
        return "_Num()"

    def __float__(self):
        return 2.5

    def __bool__(self):
        return True


class _FloatErr:
    def __init__(self, exc):
        self.exc = exc

    def __repr__(self):
        return f"_FloatErr({self.exc.__name__})"

    def __float__(self):
        raise self.exc("custom float failure")


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


# ---- A46-1 horizon _mapping ----
@pytest.mark.parametrize("value", [None, {}, {"a": 1}, _MapSub(a=1), [], [("a", 1)], "s", 5, {"n": {"deep": [1]}}])
def test_hc_mapping(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_mapping", value)


def test_hc_mapping_identity_and_seam(orig_nodes, monkeypatch, guards):
    src = {"a": 1}
    assert HC._mapping(src) is src and HC._mapping(None) == {} and HC._mapping(None) is not HC._mapping(None)
    sub = _MapSub(a=1)
    assert HC._mapping(sub) is sub

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_mapping", {"a": 1}, overrides={"Mapping": NeverMapping}) == {}


# ---- A46-2 horizon _num ----
@pytest.mark.parametrize("value", [None, "", 0, 0.0, "0", " 1.5 ", "abc", "1e3", "nan", "inf", NAN, True, [], {}, b"2", _Num(), _FloatErr(TypeError), _FloatErr(ValueError), (), "-0"])
def test_hc_num(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_num", value)


def test_hc_num_exact_and_not_broadened(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_num", None) is None and check(orig_nodes, monkeypatch, "_num", "") is None and check(orig_nodes, monkeypatch, "_num", 0) == 0.0
    assert check(orig_nodes, monkeypatch, "_num", _FloatErr(TypeError)) is None and check(orig_nodes, monkeypatch, "_num", _FloatErr(ValueError)) is None
    assert check(orig_nodes, monkeypatch, "_num", _FloatErr(RuntimeError)) == ("err", "RuntimeError", "custom float failure")  # only TypeError/ValueError caught
    out = check(orig_nodes, monkeypatch, "_num", "nan")
    assert out != out


# ---- A46-3 _bucket_key ----
BK = [{}, {"horizon_alignment": {"strategy_horizon": "swing"}, "exit_quality": {"reason": "stop"}}, {"horizon_alignment": {"strategy_horizon": ""}, "exit_quality": {"reason": ""}, "exit_reason": "fallback"},
      {"exit_reason": "only_top"}, {"horizon_alignment": None, "exit_quality": None}, {"horizon_alignment": "bad", "exit_quality": "bad", "exit_reason": 0},
      {"horizon_alignment": {"strategy_horizon": 5}, "exit_quality": {"reason": _Str("한글")}}, {"horizon_alignment": {"strategy_horizon": None}, "exit_quality": {"reason": None}, "exit_reason": None}]


@pytest.mark.parametrize("evaluation", BK)
def test_bucket_key(orig_nodes, monkeypatch, guards, evaluation):
    check(orig_nodes, monkeypatch, "_bucket_key", evaluation)


def test_bucket_key_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_bucket_key", BK[1]) == ("swing", "stop") and check(orig_nodes, monkeypatch, "_bucket_key", {}) == ("unknown", "unknown")
    assert check(orig_nodes, monkeypatch, "_bucket_key", BK[2]) == ("unknown", "fallback")  # quality reason blank -> top-level exit_reason
    assert check(orig_nodes, monkeypatch, "_bucket_key", None)[0] == "err"
    seen = []
    out = check(orig_nodes, monkeypatch, "_bucket_key", {"x": 1}, overrides={"_mapping": lambda v: seen.append(v) or {"strategy_horizon": "H", "reason": "R"}})
    assert out == ("H", "R") and len(seen) == 4  # two _mapping calls per side, horizon first


# ---- A46-4 build_horizon_compliance_report ----
def _ev(tid="T1", horizon="intraday", reason="stop", ret=1.0, hold=100, **hz):
    h = {"strategy_horizon": horizon, "actual_hold_sec": hold, "bucket": "b1"}
    h.update(hz)
    return {"trade_id": tid, "symbol": "S" + tid, "horizon_alignment": h, "exit_quality": {"reason": reason}, "realized_outcome": {"net_return_pct": ret, "holding_seconds": 77}, "integrity": {}}


EVS = [_ev("1"), _ev("2", ret=-2.0, exited_before_min_hold=True), _ev("3", horizon="swing", reason="take", ret=0.5, hold=None, exited_before_target_hold=True, target_hold_would_improve_exit=True),
       _ev("4", ret=None, hold="bad", exited_beyond_max_hold=True, horizon_violation_candidate=True), _ev("5", valid_early_exit=True), _ev("6", early_exit_allowed_match=["m1"]),
       {**_ev("7"), "integrity": {"promotion_metric_eligible": False}}, {**_ev("8"), "integrity": {"exit_metric_eligible": False}},
       {**_ev("9"), "integrity": {"promotion_metric_eligible": False, "exit_metric_eligible": False}}, {"trade_id": "10"}, _ev("11", hold=0, ret=0.0), {**_ev("12", hold=None), "realized_outcome": {"holding_seconds": 55}}]


@pytest.mark.parametrize("evs", [[], EVS, EVS[:1], EVS[1:3], EVS[6:9], EVS[9:], [EVS[0]] * 3])
def test_build_horizon_compliance_report(orig_nodes, monkeypatch, guards, evs):
    check(orig_nodes, monkeypatch, "build_horizon_compliance_report", evs)


def test_build_horizon_compliance_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "build_horizon_compliance_report", EVS)
    assert list(out) == ["schema_version", "behavior_effect", "trade_count", "excluded_trade_count", "exit_incident_excluded_trade_count", "horizon_counts", "group_rows", "rows", "policy_warning"]
    assert out["excluded_trade_count"] == 2 and out["exit_incident_excluded_trade_count"] == 1 and out["trade_count"] == len(out["rows"]) == 9
    keys = [(g["strategy_horizon"], g["exit_reason"]) for g in out["group_rows"]]
    assert keys == sorted(keys) and out["horizon_counts"]["swing"] == 1
    assert out["rows"][2]["actual_hold_sec"] == 77.0 and out["rows"][-1]["actual_hold_sec"] == 55.0  # blank actual_hold_sec falls back to realized holding_seconds
    assert out["policy_warning"].startswith("Do not convert this into delayed exits directly.")
    assert check(orig_nodes, monkeypatch, "build_horizon_compliance_report", None)[0] == "err" and check(orig_nodes, monkeypatch, "build_horizon_compliance_report", [None])[0] == "err"
    src = [copy.deepcopy(EVS[0])]
    HC.build_horizon_compliance_report(src)
    assert src == [EVS[0]]
    out = check(orig_nodes, monkeypatch, "build_horizon_compliance_report", EVS[:3],
                overrides={"performance_metrics": lambda vals: {"n": len(vals)}, "_bucket_key": lambda e: ("K", e["trade_id"]), "_num": lambda v: 7.0 if v else None})
    assert [g["strategy_horizon"] for g in out["group_rows"]] == ["K", "K", "K"] and out["group_rows"][0]["performance"] == {"n": 1}
    made = []

    def spy_dd(factory):
        made.append(1)
        return collections.defaultdict(factory)

    class SpyCounter(collections.Counter):
        def __init__(self, *a, **k):
            made.append("c")
            super().__init__(*a, **k)
    check(orig_nodes, monkeypatch, "build_horizon_compliance_report", EVS[:1], overrides={"defaultdict": spy_dd, "Counter": SpyCounter})
    assert sorted(map(str, made)) == ["1", "1", "c", "c"]


# ---- A46-5 render_horizon_compliance_report ----
GROW = {"strategy_horizon": "intraday", "exit_reason": "stop", "count": 3, "average_hold_sec": 12.5, "exit_before_min_hold_count": 1, "exit_before_target_hold_count": 0,
        "target_hold_would_improve_exit_count": 2, "performance": {"average_return_pct": 0.123456}}
HP = {"behavior_effect": "observation_only", "trade_count": 3, "policy_warning": "warn 한글", "horizon_counts": {"swing": 1, "intraday": 2}, "group_rows": [GROW, "bad", {"performance": None}, {"performance": {"average_return_pct": None}}]}
HPS = [{}, HP, {**HP, "horizon_counts": {}}, {**HP, "horizon_counts": None, "group_rows": None}, {**HP, "group_rows": [GROW] * 2}, {"horizon_counts": "bad"}, {**HP, "group_rows": [{"performance": {"average_return_pct": "x"}}]}]


@pytest.mark.parametrize("payload", HPS)
def test_render_horizon_compliance_report(orig_nodes, monkeypatch, guards, payload):
    check(orig_nodes, monkeypatch, "render_horizon_compliance_report", payload)


def test_render_horizon_compliance_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_horizon_compliance_report", HP)
    assert out.startswith("# Horizon Compliance Report\n\n- Behavior effect: `observation_only`\n- Trades: 3\n- Policy warning: warn 한글\n\n## Horizon Counts\n\n- `intraday`: 2\n- `swing`: 1\n")  # sorted keys
    assert "| intraday | stop | 3 | 12.5 | 1 | 0 | 2 | 0.1235% |\n" in out and out.endswith("-  |\n") is False and out.endswith("\n") and not out.endswith("\n\n")
    assert "| None | None | None | None | None | None | None | - |\n" in out
    assert "- No observed horizons.\n" in check(orig_nodes, monkeypatch, "render_horizon_compliance_report", {})
    assert check(orig_nodes, monkeypatch, "render_horizon_compliance_report", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "render_horizon_compliance_report", {"group_rows": [{"performance": {"average_return_pct": "x"}}]})[0:2] == ("err", "ValueError")
    out = check(orig_nodes, monkeypatch, "render_horizon_compliance_report", HP, overrides={"_mapping": lambda v: {"swing": 9} if v is HP["horizon_counts"] or (isinstance(v, dict) and "swing" in v) else {}})
    assert "- `swing`: 9\n" in out

    class NeverMapping:
        pass
    assert "| intraday" not in check(orig_nodes, monkeypatch, "render_horizon_compliance_report", HP, overrides={"Mapping": NeverMapping})


# ---- A46-6 _pct ----
@pytest.mark.parametrize("value", [0, 0.0, 1, 0.009, 0.00015, 0.002, -0.5, 1e-9, 123456.789, "0.5", NAN, float("inf"), True, _Num(), None, "x", [], _FloatErr(TypeError)])
def test_pct(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_pct", value)


def test_pct_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_pct", 0.009) == 0.9 and check(orig_nodes, monkeypatch, "_pct", 0.00015) == 0.015 and check(orig_nodes, monkeypatch, "_pct", 1e-6) == 0.0001 and check(orig_nodes, monkeypatch, "_pct", 1e-9) == 0.0
    out = check(orig_nodes, monkeypatch, "_pct", NAN)
    assert out != out
    assert check(orig_nodes, monkeypatch, "_pct", None)[0:2] == ("err", "TypeError") and check(orig_nodes, monkeypatch, "_pct", "x")[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, "_pct", float("inf")) == float("inf")


# ---- A46-7 build_evaluation_cost_bases ----
PROFILES = [None, {}, {"source": "fake", "sample_count": 7, "ema_round_trip_cost_pct": 0.004, "conservative_round_trip_cost_pct": 0.006}, {"ema_round_trip_cost_pct": 0.002},
            {"conservative_round_trip_cost_pct": 0, "ema_round_trip_cost_pct": 0.01, "sample_count": "3"}, {"sample_count": "bad"}, {"conservative_round_trip_cost_pct": "x"}, {"source": ""}]


@pytest.mark.parametrize("profile", PROFILES)
def test_build_cost_bases_profiles(orig_nodes, monkeypatch, guards, profile):
    check(orig_nodes, monkeypatch, "build_evaluation_cost_bases", profile)


@pytest.mark.parametrize("slippage", [0.0, 0.05, 0.123456789, -0.1, 1, "0.2", None, "x"])
def test_build_cost_bases_slippage(orig_nodes, monkeypatch, guards, slippage):
    check(orig_nodes, monkeypatch, "build_evaluation_cost_bases", {"source": "s"}, slippage_pct=slippage)


def test_build_cost_bases_default_exact_and_seams(orig_nodes, monkeypatch, guards):
    sig = inspect.signature(CB.build_evaluation_cost_bases)
    assert sig.parameters["slippage_pct"].default == CB.DEFAULT_EVALUATION_SLIPPAGE_PCT == 0.05 and sig.parameters["slippage_pct"].kind.name == "KEYWORD_ONLY"
    out = check(orig_nodes, monkeypatch, "build_evaluation_cost_bases", None)
    assert list(out) == ["schema_version", "primary_interpretation", "slippage_pct", "mock_observed", "live_deployment_equity"] and out["slippage_pct"] == 0.05
    assert out["mock_observed"]["round_trip_cost_pct"] == 0.9 and out["mock_observed"]["source"] == "fallback" and out["live_deployment_equity"]["round_trip_cost_pct"] == 0.23
    assert out["live_deployment_equity"]["total_drag_with_slippage_pct"] == 0.28
    out = check(orig_nodes, monkeypatch, "build_evaluation_cost_bases", {"conservative_round_trip_cost_pct": 0.006}, slippage_pct=0.1)
    assert out["mock_observed"]["round_trip_cost_pct"] == 0.6 and out["mock_observed"]["total_drag_with_slippage_pct"] == 0.7
    out = check(orig_nodes, monkeypatch, "build_evaluation_cost_bases", {}, overrides={"LIVE_BUY_FEE_RATE": 0.01, "LIVE_SELL_FEE_RATE": 0.02, "LIVE_EQUITY_SELL_TAX_RATE_2026": 0.03, "_pct": lambda v: round(v * 1000, 3)})
    assert out["live_deployment_equity"]["buy_fee_pct"] == 10.0 and out["live_deployment_equity"]["round_trip_cost_pct"] == 60.0


def test_build_cost_bases_default_bound_at_definition_time(monkeypatch, guards):
    # the default stays bound by the SOURCE signature (definition time), exactly as before: patching the constant later does not change it
    monkeypatch.setattr(CB, "DEFAULT_EVALUATION_SLIPPAGE_PCT", 9.0)
    assert CB.build_evaluation_cost_bases(None)["slippage_pct"] == 0.05


# ---- A46-8 render_cost_basis_comparison ----
CP = {"range": {"start": "2026-04-10", "end": "2026-04-14"}, "forward_data_source": "src", "cohort_scope": "scope 한글",
      "cost_bases": {"slippage_pct": 0.05, "mock_observed": {"round_trip_cost_pct": 0.9, "total_drag_with_slippage_pct": 0.95}, "live_deployment_equity": {"round_trip_cost_pct": 0.23, "total_drag_with_slippage_pct": 0.28}},
      "rows": [{"top_k": 3, "horizon": "+30m", "window_count": 5, "observed_day_count": 3, "gross": {"expectancy_pct": 1.23456}, "mock_net": {"expectancy_pct": 0.3}, "live_net": {"expectancy_pct": 1.0},
                "expectancy_delta_live_minus_mock_pct": 0.7}, {}, {"gross": None}]}
CPS = [{}, {"range": None, "cost_bases": None, "rows": None}, CP, {**CP, "forward_data_source": "", "cohort_scope": None}, {**CP, "rows": []}, {**CP, "cost_bases": {"mock_observed": None, "live_deployment_equity": None}}]


@pytest.mark.parametrize("payload", CPS)
def test_render_cost_basis_comparison(orig_nodes, monkeypatch, guards, payload):
    check(orig_nodes, monkeypatch, "render_cost_basis_comparison", payload)


def test_render_cost_basis_exact_and_errors(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_cost_basis_comparison", CP)
    assert out.startswith("# Cost Basis Comparison (2026-04-10 ~ 2026-04-14)\n\nEvaluation-only. Runtime entry, exit, and broker accounting are unchanged.\nForward data source: `src`.\nCohort scope: `scope 한글`.\n")
    assert "| Mock observed | 0.9000% | 0.0500% | 0.9500% | Mock PnL/cash truth |\n" in out and "| 3 | +30m | 5/3 | 1.2346% | 0.3000% | 1.0000% | +0.7000% |\n" in out
    assert "| None | None | None/None | 0.0000% | 0.0000% | 0.0000% | +0.0000% |\n" in out and out.endswith("- This report does not authorize a trading-policy change.\n")
    empty = check(orig_nodes, monkeypatch, "render_cost_basis_comparison", {})
    assert "(None ~ None)" in empty and "Forward data source: `unknown`." in empty and "Cohort scope: `unknown`." in empty
    assert check(orig_nodes, monkeypatch, "render_cost_basis_comparison", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "render_cost_basis_comparison", {"cost_bases": {"slippage_pct": "x"}})[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, "render_cost_basis_comparison", {"rows": ["bad"]})[0] == "err"


# ---- structure ----
@pytest.mark.parametrize("name", list(SPEC))
def test_wrapper_thin_and_owner_holds_body(name):
    mod = MODS[SPEC[name][0]]
    wrapper = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], name)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name])
    stem = SPEC[name][0]
    assert f"import {stem}" not in src and f"{stem} import" not in src.replace("from . import", "") and f"from .{stem} " not in src
