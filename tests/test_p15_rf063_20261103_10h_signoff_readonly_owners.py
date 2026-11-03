from __future__ import annotations
import json
from pathlib import Path
import pytest
from scripts.diagnostics import run_m30_final_golive_signoff as golive
from scripts.diagnostics import run_m30_release_signoff_checklist as checklist
from scripts.diagnostics import run_m30_final_golive_signoff_build_markdown as golive_markdown
from scripts.diagnostics import run_m30_final_golive_signoff_build_parser as golive_parser
from scripts.diagnostics import run_m30_final_golive_signoff_run_json as golive_run_json
from scripts.diagnostics import run_m30_release_signoff_checklist_build_parser as checklist_parser
from scripts.diagnostics import run_m30_release_signoff_checklist_gitignore_has_env as gitignore_owner
from scripts.diagnostics import run_m30_release_signoff_checklist_item as item_owner
from scripts.diagnostics import run_m30_release_signoff_checklist_read_json as read_json_owner
from scripts.diagnostics import run_m30_release_signoff_checklist_run_json as run_json_owner
def test_checklist_helpers_keep_fake_only_behaviors(tmp_path: Path):
    seen=[]
    def fake_main(argv): seen.append(argv); print(json.dumps({"ok":True})); return 7
    assert checklist._run_json(fake_main,["--fake"]) == (7,{"ok":True}); assert seen == [["--fake"]]
    good=tmp_path/"good.json"; good.write_text('{"x":1}',encoding="utf-8"); bad=tmp_path/"bad.json"; bad.write_text("[]",encoding="utf-8")
    assert checklist._read_json(good)=={"x":1}; assert checklist._read_json(bad)=={}; assert checklist._read_json(tmp_path/"missing")=={}
    (tmp_path/".gitignore").write_text(".env\n",encoding="utf-8"); assert checklist._gitignore_has_env(tmp_path)
    assert checklist._item(item_id="x",category="c",title="t",passed=1,evidence=2)=={"id":"x","category":"c","title":"t","required":True,"passed":True,"evidence":"2"}
    assert checklist._build_parser().parse_args(["--day","fake","--json"]).day == "fake"
def test_golive_helpers_keep_fake_stdout_markdown_and_parser():
    def fake_main(argv): print("not json"); return 3
    assert golive._run_json(fake_main,[]) == (3,{})
    out={"day":"fake","approved":False,"go_live_decision":"hold_go_live","failure_total":1,"m30_1_quality_gates":{"rc":1,"ok":False},"m30_2_signoff":{"rc":2,"release_ready":False},"m30_3_policy":{"rc":3,"escalation_level":"hold"},"failures":["fake failure"]}
    assert golive._build_markdown(out).endswith("- fake failure\n"); assert golive._build_parser().parse_args(["--day","fake","--no-clear"]).no_clear
def test_owner_facades_preserve_call_time_dependencies(tmp_path: Path):
    (tmp_path/".gitignore").write_text(".env\n",encoding="utf-8"); assert gitignore_owner._gitignore_has_env(tmp_path,facade=checklist); assert read_json_owner._read_json(tmp_path/"missing",facade=checklist)=={}
    assert item_owner._item(item_id="i",category="c",title="t",passed=False,evidence="e",facade=checklist)["required"]
    assert checklist_parser._build_parser(facade=checklist).parse_args([]).json is False; assert golive_parser._build_parser(facade=golive).parse_args([]).json is False
    assert run_json_owner._run_json(lambda _:0,[],facade=checklist)==(0,{}); assert golive_run_json._run_json(lambda _:0,[],facade=golive)==(0,{})
    assert golive_markdown._build_markdown({"failures":[]},facade=golive).endswith("- (none)\n")
def test_keyword_only_item_contract_is_preserved():
    with pytest.raises(TypeError): checklist._item("i","c","t",True,"e")
