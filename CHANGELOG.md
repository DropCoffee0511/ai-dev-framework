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

### Changed (rule simplification, 2026-10-05, user-approved)
- Gate 기록 규칙을 `docs/traceability-convention.md` §5 한 곳으로 통합 (판정자 유형 `USER`/`REVIEWER` 2종, Gate별 기록자 표 3행, 재판정 규칙 1절로 통합). `workflows/README.md`는 이를 복제하지 않고 가리킴
- `EXEMPT_*` 면제 제도 폐지, 기능 상태 이름 열(`DRAFT`~`REVIEWED`) 삭제, 부트스트랩 Gate `B0`~`B4` 폐지(`B_FINAL` 하나와 체크리스트만 유지)
- `docs/gates.md`: 기록 표를 5칸으로 줄이고, 기존 14개 줄은 수정 없이 이력 구역으로 이동
- 유지: Gate 별도 파일·append-only, 독립 리뷰 필수, 사용자 승인 3곳(`APPROVAL_SPEC`/`APPROVAL_IMPLEMENTATION`/`ACCEPTANCE`), DONE 계산, 테스트 실행 증거

### Added (cross-model audit, 2026-10-06)
- `docs/audits/audit-002.md`: Codex CLI(`gpt-6.1-sol`) 독립 감사 원문. 대상 `bfbe160`, `B_FINAL = FAIL` (CRITICAL 0, HIGH 4, MEDIUM 12, LOW 3)
- `docs/gates.md`: `B_FINAL = false` 기록 줄 추가(대리 기록). 지적 사항은 이 시점에는 수정하지 않았다 (일부는 아래 항목에서 수정)

### Changed (audit-002 HIGH 3건 + 후속 2건 수정, 2026-10-06, user-approved minimal plan. 1차 검증 FAIL(미추적 파일 누락) 후 반영, 2차 검증 PASS)
- H-01: `traceability.md`는 `spec.md`가 선언한 REQ 전부를 가져야 하고, `acceptance`는 등록된 활성 AC 전부, `permission`·`error_cases`는 등록된 PERM·ERR 전부를 포함해야 함 (빠진 AC는 Requirement `MISSING`, 일부 PERM/ERR는 `PARTIAL`). `docs/traceability-convention.md` §2, §3
- H-02: 계산할 수 없는 DoD 항목(회귀 테스트·문서 일치·변경 기록)은 `ACCEPTANCE` 근거에 `docs/10_release_checklist.md` 확인을 적도록 연결. `NO_CRITICAL_OPEN_ISSUES`를 미해결 CRITICAL **및 HIGH** 없음으로 해석(MASTER_PROMPT §5.10보다 엄격한 프로젝트 규약, 원문은 미수정). convention §4, §5, `workflows/red-team/README.md`, `docs/10_release_checklist.md`
- H-03: Gate는 **커밋된 상태**에서만 판정("커밋 전" 허용 삭제), 재판정 확인 명령을 `git diff --stat <근거 커밋> -- <파일>`과 `git status --short -- <파일>` 병행으로 변경(미커밋·미추적 새 파일 포함), 대상에 plan의 "변경할 파일" 추가, plan 목록 밖 공유 모듈은 한계로 명시. convention §5.1, §5.3, §5.4
- M-03: REQ별 적용 목록 문구를 삭제하고 "Gate는 change 폴더 단위로 범위 전체에 적용, REQ마다 진행이 다르면 change를 나눈다"로 대체
- M-10: 이력 구역의 구 형식 줄은 통과로 계산하지 않음. `docs/gates.md` 안내 문구도 이에 맞춤 (기록 줄은 수정하지 않음)
- 미수정: H-04, M-01·M-02·M-04~M-09·M-11·M-12, LOW 전부 (`NEXT.md`). `B_FINAL`은 여전히 `false`

### Added (audit-002 H-04, 2026-10-06, user-approved plan A)
- `ADOPTING.md`: 다른 프로젝트에 적용하는 방법. 복사 허용 목록(allowlist), 대상이 자기 것으로 만드는 파일, 가져가지 않을 파일, 진입 파일 블록, Greenfield/Brownfield 절차, 출처·라이선스 기록, 수동 확인표, 한계
- `README.md`: 구조 목록과 사용 방법에 `ADOPTING.md` 안내 추가
- 폴더는 옮기지 않았다. 템플릿과 자체 기록의 물리적 분리는 `NEXT.md`의 사용자 결정 사항이다. 검증자 3회(1차 FAIL MEDIUM 3건, 2차 FAIL MEDIUM 1건 반영 후 3차 PASS)

### Added (traceability check script, 2026-10-09)
- `scripts/check_traceability.py`: `docs/traceability-convention.md` §3–§5 자동 계산 (`NEXT.md` 구현 후보 2). 단일 파일, python3 표준 라이브러리만 사용(외부 의존성 0). REQ별 차원 판정(§3)·상태 계산(§4), `gates.md` 기록 표 판독(맨 아래 유효 줄, 이력 구역 제외, 판정자 규칙 §5.2), Review 차원의 커밋-핀 재판정 확인(§5.3), 계산 못 하는 항목은 보수적으로 PARTIAL/MISSING 처리. `--self-test` 내장 시험 21건 통과. 자기 저장소 적용: `docs/gates.md`에서 `B_FINAL = false` 판독, 구조 위반 0건. 계산기이며 규칙의 단일 출처는 convention이다 — 규칙 문서 변경은 도입 안내 1문장뿐이다

### Not changed
- `MASTER_PROMPT.md`, `BOOTSTRAP.md`, `261002 대화내용.txt`
