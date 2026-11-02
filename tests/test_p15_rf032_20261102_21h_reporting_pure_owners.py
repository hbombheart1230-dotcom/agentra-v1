"""RF-032 A45-1..8: eight ``loss_decomposition`` / ``evaluation_lens_report`` / ``cost_basis_comparison`` bodies, original vs thin wrappers + Owners.

Original = A preimage aa2f2ab1 (SOURCE blobs bbe3777b / c58aac7e / d6ceae36 == canonical 6915f64d). Each original function is compiled from
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

A_PRE = "aa2f2ab1ff9efc12e577e11182e9cf480d151c01"
CANON = "6915f64dd56b6e8fa2771fd4fa4252b79b8feb2b"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_entry_timing_summary": ("loss_decomposition", "bbe3777bbf339812766aed8816818939ce788242", "loss_decomposition_entry_timing_summary"),
    "_exit_hold_summary": ("loss_decomposition", "bbe3777bbf339812766aed8816818939ce788242", "loss_decomposition_exit_hold_summary"),
    "_diagnosis": ("loss_decomposition", "bbe3777bbf339812766aed8816818939ce788242", "loss_decomposition_diagnosis"),
    "_next_action": ("loss_decomposition", "bbe3777bbf339812766aed8816818939ce788242", "loss_decomposition_next_action"),
    "render_loss_decomposition": ("loss_decomposition", "bbe3777bbf339812766aed8816818939ce788242", "loss_decomposition_render_loss_decomposition"),
    "_candidate_rows": ("evaluation_lens_report", "c58aac7eac505f4e0a847261fd4e0ab02995c9ae", "evaluation_lens_report_candidate_rows"),
    "_q9_candidate_rows": ("evaluation_lens_report", "c58aac7eac505f4e0a847261fd4e0ab02995c9ae", "evaluation_lens_report_q9_candidate_rows"),
    "_topk_rows": ("cost_basis_comparison", "d6ceae367fead768c76155bb775987e92e2bbdde", "cost_basis_comparison_topk_rows"),
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


import datetime as _dt

LD = MODS["loss_decomposition"]
EL = MODS["evaluation_lens_report"]
CB = MODS["cost_basis_comparison"]


class _Str:
    def __init__(self, text):
        self.text = text

    def __repr__(self):
        return f"_Str({self.text!r})"

    def __str__(self):
        return self.text


def _ep(ts):
    return int(_dt.datetime.fromisoformat(ts).timestamp())


TS0 = "2026-04-10T01:00:00+00:00"
E0 = _ep(TS0)


def _c(sym, epoch, price, reason="r"):
    return {"symbol": sym, "reason": reason, "shadow_forward_base": {"baseline_epoch": epoch, "baseline_price": price}}


def _mod(tid, sym, ts, price, day="2026-04-10T00:00:00"):
    return {"trade_id": tid, "symbol": sym, "day": day, "entry": {"timestamp": ts, "price": price}}


# ---- A45-1 _entry_timing_summary ----
CANDS = [_c("A", E0 - 600, 100.0, "early"), _c("A", E0 - 60, 100.0, "late"), _c("B", E0 - 900, 50.0, "edge"), _c("B", E0 - 901, 50.0, "too_old"), _c("C", E0 + 60, 10.0, "future"),
         _c("D", 0, 10.0), _c("D", E0 - 10, 0.0), _c("D", E0 - 10, None), _c("", E0 - 10, 5.0, "nosym"), {"symbol": "A"}, {"symbol": "A", "shadow_forward_base": "bad"}, _c("E", E0 - 5, 20.0, "e")]
MODELS = [_mod("T1", "A", TS0, 101.0), _mod("T2", "B", TS0, 49.0, day="2026-04-11"), _mod("T3", "C", TS0, 10.0), _mod("T4", "A", "bad", 1.0), _mod("T5", "A", TS0, None), _mod("T6", "A", TS0, 0),
          _mod("T7", "Z", TS0, 5.0), _mod("T8", "E", TS0, 22.0, day=""), _mod("T9", "", TS0, 5.0), _mod("T10", "A", "2026-04-10T01:00:00Z", 100.5), {"symbol": "A"}, {"symbol": "A", "entry": None}]


@pytest.mark.parametrize("models,cands", [([], []), (MODELS, CANDS), (MODELS[:1], CANDS), (MODELS[1:2], CANDS), (MODELS[2:3], CANDS), (MODELS[3:], CANDS), (MODELS, []), ([], CANDS)])
def test_entry_timing_summary(orig_nodes, monkeypatch, guards, models, cands):
    check(orig_nodes, monkeypatch, "_entry_timing_summary", models, cands)


def test_entry_timing_summary_exact_and_boundary(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_entry_timing_summary", MODELS, CANDS)
    assert list(out) == ["matched_trade_count", "matched_day_count", "average_entry_price_delta_pct", "median_entry_price_delta_pct", "late_entry_count", "better_entry_count", "examples", "limitation"]
    assert out["matched_trade_count"] >= 3 and out["limitation"].startswith("matched to nearest same-symbol shadow baseline within 15 minutes")
    ex = {e["trade_id"]: e for e in out["examples"]}
    assert ex["T1"]["candidate_reason"] == "late" and ex["T1"]["entry_price_delta_pct"] == 1.0  # nearest (latest) eligible baseline
    assert ex["T2"]["candidate_reason"] == "edge"  # exactly 15 minutes is eligible, 901s is not
    assert "T3" not in ex and "T7" not in ex and "T4" not in ex
    assert check(orig_nodes, monkeypatch, "_entry_timing_summary", [], [])["average_entry_price_delta_pct"] is None
    assert check(orig_nodes, monkeypatch, "_entry_timing_summary", None, [])[0] == "err"
    assert check(orig_nodes, monkeypatch, "_entry_timing_summary", [], None)[0] == "err"


def test_entry_timing_summary_seams(orig_nodes, monkeypatch, guards):
    calls = []
    out = check(orig_nodes, monkeypatch, "_entry_timing_summary", MODELS[:2], CANDS,
                overrides={"_parse_ts": lambda v: calls.append(v) or _dt.datetime.fromisoformat(TS0)})
    assert len(calls) == 4 and out["matched_trade_count"] >= 1
    out = check(orig_nodes, monkeypatch, "_entry_timing_summary", MODELS[:1], CANDS, overrides={"median": lambda vals: 123.456789})
    assert out["median_entry_price_delta_pct"] == 123.4568

    class NeverMapping:
        pass
    out = check(orig_nodes, monkeypatch, "_entry_timing_summary", MODELS[:1], CANDS, overrides={"Mapping": NeverMapping})
    assert out["matched_trade_count"] == 0


# ---- A45-2 _exit_hold_summary ----
def _xm(tid, realized=None, cps=None, day="2026-04-10T00:00:00", monitor=True):
    m = {"trade_id": tid, "symbol": "S" + tid, "day": day, "outcome": {"net_return_pct": realized}}
    if monitor:
        m["monitor"] = {"post_exit": {"checkpoints": cps or {}}}
    return m


def _xcp(v, status="observed"):
    return {"status": status, "return_pct": v}


XM = [_xm("1", -1.0, {"+5m": _xcp(0.01), "+15m": _xcp(-0.02), "+30m": _xcp("0.005"), "+60m": _xcp(0)}), _xm("2", 0.5, {"+5m": _xcp(0.03), "+15m": _xcp(0.0, "pending")}, day="2026-04-11T00:00:00"),
      _xm("3", None, {"+5m": _xcp("bad"), "+15m": _xcp(None), "+99m": _xcp(1)}), _xm("4", 1, {}), _xm("5", 1, monitor=False), {"outcome": None, "monitor": None}, {"monitor": {"post_exit": "bad"}},
      _xm("6", 2.0, {"+5m": _xcp(0.0002)}, day="")]


@pytest.mark.parametrize("models", [[], XM, XM[:1], XM[1:3], XM[3:], [XM[0]] * 25])
def test_exit_hold_summary(orig_nodes, monkeypatch, guards, models):
    check(orig_nodes, monkeypatch, "_exit_hold_summary", models)


def test_exit_hold_summary_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_exit_hold_summary", XM)
    assert list(out) == ["observed_trade_count", "observed_day_count", "by_hold_offset", "examples", "limitation"]
    off = {r["offset"]: r for r in out["by_hold_offset"]}
    assert [r["offset"] for r in out["by_hold_offset"]] == ["+5m", "+15m", "+30m", "+60m"]  # insertion order of first observation
    assert off["+5m"]["count"] == 3 and off["+5m"]["improved_count"] == 3 and off["+15m"]["worsened_count"] == 1 and off["+60m"]["improved_count"] == 0 and off["+60m"]["worsened_count"] == 0
    assert out["examples"][0]["hold_improvement_pct"] == {"+5m": 1.0, "+15m": -2.0, "+30m": 0.5, "+60m": 0.0}
    assert len(check(orig_nodes, monkeypatch, "_exit_hold_summary", [XM[0]] * 25)["examples"]) == 20
    assert check(orig_nodes, monkeypatch, "_exit_hold_summary", None)[0] == "err" and check(orig_nodes, monkeypatch, "_exit_hold_summary", [None])[0] == "err"
    out = check(orig_nodes, monkeypatch, "_exit_hold_summary", XM[:2], overrides={"_to_float": lambda v: 0.5 if v is not None else None})
    assert out["by_hold_offset"][0]["average_improvement_pct"] == 50.0

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_exit_hold_summary", XM[:2], overrides={"Mapping": NeverMapping})["observed_trade_count"] == 0
    made = []
    import collections

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "_exit_hold_summary", XM[:1], overrides={"defaultdict": spy})
    assert made == [1, 1]


# ---- A45-3 _diagnosis ----
SHADOW = {"entry_lane_forward_outcomes": {"by_time_bucket": [{"name": "open_20_60m", "avg_return_30m_pct": 0.5, "avg_return_60m_pct": 0.9}, {"name": "mid_session", "avg_return_30m_pct": -0.2, "avg_return_60m_pct": -0.4}, "bad"]}}
DKW = dict(shadow=SHADOW, candidate_rank=[], realized={"performance": {"count": 5, "expectancy_pct": -0.7, "profit_factor": 0.4}}, entry={"matched_trade_count": 3, "average_entry_price_delta_pct": 0.12},
           exit_hold={"observed_trade_count": 4})


@pytest.mark.parametrize("override", [{}, dict(shadow={}), dict(shadow={"entry_lane_forward_outcomes": None}), dict(shadow={"entry_lane_forward_outcomes": {"by_time_bucket": None}}),
                                       dict(realized={}), dict(realized={"performance": {}}), dict(entry={}), dict(exit_hold={}), dict(candidate_rank=[{"x": 1}]),
                                       dict(shadow={"entry_lane_forward_outcomes": {"by_time_bucket": [{"name": "mid_session"}]}})])
def test_diagnosis(orig_nodes, monkeypatch, guards, override):
    check(orig_nodes, monkeypatch, "_diagnosis", **{**DKW, **override})


def test_diagnosis_exact_errors_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_diagnosis", **DKW)
    assert [f["stage"] for f in out] == ["raw_candidate_edge", "scanner_ranking", "strategist_commander", "monitor_entry", "monitor_exit", "realized_system"]
    assert out[0]["finding"].startswith("Candidate edge is horizon- and time-bucket dependent, not universally absent. open_20_60m +30m=0.5%, +60m=0.9%; mid_session +30m=-0.2%, +60m=-0.4%.")
    assert out[3]["finding"] == "3 trades matched a nearby shadow baseline; average entry price delta=0.12%."
    assert out[5]["finding"] == "Realized count=5, expectancy=-0.7%, profit_factor=0.4."
    assert check(orig_nodes, monkeypatch, "_diagnosis", **{**DKW, "realized": {"performance": None}})[0] == "err"  # .get on None
    assert check(orig_nodes, monkeypatch, "_diagnosis", **{**DKW, "shadow": None})[0] == "err"

    class NeverMapping:
        pass
    out = check(orig_nodes, monkeypatch, "_diagnosis", **DKW, overrides={"Mapping": NeverMapping})
    assert "open_20_60m +30m=None%" in out[0]["finding"]
    assert all(p.kind.name == "KEYWORD_ONLY" for p in inspect.signature(LD._diagnosis).parameters.values())


# ---- A45-4 _next_action ----
NKW = dict(role_rows=[{"name": "top_pick", "avg_return_15m_pct": 0.1, "avg_return_30m_pct": 0.2, "avg_return_60m_pct": 0.3}],
           realized={"performance": {"expectancy_pct": "-1.5"}}, exit_hold={"by_hold_offset": [{"offset": "+15m", "average_improvement_pct": 9}, {"offset": "+5m", "average_improvement_pct": 0.4}]})


@pytest.mark.parametrize("override", [{}, dict(role_rows=[]), dict(role_rows=[{"name": "other"}]), dict(realized={}), dict(realized={"performance": {"expectancy_pct": "bad"}}),
                                       dict(exit_hold={}), dict(exit_hold={"by_hold_offset": []}), dict(exit_hold={"by_hold_offset": [{"offset": "+15m"}]}), dict(role_rows=[{"name": None}, {"name": "top_pick"}])])
def test_next_action(orig_nodes, monkeypatch, guards, override):
    check(orig_nodes, monkeypatch, "_next_action", **{**NKW, **override})


def test_next_action_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_next_action", **NKW)
    assert list(out) == ["priority", "component", "decision", "reason", "evidence", "required_follow_up", "behavior_change_authorized"]
    assert out["behavior_change_authorized"] is False and out["priority"] == 1 and out["decision"] == "FIX_BEFORE_ENTRY_OR_EXIT_TUNING"
    assert out["evidence"] == {"top_pick_15m_pct": 0.1, "top_pick_30m_pct": 0.2, "top_pick_60m_pct": 0.3, "realized_expectancy_pct": -1.5, "post_exit_5m_average_improvement_pct": 0.4}
    assert out["required_follow_up"][-1] == "do not attribute the problem to Strategist until a trusted raw Scanner control exists"
    assert check(orig_nodes, monkeypatch, "_next_action", **{**NKW, "realized": None})[0] == "err"
    assert check(orig_nodes, monkeypatch, "_next_action", **{**NKW, "exit_hold": {"by_hold_offset": ["bad"]}})[0] == "err"
    out = check(orig_nodes, monkeypatch, "_next_action", **NKW, overrides={"_to_float": lambda v: 42.0})
    assert out["evidence"]["realized_expectancy_pct"] == 42.0


# ---- A45-5 render_loss_decomposition ----
RP = {"range": {"start": "2026-04-10", "end": "2026-04-14"}, "evidence": {"shadow_payload_count": 3, "raw_shadow_candidate_count": 100, "deduped_shadow_candidate_count": 80, "trusted_forward_count": 40,
                                                                          "trusted_forward_coverage": 0.5, "trusted_forward_observed_days": ["2026-04-10", "2026-04-11"], "trade_model_count": 6},
      "diagnosis": [{"stage": "s1", "status": "OK", "finding": "f 한글"}, {}], "raw_candidate_edge": {"by_time_bucket": [{"name": "open", "observed_count": 3, "avg_return_5m_pct": 0.1, "avg_return_15m_pct": None}, {}]},
      "scanner_ranking": {"by_rank_bucket": [{"name": "rank1", "observed_count": 2, "avg_return_30m_pct": 1.5}]}, "realized_system": {"performance": {"count": 4, "win_rate": 0.25, "average_return_pct": -0.5, "expectancy_pct": -0.5, "profit_factor": 0.3, "maximum_drawdown_pct": -3}},
      "monitor_entry": {"matched_trade_count": 2, "average_entry_price_delta_pct": 0.2, "late_entry_count": 1},
      "monitor_exit": {"by_hold_offset": [{"offset": "+5m", "count": 3, "average_improvement_pct": 0.5, "improved_count": 2, "worsened_count": 1}]},
      "next_action": {"component": "c", "decision": "d", "reason": "r 이유"}}
RPS = [{}, {"range": None, "evidence": None}, RP, {**RP, "evidence": {"trusted_forward_coverage": "bad"}}, {**RP, "diagnosis": None, "raw_candidate_edge": None, "scanner_ranking": None, "monitor_exit": None},
       {**RP, "evidence": {"trusted_forward_observed_days": []}}, {**RP, "next_action": None, "monitor_entry": None, "realized_system": None}]


@pytest.mark.parametrize("payload", RPS)
def test_render_loss_decomposition(orig_nodes, monkeypatch, guards, payload):
    out = check(orig_nodes, monkeypatch, "render_loss_decomposition", payload)
    assert (isinstance(out, str) and out.endswith("\n") and "\r" not in out) or out[0] == "err"


def test_render_loss_decomposition_exact_bytes_and_errors(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_loss_decomposition", RP)
    assert out.startswith("# Full-Chain Loss Decomposition (2026-04-10 ~ 2026-04-14)\n\nThis report is evaluation-only and does not change trading behavior.\n\n## Evidence\n\n- shadow payloads: 3\n")
    assert "- raw/deduped candidates: 100 / 80\n- trusted forward: 40 (50.0%)\n- trusted forward observed days: 2026-04-10, 2026-04-11\n" in out
    assert "| s1 | `OK` | f 한글 |\n| None | `None` | None |\n" in out and "| open | 3 | 0.1 | None | None | None |\n" in out
    assert "| +5m | 3 | 0.5% | 2 | 1 |\n" in out and out.endswith("- reason: r 이유\n- behavior change authorized: **False**\n")
    empty = check(orig_nodes, monkeypatch, "render_loss_decomposition", {})
    assert "(None ~ None)" in empty and "- trusted forward: None (0.0%)\n- trusted forward observed days: -\n" in empty
    assert check(orig_nodes, monkeypatch, "render_loss_decomposition", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "render_loss_decomposition", {"evidence": {"trusted_forward_coverage": [1]}})[0] == "err"
    assert check(orig_nodes, monkeypatch, "render_loss_decomposition", {"diagnosis": ["bad"]})[0] == "err"


# ---- A45-6 / A45-7 evaluation_lens_report candidate rows ----
def _attach_spy():
    log = []

    def attach(rows):
        log.append(copy.deepcopy(rows))
        return [{**r, "attached": True} for r in rows]
    attach.log = log
    return attach


EPAYS = [[], [{}], [{"candidates": None}], [{"candidates": []}], [{"generated_at": "g", "candidates": [{"a": 1}, "bad", None, {"b": 2, "_payload_generated_at": "keep"}]}],
         [{"generated_at": "g1", "candidates": [{"a": 1}], "q9_decision_candidates": [{"q": 1}]}, {"generated_at": "g2", "candidates": [{"a": 2}], "q9_decision_candidates": [{"q": 2}, 5]}],
         [{"q9_decision_candidates": [{"q": 1}]}], (), [{"candidates": ({"t": 1},)}]]


@pytest.mark.parametrize("name,key", [("_candidate_rows", "candidates"), ("_q9_candidate_rows", "q9_decision_candidates")])
@pytest.mark.parametrize("payloads", EPAYS)
def test_lens_candidate_rows(orig_nodes, monkeypatch, guards, name, key, payloads):
    attach = _attach_spy()
    check(orig_nodes, monkeypatch, name, payloads, overrides={"attach_forward_outcomes": attach})
    half = len(attach.log) // 2
    assert half * 2 == len(attach.log) and attach.log[:half] == attach.log[half:]


@pytest.mark.parametrize("name,key", [("_candidate_rows", "candidates"), ("_q9_candidate_rows", "q9_decision_candidates")])
def test_lens_candidate_rows_exact_generator_and_errors(orig_nodes, monkeypatch, guards, name, key):
    attach = _attach_spy()
    src = {"a": 1}
    out = check(orig_nodes, monkeypatch, name, [{"generated_at": "g", key: [src]}], overrides={"attach_forward_outcomes": attach})
    assert out == [{"a": 1, "_payload_generated_at": "g", "attached": True}] and "_payload_generated_at" not in src  # copy, no mutation
    other = "q9_decision_candidates" if key == "candidates" else "candidates"
    assert check(orig_nodes, monkeypatch, name, [{other: [{"x": 1}]}], overrides={"attach_forward_outcomes": attach}) == []  # other key ignored
    # a one-shot generator of payloads is consumed exactly once
    fn = getattr(EL, name)
    consumed = []

    def gen():
        for p in ({"generated_at": "g", key: [{"i": 1}]}, {"generated_at": "h", key: [{"i": 2}]}):
            consumed.append(p["generated_at"])
            yield p
    monkeypatch.setattr(EL, "attach_forward_outcomes", attach)
    assert [r["i"] for r in fn(gen())] == [1, 2] and consumed == ["g", "h"]
    assert check(orig_nodes, monkeypatch, name, None, overrides={"attach_forward_outcomes": attach})[0] == "err"
    assert check(orig_nodes, monkeypatch, name, ["x"], overrides={"attach_forward_outcomes": attach})[0] == "err"

    def boom(rows):
        raise RuntimeError("attach failure")
    assert check(orig_nodes, monkeypatch, name, [{key: [{"a": 1}]}], overrides={"attach_forward_outcomes": boom}) == ("err", "RuntimeError", "attach failure")

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, name, [{key: [{"a": 1}]}], overrides={"Mapping": NeverMapping, "attach_forward_outcomes": attach}) == []


# ---- A45-8 cost_basis_comparison._topk_rows ----
TK = [{}, {"topk_forward_performance": None}, {"topk_forward_performance": "x"}, {"topk_forward_performance": {}}, {"topk_forward_performance": {"rows": None}},
      {"topk_forward_performance": {"rows": [{"top_k": 1, "horizon": "+5m", "v": 1}, {"top_k": "3", "horizon": "+15m", "v": 2}, "bad", None, {"v": 3}, {"top_k": 0, "horizon": None, "v": 4},
                                             {"top_k": 1, "horizon": "+5m", "v": "dup"}]}},
      {"topk_forward_performance": {"rows": ({"top_k": 2, "horizon": "EOD"},)}}, {"topk_forward_performance": {"rows": [{"top_k": "x"}]}}, {"topk_forward_performance": {"rows": [{"top_k": 1.7, "horizon": 5}]}}]


@pytest.mark.parametrize("review", TK)
def test_topk_rows(orig_nodes, monkeypatch, guards, review):
    check(orig_nodes, monkeypatch, "_topk_rows", review)


def test_topk_rows_exact_copy_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_topk_rows", TK[5])
    assert list(out)[:2] == [(1, "+5m"), (3, "+15m")] and out[(1, "+5m")]["v"] == "dup" and (0, "") in out  # later duplicate wins, key insertion order of first occurrence
    row = {"top_k": 1, "horizon": "h", "v": 1}
    got = CB._topk_rows({"topk_forward_performance": {"rows": [row]}})
    assert got[(1, "h")] == row and got[(1, "h")] is not row  # dict copy
    assert check(orig_nodes, monkeypatch, "_topk_rows", {"topk_forward_performance": {"rows": [{"top_k": "x"}]}}) == ("err", "ValueError", "invalid literal for int() with base 10: 'x'")
    assert check(orig_nodes, monkeypatch, "_topk_rows", None)[0] == "err"

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_topk_rows", TK[5], overrides={"Mapping": NeverMapping}) == {}


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
