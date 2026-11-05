"""RF-032 A57-2: ``cumulative_improvement_review._candidate_rows``, original vs thin wrappers + Owners.

Original = A preimage 825124e5 (SOURCE blob 7cf50b31 = canonical a2f64696 + the A57-1 `_rank_row` wrapper; `_candidate_rows` source text is identical on both). Each original function is compiled from
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

A_PRE = "825124e5dc54f92dce76d7137e0c87d04da763c4"
CANON = "f804efddedea841a0df36da441118e511080e548"
EV = "libs/reporting/evaluation/"
# name -> (source stem, pinned blob, owner module stem)
SPEC = {
    "_candidate_rows": ("cumulative_improvement_review", "7cf50b31af540c9bfde01c6e15b768836fc40cc2", "cumulative_improvement_review_candidate_rows", "_candidate_rows"),
}
CANON_BLOB = "a2f64696546cb729afd7c5b89d9d1c1e06edeac7"
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
            assert _sha(raws[label]) == (blob if label == "A" else CANON_BLOB), f"BLOCKED_PIN {stem} {label} blob"
        tree = ast.parse(raws["A"].decode("utf-8"))
        ctree = ast.parse(raws["canonical"].decode("utf-8"))
        for n, v in SPEC.items():  # the moved function's source text must be identical on A and canonical
            if v[0] == stem:
                seg = lambda raw, t: ast.get_source_segment(raw.decode("utf-8"), [x for x in t.body if isinstance(x, ast.FunctionDef) and x.name == v[3]][-1])
                assert seg(raws["A"], tree) == seg(raws["canonical"], ctree), f"HOLD: {v[3]} differs between A and canonical"
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


CI = MODS["cumulative_improvement_review"]


class NeverMapping:
    pass


class _MapSub(dict):
    def __repr__(self):
        return f"_MapSub({dict(self)!r})"


class _FloatErr:
    def __repr__(self):
        return "_FloatErr()"

    def __float__(self):
        raise RuntimeError("custom float failure")


def _rr(bucket, expectancy):
    return {"rank_bucket": bucket, "horizon": "+30m", "live_net": {"expectancy_pct": expectancy}}


def _ep(r1=None, r23=None, status="READY", gross=0.4):
    rows = []
    if r1 is not None:
        rows.append(_rr("rank1", r1))
    if r23 is not None:
        rows.append(_rr("rank2_3", r23))
    return {"rank_horizon_rows": rows, "score_component_review": {"status": status}, "rank1_minus_rank2_3_gross_30m_pct": gross}


RE = {"eligible": {"behavior_candidate_eligible": True, "repeat_entry": {"count": 5, "expectancy_pct": -0.3}, "repeat_minus_first_expectancy_pct": -0.7, "repeat_after_loss": {"count": 3}, "repeat_after_non_loss": {"count": 2}},
      "ineligible": {"behavior_candidate_eligible": False, "repeat_entry": None}, "empty": {}}
PR = {"full": {"promotion_status": "RESEARCH", "observed_count": 8, "observed_day_count": 3, "rows": [{"horizon": "+30m"}]}, "empty": {}}
SR = {"negative": {"rows": [{"horizon": "+5m", "avg_strategist_minus_scanner_pct": 9}, {"horizon": "+30m", "avg_strategist_minus_scanner_pct": -0.2, "x": 1}]}, "positive": {"rows": [{"horizon": "+30m", "avg_strategist_minus_scanner_pct": 0.2}]},
      "zero": {"rows": [{"horizon": "+30m", "avg_strategist_minus_scanner_pct": 0}]}, "none": {"rows": [{"horizon": "+30m", "avg_strategist_minus_scanner_pct": None}]}, "missing": {}, "bad_rows": {"rows": ["bad", None, 5]},
      "rows_none": {"rows": None}, "sub": {"rows": [_MapSub(horizon="+30m", avg_strategist_minus_scanner_pct=-1)]}}
EPS = {"diag": _ep(-0.1, -0.2), "not_ready": _ep(-0.1, -0.2, status="NOT_READY"), "retain": _ep(0.3, -0.2), "retain2": _ep(-0.1, 0.4), "zero": _ep(0, 0), "missing_rows": _ep(), "only_r1": _ep(r1=-1), "no_review": {}, "no_score": {"rank_horizon_rows": [_rr("rank1", -1), _rr("rank2_3", -1)]},
       "strings": {"rank_horizon_rows": [_rr("rank1", "-0.5"), _rr("rank2_3", "-0.1")], "score_component_review": {"status": "READY"}}, "bad_float": {"rank_horizon_rows": [_rr("rank1", "x")]}, "none_values": {"rank_horizon_rows": [_rr("rank1", None), {"rank_bucket": "rank2_3", "horizon": "+30m", "live_net": None}]}}


def _kw(ep="diag", re="eligible", pr="full", sr="negative"):
    return dict(episode_review=EPS[ep], reentry_review=RE[re], post_reclaim_review=PR[pr], strategist_review=SR[sr])


@pytest.mark.parametrize("ep", list(EPS))
@pytest.mark.parametrize("sr", list(SR))
def test_candidate_rows_episode_and_strategist(orig_nodes, monkeypatch, guards, ep, sr):
    check(orig_nodes, monkeypatch, "_candidate_rows", **_kw(ep=ep, sr=sr))


@pytest.mark.parametrize("re", list(RE))
@pytest.mark.parametrize("pr", list(PR))
def test_candidate_rows_reentry_and_post_reclaim(orig_nodes, monkeypatch, guards, re, pr):
    check(orig_nodes, monkeypatch, "_candidate_rows", **_kw(re=re, pr=pr))


def test_candidate_rows_exact_structure_and_statuses(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_candidate_rows", **_kw())
    assert [r["priority"] for r in out] == [1, 2, 3, 4] and [r["candidate"] for r in out] == ["same_symbol_loss_reentry_control", "confirmed_post_reclaim_pullback_subtype", "scanner_rank_ordering_component_review", "strategist_ranking_weight_guard"]
    assert [r["class"] for r in out] == ["damage_reduction", "alpha_research", "ranking_diagnosis", "strategist_effectiveness"] and [list(r)[:4] for r in out] == [["priority", "candidate", "class", "status"]] * 4
    assert out[0]["status"] == "APPLIED_2026_07_29" and out[1]["status"] == "RESEARCH" and out[2]["status"] == "DIAGNOSTIC_CANDIDATE" and out[3]["status"] == "DIAGNOSTIC_CANDIDATE"
    assert list(out[0]["evidence"]) == ["repeat_count", "repeat_expectancy_pct", "repeat_minus_first_expectancy_pct", "repeat_after_loss", "repeat_after_non_loss"] and out[0]["evidence"]["repeat_count"] == 5
    assert out[1]["evidence"] == {"observed_count": 8, "observed_day_count": 3, "horizon_rows": [{"horizon": "+30m"}]} and out[3]["evidence"] == {"horizon": "+30m", "avg_strategist_minus_scanner_pct": -0.2, "x": 1}
    ineligible = check(orig_nodes, monkeypatch, "_candidate_rows", **_kw(re="ineligible", pr="empty", sr="positive"))
    assert ineligible[0]["status"] == "INSUFFICIENT_EVIDENCE" and ineligible[1]["status"] is None and ineligible[3]["status"] == "RETAIN_UNDER_OBSERVATION" and ineligible[0]["evidence"]["repeat_count"] is None


def test_candidate_rows_rank_ordering_status_matrix(orig_nodes, monkeypatch, guards):
    status = lambda ep: check(orig_nodes, monkeypatch, "_candidate_rows", **_kw(ep=ep))[2]["status"]
    assert status("diag") == "DIAGNOSTIC_CANDIDATE" and status("not_ready") == "OBSERVABILITY_NOT_READY" and status("retain") == "RETAIN_UNDER_OBSERVATION"
    assert status("retain2") == "RETAIN_UNDER_OBSERVATION" and status("zero") == "DIAGNOSTIC_CANDIDATE"  # <= 0 counts as non-positive
    assert status("no_review") == "OBSERVABILITY_NOT_READY" and status("no_score") == "OBSERVABILITY_NOT_READY"  # missing score review is not READY
    ev = check(orig_nodes, monkeypatch, "_candidate_rows", **_kw(ep="diag"))[2]["evidence"]
    assert list(ev) == ["rank1_live_net_30m_pct", "rank2_3_live_net_30m_pct", "rank1_minus_rank2_3_gross_30m_pct", "score_component_review"] and ev["rank1_live_net_30m_pct"] == -0.1
    out = CI._candidate_rows(**_kw(re="eligible"))  # direct call: check() deep-copies its inputs, identity needs the real objects
    assert out[2]["evidence"]["score_component_review"] is EPS["diag"]["score_component_review"]  # nested object identity preserved
    assert out[0]["evidence"]["repeat_after_loss"] is RE["eligible"]["repeat_after_loss"] and out[1]["evidence"]["horizon_rows"] is PR["full"]["rows"]


def test_candidate_rows_errors_and_signature(orig_nodes, monkeypatch, guards):
    assert check(orig_nodes, monkeypatch, "_candidate_rows", **_kw(ep="bad_float"))[0:2] == ("err", "ValueError")  # float("x")
    bad_float = dict(_kw(), episode_review={"rank_horizon_rows": [{"rank_bucket": "rank1", "horizon": "+30m", "live_net": {"expectancy_pct": _FloatErr()}}]})
    assert check(orig_nodes, monkeypatch, "_candidate_rows", **bad_float) == ("err", "RuntimeError", "custom float failure")
    assert check(orig_nodes, monkeypatch, "_candidate_rows", **dict(_kw(), episode_review=None))[0] == "err"
    assert check(orig_nodes, monkeypatch, "_candidate_rows", **dict(_kw(), reentry_review=None))[0] == "err"
    assert check(orig_nodes, monkeypatch, "_candidate_rows", **dict(_kw(), strategist_review=None))[0] == "err"
    assert check(orig_nodes, monkeypatch, "_candidate_rows", **dict(_kw(), post_reclaim_review=None))[0] == "err"
    assert all(p.kind.name == "KEYWORD_ONLY" for p in inspect.signature(CI._candidate_rows).parameters.values()) and len(inspect.signature(CI._candidate_rows).parameters) == 4


def test_candidate_rows_rank_row_call_time_seam(orig_nodes, monkeypatch, guards):
    seen = []

    def fake_rank_row(review, *, bucket, horizon):
        seen.append((bucket, horizon))
        return {"live_net": {"expectancy_pct": 5.0 if bucket == "rank1" else -5.0}}
    out = check(orig_nodes, monkeypatch, "_candidate_rows", **_kw(), overrides={"_rank_row": fake_rank_row})
    assert seen == [("rank1", "+30m"), ("rank2_3", "+30m")] * 2 and out[2]["evidence"]["rank1_live_net_30m_pct"] == 5.0 and out[2]["status"] == "RETAIN_UNDER_OBSERVATION"


def test_candidate_rows_mapping_seam(orig_nodes, monkeypatch, guards):
    out = check(orig_nodes, monkeypatch, "_candidate_rows", **_kw(sr="negative"), overrides={"Mapping": NeverMapping})
    assert out[3]["evidence"] == {} and out[3]["status"] == "RETAIN_UNDER_OBSERVATION"  # strategist rows ignored when Mapping never matches
    assert out[2]["evidence"]["rank1_live_net_30m_pct"] == 0.0  # the real _rank_row also resolves Mapping at call time


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
    owner_tree = ast.parse(inspect.getsource(OWNERS[name]))
    stem = SPEC[name][0]
    imported = []
    for n in ast.walk(owner_tree):
        if isinstance(n, ast.Import):
            imported += [alias.name for alias in n.names]
        elif isinstance(n, ast.ImportFrom):
            imported.append(("." * n.level) + (n.module or ""))
            imported += [alias.name for alias in n.names]
    assert not [i for i in imported if i.split(".")[-1] == stem], f"Owner must not import its SOURCE: {imported}"
