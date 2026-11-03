# C01 — Codex B | ORDER_ID=B-20261103-10-C03 | RF-063 DEV | B43 NEW_READY=8/8 | B42 REMOTE_DONE=8/8 | RESERVE_NOT_VERIFIED

## 2026-11-03 역할별 Agentra 스킬 적용
`agentra-rf-executor` 실행 체크리스트를 적용하고 `agentra-contract-guard`로 변경 대상의 Owner/안전 경계를 확인한다. 스킬은 본 C01 주문 밖 신규 과제를 허용하지 않으며, 자동 로딩이 확인되지 않으면 `.agents/skills/<skill-name>/SKILL.md`를 참고 자료로만 사용한다.

---

## 2026-11-03 LEAD CORRECTION — B execution accountability (D00 subordinate)
Complete any already-started B43 safe items without retroactive cancellation. Before each item check its actual RF FIRST_UNMET and whether the item can close it; report `GATE_IMPACT=YES/NO` honestly. BODY MOVE and targeted PASS never imply whole RF G1/G3/DONE. If a pinned item is already complete, unsafe, or drifted, record precise blocker and continue other safe items; do not invent a replacement or touch protected resolver/operational code. Deliver exact source/target/test SHA and remote push to #12. C03 must provide next gate-closing work; do not self-assign. No repeated prior PASS or dummy commits.

---

## START / PROTECTION
Fetch this file directly from `integration/p1.5`, log exact C01 blob/canonical HEAD/B branch HEAD to #12. Finish any genuinely in-progress prior starting order before this order; do not redo B42. B42 #12 6591950111 remote `abd03cbf09ed4b8e19eea53765babf4c6e7497f1`, 8/8, normal EXIT0 PASS5; C04 #36 6592259700 selected 13/13 to integration `11f8ee2d074dd21e98ea3725ce0d6cca540435f0`. First shell `python -m pytest --version`, install `python -m pip install --user pytest` only if missing, recheck. A/B never self-select RF, never reread D00/RF/INDEX/SKILL. Code/test edits only on B branch `work/p15-b-operator-structure-20261022`, non-force push. Preserve operational/Guard/Step5C/UEF/real trading and all go-live effects: **do not call main, live subprocess, real logs, reports, network or real signoff**. C03 only assigns read-only pure body extraction. RF-063 whole G3 remains blocked by `llm_artifacts.py` resolver/consumer canonical-vs-B drift; do not touch resolver; C04/C05 own closure.

## B43 — 8 independent BODY MOVEs, all mandatory
For each item, verify exact pinned SOURCE blob on current B and canonical, TARGET 404 on both; if drift/already moved, report item-specific FIRST_BLOCKER and continue all other safe items. Move **actual calculation body** into the one named Owner, leave thin original signature wrapper, preserve call-time monkeypatch, exception, IO and output bytes. No duplicate calculation or dummy wrapper. Original pinned AST vs new Owner+facade parity using fake-only fixtures.

### B43-1 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_run_json` | SOURCE_BLOB=`5f8287986ce9569cc00a8e337740762bd4713e3c`
TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_run_json.py::_run_json` | TARGET=404 canonical+B at assignment
BODY/TEST=fake main_fn stdout, JSON parse and rc parity; no real main; preserve exact signature, wrapper and error behavior; fake-only targeted normal parity.

### B43-2 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_read_json` | SOURCE_BLOB=`5f8287986ce9569cc00a8e337740762bd4713e3c`
TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_read_json.py::_read_json` | TARGET=404 canonical+B at assignment
BODY/TEST=tmp_path dict/non-dict/malformed JSON and exception parity; preserve exact signature, wrapper and error behavior; fake-only targeted normal parity.

### B43-3 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_gitignore_has_env` | SOURCE_BLOB=`5f8287986ce9569cc00a8e337740762bd4713e3c`
TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_gitignore_has_env.py::_gitignore_has_env` | TARGET=404 canonical+B at assignment
BODY/TEST=fake .gitignore/.env text, no credentials; preserve exact signature, wrapper and error behavior; fake-only targeted normal parity.

### B43-4 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_item` | SOURCE_BLOB=`5f8287986ce9569cc00a8e337740762bd4713e3c`
TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_item.py::_item` | TARGET=404 canonical+B at assignment
BODY/TEST=pure keyword-only item builder, exact defaults/order; preserve exact signature, wrapper and error behavior; fake-only targeted normal parity.

### B43-5 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_release_signoff_checklist.py::_build_parser` | SOURCE_BLOB=`5f8287986ce9569cc00a8e337740762bd4713e3c`
TARGET=`scripts/diagnostics/run_m30_release_signoff_checklist_build_parser.py::_build_parser` | TARGET=404 canonical+B at assignment
BODY/TEST=argparse construction and fake argv only, never main; preserve exact signature, wrapper and error behavior; fake-only targeted normal parity.

### B43-6 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_final_golive_signoff.py::_build_markdown` | SOURCE_BLOB=`20c5ba5c9d94bf3d1b2fb43bee6206df18872271`
TARGET=`scripts/diagnostics/run_m30_final_golive_signoff_build_markdown.py::_build_markdown` | TARGET=404 canonical+B at assignment
BODY/TEST=pure in-memory Markdown bytes, failure list and numeric parity; preserve exact signature, wrapper and error behavior; fake-only targeted normal parity.

### B43-7 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_final_golive_signoff.py::_run_json` | SOURCE_BLOB=`20c5ba5c9d94bf3d1b2fb43bee6206df18872271`
TARGET=`scripts/diagnostics/run_m30_final_golive_signoff_run_json.py::_run_json` | TARGET=404 canonical+B at assignment
BODY/TEST=injected fake callable only, stdout capture/rc/json parity; never invoke real signoff; preserve exact signature, wrapper and error behavior; fake-only targeted normal parity.

### B43-8 | RF-063 | NEW_BODY_MOVE
SOURCE=`scripts/diagnostics/run_m30_final_golive_signoff.py::_build_parser` | SOURCE_BLOB=`20c5ba5c9d94bf3d1b2fb43bee6206df18872271`
TARGET=`scripts/diagnostics/run_m30_final_golive_signoff_build_parser.py::_build_parser` | TARGET=404 canonical+B at assignment
BODY/TEST=argparse parser fake argv/defaults only, never invoke main; preserve exact signature, wrapper and error behavior; fake-only targeted normal parity.

## TEST / PUSH / ACCEPTANCE
New test `tests/test_p15_rf063_20261103_10h_signoff_readonly_owners.py` must be absent before creation; write targeted fake-only parity for all eight, including stdout capture, dict/JSON error cases, parser defaults, Markdown exact bytes, call-time injected functions. `python -m py_compile` all changed files EXIT0 and `python -m pytest -q tests/test_p15_rf063_20261103_10h_signoff_readonly_owners.py` normal EXIT0. No real main/side effects. Before push verify staged manifest SOURCE2 + Owner8 + test1 = 11 paths, full-root tree intact, no other files. Non-force B push or authorized expected-head CAS; re-fetch remote HEAD/tree and all 11 blobs. #12 report each B43-1..8 DONE or exact BLOCKED with SOURCE/TARGET/blob/FIRST_BLOCKER, actual START_KST/END_KST/ELAPSED_MIN, command/EXIT/PASS, remote SHA. If environment blocks pytest/push, continue safe items and distinguish LOCAL_ONLY from G1. C04 alone integration/G3, C05 alone RF/STATUS/DONE. No documents, CI, protected state or operational edits.
