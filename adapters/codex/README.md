# Codex CLI adapter

진입 파일: 저장소 루트의 `AGENTS.md`. 이 파일은 다른 파일을 import하지 않으므로, `AGENTS.md`가 **읽어야 할 파일 목록을 명시**한다.
공통 규칙은 `adapters/README.md`와 `MASTER_PROMPT.md`가 정의한다. 아래는 Codex CLI에만 해당하는 사용 방법이다.

## 시작 프롬프트

```text
AGENTS.md가 가리키는 파일을 모두 읽고, MASTER_PROMPT.md의 규칙에 따라 작업하라.
현재 Gate를 먼저 보고하라 (기록 위치: docs/traceability-convention.md §5, 기록이 없으면 UNKNOWN).
통과하지 않은 Gate의 다음 단계로 진행하지 마라.
```

## 독립 리뷰 만들기

| 방법 | 설명 |
|---|---|
| 새 세션 | 구현한 세션과 다른 Codex 세션을 열고 코드와 `specs/<change-id>/` 문서만 읽힌다 |
| 다른 도구 | Claude Code가 구현했다면 Codex CLI가 리뷰한다 (또는 반대) — `adapters/README.md` |

## 단계별 읽기/쓰기 제한

공통 규약은 `workflows/README.md`의 "단계별 쓰기 허용 범위"를 따른다.
Codex의 sandbox/approval 모드로 자동 강제하는 방법은 `NEXT.md`에서 별도 계획을 거친다.
