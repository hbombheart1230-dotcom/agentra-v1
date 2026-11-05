# Agentra 작업 진입점

최상위 운영 결정: [P1.5 중단·P1.6 이관](docs/refactor/p1_6/P15_STOP_AND_HANDOFF_20261105.md).

P1.5는 STOPPED / CLOSEOUT_ONLY. 신규 개발 및 자동 연속 수행을 중단하고 미완료는 P1.6으로 이관한다.
지팀장 전용 쓰기·승인 권한은 폐지했다. 홍사장이 승인한 범위에서 담당 Claude/Codex는 코드·테스트·문서·원장·STATUS·RF·patchnotes를 직접 수정·커밋·푸시할 수 있다. 최신 원격과 검증 근거를 확인하고 비강제 푸시한다.

P1.6 진입점: docs/refactor/p1_6/README.md. 안전·frozen·UEF·Guard·Step5C·운영 데이터 보호는 유지한다. 실제 Git 인증 실패나 NOT_RUN을 숨기지 않는다.
