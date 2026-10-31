import unittest
from scripts.diagnostics import run_m26_replay_runner as r
class T(unittest.TestCase):
 def test_b7__to_epoch(self):self.assertEqual(r._to_epoch('1970-01-01T00:00:01Z'),1);self.assertEqual(r._to_epoch('1'),1);self.assertIsNone(r._to_epoch('bad'))
 def test_b8__num_summary(self):self.assertEqual(r._num_summary([1.,2.,3.]),{'count':3.,'avg':2.,'p50':2.,'p95':3.,'max':3.});self.assertEqual(r._num_summary([])['count'],0.)
if __name__=='__main__':unittest.main()
