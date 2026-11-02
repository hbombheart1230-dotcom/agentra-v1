"""RF-032 A55-1..8: ``scanner_quality`` / ``scanner_alignment_root_cause`` / ``no_trade_attribution`` / ``historical_prior`` read-only builder and loader bodies, original vs thin wrappers + Owners.

Original = A preimage 7d1dcb8b (SOURCE blobs 26a5eedd / b46c7569 / 59126f3b / 6adbc1e9 == canonical 15207cf4). Each original function is compiled from
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

A_PRE = "7d1dcb8b55ea98b52fc4bcbdacf4aaaa0d9eeca1"
CANON = "15207cf47e3b1b447545f5948a73eed3801f1e9d"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "sq_pre": ("scanner_quality", "26a5eedd4adb46308a715256a791bd6f1a0c4d05", "scanner_quality_pre_strategist_candidate_rows", "pre_strategist_candidate_rows"),
    "sar_build": ("scanner_alignment_root_cause", "b46c7569ab1cd3730193642d1e93f80f9035590d", "scanner_alignment_root_cause_build_scanner_alignment_root_cause_report", "build_scanner_alignment_root_cause_report"),
    "sar_load": ("scanner_alignment_root_cause", "b46c7569ab1cd3730193642d1e93f80f9035590d", "scanner_alignment_root_cause_load_day_models_and_evaluations", "_load_day_models_and_evaluations"),
    "sar_range": ("scanner_alignment_root_cause", "b46c7569ab1cd3730193642d1e93f80f9035590d", "scanner_alignment_root_cause_build_scanner_alignment_root_cause_range", "build_scanner_alignment_root_cause_range"),
    "nt_build": ("no_trade_attribution", "59126f3b2695c52b3b5339f4488e5946c3f278ab", "no_trade_attribution_build_no_trade_attribution_report", "build_no_trade_attribution_report"),
    "nt_read_json": ("no_trade_attribution", "59126f3b2695c52b3b5339f4488e5946c3f278ab", "no_trade_attribution_read_json", "_read_json"),
    "sar_read_json": ("scanner_alignment_root_cause", "b46c7569ab1cd3730193642d1e93f80f9035590d", "scanner_alignment_root_cause_read_json", "_read_json"),
    "hp_rank_bucket": ("historical_prior", "6adbc1e96e1fd160c5efcd9e7e7704c300c32c20", "historical_prior_rank_bucket", "_rank_bucket"),
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
import json as _json

SQ = MODS["scanner_quality"]
SAR = MODS["scanner_alignment_root_cause"]
NT = MODS["no_trade_attribution"]
HP = MODS["historical_prior"]


class NeverMapping:
    pass


class _FloatErr:
    def __init__(self, exc):
        self.exc = exc

    def __repr__(self):
        return f"_FloatErr({self.exc.__name__})"

    def __float__(self):
        raise self.exc("custom float failure")


# ---- A55-1 pre_strategist_candidate_rows ----
def _extract(rows):
    log = []

    def extract(payloads):
        log.append(copy.deepcopy(payloads))
        return copy.deepcopy(rows)
    extract.log = log
    return extract


def _attach():
    log = []

    def attach(rows, **kw):
        log.append((copy.deepcopy(rows), copy.deepcopy(kw)))
        return [{**r, "attached": True} for r in rows]
    attach.log = log
    return attach


@pytest.mark.parametrize("rows", [[], [{"a": 1}], [{"a": 1}, {"a": 1}]])
@pytest.mark.parametrize("minute_rows", ["omit", None, {}, {"005930": [{"ts": 1}]}])
def test_pre_strategist_candidate_rows(orig_nodes, monkeypatch, guards, rows, minute_rows):
    extract, attach = _extract(rows), _attach()
    kw = {} if minute_rows == "omit" else {"minute_rows_by_symbol": minute_rows}
    out = check(orig_nodes, monkeypatch, "sq_pre", [{"p": 1}], overrides={"extract_pre_strategist_candidate_rows": extract, "attach_forward_outcomes": attach}, **kw)
    half = len(attach.log) // 2
    assert half * 2 == len(attach.log) and attach.log[:half] == attach.log[half:] and extract.log[: len(extract.log) // 2] == extract.log[len(extract.log) // 2:]
    assert isinstance(out, list) and all(r["attached"] for r in out)


def test_pre_strategist_candidate_rows_none_vs_supplied(orig_nodes, monkeypatch, guards):
    extract, attach = _extract([{"a": 1}]), _attach()
    ov = {"extract_pre_strategist_candidate_rows": extract, "attach_forward_outcomes": attach}
    check(orig_nodes, monkeypatch, "sq_pre", [], overrides=ov)
    check(orig_nodes, monkeypatch, "sq_pre", [], minute_rows_by_symbol={"A": []}, overrides=ov)
    assert [kw for _, kw in attach.log] == [{}, {}, {"minute_rows_by_symbol": {"A": []}}, {"minute_rows_by_symbol": {"A": []}}]  # None omits the keyword; supplied maps (even empty) are forwarded
    assert [p.kind.name for p in inspect.signature(SQ.pre_strategist_candidate_rows).parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY"]

    def boom(rows, **kw):
        raise RuntimeError("attach failure")
    assert check(orig_nodes, monkeypatch, "sq_pre", [], overrides={**ov, "attach_forward_outcomes": boom}) == ("err", "RuntimeError", "attach failure")

    def bad_extract(payloads):
        raise ValueError("extract failure")
    assert check(orig_nodes, monkeypatch, "sq_pre", [], overrides={**ov, "extract_pre_strategist_candidate_rows": bad_extract}) == ("err", "ValueError", "extract failure")


def test_pre_strategist_candidate_rows_real_extract_helper(orig_nodes, monkeypatch, guards):
    real = check(orig_nodes, monkeypatch, "sq_pre", [{"q9_decision_candidates": [{"q9_decision_role": "P_SCANNER_PRE_STRATEGIST_UNIVERSE", "q9_decision_id": "D", "symbol": "A", "rank": 1}]}], overrides={"attach_forward_outcomes": lambda rows, **kw: rows})
    assert len(real) == 1 and real[0]["symbol"] == "A"  # real extract helper, fake attach


# ---- A55-2 build_scanner_alignment_root_cause_report ----
def _srow(tid="T1", raw="A", post="A", sel="A", exe="A", f2e=None, **extra):
    return {"trade_id": tid, "raw_scanner_top1": raw, "post_strategy_top1": post, "selected_symbol": sel, "executed_symbol": exe, "final_to_executed_changed": f2e, **extra}


def _mdl(tid, rank=1, top=None, sel=None, ret=None):
    s = {"selected_rank": rank}
    if top is not None:
        s["scanner_top1"] = {"score_total": top}
    if sel is not None:
        s["selected_candidate"] = {"score_total": sel}
    m = {"trade_id": tid, "selection": s}
    if ret is not None:
        m["outcome"] = {"net_return_pct": ret}
    return m


def _evl(tid, ret):
    return {"trade_id": tid, "realized_outcome": {"net_return_pct": ret}}


SAUTH = {"rows": [_srow("T1"), _srow("T2", sel="B", exe="B", f2e=True), _srow("T3", raw="X", post="A", sel="A"), _srow("T4", sel="B", exe="B"), _srow("T5", raw="", post=""), _srow("T6"), _srow("T7", symbol="Z"), "bad", None, _srow("")]}
SMODELS = [_mdl("T1", 1, 5, 5, ret=-1.0), _mdl("T2", 1), _mdl("T3", 1), _mdl("T4", 3, 9, 4), _mdl("T6", 1, ret=2.0)]
SEVALS = [_evl("T1", -2.0), _evl("T6", None), _evl("T3", 0.5)]
SCASES = {"empty": ([], [], {}), "no_rows": ([], [], {"rows": []}), "rows_bad": ([], [], {"rows": "bad"}), "full": (SMODELS, SEVALS, SAUTH), "no_models": ([], SEVALS, SAUTH), "no_evals": (SMODELS, [], SAUTH),
          "dupe_trade_ids": (SMODELS + [_mdl("T1", 2)], SEVALS + [_evl("T1", 9.0)], SAUTH), "bad_return": (SMODELS, [_evl("T1", "x")], {"rows": [_srow("T1")]}), "models_with_none_ids": ([{"selection": {}}], [{}], {"rows": [_srow("")]})}


@pytest.mark.parametrize("case", list(SCASES))
def test_build_scanner_alignment_root_cause_report(orig_nodes, monkeypatch, guards, case):
    models, evals, auth = SCASES[case]
    check(orig_nodes, monkeypatch, "sar_build", day="2026-04-10", models=models, evaluations=evals, selection_authority=auth)


def test_build_scanner_alignment_report_exact_and_seams(orig_nodes, monkeypatch, guards):
    models, evals, auth = SCASES["full"]
    out = check(orig_nodes, monkeypatch, "sar_build", day="2026-04-10", models=models, evaluations=evals, selection_authority=auth)
    assert list(out) == ["schema_version", "measurement_contract_version", "evaluation_program_id", "behavior_effect", "day", "trade_count", "cause_summary", "largest_root_cause", "largest_observed_root_cause",
                         "largest_behavior_root_cause", "largest_structural_root_cause", "outcome_conditioned_causes", "q15_behavior_patch_candidate", "rows", "interpretation_rule"]
    assert out["trade_count"] == 8 and [c["root_cause"] for c in out["cause_summary"]] == list(SAR.ROOT_CAUSES)
    assert out["largest_root_cause"] == out["largest_observed_root_cause"]
    assert out["outcome_conditioned_causes"] == sorted(SAR.OUTCOME_CONDITIONED_CAUSES) and list(out["rows"][0]) == ["trade_id", "symbol", "raw_scanner_top1", "post_strategy_top1", "selected_symbol", "executed_symbol", "net_return_pct",
                                                                                                                       "root_cause", "diagnostic_kind", "causal_eligible", "confidence", "selected_rank", "score_gap", "reasons"]
    assert out["rows"][0]["net_return_pct"] == -2.0  # evaluation wins over the model outcome
    assert out["rows"][1]["root_cause"] == "Symbol Mapping" and out["rows"][-1]["trade_id"] == ""
    assert [p.kind.name for p in inspect.signature(SAR.build_scanner_alignment_root_cause_report).parameters.values()] == ["KEYWORD_ONLY"] * 4
    assert check(orig_nodes, monkeypatch, "sar_build", day="d", models=None, evaluations=[], selection_authority={})[0] == "err"
    assert check(orig_nodes, monkeypatch, "sar_build", day="d", models=[], evaluations=[], selection_authority=None)[0] == "err"
    out = check(orig_nodes, monkeypatch, "sar_build", day="d", models=[], evaluations=[], selection_authority={"rows": [_srow("T1")]},
                overrides={"classify_scanner_alignment_root_cause": lambda *, row, model, net_return_pct: {"root_cause": "Rank Drift", "confidence": "low", "selected_rank": 7, "score_gap": 0.5, "reasons": ["fake"]},
                           "_patch_candidate": lambda cause: f"PATCH({cause})", "performance_metrics": lambda vals: {"win_rate": 0.1, "average_return_pct": 0.2, "profit_factor": 0.3, "maximum_drawdown_pct": 0.4}})
    assert out["rows"][0]["confidence"] == "low" and out["q15_behavior_patch_candidate"].startswith("PATCH(")
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "sar_build", day="d", models=[], evaluations=[], selection_authority={"rows": [_srow("T1")]}, overrides={"defaultdict": spy})
    assert made == [1, 1]


# ---- A55-3 _load_day_models_and_evaluations (fake directory objects, no real FS) ----
class FakeEntry:
    def __init__(self, name, is_dir=True):
        self.name, self._dir = name, is_dir

    def __repr__(self):
        return f"FakeEntry({self.name!r},{self._dir})"

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return isinstance(other, FakeEntry) and self.name == other.name and self._dir == other._dir

    def __hash__(self):
        return hash((self.name, self._dir))

    def is_dir(self):
        return self._dir

    def __truediv__(self, part):
        return FakeEntry(f"{self.name}/{part}", False)


class FakeRoot:
    def __init__(self, entries=None, exists=True, trail=""):
        self.entries, self._exists, self.trail = entries or [], exists, trail

    def __repr__(self):
        return f"FakeRoot({self.trail!r},{[e.name for e in self.entries]},{self._exists})"

    def __truediv__(self, part):
        return FakeRoot(self.entries, self._exists, f"{self.trail}/{part}")

    def exists(self):
        return self._exists

    def iterdir(self):
        return iter(list(self.entries))


def _fake_json(mapping):
    calls = []

    def read(path):
        calls.append(path.name)
        return copy.deepcopy(mapping.get(path.name, {}))
    read.calls = calls
    return read


TRADES = {"d1/trade_read_model.json": {"id": "m1"}, "d1/trade_evaluation.json": {"id": "e1"}, "d2/trade_read_model.json": {"id": "m2"}, "d2/trade_evaluation.json": {},
          "d3/trade_read_model.json": {}, "d3/trade_evaluation.json": {"id": "e3"}, "d4/trade_read_model.json": {}, "d4/trade_evaluation.json": {}}


@pytest.mark.parametrize("entries,exists", [([], True), ([FakeEntry("d2"), FakeEntry("d1"), FakeEntry("d4"), FakeEntry("d3")], True), ([FakeEntry("d1"), FakeEntry("file", False)], True), ([FakeEntry("d1")], False), ([FakeEntry("d3"), FakeEntry("d2")], True)])
def test_load_day_models_and_evaluations(orig_nodes, monkeypatch, guards, entries, exists):
    read = _fake_json(TRADES)
    check(orig_nodes, monkeypatch, "sar_load", FakeRoot(entries, exists), "2026-04-10", overrides={"_read_json": read})
    half = len(read.calls) // 2
    assert half * 2 == len(read.calls) and read.calls[:half] == read.calls[half:]


def test_load_day_models_and_evaluations_exact_and_errors(orig_nodes, monkeypatch, guards):
    entries = [FakeEntry("d2"), FakeEntry("d1"), FakeEntry("d4"), FakeEntry("d3"), FakeEntry("skipme", False)]
    out = check(orig_nodes, monkeypatch, "sar_load", FakeRoot(entries), "d", overrides={"_read_json": _fake_json(TRADES)})
    assert out == ([{"id": "m1"}, {"id": "m2"}], [{"id": "e1"}, {"id": "e3"}])  # sorted by directory, falsy payloads skipped, non-dirs ignored
    assert check(orig_nodes, monkeypatch, "sar_load", FakeRoot(entries, exists=False), "d", overrides={"_read_json": _fake_json(TRADES)}) == ([], [])
    read = _fake_json(TRADES)
    check(orig_nodes, monkeypatch, "sar_load", FakeRoot([FakeEntry("d1")]), "2026-04-10", overrides={"_read_json": read})
    assert read.calls == ["d1/trade_read_model.json", "d1/trade_evaluation.json"] * 2  # model first, then evaluation, per trade dir
    assert check(orig_nodes, monkeypatch, "sar_load", None, "d", overrides={"_read_json": _fake_json({})})[0] == "err"

    def boom(path):
        raise RuntimeError("read failure")
    assert check(orig_nodes, monkeypatch, "sar_load", FakeRoot([FakeEntry("d1")]), "d", overrides={"_read_json": boom}) == ("err", "RuntimeError", "read failure")


# ---- A55-4 build_scanner_alignment_root_cause_range ----
def _range_fakes(auth_by_day=None, dirs_by_day=None):
    seen = []
    auth_by_day = auth_by_day or {}
    dirs_by_day = dirs_by_day or {}

    def read(path):
        seen.append(("read", str(path)))
        return copy.deepcopy(auth_by_day.get(path.parts[-2], {}))

    def load(root, day):
        seen.append(("load", day))
        return copy.deepcopy(dirs_by_day.get(day, ([], [])))

    def build(*, day, models, evaluations, selection_authority):
        seen.append(("build", day))
        return {"day": day, "rows": [{"root_cause": "Rank Drift", "net_return_pct": -1.0, "trade_id": f"{day}-{i}"} for i in range(len(selection_authority.get("rows") or [1]))]}
    return read, load, build, seen


RANGE_CASES = {"single_empty": ("2026-04-10", "2026-04-10", {}, {}), "three_days": ("2026-04-10", "2026-04-12", {"2026-04-10": {"rows": [1]}, "2026-04-12": {"rows": [1, 2]}}, {"2026-04-11": ([{"m": 1}], [])}),
               "reversed": ("2026-04-12", "2026-04-10", {"2026-04-10": {"rows": [1]}}, {}), "month_boundary": ("2026-04-30", "2026-05-02", {"2026-05-01": {"rows": [1]}}, {}), "leap": ("2024-02-28", "2024-03-01", {"2024-02-29": {"rows": [1]}}, {})}


@pytest.mark.parametrize("case", list(RANGE_CASES))
def test_build_scanner_alignment_root_cause_range(orig_nodes, monkeypatch, guards, case):
    start, end, auth, dirs = RANGE_CASES[case]
    read, load, build, seen = _range_fakes(auth, dirs)
    check(orig_nodes, monkeypatch, "sar_range", reports_root=Path("rr"), start=start, end=end, overrides={"_read_json": read, "_load_day_models_and_evaluations": load, "build_scanner_alignment_root_cause_report": build})
    half = len(seen) // 2
    assert half * 2 == len(seen) and seen[:half] == seen[half:]


def test_build_scanner_alignment_range_exact_errors_and_seams(orig_nodes, monkeypatch, guards):
    start, end, auth, dirs = RANGE_CASES["three_days"]
    read, load, build, seen = _range_fakes(auth, dirs)
    ov = {"_read_json": read, "_load_day_models_and_evaluations": load, "build_scanner_alignment_root_cause_report": build}
    out = check(orig_nodes, monkeypatch, "sar_range", reports_root=Path("rr"), start=start, end=end, overrides=ov)
    assert [e for e in seen[: len(seen) // 2] if e[0] == "build"] == [("build", "2026-04-10"), ("build", "2026-04-11"), ("build", "2026-04-12")]  # inclusive iteration, days with evidence only
    assert seen[0] == ("read", str(Path("rr") / "evaluation" / "daily" / "2026-04-10" / "selection_authority_audit.json"))
    assert list(out)[:7] == ["schema_version", "evaluation_program_id", "behavior_effect", "start", "end", "day_count", "trade_count"] and out["day_count"] == 3 and out["trade_count"] == 4  # 1 + 1 + 2 rows from the fake daily builder
    assert [r["day"] for r in out["daily_rows"]] == ["2026-04-10", "2026-04-11", "2026-04-12"] and out["start"] == start and out["end"] == end
    reversed_out = check(orig_nodes, monkeypatch, "sar_range", reports_root=Path("rr"), start="2026-04-12", end="2026-04-10", overrides=ov)
    assert reversed_out["day_count"] == 0 and reversed_out["trade_count"] == 0 and reversed_out["daily_rows"] == []  # a reversed range iterates nothing
    assert check(orig_nodes, monkeypatch, "sar_range", reports_root=Path("rr"), start="bad", end="2026-04-10", overrides=ov)[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, "sar_range", reports_root=Path("rr"), start="2026-04-10", end="bad", overrides=ov)[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, "sar_range", reports_root=Path("rr"), start=None, end="2026-04-10", overrides=ov)[0] == "err"
    sig = inspect.signature(SAR.build_scanner_alignment_root_cause_range)
    assert all(p.kind.name == "KEYWORD_ONLY" for p in sig.parameters.values()) and sig.parameters["reports_root"].default == Path("reports")


def test_build_scanner_alignment_range_path_seam(orig_nodes, monkeypatch, guards):
    paths = []

    class FakePathFactory:
        def __new__(cls, value):
            paths.append(value)
            return Path(value)
    read, load, build, seen = _range_fakes({}, {})
    check(orig_nodes, monkeypatch, "sar_range", reports_root="plain-string-root", start="2026-04-10", end="2026-04-10", overrides={"_read_json": read, "_load_day_models_and_evaluations": load, "build_scanner_alignment_root_cause_report": build, "Path": FakePathFactory})
    assert paths == ["plain-string-root", "plain-string-root"]  # Path(...) is resolved on the module at call time


# ---- A55-5 build_no_trade_attribution_report ----
def _win(decision="approve", intent="NOOP", reason="r", detail="d", monitor_reason=None, scanner="A", strategist="B", selected="C", obs_reason=None):
    commander = {"decision": decision, "monitor_intent": intent, "reason": reason, "detail": detail, "selected_symbol": selected}
    if monitor_reason is not None:
        commander["monitor_reason"] = monitor_reason
    if obs_reason is not None:
        commander["monitor_observation"] = {"reason": obs_reason}
    return {"scanner_control": {"top1_symbol": scanner}, "strategist_selection": {"selected_symbol": strategist}, "commander_final": commander}


def _q11(avail=True, trades=3, net=0.5, mfe=1.0):
    return {"available": avail, "virtual_trades": trades, "avg_net_return_pct": net, "avg_mfe_pct": mfe}


NTW = {"none": [], "approve_noop": [_win(), _win(detail="x" * 200, monitor_reason="mr"), _win(obs_reason="obs")], "approve_buy": [_win(intent="BUY"), _win(intent="BUY")], "reject": [_win(decision="reject", intent="")],
       "mixed": [_win(), _win(intent="BUY"), _win(decision="reject", intent="NOOP", monitor_reason="m2"), _win(scanner="", strategist="", selected="")], "malformed": [{}, {"commander_final": "bad"}, {"scanner_control": None}],
       "noop_no_reason": [_win(intent="NOOP")], "long_detail": [_win(detail="d" * 400)]}


def _nt_ov(windows, q11):
    return {"_q9_windows": lambda root, day: copy.deepcopy(windows), "_q11_opening": lambda root, day: copy.deepcopy(q11), "_baseline_samsung": lambda root, day: {"s": day}, "_q12_btc_woori": lambda root, day: {"q": day}}


@pytest.mark.parametrize("wcase", list(NTW))
@pytest.mark.parametrize("q11", [_q11(), _q11(trades=0), _q11(net=-0.1, mfe=0.5), _q11(net=-0.1, mfe=-0.5), _q11(net=None, mfe=None), _q11(False), {}, _q11(net="bad")])
@pytest.mark.parametrize("trades", [0, 2, -1])
def test_build_no_trade_attribution_report(orig_nodes, monkeypatch, guards, wcase, q11, trades):
    check(orig_nodes, monkeypatch, "nt_build", day="2026-04-10", reports_root=Path("rr"), trade_count=trades, overrides=_nt_ov(NTW[wcase], q11))


def test_build_no_trade_attribution_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "nt_build", day="d", reports_root=Path("rr"), trade_count=0, overrides=_nt_ov(NTW["approve_noop"], _q11()))
    assert list(out) == ["schema_version", "behavior_effect", "day", "trade_count", "q9_window_count", "no_trade_class", "primary_issue", "commander_approve_monitor_noop_count", "commander_approve_monitor_buy_count",
                         "commander_decisions", "commander_reasons", "commander_details", "monitor_intents", "monitor_noop_reasons", "scanner_top1", "strategist_selected", "commander_selected", "shadow_opportunity_status",
                         "q10_samsung_hynix", "q11_opening_opportunity", "q12_btc_woori", "interpretation"]
    assert out["no_trade_class"] == "POSSIBLE_OVER_FILTERING" and out["primary_issue"] == "positive_net_shadow_blocked_after_commander_approval" and out["shadow_opportunity_status"] == "POSITIVE_NET_SHADOW"
    assert out["commander_approve_monitor_noop_count"] == 3 and [r["name"] for r in out["monitor_noop_reasons"]] == ["mr", "obs"] and len(out["commander_details"][0]["name"]) <= 160
    expect = {("none", 0): "MISSING_Q9_EVIDENCE", ("reject", 0): "UPSTREAM_REJECTED", ("approve_buy", 0): "NO_ACTIONABLE_CANDIDATE", ("approve_noop", 2): "NOT_NO_TRADE_DAY"}
    for (wcase, trades), cls in expect.items():
        assert check(orig_nodes, monkeypatch, "nt_build", day="d", reports_root=Path("rr"), trade_count=trades, overrides=_nt_ov(NTW[wcase], _q11()))["no_trade_class"] == cls
    assert check(orig_nodes, monkeypatch, "nt_build", day="d", reports_root=Path("rr"), trade_count=0, overrides=_nt_ov(NTW["approve_noop"], _q11(net=-1.0)))["no_trade_class"] == "FILTERING_REVIEW_REQUIRED"
    shadow = {"NO_SHADOW_TRADES": _q11(trades=0), "MFE_ONLY_SHADOW": _q11(net=-1.0, mfe=1.0), "NEGATIVE_SHADOW": _q11(net=-1.0, mfe=-1.0), "UNAVAILABLE": _q11(False)}
    for name, q in shadow.items():
        assert check(orig_nodes, monkeypatch, "nt_build", day="d", reports_root=Path("rr"), trade_count=1, overrides=_nt_ov([], q))["shadow_opportunity_status"] == name
    assert check(orig_nodes, monkeypatch, "nt_build", day="d", reports_root=Path("rr"), trade_count="x", overrides=_nt_ov([], {}))[0:2] == ("err", "TypeError")
    assert check(orig_nodes, monkeypatch, "nt_build", day="d", reports_root=None, trade_count=0, overrides=_nt_ov([], {}))[0:2] == ("err", "TypeError")  # Path(None)
    assert all(p.kind.name == "KEYWORD_ONLY" for p in inspect.signature(NT.build_no_trade_attribution_report).parameters.values())
    made = []

    def spy(*a, **k):
        made.append(1)
        return collections.Counter(*a, **k)
    check(orig_nodes, monkeypatch, "nt_build", day="d", reports_root=Path("rr"), trade_count=0, overrides={**_nt_ov([], {}), "Counter": spy})
    assert made == [1] * 16  # eight counters per side, resolved at call time


# ---- A55-6 / A55-7 _read_json (fake path objects, no real file) ----
class FakeReadPath:
    def __init__(self, result=None, exc=None, text=None):
        self.result, self.exc, self.text, self.calls = result, exc, text, []

    def __repr__(self):
        return f"FakeReadPath({self.text!r},{self.exc!r})"

    def read_text(self, encoding=None):
        if self.exc:
            raise self.exc
        return self.text


READ_CASES = [FakeReadPath(text='{"a": 1, "b": [1, 2]}'), FakeReadPath(text="[1, 2]"), FakeReadPath(text="null"), FakeReadPath(text='"str"'), FakeReadPath(text="{bad json"), FakeReadPath(text=""),
              FakeReadPath(text='{"한글": "값"}'), FakeReadPath(exc=FileNotFoundError("missing")), FakeReadPath(exc=PermissionError("denied")), FakeReadPath(exc=UnicodeDecodeError("utf-8", b"\xff", 0, 1, "bad")),
              FakeReadPath(exc=RuntimeError("custom")), FakeReadPath(text=b"bytes-not-str"), None, "not a path", FakeReadPath(text='{"z": 1, "a": 2}')]


@pytest.mark.parametrize("key", ["nt_read_json", "sar_read_json"])
@pytest.mark.parametrize("path", READ_CASES)
def test_read_json(orig_nodes, monkeypatch, guards, key, path):
    check(orig_nodes, monkeypatch, key, path)


@pytest.mark.parametrize("key", ["nt_read_json", "sar_read_json"])
def test_read_json_exact_and_seams(orig_nodes, monkeypatch, guards, key):
    assert check(orig_nodes, monkeypatch, key, FakeReadPath(text='{"z": 1, "a": 2}')) == {"z": 1, "a": 2} and list(check(orig_nodes, monkeypatch, key, FakeReadPath(text='{"z": 1, "a": 2}'))) == ["z", "a"]
    assert check(orig_nodes, monkeypatch, key, FakeReadPath(text="[1]")) == {} and check(orig_nodes, monkeypatch, key, FakeReadPath(exc=RuntimeError("x"))) == {} and check(orig_nodes, monkeypatch, key, None) == {}  # every Exception -> {}
    assert check(orig_nodes, monkeypatch, key, FakeReadPath(text='{"한글": "값"}')) == {"한글": "값"}

    class FakeJson:
        @staticmethod
        def loads(text):
            return {"seam": text}
    assert check(orig_nodes, monkeypatch, key, FakeReadPath(text="whatever"), overrides={"json": FakeJson}) == {"seam": "whatever"}  # json resolved at call time


# ---- A55-8 historical_prior._rank_bucket ----
@pytest.mark.parametrize("value", [None, "", "x", [], {}, 0, -1, -100, 1, 1.9, 2, 3, 3.9, 4, 10, 10.9, 11, 100, "1", "3.5", " 10 ", "11", NAN, float("inf"), float("-inf"), True, False, 0.5, _FloatErr(TypeError), _FloatErr(ValueError), _FloatErr(RuntimeError)])
def test_historical_rank_bucket(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "hp_rank_bucket", value)


def test_historical_rank_bucket_exact(orig_nodes, monkeypatch, guards):
    exp = {1: "rank1", 0: "rank1", -5: "rank1", 2: "rank2-3", 3: "rank2-3", 3.9: "rank2-3", 4: "rank4-10", 10: "rank4-10", 10.9: "rank4-10", 11: "rank11_plus", 100: "rank11_plus", "x": "unknown", None: "unknown", NAN: "unknown"}
    for value, name in exp.items():
        assert check(orig_nodes, monkeypatch, "hp_rank_bucket", value) == name
    assert check(orig_nodes, monkeypatch, "hp_rank_bucket", float("inf")) == ("err", "OverflowError", "cannot convert float infinity to integer")  # OverflowError is NOT caught
    assert check(orig_nodes, monkeypatch, "hp_rank_bucket", _FloatErr(RuntimeError)) == ("err", "RuntimeError", "custom float failure")


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
