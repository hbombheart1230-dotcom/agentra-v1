# Engineering delivery policy — 오너 결정 반영

[2026-11-05 중단·이관 결정](../p1_6/P15_STOP_AND_HANDOFF_20261105.md)이 이전 DONE-FIRST 및 C03~C06 역할 정책을 대체한다.

P1.5 신규 개발·자동 작업 공급·DONE 증가 목표는 중단한다. 정리 후 잔여는 P1.6으로 이관한다. 지팀장 역할 및 독점 쓰기·승인 권한은 폐지한다. 홍사장이 승인한 범위의 담당자는 코드·테스트·문서·원장·STATUS·RF·patchnotes를 직접 수정·커밋·푸시한다.

유지할 계약:
- 실제 검증 증거, 정확한 SHA, 독립 리뷰 및 PASS/FAIL/NOT_RUN 구분.
- 소스 모듈 Owner 경계, frozen oracle 및 기존 테스트 계약.
- Guard, Writer, UEF, Step5C, 실거래·브로커·운영 데이터 안전 제한.
- 기존 결과와 실패 증거 보존, 완료 작업 재계상 금지, 비강제 푸시.

이관이나 KEEP_VERIFIED는 전체 회귀·런타임 검증 PASS가 아니다. 문서 쓰기 허용은 운영 배포 승인과 별개다.
