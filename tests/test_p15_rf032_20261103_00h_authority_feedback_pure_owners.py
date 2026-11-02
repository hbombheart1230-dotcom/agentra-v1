"""RF-032 A48-1..8: eight ``scanner_quality`` / ``selection_authority_audit`` / ``feedback_effectiveness`` bodies, original vs thin wrappers + Owners.

Original = A preimage 128bad77 (SOURCE blobs 13abc5dd / 7f139a43 / f12cec33 == canonical 1edf8dfc). Each original function is compiled from
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

A_PRE = "128bad7750e7e0dc472303755337d16cd38f4d60"
CANON = "1edf8dfc4d1eb82a5512709977d3e3cc52392dc3"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "build_scanner_topk_forward_performance": ("scanner_quality", "13abc5dd46c0f6912fe263fd1dfd3dbbf3fd3df5", "scanner_quality_build_scanner_topk_forward_performance"),
    "build_scanner_source_performance": ("scanner_quality", "13abc5dd46c0f6912fe263fd1dfd3dbbf3fd3df5", "scanner_quality_build_scanner_source_performance"),
    "_mapping": ("selection_authority_audit", "7f139a43a46a53c947c033d19a2eea4fff36ac7c", "selection_authority_audit_mapping"),
    "_symbol": ("selection_authority_audit", "7f139a43a46a53c947c033d19a2eea4fff36ac7c", "selection_authority_audit_symbol"),
    "_changed": ("selection_authority_audit", "7f139a43a46a53c947c033d19a2eea4fff36ac7c", "selection_authority_audit_changed"),
    "build_selection_authority_audit": ("selection_authority_audit", "7f139a43a46a53c947c033d19a2eea4fff36ac7c", "selection_authority_audit_build_selection_authority_audit"),
    "render_selection_authority_audit": ("selection_authority_audit", "7f139a43a46a53c947c033d19a2eea4fff36ac7c", "selection_authority_audit_render_selection_authority_audit"),
    "build_feedback_effectiveness": ("feedback_effectiveness", "f12cec33f28a492c41e306dbede6c8c4540eb4a0", "feedback_effectiveness_build_feedback_effectiveness"),
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
SA = MODS["selection_authority_audit"]
FE = MODS["feedback_effectiveness"]


class _Str:
    def __init__(self, text, truthy=True):
        self.text, self.truthy = text, truthy

    def __repr__(self):
        return f"_Str({self.text!r},{self.truthy})"

    def __str__(self):
        return self.text

    def __bool__(self):
        return self.truthy


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


class _BadStr:
    def __repr__(self):
        return "_BadStr()"

    def __str__(self):
        raise RuntimeError("str failure")


# ---- scanner_quality fixtures ----
def _cp(v, status="observed"):
    return {"status": status, "return_pct": v}


def _q(did, rank, cps, day="2026-04-10", sources=None, **extra):
    row = {"q9_decision_id": did, "rank": rank, "generated_at": f"{day}T00:00:00+00:00", "shadow_forward_outcome": {"checkpoints": cps}}
    if sources is not None:
        row["q9_candidate_sources"] = sources
    row.update(extra)
    return row


QROWS = [_q("D1", 1, {"+5m": _cp(1.0), "+15m": _cp(2.0)}, sources=["s1"]), _q("D1", 2, {"+5m": _cp(3.0), "EOD": _cp(-1.0)}, sources=["s1", "s2"]), _q("D1", 5, {"+5m": _cp(0.5)}),
         _q("D1", "x", {"+5m": _cp(9.0)}), _q("D1", None, {"+5m": _cp(7.0)}), _q("D2", 1, {"+5m": _cp(-1.0), "+30m": _cp("bad")}, day="2026-04-11", sources=[""]), _q("D2", 3, {}, day="2026-04-11"),
         _q("D2", 11, {"+5m": _cp(2.0, "pending")}, day="2026-04-11"), _q("", 1, {"+5m": _cp(5.0)}), {"q9_decision_id": "D3"}, _q("D3", 2, {"+5m": _cp(0.0)}, day="", sources=None, sources_alt=1),
         {**_q("D4", 4, {"+5m": _cp(1.5)}), "sources": ["z"]}]


# ---- A48-1 build_scanner_topk_forward_performance ----
@pytest.mark.parametrize("rows", [[], QROWS, QROWS[:3], QROWS[5:8], QROWS[8:], [QROWS[0]]])
@pytest.mark.parametrize("cost,slip", [(0.0, 0.0), (0.9, 0.05), (0.123456789, 0.987654321), (-0.5, 0.1)])
def test_topk_forward_performance(orig_nodes, monkeypatch, guards, rows, cost, slip):
    check(orig_nodes, monkeypatch, "build_scanner_topk_forward_performance", rows, cost_pct=cost, slippage_pct=slip)


def test_topk_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "build_scanner_topk_forward_performance", QROWS, cost_pct=0.9, slippage_pct=0.05)
    assert list(out) == ["schema_version", "behavior_effect", "decision_window_count", "candidate_row_count", "top_k_values", "horizons", "rows"]
    assert out["top_k_values"] == [1, 3, 5, 10] and out["horizons"] == ["+5m", "+15m", "+30m", "EOD"] and len(out["rows"]) == 16
    assert [(r["horizon"], r["top_k"]) for r in out["rows"]][:5] == [("+5m", 1), ("+5m", 3), ("+5m", 5), ("+5m", 10), ("+15m", 1)]
    r = out["rows"][0]
    assert list(r) == ["top_k", "horizon", "window_count", "candidate_observation_count", "observed_day_count", "cost_pct", "slippage_pct", "gross", "net"]
    assert r["cost_pct"] == 0.9 and r["slippage_pct"] == 0.05 and out["decision_window_count"] == 4 and out["candidate_row_count"] == len(QROWS)
    assert check(orig_nodes, monkeypatch, "build_scanner_topk_forward_performance", [], cost_pct=0.0, slippage_pct=0.0)["decision_window_count"] == 0
    assert check(orig_nodes, monkeypatch, "build_scanner_topk_forward_performance", None, cost_pct=0.0, slippage_pct=0.0)[0] == "err"
    assert check(orig_nodes, monkeypatch, "build_scanner_topk_forward_performance", QROWS, cost_pct="x", slippage_pct=0.0)[0:2] == ("err", "ValueError")
    assert check(orig_nodes, monkeypatch, "build_scanner_topk_forward_performance", [None], cost_pct=0.0, slippage_pct=0.0)[0] == "err"
    assert [p.kind.name for p in inspect.signature(SQ.build_scanner_topk_forward_performance).parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY", "KEYWORD_ONLY"]
    out = check(orig_nodes, monkeypatch, "build_scanner_topk_forward_performance", QROWS[:3], cost_pct=0.0, slippage_pct=0.0,
                overrides={"SCANNER_HORIZONS": ("+5m",), "TOP_K_VALUES": (2,), "performance_metrics": lambda vals: {"n": len(vals)}, "candidate_day": lambda r: "DAY", "_checkpoint_return": lambda r, h: 1.0})
    assert out["rows"] == [{"top_k": 2, "horizon": "+5m", "window_count": 1, "candidate_observation_count": 2, "observed_day_count": 1, "cost_pct": 0.0, "slippage_pct": 0.0, "gross": {"n": 1}, "net": {"n": 1}}]
    out = check(orig_nodes, monkeypatch, "build_scanner_topk_forward_performance", QROWS[:3], cost_pct=0.0, slippage_pct=0.0, overrides={"_number": lambda v: 1.0 if v is not None else None})
    assert out["rows"]  # rank ordering seam via _number
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "build_scanner_topk_forward_performance", QROWS[:2], cost_pct=0.0, slippage_pct=0.0, overrides={"defaultdict": spy})
    assert made == [1, 1]


# ---- A48-2 build_scanner_source_performance ----
@pytest.mark.parametrize("rows", [[], QROWS, QROWS[:3], QROWS[5:8], QROWS[8:], [QROWS[1]]])
@pytest.mark.parametrize("cost,slip", [(0.0, 0.0), (0.9, 0.05), (0.123456789, 0.987654321)])
def test_source_performance(orig_nodes, monkeypatch, guards, rows, cost, slip):
    check(orig_nodes, monkeypatch, "build_scanner_source_performance", rows, cost_pct=cost, slippage_pct=slip)


def test_source_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "build_scanner_source_performance", QROWS, cost_pct=0.9, slippage_pct=0.05)
    assert list(out) == ["schema_version", "behavior_effect", "rows"] and out["schema_version"] == "q9_scanner_source_performance.v1"
    keys = [(r["source"], r["horizon"]) for r in out["rows"]]
    assert keys == sorted(keys) and ("unknown", "+5m") in keys and ("s2", "+5m") in keys
    assert list(out["rows"][0])[:5] == ["source", "horizon", "observed_day_count", "cost_pct", "slippage_pct"]
    s1 = [r for r in out["rows"] if r["source"] == "s1" and r["horizon"] == "+5m"][0]
    assert s1["cost_pct"] == 0.9 and s1["slippage_pct"] == 0.05 and s1["count"] == 2  # net of 0.95 drag, performance_metrics keys merged last
    assert check(orig_nodes, monkeypatch, "build_scanner_source_performance", None, cost_pct=0.0, slippage_pct=0.0)[0] == "err"
    assert check(orig_nodes, monkeypatch, "build_scanner_source_performance", QROWS, cost_pct=None, slippage_pct=0.0)[0:2] == ("err", "TypeError")
    out = check(orig_nodes, monkeypatch, "build_scanner_source_performance", QROWS[:2], cost_pct=1.0, slippage_pct=0.0,
                overrides={"SCANNER_HORIZONS": ("+5m",), "_checkpoint_return": lambda r, h: 2.0, "candidate_day": lambda r: "D", "performance_metrics": lambda vals: {"vals": list(vals)}})
    assert [(r["source"], r["vals"]) for r in out["rows"]] == [("s1", [1.0, 1.0]), ("s2", [1.0])]
    made = []

    def spy(factory):
        made.append(1)
        return collections.defaultdict(factory)
    check(orig_nodes, monkeypatch, "build_scanner_source_performance", QROWS[:2], cost_pct=0.0, slippage_pct=0.0, overrides={"defaultdict": spy})
    assert made == [1, 1, 1, 1]  # buckets + days, per side


# ---- A48-3 selection_authority_audit._mapping ----
@pytest.mark.parametrize("value", [None, {}, {"a": 1}, _MapSub(a=1), [], [("a", 1)], "s", 5, {"n": {"deep": [1]}}])
def test_sa_mapping(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_mapping", value)


def test_sa_mapping_identity_and_seam(orig_nodes, monkeypatch, guards):
    src = {"a": 1}
    assert SA._mapping(src) is src and SA._mapping(None) == {} and SA._mapping(None) is not SA._mapping(None)

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_mapping", {"a": 1}, overrides={"Mapping": NeverMapping}) == {}


# ---- A48-4 _symbol ----
@pytest.mark.parametrize("value", [None, "", " ", " 005930 ", "한글", 0, 5, 1.5, [], {}, {"symbol": " A "}, {"symbol": None}, {"symbol": 0}, {"other": 1}, _MapSub(symbol="B"), _Str(" x "), _Str("y", truthy=False),
                                   [1], {"symbol": _Str(" z ")}, {"symbol": _BadStr()}, _BadStr()])
def test_sa_symbol(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_symbol", value)


def test_sa_symbol_exact_and_seam(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_symbol", {"symbol": " A "}) == "A" and check(orig_nodes, monkeypatch, "_symbol", " B ") == "B" and check(orig_nodes, monkeypatch, "_symbol", None) == ""
    assert check(orig_nodes, monkeypatch, "_symbol", {"symbol": 0}) == "" and check(orig_nodes, monkeypatch, "_symbol", 0) == ""
    assert check(orig_nodes, monkeypatch, "_symbol", _BadStr()) == ("err", "RuntimeError", "str failure")

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_symbol", {"symbol": "A"}, overrides={"Mapping": NeverMapping}) == "{'symbol': 'A'}"


# ---- A48-5 _changed ----
@pytest.mark.parametrize("a,b", [("", ""), ("a", ""), ("", "b"), ("a", "a"), ("a", "b"), (" a", "a"), ("A", "a"), (None, "a"), ("a", None), (None, None), (0, 0), (1, 1), (1, 2), ("한글", "한글"), ([], "x")])
def test_sa_changed(orig_nodes, monkeypatch, guards, a, b):
    check(orig_nodes, monkeypatch, "_changed", a, b)


def test_sa_changed_exact(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_changed", "", "x") is None and check(orig_nodes, monkeypatch, "_changed", "x", "") is None
    assert check(orig_nodes, monkeypatch, "_changed", "x", "x") is False and check(orig_nodes, monkeypatch, "_changed", "x", "y") is True


# ---- A48-6 build_selection_authority_audit ----
def _sm(tid="T1", raw="A", post="A", sel="A", mon_sel=None, entry_ctx_sel=None, cand="A", csel="A", sym="A", defects=None, scope="final", decision="APPROVE", mismatch=None):
    selection = {"raw_scanner_top1": {"symbol": raw}, "scanner_top1": post, "selected_symbol": sel, "commander_final": {"candidate_symbol": cand, "selected_symbol": csel, "authority_scope": scope, "decision": decision}}
    if mismatch is not None:
        selection["selection_mismatch"] = mismatch
    monitor = {}
    if mon_sel is not None:
        monitor["selected_symbol"] = mon_sel
    if entry_ctx_sel is not None:
        monitor["entry_context"] = {"selected_symbol": entry_ctx_sel}
    return {"trade_id": tid, "symbol": sym, "selection": selection, "monitor": monitor, "integrity": {"defects": defects or []}}


MS = [_sm(), _sm("T2", raw="A", post="B", sel="C", mon_sel="D", cand="E", csel="F", sym="G"), _sm("T3", raw="", post="B"), _sm("T4", defects=["broker_day_partial_exit_duplicate"]), _sm("T5", defects=["confirmed_runtime_defect"]),
      _sm("T6", defects=["other", "confirmed_runtime_defect"]), _sm("T7", mon_sel=None, entry_ctx_sel="Z"), _sm("T8", cand="", csel=""), _sm("T9", mismatch={"k": "v"}), {"trade_id": "T10"}, {}, _sm("T11", sym=""),
      {"trade_id": "T12", "selection": "bad", "monitor": "bad", "integrity": "bad"}, _sm("T13", sel="", mon_sel="", entry_ctx_sel=""), {"integrity": {"defects": None}}]


@pytest.mark.parametrize("models", [[], MS, MS[:2], MS[3:6], MS[6:9], MS[9:], [MS[0]] * 3])
def test_build_selection_authority_audit(orig_nodes, monkeypatch, guards, models):
    check(orig_nodes, monkeypatch, "build_selection_authority_audit", models)


def test_selection_audit_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "build_selection_authority_audit", MS)
    assert list(out) == ["schema_version", "behavior_effect", "trade_count", "summary", "interpretation", "rows"]
    assert out["summary"]["excluded:broker_day_partial_exit_duplicate"] == 1 and out["summary"]["excluded:confirmed_runtime_defect"] == 2  # T5, T6 (first defect branch wins)
    row = out["rows"][1]
    assert row["trade_id"] == "T2" and row["raw_to_post_changed"] is True and row["final_to_executed_changed"] is True and list(row)[:4] == ["trade_id", "symbol", "raw_scanner_top1", "post_strategy_top1"]
    t3 = [r for r in out["rows"] if r["trade_id"] == "T3"][0]
    assert t3["raw_to_post_changed"] is None  # blank raw -> unavailable
    assert [r for r in out["rows"] if r["trade_id"] == "T7"][0]["monitor_symbol"] == "Z"  # entry_context fallback
    assert any(k.endswith(":unavailable") for k in out["summary"]) and out["interpretation"]["commander_scope"].startswith("final approval/veto")
    assert check(orig_nodes, monkeypatch, "build_selection_authority_audit", None)[0] == "err" and check(orig_nodes, monkeypatch, "build_selection_authority_audit", [None])[0] == "err"
    out = check(orig_nodes, monkeypatch, "build_selection_authority_audit", MS[:2], overrides={"_changed": lambda a, b: True, "_symbol": lambda v: "S"})
    assert out["rows"][0]["raw_to_post_changed"] is True and out["rows"][0]["symbol"] == "S" and out["summary"]["raw_to_post_changed:True"] == 2
    made = []

    class SpyCounter(collections.Counter):
        def __init__(self, *a, **k):
            made.append(1)
            super().__init__(*a, **k)
    check(orig_nodes, monkeypatch, "build_selection_authority_audit", MS[:1], overrides={"Counter": SpyCounter})
    assert made == [1, 1]


# ---- A48-7 render_selection_authority_audit ----
SP = {"behavior_effect": "observation_only", "trade_count": 2, "summary": {"b:True": 2, "a:False": 1}, "rows": [{"trade_id": "T1", "raw_scanner_top1": "A", "post_strategy_top1": "B", "selected_symbol": "C", "monitor_symbol": "",
                                                                                                         "commander_candidate_symbol": "E", "commander_selected_symbol": None, "executed_symbol": "한글"}, "bad", {}, None]}
SPS = [{}, SP, {**SP, "summary": {}}, {**SP, "summary": None, "rows": None}, {"summary": "bad"}, {**SP, "rows": [{"trade_id": 0, "executed_symbol": 0}]}, {"summary": {"z": 1, "y": 2}}]


@pytest.mark.parametrize("payload", SPS)
def test_render_selection_authority_audit(orig_nodes, monkeypatch, guards, payload):
    check(orig_nodes, monkeypatch, "render_selection_authority_audit", payload)


def test_render_selection_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "render_selection_authority_audit", SP)
    assert out.startswith("# Selection Authority Audit\n\n- Behavior effect: `observation_only`\n- Trades: 2\n\n## Summary\n\n- `a:False`: 1\n- `b:True`: 2\n")  # sorted
    assert "| T1 | A | B | C | - | E | - | 한글 |\n" in out and out.endswith(" |\n")  # last table row, "" joined -> trailing newline
    assert "- No rows." in check(orig_nodes, monkeypatch, "render_selection_authority_audit", {}) and check(orig_nodes, monkeypatch, "render_selection_authority_audit", None)[0] == "err"

    class NeverMapping:
        pass
    assert "| T1 |" not in check(orig_nodes, monkeypatch, "render_selection_authority_audit", SP, overrides={"Mapping": NeverMapping})
    out = check(orig_nodes, monkeypatch, "render_selection_authority_audit", SP, overrides={"_mapping": lambda v: {"only": 1}})
    assert "- `only`: 1\n" in out


# ---- A48-8 build_feedback_effectiveness ----
def _win(fid="F1", did="D1", status="CHANGE_OBSERVED_WITH_FEEDBACK_EXPOSURE", **fb):
    feedback = {"feedback_id": fid, "adoption_status": status, "source_day": "2026-04-09", "consumed": True, "changed_fields": ["x"], **fb}
    return {"decision_id": did, "strategist_provenance": {"feedback": feedback}}


def _tm(tid="T1", source="strategy_feedback_v1"):
    return {"trade_id": tid, "provenance": {"field_sources": {"strategy_policy_source": source}}}


WINS = [_win(), _win(), _win("F1", "D2"), _win("F2", "D1", status="NO_CHANGE"), {"decision_id": "X"}, {"q9_decision_id": "Q", "strategist_provenance": {"feedback": {"feedback_id": "F9"}}},
        {"strategist_provenance": "bad"}, {"strategist_provenance": {"feedback": "bad"}}, {"strategist_provenance": {"feedback": {"feedback_id": ""}}}, _win("F3", "", consumed=0, changed_fields=None)]
TMS = [_tm(), _tm(), _tm("T2", "FEEDBACK_policy"), _tm("T3", "other"), {"trade_id": "T4"}, {"provenance": "bad"}, {"provenance": {"field_sources": "bad"}}, {"provenance": {"field_sources": {"strategy_policy_source": None}}}, _tm("T5", "x_Feedback_y")]


@pytest.mark.parametrize("tms", [[], TMS, TMS[:2], TMS[2:4], TMS[4:]])
@pytest.mark.parametrize("wins", [None, [], WINS, WINS[:3], WINS[3:6], WINS[6:]])
def test_build_feedback_effectiveness(orig_nodes, monkeypatch, guards, tms, wins):
    check(orig_nodes, monkeypatch, "build_feedback_effectiveness", tms, wins)


def test_feedback_effectiveness_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "build_feedback_effectiveness", TMS, WINS)
    assert list(out) == ["schema_version", "contract_version", "decision_class", "exposure_count", "adoption_count", "adoption_rate", "usefulness_score", "records", "provenance_linkage_status", "missing_requirement", "causal_claim_allowed"]
    assert out["decision_class"] == "INSUFFICIENT_EVIDENCE" and out["causal_claim_allowed"] is False and out["usefulness_score"] is None and out["provenance_linkage_status"] == "ACTIVE"
    assert out["exposure_count"] == len(out["records"]) and out["adoption_rate"] == round(out["adoption_count"] / out["exposure_count"], 4)
    empty = check(orig_nodes, monkeypatch, "build_feedback_effectiveness", [], None)
    assert empty["adoption_rate"] == 0.0 and empty["provenance_linkage_status"] == "AWAITING_NEW_RUNTIME_ARTIFACTS" and empty["records"] == []
    dup = check(orig_nodes, monkeypatch, "build_feedback_effectiveness", [_tm(), _tm()], [_win(), _win()])
    assert dup["exposure_count"] == 2  # one window + one trade, duplicates removed
    assert check(orig_nodes, monkeypatch, "build_feedback_effectiveness", None, [])[0] == "err" and check(orig_nodes, monkeypatch, "build_feedback_effectiveness", [], [None])[0] == "err"
    assert check(orig_nodes, monkeypatch, "build_feedback_effectiveness", [None], [])[0] == "err"
    assert inspect.signature(FE.build_feedback_effectiveness).parameters["q9_windows"].default is None
    src_t, src_w = copy.deepcopy(TMS), copy.deepcopy(WINS)
    FE.build_feedback_effectiveness(src_t, src_w)
    assert src_t == TMS and src_w == WINS
    class FakeDecision:
        class INSUFFICIENT_EVIDENCE:
            value = "FAKE"
    out = check(orig_nodes, monkeypatch, "build_feedback_effectiveness", [], [], overrides={"DecisionClass": FakeDecision, "CONTRACT_VERSION": "fake.v1"})
    assert out["decision_class"] == "FAKE" and out["contract_version"] == "fake.v1"


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
