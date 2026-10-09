# Traceability Convention (v0.1)

`MASTER_PROMPT.md` §7의 Traceability Matrix를 **파일로 표현하는 규약**이다. 형식은 Markdown + YAML이다. 검사 스크립트는 v0.1 범위 밖으로 `NEXT.md`에 이월했다가, 2026-10-09에 구현 후보 2로 `scripts/check_traceability.py`(§3–§5 계산)를 추가했다. 이 스크립트는 계산기일 뿐이며 규칙의 단일 출처는 이 문서다 (`docs/discovery.md` A4).

## 1. ID 규칙

| 접두사 | 대상 | 정의 위치 |
|---|---|---|
| `REQ-###` | 요구사항 | `docs/02_requirements.md` (**ID 등록부**) |
| `AC-###` | 완료조건 | `docs/02_requirements.md` (**ID 등록부**) |
| `WF-###` | 업무 흐름 | `docs/03_workflow.md` |
| `SCR-###` | 화면 | `docs/04_screens.md` |
| `API-###` | API | `docs/04_screens.md` |
| `DATA-###` | 데이터 구조 | `docs/05_data_model.md` |
| `PERM-###` | 권한 | `docs/06_permissions.md` |
| `ERR-###` | 오류 상황 | `docs/08_error_cases.md` |
| `TC-###` | 테스트 케이스 | `docs/09_test_cases.md` |
| `TASK-###` | 작업 | `specs/<change-id>/tasks.md` |

- 형식: 대문자 접두사 + `-` + 3자리 이상 숫자 (`REQ-023`). 정규식 `^(REQ|AC|WF|SCR|API|DATA|PERM|ERR|TC|TASK)-\d{3,}$`
- ID는 **한 번 부여하면 재사용하지 않는다.** 폐기된 항목은 삭제하지 않고 `status: RETIRED`로 둔다.
- 번호는 프로젝트 전체에서 접두사별로 단조 증가한다. 번호 순서는 의미를 갖지 않는다.
- 하나의 의미는 한 곳에서만 정의한다. 다른 문서는 ID로 참조한다.
- **REQ/AC의 정의 위치**: ID는 `docs/02_requirements.md`에 먼저 등록한다. 변경 단위 문서(`specs/<change-id>/spec.md`, `acceptance.md`)는 **등록된 ID를 사용해** 그 변경의 범위와 상세를 적는다. 변경 명세에만 있고 등록부에 없는 ID는 dangling reference다.

## 2. 링크 스키마

각 REQ는 `specs/<change-id>/traceability.md`(또는 프로젝트 전체용 `docs/traceability.md`)에서 다음 YAML 블록으로 표현한다.

```yaml
- id: REQ-<###>
  workflow:       [WF-<###>]
  screen_api:     [SCR-<###>, API-<###>]
  data:           [DATA-<###>]
  permission:     [PERM-<###>]
  error_cases:    [ERR-<###>]
  acceptance:                      # AC → 검증하는 TC (AC마다 TC 목록)
    AC-<###>: [TC-<###>]
  tests:          [TC-<###>]       # 이 REQ의 모든 TC (acceptance에 쓴 TC + PERM/ERR 테스트)
  tasks:          [TASK-<###>]
  code:           [<repo-relative path>]
  not_applicable: {}               # 예: {permission: "공개 읽기 전용 화면이라 권한 없음"}
```

이 파일에는 **리뷰 결과 필드를 두지 않는다.** 구현자가 수정하는 파일에 `review: PASS`를 두면 `gates.md`의 판정을 우회해 `DONE`을 만들 수 있기 때문이다. Review 차원은 §3과 §5에 따라 `gates.md`에서만 계산한다.

규칙:

- 비어 있는 차원은 `[]`이다. 해당하지 않는 차원은 **이유를 `not_applicable`에 적어야** 한다. 이유 없는 빈 칸은 `MISSING`이다.
- **`not_applicable`을 쓸 수 있는 차원은 `workflow`, `screen_api`, `data`, `permission`, `error_cases`뿐이다.** Requirement(`acceptance`), Tests, Implementation, Review는 해당 없음이 될 수 없다 (Review는 `traceability.md`에 값이 없고 `gates.md`에서 계산된다).
- 모든 링크 대상 ID는 정의 위치에 실제로 존재해야 한다 (dangling reference 금지).
- **범위**: 변경의 REQ 목록은 `specs/<change-id>/spec.md`가 선언하고, `traceability.md`는 그 REQ 전부의 항목을 가져야 한다. 항목이 없는 REQ는 `MISSING`이다.
- `acceptance`의 키는 `docs/02_requirements.md`에 등록된 그 REQ의 **활성 AC 전부**(`RETIRED` 제외)여야 하고, 각 AC는 하나 이상의 TC를 가져야 한다. 빠진 AC가 있으면 Requirement는 `MISSING`이다.
- `permission`·`error_cases`는 같은 문서의 REQ 상세 블록(권한·예외 상황 칸)에 적힌 PERM·ERR **전부**를 포함해야 한다. 일부만 연결하면 해당 차원은 `PARTIAL`이다.
- `permission`에 연결된 PERM마다 권한 테스트 TC(`docs/06_permissions.md` 필수 권한 테스트 표)가, `error_cases`에 연결된 ERR마다 그 ERR의 테스트 TC가 `tests`에 포함되어야 한다.
- `code` 경로는 저장소에 존재하는 파일이어야 한다.

## 3. 차원별 판정

차원은 `MASTER_PROMPT.md` §7의 표와 같다. 각 차원은 `PASS / PARTIAL / MISSING` 중 하나로 계산한다. **아래 조건을 위에서부터 평가해 처음 맞는 것을 채택한다.**

| 차원 | MISSING | PARTIAL | PASS |
|---|---|---|---|
| Requirement | `acceptance`가 비어 있거나 등록된 활성 AC 중 빠진 것이 있음 | AC 중 검증 불가능한 문구가 있음 | AC가 1개 이상이고 모두 검증 가능 |
| Workflow | 연결도 `not_applicable` 사유도 없음 | — | 연결 또는 사유 있음 |
| Screen/API | 연결도 사유도 없음 | 화면만 있고 대응 API가 없음(또는 반대) | 연결 또는 사유 있음 |
| Data | 연결도 사유도 없음 | — | 연결 또는 사유 있음 |
| Permission | 연결도 사유도 없음 | 권한은 있으나 서버/API 검사 위치가 없음, 또는 등록된 PERM 일부만 연결 | 연결(서버 검사 위치 포함) 또는 사유 있음 |
| Error Cases | 연결도 사유도 없음 | 등록된 ERR 일부만 연결 | 연결 또는 사유 있음 |
| Tests | `tests`가 비어 있거나, AC·PERM·ERR 중 TC가 없는 항목이 있음 | TC가 있으나 일부가 `NOT RUN` 또는 `FAIL` (전부 FAIL 포함) | 필요한 모든 TC가 **실제 실행되어 PASS** |
| Implementation | `code`가 비어 있음 | 일부 TASK 미완료 | 모든 TASK 완료 + `code` 연결 |
| Review | `gates.md`의 `IMPLEMENTATION_REVIEW_PASS` 가장 아래 줄이 유효하고 값이 `false` | 유효한 기록이 없음 (`UNKNOWN`) 또는 §5.3에 따라 재판정이 필요함 | `gates.md`의 `IMPLEMENTATION_REVIEW_PASS` 가장 아래 줄이 유효(§5.2, §5.3)하고 값이 `true` (독립 리뷰, Critical/High 없음) |

## 4. REQ 상태 계산

```text
if 어떤 차원이든 MISSING            → NOT READY
else if 어떤 차원이든 PARTIAL        → IN PROGRESS
else if 모든 차원이 PASS             → DONE
else                                → NOT READY   (방어용: 위 표로 계산되지 않는 경우)
```

- `DONE`은 **계산 결과**이다. 에이전트가 직접 써 넣지 않는다.
- 하나라도 `MISSING`이면 에이전트는 해당 기능을 "완료"라고 보고하지 않는다 (`MASTER_PROMPT.md` §7, §21).
- Tests 차원의 PASS는 `docs/09_test_cases.md` 또는 `test-plan.md`의 **실제 실행 결과**에서만 나온다. `NOT RUN`은 PASS가 아니다.
- **실행 증거가 없는 PASS는 `NOT RUN`으로 취급한다.** 결과에는 실행 일시, 실행한 명령, 실행 시점의 커밋, 증거 경로(로그 등)가 있어야 한다 (`docs/09_test_cases.md`). 코드가 증거의 커밋 이후 바뀌었다면 그 PASS는 재실행이 필요하다.
- TC는 실제 테스트 코드와 연결되어야 한다: 테스트 이름이나 주석에 TC ID를 넣고(예: `[TC-104]`), `docs/09_test_cases.md`의 "테스트 코드 위치" 칸에 파일 경로를 적는다. 자동화 테스트가 없는 TC(수동 테스트)는 그렇게 표시하고, 증거로 실행 절차와 관찰 결과 기록을 둔다.
- 리뷰 기록이 아직 없는 REQ는 `IN PROGRESS`이다 (`NOT READY`가 아니다). 유효한 `IMPLEMENTATION_REVIEW_PASS = false`가 있으면 `NOT READY`이다.
- 계산된 `DONE`은 **구현·추적 상태**일 뿐이다. 기능을 완료로 **보고**하려면 사용자 승인 기록 `ACCEPTANCE`가 추가로 필요하다 (`workflows/README.md` 사용자 승인 기록). 계산하지 못하는 DoD 항목(회귀 테스트, 문서·구현 일치, 변경 기록)은 `docs/10_release_checklist.md`로 확인하고, `ACCEPTANCE` 줄의 근거에 그 확인을 적는다.

## 5. Gate 기록 규칙 (이 규약의 단일 출처)

다른 문서(`workflows/README.md`, 어댑터 등)는 이 절을 복제하지 않고 가리킨다.

- `TRACEABILITY_COMPLETE`(`workflows/converge`)는 **범위 안의 모든 REQ가 `DONE`으로 계산되고 `INTENT_UNKNOWN`이 사용자에게 인지되어 있을 때** 참이다. (`MASTER_PROMPT.md` §5.11의 Gate에 대한 이 규약의 해석이다.)
- `NO_CRITICAL_OPEN_ISSUES`는 모든 리뷰·red-team 기록에 **미해결 CRITICAL과 HIGH가 모두 없을 때** 참이다. `MASTER_PROMPT.md` §6의 "Critical/High blocker 없음"에 맞춘 해석이며, §5.10의 red-team Gate는 CRITICAL만 말하므로 이 규약이 더 엄격하다 (원문 개정은 사용자 결정, `NEXT.md`).

### 5.1 기록 위치와 형식

- Gate 값은 `traceability.md`가 아니라 **별도 파일**에 기록한다. 구현자가 수정하는 파일에 두면 구현자가 리뷰 Gate를 고칠 수 있기 때문이다.
  - 변경 단위: `specs/<change-id>/gates.md` (그 REQ의 `traceability.md`와 같은 폴더의 것만 읽는다). Gate는 change 폴더 단위로 범위(§2의 REQ 목록) 전체에 함께 적용한다. REQ마다 진행이 다르면 change를 나눈다
  - 프로젝트 단위(부트스트랩 등): `docs/gates.md`
- 표의 칸: `일시 | Gate | 값 | 판정자 | 근거`
  - 값: `true | false | STALE` (숫자 Gate `SPEC_AMBIGUITY_BLOCKERS = 0`은 blocker가 0이면 `true`)
  - 근거: 판정이 본 **커밋된 상태**의 git 커밋 해시와 증거(파일 경로 또는 사용자 메시지 인용). 그 Gate가 검토한 산출물(§5.3의 대상 파일)에 미커밋 변경이 있는 상태에서는 판정하지 않는다(그때 쓴 줄은 무효). 판정 단계 자신의 산출물(리뷰·테스트 결과 파일, `gates.md`)은 제외한다
- **이력 구역**: 규칙 단순화 이전의 구 형식 줄(`docs/gates.md` 이력 구역)은 읽을 수 있지만 통과로 계산하지 않는다(`STALE`과 같은 취급). 현재 값은 맨 아래 `기록` 표의 줄로만 정한다.
- **append-only**: 기존 줄을 수정·삭제하지 않는다. 값을 바꾸려면 새 줄을 추가하고, 같은 Gate의 **가장 아래 줄**이 현재 값이다.
- 기록이 없거나 아래 판정자 규칙을 어긴 줄만 있으면 그 Gate는 `UNKNOWN`이다. 에이전트는 진행하지 않고 그렇게 보고한다.
- implement 단계의 developer는 `gates.md`를 수정하지 않는다. 위반은 `git log`/`git diff`로 사후 탐지한다.

### 5.2 판정자 규칙

판정자 유형은 두 가지다.

| 유형 | 의미 |
|---|---|
| `USER` | 사람인 사용자. AI는 승인을 **추정해서 적지 않는다.** 사용자가 실제로 보낸 메시지를 근거 칸에 **인용**(일시·승인 범위 포함)할 때만 대신 적을 수 있다 |
| `REVIEWER` | 작성자와 **다른 컨텍스트**(다른 에이전트·서브에이전트·세션·도구)가 직접 spec/코드를 읽고 판정 |

| Gate | 허용되는 기록자 |
|---|---|
| `APPROVAL_SPEC`, `APPROVAL_IMPLEMENTATION`, `ACCEPTANCE` (`workflows/README.md`) | `USER`만 |
| `PLAN_REVIEW_PASS`, `IMPLEMENTATION_REVIEW_PASS`, `NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS`, `TRACEABILITY_COMPLETE`, `NO_CRITICAL_OPEN_ISSUES`, 부트스트랩 `B_FINAL` | `REVIEWER` 또는 `USER`. 작성자가 쓴 줄은 무효 |
| 그 밖의 Gate (`DISCOVERY_COMPLETE`, `SPEC_READY`, `SPEC_AMBIGUITY_BLOCKERS`, `DESIGN_READY`, `PLAN_READY`, `IMPLEMENTATION_COMPLETE`, `REQUIRED_TESTS_PASS`) | 그 산출물을 만든 단계의 컨텍스트. `IMPLEMENTATION_COMPLETE`·`REQUIRED_TESTS_PASS`는 **verify 컨텍스트**가 기록하며 developer는 기록하지 않는다. 판정자 칸에는 컨텍스트 이름을 적는다. verify가 구현자와 같은 컨텍스트이면 `구현자와 동일`이라고 덧붙인다 (분리가 바람직하지만 필수는 아니다) |

- **대리 기록**: 사용자와 대화하는 메인 컨텍스트(implement를 수행하는 동안은 제외)는 위 줄을 대신 적을 수 있다. 판정자 칸 끝에 `(대리 기록)`을 붙이고, 근거에 사용자 메시지 인용(`USER`) 또는 리뷰어가 **저장한 결과 파일**·사용자가 확인한 리뷰 보고(`REVIEWER`)를 적는다. 근거가 없으면 기록하지 않는다. 읽기 전용 리뷰어는 직접 쓸 수 없으므로 이 경로를 쓴다.
- 독립 컨텍스트를 만들 수 없으면 리뷰 Gate는 `UNKNOWN`으로 두고 진행하지 않는다. 사용자가 직접 리뷰해 `USER`로 기록하는 것은 유효하다.

### 5.3 재판정

- 판정의 근거 커밋 **이후에** 그 Gate가 본 산출물(spec·design·plan)이 바뀌었으면 그 Gate와 뒤 Gate는 재판정이 필요하다. `IMPLEMENTATION_REVIEW_PASS`, `NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS`, `REQUIRED_TESTS_PASS`, `ACCEPTANCE`는 REQ의 **`code`·테스트 파일과 plan의 "변경할 파일"**이 바뀐 경우도 같다.
- 확인 방법: `git diff --stat <근거 커밋> -- <해당 파일>`(커밋된 변경과 추적 중인 파일의 미커밋 변경)과 `git status --short -- <해당 파일>`(새로 만들어 아직 추적되지 않은 파일은 `??`로 나온다) **둘 다**에 변경이 없는지 본다. 재판정이 필요한 Gate는 통과로 계산하지 않는다. 눈에 보이게 하려면 값 `STALE`인 새 줄을 추가한다.

### 5.4 한계 (v0.1)

판정자 칸은 자유 텍스트이므로 위조를 막지 못한다. 이 규약은 위반을 사후에 탐지할 수 있게 할 뿐이며, 자동 강제는 `NEXT.md`에 있다. 또 plan의 파일 목록에 없는 공유 모듈(인증 등)의 변경은 §5.3으로 탐지되지 않는다.

## 6. 누락 탐지 규칙 (수동 검사 절차, 자동화 전)

CONVERGE 단계(`MASTER_PROMPT.md` §5.11)에서 다음을 점검하고, 위반은 `CODE_BUG / SPEC_OUTDATED / DOC_OUTDATED / TEST_MISSING / INTENT_UNKNOWN` 중 하나로 분류한다.

1. 링크 대상 ID가 정의 위치에 없다 → `DOC_OUTDATED` 또는 `SPEC_OUTDATED`
2. AC에 연결된 TC가 없다 → `TEST_MISSING`
3. 화면은 있는데 대응 API가 없다 / API 권한과 화면 권한이 다르다 → 불일치 분류
4. 권한이 UI에만 있고 서버 검사 위치가 없다 → `CODE_BUG` 후보
5. 데이터 변경이 있는데 migration 기록이 없다 → `DOC_OUTDATED` 후보
6. 의도를 근거로 판단할 수 없다 → `INTENT_UNKNOWN`으로 남기고 조용히 고치지 않는다

## 7. 변경 이력 연결

커밋 또는 작업 기록에 REQ ID를 포함한다 (`MASTER_PROMPT.md` §17).
