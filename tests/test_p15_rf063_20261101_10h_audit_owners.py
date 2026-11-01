import unittest
from scripts.diagnostics import check_audit_trail_completeness as a
class T(unittest.TestCase):
 def test_b1_to_epoch(self):self.assertEqual(a._to_epoch('1970-01-01T00:00:01Z'),1);self.assertIsNone(a._to_epoch(None))
 def test_b2_utc_day(self):self.assertEqual(a._utc_day(1),'1970-01-01')
 def test_b3_extract_ts(self):self.assertEqual(a._extract_ts({'ts':0,'payload':{'ts':42}}),42)
 def test_b4_extract_decision_action(self):self.assertEqual(a._extract_decision_action({'payload':{'decision_packet':{'intent':{'action':'buy'}}}}),'BUY')
 def test_b5_extract_allowed(self):self.assertTrue(a._extract_allowed({'payload':{'allowed':True}}));self.assertIsNone(a._extract_allowed({'payload':{'allowed':1}}))
 def test_b6_latest_day(self):self.assertEqual(a._latest_day([{'_day':'2026-10-30'},{'_day':'2026-11-01'}]),'2026-11-01')
 def test_k2__build_parser(self):self.assertEqual(a._build_parser().parse_args([]).event_log_path,'data/logs/events.jsonl')
if __name__=='__main__':unittest.main()
