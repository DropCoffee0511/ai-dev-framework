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
  review:         NOT_STARTED      # NOT_STARTED | PASS | FAIL
  not_applicable: {}               # 예: {permission: "공개 읽기 전용 화면이라 권한 없음"}
```

규칙:

- 비어 있는 차원은 `[]`이다. 해당하지 않는 차원은 **이유를 `not_applicable`에 적어야** 한다. 이유 없는 빈 칸은 `MISSING`이다.
- **`not_applicable`을 쓸 수 있는 차원은 `workflow`, `screen_api`, `data`, `permission`, `error_cases`뿐이다.** Requirement(`acceptance`), Tests, Implementation, Review는 해당 없음이 될 수 없다.
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
| Review | `review: FAIL` | `review: NOT_STARTED` | `review: PASS` (독립 리뷰, Critical/High 없음) |

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
- Review가 아직 시작되지 않은 REQ는 `IN PROGRESS`이다 (`NOT READY`가 아니다). `review: FAIL`이면 `NOT READY`이다.

## 5. Gate와의 관계

- `TRACEABILITY_COMPLETE`(`workflows/converge`)는 **범위 안의 모든 REQ가 `DONE`으로 계산되고 `INTENT_UNKNOWN`이 사용자에게 인지되어 있을 때** 참이다. (`MASTER_PROMPT.md` §5.11의 Gate에 대한 이 규약의 해석이다.)
- Gate의 현재 값은 `specs/<change-id>/traceability.md`의 `Gate` 섹션에 `이름: true/false (날짜, 판정한 컨텍스트)`로 기록한다. `review-*`, `red-team`, `converge`의 Gate는 **작성자와 다른 컨텍스트**가 값을 기록한다 (`MASTER_PROMPT.md` §0.7).
- 에이전트가 "현재 Gate"를 보고할 때는 이 기록을 읽는다. 기록이 없으면 `UNKNOWN`으로 보고하고 진행하지 않는다.

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
