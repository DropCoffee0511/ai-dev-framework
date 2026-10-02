# verify

규칙의 단일 출처: `MASTER_PROMPT.md` §5.8. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | tester |
| 목적 | 정상/예외/경계/회귀 검증. 결과를 숨기지 않는다 |
| 입력 | 구현, `test-plan.md`, `docs/09_test_cases.md` |
| 산출물 | TC별 PASS/FAIL/NOT RUN 결과 |
| Gate | `REQUIRED_TESTS_PASS = true` |

실행하지 않은 테스트를 PASS로 쓰지 않는다 (§18). PASS/FAIL에는 실행 일시·명령·커밋·증거 경로를 함께 기록한다 (`docs/09_test_cases.md`). 증거가 없는 PASS는 `NOT RUN`이다. 쓰기 범위는 `workflows/README.md`의 verify 행을 따른다.
