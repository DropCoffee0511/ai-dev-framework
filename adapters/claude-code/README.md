# Claude Code adapter

진입 파일: 저장소 루트의 `CLAUDE.md` (공통 규칙은 `@MASTER_PROMPT.md`로 import).
공통 규칙은 `adapters/README.md`와 `MASTER_PROMPT.md`가 정의한다. 아래는 Claude Code에만 해당하는 사용 방법이다.

## 독립 리뷰 만들기

| 단계 | 방법 |
|---|---|
| `review-plan`, `review-implementation`, `red-team`, `converge` | 새 컨텍스트의 서브에이전트(Agent 도구)에게 **문서와 diff만** 전달한다. 구현 과정의 추론을 넘기지 않는다 |
| 더 강한 분리가 필요할 때 | 별도 도구(Codex CLI 등)가 리뷰한다 — `adapters/README.md` |

서브에이전트를 쓸 수 없는 환경이면 같은 컨텍스트에서 자기 승인을 하지 말고 사용자에게 리뷰를 요청한다.

## 단계별 읽기/쓰기 제한

공통 규약은 `workflows/README.md`의 "단계별 쓰기 허용 범위"를 따른다.
v0.1에서는 에이전트가 규약을 따르는 방식이다. Claude Code의 권한 설정(hooks, permissions)으로 자동 강제하는 방법은 `NEXT.md`에서 별도 계획·리뷰를 거친다.

## 명령 이름 예약

`/project-discover`, `/feature`는 이름만 예약한다 (동작 미정의). `/init`은 Claude Code 내장 명령과 충돌하므로 확정하지 않는다 (`docs/discovery.md` R4).
