# review-implementation

규칙의 단일 출처: `MASTER_PROMPT.md` §5.9. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | independent-reviewer (구현자와 다른 컨텍스트) |
| 목적 | spec과 실제 구현의 불일치 발견. 코드 미화가 목적이 아님 |
| 입력 | spec, 구현 diff, 테스트 결과 |
| 산출물 | `specs/<change-id>/review.md`의 구현 리뷰 항목 |
| Gate | `IMPLEMENTATION_REVIEW_PASS = true` |


