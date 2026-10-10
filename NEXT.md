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
| 폴더 구조 변경 | 대상 프로젝트 설치 모델(H4, audit-002 H-04)은 2026-10-06에 `ADOPTING.md`(복사 허용 목록 + Greenfield/Brownfield 절차)로 대응했고 폴더는 옮기지 않았다. 템플릿과 자기 기록(`docs/discovery.md`·`gates.md`·`audits/`)을 **물리적으로 분리**하려면 약 16개 파일의 참조 약 65곳 수정이 필요하고, 템플릿 위치를 `docs/01~10`으로 정한 `MASTER_PROMPT.md` §12·§19 개정이 필요할 수 있다 (사용자 승인 필요). 엄격한 감사는 "섞여 있음"을 다시 지적할 수 있다 |

## 진행 중 / 보류

- **wave 002 잔여 지적 흡수 — 수정 완료, 신규 커밋 대상 재검토 대기 (2026-10-10)** — N1(HIGH: gates.md `## 기록` 절 부재 크래시)·R1(HIGH: 거짓 DONE 경로)과 N2·N3·R2·R3·R5·TRACEABILITY_COMPLETE 교차검증을 수정했다. CLAUDE.md 미갱신·git 요구 문서화·R6·R7·R8도 함께 처리했다. R4는 convention 대조 후 동작 유지·v0 한계 명시로 처리했고 방향 확정은 사용자 결정이다. `--self-test` 44건 통과, 자기 저장소 적용 위반 0건, ADOPTING 절차 /tmp 시뮬레이션(새 프로젝트 첫 실행 2케이스) 통과. 경위는 `PROGRESS.md` wave 002 참조
- **ADOPTING.md §1 복사 허용 목록에 `scripts/` 분류 추가 — 완료 (2026-10-10)**: `scripts/check_traceability.py` 1줄 추가. 근거: convention 도입 안내가 이 스크립트를 §3–§5 계산기로 가리키므로 채택 프로젝트의 상태 계산에 필요하다 (`CHANGELOG.md`, `PROGRESS.md` wave 002)
- **Codex CLI 독립 감사: 2026-10-06 수행, `B_FINAL = FAIL`** (CRITICAL 0, HIGH 4, MEDIUM 12, LOW 3). 대상은 규칙 단순화 후 커밋 `bfbe160`. 결과는 `docs/audits/audit-002.md`, Gate 기록은 `docs/gates.md`. 10월 2일에 거부됐던 `gpt-6.1-sol`이 이번에는 ChatGPT 로그인(OAuth)으로 작동했다(원인 미확인, 설정 파일은 수정하지 않음). **처리 상황(2026-10-06): H-01~H-03, M-03, M-10은 사용자 승인 계획대로 최소 수정했다(규칙 문서 순증가 6줄). 새 컨텍스트의 verifier가 두 번 검증했다(1차 FAIL: 재판정 명령이 미추적 새 파일을 놓침 → 반영, 2차 PASS: CRITICAL/HIGH/MEDIUM 없음). 단 미추적 파일 동작은 실험이 아니라 표준 git 지식에 근거한다(실험 권한 거부). H-04는 `ADOPTING.md`로 대응했다(새 컨텍스트 검증자 3회: 1차 FAIL MEDIUM 3건, 2차 FAIL MEDIUM 1건을 각각 반영한 뒤 3차 PASS. H-04 "적용 절차 없음"은 해소, "섞여 있음"은 부분 해소. 3차의 미수정 LOW: 진입 블록의 "§19·§24의 '이 저장소'" 표현이 부정확함, §23 6~7번(최소 문서 구조·plan/review gate 생성)의 처리가 명시되지 않음, 위 "약 16개 파일/65곳" 산정 근거가 재현되지 않음. 진입 블록 문제의 근본 해결은 `MASTER_PROMPT.md` 개정(M13)이다). 나머지(M-01·M-02·M-04~M-09·M-11·M-12, LOW 전부)는 미수정이며 `B_FINAL`은 여전히 `false`다.** HIGH: H-01 등록 AC/REQ의 부분집합 누락을 탐지 못함 / H-02 계산된 DONE이 §6 DoD보다 약하고 red-team HIGH를 차단하지 않음 / H-03 재판정이 커밋 해시에만 의존해 미커밋 변경을 놓침 / H-04 대상 프로젝트 적용 방법 없음(= audit-001 H4, 폴더 재구성은 사용자 승인 필요). M-03(다중 REQ의 Gate 선택)과 M-10(구 형식 기록 인정 범위)은 2026-10-06에 추가한 문구와 관련된다. 지적 대부분의 해결책이 규칙을 늘리는 방향이므로 남은 항목도 수정 범위를 정한 뒤 진행한다. 이번 수정의 검증에서 나온 미수정 LOW: `not_applicable`을 쓰면 등록된 PERM/ERR가 있어도 PASS가 될 수 있음(L-1), spec.md의 REQ 목록 선언 형식과 프로젝트 단위의 선언처가 없음(L-4), AC의 `RETIRED` 표기 칸이 없음(L-7). 2차 검증의 미수정 LOW: Gate 판정 전 커밋을 누가 언제 하는지 절차가 없음, §5.1 "판정 단계 자신의 산출물" 문구가 모호함, `NO_CRITICAL_OPEN_ISSUES`가 이름과 달리 HIGH도 막는데 `workflows/converge/README.md`에 포인터가 없음, `ACCEPTANCE` 근거의 DoD 확인에 작성자 구분이 없음.
- **audit-001 미해결 항목**: H1~H8(Gate 통과 조건, blocker 칸, `review.md`·`tasks.md` 형식, 설치 모델(`ADOPTING.md`로 대응, 위 결정 사항 표 참조), converge 재작업 루프, N/A 승인자·DoD 일치), M1~M15, L5~L10. `docs/audits/audit-001.md` 참조. C1~C3, H6, H9, L1~L4, Kiro는 수정함. 수정분은 새 컨텍스트의 verifier가 1차 검증했고(6개 수정 중 5개 DONE, C1은 PARTIAL), 그때 나온 새 지적 N1~N8(Review 값 우회 경로, 일부 Gate의 기록 주체 부재, B0~B4 판정자 표 누락, DONE 정의 불일치, 승인 조항 인용 부정확, USER 기록 방식 모순, 독립 리뷰 "가능하면"과 규약 불일치, 어댑터 포인터)을 반영했다. 2차 검증(새 컨텍스트)도 FAIL이었고(HIGH 2: 코드 변경 후 리뷰·승인 재판정 규칙 없음, `gates.md` 기록 주체 규칙 충돌 / MEDIUM 5), 그 지적도 반영했다(`STALE` 값, 오케스트레이터 대리 기록, 범위 규칙 등). **2차 지적 반영분은 아직 재검증하지 않았다.** 검증 보고는 저장된 파일이 없고 대화 보고뿐이며, `docs/gates.md`에도 수정분 판정은 기록하지 않았다. 규칙이 계속 늘어나는 점 자체가 과잉 설계 위험(audit-001 Over-engineered)이므로 2026-10-05에 Gate/승인 메커니즘을 단순화했다 (판정자 유형 3→2, `EXEMPT_*`·부트스트랩 `B0`~`B4` 폐지, 기록 표 8→5칸, 규칙 단일 출처를 convention §5로 통합). 단순화분은 새 컨텍스트의 verifier가 두 번 검증했다(1차 FAIL: MEDIUM 2·LOW 6 → 반영, 2차 PASS: CRITICAL/HIGH/MEDIUM 없음). 2차 이후 남은 LOW: `docs/02_requirements.md`의 `<DRAFT>` 상태 칸 값 정의 없음, implement 쓰기 범위에 `traceability.md`·`tasks.md` 명시 없음, Gate 순서 표의 implement→verify 행 전제 표기. `docs/gates.md`의 `기록` 표에는 `B_FINAL = false` 외의 줄이 없어 나머지 Gate(`DISCOVERY_COMPLETE` 포함)는 `UNKNOWN`이며 재판정이 필요하다.

## 구현 후보 (우선순위 순)

1. **Gate 자동 강제** — 현재는 에이전트가 규칙을 따르는 방식 (`docs/discovery.md` R3). 도구별 방식 조사 필요
2. **Traceability 검사 스크립트** — **완료 (2026-10-10)**: `scripts/check_traceability.py`. `docs/traceability-convention.md` §3–§5를 자동 계산한다(입력 Markdown/YAML). 단일 파일·외부 의존성 없음 원칙 준수. 1차 독립 검토(`docs/audits/wave002-review-2026-10-10.md`) FAIL(계산 격차 HIGH 2건 포함 13지적)의 지적을 수정했고 재검증(`docs/audits/wave002-reverify-2026-10-10.md`, 런 `dwfrun-edf17f7f`)에서 지적 9건 전부 RESOLVED·규칙 약화 0건으로 **APPROVE**. `--self-test` 27건, 자기 저장소 적용 위반 0건. 경위는 `PROGRESS.md` wave 002
3. **Brownfield discovery 절차 구체화** (`workflows/discover/`) 와 `/project-discover` 동작 정의
4. **Phase 5 Self Test** — 작은 샘플 프로젝트로 Greenfield/Brownfield 흐름, 누락 requirement·permission·test 탐지, 독립 리뷰, provenance 흐름 검증
5. `agents/` 역할 문서 (analyst, architect, developer, tester, security-reviewer, independent-reviewer) — 현재는 `MASTER_PROMPT.md` §13이 정의
6. `standards/` 문서 — Greenfield는 대상 프로젝트 결정 후, Brownfield는 discover 결과에서 생성
7. Gemini CLI / Cursor / GitHub Copilot 어댑터
8. 사용자용 단순 명령 (`/project-discover`, `/feature`) 설계. `/init`은 내장 명령과 충돌

## 이월된 위험

`docs/discovery.md` §6 참조 (R1 MASTER_PROMPT 개정 시 불일치, R2 외부 라이선스 미재확인, R3 자동 Gate 없음, R4 명령 이름 충돌).
