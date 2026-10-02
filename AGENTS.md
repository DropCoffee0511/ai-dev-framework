# AGENTS.md

이 파일은 Codex CLI 등 AGENTS.md를 읽는 에이전트용 **adapter**다. 공통 규칙을 정의하지 않고 가리키기만 한다 (`MASTER_PROMPT.md` §14). 충돌하면 아래 문서가 우선한다.

작업을 시작하기 전에 다음 파일을 **전체 읽고** 적용한다.

1. `MASTER_PROMPT.md` — 최상위 운영 규칙
2. `constitution/principles.md` — 원칙
3. `docs/discovery.md` — 현재 상태 조사
4. `workflows/README.md` — 단계 Gate와 쓰기 허용 범위
5. `docs/traceability-convention.md` — ID·링크·상태 계산·Gate 기록
6. `NEXT.md` — 다음 작업

`BOOTSTRAP.md`는 **첫 실행(v0.1 구축) 전용**이다. 부트스트랩은 `docs/discovery.md`에 기록된 대로 수행되었으므로 일상 작업에서는 읽어 적용하지 않는다. 사용자가 부트스트랩 재실행을 지시할 때만 따른다.

Codex CLI 전용 세부 사항: `adapters/codex/README.md`

## 저장소 현황

문서 전용 저장소다 (2026-10-02 기준 소스코드·manifest 없음). 실행할 build/lint/test 명령이 아직 없다.
`261002 대화내용.txt`는 설계 원천 기록이므로 수정하지 않는다.
