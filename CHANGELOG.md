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
- `scripts/check_traceability.py`: `docs/traceability-convention.md` §3–§5 자동 계산 (`NEXT.md` 구현 후보 2). 단일 파일, python3 표준 라이브러리만 사용(외부 의존성 0). REQ별 차원 판정(§3)·상태 계산(§4), `gates.md` 기록 표 판독(맨 아래 유효 줄, 이력 구역 제외, 판정자 규칙 §5.2), Review 차원의 커밋-핀 재판정 확인(§5.3), 판정 한계는 비고와 v0 한계로 명시. `--self-test` 내장 시험 통과(초기 21건). 자기 저장소 적용: `docs/gates.md`에서 `B_FINAL = false` 판독, 구조 위반 0건. 계산기이며 규칙의 단일 출처는 convention이다 — 규칙 문서 변경은 도입 안내 1문장뿐이다

### Fixed (wave 002 1차 독립 검토 반영, 2026-10-10)
- 1차 독립 검토(`docs/audits/wave002-review-2026-10-10.md`, dynamic-workflow 런 `dwfrun-3d1d3dfe`)는 종합 **FAIL** — 규칙 무결성 APPROVE(규칙 약화 0건), 계산 격차 HIGH 2건·MEDIUM 4건·LOW 7건. `scripts/check_traceability.py` 수정: AC의 TC 목록이 비거나 필수 권한 테스트 TC 칸이 비면 Tests `MISSING`(HIGH), 실행 증거는 §4 필수 칸(실행 일시·명령·커밋·증거 경로)이 채워진 PASS 줄만 인정(HIGH), §5.2 3행 Gate의 판정자 빈 칸을 무효 줄로 처리·보고에 해당 Gate 표시(MEDIUM), Review 차원에서 값 `false`를 STALE·변경 확인보다 먼저 평가(MEDIUM), screen_api의 SCR-/API- 외 ID·code의 저장소 밖 경로를 위반 처리(LOW), spec 선언 밖 초과 REQ는 위반에서 비고로 완화(LOW), "보수적 PARTIAL/MISSING 처리" 주장을 실제 동작에 맞게 정정(LOW). `--self-test`에 5칸·값·판정자 빈 칸·맨 아래 유효 줄 채택 사례 추가(21건→27건). 규칙 문서 변경 없음(규칙 순증가 0줄). 재검증 APPROVE(`docs/audits/wave002-reverify-2026-10-10.md`, 런 `dwfrun-edf17f7f`: 지적 9건 전부 RESOLVED, 규칙 약화 0건, 새 CRITICAL/HIGH 0건)

### Fixed (wave 002 잔여 지적 흡수, 2026-10-10)
- 구 검토 런들(`87a8f59c`·`b216d5a7`·`5ecaf5b2`)이 인계한 잔여 지적 11건을 수정했다. **N1(HIGH)**: `gates.md`에 `## 기록` 절이 없거나 유효 줄이 없으면 TypeError 크래시 대신 전 Gate `UNKNOWN`으로 계산하고 "새 프로젝트·새 change의 정상 상태" 안내를 출력한다 (새 프로젝트 첫 실행 경로). **R1(HIGH)**: plan.md의 슬래시 없는 파일명(NOTICE 등)도 §5.3 재판정 대상에 포함한다 — 후보는 존재하는 파일로 한정한다 (거짓 DONE 경로 제거). **N2**: spec.md가 REQ를 선언하는데 traceability.md 파일 자체가 없으면 전 차원 MISSING(NOT READY) 항목을 만든다. **N3**: change 폴더에 spec.md가 없으면 범위 검사 생략을 비고로 보고한다. **R2**: 케이스 목록 표는 헤더에서 찾은 대상(AC/ERR/PERM) 칸만 읽는다 (절차 칸의 ID 언급을 커버로 인정하지 않는다). **R3**: TASK 완료 휴리스틱을 `[x]`/`DONE`/✅로 축소하고 비고로 고지한다 ("완료 후 재검토 필요" 오판 제거). **R5**: USER 승인 Gate를 제외한 기록 줄의 근거에 커밋 해시가 없으면 비고로 보고한다 (§5.1). **교차검증**: TRACEABILITY_COMPLETE=true 기록과 DONE이 아닌 REQ의 모순을 비고로 보고한다. **R4**: REQ 상세 블록 부재 시 현재 동작(PASS+비고)은 유지하고 v0 한계로 명시했다 (검토자 간 상반 — 방향 확정은 사용자 결정). `--self-test` 사례 추가(27건→47건). 1차 재검토(런 `dwfrun-76f40125`, `docs/audits/wave002-residual-review-2026-10-11.md`)는 지적 15건 전부 RESOLVED·규칙 약화 없음·규칙 무결성 CLEAR로 판정하되 신규 HIGH 1건(케이스 목록 데이터 행의 임의 칸에 '대상'이 있으면 헤더로 오판)을 발견해 종합 FAIL이었다 — 헤더 판정을 첫 칸이 'ID'인 행으로 한정해 수정하고 회귀 사례(사례 11)를 추가했다. 2차 재검토(런 `dwfrun-12ca5a04`, `docs/audits/wave002-residual-reverify2-2026-10-11.md`)는 NEW-1 해소를 수정 검증 4/4·규칙 무결성 CLEAR(규칙 약화 0건·새 CRITICAL/HIGH 0건)로 확인했다. 미해소로 남았던 RECORDS 1건(감사 보고 ↔ 1차 런 반환값의 직접 대조 불가 — 검증자 세션의 런 아카이브 접근 제한)은 아카이브에 접근 가능한 메인 세션이 검증자가 제시한 대조를 수행해 전 항목 일치로 닫았다 — wave 002 잔여 지적 흡수 완결
- 문서 보완: CLAUDE.md를 AGENTS.md의 스크립트 문구와 동기화(런 `5ecaf5b2` 지적), git 실행 요구를 README·AGENTS.md·CLAUDE.md·`사용자사용메뉴얼.md`에 문서화, README 상태 문구의 "소스코드는 없다"와 "스크립트가 있다" 모순 제거(R6)와 사용자 메뉴얼 안내 추가, `.gitignore`에 `.autopilot.lock`·`.autopilot-skip.log` 추가(R8), PROGRESS.md의 AUTOPILOT.md 참조에 로컬 전용 명시(R7)
- ADOPTING.md §1 복사함 목록에 `scripts/check_traceability.py` 1줄 추가 (근거: convention 도입 안내가 이 스크립트를 §3–§5 계산기로 가리키므로 채택 프로젝트의 상태 계산에 필요하다. 적용 절차 문서의 1줄이며 규칙 문서 변경은 없다)

### Added (brownfield discovery procedure, 2026-10-11)
- `workflows/discover/brownfield.md`: `MASTER_PROMPT.md` §3.2의 Brownfield 10개 절차의 실행 방법 (`NEXT.md` 구현 후보 3). 기준선 범위 판정("이번 변경이 닿는 범위" 기본 + 사용자 확인), 절차별 확인 대상·`docs/discovery.md` 기록 위치 표, 기능 인벤토리 표(근거 파일:위치 필수), `DISCOVERY_COMPLETE` 판정 전 채우는 완료 확인 표 — `docs/audits/audit-002.md`가 지적한 "인벤토리·기준선 범위 형식 부재", "어느 범위를 기준선으로 삼을지, 어떤 표로 완료를 확인할지"를 직접 답한다. 규칙 단일 출처(§3.2·§5.1, convention)는 변경하지 않았다
- `workflows/discover/README.md`: `/project-discover` 동작 정의 초안(목적·입력·수행·금지·종료). 이름·동작의 확정과 어댑터 명령 등록은 사용자 결정 사항으로 남긴다 (`docs/discovery.md` 미결 #3)

### Not changed
- `MASTER_PROMPT.md`, `BOOTSTRAP.md`, `261002 대화내용.txt`
