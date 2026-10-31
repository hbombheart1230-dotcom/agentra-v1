"""P15 RF-035 (20261101-07h): seven q8_evaluation_contract and one quant_shadow_candidate_evaluation bodies moved to projection Owners; parity with the pre-move bodies (stdlib unittest)."""
from __future__ import annotations

import ast
import hashlib
import inspect
import json
import unittest
from pathlib import Path
from types import MappingProxyType
from unittest import mock

from libs.reporting import q8_dedupe_candidates_projection as dedupe_owner
from libs.reporting import q8_dedupe_key_projection as key_owner
from libs.reporting import q8_entry_lane_projection as lane_owner
from libs.reporting import q8_evaluation_contract as q8c
from libs.reporting import q8_forward_base_projection as base_owner
from libs.reporting import q8_repeatable_projection as repeatable_owner
from libs.reporting import q8_text_value_projection as text_owner
from libs.reporting import q8_trust_gate_projection as gate_owner
from libs.reporting import quant_shadow_candidate_evaluation as qs
from libs.reporting import quant_shadow_range_load_projection as range_owner

GOLDENS = {
    "a1": "d9584fd6a80312f38e7652d668697f7d24c503e5b04724bbb73e7a49f9740f1c",
    "a2": "347bb2d11a5be04c0d8526c5d07305a50a86d13845d6ee8982ba7f0ce427c612",
    "a3": "7eb4ab0f63f13a7e951cfd2482955b3abe9ee3d26677b725887f1f4372fc8ac3",
    "a4": "6b348aa3ddfcf4bc582f813c3bc06a9bcca373210fa6e77259fcc5825058e724",
    "a5": "21626d16d31c6aa6358229932abfc19556f7e5f9e5b2c871172c190b90103af9",
    "a6": "d396f9259770f0fa7d8af14ab394b8c053eda978d59ee3c7d65a1a77194c98eb",
    "a7": "8b1b12283dcbf780840a515c3063f70597b2b07effcfbf293e8932be2cdea06e",
    "a8": "afb974fc16219740bc29339196c4c055d7787f1c021b57617d05e67adf39d004",
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


def _lane_fake(row):
    return {"primary_lane": row.get("lane", "trend"), "subtype": row.get("sub", "x")}


def _a1(fn, mod):
    values = [" none ", "A", None, "", "-", "NULL", " Unknown ", "not_captured", 0, 1, 1.5, True, False, [], [1], {}, "a b", _Odd(), "UNKNOWN"]
    return [_call(lambda v=v: fn(v)) for v in values] + [_call(lambda: fn())]


def _a2(fn, mod):
    inner = {"x": 1}
    res = fn({"shadow_forward_base": inner})
    out = [
        ["copy", [res == inner, res is not inner]],
        _call(lambda: fn({})),
        _call(lambda: fn({"shadow_forward_base": [1]})),
        _call(lambda: fn({"shadow_forward_base": None})),
        _call(lambda: fn(MappingProxyType({"shadow_forward_base": MappingProxyType({"m": 1})}))),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(q8c, "Mapping", tuple):
        out.append(_call(lambda: fn({"shadow_forward_base": {"a": 1}})))
    with mock.patch.object(q8c, "Mapping", dict):
        out.append(_call(lambda: fn({"shadow_forward_base": MappingProxyType({"a": 1})})))
    return out


def _a3(fn, mod):
    row = {"generated_at": "2026-11-01T00:00:00", "symbol": "005930", "shadow_forward_base": {"baseline_epoch": 42}}
    out = []
    with mock.patch.object(q8c, "build_entry_lane_observation", _lane_fake):
        out += [
            _call(lambda: fn(dict(row, lane="trend", sub="x"))),
            _call(lambda: fn(dict(row, shadow_forward_base={"baseline_epoch": "bad"}))),
            _call(lambda: fn(dict(row, shadow_forward_base={"baseline_epoch": "7.9"}))),
            _call(lambda: fn(dict(row, symbol=" abc "))),
            _call(lambda: fn(dict(row, symbol=None))),
            _call(lambda: fn({})),
            _call(lambda: fn(dict(row, shadow_forward_base={"baseline_raw_ts": "20260217T0100", "baseline_epoch": None}))),
            _call(lambda: fn(None)),
            _call(lambda: fn()),
        ]
    with mock.patch.object(q8c, "forward_base", lambda r: {"baseline_epoch": "5"}), mock.patch.object(q8c, "candidate_day", lambda r: "D"), mock.patch.object(q8c, "entry_lane_subtype", lambda r: "L"), mock.patch.object(q8c, "text_value", lambda v: "sym"):
        out.append(_call(lambda: fn(row)))
    return out


def _a4(fn, mod):
    def mk(sym, **kw):
        return dict({"generated_at": "2026-11-01T00:00:00", "symbol": sym, "shadow_forward_base": {"baseline_epoch": 1}}, **kw)

    a, b, c = mk("A", n=1), mk("A", n=2), mk("B", n=3)
    out = []
    with mock.patch.object(q8c, "build_entry_lane_observation", _lane_fake):
        res = fn([a, b, c])
        out += [
            ["copy", [res == [a, c], res[0] is not a, res[1] is not c]],
            _call(lambda: fn([a, c])),
            _call(lambda: fn([])),
            _call(lambda: fn(iter([a, b]))),
            _call(lambda: fn([a, "junk"])),
            _call(lambda: fn(None)),
            _call(lambda: fn()),
        ]
    with mock.patch.object(q8c, "canonical_dedupe_key", lambda row: ("k",)):
        out.append(_call(lambda: fn([a, b, c])))
    with mock.patch.object(q8c, "canonical_dedupe_key", lambda row: (row["n"] % 2,)):
        out.append(_call(lambda: fn([a, b, c])))
    return out


def _a5(fn, mod):
    out = [
        _call(lambda: fn({"observed_count": 50, "observed_day_count": 2, "avg_return_5m_pct": 1, "avg_return_15m_pct": 1})),
        _call(lambda: fn({"observed_count": 50, "observed_day_count": 2, "avg_return_5m_pct": 0, "avg_return_15m_pct": 1})),
        _call(lambda: fn({"observed_count": 49, "observed_day_count": 2, "avg_return_5m_pct": 1, "avg_return_15m_pct": 1})),
        _call(lambda: fn({"observed_count": 50, "observed_day_count": 1, "avg_return_5m_pct": 1, "avg_return_15m_pct": 1})),
        _call(lambda: fn({"observed_count": "50", "observed_day_count": "2", "avg_return_5m_pct": "0.5", "avg_return_15m_pct": "0.5"})),
        _call(lambda: fn({"observed_count": 50, "observed_day_count": 2, "avg_return_5m_pct": -1, "avg_return_15m_pct": 1})),
        _call(lambda: fn({"observed_count": 50, "observed_day_count": 2, "avg_return_5m_pct": 1, "avg_return_15m_pct": "bad"})),
        _call(lambda: fn({})),
        _call(lambda: fn(MappingProxyType({"observed_count": 99, "observed_day_count": 9, "avg_return_5m_pct": 2, "avg_return_15m_pct": 2}))),
        _call(lambda: fn(None)),
        _call(lambda: fn()),
    ]
    with mock.patch.object(q8c, "PROMOTION_CANDIDATE_MIN_OBSERVED", 1), mock.patch.object(q8c, "PROMOTION_CANDIDATE_MIN_DAYS", 1):
        out.append(_call(lambda: fn({"observed_count": 1, "observed_day_count": 1, "avg_return_5m_pct": 1, "avg_return_15m_pct": 1})))
    with mock.patch.object(q8c, "PROMOTION_CANDIDATE_MIN_OBSERVED", 500):
        out.append(_call(lambda: fn({"observed_count": 50, "observed_day_count": 2, "avg_return_5m_pct": 1, "avg_return_15m_pct": 1})))
    return out


def _a6(fn, mod):
    out = []
    with mock.patch.object(q8c, "build_entry_lane_observation", _lane_fake):
        out += [
            _call(lambda: fn({"lane": "trend", "sub": "pullback"})),
            _call(lambda: fn({"lane": "", "sub": ""})),
            _call(lambda: fn({"lane": " none ", "sub": "Unknown"})),
            _call(lambda: fn({})),
            _call(lambda: fn({"lane": None, "sub": 5})),
            _call(lambda: fn(None)),
            _call(lambda: fn()),
        ]
    with mock.patch.object(q8c, "build_entry_lane_observation", lambda row: {}):
        out.append(_call(lambda: fn({"lane": "x"})))
    with mock.patch.object(q8c, "build_entry_lane_observation", lambda row: (_ for _ in ()).throw(RuntimeError("boom"))):
        out.append(_call(lambda: fn({})))
    with mock.patch.object(q8c, "build_entry_lane_observation", _lane_fake), mock.patch.object(q8c, "text_value", lambda v: "T" if v else ""):
        out.append(_call(lambda: fn({"lane": "trend", "sub": "x"})))
    return out


def _watch(**kw):
    return dict({"observed_count": 60, "observed_day_count": 3, "avg_return_5m_pct": 1, "avg_return_15m_pct": 1}, **kw)


def _a7(fn, mod):
    def run(**over):
        base = dict(raw_candidate_count=100, deduped_candidate_count=100, trusted_forward_count=100, trusted_forward_coverage=0.9, candidate_watchlist=[_watch()])
        base.update(over)
        return _call(lambda: fn(**base))

    out = [
        run(),
        run(trusted_forward_count=0),
        run(trusted_forward_coverage=0.5),
        run(raw_candidate_count=1000, deduped_candidate_count=100),
        run(candidate_watchlist=[]),
        run(candidate_watchlist=[_watch(avg_return_5m_pct=0)]),
        run(raw_candidate_count=0, deduped_candidate_count=0),
        run(raw_candidate_count=10, deduped_candidate_count=20),
        run(trusted_forward_count="100", trusted_forward_coverage="0.7"),
        run(trusted_forward_coverage="bad"),
        run(candidate_watchlist=None),
        run(candidate_watchlist=[None]),
        run(raw_candidate_count=1000, deduped_candidate_count=100, trusted_forward_count=1, candidate_watchlist=[]),
        _call(lambda: fn()),
    ]
    with mock.patch.object(q8c, "TRUSTED_FORWARD_MIN_COUNT", 1), mock.patch.object(q8c, "TRUSTED_FORWARD_MIN_COVERAGE", 0.1), mock.patch.object(q8c, "DUPLICATE_RATE_MAX", 1.0):
        out.append(run(trusted_forward_count=1, trusted_forward_coverage=0.2, raw_candidate_count=5, deduped_candidate_count=1))
    with mock.patch.object(q8c, "promotion_candidate_is_repeatable", lambda row: True):
        out.append(run(candidate_watchlist=[{}], trusted_forward_count=0))
    with mock.patch.object(q8c, "TRUST_GATE_STATUS_READY", "PATCHED_READY"):
        out.append(run())
    return out


def _a8(fn, mod):
    calls = []

    def fake_iter_days(start, end):
        calls.append(["days", start, end])
        return iter(["20261101", "20261102"])

    def fake_loader(**kw):
        calls.append(["load", sorted(kw), kw["days"], kw["keys"], kw["drop_q9_row_keys"], str(kw["reports_root"])])
        return [{"id": "x"}]

    out = []
    with mock.patch.object(qs, "_iter_days", fake_iter_days), mock.patch.object(qs, "load_quant_shadow_candidate_payloads", fake_loader):
        out += [
            _call(lambda: fn(reports_root=Path("/tmp/fake/reports"), start="2026-11-01", end="2026-11-01")),
            _call(lambda: fn(reports_root="/r", start="a", end="b", keys=["candidates"], drop_q9_row_keys=["x"])),
            _call(lambda: fn(reports_root=None, start=None, end=None)),
            _call(lambda: fn(start="a", end="b")),
            _call(lambda: fn()),
        ]
    out.append(["calls", calls])
    with mock.patch.object(qs, "load_quant_shadow_candidate_payloads", lambda **kw: (_ for _ in ()).throw(RuntimeError("boom"))), mock.patch.object(qs, "_iter_days", lambda s, e: iter([])):
        out.append(_call(lambda: fn(reports_root="/r", start="a", end="b")))
    with mock.patch.object(qs, "load_quant_shadow_candidate_payloads", lambda **kw: kw["days"]):
        out.append(_call(lambda: fn(reports_root="/nonexistent-root", start="2026-10-30", end="2026-11-01")))
        out.append(_call(lambda: fn(reports_root="/nonexistent-root", start="bad", end="2026-11-01")))
        out.append(_call(lambda: fn(reports_root="/nonexistent-root", start="2026-11-02", end="2026-11-01")))
    return out


CASES = {
    "a1": (_a1, q8c, "text_value", lambda: text_owner.text_value, False, text_owner),
    "a2": (_a2, q8c, "forward_base", lambda: base_owner.forward_base, True, base_owner),
    "a3": (_a3, q8c, "canonical_dedupe_key", lambda: key_owner.canonical_dedupe_key, True, key_owner),
    "a4": (_a4, q8c, "dedupe_q8_candidates", lambda: dedupe_owner.dedupe_q8_candidates, True, dedupe_owner),
    "a5": (_a5, q8c, "promotion_candidate_is_repeatable", lambda: repeatable_owner.promotion_candidate_is_repeatable, True, repeatable_owner),
    "a6": (_a6, q8c, "entry_lane_subtype", lambda: lane_owner.entry_lane_subtype, True, lane_owner),
    "a7": (_a7, q8c, "build_q8_trust_gate", lambda: gate_owner.build_q8_trust_gate, True, gate_owner),
    "a8": (_a8, qs, "load_quant_shadow_candidate_payloads_for_range", lambda: range_owner.load_quant_shadow_candidate_payloads_for_range, True, range_owner),
}


def _run(key, which):
    scenario, mod, name, owner_factory, facade, _ = CASES[key]
    if which == "wrapper":
        fn = getattr(mod, name)
    else:
        raw = owner_factory()
        fn = (lambda *a, **k: raw(*a, facade=mod, **k)) if facade else raw
    return json.loads(json.dumps(scenario(fn, mod), default=repr))


class Test(unittest.TestCase):
    def _parity(self, key):
        a = _run(key, "wrapper")
        b = _run(key, "owner")
        self.assertEqual(a, b)
        self.assertEqual(_h(a), GOLDENS[key])
        _, mod, name, _, _, owner_mod = CASES[key]
        fn = ast.parse(inspect.getsource(getattr(mod, name))).body[0]
        stmts = [n for n in fn.body if not (isinstance(n, ast.Expr) and isinstance(getattr(n, "value", None), ast.Constant))]
        self.assertTrue(len(stmts) == 1 and isinstance(stmts[0], ast.Return))
        self.assertNotIn("import " + mod.__name__.split(".")[-1], inspect.getsource(owner_mod))
        return a

    def test_a1_text_value(self):
        out = self._parity("a1")
        self.assertEqual(q8c.text_value(" none "), "")
        self.assertEqual(q8c.text_value("A"), "A")
        self.assertEqual(out[-2][0], "ok")

    def test_a2_forward_base(self):
        out = self._parity("a2")
        self.assertEqual(q8c.forward_base({"shadow_forward_base": {"x": 1}}), {"x": 1})
        self.assertEqual(q8c.forward_base({}), {})
        self.assertEqual(out[0], ["copy", [True, True]])

    def test_a3_canonical_dedupe_key(self):
        out = self._parity("a3")
        self.assertEqual(out[0], ["ok", ["20261101", "005930", 42, "trend:x"]])
        self.assertEqual(out[1][1][2], 0)

    def test_a4_dedupe_q8_candidates(self):
        out = self._parity("a4")
        self.assertEqual(out[0], ["copy", [True, True, True]])
        self.assertEqual(out[-2], ["ok", [{"generated_at": "2026-11-01T00:00:00", "symbol": "A", "shadow_forward_base": {"baseline_epoch": 1}, "n": 1}]])

    def test_a5_promotion_candidate_is_repeatable(self):
        out = self._parity("a5")
        self.assertEqual(out[0], ["ok", True])
        self.assertEqual(out[1], ["ok", False])

    def test_a6_entry_lane_subtype(self):
        out = self._parity("a6")
        self.assertEqual(out[0], ["ok", "trend:pullback"])
        self.assertEqual(out[-3], ["ok", "unknown:unknown"])

    def test_a7_build_q8_trust_gate(self):
        out = self._parity("a7")
        self.assertEqual((out[0][1]["status"], out[0][1]["promotion_allowed"]), ("promotion_review_ready", True))
        self.assertEqual(out[1][1]["status"], "promotion_blocked_sample_or_coverage")
        self.assertEqual(out[4][1]["status"], "promotion_blocked_no_repeatable_candidate")
        self.assertEqual(out[-1][1]["status"], "PATCHED_READY")

    def test_a8_load_quant_shadow_candidate_payloads_for_range(self):
        out = self._parity("a8")
        self.assertEqual(out[0], ["ok", [{"id": "x"}]])
        self.assertEqual(out[-4][0], "exc")
        self.assertEqual(out[-3][1], ["2026-10-30", "2026-10-31", "2026-11-01"])


if __name__ == "__main__":
    unittest.main()
