# review-plan

규칙의 단일 출처: `MASTER_PROMPT.md` §5.6. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | independent-reviewer (plan 작성자와 다른 컨텍스트) |
| 목적 | 계획의 누락·범위 확대·위험을 심각도(CRITICAL/HIGH/MEDIUM/LOW)로 평가 |
| 입력 | plan, spec, design |
| 산출물 | `specs/<change-id>/review.md`의 plan 리뷰 항목 |
| Gate | `PLAN_REVIEW_PASS = true` |

CRITICAL 또는 HIGH가 미해결이면 IMPLEMENT로 진행하지 않는다. 작성자가 자기 plan을 승인하지 않는다.
