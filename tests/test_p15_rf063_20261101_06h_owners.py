import tempfile,unittest
from pathlib import Path
from scripts.diagnostics import run_m26_dataset_manifest_check as m
from scripts.diagnostics import run_m26_closeout_check as c

class T(unittest.TestCase):
 def test_b1_utc_now_iso(self): self.assertTrue(m._utc_now_iso().endswith('+00:00'))
 def test_b2_write_text(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'a/b';m._write_text(p,'x');self.assertEqual(p.read_text(),'x')
 def test_b4__validate_dataset(self):
  with tempfile.TemporaryDirectory() as d:
   self.assertIn('missing:manifest.json',m._validate_dataset(Path(d))['failures'])
 def test_b5_build_parser(self):
  x=m._build_parser().parse_args(['--seed-demo','--json']);self.assertTrue(x.seed_demo and x.json)
 def test_b6_build_parser(self):
  x=c._build_parser().parse_args(['--day','2026-11-01','--json']);self.assertEqual((x.day,x.json),('2026-11-01',True))
 def test_b7_run_manifest_json(self):
  seen=[];c._run_json=lambda fn,a:(seen.append(a) or (0,{'ok':True}));self.assertEqual(c._run_manifest_json(dataset_root=Path('/tmp/fake'),seed_demo=True),(0,{'ok':True}));self.assertIn('--seed-demo',seen[0])
 def test_b8_run_replay_json(self):
  seen=[];c._run_json=lambda fn,a:(seen.append(a) or (0,{}));c._run_replay_json(dataset_root=Path('/tmp/fake'),day='2026-11-01');self.assertEqual(seen[0][-2:],['--day','2026-11-01'])
if __name__=='__main__':unittest.main()
