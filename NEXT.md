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
| `MASTER_PROMPT.md` 개정 | 버전이 `0.1-draft`. 개정은 사용자 승인 후. 감사에서 나온 개정 후보: (1) 사용자 승인 기록을 §5 Gate로 정식화 (현재는 `workflows/README.md`의 추가 요구), (2) 독립 리뷰어 분리를 "가능하면"에서 필수로 (M1), (3) red-team 필수 조건과 High 처리 기준 (M5), (4) §23 "첫 실행 시" 문구가 `@import`로 매 세션 로드되는 문제 (M13) |
| 설계 대화록 처리 | `261002 대화내용.txt`는 공개 저장소에 있고 ChatGPT 내부 표식이 15곳 남아 있음. 선택지: 그대로 둠 / 이후 커밋에서만 제거(이력에는 남음) / 이력까지 재작성(강제 푸시, 되돌릴 수 없음). 장기적으로 결정 기록(ADR)만 남기는 안이 제안됨 |
| 라이선스 미검증 항목 | `THIRD_PARTY_NOTICES.md`의 `NEEDS LICENSE VERIFICATION` 3건 (외부 분류 근거, MASTER_PROMPT·BOOTSTRAP·대화록의 권리 귀속, 단계 이름 유사성) |
| 폴더 구조 변경 | 대상 프로젝트 설치 모델(H4)을 위해 템플릿과 자기 기록을 분리하려면 `docs/` 재구성이 필요함 (승인 필요) |

## 진행 중 / 보류

- **Codex CLI 독립 감사: 미실행.** 2026-10-02 시도에서 Codex 기본 모델 `gpt-6.1-sol`이 ChatGPT 계정 로그인에서 지원되지 않아 분석 시작 전에 거부됨. 지원 모델을 지정하거나 `~/.codex/config.toml`의 기본 모델을 바꾼 뒤 재시도해야 함. 감사 대상은 커밋 `b9c8c61`(수정 전). 결과는 `docs/audits/audit-002.md`로 기록하고 `docs/gates.md`에 반영.
- **audit-001 미해결 항목**: H1~H8(Gate 통과 조건, blocker 칸, `review.md`·`tasks.md` 형식, 설치 모델, converge 재작업 루프, N/A 승인자·DoD 일치), M1~M15, L5~L10. `docs/audits/audit-001.md` 참조. C1~C3, H6, H9, L1~L4, Kiro는 수정함. 수정분은 새 컨텍스트의 verifier가 1차 검증했고(6개 수정 중 5개 DONE, C1은 PARTIAL), 그때 나온 새 지적 N1~N8(Review 값 우회 경로, 일부 Gate의 기록 주체 부재, B0~B4 판정자 표 누락, DONE 정의 불일치, 승인 조항 인용 부정확, USER 기록 방식 모순, 독립 리뷰 "가능하면"과 규약 불일치, 어댑터 포인터)을 반영했다. 2차 검증(새 컨텍스트)도 FAIL이었고(HIGH 2: 코드 변경 후 리뷰·승인 재판정 규칙 없음, `gates.md` 기록 주체 규칙 충돌 / MEDIUM 5), 그 지적도 반영했다(`STALE` 값, 오케스트레이터 대리 기록, 범위 규칙 등). **2차 지적 반영분은 아직 재검증하지 않았다.** 검증 보고는 저장된 파일이 없고 대화 보고뿐이며, `docs/gates.md`에도 수정분 판정은 기록하지 않았다. 규칙이 계속 늘어나는 점 자체가 과잉 설계 위험(audit-001 Over-engineered)이므로 2026-10-05에 Gate/승인 메커니즘을 단순화했다 (판정자 유형 3→2, `EXEMPT_*`·부트스트랩 `B0`~`B4` 폐지, 기록 표 8→5칸, 규칙 단일 출처를 convention §5로 통합). 단순화분은 새 컨텍스트의 verifier가 두 번 검증했다(1차 FAIL: MEDIUM 2·LOW 6 → 반영, 2차 PASS: CRITICAL/HIGH/MEDIUM 없음). 2차 이후 남은 LOW: `docs/02_requirements.md`의 `<DRAFT>` 상태 칸 값 정의 없음, implement 쓰기 범위에 `traceability.md`·`tasks.md` 명시 없음, Gate 순서 표의 implement→verify 행 전제 표기. `docs/gates.md`의 `DISCOVERY_COMPLETE`는 여전히 `STALE`이며 재판정이 필요하다.

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
