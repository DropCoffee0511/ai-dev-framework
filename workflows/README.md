# workflows

표준 개발 흐름의 단계별 입력·산출물·Gate 정의. 단계 규칙의 **단일 출처는 `MASTER_PROMPT.md` §4–§5**이며, 하위 폴더는 그것을 가리킨다. Gate 기록 규칙(위치·형식·판정자·재판정)의 단일 출처는 `docs/traceability-convention.md` §5이다.

```text
discover → specify → clarify → design → plan → review-plan
        → implement → verify → review-implementation → red-team → converge → DONE
```

## Gate 순서

Gate를 통과해야만 다음 단계로 진행한다. 기능이 지금 어느 단계인지는 별도 상태 이름 없이 **통과한 마지막 Gate**로 말한다.

| 순서 | 통과해야 하는 Gate |
|---|---|
| discover → specify | `DISCOVERY_COMPLETE` |
| specify → clarify | `SPEC_READY` |
| clarify → design | `SPEC_AMBIGUITY_BLOCKERS = 0` + **`APPROVAL_SPEC`** |
| design → plan | `DESIGN_READY` |
| plan → review-plan | `PLAN_READY` |
| review-plan → implement | `PLAN_REVIEW_PASS` + **`APPROVAL_IMPLEMENTATION`** |
| implement → verify | (구현 완료는 verify가 `IMPLEMENTATION_COMPLETE`로 기록) |
| verify → review-implementation | `REQUIRED_TESTS_PASS` |
| review-implementation → red-team | `IMPLEMENTATION_REVIEW_PASS` |
| red-team → converge | `NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS` |
| converge → DONE | `TRACEABILITY_COMPLETE` + `NO_CRITICAL_OPEN_ISSUES` + **`ACCEPTANCE`** |

"계산된 `DONE`"은 REQ의 추적 상태(convention §4)이고, 기능을 완료로 **보고**하려면 그 위에 `ACCEPTANCE`가 있어야 한다.

선행 Gate가 없는데 다음 단계를 시도하면 `BLOCKED`로 보고하고 진행하지 않는다 (예: `PLAN_REVIEW_PASS`나 `APPROVAL_IMPLEMENTATION`이 없는데 구현). v0.1에서는 에이전트가 규칙을 따르는 방식이며, 자동 강제는 `NEXT.md`.

Gate 값은 변경 단위는 `specs/<change-id>/gates.md`, 프로젝트 단위는 `docs/gates.md`에 기록한다. 현재 프로젝트 단위 Gate 값은 `docs/gates.md`를 읽는다.

## 사용자 승인 기록

`MASTER_PROMPT.md` §0.10·§21은 핵심 업무 규칙·DB 구조·인증·권한·결제·주요 기술 스택을 사용자 승인 없이 바꾸지 말라고 한다. 이 프로젝트는 그 승인을 흐름 안에 **기록**하도록 세 지점을 둔다. §5의 Gate를 대체하지 않고 추가로 요구하는 이 프로젝트의 규약이며, `MASTER_PROMPT.md`에 정식 반영할지는 사용자 결정이다 (`NEXT.md`). 사소한 선택은 승인 대상이 아니며 §22대로 가정으로 기록한다.

| 기록 | 승인 대상 | 이것이 없으면 |
|---|---|---|
| `APPROVAL_SPEC` | 핵심 업무 규칙(`docs/01_product.md`의 RULE), blocker 질문의 답, 기술 스택 | design으로 진행하지 않는다 |
| `APPROVAL_IMPLEMENTATION` | 승인된 plan(변경 범위, migration, 영향받는 기존 기능) | implement로 진행하지 않는다 |
| `ACCEPTANCE` | 실제 사용자 검증 결과 (`MASTER_PROMPT.md` §25) | 기능을 `DONE`으로 보고하지 않는다 |

- 기록자는 `USER`만이다. 기록 방법(메시지 인용, 대리 기록)은 convention §5.2.
- 승인 뒤에 승인 범위의 spec/plan/코드가 바뀌면 재확인이 필요하다 (convention §5.3).
- 문서만 바꾸는 변경도 같은 승인을 받는다. 면제 제도는 없다.

## 단계별 쓰기 허용 범위

| 단계 | 쓰기 허용 범위 |
|---|---|
| discover / specify / clarify / design / plan | `docs/`, `specs/` 문서와 자기 단계 Gate의 `gates.md` 줄 추가만. 코드 수정 금지. `constitution/`, `MASTER_PROMPT.md`는 사용자 승인 없이 수정 금지 |
| review-plan / review-implementation / red-team / converge | 리뷰 기록(`specs/<change-id>/review.md` 등)과 자신이 판정한 Gate의 `gates.md` 줄만. 코드 수정은 지적 후 implement에서 |
| implement | 승인된 plan에 적힌 파일만. `gates.md`, `docs/09_test_cases.md`의 결과·증거 칸, `evidence/`는 수정하지 않는다 |
| verify | 테스트 결과·증거(`docs/09_test_cases.md`의 결과·증거 칸, `specs/<change-id>/evidence/`)와 `IMPLEMENTATION_COMPLETE`·`REQUIRED_TESTS_PASS` 줄만. 결과를 바꾸려고 테스트나 구현을 고치지 않는다 (필요하면 implement로 돌아간다) |

도구별 어댑터는 이 표를 복제하지 않고 가리킨다.

## 독립 리뷰

`review-plan`, `review-implementation`, `red-team`, `converge`는 **작성자와 다른 컨텍스트**가 수행한다. `MASTER_PROMPT.md` §13은 "가능하면"이라고 하지만 이 프로젝트의 규약은 **필수**로 본다. 작성자가 쓴 리뷰 Gate 줄은 무효이고, 독립 컨텍스트가 없으면 Gate는 `UNKNOWN`으로 두고 사용자가 직접 리뷰해 `USER`로 기록할 수 있다 (convention §5.2). `MASTER_PROMPT.md`를 이에 맞추는 개정은 사용자 결정이다 (`NEXT.md`).

## 부트스트랩 (v0.1 구축용)

제품 개발의 Gate와 별개로, 부트스트랩의 종료 Gate는 **`B_FINAL` 하나**다. `REVIEWER`(또는 `USER`)가 아래 체크리스트를 검토해 CRITICAL/HIGH가 없다고 판정할 때 통과한다. (`MASTER_PROMPT.md` §19 Phase 0–4, §24를 매핑한 것.)

- [ ] `docs/discovery.md`에 GREENFIELD/BROWNFIELD 판정·보존 목록·충돌 목록이 있고 기존 파일이 손실되지 않았다
- [ ] README, LICENSE, THIRD_PARTY_NOTICES, constitution, `docs/01~10`이 있고 제3자 코드가 없다
- [ ] 11개 단계 폴더 각각에 입력·산출물·Gate가 정의되어 있고 `MASTER_PROMPT.md` §5의 Gate 이름과 일치한다
- [ ] `docs/traceability-convention.md`에 ID 규칙·링크 스키마·누락 규칙·상태 계산 규칙이 있다
- [ ] Claude Code·Codex CLI 어댑터 전략 문서와 얇은 진입 파일(`CLAUDE.md`, `AGENTS.md`)이 있다

이전의 `B0_INSPECTED`~`B4_ADAPTERS` Gate는 폐지했다 (`docs/gates.md`의 해당 줄은 이력이다). 현재 값은 `docs/gates.md`를 읽는다. Phase 5(Self Test)는 `NEXT.md`에 있다.
