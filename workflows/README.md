# workflows

표준 개발 흐름의 단계별 입력·산출물·Gate 정의. 단계 규칙의 **단일 출처는 `MASTER_PROMPT.md` §4–§5**이며, 하위 폴더는 그것을 가리킨다.

```text
discover → specify → clarify → design → plan → review-plan
        → implement → verify → review-implementation → red-team → converge → DONE
```

## Gate 순서와 기능 수명 상태

Gate를 통과해야만 다음 단계로 진행한다. 아래 상태명은 설계 대화록(2026-10-02 §7)에서 온 **표기 규약**이며, 판정은 Gate로 한다.

| 통과한 Gate | 기능의 상태 |
|---|---|
| (시작) | `DRAFT` |
| `SPEC_READY` (+ clarify의 `SPEC_AMBIGUITY_BLOCKERS = 0`) | `SPECIFIED` |
| (`APPROVAL_SPEC` 기록 후 design 진입) | — |
| `DESIGN_READY` | `DESIGNED` |
| `PLAN_READY` | `PLANNED` |
| `PLAN_REVIEW_PASS` | `PLAN_REVIEWED` |
| (`APPROVAL_IMPLEMENTATION` 기록 후) implement 시작 | `IMPLEMENTING` |
| `IMPLEMENTATION_COMPLETE` (verify가 기록) | (상태 변화 없음) |
| `REQUIRED_TESTS_PASS` | `VERIFIED` |
| `IMPLEMENTATION_REVIEW_PASS` | `REVIEWED` |
| `NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS` | (상태 변화 없음) |
| (범위 안의 모든 REQ가 `DONE`으로 **계산**됨 — 이것이 converge 판정의 선행 조건) → `TRACEABILITY_COMPLETE`, `NO_CRITICAL_OPEN_ISSUES` | (상태 변화 없음) |
| `ACCEPTANCE` 기록 | `DONE` (완료로 **보고**할 수 있음) |

"계산된 `DONE`"은 REQ의 추적 상태(`docs/traceability-convention.md` §4)이고, "보고하는 `DONE`"은 그 위에 `ACCEPTANCE`가 있는 상태이다.

상태가 `PLAN_REVIEWED`가 아니거나 `APPROVAL_IMPLEMENTATION` 기록이 없는데 구현을 시도하면 `BLOCKED`로 보고하고 코딩하지 않는다. (v0.1에서는 에이전트가 규칙을 따르는 방식이며, 자동 강제는 `NEXT.md`.)

Gate 값은 `gates.md`(변경 단위는 `specs/<change-id>/gates.md`, 프로젝트 단위는 `docs/gates.md`)에 기록한다. 기록 위치·형식·판정자 규칙·유효성은 `docs/traceability-convention.md` §5를 따른다. 현재 프로젝트 단위 Gate 값은 `docs/gates.md`를 읽는다.

## 사용자 승인 기록

`MASTER_PROMPT.md` §0.10은 핵심 업무 규칙·DB 구조·인증·권한·결제·주요 기술 스택을 사용자 승인 없이 바꾸지 말라고 하고, §21은 이런 행동을 "사용자 승인 또는 명확한 spec" 없이 하지 말라고 하며, §22는 사소한 선택은 가정으로 기록하고 반복 질문하지 말라고 한다. 이 프로젝트는 그 승인이 흐름 안에서 **기록되도록** 아래 세 지점을 둔다. 이는 §5의 Gate를 **대체하지 않고 추가로 요구하는** 이 프로젝트의 규약이며, 위 조문보다 엄격하다. `MASTER_PROMPT.md`에 정식 반영할지는 사용자 결정이다 (`NEXT.md`). 사소한 선택까지 승인 대상으로 삼지 않는다. 승인 대상은 아래 표의 항목에 한정한다.

| 기록 | 시점 | 승인 대상 | 이것이 없으면 |
|---|---|---|---|
| `APPROVAL_SPEC` | clarify 이후, design 이전 | 핵심 업무 규칙(`docs/01_product.md`의 RULE), blocker 질문에 대한 답, 기술 스택 | design으로 진행하지 않는다 |
| `APPROVAL_IMPLEMENTATION` | `PLAN_REVIEW_PASS` 이후, implement 이전 | 승인된 plan(변경 범위, migration, 영향받는 기존 기능) | implement로 진행하지 않는다 (`BLOCKED`) |
| `ACCEPTANCE` | converge 이후 | 실제 사용자 검증 결과 (`MASTER_PROMPT.md` §25) | 기능을 `DONE`으로 보고하지 않는다 |

- 판정자 유형은 **`USER`만** 허용된다. AI는 사용자의 승인을 추정해서 적지 않는다.
- AI가 기록을 대신 적을 수 있는 경우는 **사용자가 실제로 보낸 승인 메시지를 "근거" 칸에 인용**할 때뿐이다. "근거" 칸에는 **인용, 일시, 승인 범위**를 적는다. 사용자가 승인한 메시지가 대화에 없으면 기록하지 않는다.
- 사용자가 승인한 뒤 승인 범위의 spec/plan **또는 코드**가 바뀌면 승인은 **재확인이 필요**하다 (`docs/traceability-convention.md` §5.3).
- 변경이 문서만 바꾸고 동작에 영향이 없다면 `APPROVAL_IMPLEMENTATION`과 `ACCEPTANCE`를 면제할 수 있다. 면제는 `gates.md`에 Gate 이름 `EXEMPT_<기록 이름>`, 값 `true`, 판정자 유형 `USER`, 근거에 사용자의 면제 확인 메시지 인용으로 기록한다. 이 기록이 없으면 면제는 무효다.
- v0.1에서 `USER` 표기는 규약이며 위조를 기술적으로 막지 못한다 (`docs/traceability-convention.md` §5.4).

## 단계별 쓰기 허용 범위 (공통 규약)

| 단계 | 쓰기 허용 범위 |
|---|---|
| discover / specify / clarify / design / plan | `docs/`, `specs/` 등 문서와 **자기 단계 Gate의 `gates.md` 줄 추가**만. 애플리케이션 코드 수정 금지. `constitution/`과 `MASTER_PROMPT.md`는 사용자 승인 없이 수정 금지 |
| review-plan / review-implementation / red-team / converge | 리뷰 기록(`specs/<change-id>/review.md` 등)과 자신이 판정한 Gate의 `gates.md` 줄 추가만. 코드 수정은 지적 후 implement 단계에서 |
| implement | 승인된 plan에 적힌 파일만. **`gates.md`는 수정하지 않는다.** `docs/09_test_cases.md`의 결과·증거 칸과 `evidence/`도 수정하지 않는다(verify 전용) |
| verify | 테스트 결과와 증거(`docs/09_test_cases.md`의 결과·증거 칸, `specs/<change-id>/evidence/`)와 `IMPLEMENTATION_COMPLETE`·`REQUIRED_TESTS_PASS`의 `gates.md` 줄 추가만. 결과를 바꾸려고 테스트나 구현을 수정하지 않는다 (수정이 필요하면 implement로 돌아간다) |

- `gates.md`에 줄을 추가할 수 있는 것은 그 Gate를 판정한 컨텍스트이다 (`docs/traceability-convention.md` §5.2). 같은 컨텍스트가 자기 작업의 리뷰 Gate를 쓰지 않는다.
- **오케스트레이터**(사용자와 대화하는 메인 컨텍스트. implement 단계를 수행하는 동안은 제외)는 다음을 **대리 기록**할 수 있다. 대리 기록은 비고에 `대리 기록`이라고 적는다.
  - `USER` 줄(`APPROVAL_*`, `ACCEPTANCE`, `EXEMPT_*`): 사용자가 실제로 보낸 메시지를 근거 칸에 인용할 때만
  - `INDEPENDENT_REVIEWER` 줄: 독립 리뷰어가 **저장한 리뷰 결과 파일**(또는 사용자가 확인한 리뷰 보고)을 근거 칸에 적을 때만. 판정자 칸에는 리뷰어를, 판정 기준에는 리뷰어가 본 커밋을 적는다. 읽기 전용 리뷰어는 직접 쓸 수 없으므로 이 경로를 쓴다
- 부트스트랩 Gate(`B0`~`B4`, `B_FINAL`)도 같은 규칙을 따른다: B0~B4는 부트스트랩을 수행한 컨텍스트가, `B_FINAL`은 독립 리뷰어의 결과를 근거로 기록한다.
- 도구별 어댑터는 이 표를 복제하지 않고 가리킨다.

## 독립 리뷰 규칙

`review-plan`, `review-implementation`, `red-team`, `converge`는 **작성자와 다른 컨텍스트**(다른 에이전트/서브에이전트/도구)가 수행한다. `MASTER_PROMPT.md` §13은 "가능하면"이라고 하지만, 이 프로젝트의 규약은 이를 **필수**로 본다: 작성자가 쓴 리뷰 Gate 줄은 무효이며(`docs/traceability-convention.md` §5.2), 독립 컨텍스트가 없으면 Gate는 `UNKNOWN`으로 두고 사용자가 직접 리뷰해 `USER`로 기록할 수 있다. `MASTER_PROMPT.md`를 이에 맞추는 개정은 사용자 결정이다 (`NEXT.md`). 같은 컨텍스트가 자기 작업을 승인하지 않는다.

## 부트스트랩 단계의 Gate (v0.1 구축용)

`MASTER_PROMPT.md` §19의 Phase 0–4에는 종료 조건이 없어, `BOOTSTRAP.md` 완료 목록과 `MASTER_PROMPT.md` §24를 Phase에 매핑해 정의한다. (제품 개발의 Gate와는 별개.)

| Phase | Gate | 통과 조건 |
|---|---|---|
| 0 Inspect | `B0_INSPECTED` | `docs/discovery.md`에 GREENFIELD/BROWNFIELD 판정·보존 목록·충돌 목록 기록. 기존 파일 미손실 |
| 1 Foundation | `B1_FOUNDATION` | README, LICENSE, THIRD_PARTY_NOTICES, constitution, `docs/01~10` 존재. 제3자 코드 없음 |
| 2 Workflow | `B2_WORKFLOW` | 11개 단계 폴더 각각에 입력·산출물·Gate 정의, §5의 Gate 이름과 일치 |
| 3 Traceability | `B3_TRACEABILITY` | `docs/traceability-convention.md`에 ID 규칙·링크 스키마·누락 규칙·상태 계산 규칙 정의 |
| 4 Adapters | `B4_ADAPTERS` | Claude Code·Codex CLI 어댑터 전략 문서와 얇은 진입 파일(`CLAUDE.md`, `AGENTS.md`) 존재 |
| 종료 | `B_FINAL` | **독립 reviewer**가 위 전부와 BOOTSTRAP 완료 목록을 검토해 CRITICAL/HIGH 없음 판정 |

현재 값은 `docs/gates.md`를 읽는다. Phase 5(Self Test)는 이번 범위 밖이며 `NEXT.md`에 있다.
