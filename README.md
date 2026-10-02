# ai-dev-framework (작업명)

AI 코딩 도구(Claude Code, Codex CLI 등)로 개발할 때 **요구사항·업무흐름·데이터·권한·예외·테스트·완료조건을 먼저 명확히 하고, 명세에 맞는 최소 변경만 구현한 뒤 독립 리뷰까지 통과**하도록 만드는 운영 프레임워크.

> 상태: **v0.1 부트스트랩 (문서 전용)**. 소스코드·CLI·자동 검사는 아직 없다. 프로젝트 이름은 작업명이며 확정되지 않았다 (`docs/discovery.md` A1).

## 해결하려는 문제

기능이 늘수록 구조가 무너짐 / AI의 요구사항 누락 / 한 기능 수정 시 기존 기능 파손 / 화면과 API의 권한 불일치 / 늦게 발견되는 예외 / AI가 스스로 "완료"를 선언 / 도구마다 다른 프로젝트 이해 / 이미 만들어진 프로젝트를 정리하기 어려움.

## 구조

```text
MASTER_PROMPT.md        최상위 운영 규칙 (모든 규칙의 단일 출처)
BOOTSTRAP.md            첫 실행 지시
constitution/           원칙
docs/                   01~10 문서 템플릿, discovery.md, traceability-convention.md
specs/                  변경 단위 명세 (specs/README.md)
workflows/              11단계 개발 흐름의 입력·산출물·Gate
adapters/               Claude Code / Codex CLI 진입 전략
CLAUDE.md, AGENTS.md    도구별 얇은 진입 파일 (규칙은 MASTER_PROMPT.md를 가리킴)
LICENSE                 MIT
THIRD_PARTY_NOTICES.md  가져온 제3자 코드 (현재 없음)
REFERENCES.md           아이디어만 참고한 프로젝트
NEXT.md                 다음 작업
```

## 사용 방법 (v0.1)

1. AI 에이전트를 이 저장소 루트에서 실행한다.
2. 에이전트에게 `MASTER_PROMPT.md`를 읽고 따르라고 지시한다 (`CLAUDE.md`/`AGENTS.md`가 자동으로 안내한다).
3. 개발 흐름은 `discover → specify → clarify → design → plan → review-plan → implement → verify → review-implementation → red-team → converge` 순서이며, 각 단계의 Gate를 통과해야 다음으로 넘어간다 (`workflows/README.md`).
4. 기능은 `docs/traceability-convention.md`의 규칙으로 요구사항부터 코드·테스트까지 연결되어야 완료로 본다.

## 라이선스

MIT (`LICENSE`). 외부 프로젝트의 코드는 포함하지 않았다 (`THIRD_PARTY_NOTICES.md`). 참고한 프로젝트와 사용하지 않는 대상(Task Master 소스, BMAD 상표)은 `REFERENCES.md`와 `MASTER_PROMPT.md` §15에 있다.
