# red-team

규칙의 단일 출처: `MASTER_PROMPT.md` §5.10. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | security-reviewer / independent-reviewer |
| 목적 | 작성자가 기대하지 않은 사용 방식(직접 URL/API 호출, 중복 제출, 동시 수정 등)으로 검토. 위험도에 맞춰 수행 |
| 입력 | 구현, 권한 정의, 오류 정의 |
| 산출물 | red-team 발견 목록 (심각도 포함) |
| Gate | `NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS = true` |


