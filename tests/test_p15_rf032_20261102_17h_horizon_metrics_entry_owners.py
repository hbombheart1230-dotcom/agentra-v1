"""RF-032 A41-1..8: eight horizon_alignment / attribution_score_v0 / metrics / entry_timing_attribution bodies.

Original = A preimage 8c26d830 (== canonical 37216b33 for these four SOURCE blobs); each original function is compiled
from ``git show`` into a copy of the live module namespace and compared with the final wrapper + Owner. Dependency
overrides apply to both sides. Fake objects only: no real file reads/writes, sockets, subprocess or UEF/validation-id
writer. ``load_minute_rows_from_state``, ``_daily_windows_by_id`` and the loaders are replaced by fakes.
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

A_PRE = "8c26d830cc774e80fe4a46a945286b00d20bd9c7"
CANON = "37216b3378c9a3992d2f26f4c88daace84f441d2"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_text": ("horizon_alignment", "c02845b19570057a3292e2a1d959bff67cabcd19", "horizon_alignment_text"),
    "_lane_observation": ("horizon_alignment", "c02845b19570057a3292e2a1d959bff67cabcd19", "horizon_alignment_lane_observation"),
    "_combo_rows": ("horizon_alignment", "c02845b19570057a3292e2a1d959bff67cabcd19", "horizon_alignment_combo_rows"),
    "build_horizon_alignment_review": ("horizon_alignment", "c02845b19570057a3292e2a1d959bff67cabcd19", "horizon_alignment_build_horizon_alignment_review"),
    "render_horizon_alignment_review": ("horizon_alignment", "c02845b19570057a3292e2a1d959bff67cabcd19", "horizon_alignment_render_horizon_alignment_review"),
    "_mapping": ("attribution_score_v0", "2dfe8ca9bd3daef3c2f1e233d951a1b85a5ca415", "attribution_score_v0_mapping"),
    "performance_metrics": ("metrics", "6427c295f42a72b62b5083430edc862679dbc32c", "metrics_performance_metrics"),
    "build_entry_timing_attribution_report": ("entry_timing_attribution", "203e0edd5baea6ad174536670c5fd553271a7db5", "entry_timing_attribution_build_entry_timing_attribution_report"),
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


class _Str:
    def __init__(self, text, truthy=True):
        self.text, self.truthy = text, truthy

    def __repr__(self):
        return f"_Str({self.text!r},{self.truthy})"

    def __str__(self):
        return self.text

    def __bool__(self):
        return self.truthy


class _BadStr:
    def __repr__(self):
        return "_BadStr()"

    def __str__(self):
        raise RuntimeError("str failure")


class _BadBool:
    def __repr__(self):
        return "_BadBool()"

    def __bool__(self):
        raise RuntimeError("bool failure")


# ---- A41-1 _text ----
@pytest.mark.parametrize("value", [None, 0, 0.0, False, "", "  ", "\t\n", " a ", "한글", " 한글 ", "x ", 5, 1.5, [], [1], {}, _Str(" custom "), _Str("  ")])
@pytest.mark.parametrize("fallback", ["unknown", "", "FB"])
def test_text_values(orig_nodes, monkeypatch, guards, value, fallback):
    check(orig_nodes, monkeypatch, "_text", value, fallback)
    check(orig_nodes, monkeypatch, "_text", value)


def test_text_exact_and_errors(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_text", None) == "unknown"
    assert check(orig_nodes, monkeypatch, "_text", 0, "z") == "z"  # falsy -> fallback
    assert check(orig_nodes, monkeypatch, "_text", "  한글 ") == "한글"
    assert check(orig_nodes, monkeypatch, "_text", _Str(" cu ")) == "cu"
    assert check(orig_nodes, monkeypatch, "_text", "  ", "") == ""
    assert check(orig_nodes, monkeypatch, "_text", _BadStr()) == ("err", "RuntimeError", "str failure")
    assert check(orig_nodes, monkeypatch, "_text", _BadBool()) == ("err", "RuntimeError", "bool failure")
    assert inspect.signature(MODS["horizon_alignment"]._text).parameters["fallback"].default == "unknown"


# ---- A41-2 _lane_observation ----
@pytest.mark.parametrize("row", [{}, {"entry_lane_observation": None}, {"entry_lane_observation": {}}, {"entry_lane_observation": {"b": 1, "a": 2}},
                                 {"entry_lane_observation": [("a", 1)]}, {"entry_lane_observation": "s"}, {"entry_lane_observation": {"n": {"deep": [1]}}}, None, [], "row"])
def test_lane_observation(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_lane_observation", row)


def test_lane_observation_copy_order_and_seam(orig_nodes, monkeypatch, guards):
    mod = MODS["horizon_alignment"]
    src = {"z": 1, "a": {"x": 1}}
    out = mod._lane_observation({"entry_lane_observation": src})
    assert out == src and out is not src and list(out) == ["z", "a"] and out["a"] is src["a"]  # shallow copy, order kept
    assert mod._lane_observation({}) == {} and mod._lane_observation({}) is not mod._lane_observation({})

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_lane_observation", {"entry_lane_observation": {"a": 1}}, overrides={"Mapping": NeverMapping}) == {}


# ---- A41-3 _combo_rows ----
def _cand(day="2026-04-10", symbol="005930", tactic="t1", lane="L1", bucket="open", rail="up", rets=None):
    cps = {h: {"status": "observed", "return_pct": r} for h, r in (rets or {}).items()}
    return {"generated_at": f"{day}T00:00:00+00:00", "symbol": symbol, "quant_tactic_id": tactic, "shadow_role": "primary",
            "entry_lane_observation": {"time_bucket": bucket, "primary_lane": lane, "market_regime_rail": rail},
            "shadow_forward_outcome": {"checkpoints": cps}}


def _big(avg=1.0, n=24):
    days = ["2026-04-10", "2026-04-11", "2026-04-12", "2026-04-13"]
    syms = ["A", "B", "C", "D", "E"]
    return [_cand(day=days[i % 4], symbol=syms[i % 5], rets={"+5m": avg + (i % 3) * 0.1, "+15m": avg - 0.5}) for i in range(n)]


DIMS = [("time_bucket", "tactic"), ("time_bucket", "primary_lane"), ("time_bucket", "tactic", "market_regime_rail"), ("tactic",), ()]


@pytest.mark.parametrize("dimensions", DIMS)
@pytest.mark.parametrize("cost", [0.0, 0.9, 5.0])
def test_combo_rows_real_helpers(orig_nodes, monkeypatch, guards, dimensions, cost):
    cands = _big() + [_cand(tactic="t2", lane="L2", rets={"+5m": -1.0, "+30m": 0.2}), _cand(tactic="t2", rets={}), _cand(symbol="", tactic="", rets={"+60m": 0.4})]
    check(orig_nodes, monkeypatch, "_combo_rows", cands, dimensions=dimensions, cost_pct=cost)


@pytest.mark.parametrize("cands", [[], [_cand(rets={})], [_cand(rets={"+5m": 1.0})], _big(0.2, 5), _big(-2.0), _big(0.35, 30)])
def test_combo_rows_shapes(orig_nodes, monkeypatch, guards, cands):
    check(orig_nodes, monkeypatch, "_combo_rows", cands, dimensions=("time_bucket", "tactic"), cost_pct=0.9)


def test_combo_rows_decisions_and_order(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_combo_rows", _big(2.0, 24) + [_cand(tactic="t9", rets={"+5m": 0.3})], dimensions=("tactic",), cost_pct=0.9)
    assert out[0]["cost_positive"] is True and out[0]["decision"] == "CONTROLLED_ADOPTION_CANDIDATE" and out[0]["dimensions"] == {"tactic": "t1"}
    assert [r["horizon"] for r in out][:2] == ["+5m", "+15m"] or out[0]["horizon"] in ("+5m", "+15m")
    assert out[-1]["decision"] == "INSUFFICIENT_EVIDENCE"
    out = check(orig_nodes, monkeypatch, "_combo_rows", _big(-3.0, 24), dimensions=("tactic",), cost_pct=0.9)
    assert {r["decision"] for r in out} == {"REJECT_COST_NEGATIVE"}
    # ties keep insertion order (stable sort): identical returns for two tactics
    ties = [_cand(tactic="a", rets={"+5m": 1.0}), _cand(tactic="b", rets={"+5m": 1.0})]
    out = check(orig_nodes, monkeypatch, "_combo_rows", ties, dimensions=("tactic",), cost_pct=0.0)
    assert [r["dimensions"]["tactic"] for r in out] == ["a", "b"]


def test_combo_rows_errors_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_combo_rows", None, dimensions=("tactic",), cost_pct=0.0)[0] == "err"
    assert check(orig_nodes, monkeypatch, "_combo_rows", [5], dimensions=("tactic",), cost_pct=0.0)[0] == "err"
    sig = inspect.signature(MODS["horizon_alignment"]._combo_rows)
    assert [p.kind.name for p in sig.parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY", "KEYWORD_ONLY"]


def test_combo_rows_helper_patches(orig_nodes, monkeypatch, guards):
    cands = [{"id": i, "d": f"d{i % 2}", "sym": "s", "r": float(i)} for i in range(6)]
    seen = []
    out = check(orig_nodes, monkeypatch, "_combo_rows", cands, dimensions=("k",), cost_pct=1.0,
                overrides={"_group_key": lambda row, dims: ("g",), "_checkpoint_return": lambda row, h: row["r"] if h == "+5m" else None,
                           "candidate_day": lambda row: row["d"], "_text": lambda v, fb="unknown": "T", "_profit_factor": lambda vals: 7.0 if seen.append(len(vals)) is None else 0,
                           "HORIZONS": ("+5m", "+7m"), "MIN_OBSERVATIONS": 1, "MIN_DAYS": 1, "MAX_DAY_SHARE": 1.0, "MAX_SYMBOL_SHARE": 1.0,
                           "MIN_AVERAGE_NET_RETURN_PCT": -100.0, "MIN_NET_PROFIT_FACTOR": 0.0})
    assert len(out) == 1 and out[0]["horizon"] == "+5m" and out[0]["net_profit_factor"] == 7.0 and out[0]["top_symbols"] == [{"symbol": "T", "count": 6}]
    assert seen == [6, 6]  # called once per side


def test_combo_rows_counter_defaultdict_seams(orig_nodes, monkeypatch, guards):
    import collections
    made = []

    class SpyCounter(collections.Counter):
        def __init__(self, *a, **k):
            made.append(1)
            super().__init__(*a, **k)
    check(orig_nodes, monkeypatch, "_combo_rows", _big(), dimensions=("tactic",), cost_pct=0.9, overrides={"Counter": SpyCounter})
    assert made and len(made) % 2 == 0  # both sides resolve Counter at call time


# ---- A41-4 build_horizon_alignment_review ----
def _fake_loader(payloads):
    def loader(*, reports_root, start, end):
        return [{"candidates": [{"echo": (str(reports_root), start, end)}]}] + copy.deepcopy(payloads)
    return loader


PROFILES = [{}, {"source": "fake", "sample_count": 7, "ema_round_trip_cost_pct": 0.004, "conservative_round_trip_cost_pct": 0.006},
            {"ema_round_trip_cost_pct": 0.002}, {"conservative_round_trip_cost_pct": 0, "ema_round_trip_cost_pct": 0.01, "sample_count": "3"}]


def _combo_spy(decisions):
    def combo(candidates, *, dimensions, cost_pct):
        return [{"echo": (len(candidates), dimensions, cost_pct), "decision": d, "cost_positive": d == "CPOS"} for d in decisions]
    return combo


@pytest.mark.parametrize("profile", PROFILES)
@pytest.mark.parametrize("decisions", [[], ["INSUFFICIENT_EVIDENCE"], ["RETAIN_UNDER_OBSERVATION", "INSUFFICIENT_EVIDENCE"], ["CPOS", "RETAIN_UNDER_OBSERVATION"]])
def test_build_review_fake_seams(orig_nodes, monkeypatch, guards, profile, decisions):
    ov = {"load_quant_shadow_candidate_payloads_for_range": _fake_loader([]), "load_broker_cost_profile": lambda path: dict(profile),
          "_candidate_rows": lambda payloads: [c for p in payloads for c in p["candidates"]], "_combo_rows": _combo_spy(decisions)}
    out = check(orig_nodes, monkeypatch, "build_horizon_alignment_review", reports_root=Path("rr"), start="2026-04-10T09:00", end="2026-04-14", overrides=ov)
    assert out["schema_version"] == "horizon_alignment_review.v2" and out["range"] == {"start": "2026-04-10", "end": "2026-04-14"}
    assert out["time_tactic"][0:1] == ([] if not decisions else [{"echo": (1, ("time_bucket", "tactic"), out["cost_model"]["conservative_round_trip_cost_pct"]), **{
        "decision": decisions[0], "cost_positive": decisions[0] == "CPOS"}}]) or not decisions


def test_build_review_cost_path_and_default_args(orig_nodes, monkeypatch, guards):
    seen = []
    ov = {"load_quant_shadow_candidate_payloads_for_range": _fake_loader([]), "load_broker_cost_profile": lambda path: seen.append(path) or {},
          "_candidate_rows": lambda payloads: [], "_combo_rows": _combo_spy([])}
    out = check(orig_nodes, monkeypatch, "build_horizon_alignment_review", reports_root=Path("rr"), start="a", end="b", overrides=ov)
    assert out["cost_model"]["profile_path"] == "data/state/broker_cost_profile.json" and out["cost_model"]["conservative_round_trip_cost_pct"] == 0.009 * 100.0
    assert out["decision"] == "NO_COST_POSITIVE_COMBINATION" and out["next_action"]["decision"] == "REJECT_CURRENT_HYPOTHESIS_AND_RESEARCH_NEW_ALPHA"
    check(orig_nodes, monkeypatch, "build_horizon_alignment_review", reports_root=Path("rr"), start="a", end="b", cost_profile_path=Path("cp.json"), overrides=ov)
    assert seen[0] is None and seen[2] == Path("cp.json") and len(seen) == 4
    out = check(orig_nodes, monkeypatch, "build_horizon_alignment_review", reports_root=Path("rr"), start="a", end="b", cost_profile_path=Path("cp.json"), overrides=ov)
    assert out["cost_model"]["profile_path"] == "cp.json"
    sig = inspect.signature(MODS["horizon_alignment"].build_horizon_alignment_review)
    assert all(p.kind.name == "KEYWORD_ONLY" for p in sig.parameters.values()) and sig.parameters["cost_profile_path"].default is None


def test_build_review_real_combo_and_errors(orig_nodes, monkeypatch, guards):
    payloads = [{"generated_at": "2026-04-10T00:00:00+00:00", "candidates": _big(2.0, 24)}]
    ov = {"load_quant_shadow_candidate_payloads_for_range": _fake_loader(payloads), "load_broker_cost_profile": lambda path: {"conservative_round_trip_cost_pct": 0.009},
          "_candidate_rows": lambda ps: [c for p in ps for c in p["candidates"] if "echo" not in c]}
    out = check(orig_nodes, monkeypatch, "build_horizon_alignment_review", reports_root=Path("rr"), start="2026-04-10", end="2026-04-13", overrides=ov)
    assert out["candidate_count"] == 24 and out["decision"] == "CONTROLLED_ADOPTION_CANDIDATE_FOUND"
    assert out["next_action"]["decision"] == "PREPARE_SHADOW_POLICY_SPEC"

    def boom(**k):
        raise ValueError("loader failure")
    got = check(orig_nodes, monkeypatch, "build_horizon_alignment_review", reports_root=Path("rr"), start="a", end="b",
                overrides={"load_quant_shadow_candidate_payloads_for_range": boom})
    assert got == ("err", "ValueError", "loader failure")
    assert check(orig_nodes, monkeypatch, "build_horizon_alignment_review", reports_root=Path("rr"), start=None, end="b",
                 overrides={"load_quant_shadow_candidate_payloads_for_range": _fake_loader([]), "load_broker_cost_profile": lambda p: {},
                            "_candidate_rows": lambda ps: [], "_combo_rows": _combo_spy([])})[0] == "err"


# ---- A41-5 render_horizon_alignment_review ----
ROW = {"dimensions": {"time_bucket": "open", "tactic": "t1"}, "horizon": "+5m", "observed_count": 25, "observed_day_count": 4,
       "average_gross_return_pct": 1.2345, "average_net_return_pct": 0.3345, "net_win_rate": 0.62, "net_profit_factor": 1.5,
       "maximum_day_share": 0.3, "maximum_symbol_share": 0.25, "decision": "CONTROLLED_ADOPTION_CANDIDATE", "worst_leave_one_day_out_net_return_pct": 0.1, "robust_across_days": True}
FULL = {"range": {"start": "2026-04-10", "end": "2026-04-14"}, "cost_model": {"source": "fake한글", "sample_count": 3, "ema_round_trip_cost_pct": 0.4, "conservative_round_trip_cost_pct": 0.9},
        "decision": "CONTROLLED_ADOPTION_CANDIDATE_FOUND", "time_tactic": [ROW, {"dimensions": None, "horizon": "+15m"}, {}],
        "controlled_adoption_candidates": [ROW, {}], "observation_candidates": [ROW], "next_action": {"decision": "PREPARE_SHADOW_POLICY_SPEC", "reason": "why 이유"}}
PAYLOADS = [{}, {"range": None, "cost_model": None, "time_tactic": None}, {"decision": "X"}, FULL, {**FULL, "controlled_adoption_candidates": [], "observation_candidates": []},
            {**FULL, "cost_model": {"ema_round_trip_cost_pct": None}}, {**FULL, "next_action": None}, {"time_tactic": [{"net_win_rate": 1}]}]


@pytest.mark.parametrize("payload", PAYLOADS)
def test_render_review(orig_nodes, monkeypatch, guards, payload):
    out = check(orig_nodes, monkeypatch, "render_horizon_alignment_review", payload)
    assert out.endswith("\n") and "\r" not in out


def test_render_review_exact_and_errors(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_horizon_alignment_review", FULL)
    assert out.startswith("# Horizon Alignment Review (2026-04-10 ~ 2026-04-14)\n\nThis report is evaluation-only. It does not change runtime behavior.\n\n## Cost Basis\n")
    assert "- source: `fake한글`\n- samples: 3\n- EMA round-trip cost: 0.4000%\n- conservative round-trip cost: 0.9000%\n" in out
    assert "| open | t1 | +5m | 25/4 | 1.2345% | 0.3345% | 62.0% | 1.5 | 30.0% | 25.0% | `CONTROLLED_ADOPTION_CANDIDATE` |" in out
    assert "- `open | t1 | +5m`: net 0.3345%, PF 1.5, 25 observations across 4 days\n" in out
    assert "worst leave-one-day-out 0.1%, robust=True\n" in out
    assert out.endswith("- reason: why 이유\n- behavior change authorized: **False**\n")
    empty = check(orig_nodes, monkeypatch, "render_horizon_alignment_review", {})
    assert "## Controlled-Adoption Candidates\n\n- None\n" in empty and "- decision: **None**" in empty
    assert check(orig_nodes, monkeypatch, "render_horizon_alignment_review", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "render_horizon_alignment_review", {"cost_model": {"sample_count": 1, "ema_round_trip_cost_pct": "x"}})[0] == "err"
    assert check(orig_nodes, monkeypatch, "render_horizon_alignment_review", {"time_tactic": ["bad"]})[0] == "err"


# ---- A41-6 attribution_score_v0._mapping ----
@pytest.mark.parametrize("value", [None, {}, {"a": 1}, [], [("a", 1)], "s", 5, {"n": {"deep": [1]}}])
def test_attribution_mapping(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_mapping", value)


def test_attribution_mapping_identity_and_seam(orig_nodes, monkeypatch, guards):
    mod = MODS["attribution_score_v0"]
    src = {"a": 1}
    assert mod._mapping(src) is src
    assert mod._mapping(None) == {} and mod._mapping(None) is not mod._mapping(None)

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_mapping", {"a": 1}, overrides={"Mapping": NeverMapping}) == {}


# ---- A41-7 performance_metrics ----
VALUE_SETS = [[], [1.0], [-1.0], [0.0], [0, 0, 0], [1, 2, 3], [-1, -2, -3], [1, -1, 2, -2, 0], [3.3333333, -1.11111, 0.00005],
              [NAN], [1.0, NAN], [float("inf"), -1.0], ["1.5", "-2", 0], [1e-9, -1e-9], list(range(-5, 6)), (1, -1), {1.0, -2.0}, [True, False]]


@pytest.mark.parametrize("values", VALUE_SETS)
def test_performance_metrics_values(orig_nodes, monkeypatch, guards, values):
    check(orig_nodes, monkeypatch, "performance_metrics", values)


def test_performance_metrics_exact_and_errors(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "performance_metrics", [1.0, -2.0, 3.0, -1.0])
    assert list(out) == ["count", "win_count", "loss_count", "flat_count", "win_rate", "average_return_pct", "average_gain_pct", "average_loss_pct",
                         "profit_factor", "expectancy_pct", "maximum_drawdown_pct"]
    assert out["count"] == 4 and out["win_rate"] == 0.5 and out["profit_factor"] == 1.3333 and out["maximum_drawdown_pct"] == -2.0
    assert check(orig_nodes, monkeypatch, "performance_metrics", [])["profit_factor"] == 0.0
    assert check(orig_nodes, monkeypatch, "performance_metrics", [1.0, 2.0])["profit_factor"] == 999.0  # zero gross loss
    assert check(orig_nodes, monkeypatch, "performance_metrics", [0.0, 0.0])["flat_count"] == 2
    assert check(orig_nodes, monkeypatch, "performance_metrics", ["x"])[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, "performance_metrics", [None])[0:2] == ("err", "TypeError")
    assert check(orig_nodes, monkeypatch, "performance_metrics", None)[0:2] == ("err", "TypeError")


def test_performance_metrics_generator_consumed_once(guards):
    mod = MODS["metrics"]

    def gen():
        yield from (1.0, -0.5, 2.0)
    assert mod.performance_metrics(gen()) == mod.performance_metrics([1.0, -0.5, 2.0])
    consumed = []

    def tracking():
        for v in (1.0, -1.0):
            consumed.append(v)
            yield v
    mod.performance_metrics(tracking())
    assert consumed == [1.0, -1.0]


# ---- A41-8 build_entry_timing_attribution_report ----
def _attach_factory(outcome):
    calls = []

    def attach(items, *, minute_rows_by_symbol):
        calls.append(len(items))
        out = copy.deepcopy(items)
        out[0]["shadow_forward_outcome"] = copy.deepcopy(outcome)
        return out
    attach.calls = calls
    return attach


OUT_OBS = {"available": True, "reason": None, "observed_checkpoint_count": 2,
           "checkpoints": {"+5m": {"status": "observed", "return_pct": 0.8, "mfe_pct": 1.0, "mae_pct": -0.1}, "+15m": {"status": "observed", "return_pct": 1.5, "mfe_pct": 2.0, "mae_pct": -0.2},
                           "+30m": {"status": "pending"}, "+60m": {"status": "pending"}}}
OUT_BAD = {"available": True, "checkpoints": {"+5m": {"status": "observed", "return_pct": -1.0, "mfe_pct": 0.1, "mae_pct": -0.9}}}
MIN_ROWS = {"005930": [{"ts": 1776297000, "close": 100.0}, {"ts": 1776297300, "price": 101.0, "raw_ts": "r"}], "000660": []}
WINDOWS = {"D1": {"decision_epoch": 1776297000, "generated_at": "x", "strategist_selection": {"confirmed_at": 1776297100}},
           "D2": {"generated_at": "2026-04-16T00:00:00+00:00"}}


def _model(trade="T1", symbol="005930", decision="D1", lane=None, defects=None, entry_ts=1776297600, price=102.0, ret=0.5, horizon="intraday"):
    m = {"trade_id": trade, "symbol": symbol, "selection": {"q9_decision_id": decision, "selected_symbol": symbol, "selected_rank": 2, "raw_scanner_top1": {"symbol": "AAA"},
                                                           "scanner_top1": {"symbol": "BBB"}, "selected_at": 1776297200, "selected_candidate": {"rank": 3}},
         "entry": {"timestamp": entry_ts, "price": price}, "outcome": {"net_return_pct": ret}, "horizon_contract": {"strategy_horizon": horizon},
         "controlled_mock_lane": lane or {}, "integrity": {"defects": defects or []}}
    return m


def _ov(outcome=OUT_OBS, windows=WINDOWS, rows=MIN_ROWS):
    loads = []
    return {"attach_forward_outcomes": _attach_factory(outcome), "_daily_windows_by_id": lambda root, day: copy.deepcopy(windows),
            "load_minute_rows_from_state": lambda: loads.append(1) or copy.deepcopy(rows)}, loads


def _run(orig_nodes, monkeypatch, models, outcome=OUT_OBS, windows=WINDOWS, rows=MIN_ROWS, **extra):
    ov, loads = _ov(outcome, windows, rows)
    return check(orig_nodes, monkeypatch, "build_entry_timing_attribution_report", day="2026-04-16", models=models, overrides=ov, **extra), loads


def test_build_report_empty_and_default_loader(orig_nodes, monkeypatch, guards):
    out, loads = _run(orig_nodes, monkeypatch, [])
    assert out["trade_count"] == 0 and out["excluded_trade_count"] == 0 and out["rows"] == [] and len(loads) == 2  # loader used once per side (rows missing)
    assert [r["label"] for r in out["label_summary"]] == list(MODS["entry_timing_attribution"].LABELS)
    out, loads = _run(orig_nodes, monkeypatch, [], minute_rows_by_symbol={"005930": []})
    assert loads == []  # injected rows: real loader never called
    out, loads = _run(orig_nodes, monkeypatch, [], minute_rows_by_symbol={})
    assert loads == []  # empty dict is not None


@pytest.mark.parametrize("outcome", [OUT_OBS, OUT_BAD, {}, {"available": False, "reason": "minute_rows_unavailable", "checkpoints": {}}])
@pytest.mark.parametrize("variant", range(5))
def test_build_report_variants(orig_nodes, monkeypatch, guards, outcome, variant):
    models = [[_model()], [_model(lane={"selection_authority": "deterministic_independent_lane", "signal_epoch": 1776297300, "lane_id": "LX"})],
              [_model(decision="D2", entry_ts="2026-04-16T00:10:00Z"), _model(trade="T2", symbol="000660", decision="NONE", price=None)],
              [_model(entry_ts=0, ret=None), _model(symbol="", price=-1)],
              [_model(horizon="swing"), _model(trade="T3", horizon="scalp", ret="bad")]][variant]
    _run(orig_nodes, monkeypatch, models, outcome=outcome)


def test_build_report_exclusion_and_exact_bits(orig_nodes, monkeypatch, guards):
    models = [_model(), _model(trade="T2", defects=["broker_day_partial_exit_duplicate"]), _model(trade="T3", defects=["confirmed_runtime_defect"]), _model(trade="T4", defects=["other"])]
    out, _ = _run(orig_nodes, monkeypatch, models)
    assert out["trade_count"] == 2 and out["excluded_trade_count"] == 2 and [r["trade_id"] for r in out["rows"]] == ["T1", "T4"]
    row = out["rows"][0]
    assert row["selection_authority"] == "main_scanner_pipeline" and row["selected_rank"] == 2 and row["strategy_horizon"] == "intraday"
    assert row["missing_stage_timestamps"] == ["strategist_confirm_time"] or row["missing_stage_timestamps"] == []
    assert row["entry_forward_quality"]["+5m_return_pct"] == 0.8 and row["entry_forward_quality"]["forward_available"] is True
    assert out["schema_version"] == "entry_timing_attribution_report.v1" and out["limitations"][1] == "Labels are attribution hypotheses, not trading behavior."
    assert list(out)[:8] == ["schema_version", "measurement_contract_version", "evaluation_program_id", "behavior_effect", "day", "trade_count", "excluded_trade_count", "label_summary"]


def test_build_report_independent_lane_and_stage_gaps(orig_nodes, monkeypatch, guards):
    lane = {"selection_authority": "deterministic_independent_lane", "signal_epoch": 1776297300, "lane_id": "LX"}
    out, _ = _run(orig_nodes, monkeypatch, [_model(lane=lane), _model(trade="T2", decision="ZZ")])
    a, b = out["rows"]
    assert a["selection_authority"] == "deterministic_independent_lane" and a["selected_rank"] is None and a["missing_stage_timestamps"] == [] and a["controlled_lane_id"] == "LX"
    assert b["stage_timing_status"] == "PARTIAL" and b["missing_stage_timestamps"] == ["strategist_confirm_time", "selected_candidate_time"] or b["stage_timing_status"] in ("PARTIAL", "COMPLETE")


def test_build_report_errors_and_seams(orig_nodes, monkeypatch, guards):
    ov, _ = _ov()
    assert check(orig_nodes, monkeypatch, "build_entry_timing_attribution_report", day="d", models=[None], overrides=ov)[0:2] == ("err", "AttributeError")
    assert check(orig_nodes, monkeypatch, "build_entry_timing_attribution_report", day="d", models=None, overrides=ov)[0:2] == ("err", "TypeError")

    def boom():
        raise RuntimeError("loader failure")
    got = check(orig_nodes, monkeypatch, "build_entry_timing_attribution_report", day="d", models=[], overrides={**ov, "load_minute_rows_from_state": boom})
    assert got == ("err", "RuntimeError", "loader failure")
    out = check(orig_nodes, monkeypatch, "build_entry_timing_attribution_report", day="d", models=[_model()], overrides={**ov, "_label": lambda **k: ("ENTRY_APPROPRIATE", ["r"]),
                "_pre_entry_move_pct": lambda **k: (9.9, {"x": 1})})
    assert out["rows"][0]["label"] == "ENTRY_APPROPRIATE" and out["rows"][0]["pre_entry_move_pct"] == 9.9
    sig = inspect.signature(MODS["entry_timing_attribution"].build_entry_timing_attribution_report)
    assert all(p.kind.name == "KEYWORD_ONLY" for p in sig.parameters.values()) and sig.parameters["reports_root"].default == Path("reports")
    assert sig.parameters["minute_rows_by_symbol"].default is None


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
