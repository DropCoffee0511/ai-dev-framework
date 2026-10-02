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
| `DESIGN_READY` | `DESIGNED` |
| `PLAN_READY` | `PLANNED` |
| `PLAN_REVIEW_PASS` | `PLAN_REVIEWED` |
| implement 시작 | `IMPLEMENTING` |
| `IMPLEMENTATION_COMPLETE` | (상태 변화 없음. verify 진입 조건) |
| `REQUIRED_TESTS_PASS` | `VERIFIED` |
| `IMPLEMENTATION_REVIEW_PASS` | `REVIEWED` |
| red-team + converge Gate 모두 통과 | `DONE` |

상태가 `PLAN_REVIEWED`가 아닌데 구현을 시도하면 `BLOCKED`로 보고하고 코딩하지 않는다. (v0.1에서는 에이전트가 규칙을 따르는 방식이며, 자동 강제는 `NEXT.md`.)

Gate 값의 기록 위치와 기록 주체는 `docs/traceability-convention.md` §5를 따른다.

## 단계별 쓰기 허용 범위 (공통 규약)

| 단계 | 쓰기 허용 범위 |
|---|---|
| discover / specify / clarify / design / plan | `docs/`, `specs/` 등 문서만. 애플리케이션 코드 수정 금지. `constitution/`과 `MASTER_PROMPT.md`는 사용자 승인 없이 수정 금지 |
| review-plan / review-implementation / red-team / converge | 리뷰 기록(`specs/<change-id>/review.md` 등)만. 코드 수정은 지적 후 implement 단계에서 |
| implement | 승인된 plan에 적힌 파일만 |

도구별 어댑터는 이 표를 복제하지 않고 가리킨다.

## 독립 리뷰 규칙

`review-plan`, `review-implementation`, `red-team`, `converge`는 가능하면 **작성자와 다른 컨텍스트**(다른 에이전트/서브에이전트/도구)가 수행한다 (`MASTER_PROMPT.md` §13). 같은 컨텍스트가 자기 작업을 승인하지 않는다.

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

Phase 5(Self Test)는 이번 범위 밖이며 `NEXT.md`에 있다.
