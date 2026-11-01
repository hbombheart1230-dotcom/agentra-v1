import unittest,tempfile
from pathlib import Path
from scripts.diagnostics import run_m26_replay_runner as r
from scripts.diagnostics import run_m26_closeout_check as c
class T(unittest.TestCase):
 def test_b1__write_jsonl(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'x/a';c._write_jsonl(p,[{'x':1}]);self.assertIn('"x": 1',p.read_text())
 def test_b2__run_json(self):
  c.capture_cli_json=lambda f,a:(0,{'ok':True});self.assertEqual(c._run_json(lambda:0,['--json']),(0,{'ok':True}))
 def test_b3__run_scorecard_json(self):
  seen=[];c._run_json=lambda f,a:(seen.append(a) or (0,{}));c._run_scorecard_json(dataset_root=Path('/x'),day='d');self.assertIn('--day',seen[0])
 def test_b4__run_ab_eval_json(self):
  seen=[];c._run_json=lambda f,a:(seen.append(a) or (0,{}));c._run_ab_eval_json(base_root=Path('/a'),candidate_root=Path('/b'),day='d');self.assertIn('candidate',seen[0])
 def test_b5__run_gate_json(self):
  seen=[];c._run_json=lambda f,a:(seen.append(a) or (0,{}));c._run_gate_json(base_root=Path('/a'),candidate_root=Path('/b'),day='',min_delta_total_pnl_proxy=1.5);self.assertIn('1.5',seen[0])
 def test_b7__to_epoch(self):self.assertEqual(r._to_epoch('1970-01-01T00:00:01Z'),1);self.assertEqual(r._to_epoch('1'),1);self.assertIsNone(r._to_epoch('bad'))
 def test_b8__num_summary(self):self.assertEqual(r._num_summary([1.,2.,3.]),{'count':3.,'avg':2.,'p50':2.,'p95':3.,'max':3.});self.assertEqual(r._num_summary([])['count'],0.)
if __name__=='__main__':unittest.main()
