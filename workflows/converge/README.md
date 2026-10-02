# converge

규칙의 단일 출처: `MASTER_PROMPT.md` §5.11. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | independent-reviewer |
| 목적 | 문서와 코드를 다시 맞추고 불일치를 분류 (CODE_BUG / SPEC_OUTDATED / DOC_OUTDATED / TEST_MISSING / INTENT_UNKNOWN) |
| 입력 | 전 단계 산출물, traceability |
| 산출물 | 최종 `traceability.md`, 불일치 분류 목록 |
| Gate | `TRACEABILITY_COMPLETE = true, NO_CRITICAL_OPEN_ISSUES = true` |

의도가 불명확한 항목은 조용히 고치지 않고 `INTENT_UNKNOWN`으로 남긴다.
