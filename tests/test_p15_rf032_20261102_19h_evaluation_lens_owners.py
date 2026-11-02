"""RF-032 A43-1..8: eight ``evaluation_lens_report`` bodies, original vs thin wrappers + Owners.

Original = A preimage c845ba69 (SOURCE blob cade83e2 == canonical 0c4ac82a). Each original function is compiled from
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

A_PRE = "c845ba697cd5be3002a85e436f67e43592e851ed"
CANON = "0c4ac82a481bdb6844cc5f569de741a085cc49b9"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_rail": ("evaluation_lens_report", "cade83e2c18aecbde557acad9a0e26ca2fbe3938", "evaluation_lens_report_rail"),
    "_blocker": ("evaluation_lens_report", "cade83e2c18aecbde557acad9a0e26ca2fbe3938", "evaluation_lens_report_blocker"),
    "_forward_group": ("evaluation_lens_report", "cade83e2c18aecbde557acad9a0e26ca2fbe3938", "evaluation_lens_report_forward_group"),
    "_blocker_forward_review": ("evaluation_lens_report", "cade83e2c18aecbde557acad9a0e26ca2fbe3938", "evaluation_lens_report_blocker_forward_review"),
    "_best_role_by_horizon": ("evaluation_lens_report", "cade83e2c18aecbde557acad9a0e26ca2fbe3938", "evaluation_lens_report_best_role_by_horizon"),
    "_strategist_delta_review": ("evaluation_lens_report", "cade83e2c18aecbde557acad9a0e26ca2fbe3938", "evaluation_lens_report_strategist_delta_review"),
    "_exit_counterfactual_review": ("evaluation_lens_report", "cade83e2c18aecbde557acad9a0e26ca2fbe3938", "evaluation_lens_report_exit_counterfactual_review"),
    "render_evaluation_lens_report": ("evaluation_lens_report", "cade83e2c18aecbde557acad9a0e26ca2fbe3938", "evaluation_lens_report_render_evaluation_lens_report"),
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
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"_Str({self.text!r})"

    def __str__(self):
        return self.text


MOD = MODS["evaluation_lens_report"]


def _cp(ret=None, mfe=None, mae=None, status="observed"):
    return {"status": status, "return_pct": ret, "mfe_pct": mfe, "mae_pct": mae}


def _cand(group=None, cps=None, day="2026-04-10", **extra):
    row = {"generated_at": f"{day}T00:00:00+00:00", "shadow_forward_outcome": {"checkpoints": cps or {}}}
    row.update(extra)
    if group is not None:
        row["grp"] = group
    return row


# ---- A43-1 _rail ----
RAILS = [{}, None if False else {"entry_lane_observation": None}, {"entry_lane_observation": {"market_regime_rail": "up"}}, {"entry_lane_observation": {"market_regime_rail": "  up  "}},
         {"entry_lane_observation": {"market_regime_rail": "", "market_regime_rail_shadow": {"market_regime_rail": "down"}}},
         {"entry_lane_observation": {"market_regime_rail_shadow": {"market_regime_rail": " "}}}, {"entry_lane_observation": {"market_regime_rail_shadow": "bad"}},
         {"entry_lane_observation": {"market_regime_rail": 0, "market_regime_rail_shadow": {"market_regime_rail": "flat"}}}, {"entry_lane_observation": {"market_regime_rail": _Str(" 한글 ")}},
         {"entry_lane_observation": "x"}, {"entry_lane_observation": {"market_regime_rail": "dir", "market_regime_rail_shadow": {"market_regime_rail": "ignored"}}}]


@pytest.mark.parametrize("row", RAILS)
def test_rail(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_rail", row)


def test_rail_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_rail", RAILS[2]) == "up" and check(orig_nodes, monkeypatch, "_rail", {}) == "unknown"
    assert check(orig_nodes, monkeypatch, "_rail", RAILS[4]) == "down" and check(orig_nodes, monkeypatch, "_rail", RAILS[10]) == "dir"
    assert check(orig_nodes, monkeypatch, "_rail", None)[0] == "err"
    seen = []
    out = check(orig_nodes, monkeypatch, "_rail", RAILS[2], overrides={"_as_dict": lambda v: seen.append(v) or {"market_regime_rail": "X"},
                                                                   "_text": lambda v: f"T({v})"})
    assert out == "T(X)" and len(seen) == 2  # one _as_dict call per side


# ---- A43-2 _blocker ----
BLK = [{}, {"guard_reason": "g"}, {"reason": "r"}, {"primary_failure_axis": "p"}, {"guard_reason": " ", "reason": "r", "primary_failure_axis": "p"}, {"guard_reason": 0, "reason": None, "primary_failure_axis": "p"},
       {"entry_quant_decision": {"blockers": ["b1", "b2"]}}, {"entry_quant_decision": {"blockers": []}}, {"entry_quant_decision": {"blockers": "notalist"}}, {"entry_quant_decision": {"blockers": [" "]}},
       {"entry_quant_decision": {"blockers": [None]}}, {"entry_quant_decision": {"blockers": ("t",)}}, {"entry_quant_decision": "x"}, {"guard_reason": _Str(" 한글 ")}, {"reason": "r", "entry_quant_decision": {"blockers": ["b"]}}]


@pytest.mark.parametrize("row", BLK)
def test_blocker(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_blocker", row)


def test_blocker_precedence_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_blocker", BLK[4]) == "r" and check(orig_nodes, monkeypatch, "_blocker", BLK[6]) == "b1"
    assert check(orig_nodes, monkeypatch, "_blocker", BLK[9]) == "" and check(orig_nodes, monkeypatch, "_blocker", {}) == "unknown"  # blank first blocker is returned as-is
    assert check(orig_nodes, monkeypatch, "_blocker", None)[0] == "err"
    out = check(orig_nodes, monkeypatch, "_blocker", {"reason": "x"}, overrides={"_text": lambda v: "T" if v == "x" else ""})
    assert out == "T"


# ---- A43-3 _forward_group ----
def _fg_rows():
    return [_cand("A", {"+5m": _cp(1.0, 2.0, -0.5), "+15m": _cp(-1.0, 0.1, -1.5), "EOD": _cp(0.5, 3.0, -0.1)}, day="2026-04-10"),
            _cand("A", {"+5m": _cp(2.0, 0.3, -0.2), "+30m": _cp(None, 1.0, None)}, day="2026-04-11"),
            _cand("B", {"+5m": _cp(0.5, 0.2, 0.0, status="pending")}, day="2026-04-10"),
            _cand("B", {}, day=""), _cand(None, {"+5m": _cp(3.0, 1.0, -1.0)}), _cand("", {"+30m": _cp(1.0, 5.0, -2.0)}), {"grp": 0}]


@pytest.mark.parametrize("cost", [0.0, 0.3, 1.0, 2.5, -1.0])
def test_forward_group_costs(orig_nodes, monkeypatch, guards, cost):
    check(orig_nodes, monkeypatch, "_forward_group", _fg_rows(), "grp", cost_floor_pct=cost)


@pytest.mark.parametrize("rows", [[], [{}], [_cand("Z")], [_cand("B", {"+5m": _cp(1, 1, 1)}), _cand("A", {"+5m": _cp(1, 1, 1)})]])
def test_forward_group_shapes(orig_nodes, monkeypatch, guards, rows):
    check(orig_nodes, monkeypatch, "_forward_group", rows, "grp", cost_floor_pct=0.3)


def test_forward_group_exact_order_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_forward_group", _fg_rows(), "grp", cost_floor_pct=0.3)
    assert [r["name"] for r in out][0] == "A" and list(out[0])[:4] == ["name", "candidate_count", "observed_days", "+5m"]
    assert out[0]["observed_days"] == ["2026-04-10", "2026-04-11"] or out[0]["observed_days"]
    five = out[0]["+5m"]
    assert five["observed_count"] == 2 and five["cost_floor_reachable_count"] == 2 and five["cost_floor_reachable_rate"] == 1.0 and five["avg_mfe_pct"] == 1.15
    ties = check(orig_nodes, monkeypatch, "_forward_group", [_cand("B", {"+5m": _cp(1, 1, 1)}), _cand("A", {"+5m": _cp(1, 1, 1)})], "grp", cost_floor_pct=0.3)
    assert [r["name"] for r in ties] == ["A", "B"]
    assert check(orig_nodes, monkeypatch, "_forward_group", None, "grp", cost_floor_pct=0.3)[0] == "err"
    assert [p.kind.name for p in inspect.signature(MOD._forward_group).parameters.values()] == ["POSITIONAL_OR_KEYWORD", "POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY"]
    out = check(orig_nodes, monkeypatch, "_forward_group", [{"k": 1}, {"k": 2}], "k", cost_floor_pct=0.0,
                overrides={"HORIZONS": ("+9m",), "_checkpoint_return": lambda r, h: float(r["k"]), "_checkpoint_mfe": lambda r, h: None, "_checkpoint_mae": lambda r, h: None,
                           "candidate_day": lambda r: "D", "performance_metrics": lambda vals: {"n": len(vals)}})
    assert [(r["name"], r["+9m"]["return"]) for r in out] == [("1", {"n": 1}), ("2", {"n": 1})]


# ---- A43-4 _blocker_forward_review ----
BFR_ROWS = [{"guard_reason": "pullback_not_mature", "shadow_forward_outcome": {"checkpoints": {"+5m": _cp(1.0, 1.0, -1.0)}}, "entry_lane_observation": {"market_regime_rail": "up"}},
            {"reason": "x_breakout_not_ready_y", "shadow_forward_outcome": {"checkpoints": {"+5m": _cp(2.0, 0.1, -0.1)}}},
            {"reason": "unrelated", "shadow_forward_outcome": {"checkpoints": {}}, "entry_lane_observation": {"market_regime_rail": "up"}},
            {"entry_quant_decision": {"blockers": ["quant_entry_block:vwap_pullback_promoted_quality_gate"]}}, {}]


@pytest.mark.parametrize("rows", [[], BFR_ROWS, BFR_ROWS[2:], [BFR_ROWS[0]], [{}]])
@pytest.mark.parametrize("cost", [0.0, 0.123456, 3.0])
def test_blocker_forward_review(orig_nodes, monkeypatch, guards, rows, cost):
    check(orig_nodes, monkeypatch, "_blocker_forward_review", rows, cost_floor_pct=cost)


def test_blocker_forward_review_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_blocker_forward_review", BFR_ROWS, cost_floor_pct=0.123456)
    assert list(out) == ["schema_version", "behavior_effect", "cost_floor_pct", "candidate_count", "focused_candidate_count", "by_blocker", "by_market_rail"]
    assert out["cost_floor_pct"] == 0.1235 and out["candidate_count"] == 5 and out["focused_candidate_count"] == 3
    src = [{"guard_reason": "pullback_not_mature"}]
    check(orig_nodes, monkeypatch, "_blocker_forward_review", src, cost_floor_pct=0.0)
    assert "blocker" not in src[0]  # input rows are copied, never mutated
    assert check(orig_nodes, monkeypatch, "_blocker_forward_review", None, cost_floor_pct=0.0)[0] == "err"
    calls = []
    out = check(orig_nodes, monkeypatch, "_blocker_forward_review", [{"a": 1}, {"a": 2}], cost_floor_pct=1.0,
                overrides={"BLOCKERS_OF_INTEREST": ("zz",), "_blocker": lambda r: "zz" if r["a"] == 1 else "no", "_rail": lambda r: "R",
                           "_forward_group": lambda rows, key, *, cost_floor_pct: calls.append((key, [dict(r) for r in rows])) or [key, len(rows)]})
    assert out["by_blocker"] == ["blocker", 1] and out["by_market_rail"] == ["market_rail", 2]
    assert calls[0] == ("blocker", [{"a": 1, "blocker": "zz", "market_rail": "R"}]) and len(calls) == 4


# ---- A43-5 _best_role_by_horizon ----
ROLES = ["P_SCANNER_PRE_STRATEGIST_UNIVERSE", "A_SCANNER_CONTROL", "B_STRATEGIST_RANKED", "C_COMMANDER_FINAL"]


def _rr(role, ret, h="+5m"):
    return {"q9_decision_role": role, "shadow_forward_outcome": {"checkpoints": {h: _cp(ret)}}}


BR_ROWS = [[], [{}], [_rr("OTHER", 1.0)], [_rr(ROLES[0], 1.0), _rr(ROLES[0], 3.0), _rr(ROLES[1], 5.0), _rr(ROLES[2], -1.0), _rr(ROLES[3], 2.0)],
           [_rr(ROLES[1], 1.0), _rr(ROLES[2], 1.0)], [_rr(ROLES[3], None), _rr(ROLES[2], 0.5, "+15m")], [_rr(" " + ROLES[1] + " ", 4.0)], [_rr(ROLES[0], -1.0), _rr(ROLES[1], -2.0)]]


@pytest.mark.parametrize("rows", BR_ROWS)
@pytest.mark.parametrize("horizon", ["+5m", "+15m", "EOD"])
def test_best_role_by_horizon(orig_nodes, monkeypatch, guards, rows, horizon):
    check(orig_nodes, monkeypatch, "_best_role_by_horizon", rows, horizon)


def test_best_role_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_best_role_by_horizon", BR_ROWS[3], "+5m")
    assert out["best_role"] == ROLES[1] and [r["role"] for r in out["roles"]] == [ROLES[1], ROLES[0], ROLES[3], ROLES[2]] and list(out) == ["horizon", "roles", "best_role"]
    tie = check(orig_nodes, monkeypatch, "_best_role_by_horizon", BR_ROWS[4], "+5m")
    assert [r["role"] for r in tie["roles"]] == [ROLES[1], ROLES[2]]  # stable sort keeps insertion order for equal expectancy
    assert check(orig_nodes, monkeypatch, "_best_role_by_horizon", [], "+5m") == {"horizon": "+5m", "roles": [], "best_role": ""}
    assert check(orig_nodes, monkeypatch, "_best_role_by_horizon", None, "+5m")[0] == "err"
    out = check(orig_nodes, monkeypatch, "_best_role_by_horizon", [{"q9_decision_role": ROLES[0], "v": 1.0}, {"q9_decision_role": ROLES[1], "v": 9.0}], "+5m",
                overrides={"_checkpoint_return": lambda r, h: r["v"], "performance_metrics": lambda vals: {"expectancy_pct": vals[0]}})
    assert out["best_role"] == ROLES[1]


# ---- A43-6 _strategist_delta_review ----
def _q9(did, role, ret_by_h, rank=None, selected=False):
    row = {"q9_decision_id": did, "q9_decision_role": role, "q9_selected": selected, "shadow_forward_outcome": {"checkpoints": {h: _cp(v) for h, v in ret_by_h.items()}}}
    if rank is not None:
        row["rank"] = rank
    return row


Q9 = [_q9("D1", ROLES[1], {"+5m": 1.0, "+15m": 0.0}, rank=2), _q9("D1", ROLES[1], {"+5m": 9.0}, rank=5), _q9("D1", ROLES[2], {"+5m": 3.0, "+15m": 1.0}, rank=1),
      _q9("D1", ROLES[2], {"+5m": 7.0}, rank=2, selected=True), _q9("D1", ROLES[3], {"+5m": 2.0, "+15m": 2.0}, rank=3),
      _q9("D2", ROLES[1], {"+5m": 0.5}), _q9("D2", ROLES[2], {"+5m": 1.5}, rank=4), _q9("D2", ROLES[3], {"+5m": -1.5, "EOD": 1.0}, rank="2"),
      _q9("D3", ROLES[2], {"+5m": 4.0}), _q9("", ROLES[1], {"+5m": 1.0}), _q9("D4", "", {"+5m": 1.0}), {"q9_decision_id": "D5", "q9_decision_role": ROLES[1]}]


@pytest.mark.parametrize("rows", [[], Q9, Q9[:5], Q9[5:8], Q9[8:], [Q9[0]], [{}]])
def test_strategist_delta_review(orig_nodes, monkeypatch, guards, rows):
    check(orig_nodes, monkeypatch, "_strategist_delta_review", rows)


def test_strategist_delta_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_strategist_delta_review", Q9)
    assert list(out) == ["schema_version", "behavior_effect", "decision_window_count", "best_role_by_horizon", "deltas_by_horizon"] and out["decision_window_count"] == 4
    d5 = out["deltas_by_horizon"][0]
    assert d5["horizon"] == "+5m" and d5["strategist_minus_scanner_control"]["count"] >= 1
    bad = [_q9("D", ROLES[1], {"+5m": 1.0}, rank="x")]
    assert check(orig_nodes, monkeypatch, "_strategist_delta_review", bad)[0:2] == ("err", "ValueError")  # int(float("x")) not caught
    assert check(orig_nodes, monkeypatch, "_strategist_delta_review", None)[0] == "err"
    seen = []
    out = check(orig_nodes, monkeypatch, "_strategist_delta_review", Q9[:5],
                overrides={"HORIZONS": ("+5m",), "performance_metrics": lambda vals: seen.append(list(vals)) or {"n": len(vals)}, "_best_role_by_horizon": lambda rows, h: {"horizon": h, "best_role": "R"}})
    assert out["best_role_by_horizon"] == [{"horizon": "+5m", "best_role": "R"}] and out["deltas_by_horizon"][0]["strategist_minus_scanner_control"] == {"n": 1}
    assert seen[0] == [6.0] and len(seen) == 4  # selected B (7.0) minus min-rank A (1.0); 2 per side


# ---- A43-7 _exit_counterfactual_review ----
def _em(tid, reason=None, outcome=None, cps=None, monitor=None, post=None):
    m = {"trade_id": tid, "symbol": "S" + tid}
    if reason is not None:
        m["exit"] = {"reason": reason}
    if outcome is not None:
        m["outcome"] = outcome
    if post is not None:
        m["post_exit_shadow"] = {"checkpoints": post}
    if monitor is not None:
        m["monitor"] = monitor
    return m


EM = [_em("1", "stop", {"net_return_pct": -1.0}, post={"+5m": {"return_pct": 0.5}, "+15m": {"return_pct": 1.0}, "EOD": {"return_pct": -3.0}}),
      _em("2", "stop", {"net_return_pct": -0.5}, post={"+5m": {"return_pct": -0.5}, "+60m": {"return_pct": 2.0}}),
      _em("3", None, {"exit_reason": "timeout", "return_pct": 0.2}, monitor={"post_exit": {"checkpoints": {"+30m": {"return_pct": 1.2}}}}),
      _em("4", "", {"return_pct": 0}, post={"+5m": {"return_pct": 1.0}}), _em("5", "take", {"net_return_pct": 0.0, "return_pct": 9.0}, post={"+5m": {"return_pct": "bad"}}),
      _em("6", "take", {}, post={"+5m": {"return_pct": 1.0}}), {}, {"exit": "bad", "outcome": "bad", "monitor": "bad"}]


@pytest.mark.parametrize("models", [[], EM, EM[:2], EM[2:3], EM[3:6], EM[6:], [EM[0]]])
def test_exit_counterfactual_review(orig_nodes, monkeypatch, guards, models):
    check(orig_nodes, monkeypatch, "_exit_counterfactual_review", models)


def test_exit_counterfactual_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_exit_counterfactual_review", EM)
    assert list(out) == ["schema_version", "behavior_effect", "trade_count", "by_exit_reason"] and out["trade_count"] == len(EM)
    groups = out["by_exit_reason"]
    assert groups[0]["exit_reason"] == "unknown" and groups[0]["trade_count"] == 3  # most trades first; blank/missing reasons -> unknown
    stop = [g for g in groups if g["exit_reason"] == "stop"][0]
    assert stop["trade_count"] == 2 and list(stop) == ["exit_reason", "trade_count", "+5m", "+15m", "+30m", "+60m", "EOD"]
    assert stop["+5m"]["count"] == 2 and stop["+5m"]["average_return_pct"] == 0.75 and [g["trade_count"] for g in groups] == sorted((g["trade_count"] for g in groups), reverse=True)
    assert check(orig_nodes, monkeypatch, "_exit_counterfactual_review", [])["by_exit_reason"] == []
    assert check(orig_nodes, monkeypatch, "_exit_counterfactual_review", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "_exit_counterfactual_review", [None])[0] == "err"
    made = []
    import collections

    def spy_defaultdict(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "_exit_counterfactual_review", EM[:2], overrides={"defaultdict": spy_defaultdict})
    assert made == [1, 1]
    out = check(orig_nodes, monkeypatch, "_exit_counterfactual_review", EM[:2], overrides={"performance_metrics": lambda vals: {"n": len(vals)}, "_text": lambda v: "T" if v else ""})
    assert out["by_exit_reason"][0]["exit_reason"] == "T" and out["by_exit_reason"][0]["+5m"] == {"n": 2}


# ---- A43-8 render_evaluation_lens_report ----
HROW = {"name": "pullback_not_mature", "candidate_count": 7, "+5m": {"return": {"count": 3, "average_return_pct": 0.12}}, "+15m": {"return": {"count": 0, "average_return_pct": 9}},
        "+30m": {"return": {"count": 2, "average_return_pct": -0.5}, "avg_mfe_pct": 1.25, "cost_floor_reachable_rate": 0.5}}
FULLP = {"range": {"start": "2026-04-10", "end": "2026-04-14"}, "evidence": {"shadow_payload_count": 3, "candidate_count": 40, "q9_candidate_count": 12, "trade_model_count": 4},
         "blocker_forward_review": {"by_blocker": [HROW, {}, {"name": "한글 사유"}]},
         "strategist_delta_review": {"best_role_by_horizon": [{"horizon": "+5m", "best_role": "B_STRATEGIST_RANKED"}, {"horizon": "EOD"}],
                                     "deltas_by_horizon": [{"horizon": "+5m", "strategist_minus_scanner_control": {"count": 2, "average_return_pct": 0.3}, "commander_minus_strategist": {"count": 0}},
                                                           {"horizon": "EOD"}]},
         "exit_hold_counterfactual_review": {"by_exit_reason": [{"exit_reason": "stop", "trade_count": 2, "+5m": {"count": 2, "average_return_pct": 0.75}, "EOD": {"count": 1, "average_return_pct": -3.0}}, {}]}}
RPAYS = [{}, {"range": None}, FULLP, {**FULLP, "blocker_forward_review": None, "strategist_delta_review": None, "exit_hold_counterfactual_review": None},
         {**FULLP, "blocker_forward_review": {"by_blocker": None}}, {"evidence": "bad"}]


@pytest.mark.parametrize("payload", RPAYS)
def test_render_evaluation_lens_report(orig_nodes, monkeypatch, guards, payload):
    out = check(orig_nodes, monkeypatch, "render_evaluation_lens_report", payload)
    assert out.endswith("\n") and "\r" not in out


def test_render_exact_bytes_errors_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_evaluation_lens_report", FULLP)
    assert out.startswith("# Evaluation Lens Report (2026-04-10 ~ 2026-04-14)\n\nBehavior effect: evaluation_only. This report does not change trading behavior or reset the freeze window.\n\n## Evidence\n- shadow payloads: 3\n")
    assert "| pullback_not_mature | 7 | 0.12 | - | -0.5 | 1.25 | 0.5 |\n" in out and "| 한글 사유 | None | - | - | - | None | None |\n" in out
    assert "| +5m | B_STRATEGIST_RANKED | 0.3 | - |\n" in out and "| EOD |  | - | - |\n" in out
    assert "| stop | 2 | 0.75 | - | - | -3.0 |\n" in out
    assert out.endswith("- Promotion decisions still require the promotion framework and enough comparable days.\n")
    empty = check(orig_nodes, monkeypatch, "render_evaluation_lens_report", {})
    assert "(None ~ None)" in empty and "- shadow payloads: None\n" in empty
    assert check(orig_nodes, monkeypatch, "render_evaluation_lens_report", None)[0] == "err"
    out = check(orig_nodes, monkeypatch, "render_evaluation_lens_report", FULLP, overrides={"_metric_avg": lambda metric: "M"})
    assert "| pullback_not_mature | 7 | M | M | M | 1.25 | 0.5 |" in out


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
