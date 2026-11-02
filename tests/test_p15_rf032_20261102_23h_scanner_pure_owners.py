"""RF-032 A47-1..8: eight ``scanner_score_decomposition`` / ``rolling_scorecard`` / ``scanner_quality`` bodies, original vs thin wrappers + Owners.

Original = A preimage d36550e5 (SOURCE blobs 52223768 / eb3b0347 / 5d36b62d == canonical 8e2765e8). Each original function is compiled from
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

A_PRE = "d36550e5dc1b6395ab861d4ac9e03a34be725cc4"
CANON = "8e2765e85c5e1fae62ce7f4dedb2e2551188de7b"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_num": ("scanner_score_decomposition", "52223768fde20d6de276e5e22a3aad28d5e49209", "scanner_score_decomposition_num"),
    "_first_num": ("scanner_score_decomposition", "52223768fde20d6de276e5e22a3aad28d5e49209", "scanner_score_decomposition_first_num"),
    "_nested_mapping": ("scanner_score_decomposition", "52223768fde20d6de276e5e22a3aad28d5e49209", "scanner_score_decomposition_nested_mapping"),
    "decompose_scanner_score": ("scanner_score_decomposition", "52223768fde20d6de276e5e22a3aad28d5e49209", "scanner_score_decomposition_decompose_scanner_score"),
    "build_rolling_scorecard": ("rolling_scorecard", "eb3b034783764055a3fcf4222f8a903d29c1ec6f", "rolling_scorecard_build_rolling_scorecard"),
    "_number": ("scanner_quality", "5d36b62d61fcbd7b3a99c2b5d4e4ba7c6a3f52b2", "scanner_quality_number"),
    "_checkpoint_return": ("scanner_quality", "5d36b62d61fcbd7b3a99c2b5d4e4ba7c6a3f52b2", "scanner_quality_checkpoint_return"),
    "extract_pre_strategist_candidate_rows": ("scanner_quality", "5d36b62d61fcbd7b3a99c2b5d4e4ba7c6a3f52b2", "scanner_quality_extract_pre_strategist_candidate_rows"),
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

SD = MODS["scanner_score_decomposition"]
RS = MODS["rolling_scorecard"]
SQ = MODS["scanner_quality"]


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


VALS = [None, "", 0, 0.0, "0", " 1.5 ", "abc", "1e3", "nan", "inf", NAN, True, [], {}, b"2", _Num(), _FloatErr(TypeError), _FloatErr(ValueError), (), "-0", -3, "１２"]


def _scalar_checks(orig_nodes, monkeypatch, name):
    assert check(orig_nodes, monkeypatch, name, None) is None and check(orig_nodes, monkeypatch, name, "") is None and check(orig_nodes, monkeypatch, name, 0) == 0.0
    assert check(orig_nodes, monkeypatch, name, _FloatErr(TypeError)) is None and check(orig_nodes, monkeypatch, name, _FloatErr(ValueError)) is None
    assert check(orig_nodes, monkeypatch, name, _FloatErr(RuntimeError)) == ("err", "RuntimeError", "custom float failure")  # only TypeError/ValueError caught
    out = check(orig_nodes, monkeypatch, name, "nan")
    assert out != out


# ---- A47-1 scanner_score_decomposition._num ----
@pytest.mark.parametrize("value", VALS)
def test_sd_num(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_num", value)


def test_sd_num_exact(orig_nodes, monkeypatch, guards):
    _scalar_checks(orig_nodes, monkeypatch, "_num")
    assert list(inspect.signature(SD._num).parameters) == ["value"]


# ---- A47-2 _first_num ----
FN_ROWS = [{}, {"a": 1}, {"a": None, "b": 2}, {"a": "", "b": "bad", "c": "3"}, {"a": 0, "b": 5}, {"a": "x"}, {"b": 2.5, "a": 9}, {"a": _FloatErr(RuntimeError)}, {"a": NAN, "b": 1}, {"a": [], "b": {}}]


@pytest.mark.parametrize("row", FN_ROWS)
@pytest.mark.parametrize("keys", [(), ("a",), ("a", "b"), ("b", "a"), ("a", "b", "c"), ("zz",)])
def test_sd_first_num(orig_nodes, monkeypatch, guards, row, keys):
    check(orig_nodes, monkeypatch, "_first_num", row, keys)


def test_sd_first_num_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_first_num", {"a": None, "b": 2}, ("a", "b")) == 2.0
    assert check(orig_nodes, monkeypatch, "_first_num", {"a": 0, "b": 5}, ("a", "b")) == 0.0  # 0.0 is a value, not None
    assert check(orig_nodes, monkeypatch, "_first_num", {}, ("a",)) is None
    assert check(orig_nodes, monkeypatch, "_first_num", None, ("a",))[0] == "err" and check(orig_nodes, monkeypatch, "_first_num", {"a": 1}, None)[0] == "err"
    assert check(orig_nodes, monkeypatch, "_first_num", {"a": _FloatErr(RuntimeError)}, ("a",)) == ("err", "RuntimeError", "custom float failure")
    seen = []
    out = check(orig_nodes, monkeypatch, "_first_num", {"a": 1, "b": 2}, ("a", "b"), overrides={"_num": lambda v: seen.append(v) or (None if v == 1 else 99.0)})
    assert out == 99.0 and seen == [1, 2, 1, 2]


# ---- A47-3 _nested_mapping ----
@pytest.mark.parametrize("row", [{}, {"k": None}, {"k": {}}, {"k": {"a": 1}}, {"k": _MapSub(a=1)}, {"k": []}, {"k": "s"}, {"k": 5}, {"k": [("a", 1)]}, None, []])
def test_sd_nested_mapping(orig_nodes, monkeypatch, guards, row):
    check(orig_nodes, monkeypatch, "_nested_mapping", row, "k")


def test_sd_nested_mapping_identity_and_seam(orig_nodes, monkeypatch, guards):
    inner = {"a": 1}
    assert SD._nested_mapping({"k": inner}, "k") is inner and SD._nested_mapping({}, "k") == {} and SD._nested_mapping({}, "k") is not SD._nested_mapping({}, "k")

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_nested_mapping", {"k": {"a": 1}}, "k", overrides={"Mapping": NeverMapping}) == {}


# ---- A47-4 decompose_scanner_score ----
FULL = {"symbol": "005930", "rank": 2, "score_total": "81.5", "raw_momentum_quality_score": 70, "strategy_context_score": "60", "cost_horizon_fit_score": 0.5, "execution_readiness_score": 55,
        "score_breakdown": {"momentum": 1, "strategy": 2}, "features": {"reward_room_pct": 3}, "quant_factors": {"entry_quality_score": 4}, "cost_filter": {"expected_edge_pct": 5}, "monitor": {"entry_quality_score": 6}}
FALLBACK = {"symbol": "A", "score_breakdown": {"momentum": 11, "strategy": 12}, "cost_filter": {"cost_adjusted_edge_pct": 13}, "monitor": {"transition_readiness_score": 14}}
FALLBACK2 = {"quant_factors": {"cost_adjusted_edge_pct": 21, "confidence_score": 22}, "features": {"expected_move_pct": 23}}
DS = [None, {}, FULL, FALLBACK, FALLBACK2, {"momentum_score": 5, "theme_score": 6, "expected_edge_pct": 7, "confidence_score": 8, "score": 9}, {"trend_score": "x", "score_breakdown": {"trend": 3}},
      {"breakout_score": 0, "score_intrinsic": 4, "rank_score": 0, "rank": 0}, {"features": {"reward_room_pct": "bad"}, "monitor": "bad", "cost_filter": [], "quant_factors": None}, "notmapping", [1], _MapSub(symbol="S"),
      {"symbol": None, "rank": None, "combined_score": 3}, {"symbol": _Str("한글")}]


@pytest.mark.parametrize("candidate", DS)
def test_decompose_scanner_score(orig_nodes, monkeypatch, guards, candidate):
    check(orig_nodes, monkeypatch, "decompose_scanner_score", candidate)


def test_decompose_exact_precedence_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "decompose_scanner_score", FULL)
    assert list(out) == ["schema_version", "behavior_effect", "symbol", "rank", "total_score", "raw_momentum_quality_score", "strategy_context_score", "cost_horizon_fit_score",
                         "execution_readiness_score", "source_fields_present", "limitations"]
    assert out["total_score"] == 81.5 and out["raw_momentum_quality_score"] == 70.0 and out["strategy_context_score"] == 60.0 and out["cost_horizon_fit_score"] == 0.5 and out["execution_readiness_score"] == 55.0
    assert out["source_fields_present"] == {"score_breakdown": True, "features": True, "quant_factors": True, "cost_filter": True, "monitor": True}
    fb = check(orig_nodes, monkeypatch, "decompose_scanner_score", FALLBACK)
    assert (fb["raw_momentum_quality_score"], fb["strategy_context_score"], fb["cost_horizon_fit_score"], fb["execution_readiness_score"]) == (11.0, 12.0, 13.0, 14.0)
    fb2 = check(orig_nodes, monkeypatch, "decompose_scanner_score", FALLBACK2)
    assert (fb2["cost_horizon_fit_score"], fb2["execution_readiness_score"]) == (21.0, 22.0)  # quant_factors checked before features
    empty = check(orig_nodes, monkeypatch, "decompose_scanner_score", None)
    assert empty["symbol"] == "" and empty["rank"] is None and empty["raw_momentum_quality_score"] is None and empty["limitations"][0].startswith("Field names vary")
    assert check(orig_nodes, monkeypatch, "decompose_scanner_score", {"rank_score": 0, "strategy_context_score": None})["strategy_context_score"] == 0.0
    assert SD.decompose_scanner_score.__doc__.startswith("Return an additive, read-only score view")  # wrapper keeps the original docstring
    out = check(orig_nodes, monkeypatch, "decompose_scanner_score", FULL, overrides={"_first_num": lambda r, keys: float(len(keys)), "_nested_mapping": lambda r, k: {"x": 1} if k == "monitor" else {}})
    assert out["total_score"] == 3.0 and out["source_fields_present"]["monitor"] is True and out["source_fields_present"]["features"] is False

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "decompose_scanner_score", FULL, overrides={"Mapping": NeverMapping})["symbol"] == ""


# ---- A47-5 build_rolling_scorecard ----
def _card(day, valid=None, ready=None, samples=None, counts=None, extra=None):
    ph = {}
    if valid is not None:
        ph["q9_day_validity"] = {"status": valid}
    if ready is not None:
        ph["full_chain_start_gate"] = {"status": ready}
    row = {"day": day, "evaluation_phase": ph, "realized_performance": {"return_samples_pct": samples if samples is not None else []}, "artifact_integrity": {"status_counts": counts or {}}}
    row.update(extra or {})
    return row


def _many(n_per_day, days=3, val=0.5):
    return [_card(f"2026-04-{10 + i}", valid="VALID", samples=[val] * n_per_day, counts={"OK": 1}) for i in range(days)]


SCS = [[], _many(10, 3), _many(5, 3), _many(10, 1), _many(10, 3, -0.5), _many(10, 3, 0.0), [_card("2026-04-10", ready="READY", samples=[1.0] * 25), _card("2026-04-11", ready="READY", samples=[2.0] * 25)],
       [_card("2026-04-12", valid="INVALID", samples=[1.0] * 40), _card("2026-04-11", valid="VALID", ready="NOT", samples=[1.0] * 25), _card("2026-04-10", valid=None, ready="READY", samples=[1.0] * 25)],
       [_card("2026-04-10", valid="VALID", samples=None, extra={"realized_performance": "bad"})], [{"day": "2026-04-10"}, {}], [_card("b", valid="VALID", samples=[1.0, "2"], counts={"A": 2, "B": 1}), _card("a", valid="VALID", samples=[3], counts={"A": 1})],
       [_card("2026-04-10", valid="VALID", samples=[1.0] * 25, counts=None)]]


@pytest.mark.parametrize("cards", SCS)
@pytest.mark.parametrize("window", [1, 2, 3, 7, 0])
def test_build_rolling_scorecard(orig_nodes, monkeypatch, guards, cards, window):
    check(orig_nodes, monkeypatch, "build_rolling_scorecard", cards, window_days=window)


def test_rolling_scorecard_exact_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "build_rolling_scorecard", _many(10, 3), window_days=3)
    assert list(out) == ["schema_version", "contract_version", "window_days", "start_day", "end_day", "valid_day_count", "decision_class", "realized_performance", "integrity_status_counts",
                         "source_days", "forward_window_eligible_days", "excluded_pre_start_gate_days"]
    assert out["decision_class"] == "RETAIN" and out["valid_day_count"] == 3 and out["integrity_status_counts"] == {"OK": 3} and len(out["realized_performance"]["return_samples_pct"]) == 30
    assert check(orig_nodes, monkeypatch, "build_rolling_scorecard", _many(5, 3), window_days=3)["decision_class"] == "INSUFFICIENT_EVIDENCE"  # 15 < 20 observations
    assert check(orig_nodes, monkeypatch, "build_rolling_scorecard", _many(10, 1), window_days=3)["decision_class"] == "INSUFFICIENT_EVIDENCE"  # one day < 2 days
    assert check(orig_nodes, monkeypatch, "build_rolling_scorecard", _many(10, 3, -0.5), window_days=3)["decision_class"] == "ADJUST_AND_RETEST"
    assert check(orig_nodes, monkeypatch, "build_rolling_scorecard", _many(10, 3, 0.0), window_days=3)["decision_class"] == "RETAIN"  # non-negative mean retains
    mixed = check(orig_nodes, monkeypatch, "build_rolling_scorecard", SCS[7], window_days=7)
    assert mixed["source_days"] == ["2026-04-10", "2026-04-11", "2026-04-12"] and mixed["forward_window_eligible_days"] == ["2026-04-10", "2026-04-11"] and mixed["excluded_pre_start_gate_days"] == ["2026-04-12"]  # VALID wins over gate; no validity -> READY gate
    assert check(orig_nodes, monkeypatch, "build_rolling_scorecard", None, window_days=3)[0] == "err" and check(orig_nodes, monkeypatch, "build_rolling_scorecard", [None], window_days=3)[0] == "err"
    src = copy.deepcopy(_many(10, 2))
    RS.build_rolling_scorecard(src, window_days=2)
    assert src == _many(10, 2)  # inputs untouched, samples list is a fresh list
    assert [p.kind.name for p in inspect.signature(RS.build_rolling_scorecard).parameters.values()] == ["POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY"]
    out = check(orig_nodes, monkeypatch, "build_rolling_scorecard", _many(2, 2), window_days=2, overrides={"DIRECTIONAL_MIN_OBSERVATIONS": 1, "DIRECTIONAL_MIN_DAYS": 1, "CONTRACT_VERSION": "fake.v9",
                                                                                                          "performance_metrics": lambda vals: {"n": len(vals)}})
    assert out["decision_class"] == "RETAIN" and out["contract_version"] == "fake.v9" and out["realized_performance"] == {"n": 4, "return_samples_pct": [0.5] * 4}


def test_rolling_scorecard_counter_and_decision_class_seams(orig_nodes, monkeypatch, guards):
    made = []

    class SpyCounter(collections.Counter):
        def __init__(self, *a, **k):
            made.append(1)
            super().__init__(*a, **k)
    check(orig_nodes, monkeypatch, "build_rolling_scorecard", _many(10, 3), window_days=3, overrides={"Counter": SpyCounter})
    assert made == [1, 1]

    class FakeDecision:
        class INSUFFICIENT_EVIDENCE:
            value = "FAKE_INSUFFICIENT"

        class ADJUST_AND_RETEST:
            value = "FAKE_ADJUST"

        class RETAIN:
            value = "FAKE_RETAIN"
    assert check(orig_nodes, monkeypatch, "build_rolling_scorecard", _many(10, 3), window_days=3, overrides={"DecisionClass": FakeDecision})["decision_class"] == "FAKE_RETAIN"


# ---- A47-6 scanner_quality._number ----
@pytest.mark.parametrize("value", VALS)
def test_sq_number(orig_nodes, monkeypatch, guards, value):
    check(orig_nodes, monkeypatch, "_number", value)


def test_sq_number_exact(orig_nodes, monkeypatch, guards):
    _scalar_checks(orig_nodes, monkeypatch, "_number")


# ---- A47-7 scanner_quality._checkpoint_return ----
def _qrow(cp, **extra):
    return {"shadow_forward_outcome": {"checkpoints": cp, **extra}}


QR = [{}, None, "row", {"shadow_forward_outcome": None}, {"shadow_forward_outcome": "x"}, _qrow(None), _qrow("x"), _qrow({}), _qrow({"+5m": None}), _qrow({"+5m": "x"}), _qrow({"+5m": {}}),
      _qrow({"+5m": {"status": "pending", "return_pct": 1}}), _qrow({"+5m": {"status": "observed"}}), _qrow({"+5m": {"status": "observed", "return_pct": 0}}), _qrow({"+5m": {"status": "observed", "return_pct": "1.25"}}),
      _qrow({"+5m": {"status": "observed", "return_pct": "bad"}}), _qrow({"+5m": {"status": "observed", "return_pct": ""}}), _qrow({"+15m": {"status": "observed", "return_pct": -2}}),
      _qrow({"+5m": {"status": "OBSERVED", "return_pct": 1}}), _qrow({"+5m": _MapSub(status="observed", return_pct=3)}), _qrow({"+5m": {"status": _Str("observed"), "return_pct": 4}})]


@pytest.mark.parametrize("row", QR)
@pytest.mark.parametrize("horizon", ["+5m", "+15m", "missing"])
def test_sq_checkpoint_return(orig_nodes, monkeypatch, guards, row, horizon):
    check(orig_nodes, monkeypatch, "_checkpoint_return", row, horizon)


def test_sq_checkpoint_return_exact_and_seams(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", _qrow({"+5m": {"status": "observed", "return_pct": 0}}), "+5m") == 0.0
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", _qrow({"+5m": {"status": "observed"}}), "+5m") is None
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", None, "+5m")[0] == "err"
    seen = []
    out = check(orig_nodes, monkeypatch, "_checkpoint_return", _qrow({"+5m": {"status": "observed", "return_pct": "7"}}), "+5m", overrides={"_number": lambda v: seen.append(v) or 99.0})
    assert out == 99.0 and seen == ["7", "7"]

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "_checkpoint_return", _qrow({"+5m": {"status": "observed", "return_pct": 1}}), "+5m", overrides={"Mapping": NeverMapping}) is None


# ---- A47-8 extract_pre_strategist_candidate_rows ----
ROLE = "P_SCANNER_PRE_STRATEGIST_UNIVERSE"


def _cand(did="D1", sym="A", rank=1, role=ROLE, **extra):
    return {"q9_decision_id": did, "symbol": sym, "rank": rank, "q9_decision_role": role, **extra}


XPAYS = [[], [{}], [{"q9_decision_candidates": None}], [{"q9_decision_candidates": []}],
         [{"generated_at": "g", "q9_decision_candidates": [_cand(), _cand(sym="B", rank=2), _cand(), "bad", None, _cand(role="OTHER"), _cand(did=""), _cand(sym=""), _cand(rank=0), _cand(rank=-1), _cand(rank="x"),
                                                         _cand(rank="3", sym="C"), _cand(sym="D", rank=4, _payload_generated_at="keep"), _cand(rank=1.9, sym="E")]}],
         [{"generated_at": "g1", "q9_decision_candidates": [_cand()]}, {"generated_at": "g2", "q9_decision_candidates": [_cand(), _cand(did="D2")]}],
         [{"q9_decision_candidates": [_cand(extra={"nested": [1]})]}], [{"generated_at": None, "q9_decision_candidates": ({"q9_decision_role": ROLE, "q9_decision_id": "D", "symbol": "S", "rank": 1},)}],
         [{"candidates": [_cand()]}]]


@pytest.mark.parametrize("payloads", XPAYS)
def test_extract_pre_strategist_candidate_rows(orig_nodes, monkeypatch, guards, payloads):
    check(orig_nodes, monkeypatch, "extract_pre_strategist_candidate_rows", payloads)


def test_extract_exact_order_copy_and_seams(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "extract_pre_strategist_candidate_rows", XPAYS[4])
    assert [(r["symbol"], r["rank"]) for r in out] == [("A", 1), ("B", 2), ("C", "3"), ("D", 4), ("E", 1.9)] and out[3]["_payload_generated_at"] == "keep" and out[0]["_payload_generated_at"] == "g"
    src = _cand()
    out = SQ.extract_pre_strategist_candidate_rows([{"generated_at": "g", "q9_decision_candidates": [src]}])
    assert out[0] is not src and "_payload_generated_at" not in src  # copied row, source untouched
    assert check(orig_nodes, monkeypatch, "extract_pre_strategist_candidate_rows", None)[0] == "err" and check(orig_nodes, monkeypatch, "extract_pre_strategist_candidate_rows", ["x"])[0] == "err"
    dup = check(orig_nodes, monkeypatch, "extract_pre_strategist_candidate_rows", [{"q9_decision_candidates": [_cand(), _cand(), _cand(rank=2)]}])
    assert [r["rank"] for r in dup] == [1, 2]  # (decision, symbol, rank) deduplicated, first wins
    seen = []
    out = check(orig_nodes, monkeypatch, "extract_pre_strategist_candidate_rows", [{"q9_decision_candidates": [_cand(rank="a"), _cand(sym="Z", rank="b")]}],
                overrides={"_number": lambda v: seen.append(v) or {"a": 1.0, "b": 2.0}.get(v)})
    assert [r["symbol"] for r in out] == ["A", "Z"] and seen == ["a", "b", "a", "b"]

    class NeverMapping:
        pass
    assert check(orig_nodes, monkeypatch, "extract_pre_strategist_candidate_rows", XPAYS[4], overrides={"Mapping": NeverMapping}) == []


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
