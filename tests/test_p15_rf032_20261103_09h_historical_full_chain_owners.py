"""RF-032 A56-1..8: ``full_chain_component_review`` / ``historical_prior`` / ``loss_decomposition`` read-only builder and summary bodies, original vs thin wrappers + Owners.

Original = A preimage 2d48eb29 (SOURCE blobs 7706d356 / a9a223da / 09352162 == canonical 3b859aa4). Each original function is compiled from
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

A_PRE = "2d48eb29c813353eddb8a9e47de1ae5f9787fa1b"
CANON = "3b859aa4facd4d38acdad3fc62507261bf48ae42"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "build_full_chain_component_review": ("full_chain_component_review", "7706d3567dc27286b3c63e6344193401e28a944b", "full_chain_component_review_build_full_chain_component_review", "build_full_chain_component_review"),
    "_day_from_trade_dir": ("historical_prior", "a9a223da81e5c29088004d8d5db0c391f8cf4373", "historical_prior_day_from_trade_dir", "_day_from_trade_dir"),
    "_net_return": ("historical_prior", "a9a223da81e5c29088004d8d5db0c391f8cf4373", "historical_prior_net_return", "_net_return"),
    "_group_metrics": ("historical_prior", "a9a223da81e5c29088004d8d5db0c391f8cf4373", "historical_prior_group_metrics", "_group_metrics"),
    "summarize_historical_prior": ("historical_prior", "a9a223da81e5c29088004d8d5db0c391f8cf4373", "historical_prior_summarize_historical_prior", "summarize_historical_prior"),
    "render_historical_prior_markdown": ("historical_prior", "a9a223da81e5c29088004d8d5db0c391f8cf4373", "historical_prior_render_historical_prior_markdown", "render_historical_prior_markdown"),
    "iter_historical_trade_dirs": ("historical_prior", "a9a223da81e5c29088004d8d5db0c391f8cf4373", "historical_prior_iter_historical_trade_dirs", "iter_historical_trade_dirs"),
    "_load_trade_models": ("loss_decomposition", "09352162fa51641be30763bf9719a126da5ba3bf", "loss_decomposition_load_trade_models", "_load_trade_models"),
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
                out[n] = [x for x in tree.body if isinstance(x, ast.FunctionDef) and x.name == v[3]][-1]
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
    fname = SPEC[name][3]
    for k, v in (overrides or {}).items():
        ns[k] = v
        monkeypatch.setattr(mod, k, v)
    got, values = {}, {}
    for label, fn in (("orig", ns[fname]), ("new", getattr(mod, fname))):
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
import datetime as _dt

FC = MODS["full_chain_component_review"]
HP = MODS["historical_prior"]
LD = MODS["loss_decomposition"]


class NeverMapping:
    pass


class _FloatErr:
    def __init__(self, exc):
        self.exc = exc

    def __repr__(self):
        return f"_FloatErr({self.exc.__name__})"

    def __float__(self):
        raise self.exc("custom float failure")


# ---- A56-1 build_full_chain_component_review (all collaborators faked) ----
class FakeOs:
    def __init__(self, value=None):
        self.value, self.calls = value, []

    def __repr__(self):
        return f"FakeOs({self.value!r})"

    def getenv(self, key, default=None):
        self.calls.append((key, default))
        return default if self.value is None else self.value


def _ent(n=30, days=3, avg=0.1, med=0.1):
    return {"matched_trade_count": n, "matched_day_count": days, "average_entry_price_delta_pct": avg, "median_entry_price_delta_pct": med}


def _ext(n=30, days=3, imp=0.1):
    return {"observed_trade_count": n, "observed_day_count": days, "by_hold_offset": [{"offset": "+15m", "average_improvement_pct": 9}, {"offset": "+5m", "average_improvement_pct": imp}]}


def _real(n=30, days=3, exp=0.2):
    return {"performance": {"count": n, "expectancy_pct": exp}}


def _fc_overrides(entry=None, exit_hold=None, realized=None, attribution=None, profile=None, models=None, os_value=None, payloads=None):
    models = models if models is not None else [{"day": f"2026-04-1{i % 3}T00:00:00", "outcome": {"net_return_pct": 0.1}, "integrity": {}} for i in range(30)] + [{"integrity": {"defects": ["confirmed_runtime_defect"]}, "day": "2026-04-10"}]
    attribution = attribution or {"by_horizon": [{"horizon": "+30m", "post_scanner_refresh_comparison_count": 25, "post_scanner_refresh_day_count": 3, "average_post_scanner_refresh_delta_pct": 0.5, "post_scanner_refresh_positive_delta_rate": 0.7, "other": 1}]}
    loads = []

    def load(**kw):
        loads.append(kw)
        return copy.deepcopy(payloads) if payloads is not None else [{"p": 1}, {"p": 2}]
    ov = {
        "load_quant_shadow_candidate_payloads_for_range": load,
        "_candidate_rows": lambda p: [{"c": i} for i in range(len(p) + 1)],
        "_load_trade_models": lambda root, s, e: copy.deepcopy(models),
        "load_broker_cost_profile": lambda path: copy.deepcopy(profile if profile is not None else {"source": "fake", "sample_count": 5, "conservative_round_trip_cost_pct": 0.006}),
        "build_scanner_quality_review": lambda payloads, *, cost_pct, slippage_pct: {"sq": (len(payloads), cost_pct, slippage_pct)},
        "_role_metrics": lambda cands, *, role, horizon, cost_pct: {"role": role, "horizon": horizon, "cost": cost_pct},
        "_paired_role_deltas": lambda cands, *, horizon: {"horizon": horizon},
        "_selection_availability": lambda m: {"n": len(m)},
        "_decision_window_attribution": lambda payloads, *, cost_pct: copy.deepcopy(attribution),
        "_entry_timing_summary": lambda m, c: copy.deepcopy(entry if entry is not None else _ent()),
        "_exit_hold_summary": lambda m: copy.deepcopy(exit_hold if exit_hold is not None else _ext()),
        "_realized_trade_summary": lambda m: copy.deepcopy(realized if realized is not None else _real()),
        "_classify_root_cause": lambda **kw: {"primary_root_cause": "fake"},
        "_scanner_decision": lambda **kw: {"decision": "RETAIN", "question": "q"},
        "_attribution_component": lambda **kw: {"decision": "COMP", "component": kw["component"]},
        "_unavailable_component": lambda **kw: {"decision": "UNAVAIL"},
        "os": FakeOs(os_value),
    }
    ov["_loads"] = loads
    return ov


def _fc_run(orig_nodes, monkeypatch, start="2026-04-10T09:00", end="2026-04-14", cost_profile_path=None, **kw):
    ov = _fc_overrides(**kw)
    loads = ov.pop("_loads")
    kwargs = {"reports_root": Path("rr"), "start": start, "end": end}
    if cost_profile_path is not None:
        kwargs["cost_profile_path"] = cost_profile_path
    out = check(orig_nodes, monkeypatch, "build_full_chain_component_review", overrides=ov, **kwargs)
    half = len(loads) // 2
    assert half * 2 == len(loads) and loads[:half] == loads[half:]
    return out


FC_SCENARIOS = {
    "all_enough": {}, "entry_short": dict(entry=_ent(n=5)), "entry_late": dict(entry=_ent(avg=0.5)), "entry_median_late": dict(entry=_ent(med=0.5)), "entry_none": dict(entry=_ent(avg=None)),
    "exit_short": dict(exit_hold=_ext(n=5)), "exit_adjust": dict(exit_hold=_ext(imp=0.3)), "exit_retain": dict(exit_hold=_ext(imp=0.29)), "realized_short": dict(realized=_real(n=5)), "realized_negative": dict(realized=_real(exp=-0.1)),
    "realized_zero": dict(realized=_real(exp=0.0)), "no_models": dict(models=[]), "refresh_short": dict(attribution={"by_horizon": [{"horizon": "+30m", "post_scanner_refresh_comparison_count": 3}]}),
    "refresh_not_material": dict(attribution={"by_horizon": [{"horizon": "+30m", "post_scanner_refresh_comparison_count": 25, "post_scanner_refresh_day_count": 3, "average_post_scanner_refresh_delta_pct": 0.1, "post_scanner_refresh_positive_delta_rate": 0.7}]}),
    "attr_empty": dict(attribution={"by_horizon": None}), "profile_ema": dict(profile={"ema_round_trip_cost_pct": 0.004}), "profile_empty": dict(profile={}), "slip_env": dict(os_value="0.2"), "slip_negative": dict(os_value="-1"), "slip_blank": dict(os_value=""),
}


@pytest.mark.parametrize("case", list(FC_SCENARIOS))
def test_build_full_chain_component_review(orig_nodes, monkeypatch, guards, case):
    _fc_run(orig_nodes, monkeypatch, **FC_SCENARIOS[case])


def test_build_full_chain_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = _fc_run(orig_nodes, monkeypatch)
    assert list(out)[:8] == ["schema_version", "contract_version", "behavior_effect", "range", "cost_model", "evidence", "problem_segment", "component_decisions"] and out["range"] == {"start": "2026-04-10", "end": "2026-04-14"}
    assert out["evidence"]["total_trade_model_count"] == 31 and out["evidence"]["trade_model_count"] == 30 and out["evidence"]["excluded_trade_model_count"] == 1  # defect model excluded
    comps = out["component_decisions"]
    assert list(comps) == ["scanner", "strategist", "commander", "monitor_entry", "monitor_exit", "full_system"] and comps["monitor_entry"]["decision"] == "RETAIN" and comps["monitor_exit"]["decision"] == "RETAIN" and comps["full_system"]["decision"] == "RETAIN"
    assert comps["strategist"]["scope"] == "ranking_overlay_only" and comps["strategist"]["post_scanner_refresh"]["decision"] == "PROMOTION_CANDIDATE" and list(comps["strategist"])[-3:] == ["scope", "full_strategist_contribution", "post_scanner_refresh"]
    assert comps["strategist"]["post_scanner_refresh"]["metrics"] == {"horizon": "+30m", "post_scanner_refresh_comparison_count": 25, "post_scanner_refresh_day_count": 3, "average_post_scanner_refresh_delta_pct": 0.5, "post_scanner_refresh_positive_delta_rate": 0.7}
    assert out["cost_model"] == {"source": "fake", "sample_count": 5, "conservative_round_trip_cost_pct": 0.6, "evaluation_slippage_pct": 0.05}
    short = _fc_run(orig_nodes, monkeypatch, entry=_ent(n=5), exit_hold=_ext(n=5), realized=_real(n=5))["component_decisions"]
    assert short["monitor_entry"]["decision"] == "INSUFFICIENT_EVIDENCE" and short["monitor_exit"]["decision"] == "INSUFFICIENT_EVIDENCE" and short["full_system"]["decision"] == "INSUFFICIENT_EVIDENCE" and short["monitor_entry"]["missing_comparison"].startswith("at least 20")
    assert _fc_run(orig_nodes, monkeypatch, realized=_real(exp=-0.1))["component_decisions"]["full_system"]["decision"] == "REJECT" and _fc_run(orig_nodes, monkeypatch, exit_hold=_ext(imp=0.3))["component_decisions"]["monitor_exit"]["decision"] == "ADJUST_AND_RETEST"
    assert _fc_run(orig_nodes, monkeypatch, os_value="-1")["cost_model"]["evaluation_slippage_pct"] == 0.0 and _fc_run(orig_nodes, monkeypatch, os_value="0.2")["cost_model"]["evaluation_slippage_pct"] == 0.2
    sig = inspect.signature(FC.build_full_chain_component_review)
    assert all(p.kind.name == "KEYWORD_ONLY" for p in sig.parameters.values()) and sig.parameters["cost_profile_path"].default is None


def test_build_full_chain_errors_and_env_seam(orig_nodes, monkeypatch, guards):
    ov = _fc_overrides()
    ov.pop("_loads")
    assert check(orig_nodes, monkeypatch, "build_full_chain_component_review", reports_root=Path("rr"), start=None, end="e", overrides=ov)[0] == "err"
    fake_os = FakeOs("bad")
    ov2 = {**ov, "os": fake_os}
    assert check(orig_nodes, monkeypatch, "build_full_chain_component_review", reports_root=Path("rr"), start="s", end="e", overrides=ov2)[0:2] == ("err", "ValueError")
    assert fake_os.calls and fake_os.calls[0] == ("Q9_EVALUATION_SLIPPAGE_PCT", "0.05")  # env read through the module-level ``os`` at call time

    def boom(**kw):
        raise RuntimeError("loader failure")
    assert check(orig_nodes, monkeypatch, "build_full_chain_component_review", reports_root=Path("rr"), start="s", end="e", overrides={**ov, "load_quant_shadow_candidate_payloads_for_range": boom}) == ("err", "RuntimeError", "loader failure")
    seen = []
    out = check(orig_nodes, monkeypatch, "build_full_chain_component_review", reports_root=Path("rr"), start="s", end="e", cost_profile_path=Path("cp.json"),
                overrides={**ov, "load_broker_cost_profile": lambda path: seen.append(path) or {}, "Q9_ROW_KEYS_UNUSED_BY_FULL_CHAIN": ("zz",)})
    assert seen == [Path("cp.json")] * 2 and out["cost_model"]["conservative_round_trip_cost_pct"] == 0.9 and out["cost_model"]["source"] == "fallback"


# ---- A56-2 _day_from_trade_dir ----
class FakeDir:
    def __init__(self, *parts):
        self.parts = tuple(parts)

    def __repr__(self):
        return f"FakeDir{self.parts!r}"

    def __eq__(self, other):
        return isinstance(other, FakeDir) and self.parts == other.parts

    def __hash__(self):
        return hash(self.parts)

    def __lt__(self, other):
        return self.parts < other.parts

    @property
    def parent(self):
        return FakeDir(*self.parts[:-1])

    def __truediv__(self, part):
        return FakeDir(*self.parts, part)


DIRS = [FakeDir("rr", "trades", "2026-04-10", "t1"), FakeDir("trades", "2026-04-11"), FakeDir("trades"), FakeDir(), FakeDir("a", "b"), FakeDir("trades", "trades", "2026-04-12"), FakeDir("x", "trades", ""), FakeDir("rr", "TRADES", "d"),
        FakeDir("trades", "2026-04-13", "trades", "x"), Path("reports/trades/2026-04-14/t1"), Path("trades"), Path("/")]


@pytest.mark.parametrize("trade_dir", DIRS)
def test_day_from_trade_dir(orig_nodes, monkeypatch, guards, trade_dir):
    check(orig_nodes, monkeypatch, "_day_from_trade_dir", trade_dir)


def test_day_from_trade_dir_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_day_from_trade_dir", FakeDir("rr", "trades", "2026-04-10", "t1")) == "2026-04-10" and check(orig_nodes, monkeypatch, "_day_from_trade_dir", FakeDir("trades")) == ""
    assert check(orig_nodes, monkeypatch, "_day_from_trade_dir", FakeDir("trades", "trades", "d")) == "trades"  # first "trades" component with a successor
    assert check(orig_nodes, monkeypatch, "_day_from_trade_dir", Path("reports/trades/2026-04-14/t1")) == "2026-04-14" and check(orig_nodes, monkeypatch, "_day_from_trade_dir", None)[0] == "err"


# ---- A56-3 _net_return ----
NRS = [{}, None if False else {"realized_outcome": None}, {"realized_outcome": {}}, {"realized_outcome": {"net_return_pct": 1.5}}, {"realized_outcome": {"net_return_pct": "2.5"}}, {"realized_outcome": {"net_return_pct": "x"}},
       {"realized_outcome": {"net_return_pct": None}}, {"realized_outcome": {"net_return_pct": 0}}, {"realized_outcome": {"net_return_pct": NAN}}, {"realized_outcome": {"net_return_pct": []}}, {"realized_outcome": "bad"}, {"realized_outcome": {"net_return_pct": _FloatErr(TypeError)}},
       {"realized_outcome": {"net_return_pct": _FloatErr(ValueError)}}, {"realized_outcome": {"net_return_pct": _FloatErr(RuntimeError)}}, {"realized_outcome": {"net_return_pct": True}}, {"realized_outcome": {"net_return_pct": ""}}]


@pytest.mark.parametrize("evaluation", NRS)
def test_net_return(orig_nodes, monkeypatch, guards, evaluation):
    check(orig_nodes, monkeypatch, "_net_return", evaluation)


def test_net_return_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_net_return", NRS[3]) == 1.5 and check(orig_nodes, monkeypatch, "_net_return", NRS[7]) == 0.0  # a literal 0 return is a value, not None
    assert check(orig_nodes, monkeypatch, "_net_return", {}) is None and check(orig_nodes, monkeypatch, "_net_return", NRS[11]) is None
    assert check(orig_nodes, monkeypatch, "_net_return", NRS[13]) == ("err", "RuntimeError", "custom float failure") and check(orig_nodes, monkeypatch, "_net_return", None)[0] == "err"


# ---- A56-4 _group_metrics ----
GROWS = [[], [("a", 1.0)], [("b", 1.0), ("a", -1.0), ("a", 2.0)], [(None, 1.0), ("", 2.0), (0, 3.0)], [("k", "1.5")], [("k", "x")], [("k", None)], [(1, 1.0), ("1", 2.0)], [("한글", 1.0), ("가", 2.0)], iter([]) if False else (("t", 1.0),), [("z", NAN)]]


@pytest.mark.parametrize("rows", GROWS)
def test_group_metrics(orig_nodes, monkeypatch, guards, rows):
    check(orig_nodes, monkeypatch, "_group_metrics", rows)


def test_group_metrics_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_group_metrics", GROWS[2])
    assert list(out) == ["a", "b"] and out["a"]["count"] == 2  # sorted keys
    assert list(check(orig_nodes, monkeypatch, "_group_metrics", GROWS[3])) == ["unknown"] and check(orig_nodes, monkeypatch, "_group_metrics", GROWS[3])["unknown"]["count"] == 3  # None, "" and 0 all fall into "unknown"
    assert check(orig_nodes, monkeypatch, "_group_metrics", [("k", "x")])[0:2] == ("err", "ValueError") and check(orig_nodes, monkeypatch, "_group_metrics", None)[0] == "err"
    out = check(orig_nodes, monkeypatch, "_group_metrics", GROWS[2], overrides={"performance_metrics": lambda vals: {"n": len(vals)}})
    assert out == {"a": {"n": 2}, "b": {"n": 1}}
    consumed = []

    def gen():
        for r in (("a", 1.0), ("b", 2.0)):
            consumed.append(r)
            yield r
    assert list(HP._group_metrics(gen())) == ["a", "b"] and len(consumed) == 2  # a generator of rows is consumed exactly once


def test_group_metrics_defaultdict_seam(orig_nodes, monkeypatch, guards):
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "_group_metrics", GROWS[2], overrides={"defaultdict": spy})
    assert made == [1, 1]


# ---- A56-5 summarize_historical_prior ----
class FixedNow:
    @staticmethod
    def now(tz):
        class _T:
            def isoformat(self):
                return f"FIXED({tz})"
        return _T()


def _ev(ret=1.0, eligible=True, status="OK", watch=None, defects=None, day="2026-04-10", bucket="swing"):
    return {"realized_outcome": {"net_return_pct": ret}, "integrity": {"promotion_metric_eligible": eligible, "status": status, "watch_items": watch or [], "defects": defects or []}, "day": day, "horizon_alignment": {"bucket": bucket}}


def _md(rank=1, playbook="pb", symbol="005930"):
    return {"selection": {"selected_rank": rank, "strategist_playbook": playbook}, "symbol": symbol}


MODELS = [_md(1), _md(2, "pb2", "000660"), _md(5, None, None), _md("x"), _md(12, "pb", "005930")]
EVALS = [_ev(1.0), _ev(-2.0, eligible=False, status="WARN", watch=["w1", "w2"]), _ev(0.5, defects=["d1"], day="2026-04-11"), _ev(None, bucket=None), _ev("3", day="")]
ATTRS = [{"deltas": {"strategist_delta_pct": 0.3}}, {"deltas": {"strategist_delta_pct": None}}, {"deltas": None}, {}]
SUM_CASES = {"full": (MODELS, EVALS, ATTRS, [{"e": i} for i in range(60)]), "empty": ([], [], [], []), "no_models": ([], EVALS, ATTRS, []), "short_models": (MODELS[:2], EVALS, [], [{"e": 1}]),
             "bad_selection": ([{"selection": "bad", "symbol": "S"}, {}], [_ev(1.0, bucket="b"), _ev(2.0)], [], []), "bad_horizon": (MODELS[:1], [{"realized_outcome": {"net_return_pct": 1}, "horizon_alignment": "bad", "integrity": None}], [], []),
             "no_integrity": ([], [{"realized_outcome": {"net_return_pct": 1}}], [], [])}


@pytest.mark.parametrize("case", list(SUM_CASES))
@pytest.mark.parametrize("window", [("", "2026-06-29"), ("2026-04-01", "2026-04-30")])
def test_summarize_historical_prior(orig_nodes, monkeypatch, guards, case, window):
    models, evals, attrs, errors = SUM_CASES[case]
    check(orig_nodes, monkeypatch, "summarize_historical_prior", models=models, evaluations=evals, attributions=attrs, errors=errors, from_day=window[0], before_day=window[1], overrides={"datetime": FixedNow})


def test_summarize_exact_and_seams(orig_nodes, monkeypatch, guards):
    models, evals, attrs, errors = SUM_CASES["full"]
    out = check(orig_nodes, monkeypatch, "summarize_historical_prior", models=models, evaluations=evals, attributions=attrs, errors=errors, from_day="a", before_day="b", overrides={"datetime": FixedNow})
    assert list(out) == ["schema_version", "behavior_effect", "generated_at", "scope", "coverage", "performance", "breakdowns", "selection_attribution", "interpretation_guardrails", "errors"]
    assert out["generated_at"].startswith("FIXED(") and len(out["errors"]) == 50 and out["coverage"]["build_error_count"] == 60 and out["coverage"]["trade_count"] == 5
    assert out["coverage"]["eligible_trade_count"] == 4 and list(out["breakdowns"]) == ["selected_rank_bucket", "strategist_playbook", "symbol", "horizon_bucket"]
    assert out["selection_attribution"] == {"comparison_count": 1, "unavailable_count": 3, "note": "Historical artifacts often lack Q9-native A/B/C forward controls; use as prior only."}
    assert out["coverage"]["source_days"] == ["2026-04-10", "2026-04-11"] and out["scope"]["official_q9_freeze_sample"] is False
    assert check(orig_nodes, monkeypatch, "summarize_historical_prior", models=None, evaluations=[_ev()], attributions=[], errors=[], from_day="", before_day="b", overrides={"datetime": FixedNow})[0] == "err"
    assert check(orig_nodes, monkeypatch, "summarize_historical_prior", models=[], evaluations=None, attributions=[], errors=[], from_day="", before_day="b", overrides={"datetime": FixedNow})[0] == "err"
    out = check(orig_nodes, monkeypatch, "summarize_historical_prior", models=MODELS[:1], evaluations=EVALS[:1], attributions=[], errors=[], from_day="", before_day="b",
                overrides={"datetime": FixedNow, "_net_return": lambda e: 7.0, "_rank_bucket": lambda r: "RB", "_group_metrics": lambda rows: {"rows": list(rows)}, "performance_metrics": lambda vals: {"n": len(vals)}})
    assert out["breakdowns"]["selected_rank_bucket"] == {"rows": [("RB", 7.0)]} and out["performance"]["eligible"] == {"n": 1}
    assert all(p.kind.name == "KEYWORD_ONLY" for p in inspect.signature(HP.summarize_historical_prior).parameters.values())


def test_summarize_counter_seam(orig_nodes, monkeypatch, guards):
    made = []

    def spy(*a, **k):
        made.append(1)
        return collections.Counter(*a, **k)
    models, evals, attrs, errors = SUM_CASES["full"]
    check(orig_nodes, monkeypatch, "summarize_historical_prior", models=models, evaluations=evals, attributions=attrs, errors=errors, from_day="", before_day="b", overrides={"datetime": FixedNow, "Counter": spy})
    assert made == [1] * 6  # three counters per side


# ---- A56-6 render_historical_prior_markdown ----
RP = {"scope": {"from_day": "2026-04-01", "before_day": "2026-06-29"}, "coverage": {"source_day_count": 5, "trade_count": 20, "eligible_trade_count": 15, "build_error_count": 2, "integrity_status_counts": {"OK": 18, "WARN": 2}},
      "performance": {"eligible": {"count": 15, "win_rate": 0.4, "average_return_pct": -0.123456, "profit_factor": 0.7, "maximum_drawdown_pct": -5.5}, "all_realized": {"count": 20, "average_return_pct": 0.1}},
      "breakdowns": {"selected_rank_bucket": {"rank1": {"count": 5, "win_rate": 0.6, "average_return_pct": 0.5, "profit_factor": 1.5}, "unknown": {}}, "strategist_playbook": {}, "horizon_bucket": {"한글": {"count": 1}}}}
RPS = [{}, RP, {**RP, "scope": {"from_day": "", "before_day": None}}, {**RP, "breakdowns": None, "performance": None, "coverage": None}, {**RP, "breakdowns": {"selected_rank_bucket": "bad", "strategist_playbook": None}},
       {**RP, "performance": {"eligible": {"win_rate": "bad"}}}, {"scope": {"from_day": "x"}}]


@pytest.mark.parametrize("payload", RPS)
def test_render_historical_prior_markdown(orig_nodes, monkeypatch, guards, payload):
    out = check(orig_nodes, monkeypatch, "render_historical_prior_markdown", payload)
    assert (isinstance(out, str) and not out.endswith("\n\n\n")) or out[0] == "err"


def test_render_historical_prior_exact(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_historical_prior_markdown", RP)
    assert out.startswith("# Historical Q9 Prior\n\n- Scope: `2026-04-01` to before `2026-06-29`\n- Behavior effect: read-only historical prior\n") and "- Eligible win rate: 40.0%\n" in out and "- Eligible average return: -0.1235%\n" in out
    assert "- rank1: count 5, win 60.0%, avg 0.5000%, PF 1.5\n- unknown: count 0, win 0.0%, avg 0.0000%, PF 0\n" in out and "### strategist_playbook\n- No comparable rows\n\n" in out and "- 한글: count 1" in out
    assert out.endswith("- Monday Q9 close remains the authoritative decision point; this report is a tie-breaker and root-cause prior.\n")
    empty = check(orig_nodes, monkeypatch, "render_historical_prior_markdown", {})
    assert "`beginning` to before `None`" in empty and check(orig_nodes, monkeypatch, "render_historical_prior_markdown", None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "render_historical_prior_markdown", RPS[5])[0:2] == ("err", "ValueError")


# ---- A56-7 iter_historical_trade_dirs (fake Path) ----
class FakeFile:
    def __init__(self, parent):
        self.parent = parent


class FakeTrades:
    def __init__(self, exists, bundles):
        self._exists, self._bundles, self.globs = exists, bundles, []

    def __repr__(self):
        return f"FakeTrades({self._exists},{self._bundles!r})"

    def exists(self):
        return self._exists

    def rglob(self, pattern):
        self.globs.append(pattern)
        return [FakeFile(b) for b in self._bundles]


class FakeRootPath:
    def __init__(self, trades):
        self.trades = trades

    def __repr__(self):
        return f"FakeRootPath({self.trades!r})"

    def __truediv__(self, part):
        assert part == "trades"
        return self.trades


def _fake_path_factory(trades):
    seen = []

    class FakePathCls:
        def __new__(cls, value):
            seen.append(value)
            return FakeRootPath(trades)
    FakePathCls.seen = seen
    return FakePathCls


B1, B2, B3, B4 = FakeDir("trades", "2026-04-09", "t1"), FakeDir("trades", "2026-04-10", "t1"), FakeDir("trades", "2026-04-10", "t2"), FakeDir("trades", "2026-06-29", "t9")
BUNDLES = [B3, B1, B2, B2, B4, FakeDir("elsewhere", "x"), FakeDir("trades")]


@pytest.mark.parametrize("exists", [True, False])
@pytest.mark.parametrize("window", ["omit", ("", "2026-06-29"), ("2026-04-10", "2026-06-29"), ("2026-04-10", ""), ("", ""), ("2026-04-09", "2026-04-10")])
def test_iter_historical_trade_dirs(orig_nodes, monkeypatch, guards, exists, window):
    trades = FakeTrades(exists, BUNDLES)
    kw = {} if window == "omit" else {"from_day": window[0], "before_day": window[1]}
    out = check(orig_nodes, monkeypatch, "iter_historical_trade_dirs", "root", overrides={"Path": _fake_path_factory(trades)}, **kw)
    assert isinstance(out, list)


def test_iter_historical_trade_dirs_exact_and_seams(orig_nodes, monkeypatch, guards):
    trades = FakeTrades(True, BUNDLES)
    ov = {"Path": _fake_path_factory(trades)}
    out = check(orig_nodes, monkeypatch, "iter_historical_trade_dirs", "root", overrides=ov)
    assert out == [B1, B2, B3] and trades.globs == ["lifecycle_bundle.json"] * 2  # sorted, deduplicated parents; day >= default before_day excluded; folders without a day skipped
    assert check(orig_nodes, monkeypatch, "iter_historical_trade_dirs", "root", from_day="2026-04-10", before_day="2026-04-10", overrides=ov) == []
    assert check(orig_nodes, monkeypatch, "iter_historical_trade_dirs", "root", before_day="", overrides=ov) == [B1, B2, B3, B4]  # empty before_day disables the upper bound
    assert check(orig_nodes, monkeypatch, "iter_historical_trade_dirs", "root", overrides={"Path": _fake_path_factory(FakeTrades(False, BUNDLES))}) == []
    sig = inspect.signature(HP.iter_historical_trade_dirs)
    assert sig.parameters["before_day"].default == HP.DEFAULT_BEFORE_DAY == "2026-06-29" and sig.parameters["from_day"].default == "" and [p.kind.name for p in sig.parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY", "KEYWORD_ONLY"]
    out = check(orig_nodes, monkeypatch, "iter_historical_trade_dirs", "root", overrides={**ov, "_day_from_trade_dir": lambda p: "2026-01-01"})
    assert len(out) == 6  # helper resolved at call time: every distinct bundle parent now passes the day filter


def test_iter_historical_trade_dirs_default_bound_at_definition_time(monkeypatch, guards):
    monkeypatch.setattr(HP, "DEFAULT_BEFORE_DAY", "1999-01-01")
    trades = FakeTrades(True, BUNDLES)
    monkeypatch.setattr(HP, "Path", _fake_path_factory(trades))
    assert HP.iter_historical_trade_dirs("root") == [B1, B2, B3]  # default stays the definition-time constant, exactly as before


# ---- A56-8 _load_trade_models ----
def _loader_fakes(days=("2026-04-10", "2026-04-11"), dirs=None):
    seen = []
    dirs = dirs if dirs is not None else {"2026-04-10": ["a", "b"], "2026-04-11": []}

    def iter_days(start, end):
        seen.append(("days", start, end))
        return iter(days)

    def iter_dirs(root, day):
        seen.append(("dirs", str(root), day))
        return iter(dirs.get(day, ["z"]))

    def model(path):
        seen.append(("model", path))
        return {"trade": path}
    return {"_iter_days": iter_days, "iter_trade_dirs": iter_dirs, "build_q9_trade_read_model": model}, seen


@pytest.mark.parametrize("days", [(), ("2026-04-10",), ("2026-04-10", "2026-04-11"), ("2026-04-12", "2026-04-10")])
def test_load_trade_models(orig_nodes, monkeypatch, guards, days):
    ov, seen = _loader_fakes(days)
    check(orig_nodes, monkeypatch, "_load_trade_models", "rr", "s", "e", overrides=ov)
    half = len(seen) // 2
    assert half * 2 == len(seen) and seen[:half] == seen[half:]


def test_load_trade_models_exact_order_errors_and_seams(orig_nodes, monkeypatch, guards):
    ov, seen = _loader_fakes()
    out = check(orig_nodes, monkeypatch, "_load_trade_models", "rr", "s", "e", overrides=ov)
    assert out == [{"trade": "a"}, {"trade": "b"}] and [e[0] for e in seen[: len(seen) // 2]] == ["days", "dirs", "model", "model", "dirs"]  # per-day interleaving, lazily consumed in order
    assert check(orig_nodes, monkeypatch, "_load_trade_models", "rr", "s", "e", overrides=_loader_fakes(days=())[0]) == []
    ov2, _ = _loader_fakes()

    def bad_model(path):
        raise RuntimeError("model failure")
    assert check(orig_nodes, monkeypatch, "_load_trade_models", "rr", "s", "e", overrides={**ov2, "build_q9_trade_read_model": bad_model}) == ("err", "RuntimeError", "model failure")
    ov3, _ = _loader_fakes()

    def bad_days(start, end):
        raise ValueError("bad range")
    assert check(orig_nodes, monkeypatch, "_load_trade_models", "rr", "s", "e", overrides={**ov3, "_iter_days": bad_days}) == ("err", "ValueError", "bad range")


def test_load_trade_models_real_iter_days_helper(orig_nodes, monkeypatch, guards):
    real = check(orig_nodes, monkeypatch, "_load_trade_models", "rr", "2026-04-10", "2026-04-11", overrides={"iter_trade_dirs": lambda root, day: [f"{day}/t"], "build_q9_trade_read_model": lambda p: {"p": p}})
    assert real == [{"p": "2026-04-10/t"}, {"p": "2026-04-11/t"}]  # real _iter_days helper, fake collaborators
    assert check(orig_nodes, monkeypatch, "_load_trade_models", "rr", "bad", "bad", overrides={"iter_trade_dirs": lambda r, d: [], "build_q9_trade_read_model": lambda p: p})[0:2] == ("err", "ValueError")


# ---- structure ----
@pytest.mark.parametrize("name", list(SPEC))
def test_wrapper_thin_and_owner_holds_body(name):
    mod = MODS[SPEC[name][0]]
    fname = SPEC[name][3]
    wrapper = ast.parse(inspect.getsource(getattr(mod, fname))).body[0]
    stmts = [n for n in wrapper.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Constant))]
    assert len(stmts) == 1 and isinstance(stmts[0], ast.Return)
    assert not [n for n in ast.walk(wrapper) if isinstance(n, (ast.If, ast.For, ast.Try, ast.ListComp, ast.GeneratorExp))]
    call = stmts[0].value
    assert isinstance(call, ast.Call) and "facade" in [k.arg for k in call.keywords], "wrapper must forward to the Owner with facade="
    owner_fn = getattr(OWNERS[name], fname)
    node = ast.parse(inspect.getsource(owner_fn)).body[0]
    assert len(node.body) >= 1 and owner_fn.__module__ == OWNERS[name].__name__
    src = inspect.getsource(OWNERS[name])
    stem = SPEC[name][0]
    assert f"import {stem}" not in src and f"{stem} import" not in src.replace("from . import", "") and f"from .{stem} " not in src
