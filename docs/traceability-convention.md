# Traceability Convention (v0.1)

`MASTER_PROMPT.md` §7의 Traceability Matrix를 **파일로 표현하는 규약**이다. 형식은 Markdown + YAML이며, 검사 스크립트는 v0.1 범위 밖이다 (`docs/discovery.md` A4, `NEXT.md`).

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
- `acceptance`의 모든 AC는 하나 이상의 TC를 가져야 한다.
- `permission`에 연결된 PERM마다 권한 테스트 TC(`docs/06_permissions.md` 필수 권한 테스트 표)가, `error_cases`에 연결된 ERR마다 그 ERR의 테스트 TC가 `tests`에 포함되어야 한다.
- `code` 경로는 저장소에 존재하는 파일이어야 한다.

## 3. 차원별 판정

차원은 `MASTER_PROMPT.md` §7의 표와 같다. 각 차원은 `PASS / PARTIAL / MISSING` 중 하나로 계산한다. **아래 조건을 위에서부터 평가해 처음 맞는 것을 채택한다.**

| 차원 | MISSING | PARTIAL | PASS |
|---|---|---|---|
| Requirement | `acceptance`가 비어 있음 | AC 중 검증 불가능한 문구가 있음 | AC가 1개 이상이고 모두 검증 가능 |
| Workflow | 연결도 `not_applicable` 사유도 없음 | — | 연결 또는 사유 있음 |
| Screen/API | 연결도 사유도 없음 | 화면만 있고 대응 API가 없음(또는 반대) | 연결 또는 사유 있음 |
| Data | 연결도 사유도 없음 | — | 연결 또는 사유 있음 |
| Permission | 연결도 사유도 없음 | 권한은 있으나 서버/API 검사 위치가 없음 | 연결(서버 검사 위치 포함) 또는 사유 있음 |
| Error Cases | 연결도 사유도 없음 | — | 연결 또는 사유 있음 |
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
- 계산된 `DONE`은 **구현·추적 상태**일 뿐이다. 기능을 완료로 **보고**하려면 사용자 승인 기록 `ACCEPTANCE`가 추가로 필요하다 (`workflows/README.md` 사용자 승인 기록).

## 5. Gate와의 관계

- `TRACEABILITY_COMPLETE`(`workflows/converge`)는 **범위 안의 모든 REQ가 `DONE`으로 계산되고 `INTENT_UNKNOWN`이 사용자에게 인지되어 있을 때** 참이다. (`MASTER_PROMPT.md` §5.11의 Gate에 대한 이 규약의 해석이다.)

### 5.1 Gate 기록 위치와 형식

- Gate 값은 **`traceability.md`가 아니라 별도 파일**에 기록한다. 구현자가 수정하는 파일에 Gate를 두면 구현자가 리뷰 Gate를 고칠 수 있기 때문이다.
  - 변경 단위: `specs/<change-id>/gates.md`
  - 프로젝트 단위(변경 단위가 없는 Gate, 부트스트랩 등): `docs/gates.md`
- 형식은 `docs/gates.md`의 표와 같다: `일시 | Gate | 값 | 판정자 유형 | 판정자 | 판정 기준 | 근거 | 비고`.
- **append-only**: 기존 줄을 수정·삭제하지 않는다. 값을 바꾸려면 새 줄을 추가하고, 같은 Gate의 **가장 아래 줄**이 현재 값이다.
- "판정 기준"은 판정한 시점의 **git 커밋 해시**(커밋 전이면 그렇게 적는다). "근거"는 판정의 증거가 되는 파일 경로다.
- 기록이 없거나 아래 판정자 규칙을 어긴 줄만 있으면 그 Gate는 `UNKNOWN`이며, 에이전트는 진행하지 않고 그렇게 보고한다. 에이전트가 "현재 Gate"를 보고할 때는 이 기록을 읽는다.
- implement 단계의 developer는 `gates.md`를 수정하지 않는다 (`workflows/README.md` 쓰기 허용 범위).
- **범위**: REQ의 Gate는 그 REQ의 `traceability.md`와 **같은 폴더의 `gates.md`**에서 읽는다. Gate 줄의 비고에 적용 범위(REQ 목록)를 적고, 범위에 없는 REQ에는 그 줄이 적용되지 않는다(해당 Gate는 `UNKNOWN`).
- **기록 주체**: 줄은 그 Gate를 판정한 컨텍스트가 추가한다. 오케스트레이터의 대리 기록 규칙은 `workflows/README.md`의 쓰기 허용 범위 아래에 있다. 대리 기록은 비고에 `대리 기록`이라고 적는다.

### 5.2 판정자 규칙

| 판정자 유형 | 의미 |
|---|---|
| `USER` | 사람인 사용자의 승인·확인·판정. AI가 사용자의 승인을 **추정해서 적지 않는다.** AI는 사용자가 실제로 보낸 승인 메시지를 "근거" 칸에 인용할 때만 `USER` 줄을 기록할 수 있다 |
| `INDEPENDENT_REVIEWER` | 작성자와 **다른 컨텍스트**(다른 에이전트·서브에이전트·세션·도구)가 직접 spec/코드를 읽고 판정 |
| `AUTHOR` | 해당 산출물을 작성한 컨텍스트의 자기 판정 |

"이상"의 순서는 `AUTHOR` < `INDEPENDENT_REVIEWER`이다. `USER`가 직접 판정한 줄은 사용자 승인 기록을 포함해 **어느 Gate에서나 유효**하다.

| Gate | 허용되는 판정자 유형 | 기록하는 단계(컨텍스트) |
|---|---|---|
| `DISCOVERY_COMPLETE`, `SPEC_READY`, `DESIGN_READY`, `PLAN_READY`, 부트스트랩 `B0_INSPECTED`~`B4_ADAPTERS` | `AUTHOR` 이상 | 그 산출물을 만든 단계 |
| `SPEC_AMBIGUITY_BLOCKERS = 0` | `AUTHOR` 이상 (blocker가 아닌 질문을 blocker가 아니라고 단정한 근거는 `docs/02_requirements.md`에 남긴다) | clarify |
| `IMPLEMENTATION_COMPLETE`, `REQUIRED_TESTS_PASS` | `AUTHOR` 이상. **developer는 기록하지 않는다** | **verify 단계의 tester 컨텍스트** (구현 완료 여부는 테스트를 실행하며 확인한 뒤 기록) |
| `PLAN_REVIEW_PASS`, `IMPLEMENTATION_REVIEW_PASS`, `NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS`, `TRACEABILITY_COMPLETE`, `NO_CRITICAL_OPEN_ISSUES`, 부트스트랩 `B_FINAL` | `INDEPENDENT_REVIEWER` 이상 (`AUTHOR`가 쓴 줄은 무효) | 해당 review/red-team/converge 컨텍스트 |
| 사용자 승인 기록 (`APPROVAL_SPEC`, `APPROVAL_IMPLEMENTATION`, `ACCEPTANCE`)과 면제 기록 (`EXEMPT_APPROVAL_IMPLEMENTATION`, `EXEMPT_ACCEPTANCE`) | **`USER`만** (`workflows/README.md`) | 사용자 (오케스트레이터가 승인 메시지 인용으로 대리 기록) |

`IMPLEMENTATION_COMPLETE`와 `REQUIRED_TESTS_PASS`를 기록하는 verify 컨텍스트가 구현자와 같은 컨텍스트이면 비고에 `구현자와 동일 컨텍스트`라고 적는다. 구현자와 분리된 컨텍스트가 바람직하지만 필수는 아니다. 이 Gate들은 `AUTHOR` 판정을 허용하기 때문이다.

독립 컨텍스트를 만들 수 없는 환경에서는 리뷰 Gate를 `UNKNOWN`으로 두고 진행하지 않는다. 사용자가 직접 리뷰하고 `USER`로 기록하는 것은 유효하다.

### 5.3 Gate의 유효성

- 앞 단계 산출물(spec, design, plan)이 어떤 Gate의 "판정 기준" 커밋 **이후에 바뀌었다면** 그 Gate와 그 뒤의 모든 Gate는 **재판정이 필요**하다. (확인: 해당 파일에 대해 `git log <판정 기준>..HEAD`에 변경이 있는지.)
- `IMPLEMENTATION_REVIEW_PASS`, `NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS`, `REQUIRED_TESTS_PASS`, `ACCEPTANCE`는 해당 REQ의 **`code`와 테스트 파일**이 판정 기준 커밋 이후 바뀌었을 때도 재판정이 필요하다. 재판정이 필요한 Gate는 새 줄에 값 `STALE`로 기록하며(값은 `true | false | STALE`), `STALE`인 Gate는 통과로 계산하지 않는다.
- 값이 숫자인 Gate(`SPEC_AMBIGUITY_BLOCKERS = 0`)는 blocker 수가 0일 때 값 `true`로 기록하고 비고에 `blockers=0`을 적는다.
- 이 규칙은 자동으로 강제되지 않는다. 규약이며 자동 강제는 `NEXT.md`에 있다.

### 5.4 한계 (v0.1)

`gates.md`의 판정자 칸은 자유 텍스트이므로 위조를 막지 못한다. 이 규약이 제공하는 것은 **위반을 `git log`/`git diff`로 사후 탐지**할 수 있다는 점뿐이다. 예: implement 단계 커밋이 `gates.md`를 수정했다면 위반이다.

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
