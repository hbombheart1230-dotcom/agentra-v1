import ast, io, unittest
from pathlib import Path
from unittest.mock import patch
from scripts.diagnostics import check_metrics_schema_v1 as schema
from scripts.diagnostics import run_m26_ab_evaluation as ab

class Owners(unittest.TestCase):
 def thin(self, mod, name):
  n=next(x for x in ast.parse(Path(mod.__file__).read_text()).body if isinstance(x,ast.FunctionDef) and x.name==name)
  self.assertEqual(len(n.body),2);self.assertIsInstance(n.body[-1],ast.Return)
 def test_b1_is_dict(self): self.assertTrue(schema._is_dict({}));self.assertFalse(schema._is_dict([]));self.thin(schema,'_is_dict')
 def test_b2_is_list(self): self.assertTrue(schema._is_list([]));self.assertFalse(schema._is_list({}));self.thin(schema,'_is_list')
 def test_b3_build_parser(self):
  x=schema._build_parser().parse_args(['--day','2026-11-01','--json']);self.assertEqual((x.day,x.json),('2026-11-01',True));self.thin(schema,'_build_parser')
 def test_b4_as_float(self): self.assertEqual(ab._as_float('2.5'),2.5);self.assertEqual(ab._as_float('bad',3),3.0);self.thin(ab,'_as_float')
 def test_b5_json_path_get(self): self.assertEqual(ab._json_path_get({'a':{'b':2}},'a.b'),2.0);self.assertEqual(ab._json_path_get({},'x',3),3.0);self.thin(ab,'_json_path_get')
 def test_b6_build_parser(self):
  x=ab._build_parser().parse_args(['--a-label','X','--json']);self.assertEqual((x.a_label,x.json),('X',True));self.thin(ab,'_build_parser')
 def test_b7_compare_metrics(self):
  a={'total_pnl_proxy':10,'risk_adjusted':{'sortino_proxy':1,'sharpe_proxy':1},'drawdown':{'max_drawdown_ratio':.2},'win_rate':.4};b={'total_pnl_proxy':12,'risk_adjusted':{'sortino_proxy':2,'sharpe_proxy':2},'drawdown':{'max_drawdown_ratio':.1},'win_rate':.6}
  x=ab._compare_metrics(a_label='A',b_label='B',a_score=a,b_score=b);self.assertEqual((x['winner'],x['points']['B'],x['promotion_gate']['recommended_action']),('B',5,'promote_B'));self.thin(ab,'_compare_metrics')
 def test_b8_run_scorecard_json(self):
  def fake(argv): print('{"ok":true}'); return 0
  with patch.object(ab,'scorecard_main',fake): self.assertEqual(ab._run_scorecard_json(dataset_root=Path('/fake'),day=''),(0,{'ok':True}))
  self.thin(ab,'_run_scorecard_json')
if __name__=='__main__':unittest.main()
