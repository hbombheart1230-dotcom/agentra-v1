"""P15 RF-014 closeout G2 seam (20261101-12h): bounded fake-only evidence for the read-only Scanner repeat/risk/NOOP-facing pure functions.

This is NOT proof of the full RF-009 caller or an actual runtime NOOP: only the pure functions below are exercised.
"""
from __future__ import annotations

import unittest

from libs.agents.scanner.candidate_risk import resolve_candidate_base_risk
from libs.agents.scanner.policy import repeat_guard
from libs.agents.scanner.projections.control_eligibility import build_full_strategist_control_eligibility


class ScannerRepeatRiskNoopSeamTests(unittest.TestCase):
    def test_resolve_candidate_base_risk(self):
        explicit = resolve_candidate_base_risk(scanner_row={"risk_score": 0.25})
        self.assertEqual((explicit["risk_score"], explicit["source"]), (0.25, "scanner_row"))
        self.assertEqual(explicit["missing_inputs"], [])
        fallback = resolve_candidate_base_risk()
        self.assertEqual(fallback["source"], "market_data_fallback")
        self.assertEqual(fallback, resolve_candidate_base_risk())  # deterministic
        self.assertEqual(resolve_candidate_base_risk(candidate={"risk_score": 0.4})["source"], "candidate")

    def test_normalize_scanner_blocker_family(self):
        f = repeat_guard._normalize_scanner_blocker_family_r3_impl
        self.assertEqual(f("risk_blocked", facade=repeat_guard), "risk_guard")
        self.assertEqual(f("none", facade=repeat_guard), "")
        self.assertEqual(f("", facade=repeat_guard), "")
        self.assertEqual(f("mixed", facade=repeat_guard), "")

    def test_full_strategist_control_eligibility_is_observation_only(self):
        result = build_full_strategist_control_eligibility({})
        self.assertEqual(result["behavior_effect"], "observation_only")
        self.assertIs(result["eligible"], False)
        self.assertNotIn("action", result)
        self.assertNotIn("order", result)


if __name__ == "__main__":
    unittest.main()
