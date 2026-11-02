"""RF-032 A53-1..8: six ``full_chain_component_review`` and two ``scanner_alignment_root_cause`` bodies, original vs thin wrappers + Owners.

Original = A preimage 20345954 (SOURCE blobs 1d44c646 / 2a595f8d == canonical 437a3f20). Each original function is compiled from
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

A_PRE = "20345954d9c422bf1a15718cfb0e0e9f5e4857dc"
CANON = "437a3f201e9cb45712ee7f52188981ef4719fd46"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_q9_role_row": ("full_chain_component_review", "1d44c646540adffd676ea16489b6212d8bbf5e97", "full_chain_component_review_q9_role_row"),
    "_decision_window_attribution": ("full_chain_component_review", "1d44c646540adffd676ea16489b6212d8bbf5e97", "full_chain_component_review_decision_window_attribution"),
    "_attribution_component": ("full_chain_component_review", "1d44c646540adffd676ea16489b6212d8bbf5e97", "full_chain_component_review_attribution_component"),
    "_scanner_decision": ("full_chain_component_review", "1d44c646540adffd676ea16489b6212d8bbf5e97", "full_chain_component_review_scanner_decision"),
    "_unavailable_component": ("full_chain_component_review", "1d44c646540adffd676ea16489b6212d8bbf5e97", "full_chain_component_review_unavailable_component"),
    "render_full_chain_component_review": ("full_chain_component_review", "1d44c646540adffd676ea16489b6212d8bbf5e97", "full_chain_component_review_render"),
    "classify_scanner_alignment_root_cause": ("scanner_alignment_root_cause", "2a595f8d1025fd6bcc31033d256e7f1766c57ab0", "scanner_alignment_root_cause_classify"),
    "render_scanner_alignment_root_cause_report": ("scanner_alignment_root_cause", "2a595f8d1025fd6bcc31033d256e7f1766c57ab0", "scanner_alignment_root_cause_render"),
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
SA = MODS["scanner_alignment_root_cause"]


class NeverMapping:
    pass


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


# ---- A53-1 _q9_role_row ----
def _r(rank=None, selected=False, tag=None):
    row = {"tag": tag, "q9_selected": selected}
    if rank is not None:
        row["rank"] = rank
    return row


ROLE_SETS = [{}, {"A": []}, {"A": [_r(3, tag="a3"), _r(1, tag="a1"), _r(2, tag="a2")]}, {"A": [_r(tag="norank"), _r(5, tag="a5")]}, {"A": [_r("2", tag="s2"), _r("1.9", tag="s19")]},
             {"B_STRATEGIST_RANKED": [_r(1, tag="b1"), _r(4, selected=True, tag="b4sel"), _r(2, tag="b2")]}, {"B_STRATEGIST_RANKED": [_r(1, tag="b1"), _r(2, tag="b2")]},
             {"B_STRATEGIST_RANKED": [_r(0, selected=False, tag="b0"), _r(3, tag="b3")]}, {"A": [_r(1, tag="x"), _r(1, tag="y")]}, {"A": [_r("x", tag="bad")]}, {"A": [_r(None, tag="n")]}, {"A": None}, {"A": [_r(0, tag="zero"), _r(2, tag="two")]}]


@pytest.mark.parametrize("roles", ROLE_SETS)
@pytest.mark.parametrize("role", ["A", "B_STRATEGIST_RANKED", "missing"])
def test_q9_role_row(orig_nodes, monkeypatch, guards, roles, role):
    check(orig_nodes, monkeypatch, "_q9_role_row", roles, role)


def test_q9_role_row_exact_and_errors(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_q9_role_row", ROLE_SETS[2], "A")["tag"] == "a1"
    assert check(orig_nodes, monkeypatch, "_q9_role_row", ROLE_SETS[5], "B_STRATEGIST_RANKED")["tag"] == "b4sel"  # selected row wins over lower rank
    assert check(orig_nodes, monkeypatch, "_q9_role_row", ROLE_SETS[6], "B_STRATEGIST_RANKED")["tag"] == "b1"
    assert check(orig_nodes, monkeypatch, "_q9_role_row", ROLE_SETS[8], "A")["tag"] == "x"  # min keeps the first of equals
    assert check(orig_nodes, monkeypatch, "_q9_role_row", ROLE_SETS[3], "A")["tag"] == "a5"  # missing rank -> 999
    assert check(orig_nodes, monkeypatch, "_q9_role_row", {}, "A") == {}
    assert check(orig_nodes, monkeypatch, "_q9_role_row", ROLE_SETS[9], "A")[0:2] == ("err", "ValueError") and check(orig_nodes, monkeypatch, "_q9_role_row", None, "A")[0] == "err"
    src = ROLE_SETS[5]["B_STRATEGIST_RANKED"][1]
    assert FC._q9_role_row(ROLE_SETS[5], "B_STRATEGIST_RANKED") is src  # identity, no copy
    assert [p.kind.name for p in inspect.signature(FC._q9_role_row).parameters.values()] == ["POSITIONAL_OR_KEYWORD"] * 2


# ---- A53-2 _decision_window_attribution ----
def _cp(v, status="observed"):
    return {"status": status, "return_pct": v}


def _q(did, role, rets, day="2026-04-10", rank=1, selected=False, no_trade=False):
    return {"q9_decision_id": did, "q9_decision_role": role, "rank": rank, "q9_selected": selected, "q9_commander_no_trade": no_trade,
            "generated_at": f"{day}T00:00:00+00:00", "shadow_forward_outcome": {"checkpoints": {h: _cp(v) for h, v in rets.items()}}}


A_, B_, R1, R2, C_ = "A_SCANNER_CONTROL", "B_STRATEGIST_RANKED", "R1_PRE_REFRESH_SCANNER", "R2_POST_REFRESH_SCANNER", "C_COMMANDER_FINAL"
QROWS = [_q("D1", A_, {"+5m": 1.0, "+30m": 0.5}), _q("D1", B_, {"+5m": 2.0, "+30m": 1.5}, selected=True), _q("D1", R1, {"+5m": 0.0}), _q("D1", R2, {"+5m": 1.0}), _q("D1", C_, {"+5m": 3.0, "+30m": 2.0}),
         _q("D2", A_, {"+5m": 2.0}, day="2026-04-11"), _q("D2", B_, {"+5m": 1.0}, day="2026-04-11"), _q("D2", C_, {}, day="2026-04-11", no_trade=True), _q("D3", B_, {"+5m": 1.0}), _q("D3", C_, {"+5m": None}),
         _q("", A_, {"+5m": 1.0}), _q("D4", "", {"+5m": 1.0}), _q("D5", B_, {"+60m": 1.0}), _q("D5", C_, {"+60m": 2.0})]


@pytest.mark.parametrize("rows", [[], QROWS, QROWS[:5], QROWS[5:8], QROWS[8:10], QROWS[10:]])
@pytest.mark.parametrize("cost", [0.0, 0.9, -0.5])
def test_decision_window_attribution(orig_nodes, monkeypatch, guards, rows, cost):
    check(orig_nodes, monkeypatch, "_decision_window_attribution", [{"generated_at": "g", "q9_decision_candidates": rows}], cost_pct=cost,
          overrides={"attach_forward_outcomes": lambda r: r})


def test_decision_window_attribution_exact_and_seams(orig_nodes, monkeypatch, guards):
    ov = {"attach_forward_outcomes": lambda r: r}
    out = check(orig_nodes, monkeypatch, "_decision_window_attribution", [{"q9_decision_candidates": QROWS}], cost_pct=0.5, overrides=ov)
    assert list(out) == ["schema_version", "role_semantics", "full_strategist_contribution_status", "full_strategist_missing_control", "decision_window_count", "candidate_row_count", "by_horizon"]
    assert out["decision_window_count"] == 4 and out["candidate_row_count"] == 12  # blank decision id / blank role rows are not counted and out["full_strategist_contribution_status"] == "NOT_MEASURABLE" and len(out["by_horizon"]) == 4
    h5 = out["by_horizon"][0]
    assert h5["horizon"] == "+5m" and h5["strategist_comparison_count"] == 2 and h5["average_strategist_delta_pct"] == 0.0 and h5["post_scanner_refresh_comparison_count"] == 1 and h5["average_post_scanner_refresh_delta_pct"] == 1.0
    assert h5["commander_comparison_count"] == 2 and list(h5)[:3] == ["horizon", "strategist_comparison_count", "strategist_day_count"]
    assert h5["strategist_comparison_count"] == h5["strategy_ranking_overlay_comparison_count"]
    empty = check(orig_nodes, monkeypatch, "_decision_window_attribution", [], cost_pct=0.0, overrides=ov)
    assert empty["decision_window_count"] == 0 and empty["by_horizon"][0]["average_strategist_delta_pct"] is None
    assert check(orig_nodes, monkeypatch, "_decision_window_attribution", None, cost_pct=0.0, overrides=ov)[0] == "err"
    assert [p.kind.name for p in inspect.signature(FC._decision_window_attribution).parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY"]
    seen = []
    out = check(orig_nodes, monkeypatch, "_decision_window_attribution", [], cost_pct=0.0, overrides={"_q9_decision_candidate_rows": lambda p: seen.append(p) or [_q("Z", A_, {"+5m": 1}), _q("Z", B_, {"+5m": 4})], "_checkpoint_return": lambda r, h: float(r["shadow_forward_outcome"]["checkpoints"].get(h, {"return_pct": None})["return_pct"] or 0) if h == "+5m" else None,
                                                                                                         "HORIZONS": ("+5m",)})
    assert out["by_horizon"][0]["average_strategist_delta_pct"] == 3.0 and len(seen) == 2
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "_decision_window_attribution", [{"q9_decision_candidates": QROWS[:2]}], cost_pct=0.0, overrides={**ov, "defaultdict": spy})
    assert len(made) >= 2 and len(made) % 2 == 0


# ---- A53-3 _attribution_component ----
def _att(count=30, days=3, delta=0.5, rate=0.7, prefix="strategist", horizon="+30m"):
    return {"by_horizon": [{"horizon": horizon, f"{prefix}_comparison_count": count, f"{prefix}_day_count": days, f"average_{prefix}_delta_pct": delta, f"{prefix}_positive_delta_rate": rate}]}


AV = {"raw_scanner_control_count": 1}
ATTS = {"enough_material": _att(), "enough_not_material_delta": _att(delta=0.1), "enough_not_material_rate": _att(rate=0.5), "boundary": _att(count=20, days=2, delta=0.30, rate=0.55),
        "count_short": _att(count=19), "days_short": _att(days=1), "none_delta": _att(delta=None), "none_rate": _att(rate=None), "bad_numbers": _att(delta="x", rate="y"), "str_numbers": _att(delta="0.5", rate="0.7"),
        "wrong_horizon": _att(horizon="+5m"), "empty": {}, "bad_rows": {"by_horizon": [None]}, "no_by_horizon": {"by_horizon": None}, "commander": _att(prefix="commander")}


@pytest.mark.parametrize("case", list(ATTS))
@pytest.mark.parametrize("component", ["strategist", "commander", "other"])
def test_attribution_component(orig_nodes, monkeypatch, guards, case, component):
    check(orig_nodes, monkeypatch, "_attribution_component", attribution=ATTS[case], component=component, question="Q?", missing_comparison="M", availability=AV)


def test_attribution_component_exact_and_seams(orig_nodes, monkeypatch, guards):
    kw = dict(question="Q?", missing_comparison="M", availability=AV)
    out = check(orig_nodes, monkeypatch, "_attribution_component", attribution=ATTS["enough_material"], component="strategist", **kw)
    assert out["decision"] == "PROMOTION_CANDIDATE" and out["finding"] == "Strategist shows a material +30m delta." and out["missing_comparison"] is None and "availability" not in out
    assert check(orig_nodes, monkeypatch, "_attribution_component", attribution=ATTS["enough_not_material_delta"], component="strategist", **kw)["decision"] == "ADJUST_AND_RETEST"
    short = check(orig_nodes, monkeypatch, "_attribution_component", attribution=ATTS["count_short"], component="commander", **kw)
    assert short["decision"] == "INSUFFICIENT_EVIDENCE" and short["availability"] == AV and short["availability"] is not AV and short["metrics"] is not None
    assert short["finding"] == "Commander has 0 comparable +30m windows across 0 day(s); the fixed 20-observation and 2-day threshold is not complete."
    assert short["missing_comparison"] == "at least 20 comparable +30m windows across 2 days; current=0 windows/0 days"
    assert check(orig_nodes, monkeypatch, "_attribution_component", attribution=ATTS["boundary"], component="strategist", **kw)["decision"] == "PROMOTION_CANDIDATE"  # thresholds are inclusive
    assert check(orig_nodes, monkeypatch, "_attribution_component", attribution=None, component="strategist", **kw)[0] == "err"
    assert check(orig_nodes, monkeypatch, "_attribution_component", attribution=ATTS["bad_rows"], component="strategist", **kw)[0] == "err"
    assert all(p.kind.name == "KEYWORD_ONLY" for p in inspect.signature(FC._attribution_component).parameters.values())
    out = check(orig_nodes, monkeypatch, "_attribution_component", attribution=ATTS["count_short"], component="strategist", **kw, overrides={"DIRECTIONAL_MIN_OBSERVATIONS": 1, "DIRECTIONAL_MIN_DAYS": 1})
    assert out["decision"] == "PROMOTION_CANDIDATE"


def test_attribution_component_decision_class_seam(orig_nodes, monkeypatch, guards):
    class FakeDecision:
        class INSUFFICIENT_EVIDENCE:
            value = "F_INS"

        class PROMOTION_CANDIDATE:
            value = "F_PROMO"

        class ADJUST_AND_RETEST:
            value = "F_ADJ"
    out = check(orig_nodes, monkeypatch, "_attribution_component", attribution=ATTS["enough_material"], component="strategist", question="Q", missing_comparison="M", availability=AV, overrides={"DecisionClass": FakeDecision})
    assert out["decision"] == "F_PROMO"


# ---- A53-4 _scanner_decision ----
def _rm(exp, role="top_pick", horizon="+30m"):
    return {"role": role, "horizon": horizon, "expectancy_pct": exp}


def _pr(n=30, days=3, avg=0.5, rate=0.7, horizon="+30m"):
    return {"horizon": horizon, "paired_window_count": n, "observed_day_count": days, "average_delta_pct": avg, "positive_delta_rate": rate}


SDC = {"retain": ([_rm(0.4)], [_pr()]), "relative_only": ([_rm(-0.4)], [_pr()]), "enough_not_relative": ([_rm(0.4)], [_pr(avg=0.1)]), "insufficient": ([_rm(0.4)], [_pr(n=3)]), "empty": ([], []),
       "boundary": ([_rm(0.0001)], [_pr(n=20, days=2, avg=0.30, rate=0.55)]), "zero_expectancy": ([_rm(0.0)], [_pr()]), "none_values": ([_rm(None)], [_pr(avg=None, rate=None)]), "wrong_horizon": ([_rm(1, horizon="+5m")], [_pr(horizon="+5m")]),
       "wrong_role": ([_rm(1, role="runner_up_evaluated")], [_pr()]), "bad_numbers": ([_rm("x")], [_pr(avg="y")]), "str_numbers": ([_rm("0.4")], [_pr(avg="0.5", rate="0.7")]), "first_match": ([_rm(0.4), _rm(-9)], [_pr(), _pr(n=0)])}


@pytest.mark.parametrize("case", list(SDC))
def test_scanner_decision(orig_nodes, monkeypatch, guards, case):
    rm, pr = SDC[case]
    check(orig_nodes, monkeypatch, "_scanner_decision", role_metrics=rm, paired=pr)


def test_scanner_decision_exact_and_seams(orig_nodes, monkeypatch, guards):
    got = {k: check(orig_nodes, monkeypatch, "_scanner_decision", role_metrics=v[0], paired=v[1]) for k, v in SDC.items() if k not in ("bad_numbers",)}
    assert {k: v["decision"] for k, v in got.items()} == {"retain": "RETAIN", "relative_only": "ADJUST_AND_RETEST", "enough_not_relative": "ADJUST_AND_RETEST", "insufficient": "INSUFFICIENT_EVIDENCE", "empty": "INSUFFICIENT_EVIDENCE",
                                                          "boundary": "RETAIN", "zero_expectancy": "ADJUST_AND_RETEST", "none_values": "ADJUST_AND_RETEST", "wrong_horizon": "INSUFFICIENT_EVIDENCE",
                                                          "wrong_role": "ADJUST_AND_RETEST", "str_numbers": "RETAIN", "first_match": "RETAIN"}
    assert got["relative_only"]["finding"].startswith("Top-pick ordering is directionally better than evaluated runner-ups") and got["insufficient"]["missing_comparison"] == "paired Top-pick and runner-up forward outcomes" and got["retain"]["missing_comparison"] is None
    assert got["retain"]["finding"] == "Scanner ranking and absolute cost-adjusted edge are both positive." and got["enough_not_relative"]["finding"].startswith("Scanner Top-pick ordering does not establish a material ranking effect")
    assert list(got["retain"]) == ["decision", "question", "relative_ranking_effect_positive", "absolute_cost_adjusted_edge_positive", "primary_horizon", "finding", "missing_comparison", "materiality_contract"]
    assert check(orig_nodes, monkeypatch, "_scanner_decision", role_metrics=SDC["bad_numbers"][0], paired=SDC["bad_numbers"][1])[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, "_scanner_decision", role_metrics=[{"role": "top_pick"}], paired=[])[0:2] == ("err", "KeyError")
    assert check(orig_nodes, monkeypatch, "_scanner_decision", role_metrics=None, paired=[])[0] == "err"
    out = check(orig_nodes, monkeypatch, "_scanner_decision", role_metrics=[_rm(1)], paired=[_pr(n=1, days=1, avg=0.2, rate=0.6)], overrides={"DIRECTIONAL_MIN_OBSERVATIONS": 1, "DIRECTIONAL_MIN_DAYS": 1, "MIN_MATERIAL_RANKING_DELTA_PCT": 0.1, "MIN_POSITIVE_RANKING_DELTA_RATE": 0.5})
    assert out["decision"] == "RETAIN" and out["materiality_contract"] == {"minimum_average_delta_pct": 0.1, "minimum_positive_delta_rate": 0.5}


# ---- A53-5 _unavailable_component ----
@pytest.mark.parametrize("availability", [{}, AV, {"nested": {"deep": [1]}}, None, "x"])
@pytest.mark.parametrize("question,missing", [("Q?", "M"), ("", ""), ("한글 질문", "한글 비교"), (None, None)])
def test_unavailable_component(orig_nodes, monkeypatch, guards, availability, question, missing):
    check(orig_nodes, monkeypatch, "_unavailable_component", question=question, missing_comparison=missing, availability=availability)


def test_unavailable_component_exact_and_seam(orig_nodes, monkeypatch, guards):
    av = {"k": [1]}
    out = check(orig_nodes, monkeypatch, "_unavailable_component", question="Q?", missing_comparison="M", availability=av)
    assert list(out) == ["decision", "question", "finding", "missing_comparison", "availability", "behavior_change_authorized"] and out["decision"] == "INSUFFICIENT_EVIDENCE" and out["behavior_change_authorized"] is False
    assert FC._unavailable_component(question="Q", missing_comparison="M", availability=av)["availability"] is av  # identity kept, no copy
    assert out["finding"] == "Historical value-add cannot be measured without the named control comparison."
    assert all(p.kind.name == "KEYWORD_ONLY" for p in inspect.signature(FC._unavailable_component).parameters.values())

    class FakeDecision:
        class INSUFFICIENT_EVIDENCE:
            value = "F_INS"
    assert check(orig_nodes, monkeypatch, "_unavailable_component", question="Q", missing_comparison="M", availability={}, overrides={"DecisionClass": FakeDecision})["decision"] == "F_INS"


# ---- A53-6 render_full_chain_component_review ----
def _tkrow(k, h, win, days, gross, net):
    return {"top_k": k, "horizon": h, "window_count": win, "observed_day_count": days, "gross": {"expectancy_pct": gross}, "net": {"expectancy_pct": net}}


FP = {"range": {"start": "2026-04-10", "end": "2026-04-14"},
      "component_decisions": {"scanner": {"decision": "RETAIN", "finding": "f1", "role_cost_adjusted_metrics": [{"role": "top_pick", "horizon": "+30m", "observed_count": 30, "observed_day_count": 3, "expectancy_pct": 0.4, "win_rate": 0.55, "profit_factor": 1.3}, {}],
                                         "paired_role_comparisons": [{"horizon": "+30m", "paired_window_count": 25, "observed_day_count": 3, "average_delta_pct": 0.5, "positive_delta_rate": 0.64}, {}]},
                              "strategist": {"decision": "INSUFFICIENT_EVIDENCE", "missing_comparison": "mc", "finding": "ignored"}, "commander": {"decision": "X"}, "monitor_entry": {"decision": "D", "metrics": {"matched_trade_count": 3, "matched_day_count": 2, "average_entry_price_delta_pct": 0.1, "median_entry_price_delta_pct": 0.2}},
                              "monitor_exit": {"metrics": {"observed_trade_count": 4, "observed_day_count": 2, "by_hold_offset": [{"offset": "+15m", "average_improvement_pct": 9}, {"offset": "+5m", "average_improvement_pct": 0.3}]}},
                              "full_system": {"decision": "ADJUST", "metrics": {"performance": {"count": 5, "win_rate": 0.4, "expectancy_pct": -0.2, "profit_factor": 0.7, "maximum_drawdown_pct": -3}}}},
      "evidence": {"scanner_quality": {"topk_forward_performance": {"rows": [_tkrow(1, "+30m", 30, 3, 0.9, 0.0), {}]}, "source_performance": {"rows": [{"source": "s1", "horizon": "+5m", "count": 7, "observed_day_count": 2, "expectancy_pct": 0.2, "win_rate": 0.5}, {}]}},
                   "selection_availability": {"trade_model_count": 6, "raw_scanner_control_count": 1, "strategist_snapshot_count": 2, "commander_snapshot_count": 3, "scanner_vs_strategist_comparable_count": 4, "strategist_vs_commander_comparable_count": 5},
                   "decision_window_attribution": {"decision_window_count": 8, "candidate_row_count": 90}},
      "problem_segment": {"primary_root_cause": "insufficient_sample", "statuses": {"b": False, "a": True, "한": "글"}}, "overall_decision": {"decision": "ADJUST_AND_RETEST", "first_actionable_component": "scanner", "reason": "r 이유"}}
FPS = [{}, {"range": None}, FP, {**FP, "component_decisions": None, "evidence": None, "problem_segment": None, "overall_decision": None}, {**FP, "evidence": {"scanner_quality": None}},
       {**FP, "component_decisions": {"scanner": {"role_cost_adjusted_metrics": [{"win_rate": "bad"}]}}}, {**FP, "problem_segment": {"statuses": None}}, {"component_decisions": {"monitor_exit": {"metrics": {"by_hold_offset": [{"offset": "+5m"}]}}}}]


@pytest.mark.parametrize("payload", FPS)
def test_render_full_chain_component_review(orig_nodes, monkeypatch, guards, payload):
    out = check(orig_nodes, monkeypatch, "render_full_chain_component_review", payload)
    assert (isinstance(out, str) and out.endswith("\n") and "\r" not in out) or out[0] == "err"


def test_render_full_chain_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_full_chain_component_review", FP)
    assert out.startswith("# Q9 Full-Chain Component Review (2026-04-10 ~ 2026-04-14)\n\nEvaluation-only. No runtime or trading policy change is authorized.\n\n## Final Component Decisions\n")
    assert "| scanner | `RETAIN` | f1 |\n| strategist | `INSUFFICIENT_EVIDENCE` | mc |\n" in out and "| top_pick | +30m | 30/3 | 0.4% | 55.0% | 1.3 |\n" in out
    assert '- statuses: `{"a": true, "b": false, "한": "글"}`\n' in out and "- +5m average improvement: 0.3%\n" in out
    assert out.endswith("- historical review complete: **True**\n- open-ended extension authorized: **False**\n- behavior change authorized: **False**\n")
    assert "| full_system" in out and "- reason: r 이유\n" in out
    empty = check(orig_nodes, monkeypatch, "render_full_chain_component_review", {})
    assert "(None ~ None)" in empty and "| scanner | `None` |  |" in empty
    assert check(orig_nodes, monkeypatch, "render_full_chain_component_review", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "render_full_chain_component_review", {"evidence": {"scanner_quality": {"topk_forward_performance": {"rows": ["bad"]}}}})[0] == "err"

    class FakeJson:
        @staticmethod
        def dumps(obj, **kw):
            return "FAKE_JSON"
    assert "- statuses: `FAKE_JSON`\n" in check(orig_nodes, monkeypatch, "render_full_chain_component_review", FP, overrides={"json": FakeJson})


# ---- A53-7 classify_scanner_alignment_root_cause ----
def _row(raw="A", post="A", sel="A", exe="A", f2e=None, m2c=None, s2m=None):
    return {"raw_scanner_top1": raw, "post_strategy_top1": post, "selected_symbol": sel, "executed_symbol": exe, "final_to_executed_changed": f2e, "monitor_to_commander_changed": m2c, "selected_to_monitor_changed": s2m}


def _mdl(rank=None, top=None, sel=None):
    s = {}
    if rank is not None:
        s["selected_rank"] = rank
    if top is not None:
        s["scanner_top1"] = {"score_total": top}
    if sel is not None:
        s["selected_candidate"] = {"score_total": sel}
    return {"selection": s}


CLS = {"missing_raw": (_row(raw=""), _mdl(), 1.0), "missing_post": (_row(post=""), _mdl(), None), "missing_sel": (_row(sel=""), _mdl(2, 5, 4), 1.0), "missing_exe": (_row(exe=""), _mdl(), 1.0),
       "symbol_mapping_final": (_row(f2e=True), _mdl(), 1.0), "symbol_mapping_monitor": (_row(m2c=True), _mdl(), 1.0), "symbol_mapping_sel": (_row(s2m=True), _mdl(), 1.0), "mapping_not_true": (_row(f2e=False, m2c=None, s2m=0), _mdl(), 1.0),
       "candidate_filtering": (_row(sel="B"), _mdl(3, 5, 4), 1.0), "candidate_filtering_nogap": (_row(sel="B"), _mdl(2), 1.0), "sel_ne_post_rank1": (_row(sel="B"), _mdl(1), 1.0), "sel_ne_post_norank": (_row(sel="B"), _mdl(), 1.0),
       "strategist_override": (_row(raw="X", post="A", sel="A"), _mdl(1), 1.0), "rank_drift_raw_post": (_row(raw="X", post="A", sel="B", exe="B"), _mdl(1), 1.0), "rank_drift_rank": (_row(), _mdl(2), 1.0),
       "ranking_failure": (_row(), _mdl(1), -1.0), "aligned": (_row(), _mdl(1), 1.0), "aligned_zero": (_row(), _mdl(), 0.0), "aligned_none": (_row(), _mdl(), None), "bad_model": (_row(), {"selection": "bad"}, -1.0),
       "str_rank": (_row(sel="B"), _mdl("4", "7.5", "2.25"), None), "non_mapping_row_fields": ({"raw_scanner_top1": None}, _mdl(), None)}


@pytest.mark.parametrize("case", list(CLS))
def test_classify_scanner_alignment_root_cause(orig_nodes, monkeypatch, guards, case):
    row, model, ret = CLS[case]
    check(orig_nodes, monkeypatch, "classify_scanner_alignment_root_cause", row=row, model=model, net_return_pct=ret)


def test_classify_exact_and_seams(orig_nodes, monkeypatch, guards):
    exp = {"missing_raw": "Missing Evidence", "missing_sel": "Missing Evidence", "symbol_mapping_final": "Symbol Mapping", "symbol_mapping_sel": "Symbol Mapping", "mapping_not_true": "Aligned / No Alignment Issue",
           "candidate_filtering": "Candidate Filtering", "sel_ne_post_rank1": "Aligned / No Alignment Issue", "sel_ne_post_norank": "Aligned / No Alignment Issue", "strategist_override": "Strategist Override", "rank_drift_raw_post": "Rank Drift",
           "rank_drift_rank": "Rank Drift", "ranking_failure": "Scanner Ranking Failure", "aligned": "Aligned / No Alignment Issue", "aligned_zero": "Aligned / No Alignment Issue", "aligned_none": "Aligned / No Alignment Issue"}
    for case, cause in exp.items():
        row, model, ret = CLS[case]
        out = check(orig_nodes, monkeypatch, "classify_scanner_alignment_root_cause", row=row, model=model, net_return_pct=ret)
        assert out["root_cause"] == cause and list(out) == ["root_cause", "confidence", "reasons", "selected_rank", "score_gap"], case
    cf = check(orig_nodes, monkeypatch, "classify_scanner_alignment_root_cause", row=CLS["candidate_filtering"][0], model=CLS["candidate_filtering"][1], net_return_pct=1.0)
    assert cf["reasons"] == ["selected candidate is below post-strategy top1", "selected_rank=3", "score_gap=1.0"] and cf["confidence"] == "high" and cf["selected_rank"] == 3 and cf["score_gap"] == 1.0
    assert check(orig_nodes, monkeypatch, "classify_scanner_alignment_root_cause", row=CLS["rank_drift_raw_post"][0], model=CLS["rank_drift_raw_post"][1], net_return_pct=1.0)["reasons"] == ["top candidate changed or selected rank drifted", "raw_top1_differs_from_post_strategy_top1"]
    assert check(orig_nodes, monkeypatch, "classify_scanner_alignment_root_cause", row=None, model={}, net_return_pct=None)[0] == "err"
    assert all(p.kind.name == "KEYWORD_ONLY" for p in inspect.signature(SA.classify_scanner_alignment_root_cause).parameters.values())
    out = check(orig_nodes, monkeypatch, "classify_scanner_alignment_root_cause", row=CLS["aligned"][0], model=CLS["aligned"][1], net_return_pct=1.0, overrides={"_selected_rank": lambda m: 9, "_score_gap": lambda m: 0.25})
    assert out["root_cause"] == "Rank Drift" and out["selected_rank"] == 9 and out["score_gap"] == 0.25


# ---- A53-8 render_scanner_alignment_root_cause_report ----
SRP = {"day": "2026-04-10", "behavior_effect": "observation_only", "trade_count": 3, "largest_observed_root_cause": {"root_cause": "Rank Drift"}, "largest_behavior_root_cause": {"root_cause": "Candidate Filtering"},
       "largest_structural_root_cause": {"root_cause": "Symbol Mapping"}, "q15_behavior_patch_candidate": "patch 한글", "interpretation_rule": "rule 1",
       "cause_summary": [{"root_cause": "Rank Drift", "diagnostic_kind": "structural", "causal_eligible": True, "trade_count": 2, "return_observation_count": 2, "win_rate": 0.5, "avg_return_pct": -0.25, "profit_factor": 0.6, "max_drawdown_pct": -2, "negative_impact_pct": -1.5}, "bad", {}],
       "rows": [{"trade_id": "T1", "symbol": "005930", "raw_scanner_top1": "A", "post_strategy_top1": "B", "selected_symbol": "C", "selected_rank": 2, "net_return_pct": -0.5, "root_cause": "Rank Drift", "reasons": ["r1", "r2"]}, "bad", {"trade_id": "T2", "net_return_pct": 0, "reasons": []}, {}]}
SRPS = [{}, SRP, {**SRP, "largest_observed_root_cause": None, "largest_root_cause": {"root_cause": "Legacy"}}, {**SRP, "largest_observed_root_cause": {}, "largest_root_cause": None}, {**SRP, "cause_summary": None, "rows": None},
        {**SRP, "largest_behavior_root_cause": "bad", "largest_structural_root_cause": []}, {**SRP, "q15_behavior_patch_candidate": None, "interpretation_rule": None}, {"cause_summary": [{"win_rate": "bad"}]}, {"rows": [{"net_return_pct": "bad"}]}]


@pytest.mark.parametrize("payload", SRPS)
def test_render_scanner_alignment_root_cause_report(orig_nodes, monkeypatch, guards, payload):
    out = check(orig_nodes, monkeypatch, "render_scanner_alignment_root_cause_report", payload)
    assert (isinstance(out, str) and out.endswith("\n") and "\r" not in out) or out[0] == "err"


def test_render_scanner_alignment_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_scanner_alignment_root_cause_report", SRP)
    assert out.startswith("# Q14 Scanner Alignment Root Cause - 2026-04-10\n\n- Behavior effect: `observation_only`\n- Trades: 3\n- Largest observed root cause: `Rank Drift`\n- Largest behavior root cause: `Candidate Filtering`\n")
    assert "- Q15 candidate: patch 한글\n" in out and "| Rank Drift | structural | True | 2 | 2 | 50.0% | -0.2500% | 0.6 | -2.0000% | -1.5000% |\n" in out
    assert "| T1 | 005930 | A | B | C | 2 | -0.5000% | Rank Drift | r1, r2 |\n" in out and "| T2 | - | - | - | - | - | 0.0000% | None | - |\n" in out
    assert out.endswith("## Interpretation\n\n- rule 1\n")
    legacy = check(orig_nodes, monkeypatch, "render_scanner_alignment_root_cause_report", SRPS[2])
    assert "Largest observed root cause: `Legacy`" in legacy
    empty = check(orig_nodes, monkeypatch, "render_scanner_alignment_root_cause_report", {})
    assert "Scanner Alignment Root Cause - \n" in empty and "- Largest observed root cause: `-`" in empty and empty.endswith("- \n")
    assert check(orig_nodes, monkeypatch, "render_scanner_alignment_root_cause_report", None)[0] == "err" and check(orig_nodes, monkeypatch, "render_scanner_alignment_root_cause_report", SRPS[7])[0] == "err"
    out = check(orig_nodes, monkeypatch, "render_scanner_alignment_root_cause_report", SRP, overrides={"_mapping": lambda v: {"root_cause": "SEAM"}})
    assert out.count("`SEAM`") == 3
    assert "| T1 |" not in check(orig_nodes, monkeypatch, "render_scanner_alignment_root_cause_report", SRP, overrides={"Mapping": NeverMapping})


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
