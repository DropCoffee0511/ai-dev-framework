# clarify

규칙의 단일 출처: `MASTER_PROMPT.md` §5.3. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | analyst |
| 목적 | 모순·미정의 상태·불명확한 권한·누락된 예외 탐지 |
| 입력 | spec, acceptance |
| 산출물 | 열린 질문 목록, 가정 기록 (`ASSUMPTION / IMPACT / REVERSIBLE`) |
| Gate | `SPEC_AMBIGUITY_BLOCKERS = 0` |

핵심 업무 규칙에 영향을 주는 가정은 사용자 확인 없이 확정하지 않는다 (§22). 이 단계가 끝나면 사용자 승인 기록 `APPROVAL_SPEC`을 받아 `gates.md`에 기록한 뒤 design으로 진행한다 (`workflows/README.md` 사용자 승인 기록).
