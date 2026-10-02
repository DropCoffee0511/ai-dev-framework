# NEXT

v0.1 부트스트랩 이후 작업. 우선순위는 `MASTER_PROMPT.md` §20을 따른다. 각 항목은 구현 전에 plan과 독립 리뷰 Gate를 거친다.

## 사용자 결정이 필요한 것

| 항목 | 내용 |
|---|---|
| 프로젝트 이름 | 작업명 `ai-dev-framework`는 확정이 아님. BMAD/Task Master 계열 이름은 사용 불가 |
| Spec Kit과의 관계 | extension / preset / 독립 CLI (현재 선호만 있음, `docs/discovery.md` A6) |
| CLI 명령어 체계 | `/project-discover`, `/feature` 등은 이름만 예약 (`adapters/claude-code/README.md`). 동작·이름 확정 필요 |
| Gate 구현 방식 | 자동 강제 수단(hooks, sandbox 등)과 Gate 기록 형식 확정 (`docs/traceability-convention.md` §5는 수동 규약) |
| 디렉터리 이름 | `ai-dev-framwork` → `ai-dev-framework` 변경 여부 |
| `MASTER_PROMPT.md` 개정 | 버전이 `0.1-draft`. 개정은 사용자 승인 후 |

## 구현 후보 (우선순위 순)

1. **Gate 자동 강제** — 현재는 에이전트가 규칙을 따르는 방식 (`docs/discovery.md` R3). 도구별 방식 조사 필요
2. **Traceability 검사 스크립트** — `docs/traceability-convention.md` §3–§5를 자동 계산. 입력은 Markdown/YAML
3. **Brownfield discovery 절차 구체화** (`workflows/discover/`) 와 `/project-discover` 동작 정의
4. **Phase 5 Self Test** — 작은 샘플 프로젝트로 Greenfield/Brownfield 흐름, 누락 requirement·permission·test 탐지, 독립 리뷰, provenance 흐름 검증
5. `agents/` 역할 문서 (analyst, architect, developer, tester, security-reviewer, independent-reviewer) — 현재는 `MASTER_PROMPT.md` §13이 정의
6. `standards/` 문서 — Greenfield는 대상 프로젝트 결정 후, Brownfield는 discover 결과에서 생성
7. Gemini CLI / Cursor / GitHub Copilot 어댑터
8. 사용자용 단순 명령 (`/project-discover`, `/feature`) 설계. `/init`은 내장 명령과 충돌

## 이월된 위험

`docs/discovery.md` §6 참조 (R1 MASTER_PROMPT 개정 시 불일치, R2 외부 라이선스 미재확인, R3 자동 Gate 없음, R4 명령 이름 충돌).
