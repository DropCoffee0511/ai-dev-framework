# implement

규칙의 단일 출처: `MASTER_PROMPT.md` §5.7. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | developer |
| 목적 | 승인된 plan 범위 안에서 최소 변경 구현 + 필요한 테스트 추가 |
| 입력 | 승인된 plan, tasks |
| 산출물 | 코드, 테스트, 갱신된 문서, 코드↔REQ 링크 |
| Gate | `IMPLEMENTATION_COMPLETE = true` |

진입 조건: `PLAN_REVIEW_PASS = true`. 아니면 `BLOCKED (PLAN_REVIEW_PASS gate has not passed)`로 보고하고 코딩하지 않는다.
