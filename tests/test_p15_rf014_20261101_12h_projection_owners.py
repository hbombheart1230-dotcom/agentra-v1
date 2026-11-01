"""P15 RF-014 (20261101-12h): eight scanner projection bodies moved to single-owner modules; parity with the pre-move bodies (stdlib unittest)."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import unittest
from types import MappingProxyType, SimpleNamespace
from unittest import mock

from libs.agents.scanner.projections import output_payloads as op
from libs.agents.scanner.projections import output_snapshots as osn
from libs.agents.scanner.projections import scanner_output_numeric as out_num_owner
from libs.agents.scanner.projections import scanner_selection_skill as skill_owner
from libs.agents.scanner.projections import scanner_snapshot_coverage as coverage_owner
from libs.agents.scanner.projections import scanner_snapshot_features as features_owner
from libs.agents.scanner.projections import scanner_snapshot_numeric as num_owner
from libs.agents.scanner.projections import scanner_snapshot_ranking as ranking_owner
from libs.agents.scanner.projections import scanner_snapshot_selected as selected_owner
from libs.agents.scanner.projections import selection_evidence_projection as sel
from libs.agents.scanner.projections import selection_evidence_projection_scan_select_reasons_row_conf as reasons_owner

GOLDENS = {
    "a1": "ea06e8825799b6cc2c675974fb79d66934e889468bccb711281f2c981264c0dc",
    "a2": "c7c80574c70395b2ba703edbac181dfc8961f5ca40c5fe6e4a7f84a144aec671",
    "a3": "b10946965efde0f9a51a87f6d4615dc8d3c72077805cfa51ea5fa5c37f8887de",
    "a4": "1cdd3b282105eebf50fe6e6e4f3854b694086a7c0533ff72df88f1b0747c2b39",
    "a5": "e353dcef51f7d25b93ecb5dcfb990799098752fe23dba9335b927153f6a24cd4",
    "a6": "3bd8ffc6a50af56af95ebfc6c9debcea0e7638a1658b8c31095638bf37a33cc1",
    "a7": "3909ab3acfa248205c428f4de9915fcd8641286b3bb5f7eace26997969f225d1",
    "a8": "0cb4ce474f83ca67c63a905de6b59087d58946077f6eff0a199c2ce43fa9d788",
}


def _call(fn):
    try:
        return ["ok", fn()]
    except BaseException as exc:  # noqa: BLE001 - parity of exception type/message is the point
        return ["exc", type(exc).__name__, str(exc)]


def _h(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, default=repr).encode()).hexdigest()


class _Odd:
    def __bool__(self):
        raise RuntimeError("odd-bool")

    def __float__(self):
        raise ValueError("odd-float")


def _to_float_cases(fn, mod):
    values = ["2.5", "3.25", "bad", None, "", 0, 1, True, [], "1e3", " 7 ", float("inf"), float("nan"), _Odd(), "-0.5"]
    out = [_call(lambda v=v: fn(v)) for v in values]
    out += [
        _call(lambda: fn("bad", 7)),
        _call(lambda: fn("bad", default=9)),
        _call(lambda: fn(None, "x")),
        _call(lambda: fn("bad", None)),
        _call(lambda: fn("bad", default=_Odd())),
        _call(lambda: fn()),
    ]
    return out


def _full_selected():
    return {
        "symbol": "005930", "why": "w", "asset_class_detected": "equity", "detection_source": "s", "detection_field": "f", "score_total": "0.7", "risk_score": 0.2, "confidence": "bad",
        "candidate": {"sources": list("abcdefghij"), "source_scores": {"a": 1}, "source_observations": {"b": 2}, "rank_score": "1.5", "universe_score": None},
        "features": {"quote_best_bid": 100, "quote_best_ask": 101, "quote_spread_bps": 5, "engine_adx14": 20},
        "components": {"news_sentiment": 0.1, "momentum_component": 0.3},
        "score_breakdown": {"x": 1}, "tactical_strategy": "tac", "playbook": "pb", "tactic_suitability": {"tier": "high"},
    }


def _a2(fn, mod):
    sel_row = _full_selected()
    res = fn(sel_row)
    out = [
        ["copy", [res["sources"] == list("abcdefgh"), res["source_scores"] is not sel_row["candidate"]["source_scores"]]],
        _call(lambda: fn(None)),
        _call(lambda: fn({"symbol": "005930", "candidate": {}})),
        _call(lambda: fn(sel_row)),
        _call(lambda: fn({})),
        _call(lambda: fn([])),
        _call(lambda: fn({"symbol": 5, "candidate": [1], "features": "x", "components": None})),
        _call(lambda: fn(MappingProxyType(sel_row))),
        _call(lambda: fn()),
    ]
    with mock.patch.object(osn, "build_factor_snapshot_from_candidate", lambda *a, **k: {}):
        out.append(_call(lambda: fn({"symbol": "005930", "candidate": {}})))
    seen = []
    with mock.patch.object(osn, "build_factor_snapshot_from_candidate", lambda row, **k: seen.append(sorted(k)) or {"f": 1}):
        out.append(_call(lambda: fn(sel_row)))
    out.append(["factor-call", seen])
    with mock.patch.object(osn, "to_float", lambda v: 42.0):
        out.append(_call(lambda: fn(sel_row)))
    return out


def _a3(fn, mod):
    keys = ["engine_ma20_gap", "engine_ma60", "engine_ma120", "engine_adx14", "engine_trend_strength", "engine_atr14", "engine_volume_spike20", "engine_volatility20", "engine_vwap_distance", "engine_sector_relative_strength", "engine_cross_section_rank", "engine_regime", "engine_signal_score"]
    full = {"features": {k: 1 for k in keys}}
    half = {"features": {k: 1 for k in keys[:7]}}
    weak = {"features": {k: 1 for k in keys[:2]}}
    src = {"features": {"engine_ma60": 5, "engine_regime": ""}}
    out = [
        _call(lambda: fn({"features": {}})),
        _call(lambda: fn(full)),
        _call(lambda: fn(half)),
        _call(lambda: fn(weak)),
        _call(lambda: fn(src)),
        _call(lambda: fn({})),
        _call(lambda: fn({"features": None})),
        _call(lambda: fn({"features": [1]})),
        _call(lambda: fn({"features": {"engine_ma60": 0, "engine_adx14": None}})),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    out.append(["no-mutation", [src == {"features": {"engine_ma60": 5, "engine_regime": ""}}]])
    return out


def _a4(fn, mod):
    src = {"features": {"skill_quote_price": 101, "engine_regime": "bull"}}
    res = fn(src)
    out = [
        ["output", [res["skill_quote_price"], res["engine_regime"], len(res)]],
        _call(lambda: fn({"features": {"skill_quote_price": 101}})),
        _call(lambda: fn({})),
        _call(lambda: fn({"features": None})),
        _call(lambda: fn({"features": [1]})),
        _call(lambda: fn({"features": {}})),
        _call(lambda: fn(MappingProxyType({"features": {"quote_volume": 5}}))),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
        ["no-mutation", [src == {"features": {"skill_quote_price": 101, "engine_regime": "bull"}}]],
    ]
    return out


def _rank_rows():
    return [
        {"symbol": "005930", "score_total": "0.8", "confidence": 0.5, "risk_score": 0.2, "candidate": {"sources": list("abcdefghij"), "source_why": "why", "rank_score": 3}, "tactical_strategy": "t", "playbook": "p", "tactic_suitability": {"tier": "x"}, "post_adjust_score_total": None, "scanner_macro_chart_fit_score": None},
        {"symbol": "000660", "score": 0.4, "candidate": [1]},
        {},
    ]


def _a5(fn, mod):
    rows = _rank_rows()
    out = []
    with mock.patch.object(osn, "candidate_theme_match", lambda row: {"matched": bool(row.get("symbol"))}), mock.patch.object(osn, "build_factor_snapshot_from_candidate", lambda row, **k: {"sym": row.get("symbol"), "k": sorted(k)}):
        out += [
            _call(lambda: fn(rows)),
            _call(lambda: fn(rows, max_rows=1)),
            _call(lambda: fn(rows, max_rows=0)),
            _call(lambda: fn(rows, max_rows=-3)),
            _call(lambda: fn(rows, max_rows="2")),
            _call(lambda: fn(rows, max_rows="bad")),
            _call(lambda: fn([])),
            _call(lambda: fn(None)),
            _call(lambda: fn([None])),
            _call(lambda: fn(iter(rows))),
            _call(lambda: fn()),
        ]
    out.append(_call(lambda: fn([{"symbol": "005930"}], max_rows=1)))
    with mock.patch.object(osn, "candidate_theme_match", lambda row: False), mock.patch.object(osn, "build_factor_snapshot_from_candidate", lambda *a, **k: {}):
        out.append(_call(lambda: fn(rows[:1])))
    with mock.patch.object(osn, "candidate_theme_match", lambda row: False), mock.patch.object(osn, "build_factor_snapshot_from_candidate", lambda *a, **k: {}), mock.patch.object(osn, "to_float", lambda v, default=0.0: -1.0), mock.patch.object(osn, "feature_coverage_summary", lambda r: "COV"), mock.patch.object(osn, "compact_feature_snapshot", lambda r: "FEAT"):
        out.append(_call(lambda: fn(rows[:2])))
    return out


def _a6(fn, mod):
    ns = SimpleNamespace(SKILL_CONTRACT_VERSION="fixture")
    out = [
        _call(lambda: fn([], {}, {}, [], {}, {}, facade=ns)),
        _call(lambda: fn(["e1", "e2"], {"A": 1}, {"B": 2}, 5, {"present": True}, {"present": 0}, facade=ns)),
        _call(lambda: fn([], {"A": 1}, {}, "7", {}, {"present": "yes"}, facade=ns)),
        _call(lambda: fn([], {}, {"B": 1}, 0, {"present": None}, {}, facade=ns)),
        _call(lambda: fn(["x"], {}, {}, "bad", {}, {}, facade=ns)),
        _call(lambda: fn([], {}, {}, [], None, {}, facade=ns)),
        _call(lambda: fn([], {}, {}, [], {}, {}, facade=SimpleNamespace())),
        _call(lambda: fn([], {}, {}, [], {}, {})),
        _call(lambda: fn()),
    ]
    with mock.patch.object(sel, "SKILL_CONTRACT_VERSION", "patched", create=True):
        out.append(_call(lambda: fn([], {}, {}, [], {}, {}, facade=sel)))
    return out


def _a7(fn, mod):
    ns = SimpleNamespace(_to_float=float, List=list)
    base = {"symbol": "005930", "score_total": 0.5, "confidence": 0.3, "risk_score": 0.9}
    out = []
    ups = []
    out.append(_call(lambda: fn(base, 0.8, 0.6, 0.2, ups, facade=ns)))
    out.append(["appended", ups])
    ups2 = []
    out.append(_call(lambda: fn({"symbol": "X", "score": 0.9, "confidence": 0.9, "risk_score": 0.1}, 0.8, 0.6, 0.2, ups2, facade=ns)))
    out.append(["appended-tie", ups2])
    out.append(_call(lambda: fn({}, 0.1, 0.1, 0.1, [], facade=ns)))
    out.append(_call(lambda: fn({"score_total": "bad"}, 0.1, 0.1, 0.1, [], facade=ns)))
    out.append(_call(lambda: fn(base, 0.8, 0.6, 0.2, None, facade=ns)))
    out.append(_call(lambda: fn(None, 0.8, 0.6, 0.2, [], facade=ns)))
    out.append(_call(lambda: fn(base, 0.8, 0.6, 0.2, [], facade=SimpleNamespace(List=list))))
    out.append(_call(lambda: fn(base, "x", 0.6, 0.2, [], facade=ns)))
    out.append(_call(lambda: fn(base, 0.8, 0.6, 0.2, [])))
    out.append(_call(lambda: fn()))
    ns2 = SimpleNamespace(_to_float=lambda v, default=0.0: 1.0, List=list)
    out.append(_call(lambda: fn(base, 0.5, 0.5, 0.5, [], facade=ns2)))
    return out


CASES = {
    "a1": (_to_float_cases, osn, "to_float", lambda: num_owner.to_float, False, num_owner),
    "a2": (_a2, osn, "compact_selected_snapshot", lambda: selected_owner.compact_selected_snapshot, True, selected_owner),
    "a3": (_a3, osn, "feature_coverage_summary", lambda: coverage_owner.feature_coverage_summary, True, coverage_owner),
    "a4": (_a4, osn, "compact_feature_snapshot", lambda: features_owner.compact_feature_snapshot, True, features_owner),
    "a5": (_a5, osn, "ranking_table_rows", lambda: ranking_owner.ranking_table_rows, True, ranking_owner),
    "a6": (_a6, sel, "scan_select_value_state_scanner_skill", lambda: skill_owner.scan_select_value_state_scanner_skill, "own", skill_owner),
    "a7": (_a7, sel, "scan_select_reasons_row_conf", lambda: reasons_owner.scan_select_reasons_row_conf, "own", reasons_owner),
    "a8": (_to_float_cases, op, "_to_float", lambda: out_num_owner._to_float, False, out_num_owner),
}


def _run(key, which):
    scenario, mod, name, owner_factory, facade, _ = CASES[key]
    if which == "wrapper":
        fn = getattr(mod, name)
    else:
        raw = owner_factory()
        if facade is True:
            fn = lambda *a, **k: raw(*a, facade=mod, **k)  # noqa: E731
        elif facade == "own":
            fn = raw  # wrapper forwards the caller-supplied facade as-is
        else:
            fn = raw
    return json.loads(json.dumps(scenario(fn, mod), default=repr))


class Test(unittest.TestCase):
    def _parity(self, key):
        a = _run(key, "wrapper")
        b = _run(key, "owner")
        self.assertEqual(a, b)
        self.assertEqual(_h(a), GOLDENS[key])
        _, mod, name, _, _, owner_mod = CASES[key]
        fn = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
        # selection_evidence_projection is itself a pure Owner module (p159 authority gate forbids package imports at module level),
        # so its wrappers use a function-local import before the single return.
        stmts = [n for n in fn.body if not (isinstance(n, (ast.ImportFrom, ast.Import)) or (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant)))]
        self.assertTrue(len(stmts) == 1 and isinstance(stmts[0], ast.Return))
        self.assertNotIn("import " + mod.__name__.split(".")[-1], inspect.getsource(owner_mod))
        return a

    def test_a1_to_float(self):
        self._parity("a1")
        self.assertEqual(osn.to_float("2.5"), 2.5)
        self.assertEqual(osn.to_float("bad", 7), 7.0)

    def test_a2_compact_selected_snapshot(self):
        out = self._parity("a2")
        self.assertEqual(osn.compact_selected_snapshot(None), {})
        self.assertEqual(osn.compact_selected_snapshot({"symbol": "005930", "candidate": {}})["symbol"], "005930")
        self.assertEqual(out[0], ["copy", [True, True]])

    def test_a3_feature_coverage_summary(self):
        out = self._parity("a3")
        self.assertEqual(osn.feature_coverage_summary({"features": {}})["present"], 0)
        self.assertEqual(out[-1], ["no-mutation", [True]])

    def test_a4_compact_feature_snapshot(self):
        out = self._parity("a4")
        self.assertEqual(osn.compact_feature_snapshot({"features": {"skill_quote_price": 101}})["skill_quote_price"], 101)
        self.assertEqual(out[-1], ["no-mutation", [True]])

    def test_a5_ranking_table_rows(self):
        self._parity("a5")
        with mock.patch.object(osn, "candidate_theme_match", lambda r: False), mock.patch.object(osn, "build_factor_snapshot_from_candidate", lambda *a, **k: {}):
            self.assertEqual(osn.ranking_table_rows([], max_rows=5), [])
            self.assertEqual(osn.ranking_table_rows([{"symbol": "A"}], max_rows=0), [])
            rows = osn.ranking_table_rows([{"symbol": "A"}])
        self.assertEqual((len(rows), rows[0]["status"], rows[0]["rank"]), (1, "selected", 1))

    def test_a6_scan_select_value_state_scanner_skill(self):
        out = self._parity("a6")
        # NOTE: the order text used skill_order_rows=[] but the original body does int(skill_order_rows), which raises TypeError for a list
        # (pinned by the golden: out[0] below is an "exc"); the numeric 0 is the valid form for the positive check.
        got = sel.scan_select_value_state_scanner_skill([], {}, {}, 0, {}, {}, facade=SimpleNamespace(SKILL_CONTRACT_VERSION="fixture"))
        first = got[0] if isinstance(got, tuple) else got
        self.assertEqual((first["contract_version"], first["used"]), ("fixture", False))
        self.assertEqual(out[0][0], "exc")

    def test_a7_scan_select_reasons_row_conf(self):
        out = self._parity("a7")
        ups = []
        reasons, row_conf, row_risk, row_score = sel.scan_select_reasons_row_conf({"symbol": "005930", "score_total": 0.5, "confidence": 0.3, "risk_score": 0.9}, 0.8, 0.6, 0.2, ups, facade=SimpleNamespace(_to_float=float, List=list))
        self.assertEqual(len(reasons), 3)
        self.assertEqual(ups[0]["symbol"], "005930")
        self.assertEqual(out[1][0], "appended")

    def test_a8_to_float(self):
        self._parity("a8")
        self.assertEqual(op._to_float("3.25"), 3.25)
        self.assertEqual(op._to_float("bad", 9), 9.0)


if __name__ == "__main__":
    unittest.main()
