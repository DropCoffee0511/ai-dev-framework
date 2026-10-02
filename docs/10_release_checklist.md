# 10 Release Checklist

> **템플릿.** 릴리스 전 확인표. 체크박스는 근거를 확인한 뒤에만 표시한다. 미완료 항목을 DONE으로 표시하지 않는다 (`MASTER_PROMPT.md` §21).

## 릴리스 대상

- 버전: <...>
- 포함된 REQ: <REQ-###, ...>

## Definition of Done (`MASTER_PROMPT.md` §6)

- [ ] 요구사항이 문서화되어 있다
- [ ] 완료조건이 검증 가능하다
- [ ] 관련 workflow가 정의되어 있다
- [ ] 필요한 화면/API가 정의되어 있다
- [ ] 필요한 데이터 구조가 정의되어 있다
- [ ] 권한이 정의되어 있다
- [ ] 주요 예외가 정의되어 있다
- [ ] 구현이 요구사항과 연결되어 있다
- [ ] 정상 / 예외 / 권한 / 회귀 테스트가 통과한다
- [ ] 독립 리뷰에서 Critical/High blocker가 없다
- [ ] 관련 문서가 현재 구현과 일치한다
- [ ] 변경 내용이 기록되어 있다

## Traceability

- [ ] 모든 포함 REQ의 상태가 `DONE` (`docs/traceability-convention.md`)
- [ ] `INTENT_UNKNOWN` 항목이 남아 있지 않거나, 남은 항목을 사용자가 인지하고 수용했다

## 데이터/운영

- [ ] migration 영향·rollback 확인 (`docs/05_data_model.md`)
- [ ] 프로덕션 데이터/인프라 변경 시 사용자 확인 완료
- [ ] 라이선스/provenance 확인 (`THIRD_PARTY_NOTICES.md`)
