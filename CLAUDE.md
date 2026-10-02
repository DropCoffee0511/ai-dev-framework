# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

이 파일은 **adapter**다. 공통 규칙을 정의하지 않고 가리키기만 한다 (`MASTER_PROMPT.md` §14). 이 파일의 내용이 아래 문서와 충돌하면 아래 문서가 우선한다.

@MASTER_PROMPT.md

## 먼저 읽을 것

1. `MASTER_PROMPT.md` — 최상위 운영 규칙 (위에서 import됨)
2. `constitution/principles.md`, `docs/discovery.md` — 원칙과 현재 상태 조사
3. `workflows/README.md` — 단계 Gate와 쓰기 허용 범위
4. `docs/traceability-convention.md` — ID·링크·상태 계산·Gate 기록
5. `NEXT.md` — 다음 작업

`BOOTSTRAP.md`는 **첫 실행(v0.1 구축) 전용**이다. 부트스트랩은 `docs/discovery.md`에 기록된 대로 수행되었으므로 일상 작업에서는 적용하지 않는다. 사용자가 재실행을 지시할 때만 따른다.

Claude Code 전용 세부 사항: `adapters/claude-code/README.md`

## 저장소 현황

- 문서 전용 저장소다 (2026-10-02 기준 소스코드·manifest 없음). 실행할 build/lint/test 명령이 아직 없으므로 지어내지 말고, 도입하면 이 파일에 추가한다.
- `261002 대화내용.txt`는 설계 원천 기록이다. 수정하지 않는다. 파일명에 공백·한글이 있으므로 셸에서는 따옴표로 감싼다.
- 디렉터리 이름 `ai-dev-framwork`는 철자가 틀린 상태 그대로 둔다 (이름 변경은 사용자 승인 필요).
