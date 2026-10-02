# Changelog

## [Unreleased] — v0.1 bootstrap

### Added
- 저장소 조사 및 GREENFIELD 판정 (`docs/discovery.md`)
- `README.md`, `LICENSE`(MIT), `THIRD_PARTY_NOTICES.md`, `REFERENCES.md`
- `constitution/principles.md`
- `docs/01_product.md` ~ `docs/10_release_checklist.md` 템플릿
- `docs/traceability-convention.md` (ID 규칙, 링크 스키마, 상태 계산 규칙)
- `workflows/` 11단계 골격과 Gate 매핑
- Claude Code / Codex CLI 어댑터 전략 (`adapters/`, `AGENTS.md`)
- `NEXT.md`

### Changed
- `CLAUDE.md`를 `MASTER_PROMPT.md`를 가리키는 adapter로 재작성 (사용자 승인). 기존 `/init` 초안이 MASTER_PROMPT와 충돌해서(`docs/discovery.md` §3).

### Fixed (after independent audit 001, `docs/audits/audit-001.md`)
- C1: Gate 값을 구현자가 수정하는 `traceability.md`에서 분리해 append-only `gates.md`로 이동. 판정자 유형·유효성 규칙 추가 (`docs/traceability-convention.md` §5, `docs/gates.md`)
- C2: 사용자 승인 기록 3종(`APPROVAL_SPEC`, `APPROVAL_IMPLEMENTATION`, `ACCEPTANCE`) 추가 (`workflows/README.md`, clarify/design/implement/converge)
- C3: 테스트 실행 증거 형식과 TC↔테스트 코드 연결 규약 추가 (`docs/09_test_cases.md`, convention §4), verify 쓰기 범위 추가
- H9: "부트스트랩 수행됨" 단정 정정. `B_FINAL = FAIL`을 `docs/gates.md`에 기록
- 수정분 검증에서 나온 허점 보완: Review 차원을 `traceability.md`의 `review:` 값이 아니라 `gates.md`에서 계산, `IMPLEMENTATION_COMPLETE`·`REQUIRED_TESTS_PASS`는 verify가 기록, Gate별 기록 주체 표, `USER` 기록은 사용자 메시지 인용으로만, 독립 리뷰 필수 규약 명시
- L1~L4: `docs/discovery.md` 사실 오류 정정
- Kiro 서술 분리(jasonkneen/kiro SDD, Amazon Kiro), 라이선스 분류 근거의 한계와 `NEEDS LICENSE VERIFICATION` 항목 명시

### Not changed
- `MASTER_PROMPT.md`, `BOOTSTRAP.md`, `261002 대화내용.txt`
