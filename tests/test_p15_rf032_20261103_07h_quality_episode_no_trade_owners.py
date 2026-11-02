"""RF-032 A54-1..8: ``scanner_quality`` / ``episode_scanner_review`` / ``no_trade_attribution`` builder and renderer bodies, original vs thin wrappers + Owners.

Original = A preimage 0d0c2df8 (SOURCE blobs 57f19041 / 0f0b5ac1 / 7f707a44 == canonical d045b740). Each original function is compiled from
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

A_PRE = "0d0c2df89246008df053fb1a054ad61109fd39ad"
CANON = "d045b740e2f9f60d08229697b5f294accee58822"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "build_scanner_quality_review": ("scanner_quality", "57f190411ed91e6318771f63ffda8f416a6eacac", "scanner_quality_build_scanner_quality_review"),
    "build_episode_scanner_review": ("episode_scanner_review", "0f0b5ac107f26a0aa82ff8c0b75e7a0ad65bcdfe", "episode_scanner_review_build_episode_scanner_review"),
    "build_same_symbol_reentry_review": ("episode_scanner_review", "0f0b5ac107f26a0aa82ff8c0b75e7a0ad65bcdfe", "episode_scanner_review_build_same_symbol_reentry_review"),
    "render_no_trade_attribution_report": ("no_trade_attribution", "7f707a446d06362bf3962318b7c88563a306bfd0", "no_trade_attribution_render"),
    "_baseline_samsung": ("no_trade_attribution", "7f707a446d06362bf3962318b7c88563a306bfd0", "no_trade_attribution_baseline_samsung"),
    "_q12_btc_woori": ("no_trade_attribution", "7f707a446d06362bf3962318b7c88563a306bfd0", "no_trade_attribution_q12_btc_woori"),
    "_q9_windows": ("no_trade_attribution", "7f707a446d06362bf3962318b7c88563a306bfd0", "no_trade_attribution_q9_windows"),
    "_q11_opening": ("no_trade_attribution", "7f707a446d06362bf3962318b7c88563a306bfd0", "no_trade_attribution_q11_opening"),
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

SQ = MODS["scanner_quality"]
ES = MODS["episode_scanner_review"]
NT = MODS["no_trade_attribution"]


class NeverMapping:
    pass


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


# ---- A54-1 build_scanner_quality_review ----
def _fake_pre(rows):
    log = []

    def pre(payloads, *, minute_rows_by_symbol=None):
        log.append((copy.deepcopy(payloads), copy.deepcopy(minute_rows_by_symbol)))
        return copy.deepcopy(rows)
    pre.log = log
    return pre


def _fake_builders():
    def topk(rows, *, cost_pct, slippage_pct):
        return {"topk": len(rows), "cost": cost_pct, "slip": slippage_pct}

    def source(rows, *, cost_pct, slippage_pct):
        return {"source": len(rows), "cost": cost_pct, "slip": slippage_pct}
    return topk, source


@pytest.mark.parametrize("rows", [[], [{"a": 1}], [{"a": 1}, {"b": 2}]])
@pytest.mark.parametrize("minute_rows", ["omit", None, {}, {"005930": [{"ts": 1}]}])
@pytest.mark.parametrize("cost,slip", [(0.0, 0.0), (0.9, 0.05), (None, "x")])
def test_build_scanner_quality_review(orig_nodes, monkeypatch, guards, rows, minute_rows, cost, slip):
    pre = _fake_pre(rows)
    topk, source = _fake_builders()
    kw = dict(cost_pct=cost, slippage_pct=slip, overrides={"pre_strategist_candidate_rows": pre, "build_scanner_topk_forward_performance": topk, "build_scanner_source_performance": source})
    if minute_rows == "omit":
        check(orig_nodes, monkeypatch, "build_scanner_quality_review", [{"p": 1}], **kw)
    else:
        check(orig_nodes, monkeypatch, "build_scanner_quality_review", [{"p": 1}], minute_rows_by_symbol=minute_rows, **kw)
    half = len(pre.log) // 2
    assert half * 2 == len(pre.log) and pre.log[:half] == pre.log[half:]  # same arguments reach the loader on both sides


def test_build_scanner_quality_review_exact_and_seams(orig_nodes, monkeypatch, guards):
    pre = _fake_pre([{"a": 1}])
    topk, source = _fake_builders()
    ov = {"pre_strategist_candidate_rows": pre, "build_scanner_topk_forward_performance": topk, "build_scanner_source_performance": source}
    out = check(orig_nodes, monkeypatch, "build_scanner_quality_review", [{"p": 1}], cost_pct=0.9, slippage_pct=0.05, overrides=ov)
    assert list(out) == ["schema_version", "behavior_effect", "pre_strategist_universe_available", "topk_forward_performance", "source_performance"] and out["pre_strategist_universe_available"] is True
    assert out["topk_forward_performance"] == {"topk": 1, "cost": 0.9, "slip": 0.05}
    assert pre.log[0][1] is None  # the default None is forwarded as minute_rows_by_symbol=None
    empty = check(orig_nodes, monkeypatch, "build_scanner_quality_review", [], cost_pct=0.0, slippage_pct=0.0, overrides={**ov, "pre_strategist_candidate_rows": _fake_pre([])})
    assert empty["pre_strategist_universe_available"] is False
    sig = inspect.signature(SQ.build_scanner_quality_review)
    assert [p.kind.name for p in sig.parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY", "KEYWORD_ONLY", "KEYWORD_ONLY"] and sig.parameters["minute_rows_by_symbol"].default is None

    def boom(*a, **k):
        raise RuntimeError("loader failure")
    assert check(orig_nodes, monkeypatch, "build_scanner_quality_review", [], cost_pct=0.0, slippage_pct=0.0, overrides={**ov, "pre_strategist_candidate_rows": boom}) == ("err", "RuntimeError", "loader failure")


# ---- A54-2 build_episode_scanner_review ----
def _c(day="2026-04-10", sym="A", epoch=1000, rank=1, ret30=1.0, breakdown=None, **extra):
    row = {"generated_at": f"{day}T00:00:00+00:00", "symbol": sym, "rank": rank, "shadow_forward_base": {"baseline_epoch": epoch}, "entry_lane_observation": {"subtype_v2": "S1"},
           "shadow_forward_outcome": {"checkpoints": {"+30m": {"status": "observed", "return_pct": ret30}, "+5m": {"status": "observed", "return_pct": 0.5}}}}
    if breakdown is not None:
        row["score_breakdown"] = breakdown
    row.update(extra)
    return row


def _many(n, **kw):
    return [_c(sym=f"S{i}", day=f"2026-04-{10 + i % 3}", epoch=1000 + i * 5000, rank=1 + i % 5, ret30=0.5 + (i % 7) * 0.2, breakdown={"mom": float(i % 9), "trend": float((i * 3) % 7)}, **kw) for i in range(n)]


EROWS = {"empty": [], "one": [_c()], "few": [_c(), _c(sym="B", rank=2), _c(sym="C", rank=3, ret30=-1.0), _c(sym="D", rank=7, ret30=2.0)], "many": _many(30), "no_breakdown": _many(30, ),
         "partial_breakdown": _many(24)[:12] + [dict(_c(sym=f"Z{i}", epoch=1000 + i * 5000, rank=2), score_breakdown=None) for i in range(12)], "bad_values": [_c(breakdown={"mom": "x", "other": 1})], "gap": [_c(), _c(epoch=1100), _c(epoch=5000)]}


def _esr_kw(**kw):
    base = dict(mock_drag_pct=0.9, live_drag_pct=0.23)
    base.update(kw)
    return base


@pytest.mark.parametrize("case", list(EROWS))
@pytest.mark.parametrize("gap", ["omit", 0, 300, 100000])
def test_build_episode_scanner_review_prepared(orig_nodes, monkeypatch, guards, case, gap):
    kw = _esr_kw(prepared_rows=EROWS[case])
    if gap != "omit":
        kw["episode_gap_sec"] = gap
    check(orig_nodes, monkeypatch, "build_episode_scanner_review", [], **kw)


@pytest.mark.parametrize("case", ["empty", "few", "many"])
def test_build_episode_scanner_review_loader_path(orig_nodes, monkeypatch, guards, case):
    rows = EROWS[case]
    seen = []
    check(orig_nodes, monkeypatch, "build_episode_scanner_review", [{"payload": 1}], **_esr_kw(),
          overrides={"pre_strategist_candidate_rows": lambda payloads: seen.append(payloads) or copy.deepcopy(rows)})
    assert seen == [[{"payload": 1}]] * 2  # loader used (once per side) only when prepared_rows is None


def test_build_episode_scanner_review_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "build_episode_scanner_review", [], **_esr_kw(prepared_rows=EROWS["many"]))
    assert list(out) == ["schema_version", "behavior_effect", "episode_gap_sec", "raw_candidate_row_count", "episode_count", "compression_ratio", "cost_drag_pct", "rank_horizon_rows", "score_component_review",
                         "rank1_minus_rank2_3_gross_30m_pct", "episodes", "limitations"]
    assert out["episode_gap_sec"] == 900 and out["cost_drag_pct"] == {"mock": 0.9, "live": 0.23} and len(out["rank_horizon_rows"]) == len(ES.RANK_BUCKETS) * len(ES.SCANNER_HORIZONS)
    assert [(r["rank_bucket"], r["horizon"]) for r in out["rank_horizon_rows"]][:2] == [("rank1", "+5m"), ("rank1", "+15m")] and list(out["score_component_review"]) == ["status", "forward_observed_episode_count", "component_covered_episode_count", "coverage", "rows"]
    assert out["score_component_review"]["status"] == "READY" and out["score_component_review"]["rows"]
    assert check(orig_nodes, monkeypatch, "build_episode_scanner_review", [], **_esr_kw(prepared_rows=EROWS["few"]))["score_component_review"]["status"] == "NOT_READY_MISSING_SCORE_COMPONENT_ARTIFACT"
    empty = check(orig_nodes, monkeypatch, "build_episode_scanner_review", [], **_esr_kw(prepared_rows=[]))
    assert empty["compression_ratio"] == 0.0 and empty["rank1_minus_rank2_3_gross_30m_pct"] == 0.0 and empty["episodes"] == []  # empty metrics give 0.0 expectancy, not None
    src = copy.deepcopy(EROWS["few"])
    ES.build_episode_scanner_review([], **_esr_kw(prepared_rows=src))
    assert src == EROWS["few"]  # prepared rows are copied, never mutated
    assert check(orig_nodes, monkeypatch, "build_episode_scanner_review", [], mock_drag_pct="x", live_drag_pct=0.1, prepared_rows=EROWS["few"])[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, "build_episode_scanner_review", None, **_esr_kw())[0] == "err"
    sig = inspect.signature(ES.build_episode_scanner_review)
    assert sig.parameters["episode_gap_sec"].default == 900 and sig.parameters["prepared_rows"].default is None and [p.kind.name for p in sig.parameters.values()][1:] == ["KEYWORD_ONLY"] * 4


def test_build_episode_scanner_review_helper_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "build_episode_scanner_review", [], **_esr_kw(prepared_rows=[{"x": 1}, {"x": 2}]),
                overrides={"_episode_representatives": lambda rows, *, episode_gap_sec: [{"rank_bucket": "rank1", "day": "D", "returns": {"+30m": 2.0, "+5m": None}, "score_breakdown": {"c": 3}}],
                           "RANK_BUCKETS": ("rank1",), "SCANNER_HORIZONS": ("+5m", "+30m"), "performance_metrics": lambda vals: {"n": len(vals)}})
    assert [r["gross"] for r in out["rank_horizon_rows"]] == [{"n": 0}, {"n": 1}] and out["episode_count"] == 1
    assert check(orig_nodes, monkeypatch, "build_episode_scanner_review", [], **_esr_kw(prepared_rows=EROWS["many"]), overrides={"sqrt": lambda v: 1.0})["score_component_review"]["rows"][0]["score_return_correlation"] is not None


def test_build_episode_scanner_review_defaultdict_seam(orig_nodes, monkeypatch, guards):
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "build_episode_scanner_review", [], **_esr_kw(prepared_rows=EROWS["many"]), overrides={"defaultdict": spy})
    assert len(made) >= 2 and len(made) % 2 == 0


# ---- A54-3 build_same_symbol_reentry_review ----
def _t(tid, sym, ret):
    return {"trade_id": tid, "symbol": sym, "net_return_pct": ret}


REN = {"empty": [], "single": [_t("T_20260410_AAA_1", "A", 1.0)],
       "repeat": [_t("T_20260410_AAA_1", "A", -1.0), _t("T_20260410_AAA_2", "A", 0.5), _t("T_20260410_AAA_3", "A", -0.2), _t("T_20260411_AAA_1", "A", 2.0)],
       "bad_ids": [_t("", "A", 1.0), _t("short", "A", 1.0), _t("T_xx_AAA_1", "A", 1.0), _t("T_20260410_AAA_x", "A", 1.0), _t(None, "A", 1.0)],
       "dupe_ids": [_t("T_20260410_AAA_1", "A", 1.0), _t("T_20260410_AAA_1", "A", -3.0)], "no_symbol_or_value": [_t("T_20260410_AAA_1", "", 1.0), _t("T_20260410_BBB_1", "B", None), _t("T_20260410_CCC_1", "C", "bad")],
       "many_after_loss": [_t("T_20260410_AAA_1", "A", 0.5)] + [_t(f"T_2026041{i % 9}_S{i}_1", f"S{i}", 1.0) for i in range(30)] + [_t(f"T_2026041{i % 9}_S{i}_2", f"S{i}", -1.0) for i in range(30)],
       "zero_prior": [_t("T_20260410_AAA_1", "A", 0.0), _t("T_20260410_AAA_2", "A", 1.0)], "sequence_order": [_t("T_20260410_AAA_10", "A", 1.0), _t("T_20260410_AAA_2", "A", -1.0), _t("T_20260410_AAA_1", "A", 3.0)],
       "non_mapping": [{"trade_id": "T_20260410_AAA_1", "symbol": "A", "net_return_pct": 1.0}, _MapSub(trade_id="T_20260410_AAA_2", symbol="A", net_return_pct=-1.0)]}


@pytest.mark.parametrize("case", list(REN))
def test_build_same_symbol_reentry_review(orig_nodes, monkeypatch, guards, case):
    check(orig_nodes, monkeypatch, "build_same_symbol_reentry_review", REN[case])


def test_reentry_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "build_same_symbol_reentry_review", REN["repeat"])
    assert list(out) == ["schema_version", "behavior_effect", "day_symbol_group_count", "repeated_day_symbol_group_count", "first_entry", "repeat_entry", "repeat_after_loss", "repeat_after_non_loss",
                         "repeat_minus_first_expectancy_pct", "behavior_candidate_eligible", "limitations"]
    assert out["day_symbol_group_count"] == 2 and out["repeated_day_symbol_group_count"] == 1 and out["repeat_after_loss"]["count"] == 1 and out["repeat_after_non_loss"]["count"] == 1
    assert check(orig_nodes, monkeypatch, "build_same_symbol_reentry_review", REN["dupe_ids"])["first_entry"]["count"] == 1  # last row of a duplicated trade id wins
    assert check(orig_nodes, monkeypatch, "build_same_symbol_reentry_review", REN["sequence_order"])["repeat_entry"]["count"] == 2
    assert check(orig_nodes, monkeypatch, "build_same_symbol_reentry_review", REN["many_after_loss"])["behavior_candidate_eligible"] is False  # 30 repeats after wins/losses, not enough loss-conditioned edge gap
    assert check(orig_nodes, monkeypatch, "build_same_symbol_reentry_review", None)[0] == "err" and check(orig_nodes, monkeypatch, "build_same_symbol_reentry_review", [None])[0] == "err"
    out = check(orig_nodes, monkeypatch, "build_same_symbol_reentry_review", REN["repeat"], overrides={"_number": lambda v: None if v is None else 1.0, "performance_metrics": lambda vals: {"n": len(vals), "expectancy_pct": 1.0, "win_rate": 1.0}})
    assert out["first_entry"] == {"n": 2, "expectancy_pct": 1.0, "win_rate": 1.0} and out["repeat_minus_first_expectancy_pct"] == 0.0


def test_reentry_defaultdict_seam(orig_nodes, monkeypatch, guards):
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "build_same_symbol_reentry_review", REN["repeat"], overrides={"defaultdict": spy})
    assert made == [1, 1]


# ---- A54-4 render_no_trade_attribution_report ----
NP = {"behavior_effect": "observation_only", "day": "2026-04-10", "trade_count": 0, "q9_window_count": 12, "no_trade_class": "OVER_FILTER", "primary_issue": "commander", "commander_approve_monitor_noop_count": 3,
      "commander_decisions": [{"name": "APPROVE", "count": 5}, "bad", {}], "commander_reasons": [], "commander_details": None, "monitor_intents": [{"name": "한글", "count": 2}], "monitor_noop_reasons": [{"name": "r", "count": 1}],
      "scanner_top1": [{"name": "A", "count": 4}], "strategist_selected": [{"name": "B", "count": 0}], "shadow_opportunity_status": "READY",
      "q11_opening_opportunity": {"available": True, "signal_rows": 5, "probe_candidates": 2, "probe_near_misses": 1, "virtual_trades": 3, "win_rate": 0.0, "avg_net_return_pct": 0.5, "avg_mfe_pct": 1.25, "avg_mae_pct": None},
      "q10_samsung_hynix": {"horizons": [{"horizon": "+5m", "trade_count": 4, "win_rate": 0.5, "avg_net_return_pct": -0.25, "profit_factor": 0.8}, "bad", {}]}, "q12_btc_woori": {"horizons": []}}
NPS = [{}, NP, {**NP, "q11_opening_opportunity": None, "q10_samsung_hynix": None, "q12_btc_woori": None}, {**NP, "commander_decisions": "notalist"}, {**NP, "q10_samsung_hynix": {"horizons": "bad"}}, {"q12_btc_woori": {"horizons": [{"horizon": "+5m"}]}},
       {**NP, "q11_opening_opportunity": {"win_rate": None, "avg_net_return_pct": "bad"}}]


@pytest.mark.parametrize("payload", NPS)
def test_render_no_trade_attribution_report(orig_nodes, monkeypatch, guards, payload):
    out = check(orig_nodes, monkeypatch, "render_no_trade_attribution_report", payload)
    assert (isinstance(out, str) and out.endswith("\n") and "\r" not in out) or out[0] == "err"


def test_render_no_trade_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_no_trade_attribution_report", NP)
    assert out.startswith("# No-Trade Attribution Report\n\n- Behavior effect: `observation_only`\n- Day: `2026-04-10`\n- Trades: 0\n- Q9 windows: 12\n")
    assert "### Commander Decisions\n\n- `APPROVE`: 5\n- ``: 0\n\n" in out and "### Commander Reasons\n\n- None\n\n" in out and "- `한글`: 2\n" in out
    assert "- Q11 win rate: 0.0\n" in out and "- Q11 avg net: 0.5000%\n" in out and "- Q11 avg MAE: -\n" in out
    assert "| Q10 Samsung/Hynix | +5m | 4 | 0.5 | -0.2500% | 0.8 |\n| Q10 Samsung/Hynix | - | 0 | - | - | - |\n" in out and "| Q12 BTC/Woori | - | 0 | - | - | - |\n" in out
    assert out.endswith("check whether the absence itself is an over-filtering signal.\n") or out.endswith("this report decides whether the absence itself is an over-filtering signal.\n")
    empty = check(orig_nodes, monkeypatch, "render_no_trade_attribution_report", {})
    assert "- Trades: 0\n" in empty and "### Scanner Top1\n\n- None\n" in empty
    assert check(orig_nodes, monkeypatch, "render_no_trade_attribution_report", None)[0] == "err"
    out = check(orig_nodes, monkeypatch, "render_no_trade_attribution_report", NP, overrides={"_pct": lambda v: f"<{v}>"})
    assert "- Q11 avg net: <0.5>\n" in out
    assert "- `APPROVE`: 5" not in check(orig_nodes, monkeypatch, "render_no_trade_attribution_report", NP, overrides={"Mapping": NeverMapping})


# ---- A54-5 / A54-6 baselines ----
def _hz(**kw):
    return kw


BASE = {"empty": {}, "no_summary": {"x": 1}, "summary_bad": {"summary": "bad"}, "horizons_bad": {"summary": {"horizons": "bad"}}, "horizons_empty": {"summary": {"horizons": []}},
        "top1": {"summary": {"horizons": [{"horizon": "+5m", "top1_observation_count": 7, "trade_count": 99, "top1_net": {"win_rate": 0.6, "average_return_pct": 0.3, "profit_factor": 1.5}}]}},
        "legacy": {"summary": {"horizons": [{"horizon": "+15m", "trade_count": 4, "win_rate": 0.5, "avg_net_return_pct": -0.1, "profit_factor": 0.9}]}},
        "legacy_top1_fields": {"summary": {"horizons": [{"horizon": "+30m", "top1_observation_count": 0, "trade_count": 3, "top1_win_rate": 0.4, "win_rate": 0.1, "top1_avg_net_return_pct": 0.2, "avg_net_return_pct": 9, "top1_profit_factor": 1.1, "profit_factor": 9}]}},
        "zeros": {"summary": {"horizons": [{"horizon": "+5m", "top1_net": {"win_rate": 0, "average_return_pct": 0, "profit_factor": 0}, "win_rate": 0.9, "avg_net_return_pct": 0.9, "profit_factor": 0.9}]}},
        "mixed_rows": {"summary": {"horizons": ["bad", None, {"horizon": None}, {"horizon": "+5m", "top1_net": "bad", "win_rate": "x"}, _MapSub(horizon="+60m", trade_count=2)]}}, "bad_numbers": {"summary": {"horizons": [{"trade_count": "x"}]}}}


def _fake_read(payload):
    paths = []

    def read(path):
        paths.append(path)
        return copy.deepcopy(payload)
    read.paths = paths
    return read


@pytest.mark.parametrize("name", ["_baseline_samsung", "_q12_btc_woori"])
@pytest.mark.parametrize("case", list(BASE))
def test_baseline_readers(orig_nodes, monkeypatch, guards, name, case):
    read = _fake_read(BASE[case])
    check(orig_nodes, monkeypatch, name, Path("rr"), "2026-04-10", overrides={"_read_json": read})
    half = len(read.paths) // 2
    assert half * 2 == len(read.paths) and read.paths[:half] == read.paths[half:]


PATHS = {"_baseline_samsung": ("baseline_samsung_hynix", "baseline_samsung_hynix_forward_returns.json"), "_q12_btc_woori": ("baseline_btc_woori_tech", "baseline_btc_woori_forward_returns.json")}


@pytest.mark.parametrize("name", list(PATHS))
def test_baseline_readers_paths_errors_and_seams(orig_nodes, monkeypatch, guards, name):
    sub, fname = PATHS[name]
    read = _fake_read(BASE["top1"])
    check(orig_nodes, monkeypatch, name, Path("rr"), "2026-04-10", overrides={"_read_json": read})
    assert read.paths[0] == Path("rr") / "evaluation" / sub / "2026-04-10" / fname
    assert check(orig_nodes, monkeypatch, name, Path("rr"), "d", overrides={"_read_json": _fake_read({})}) == {"available": False, "horizons": []}
    assert check(orig_nodes, monkeypatch, name, Path("rr"), "d", overrides={"_read_json": _fake_read(BASE["bad_numbers"])})[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, name, None, "d", overrides={"_read_json": _fake_read({})})[0] == "err"

    def boom(path):
        raise RuntimeError("read failure")
    assert check(orig_nodes, monkeypatch, name, Path("rr"), "d", overrides={"_read_json": boom}) == ("err", "RuntimeError", "read failure")


@pytest.mark.parametrize("name", list(PATHS))
def test_baseline_readers_num_seam(orig_nodes, monkeypatch, guards, name):
    out = check(orig_nodes, monkeypatch, name, Path("rr"), "d", overrides={"_read_json": _fake_read(BASE["top1"]), "_num": lambda v: "NUM"})
    assert out["horizons"][0]["win_rate"] == "NUM"


def test_baseline_samsung_exact(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_baseline_samsung", Path("rr"), "d", overrides={"_read_json": _fake_read(BASE["top1"])})
    assert out == {"available": True, "horizons": [{"horizon": "+5m", "trade_count": 7, "win_rate": 0.6, "avg_net_return_pct": 0.3, "profit_factor": 1.5}]} and list(out["horizons"][0]) == ["horizon", "trade_count", "win_rate", "avg_net_return_pct", "profit_factor"]
    legacy = check(orig_nodes, monkeypatch, "_baseline_samsung", Path("rr"), "d", overrides={"_read_json": _fake_read(BASE["legacy_top1_fields"])})["horizons"][0]
    assert legacy == {"horizon": "+30m", "trade_count": 3, "win_rate": 0.4, "avg_net_return_pct": 0.2, "profit_factor": 1.1}  # 0 top1 count falls back (truthiness), top1_* before legacy
    zeros = check(orig_nodes, monkeypatch, "_baseline_samsung", Path("rr"), "d", overrides={"_read_json": _fake_read(BASE["zeros"])})["horizons"][0]
    assert zeros["win_rate"] == 0.9 and zeros["avg_net_return_pct"] == 0.9  # a 0 top1 value is falsy -> legacy fallback


def test_q12_btc_woori_exact(orig_nodes, monkeypatch, guards):
    payload = {"summary": {"horizons": [{"horizon": "+5m", "trade_count": 6, "eligible_entries_net": {"win_rate": 0.8, "average_return_pct": 0.4, "profit_factor": 2.0},
                                           "top1_net": {"win_rate": 0.1, "average_return_pct": 0.1, "profit_factor": 0.1}, "win_rate": 0.01},
                                          {"horizon": "+15m", "trade_count": 2, "eligible_entries_net": {"win_rate": 0}, "top1_net": {"win_rate": 0.3, "average_return_pct": 0.2, "profit_factor": 1.1}, "avg_net_return_pct": 9},
                                          {"horizon": "+30m", "win_rate": 0.5, "avg_net_return_pct": -0.1, "profit_factor": 0.7}]}}
    out = check(orig_nodes, monkeypatch, "_q12_btc_woori", Path("rr"), "d", overrides={"_read_json": _fake_read(payload)})
    assert [h["win_rate"] for h in out["horizons"]] == [0.8, 0.3, 0.5]  # eligible_entries_net, then top1_net, then the flat field (truthiness fallback)
    assert [h["avg_net_return_pct"] for h in out["horizons"]] == [0.4, 0.2, -0.1] and [h["trade_count"] for h in out["horizons"]] == [6, 2, 0]


@pytest.mark.parametrize("name", ["_baseline_samsung", "_q12_btc_woori"])
def test_baseline_readers_mapping_seam(orig_nodes, monkeypatch, guards, name):
    out = check(orig_nodes, monkeypatch, name, Path("rr"), "d", overrides={"_read_json": _fake_read(BASE["top1"]), "Mapping": NeverMapping})
    assert out["horizons"] == []  # rows are filtered with the call-time Mapping


# ---- A54-7 _q9_windows ----
def _it(rows, error=None):
    calls = []

    def it(path, key):
        calls.append((path, key))
        for r in rows:
            yield r
        if error:
            raise error
    it.calls = calls
    return it


WROWS = [{"id": 1}, {"id": 2, "synthetic": True}, {"id": 3, "outside": True}, "bad", None, {"id": 5}]


def _filters():
    return {"is_synthetic_evaluation_row": lambda r: bool(r.get("synthetic")), "is_regular_session_evaluation_row": lambda r: not r.get("outside"), "_q9_window_view": lambda r: {"view": r["id"]}}


@pytest.mark.parametrize("rows,error", [([], None), (WROWS, None), (WROWS[:2], ValueError("broken stream")), ([], ValueError("x")), ([{"id": 9}], None), (WROWS, RuntimeError("other failure")), ([{"id": 4}], OSError("disk"))])
def test_q9_windows(orig_nodes, monkeypatch, guards, rows, error):
    it = _it(rows, error)
    check(orig_nodes, monkeypatch, "_q9_windows", Path("rr"), "2026-04-10", overrides={"iter_json_array": it, **_filters()})
    half = len(it.calls) // 2
    assert half * 2 == len(it.calls) and it.calls[:half] == it.calls[half:]


def test_q9_windows_exact_streaming_and_seams(orig_nodes, monkeypatch, guards):
    it = _it(WROWS)
    out = check(orig_nodes, monkeypatch, "_q9_windows", Path("rr"), "2026-04-10", overrides={"iter_json_array": it, **_filters()})
    assert out == [{"view": 1}, {"view": 5}] and it.calls[0] == (Path("rr") / "operator_summary" / "daily" / "2026-04-10" / "q9_decision_windows.json", "windows")
    assert check(orig_nodes, monkeypatch, "_q9_windows", Path("rr"), "d", overrides={"iter_json_array": _it([{"id": 1}], ValueError("x")), **_filters()}) == []  # ValueError mid-stream -> no windows at all
    assert check(orig_nodes, monkeypatch, "_q9_windows", Path("rr"), "d", overrides={"iter_json_array": _it([], RuntimeError("other failure")), **_filters()}) == ("err", "RuntimeError", "other failure")
    consumed = []

    def lazy(path, key):
        for r in ({"id": 1}, {"id": 2}):
            consumed.append(r["id"])
            yield r
    monkeypatch.setattr(NT, "iter_json_array", lazy)
    monkeypatch.setattr(NT, "is_synthetic_evaluation_row", lambda r: False)
    monkeypatch.setattr(NT, "is_regular_session_evaluation_row", lambda r: True)
    monkeypatch.setattr(NT, "_q9_window_view", lambda r: {"v": r["id"]})
    assert NT._q9_windows(Path("rr"), "d") == [{"v": 1}, {"v": 2}] and consumed == [1, 2]  # streamed row by row, never materialised as a whole file


# ---- A54-8 _q11_opening ----
Q11 = {"empty": ({}, {}, {}), "daily_only": ({"signal_rows": 4, "win_rate": 0.5, "avg_net_return_pct": 0.2, "avg_mfe_pct": 1.0, "avg_mae_pct": -1.0, "profit_factor": 1.2, "summary": {"trade_count": 3}}, {}, {}),
       "signals": ({}, {"signal_count": 9, "data_quality": {"probe_near_miss_count": 2}, "signals": [{"opportunity": {"probe_candidate": True}}, {"opportunity": {"probe_candidate": False}}, {"opportunity": "bad"}, "bad", None, {}, _MapSub(opportunity={"probe_candidate": 1})]}, {}),
       "virtual": ({}, {}, {"trade_count": 5, "summary": {"win_rate": 0.4, "average_net_return_pct": 0.1, "average_mfe_pct": 2.0, "average_mae_pct": -2.0, "profit_factor": 1.1}}),
       "virtual_precedence": ({"summary": {"win_rate": 0.9}}, {}, {"summary": {"win_rate": 0.1, "avg_net_return": 0.7}}), "fallback_names": ({}, {}, {"summary": {"avg_net_return": 0.3, "avg_mfe": 0.8, "avg_mae": -0.4, "virtual_trades": 6, "signal_rows": 8}}),
       "zeros": ({"win_rate": 0.7}, {}, {"summary": {"win_rate": 0, "average_net_return_pct": 0, "profit_factor": 0}}), "bad_numbers": ({}, {"signal_count": "x"}, {}), "bad_shapes": ({}, {"signals": "notalist", "data_quality": "bad"}, {"summary": "bad"}),
       "signals_none": ({}, {"signals": None, "data_quality": None}, {"summary": None})}


@pytest.mark.parametrize("case", list(Q11))
def test_q11_opening(orig_nodes, monkeypatch, guards, case):
    payload, signals, virtual = Q11[case]
    names = {"opportunity_engine_daily_report.json": payload, "opportunity_engine_signals.json": signals, "opportunity_engine_virtual_trades.json": virtual}
    paths = []

    def read(path):
        paths.append(path.name)
        return copy.deepcopy(names[path.name])
    check(orig_nodes, monkeypatch, "_q11_opening", Path("rr"), "2026-04-10", overrides={"_read_json": read})
    half = len(paths) // 2
    assert half * 2 == len(paths) and paths[:half] == paths[half:] == ["opportunity_engine_daily_report.json", "opportunity_engine_signals.json", "opportunity_engine_virtual_trades.json"]


def _q11_read(case):
    payload, signals, virtual = Q11[case]
    names = {"opportunity_engine_daily_report.json": payload, "opportunity_engine_signals.json": signals, "opportunity_engine_virtual_trades.json": virtual}
    return lambda path: copy.deepcopy(names[path.name])


def test_q11_opening_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_q11_opening", Path("rr"), "2026-04-10", overrides={"_read_json": _q11_read("signals")})
    assert list(out) == ["available", "signal_rows", "probe_candidates", "probe_near_misses", "virtual_trades", "win_rate", "avg_net_return_pct", "avg_mfe_pct", "avg_mae_pct", "profit_factor"]
    assert out["available"] is True and out["signal_rows"] == 9 and out["probe_candidates"] == 2 and out["probe_near_misses"] == 2
    virt = check(orig_nodes, monkeypatch, "_q11_opening", Path("rr"), "d", overrides={"_read_json": _q11_read("virtual_precedence")})
    assert virt["win_rate"] == 0.1 and virt["avg_net_return_pct"] == 0.7  # virtual summary wins over the daily report
    assert check(orig_nodes, monkeypatch, "_q11_opening", Path("rr"), "d", overrides={"_read_json": _q11_read("empty")})["available"] is False
    assert check(orig_nodes, monkeypatch, "_q11_opening", Path("rr"), "d", overrides={"_read_json": _q11_read("zeros")})["win_rate"] == 0.7  # falsy 0 summary value falls back to the daily report
    assert check(orig_nodes, monkeypatch, "_q11_opening", Path("rr"), "d", overrides={"_read_json": _q11_read("bad_numbers")})[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, "_q11_opening", None, "d", overrides={"_read_json": _q11_read("empty")})[0] == "err"
    out = check(orig_nodes, monkeypatch, "_q11_opening", Path("rr"), "d", overrides={"_read_json": _q11_read("virtual"), "_num": lambda v: "NUM"})
    assert out["win_rate"] == "NUM"

    class FakeMap:
        pass
    out = check(orig_nodes, monkeypatch, "_q11_opening", Path("rr"), "d", overrides={"_read_json": _q11_read("signals"), "Mapping": NeverMapping})
    assert out["probe_candidates"] == 0  # signals ignored when Mapping never matches


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
