## ACTIVE ORDER B44 — RF-063 resolver/consumer 게이트 검증 (2026-11-04)
이 주문은 아래 NO_READY_ORDER 및 B43 기록보다 우선한다. ORDER_ID=B44-RF063-CONSUMER-20261104. C03가 발행한 신규 테스트 주문이다.
기존 B 브랜치 work/p15-b-operator-structure-20261022에서 수행한다. SOURCE는 읽기 전용으로 libs/reporting/llm_artifacts.py, llm_artifacts_trade_lookup.py, llm_artifacts_path_projection.py, llm_artifacts_run_paths.py 및 실제 caller single_trade_report.py, intraday_trade_reports.py를 확인한다. 정본과 B의 resolver/caller/import 의존성 blob을 비교해 차이를 기록한다.
쓰기 허용 경로는 새 tests/test_p15_rf063_b44_resolver_consumers.py 한 파일. 이미 존재하면 그 원격 완료 여부를 확인하고 중복 생성하지 않는다. 기존 frozen 테스트 수정 금지.
실제 resolver와 최소 한 개 실제 소비자의 정상 진입점을 tmp_path와 fake/monkeypatch로 실행한다. canonical root 존재, legacy/misplaced root만 존재, 양쪽 존재 시 우선순위, 둘 다 없음, trade-id 조회 및 facade call-time monkeypatch를 검증한다. consumer가 실제로 사용하는 함수와 반환 경로를 확인한다. 네트워크·실제 reports/logs·운영 main·실거래 호출 금지. 소스 수정이 필요하면 최소 재현 테스트와 정확한 SOURCE/function/예상행동을 제출하여 C03가 후속 범위를 확정하게 한다.
B에서 정상 pytest exit/PASS 또는 실제 실패를 기록하고 테스트 파일을 비강제 푸시·원격 재조회한다. 정본에서 같은 테스트를 실행할 수 있도록 source/consumer/dependency manifest와 실행 명령을 #12에 남긴다. 성공 증거는 scoped G2이며 전체 RF DONE은 C05 판정이다.

# C01 — Codex B | ORDER_ID=B-20261103-10-C03 | RF-063 DEV | B43 REMOTE_DONE=8/8 (HISTORICAL; NEW_READY=0/8) | RESERVE_NOT_VERIFIED=0/6

## 2026-11-04 단일 운영 지침
이 절은 아래 과거 회차의 실행·수량·대기 지시를 대체한다. D00의 최신 DONE-FIRST 및 보호·Owner 계약을 따른다. 아래 기록의 코드 경로와 테스트 명령은 증거 조회에만 사용하며 완료 주문을 재발행하지 않는다.
매회 integration/p1.5 최신 HEAD와 관련 작업서 blob을 고정한다. 같은 ORDER_ID+ITEM+SOURCE_BLOB에 원격 완료 증거가 있으면 VERIFIED_ALREADY로 건너뛴다. 변경 또는 증거 누락 범위만 테스트한다. 각 항목을 완료/기완료/정확한 차단으로 판정하고 실행 가능한 나머지 항목을 끝까지 처리한다.
문서 변경, 함수 이동 수, 부분 테스트 PASS를 전체 RF DONE으로 집계하지 않는다. 8~10개 공급 및 예비 6개 강제 기준은 폐기한다. 정책 차단 한 건 때문에 독립적인 안전 작업을 중단하지 않는다.
모델 원복·PR #40/#41 정리는 PC 담당 결과를 조회하여 중복 수행을 방지한다. 실제 원격 반영과 검증 없이 완료로 판단하지 않는다.

C01 Codex B는 이 파일을 유일한 첫 진입점으로 읽는다. B43은 REMOTE_DONE이며 재실행 금지. C03이 발행한 후속 ORDER_ID의 모든 미완료 안전 항목을 기존 B 브랜치에서 수행한다. 신규 주문이 없으면 #12에 NO_READY_ORDER와 정본 SHA를 남겨 C03에 공급 요청한다. 임의 대체 작업 선택 금지. 원격 비강제 푸시와 재조회 증거까지 남긴다.

## 스킬 적용
실행자는 agentra-rf-executor와 agentra-contract-guard, 통합·종결·감사는 agentra-done-verifier를 역할 범위에서 적용한다. 자동 로딩을 확인할 수 없으면 정본 .agents/skills의 지침을 직접 적용한다. 스킬은 신규 권한·작업·검증 게이트를 추가하지 않는다.

## 과거 주문 및 증거 — 아래 지시는 실행하지 않음

# C01 — Codex B | ORDER_ID=B-20261103-10-C03 | RF-063 DEV | B43 REMOTE_DONE=8/8 (HISTORICAL; NEW_READY=0/8) | RESERVE_NOT_VERIFIED=0/6

## 2026-11-03 21:00 C03 evidence correction — exhausted assignment (not new work)
B43-1..8 were delivered on B remote `c9c4936104d93ca33c89d75424319f3c6e1b085b` (#12 6592896977) and reverified unchanged (#12 6602369042). The eight item specifications below are historical completion evidence, **not eight currently ready new tasks**. `NEW_READY=0/8`, `RESERVE_VERIFIED=0/6`, `GATE_IMPACT=NO` for B43. Do not repeat the old code/test or self-select a replacement. The RF-063 whole-G1/G3 resolver/consumer drift is not closed by B43; await C03's new verified single-file order while retaining any genuinely in-flight prior work. This is a documentation correction only, not G1/G2/G3 or RF DONE.

---

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
