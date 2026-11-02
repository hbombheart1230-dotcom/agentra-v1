"""RF-032 A52-1..8: eight ``full_chain_component_review`` helper bodies, original vs thin wrappers + Owners.

Original = A preimage 373af145 (SOURCE blob dc1e6c50 == canonical 78b1da2e). Each original function is compiled from
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

A_PRE = "373af1457fb8ebe11ef3ba61105d66592143ae65"
CANON = "78b1da2e54fd1bc771bf2d5315c780c5edf98f86"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_number": ("full_chain_component_review", "dc1e6c5017e537057864be84b659f0803efa0a8c", "full_chain_component_review_number"),
    "_behavior_metric_eligible": ("full_chain_component_review", "dc1e6c5017e537057864be84b659f0803efa0a8c", "full_chain_component_review_behavior_metric_eligible"),
    "_topk_metric": ("full_chain_component_review", "dc1e6c5017e537057864be84b659f0803efa0a8c", "full_chain_component_review_topk_metric"),
    "_classify_root_cause": ("full_chain_component_review", "dc1e6c5017e537057864be84b659f0803efa0a8c", "full_chain_component_review_classify_root_cause"),
    "_role_metrics": ("full_chain_component_review", "dc1e6c5017e537057864be84b659f0803efa0a8c", "full_chain_component_review_role_metrics"),
    "_paired_role_deltas": ("full_chain_component_review", "dc1e6c5017e537057864be84b659f0803efa0a8c", "full_chain_component_review_paired_role_deltas"),
    "_selection_availability": ("full_chain_component_review", "dc1e6c5017e537057864be84b659f0803efa0a8c", "full_chain_component_review_selection_availability"),
    "_q9_decision_candidate_rows": ("full_chain_component_review", "dc1e6c5017e537057864be84b659f0803efa0a8c", "full_chain_component_review_q9_decision_candidate_rows"),
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

FC = MODS["full_chain_component_review"]


class _Str:
    def __init__(self, text, truthy=True):
        self.text, self.truthy = text, truthy

    def __repr__(self):
        return f"_Str({self.text!r},{self.truthy})"

    def __str__(self):
        return self.text


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


class _Num:
    def __repr__(self):
        return "_Num()"

    def __float__(self):
        return 2.5


class _FloatErr:
    def __init__(self, exc):
        self.exc = exc

    def __repr__(self):
        return f"_FloatErr({self.exc.__name__})"

    def __float__(self):
        raise self.exc("custom float failure")


class NeverMapping:
    pass


VALS = [None, "", 0, 0.0, "0", " 1.5 ", "abc", "1e3", "nan", "inf", NAN, True, [], {}, b"2", _Num(), _FloatErr(TypeError), _FloatErr(ValueError), (), "-0", -3]


# ---- A52-1 _number ----
@pytest.mark.parametrize("value", VALS)
def test_number(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_number", value)


def test_number_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_number", None) is None and check(orig_nodes, monkeypatch, "_number", "") is None and check(orig_nodes, monkeypatch, "_number", 0) == 0.0
    assert check(orig_nodes, monkeypatch, "_number", _FloatErr(TypeError)) is None and check(orig_nodes, monkeypatch, "_number", _FloatErr(ValueError)) is None
    assert check(orig_nodes, monkeypatch, "_number", _FloatErr(RuntimeError)) == ("err", "RuntimeError", "custom float failure")  # only TypeError/ValueError caught
    out = check(orig_nodes, monkeypatch, "_number", "nan")
    assert out != out


# ---- A52-2 _behavior_metric_eligible ----
BM = [{}, None, {"integrity": None}, {"integrity": "bad"}, {"integrity": {}}, {"integrity": {"defects": []}}, {"integrity": {"defects": None}}, {"integrity": {"defects": ["other"]}},
      {"integrity": {"defects": ["broker_day_partial_exit_duplicate"]}}, {"integrity": {"defects": ["confirmed_runtime_defect", "x"]}}, {"integrity": {"defects": ("confirmed_runtime_defect",)}},
      {"integrity": {"defects": [1, 2]}}, {"integrity": _MapSub(defects=["confirmed_runtime_defect"])}, {"integrity": {"defects": [_Str("confirmed_runtime_defect")]}}, {"integrity": {"defects": "confirmed_runtime_defect"}},
      {"integrity": {"defects": 5}}]


@pytest.mark.parametrize("model", BM)
def test_behavior_metric_eligible(orig_nodes, monkeypatch, guards, model):
    check(orig_nodes, monkeypatch, "_behavior_metric_eligible", model)


def test_behavior_metric_eligible_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_behavior_metric_eligible", {"integrity": {"defects": ["other"]}}) is True
    assert check(orig_nodes, monkeypatch, "_behavior_metric_eligible", {"integrity": {"defects": ["confirmed_runtime_defect"]}}) is False
    assert check(orig_nodes, monkeypatch, "_behavior_metric_eligible", {}) is True and check(orig_nodes, monkeypatch, "_behavior_metric_eligible", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "_behavior_metric_eligible", {"integrity": {"defects": ["other"]}}, overrides={"BEHAVIOR_METRIC_EXCLUSION_DEFECTS": {"other"}}) is False


def test_behavior_metric_eligible_mapping_seam(orig_nodes, monkeypatch, guards):
    # call-time ``Mapping`` lookup on the facade: with a never-matching Mapping the integrity block is ignored
    assert check(orig_nodes, monkeypatch, "_behavior_metric_eligible", {"integrity": {"defects": ["confirmed_runtime_defect"]}}, overrides={"Mapping": NeverMapping}) is True


# ---- A52-3 _topk_metric ----
def _tk(*rows):
    return {"topk_forward_performance": {"rows": list(rows)}}


TKS = [{}, None, {"topk_forward_performance": None}, {"topk_forward_performance": "x"}, {"topk_forward_performance": {}}, {"topk_forward_performance": {"rows": None}},
       _tk({"top_k": 1, "horizon": "+30m", "v": 1}), _tk({"top_k": 3, "horizon": "+30m", "v": 3}, {"top_k": 1, "horizon": "+30m", "v": 1}, {"top_k": 1, "horizon": "+30m", "v": "dup"}),
       _tk("bad", None, {"top_k": "1", "horizon": "+30m", "v": "str"}), _tk({"top_k": None, "horizon": None, "v": 0}), _tk({"top_k": "x", "horizon": "+30m"}), _tk({"top_k": 1, "horizon": 5}),
       _tk(_MapSub(top_k=1, horizon="+30m", v=9)), {"topk_forward_performance": _MapSub(rows=[{"top_k": 1, "horizon": "+30m", "v": 8}])}]


@pytest.mark.parametrize("review", TKS)
@pytest.mark.parametrize("top_k,horizon", [(1, "+30m"), (3, "+30m"), (0, ""), (1, "+5m"), (10, "+30m")])
def test_topk_metric(orig_nodes, monkeypatch, guards, review, top_k, horizon):
    check(orig_nodes, monkeypatch, "_topk_metric", review, top_k=top_k, horizon=horizon)


def test_topk_metric_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_topk_metric", TKS[7], top_k=1, horizon="+30m")
    assert out == {"top_k": 1, "horizon": "+30m", "v": 1}  # first match wins
    row = {"top_k": 1, "horizon": "+30m", "v": 1}
    got = FC._topk_metric(_tk(row), top_k=1, horizon="+30m")
    assert got == row and got is not row  # copy
    assert check(orig_nodes, monkeypatch, "_topk_metric", {}, top_k=1, horizon="+30m") == {} and check(orig_nodes, monkeypatch, "_topk_metric", None, top_k=1, horizon="+30m")[0] == "err"
    assert check(orig_nodes, monkeypatch, "_topk_metric", TKS[10], top_k=1, horizon="+30m")[0:2] == ("err", "ValueError")
    assert [p.kind.name for p in inspect.signature(FC._topk_metric).parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY", "KEYWORD_ONLY"]
    assert check(orig_nodes, monkeypatch, "_topk_metric", TKS[7], top_k=1, horizon="+30m", overrides={"Mapping": NeverMapping}) == {}


# ---- A52-4 _classify_root_cause ----
def _tkm(window, days, net):
    return {"window_count": window, "observed_day_count": days, "net": {"expectancy_pct": net}}


def _sq(top1=None, top3=None):
    rows = []
    if top1 is not None:
        rows.append({"top_k": 1, "horizon": "+30m", **top1})
    if top3 is not None:
        rows.append({"top_k": 3, "horizon": "+30m", **top3})
    return {"topk_forward_performance": {"rows": rows}}


def _attr(strat=(0, 0, None), cmd=(0, 0, None)):
    return {"by_horizon": [{"horizon": "+30m", "strategist_comparison_count": strat[0], "strategist_day_count": strat[1], "average_strategist_delta_pct": strat[2],
                            "commander_comparison_count": cmd[0], "commander_day_count": cmd[1], "average_commander_delta_pct": cmd[2]}]}


ENOUGH_SQ = _sq(_tkm(30, 3, -0.5), _tkm(30, 3, -0.1))
CLS = {
    "empty": dict(scanner_quality={}, attribution={}, entry={}, exit_hold={}),
    "scanner_fail": dict(scanner_quality=ENOUGH_SQ, attribution={}, entry={}, exit_hold={}),
    "scanner_ok_not_fail": dict(scanner_quality=_sq(_tkm(30, 3, 0.2), _tkm(30, 3, -0.1)), attribution={}, entry={}, exit_hold={}),
    "scanner_short": dict(scanner_quality=_sq(_tkm(5, 3, -0.5), _tkm(5, 3, -0.1)), attribution={}, entry={}, exit_hold={}),
    "strategist_fail": dict(scanner_quality={}, attribution=_attr((25, 3, -0.4)), entry={}, exit_hold={}),
    "strategist_exact_threshold": dict(scanner_quality={}, attribution=_attr((25, 3, -0.30)), entry={}, exit_hold={}),
    "commander_fail": dict(scanner_quality={}, attribution=_attr(cmd=(25, 3, -0.5)), entry={}, exit_hold={}),
    "entry_fail": dict(scanner_quality={}, attribution={}, entry={"matched_trade_count": 25, "matched_day_count": 3, "average_entry_price_delta_pct": 0.31}, exit_hold={}),
    "entry_exact_threshold": dict(scanner_quality={}, attribution={}, entry={"matched_trade_count": 25, "matched_day_count": 3, "average_entry_price_delta_pct": 0.30}, exit_hold={}),
    "exit_fail": dict(scanner_quality={}, attribution={}, entry={}, exit_hold={"observed_trade_count": 25, "observed_day_count": 3, "by_hold_offset": [{"offset": "+15m", "average_improvement_pct": 9}, {"offset": "+5m", "average_improvement_pct": 0.3}]}),
    "all_enough_none_fail": dict(scanner_quality=_sq(_tkm(30, 3, 0.5), _tkm(30, 3, 0.5)), attribution=_attr((25, 3, 0.1), (25, 3, 0.1)),
                                 entry={"matched_trade_count": 25, "matched_day_count": 3, "average_entry_price_delta_pct": 0.0},
                                 exit_hold={"observed_trade_count": 25, "observed_day_count": 3, "by_hold_offset": [{"offset": "+5m", "average_improvement_pct": 0.0}]}),
    "multiple_fail_priority": dict(scanner_quality=ENOUGH_SQ, attribution=_attr((25, 3, -0.4), (25, 3, -0.4)), entry={"matched_trade_count": 25, "matched_day_count": 3, "average_entry_price_delta_pct": 1.0},
                                   exit_hold={"observed_trade_count": 25, "observed_day_count": 3, "by_hold_offset": [{"offset": "+5m", "average_improvement_pct": 1.0}]}),
    "bad_shapes": dict(scanner_quality={"topk_forward_performance": "x"}, attribution={"by_horizon": ["bad", None, {"horizon": "+30m"}]}, entry={"matched_trade_count": "x"}, exit_hold={"by_hold_offset": ["bad"]}),
    "string_numbers": dict(scanner_quality=_sq(_tkm(30, 3, "-0.5"), _tkm(30, 3, "-0.1")), attribution=_attr((25, 3, "-0.4")), entry={}, exit_hold={}),
}


@pytest.mark.parametrize("case", list(CLS))
def test_classify_root_cause(orig_nodes, monkeypatch, guards, case):
    check(orig_nodes, monkeypatch, "_classify_root_cause", **CLS[case])


def test_classify_root_cause_exact_and_seams(orig_nodes, monkeypatch, guards):
    got = {k: check(orig_nodes, monkeypatch, "_classify_root_cause", **v)["primary_root_cause"] for k, v in CLS.items() if k != "bad_shapes"}
    assert got == {"empty": "insufficient_sample", "scanner_fail": "scanner_intrinsic_fail", "scanner_ok_not_fail": "insufficient_sample", "scanner_short": "insufficient_sample", "strategist_fail": "strategist_degradation",
                   "strategist_exact_threshold": "strategist_degradation", "commander_fail": "commander_over_filtering", "entry_fail": "monitor_entry_fail", "entry_exact_threshold": "insufficient_sample",
                   "exit_fail": "monitor_exit_fail", "all_enough_none_fail": "no_dominant_problem", "multiple_fail_priority": "scanner_intrinsic_fail", "string_numbers": "scanner_intrinsic_fail"}
    out = check(orig_nodes, monkeypatch, "_classify_root_cause", **CLS["multiple_fail_priority"])
    assert list(out) == ["schema_version", "behavior_effect", "primary_root_cause", "statuses", "sample_status", "evidence"] and list(out["statuses"]) == ["scanner_intrinsic_fail", "strategist_degradation", "commander_over_filtering", "monitor_entry_fail", "monitor_exit_fail"]
    assert list(out["sample_status"]) == ["scanner", "strategist", "commander", "monitor_entry", "monitor_exit"] and out["evidence"]["monitor_exit_5m_improvement_pct"] == 1.0
    assert check(orig_nodes, monkeypatch, "_classify_root_cause", scanner_quality=None, attribution={}, entry={}, exit_hold={})[0] == "err"
    assert [p.kind.name for p in inspect.signature(FC._classify_root_cause).parameters.values()] == ["KEYWORD_ONLY"] * 4
    out = check(orig_nodes, monkeypatch, "_classify_root_cause", **CLS["empty"], overrides={"DIRECTIONAL_MIN_OBSERVATIONS": 0, "DIRECTIONAL_MIN_DAYS": 0})
    assert out["primary_root_cause"] == "no_dominant_problem"


def test_classify_root_cause_helper_seams(orig_nodes, monkeypatch, guards):
    calls = []
    out = check(orig_nodes, monkeypatch, "_classify_root_cause", **CLS["empty"],
                overrides={"_topk_metric": lambda sq, *, top_k, horizon: calls.append((top_k, horizon)) or {"window_count": 99, "observed_day_count": 9, "net": {"expectancy_pct": -1}}})
    assert out["primary_root_cause"] == "scanner_intrinsic_fail" and calls == [(1, "+30m"), (3, "+30m")] * 2


def test_classify_root_cause_threshold_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_classify_root_cause", **CLS["strategist_exact_threshold"], overrides={"MIN_MATERIAL_RANKING_DELTA_PCT": 0.5})
    assert out["primary_root_cause"] == "insufficient_sample"


def test_classify_root_cause_mapping_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_classify_root_cause", **CLS["exit_fail"], overrides={"Mapping": NeverMapping})
    assert out["primary_root_cause"] == "insufficient_sample" and out["evidence"]["monitor_exit_5m_improvement_pct"] is None


# ---- A52-5 _role_metrics ----
def _cand(role, ret, day="2026-04-10", h="+5m"):
    return {"shadow_role": role, "generated_at": f"{day}T00:00:00+00:00", "shadow_forward_outcome": {"checkpoints": {h: {"status": "observed", "return_pct": ret}}}}


RM = [[], [_cand("top_pick", 1.0), _cand("top_pick", 2.0, day="2026-04-11"), _cand("runner_up_evaluated", 5.0), _cand("top_pick", None), _cand("other", 9.0), {"shadow_role": "top_pick"},
           _cand("top_pick", -1.0, h="+15m"), _cand(None, 1.0)], [_cand("top_pick", "bad")], [_cand("top_pick", 0.0)], [_cand("top_pick", 1.0, day="")]]


@pytest.mark.parametrize("cands", RM)
@pytest.mark.parametrize("cost", [0.0, 0.9, -0.5])
@pytest.mark.parametrize("role,horizon", [("top_pick", "+5m"), ("runner_up_evaluated", "+5m"), ("top_pick", "+15m"), ("", "+5m"), ("missing", "EOD")])
def test_role_metrics(orig_nodes, monkeypatch, guards, cands, cost, role, horizon):
    check(orig_nodes, monkeypatch, "_role_metrics", cands, role=role, horizon=horizon, cost_pct=cost)


def test_role_metrics_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_role_metrics", RM[1], role="top_pick", horizon="+5m", cost_pct=0.5)
    assert list(out)[:6] == ["role", "horizon", "evidence_class", "observed_count", "observed_day_count", "cost_adjusted"] and out["observed_count"] == 2 and out["observed_day_count"] == 2 and out["cost_adjusted"] is True
    assert out["evidence_class"] == "TRUSTED_SHADOW" and out["count"] == 2 and out["average_return_pct"] == 1.0  # (1.0-0.5 + 2.0-0.5) / 2
    assert check(orig_nodes, monkeypatch, "_role_metrics", None, role="top_pick", horizon="+5m", cost_pct=0.0)[0] == "err"
    out = check(orig_nodes, monkeypatch, "_role_metrics", RM[1], role="top_pick", horizon="+5m", cost_pct=0.0,
                overrides={"performance_metrics": lambda vals: {"n": len(vals)}, "candidate_day": lambda r: "D", "_checkpoint_return": lambda r, h: 7.0})
    assert out["observed_count"] == 5 and out["observed_day_count"] == 1 and out["n"] == 5


# ---- A52-6 _paired_role_deltas ----
def _pc(role, ret, window="w1", day="2026-04-10", h="+5m"):
    return {"shadow_role": role, "_payload_generated_at": window, "generated_at": f"{day}T00:00:00+00:00", "shadow_forward_outcome": {"checkpoints": {h: {"status": "observed", "return_pct": ret}}}}


PD = [[], [_pc("top_pick", 2.0), _pc("runner_up_evaluated", 1.0), _pc("top_pick", 4.0), _pc("top_pick", 1.0, "w2", "2026-04-11"), _pc("runner_up_evaluated", 3.0, "w2", "2026-04-11"),
           _pc("top_pick", 5.0, "w3"), _pc("other", 9.0), _pc("top_pick", None, "w4"), _pc("top_pick", 1.0, ""), _pc("runner_up_evaluated", 1.0, "w5"), {"shadow_role": "top_pick"}],
      [_pc("top_pick", 1.0), _pc("runner_up_evaluated", 1.0)], [_pc("top_pick", 1.0, day=""), _pc("runner_up_evaluated", 1.0, day="")], [_pc("top_pick", 1.0, h="+15m"), _pc("runner_up_evaluated", 3.0, h="+15m")]]


@pytest.mark.parametrize("cands", PD)
@pytest.mark.parametrize("horizon", ["+5m", "+15m", "EOD"])
def test_paired_role_deltas(orig_nodes, monkeypatch, guards, cands, horizon):
    check(orig_nodes, monkeypatch, "_paired_role_deltas", cands, horizon=horizon)


def test_paired_role_deltas_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_paired_role_deltas", PD[1], horizon="+5m")
    assert list(out) == ["horizon", "comparison", "evidence_class", "paired_window_count", "observed_day_count", "average_delta_pct", "positive_delta_rate", "delta_distribution"]
    assert out["paired_window_count"] == 2 and out["average_delta_pct"] == 0.0 and out["positive_delta_rate"] == 0.5  # windows w1 (+2.0) and w2 (-2.0)
    assert out["observed_day_count"] == 0  # candidate_day() derives from _payload_generated_at, and "w1"/"w2" are not dates
    empty = check(orig_nodes, monkeypatch, "_paired_role_deltas", [], horizon="+5m")
    assert empty["average_delta_pct"] is None and empty["positive_delta_rate"] is None and empty["paired_window_count"] == 0
    assert check(orig_nodes, monkeypatch, "_paired_role_deltas", None, horizon="+5m")[0] == "err"
    out = check(orig_nodes, monkeypatch, "_paired_role_deltas", PD[2], horizon="+5m", overrides={"performance_metrics": lambda vals: {"n": len(vals)}, "candidate_day": lambda r: "D"})
    assert out["delta_distribution"] == {"n": 1} and out["observed_day_count"] == 1
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "_paired_role_deltas", PD[2], horizon="+5m", overrides={"defaultdict": spy})
    assert len(made) >= 2 and len(made) % 2 == 0  # outer defaultdict (and its inner factory) resolved at call time on both sides


# ---- A52-7 _selection_availability ----
def _sel(raw_src="control_snapshot", raw=("x",), run="r", post=("y",), cmd=True):
    s = {}
    if raw_src is not None:
        s["raw_scanner_snapshot_source"] = raw_src
    if raw is not None:
        s["raw_scanner_top10"] = list(raw)
    if run is not None:
        s["strategist_run_id"] = run
    if post is not None:
        s["post_strategist_top10"] = list(post)
    if cmd is not None:
        s["commander_final_explicit"] = cmd
    return {"selection": s}


SA = [_sel(), _sel("scanner_intrinsic_control_snapshot"), _sel("other"), _sel(raw=()), _sel(raw=None), _sel(run=None), _sel(run=""), _sel(post=()), _sel(post=None), _sel(cmd=False), _sel(cmd=None),
      _sel("control_snapshot", ("x",), "r", ("y",), 1), {}, {"selection": None}, {"selection": "bad"}, {"selection": {"raw_scanner_top10": "notalist", "raw_scanner_snapshot_source": "control_snapshot"}},
      {"selection": _MapSub(strategist_run_id="r", post_strategist_top10=["y"], commander_final_explicit=True)}]


@pytest.mark.parametrize("models", [[], SA, SA[:3], SA[3:9], SA[9:], [SA[0]] * 3])
def test_selection_availability(orig_nodes, monkeypatch, guards, models):
    check(orig_nodes, monkeypatch, "_selection_availability", models)


def test_selection_availability_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_selection_availability", [_sel(), _sel(raw=()), _sel(cmd=False), {}])
    assert list(out) == ["trade_model_count", "raw_scanner_control_count", "strategist_snapshot_count", "commander_snapshot_count", "scanner_vs_strategist_comparable_count", "strategist_vs_commander_comparable_count", "missing_fields"]
    assert out["trade_model_count"] == 4 and out["raw_scanner_control_count"] == 2 and out["commander_snapshot_count"] == 2 and list(out["missing_fields"]) == sorted(out["missing_fields"])
    assert check(orig_nodes, monkeypatch, "_selection_availability", [])["missing_fields"] == {}
    assert check(orig_nodes, monkeypatch, "_selection_availability", None)[0] == "err" and check(orig_nodes, monkeypatch, "_selection_availability", [None])[0] == "err"
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "_selection_availability", [_sel()], overrides={"defaultdict": spy})
    assert made == [1, 1]


def test_selection_availability_mapping_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_selection_availability", [_sel()], overrides={"Mapping": NeverMapping})
    assert out["raw_scanner_control_count"] == 0 and out["strategist_snapshot_count"] == 0  # selection ignored when Mapping never matches


# ---- A52-8 _q9_decision_candidate_rows ----
def _attach_spy():
    log = []

    def attach(rows):
        log.append(copy.deepcopy(rows))
        return [{**r, "attached": True} for r in rows]
    attach.log = log
    return attach


QP = [[], [{}], [{"q9_decision_candidates": None}], [{"q9_decision_candidates": []}], [{"generated_at": "g", "q9_decision_candidates": [{"a": 1}, "bad", None, {"b": 2, "_payload_generated_at": "keep"}]}],
      [{"generated_at": "g1", "q9_decision_candidates": [{"a": 1}], "candidates": [{"x": 1}]}, {"generated_at": "g2", "q9_decision_candidates": [{"a": 2}, 5]}], [{"candidates": [{"x": 1}]}], [{"q9_decision_candidates": ({"t": 1},)}]]


@pytest.mark.parametrize("payloads", QP)
def test_q9_decision_candidate_rows(orig_nodes, monkeypatch, guards, payloads):
    attach = _attach_spy()
    check(orig_nodes, monkeypatch, "_q9_decision_candidate_rows", payloads, overrides={"attach_forward_outcomes": attach})
    half = len(attach.log) // 2
    assert half * 2 == len(attach.log) and attach.log[:half] == attach.log[half:]


def test_q9_decision_candidate_rows_exact_and_errors(orig_nodes, monkeypatch, guards):
    attach = _attach_spy()
    src = {"a": 1}
    out = check(orig_nodes, monkeypatch, "_q9_decision_candidate_rows", [{"generated_at": "g", "q9_decision_candidates": [src]}], overrides={"attach_forward_outcomes": attach})
    assert out == [{"a": 1, "_payload_generated_at": "g", "attached": True}] and "_payload_generated_at" not in src
    assert check(orig_nodes, monkeypatch, "_q9_decision_candidate_rows", [{"candidates": [{"x": 1}]}], overrides={"attach_forward_outcomes": attach}) == []  # only q9_decision_candidates is read
    assert check(orig_nodes, monkeypatch, "_q9_decision_candidate_rows", None, overrides={"attach_forward_outcomes": attach})[0] == "err"
    assert check(orig_nodes, monkeypatch, "_q9_decision_candidate_rows", ["x"], overrides={"attach_forward_outcomes": attach})[0] == "err"

    def boom(rows):
        raise RuntimeError("attach failure")
    assert check(orig_nodes, monkeypatch, "_q9_decision_candidate_rows", [{"q9_decision_candidates": [{"a": 1}]}], overrides={"attach_forward_outcomes": boom}) == ("err", "RuntimeError", "attach failure")


def test_q9_decision_candidate_rows_mapping_seam(orig_nodes, monkeypatch, guards):
    attach = _attach_spy()
    assert check(orig_nodes, monkeypatch, "_q9_decision_candidate_rows", [{"q9_decision_candidates": [{"a": 1}]}], overrides={"Mapping": NeverMapping, "attach_forward_outcomes": attach}) == []


def test_q9_decision_candidate_rows_generator_consumed_once(monkeypatch, guards):
    attach = _attach_spy()
    monkeypatch.setattr(FC, "attach_forward_outcomes", attach)
    consumed = []

    def gen():
        for p in ({"generated_at": "g", "q9_decision_candidates": [{"i": 1}]}, {"generated_at": "h", "q9_decision_candidates": [{"i": 2}]}):
            consumed.append(p["generated_at"])
            yield p
    assert [r["i"] for r in FC._q9_decision_candidate_rows(gen())] == [1, 2] and consumed == ["g", "h"]


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
