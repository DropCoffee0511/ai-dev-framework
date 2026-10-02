# adapters

에이전트별 진입 방식. **어댑터는 공통 규칙을 덮어쓰지 않는다** (`MASTER_PROMPT.md` §14).

## 전략

```text
공통 규칙 (단일 출처)                     어댑터 (얇은 진입점)
MASTER_PROMPT.md                          CLAUDE.md                → Claude Code
constitution/                             AGENTS.md                → Codex CLI (및 AGENTS.md를 읽는 도구)
docs/  specs/  standards/                 adapters/<agent>/README.md → 도구별 사용법
```

- 공통 규칙은 위 왼쪽 파일에만 둔다. 어댑터 파일에 규칙을 복사하지 않는다 (복사하면 두 곳이 어긋난다).
- 어댑터가 하는 일: (1) 어떤 파일을 읽을지 알려준다, (2) 도구 고유의 사용법(서브에이전트, 권한 설정)을 적는다.
- 도구 전용 기능(Claude Code의 서브에이전트 등)을 **핵심 로직으로 쓰지 않는다.** 없어도 같은 Gate가 동작해야 한다.
- 독립 리뷰는 도구에 따라 다른 방식으로 만든다 (아래). 목표는 "작성자와 다른 컨텍스트"이다.

## 지원 현황

| 도구 | 진입 파일 | 상태 |
|---|---|---|
| Claude Code | `CLAUDE.md`, `adapters/claude-code/` | v0.1 전략 정의 |
| Codex CLI | `AGENTS.md`, `adapters/codex/` | v0.1 전략 정의 |
| Gemini CLI, Cursor, GitHub Copilot | — | 추후 (`NEXT.md`) |

## 도구 간 독립 리뷰

구현을 한 도구가 아닌 **다른 도구**가 리뷰할 수 있다 (예: Claude Code가 구현 → Codex CLI가 리뷰, 또는 반대). 이때 리뷰어에게 넘기는 것은 코드와 `specs/<change-id>/` 문서이지 구현자의 대화 내용이 아니다.
