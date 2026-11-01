import unittest
from scripts.diagnostics import run_m27_allocation_policy_check as a
from scripts.diagnostics import run_m27_conflict_resolution_check as c
class T(unittest.TestCase):
 def test_b4__build_parser(self):self.assertEqual(a._build_parser().parse_args([]).total_notional,1000000)
 def test_b5__default_profiles(self):self.assertEqual(len(a._default_profiles()),3)
 def test_b6__build_parser(self):self.assertTrue(c._build_parser().parse_args(['--json']).json)
 def test_b8__default_caps(self):self.assertEqual(c._default_caps(inject_fail=False)['000660'],200.)
if __name__=='__main__':unittest.main()
