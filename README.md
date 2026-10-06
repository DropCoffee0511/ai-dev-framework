# ai-dev-framework (작업명)

AI 코딩 도구(Claude Code, Codex CLI 등)로 개발할 때 **요구사항·업무흐름·데이터·권한·예외·테스트·완료조건을 먼저 명확히 하고, 명세에 맞는 최소 변경만 구현한 뒤 독립 리뷰까지 통과**하도록 만드는 운영 프레임워크.

> 상태: **v0.1 초안 (문서 전용, 검증 진행 중)**. 소스코드·CLI·자동 검사는 아직 없다. 독립 감사 2건(`docs/audits/audit-001.md`, `docs/audits/audit-002.md`)이 모두 `B_FINAL = FAIL`이었고, 지적의 일부를 고친 상태다. 현재 Gate 값은 `docs/gates.md`, 남은 작업은 `NEXT.md`에 있다. 프로젝트 이름은 작업명이며 확정되지 않았다 (`docs/discovery.md` A1).

## 해결하려는 문제

기능이 늘수록 구조가 무너짐 / AI의 요구사항 누락 / 한 기능 수정 시 기존 기능 파손 / 화면과 API의 권한 불일치 / 늦게 발견되는 예외 / AI가 스스로 "완료"를 선언 / 도구마다 다른 프로젝트 이해 / 이미 만들어진 프로젝트를 정리하기 어려움.

## 구조

```text
MASTER_PROMPT.md        최상위 운영 규칙 (모든 규칙의 단일 출처)
BOOTSTRAP.md            첫 실행 지시
ADOPTING.md             다른 프로젝트에 적용하는 방법 (복사 허용 목록, Greenfield/Brownfield 절차)
constitution/           원칙
docs/                   01~10 문서 템플릿(대상 프로젝트용), traceability-convention.md,
                        그리고 이 저장소 자체의 기록: discovery.md, gates.md, audits/ (ADOPTING.md §1)
specs/                  변경 단위 명세 (specs/README.md)
workflows/              11단계 개발 흐름의 입력·산출물·Gate
adapters/               Claude Code / Codex CLI 진입 전략
CLAUDE.md, AGENTS.md    도구별 얇은 진입 파일 (규칙은 MASTER_PROMPT.md를 가리킴)
LICENSE                 MIT
THIRD_PARTY_NOTICES.md  가져온 제3자 코드 (현재 없음)
REFERENCES.md           아이디어만 참고한 프로젝트
NEXT.md                 다음 작업
CHANGELOG.md            변경 이력
```

## 사용 방법 (v0.1)

1. **다른 프로젝트에 적용하려면 `ADOPTING.md`를 먼저 읽는다.** 이 저장소를 그대로 앱 저장소로 쓰지 않는다 (이 저장소 자체의 기록이 섞여 있다).
2. 이 저장소 자체를 작업할 때는 AI 에이전트를 이 저장소 루트에서 실행하고, `MASTER_PROMPT.md`를 읽고 따르라고 지시한다 (`CLAUDE.md`/`AGENTS.md`가 자동으로 안내한다).
3. 개발 흐름은 `discover → specify → clarify → design → plan → review-plan → implement → verify → review-implementation → red-team → converge` 순서이며, 각 단계의 Gate를 통과해야 다음으로 넘어간다 (`workflows/README.md`).
4. 기능은 `docs/traceability-convention.md`의 규칙으로 요구사항부터 코드·테스트까지 연결되어야 완료로 본다.

## 현재 한계

- **규칙은 에이전트가 따르는 방식이다.** Gate·승인 기록을 자동으로 강제하는 수단이 없고, 판정자 칸은 자유 텍스트라 위조를 막지 못한다 (`docs/traceability-convention.md` §5.4).
- **실제 프로젝트에 적용해 본 시험을 아직 하지 않았다.** `ADOPTING.md`는 문서 검토로만 검증했다 (`ADOPTING.md` §7).
- 독립 감사의 지적 일부가 아직 해결되지 않았다. audit-001의 HIGH 항목 일부와 audit-002의 H-04(템플릿과 자체 기록이 섞여 있음)가 남아 있다 (`NEXT.md`).
- 템플릿과 이 저장소 자체의 기록이 `docs/`에 함께 있다. 구분은 `ADOPTING.md`의 목록으로만 한다.
- `MASTER_PROMPT.md`는 `0.1-draft`이며, 개정 후보는 `NEXT.md`에 있다.

## 라이선스

MIT (`LICENSE`). 외부 프로젝트의 코드는 포함하지 않았다 (`THIRD_PARTY_NOTICES.md`). 외부 프로젝트의 라이선스 분류 근거와 일부 원천 문서의 권리 귀속은 아직 검증되지 않았다 (같은 파일의 `NEEDS LICENSE VERIFICATION`). 참고한 프로젝트와 사용하지 않는 대상(Task Master 소스, BMAD 상표)은 `REFERENCES.md`와 `MASTER_PROMPT.md` §15에 있다.
