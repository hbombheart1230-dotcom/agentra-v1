"""P15 RF-035 (20261101-06h): eight quant_tactic_evaluation / quant_tactic_report / q8_evaluation_contract bodies moved to projection Owners; parity with the pre-move bodies (stdlib unittest)."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import unittest
from types import MappingProxyType
from unittest import mock

from libs.reporting import q8_candidate_day_projection as day_owner
from libs.reporting import q8_evaluation_contract as q8c
from libs.reporting import quant_tactic_eval_builder_projection as builder_owner
from libs.reporting import quant_tactic_eval_mismatch_examples_projection as mismatch_owner
from libs.reporting import quant_tactic_eval_render_projection as render_owner
from libs.reporting import quant_tactic_evaluation as qe
from libs.reporting import quant_tactic_report as qt
from libs.reporting import quant_tactic_report_lines_projection as report_lines_owner
from libs.reporting import quant_tactic_selected_candidate_projection as selected_owner
from libs.reporting import quant_tactic_sources_projection as sources_owner
from libs.reporting import quant_tactic_surface_projection as surface_owner

GOLDENS = {
    "a1": "241b2c668a3acfd25bb608dc6c470744907953cf5a73ae3ef0fe27a34f6a5f66",
    "a2": "12412f706ea26f107bcf38ca3412f51db9286ed8e9a45bf4b32406cad5a2c31e",
    "a3": "e4bbb873c71421fbd779ca8ad9d151f58cda54e234bd4613d12b3f0157dbba83",
    "a4": "72888593ed5f23537ccc906fcb1316fa14d2fdebdd20d9322319562443f0a618",
    "a5": "1e90e3e67dcd625ade10aaac2e4155aed36e3d724eed07e0cd42e9f3fd7c7eb9",
    "a6": "a9cfa414707ed47105569adf5f53d787a950e9721b168508cbd7cabac4e47f1a",
    "a7": "dd6640788924504193f3f9ccdbd6d5aa98f364668999b96b2ed0526ceae8f407",
    "a8": "180538680c66400ab9b213a28139aa96a98501c51c84a5e858124b99c760f99c",
}


def _call(fn):
    try:
        return ["ok", fn()]
    except BaseException as exc:  # noqa: BLE001 - parity of exception type/message is the point
        return ["exc", type(exc).__name__, str(exc)]


def _h(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, default=repr).encode()).hexdigest()


def _a1(fn, mod):
    rows = [
        {"trade_id": "T", "symbol": "S", "quant_tactic_id": "Q", "quant_tactic_mismatch_count": 2},
        {"trade_id": "U", "quant_tactic_mismatch_count": 0},
        {"trade_id": " unknown ", "symbol": "S2", "quant_tactic_mismatch_count": "3", "quant_tactic_id": None},
        {"quant_tactic_mismatch_count": "bad"},
        {"trade_id": "V", "quant_tactic_mismatch_count": 1},
        {"trade_id": "W", "quant_tactic_mismatch_count": 5},
    ]
    out = [
        _call(lambda: fn(rows)),
        _call(lambda: fn(rows, limit=2)),
        _call(lambda: fn(rows, limit=0)),
        _call(lambda: fn(rows, limit=-1)),
        _call(lambda: fn([{"trade_id": "T", "quant_tactic_mismatch_count": 0}])),
        _call(lambda: fn([])),
        _call(lambda: fn(iter(rows))),
        _call(lambda: fn(None)),
        _call(lambda: fn([None])),
        _call(lambda: fn()),
    ]
    with mock.patch.object(qe, "_text", lambda v: "T" if v else ""):
        out.append(_call(lambda: fn(rows)))
    with mock.patch.object(qe, "_int", lambda v, default=0: 1):
        out.append(_call(lambda: fn([{}])))
    return out


def _closed(i, **kw):
    return dict({"status": "closed", "trade_id": f"T{i}", "symbol": "S", "quant_tactic_id": "Q", "quant_tactic_id_source": "entry_quant_decision",
                 "entry_quant_decision": "go", "exit_quant_decision": "ok", "tactic_suitability_tier": "high", "entry_quant_cost_floor_state": "ok"}, **kw)


def _a2(fn, mod):
    many = [_closed(i) for i in range(25)]
    out = [
        _call(lambda: fn([])),
        _call(lambda: fn([_closed(1, broker_alignment_status="bad")])),
        _call(lambda: fn(many[:3])),
        _call(lambda: fn(many[:10])),
        _call(lambda: fn(many)),
        _call(lambda: fn(many[:10] + [_closed(99, quant_tactic_mismatch_count=2, quant_exit_tactic_drift_count=1)])),
        _call(lambda: fn([_closed(i, entry_quant_decision="") for i in range(12)])),
        _call(lambda: fn([{"status": "open"}] * 3)),
        _call(lambda: fn(iter(many[:9]))),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(qe, "_MIN_REVIEW_SAMPLE", 2), mock.patch.object(qe, "_TARGET_PROMOTION_SAMPLE", 4):
        out.append(_call(lambda: fn(many[:3])))
        out.append(_call(lambda: fn(many[:5])))
    with mock.patch.object(qe, "_evaluation_rows", lambda rows: [{"x": 1}]):
        out.append(_call(lambda: fn([])))
    with mock.patch.object(qe, "_field_gap_rows", lambda rows: [{"field": "f", "coverage_ok": False}]):
        out.append(_call(lambda: fn(many)))
    return out


def _a3(fn, mod):
    with mock.patch.object(qe, "_MIN_REVIEW_SAMPLE", 8):
        ev_empty = qe.build_quant_tactic_evaluation([])
        ev_ready = qe.build_quant_tactic_evaluation([_closed(i) for i in range(25)])
        ev_invalid = qe.build_quant_tactic_evaluation([_closed(1, broker_alignment_status="bad")])
        ev_mismatch = qe.build_quant_tactic_evaluation([_closed(i, quant_tactic_mismatch_count=1) for i in range(10)])
    out = [
        _call(lambda: fn({})),
        _call(lambda: fn(None)),
        _call(lambda: fn({"status": "hold_sample_insufficient"})),
        _call(lambda: fn(ev_empty)),
        _call(lambda: fn(ev_ready)),
        _call(lambda: fn(ev_invalid)),
        _call(lambda: fn(ev_mismatch)),
        _call(lambda: fn(MappingProxyType(ev_ready))),
        _call(lambda: fn({"status": "x", "missing_required_fields": ["a", "b"], "tactic_id_source_counts": {"s": 2}, "invalid_sample_examples": [{"trade_id": "T"}, "junk"], "tactic_id_mismatch_examples": [{"trade_id": "M"}, 5]})),
        _call(lambda: fn({"status": "x", "invalid_sample_count": "bad"})),
        _call(lambda: fn([1])),
        _call(lambda: fn()),
    ]
    with mock.patch.object(qe, "_TARGET_PROMOTION_SAMPLE", 77):
        out.append(_call(lambda: fn({"status": "x"})))
    with mock.patch.object(qe, "Mapping", tuple):
        out.append(_call(lambda: fn({"status": "x", "invalid_sample_examples": [{"trade_id": "T"}]})))
    return out


def _nested_report(symbol="005930", **row_extra):
    row = dict({"symbol": symbol, "quant_factor_snapshot": {"tactic_id": "QT"}, "tactic_suitability": {"tier": "high"}, "scanner_chart_fit_score": 1}, **row_extra)
    return {"why": {"candidates": [{"symbol": "000660", "confidence": 0.1}, row, {"symbol": symbol, "score_total": 2}]}, "symbol": symbol}


def _a4(fn, mod):
    out = [
        _call(lambda: fn(_nested_report(), "005930")),
        _call(lambda: fn(_nested_report(), "999999")),
        _call(lambda: fn(_nested_report(), "")),
        _call(lambda: fn(_nested_report(), None)),
        _call(lambda: fn(_nested_report(), " 005930 ")),
        _call(lambda: fn({}, "005930")),
        _call(lambda: fn({"a": [{"symbol": "S", "confidence": 1}, {"symbol": "S", "quant_factor_snapshot": {"x": 1}, "final_selected_symbol": "S"}]}, "S")),
        _call(lambda: fn({"a": [{"symbol": "S", "confidence": 1}, {"symbol": "S", "selected_symbol": "S", "score_total": 1}]}, "S")),
        _call(lambda: fn({"a": [{"symbol": "S", "confidence": 1}, {"symbol": "S", "confidence": 2}]}, "S")),
        _call(lambda: fn(None, "S")),
        _call(lambda: fn(_nested_report())),
        _call(lambda: fn()),
    ]
    with mock.patch.object(qt, "_candidate_symbol", lambda item: "P" if "quant_factor_snapshot" in item else ""):
        out.append(_call(lambda: fn(_nested_report(), "P")))
    with mock.patch.object(qt, "_mapping", lambda v: {"m": 1}):
        out.append(_call(lambda: fn({"a": [{"symbol": "S", "confidence": 1}, {"symbol": "S", "confidence": 2, "k": 1}]}, "S")))
    with mock.patch.object(qt, "_nested_dicts", lambda root: [{"symbol": "N", "confidence": 9}]):
        out.append(_call(lambda: fn({}, "N")))
    return out


def _a5(fn, mod):
    def kw(**over):
        base = dict(entry_decision={}, factor_snapshot={}, selected_row={}, tactic_suitability={}, exit_decision={})
        base.update(over)
        return base

    out = [
        _call(lambda: fn(**kw(entry_decision={"tactic_id": "A"}))),
        _call(lambda: fn(**kw())),
        _call(lambda: fn(**kw(entry_decision={"tactic_id": " A "}, factor_snapshot={"tactic_id": "B"}, exit_decision={"tactic_id": "C"}))),
        _call(lambda: fn(**kw(selected_row={"quant_factor_snapshot": {"tactic_id": "SF"}, "tactical_strategy": "TS"}))),
        _call(lambda: fn(**kw(tactic_suitability={"tactic_id": "TSU"}))),
        _call(lambda: fn(**kw(entry_decision={"tactic_id": 0}, factor_snapshot={"tactic_id": None}, exit_decision={"tactic_id": False}))),
        _call(lambda: fn(**kw(entry_decision={"tactic_id": 5}))),
        _call(lambda: fn(**kw(selected_row=None))),
        _call(lambda: fn(**kw(entry_decision=None))),
        _call(lambda: fn()),
    ]
    with mock.patch.object(qt, "_tactic_value", lambda v: "T" if v else ""):
        out.append(_call(lambda: fn(**kw(entry_decision={"tactic_id": "x"}, exit_decision={"tactic_id": "y"}))))
    with mock.patch.object(qt, "_mapping", lambda v: {"tactic_id": "PM"}):
        out.append(_call(lambda: fn(**kw(selected_row={"quant_factor_snapshot": 1}))))
    return out


def _fake_surface(report):
    return {"tactic_id": "T", "playbook": "P", "entry_quant_decision": {"decision": "entry_ready", "blockers": ["b"], "warnings": [], "cost_edge": {"edge_ok": True, "net_edge_pct": 0.12345, "required_edge_pct": 0.1}},
            "exit_quant_decision": {"decision": "hard_exit", "reason_codes": ["r1"]}, "factors": {"momentum": 1.5}, "tactic_suitability": {"tier": "high", "score": 0.9},
            "tactic_id_mismatches": [{"source": "s", "tactic_id": "m"}], "exit_tactic_drifts": [{"source": "e", "tactic_id": "d"}], "scanner_chart_fit": {"score": 1, "authority": "a"}}


def _a6(fn, mod):
    out = [_call(lambda: fn({})), _call(lambda: fn(None)), _call(lambda: fn()), _call(lambda: fn({}, compact=True))]
    with mock.patch.object(qt, "quant_tactic_surface", lambda report: {"tactic_id": "T"}):
        out.append(_call(lambda: fn({"x": 1})))
        out.append(_call(lambda: fn({"x": 1}, compact=True)))
    with mock.patch.object(qt, "quant_tactic_surface", _fake_surface):
        out.append(_call(lambda: fn({"x": 1})))
        out.append(_call(lambda: fn({"x": 1}, compact=True)))
        out.append(_call(lambda: fn(None)))
        with mock.patch.object(qt, "_fmt", lambda v: "F"), mock.patch.object(qt, "_decision_label", lambda v: "D"), mock.patch.object(qt, "_reason_text", lambda v: "R"):
            out.append(_call(lambda: fn({"x": 1})))
        with mock.patch.object(qt, "_mapping", lambda v: {}):
            out.append(_call(lambda: fn({"x": 1})))
    with mock.patch.object(qt, "quant_tactic_surface", lambda report: (_ for _ in ()).throw(RuntimeError("boom"))):
        out.append(_call(lambda: fn({"x": 1})))
    return out


def _a7(fn, mod):
    report = {
        "symbol": "005930",
        "monitor_snapshot": {"entry_quant_decision": {"tactic_id": "T", "playbook": "P"}},
        "why_this_symbol_was_chosen": {"scanner_selection_trace": {"tactic_suitability": {"tier": "low"}}, "scanner_chart_fit": {"score": 2}},
        "entry_execution_visibility": {"monitor_focus_context": {"entry_triggered": True, "entry_reason": "ok"}},
        "candidates": [{"symbol": "005930", "quant_factor_snapshot": {"tactic_id": "QT", "factors": {"f": 1}}, "tactic_suitability": {"tier": "mid"}, "scanner_chart_fit_score": 3}],
        "exit_quant_decision": {"tactic_id": "X", "playbook": "XP"},
    }
    calls = []

    def fake_decision(entry_info, **kw):
        calls.append(["decision", sorted(entry_info), sorted(kw)])
        return {"decision": "fake", "tactic_id": kw.get("tactic_id")}

    def fake_suit(row, **kw):
        calls.append(["suit", sorted(kw)])
        return {"tier": "fake"}

    out = []
    with mock.patch.object(qt, "build_entry_quant_decision", fake_decision), mock.patch.object(qt, "score_candidate_tactic_suitability", fake_suit):
        out += [
            _call(lambda: fn({})),
            _call(lambda: fn(None)),
            _call(lambda: fn(report)),
            _call(lambda: fn({"entry_quant_decision": {"tactic_id": "T", "playbook": "P"}})),
            _call(lambda: fn({"symbol": "005930", "candidates": report["candidates"]})),
            _call(lambda: fn({"symbol": "005930", "entry_execution_visibility": report["entry_execution_visibility"]})),
            _call(lambda: fn({"exit_quant_decision": {"tactic_id": "Z"}})),
            _call(lambda: fn({"unrelated": 1})),
            _call(lambda: fn(MappingProxyType({"entry_quant_decision": {"tactic_id": "mp"}}))),
            _call(lambda: fn([1])),
            _call(lambda: fn()),
        ]
        with mock.patch.object(qt, "_playbook", lambda root, fallback="": "PB"):
            out.append(_call(lambda: fn({"symbol": "005930", "candidates": report["candidates"]})))
        with mock.patch.object(qt, "_tactic_sources", lambda **k: [("src", "ID")]):
            out.append(_call(lambda: fn({"entry_quant_decision": {"tactic_id": "Q"}})))
        with mock.patch.object(qt, "_mapping", lambda v: {}):
            out.append(_call(lambda: fn(report)))
    out.append(["calls", calls])
    return out


def _a8(fn, mod):
    out = [
        _call(lambda: fn({"shadow_forward_base": {"baseline_raw_ts": "20260217T010000"}})),
        _call(lambda: fn({"generated_at": "2026-11-01T00:00:00Z"})),
        _call(lambda: fn({})),
        _call(lambda: fn({"_payload_generated_at": "2026-11-01", "generated_at": "2025-01-01"})),
        _call(lambda: fn({"generated_at": "2026-11-0"})),
        _call(lambda: fn({"shadow_forward_base": {"baseline_raw_ts": "2026"}, "generated_at": "2026-11-01"})),
        _call(lambda: fn({"shadow_forward_base": {"baseline_raw_ts": "abcdefgh"}, "generated_at": "2026-11-01"})),
        _call(lambda: fn({"shadow_forward_base": {"baseline_raw_ts": "20260217"}})),
        _call(lambda: fn({"shadow_forward_base": [1], "generated_at": "unknown"})),
        _call(lambda: fn({"generated_at": 20261101})),
        _call(lambda: fn(MappingProxyType({"generated_at": "2026-11-01T00:00:00Z"}))),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(q8c, "forward_base", lambda row: {"baseline_raw_ts": "99999999"}):
        out.append(_call(lambda: fn({})))
    with mock.patch.object(q8c, "text_value", lambda v: "20300101xx" if v else ""):
        out.append(_call(lambda: fn({"generated_at": "x"})))
    return out


CASES = {
    "a1": (_a1, qe, "_mismatch_examples", lambda: mismatch_owner._mismatch_examples, mismatch_owner),
    "a2": (_a2, qe, "build_quant_tactic_evaluation", lambda: builder_owner.build_quant_tactic_evaluation, builder_owner),
    "a3": (_a3, qe, "render_quant_tactic_evaluation_lines", lambda: render_owner.render_quant_tactic_evaluation_lines, render_owner),
    "a4": (_a4, qt, "_selected_candidate_row", lambda: selected_owner._selected_candidate_row, selected_owner),
    "a5": (_a5, qt, "_tactic_sources", lambda: sources_owner._tactic_sources, sources_owner),
    "a6": (_a6, qt, "render_quant_tactic_report_lines", lambda: report_lines_owner.render_quant_tactic_report_lines, report_lines_owner),
    "a7": (_a7, qt, "quant_tactic_surface", lambda: surface_owner.quant_tactic_surface, surface_owner),
    "a8": (_a8, q8c, "candidate_day", lambda: day_owner.candidate_day, day_owner),
}
_REAL = {"qe": qe, "qt": qt, "q8c": q8c}


def _run(key, which):
    scenario, mod, name, owner_factory, _ = CASES[key]
    if which == "wrapper":
        fn = getattr(mod, name)
    else:
        raw = owner_factory()
        fn = lambda *a, **k: raw(*a, facade=mod, **k)  # noqa: E731
    return json.loads(json.dumps(scenario(fn, mod), default=repr))


class Test(unittest.TestCase):
    def _parity(self, key):
        a = _run(key, "wrapper")
        b = _run(key, "owner")
        self.assertEqual(a, b)
        self.assertEqual(_h(a), GOLDENS[key])
        _, mod, name, _, owner_mod = CASES[key]
        fn = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
        stmts = [n for n in fn.body if not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
        self.assertTrue(len(stmts) == 1 and isinstance(stmts[0], ast.Return))
        self.assertNotIn("import " + mod.__name__.split(".")[-1], inspect.getsource(owner_mod))
        self.assertIn("facade", inspect.getsource(getattr(owner_mod, name)))
        return a

    def test_a1_mismatch_examples(self):
        out = self._parity("a1")
        got = qe._mismatch_examples([{"trade_id": "T", "symbol": "S", "quant_tactic_id": "Q", "quant_tactic_mismatch_count": 2}])
        self.assertEqual(got[0]["mismatch_count"], 2)
        self.assertEqual(qe._mismatch_examples([{"trade_id": "T", "quant_tactic_mismatch_count": 0}]), [])
        self.assertEqual(out[2][0], "ok")

    def test_a2_build_quant_tactic_evaluation(self):
        out = self._parity("a2")
        self.assertEqual(out[0][1]["status"], "hold_sample_insufficient")
        self.assertEqual(out[0][1]["closed_or_realized_sample_count"], 0)
        self.assertEqual(out[1][1]["status"], "hold_invalid_truth_samples")

    def test_a3_render_quant_tactic_evaluation_lines(self):
        out = self._parity("a3")
        self.assertEqual(out[0], ["ok", []])
        self.assertTrue(out[2][1])
        self.assertIn("Quant Q8 readiness", out[2][1][0])

    def test_a4_selected_candidate_row(self):
        out = self._parity("a4")
        self.assertEqual(out[0][1]["quant_factor_snapshot"], {"tactic_id": "QT"})
        self.assertEqual(out[1], ["ok", {}])

    def test_a5_tactic_sources(self):
        out = self._parity("a5")
        self.assertEqual(qt._tactic_sources(entry_decision={"tactic_id": "A"}, factor_snapshot={}, selected_row={}, tactic_suitability={}, exit_decision={}), [("entry_quant_decision", "A")])
        self.assertEqual(out[1], ["ok", []])

    def test_a6_render_quant_tactic_report_lines(self):
        out = self._parity("a6")
        self.assertEqual(out[0], ["ok", []])
        self.assertIn("- 전술 ID: `T`", out[4][1])
        self.assertTrue(out[5][1][0].startswith("* 전술 진단:"))

    def test_a7_quant_tactic_surface(self):
        out = self._parity("a7")
        self.assertEqual(out[0], ["ok", {}])
        surface = out[3][1]
        self.assertEqual(surface["tactic_id"], "T")
        self.assertEqual(surface["schema_version"], "quant_tactic_report_surface.v1")

    def test_a8_candidate_day(self):
        out = self._parity("a8")
        self.assertEqual(q8c.candidate_day({"shadow_forward_base": {"baseline_raw_ts": "20260217T010000"}}), "20260217")
        self.assertEqual(q8c.candidate_day({"generated_at": "2026-11-01T00:00:00Z"}), "20261101")
        self.assertEqual(out[2], ["ok", ""])


if __name__ == "__main__":
    unittest.main()
