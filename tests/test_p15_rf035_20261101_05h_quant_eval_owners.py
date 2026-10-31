"""P15 RF-035 (20261101-05h): eight quant_tactic_evaluation helpers moved to projection Owners; parity with the pre-move bodies (stdlib unittest)."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import unittest
from types import MappingProxyType
from unittest import mock

from libs.reporting import quant_tactic_eval_closed_projection as closed_owner
from libs.reporting import quant_tactic_eval_field_gaps_projection as gaps_owner
from libs.reporting import quant_tactic_eval_int_projection as int_owner
from libs.reporting import quant_tactic_eval_invalid_examples_projection as examples_owner
from libs.reporting import quant_tactic_eval_invalid_reason_projection as reason_owner
from libs.reporting import quant_tactic_eval_rows_projection as rows_owner
from libs.reporting import quant_tactic_eval_text_projection as text_owner
from libs.reporting import quant_tactic_eval_valid_rows_projection as valid_owner
from libs.reporting import quant_tactic_evaluation as qe

GOLDENS = {
    "a1": "da22e555ee4231d517b183f508ac1aa44900b151ef1070afc4eed43ad7e156b0",
    "a2": "b4fde43ec09800dbee87645746bcf5b2a97c97e26ccbaf6f871bc465a57708fe",
    "a3": "54fb7ad720b4290edead723865a9d91b99fb2e80fc402bd8a3100c6cfa35d81b",
    "a4": "b248af7abfdf84d004dc5df79e197bbf1b704381b631e11e576b2b7d65028e6c",
    "a5": "57cdeb51272e08ea9d2dc98fb3e8ba9303871c9d79127016805d47de6133e773",
    "a6": "eead57497fb42bccb3f5774570d77eef37c230374a9faa382d65cd70aa13e727",
    "a7": "c018dd7623074a601ebebb750232c279a89992692e3f6689e3a1ebd713d25b83",
    "a8": "e091a42fec31c23a19ffea4a510db31d32ae04fa5b9bc3fbf5d5123bb5297bd5",
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

    def __str__(self):
        return " Odd "


def _a1(fn, mod):
    values = [" X ", " unknown ", None, "", "-", "NONE", " Null ", "not_captured", 0, 1, 1.5, True, False, [], [1], {}, "a b", _Odd(), "UNKNOWN"]
    return [_call(lambda v=v: fn(v)) for v in values] + [_call(lambda: fn())]


def _a2(fn, mod):
    out = [
        _call(lambda: fn("3.9")),
        _call(lambda: fn("bad", 4)),
        _call(lambda: fn("bad", "x")),
        _call(lambda: fn(None)),
        _call(lambda: fn(None, 7)),
        _call(lambda: fn("")),
        _call(lambda: fn(-2.7)),
        _call(lambda: fn("1e3")),
        _call(lambda: fn(float("inf"))),
        _call(lambda: fn(float("nan"), 2)),
        _call(lambda: fn(True)),
        _call(lambda: fn([])),
        _call(lambda: fn("5", default=None)),
        _call(lambda: fn("bad", 2.9)),
        _call(lambda: fn(" 12 ")),
        _call(lambda: fn()),
    ]
    return out


def _a3(fn, mod):
    rows = [
        {"status": "closed"}, {"status": "partial", "action": "SELL"}, {}, {"is_closed_trade": 1}, {"is_realized_nonclosed_exit": "x"},
        {"status": "partial"}, {"status": "closed", "trade_origin": "recovered_partial"}, {"trade_origin": "recovered_partial", "last_action": "sell"},
        {"last_status": " CLOSED "}, {"status": "open", "last_action": "SELL"}, {"action": "SELL", "status": "partial"}, {"status": None, "last_status": "closed"},
        {"status": 5}, {"last_action": ["SELL"]}, MappingProxyType({"status": "closed"}), [], None,
    ]
    return [_call(lambda r=r: fn(r)) for r in rows] + [_call(lambda: fn())]


def _a4(fn, mod):
    src = {"status": "closed", "trade_id": "T"}
    rows = [src, {"status": "open"}, "junk", None, MappingProxyType({"status": "closed"}), {"is_closed_trade": True}]
    res = fn(rows)
    out = [
        ["copy", [res[0] == src, res[0] is not src, len(res)]],
        _call(lambda: fn([])),
        _call(lambda: fn(iter(rows))),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(qe, "_closed_or_realized", lambda row: row.get("status") == "open"):
        out.append(_call(lambda: fn(rows)))
    with mock.patch.object(qe, "Mapping", tuple):
        out.append(_call(lambda: fn(rows)))
    return out


def _a5(fn, mod):
    out = [
        _call(lambda: fn({"broker_alignment_status": "bad"})),
        _call(lambda: fn({"broker_alignment_status": "OK"})),
        _call(lambda: fn({"broker_alignment_missing_in_local_total": 1})),
        _call(lambda: fn({"broker_alignment_missing_in_broker_total": "2"})),
        _call(lambda: fn({"broker_account_snapshot_status": "stale"})),
        _call(lambda: fn({"broker_account_snapshot_status": " Ok "})),
        _call(lambda: fn({"broker_alignment_account_snapshot_error_count": 3})),
        _call(lambda: fn({})),
        _call(lambda: fn({"broker_alignment_status": "bad", "broker_alignment_missing_in_local_total": 1})),
        _call(lambda: fn({"broker_alignment_missing_in_local_total": 1, "broker_alignment_missing_in_broker_total": 1})),
        _call(lambda: fn({"broker_alignment_missing_in_broker_total": 1, "broker_account_snapshot_status": "x"})),
        _call(lambda: fn({"broker_alignment_status": "unknown"})),
        _call(lambda: fn({"broker_alignment_missing_in_local_total": "bad"})),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(qe, "_text", lambda v: "patched" if v else ""):
        out.append(_call(lambda: fn({"broker_alignment_status": "x"})))
    with mock.patch.object(qe, "_int", lambda v, default=0: 5):
        out.append(_call(lambda: fn({})))
    return out


def _a6(fn, mod):
    rows = [{"broker_alignment_status": "bad"}, {}, {"broker_alignment_missing_in_local_total": 1}, {"x": 1}]
    out = [
        _call(lambda: fn(rows)),
        _call(lambda: fn([])),
        _call(lambda: fn(iter(rows))),
        _call(lambda: fn([None])),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    res = fn(rows)
    out.append(["identity", [res[0] is rows[1], res[1] is rows[3], res is not rows]])
    with mock.patch.object(qe, "_invalid_sample_reason", lambda row: "r" if row.get("x") else ""):
        out.append(_call(lambda: fn(rows)))
    return out


def _a7(fn, mod):
    bad = {"trade_id": "T", "symbol": "S", "broker_alignment_status": "bad"}
    rows = [bad, {}, dict(bad, trade_id=" unknown "), dict(bad, symbol=None), dict(bad, broker_alignment_status="worse"), {"broker_alignment_missing_in_local_total": 1, "trade_id": "Z"}]
    out = [
        _call(lambda: fn([bad])),
        _call(lambda: fn([bad], limit=0)),
        _call(lambda: fn(rows)),
        _call(lambda: fn(rows, limit=2)),
        _call(lambda: fn(rows, limit=1)),
        _call(lambda: fn(rows, limit=-1)),
        _call(lambda: fn([])),
        _call(lambda: fn(iter(rows), limit=3)),
        _call(lambda: fn([None])),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
        _call(lambda: fn(rows, limit="x")),
    ]
    with mock.patch.object(qe, "_invalid_sample_reason", lambda row: "R"):
        out.append(_call(lambda: fn([{"trade_id": "a"}, {"trade_id": "b"}], limit=1)))
    with mock.patch.object(qe, "_text", lambda v: "T"):
        out.append(_call(lambda: fn([bad])))
    return out


def _a8(fn, mod):
    full = {"quant_tactic_id": "X", "entry_quant_decision": "go", "exit_quant_decision": "", "tactic_suitability_tier": "none", "entry_quant_cost_floor_state": "ok"}
    out = [
        _call(lambda: fn([{"quant_tactic_id": "X"}])),
        _call(lambda: fn([])),
        _call(lambda: fn([full, full, {}])),
        _call(lambda: fn([full] * 10)),
        _call(lambda: fn([full] * 9 + [{}])),
        _call(lambda: fn([None])),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(qe, "_REQUIRED_FIELDS", ("a", "b")):
        out.append(_call(lambda: fn([{"a": 1}, {"b": "x"}])))
    with mock.patch.object(qe, "_FIELD_COVERAGE_FLOOR", 0.5):
        out.append(_call(lambda: fn([{"quant_tactic_id": "X"}, {}])))
    with mock.patch.object(qe, "_text", lambda v: "T"):
        out.append(_call(lambda: fn([{}, {}])))
    return out


CASES = {
    "a1": (_a1, "_text", lambda: text_owner._text, False, text_owner),
    "a2": (_a2, "_int", lambda: int_owner._int, False, int_owner),
    "a3": (_a3, "_closed_or_realized", lambda: closed_owner._closed_or_realized, False, closed_owner),
    "a4": (_a4, "_evaluation_rows", lambda: rows_owner._evaluation_rows, True, rows_owner),
    "a5": (_a5, "_invalid_sample_reason", lambda: reason_owner._invalid_sample_reason, True, reason_owner),
    "a6": (_a6, "_valid_evaluation_rows", lambda: valid_owner._valid_evaluation_rows, True, valid_owner),
    "a7": (_a7, "_invalid_sample_examples", lambda: examples_owner._invalid_sample_examples, True, examples_owner),
    "a8": (_a8, "_field_gap_rows", lambda: gaps_owner._field_gap_rows, True, gaps_owner),
}


def _run(key, which):
    scenario, name, owner_factory, facade, _ = CASES[key]
    if which == "wrapper":
        fn = getattr(qe, name)
    else:
        raw = owner_factory()
        fn = (lambda *a, **k: raw(*a, facade=qe, **k)) if facade else raw
    return json.loads(json.dumps(scenario(fn, qe), default=repr))


class Test(unittest.TestCase):
    def _parity(self, key):
        a = _run(key, "wrapper")
        b = _run(key, "owner")
        self.assertEqual(a, b)
        self.assertEqual(_h(a), GOLDENS[key])
        name, owner_mod = CASES[key][1], CASES[key][4]
        fn = ast.parse(inspect.getsource(getattr(qe, name))).body[0]
        stmts = [n for n in fn.body if not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
        self.assertTrue(len(stmts) == 1 and isinstance(stmts[0], ast.Return))
        self.assertNotIn("import quant_tactic_evaluation", inspect.getsource(owner_mod))
        return a

    def test_a1_text(self):
        self._parity("a1")
        self.assertEqual(qe._text(" X "), "X")
        self.assertEqual(qe._text(" unknown "), "")
        self.assertEqual(qe._text(None), "")

    def test_a2_int(self):
        out = self._parity("a2")
        self.assertEqual(qe._int("3.9"), 3)
        self.assertEqual(qe._int("bad", 4), 4)
        self.assertEqual(out[2][0], "exc")

    def test_a3_closed_or_realized(self):
        self._parity("a3")
        self.assertIs(qe._closed_or_realized({"status": "closed"}), True)
        self.assertIs(qe._closed_or_realized({"status": "partial", "action": "SELL"}), True)
        self.assertIs(qe._closed_or_realized({}), False)

    def test_a4_evaluation_rows(self):
        out = self._parity("a4")
        self.assertEqual(qe._evaluation_rows([{"status": "closed", "trade_id": "T"}, {"status": "open"}]), [{"status": "closed", "trade_id": "T"}])
        self.assertEqual(out[0][1][0:2], [True, True])

    def test_a5_invalid_sample_reason(self):
        self._parity("a5")
        self.assertEqual(qe._invalid_sample_reason({"broker_alignment_status": "bad"}), "broker_alignment_bad")
        self.assertEqual(qe._invalid_sample_reason({"broker_alignment_missing_in_local_total": 1}), "broker_missing_in_local")
        self.assertEqual(qe._invalid_sample_reason({}), "")

    def test_a6_valid_evaluation_rows(self):
        out = self._parity("a6")
        self.assertEqual(qe._valid_evaluation_rows([{"broker_alignment_status": "bad"}, {}]), [{}])
        self.assertEqual(out[-2], ["identity", [True, True, True]])

    def test_a7_invalid_sample_examples(self):
        out = self._parity("a7")
        self.assertEqual(
            qe._invalid_sample_examples([{"trade_id": "T", "symbol": "S", "broker_alignment_status": "bad"}]),
            [{"trade_id": "T", "symbol": "S", "reason": "broker_alignment_bad"}],
        )
        self.assertEqual(len(out[1][1]), 1)  # limit=0 still appends one row before the break check (original behavior)
        self.assertEqual(len(out[3][1]), 2)

    def test_a8_field_gap_rows(self):
        out = self._parity("a8")
        rows = qe._field_gap_rows([{"quant_tactic_id": "X"}])
        self.assertEqual(len(rows), 5)
        self.assertEqual((rows[0]["field"], rows[0]["coverage"]), ("quant_tactic_id", 1.0))
        self.assertTrue(all(r["coverage"] == 0.0 for r in rows[1:]))
        self.assertTrue(all(r["coverage"] == 0.0 for r in qe._field_gap_rows([])))
        self.assertEqual(out[1][0], "ok")


if __name__ == "__main__":
    unittest.main()
