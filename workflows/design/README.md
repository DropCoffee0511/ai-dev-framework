# design

규칙의 단일 출처: `MASTER_PROMPT.md` §5.4. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | architect |
| 목적 | Requirement → Workflow → Screen/API → Data → Permission → Error → Test를 연결 |
| 입력 | 확정된 spec, `standards/`(있다면) |
| 산출물 | `docs/03~08` 또는 `specs/<change-id>/design.md`, 초기 `traceability.md` |
| Gate | `DESIGN_READY = true` |

ID 규칙은 `docs/traceability-convention.md`. 핵심 기술 스택 변경은 사용자 승인 필요.
