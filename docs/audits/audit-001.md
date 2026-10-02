# Audit 001 — Independent audit of v0.1 bootstrap

- 일자: 2026-10-02
- 대상: 커밋 `b9c8c61`
- 감사자: claude-code architect 서브에이전트 (읽기 전용, 이 저장소를 작성한 컨텍스트와 분리된 새 컨텍스트). 사용자가 제공한 감사 프롬프트(Independent Reviewer / 11개 항목 + Greenfield·Brownfield 시나리오)로 수행
- 판정: **`B_FINAL = FAIL`** (CRITICAL 3, HIGH 9)
- 한계: 같은 모델 계열이다. 다른 계열(Codex CLI) 감사는 별도로 수행한다 (`audit-002`로 기록 예정, 이 파일에는 없음)
- 이 파일은 원 보고서의 **지적 목록 요약**이다. 전문은 보존하지 않았다.

## CRITICAL

| ID | 지적 | 처리 |
|---|---|---|
| C1 | Gate 값이 구현자도 수정하는 `traceability.md`에 기록되고 강제 수단이 없음 | 수정함 (`docs/gates.md`, convention §5) |
| C2 | 사용자 승인을 기록하는 Gate가 없음 | 수정함 (`workflows/README.md` 사용자 승인 기록) |
| C3 | 테스트 PASS에 실행 증거가 없고 TC↔테스트 코드 연결 규약이 없음 | 수정함 (`docs/09_test_cases.md`, convention §4) |

## HIGH

| ID | 지적 | 처리 |
|---|---|---|
| H1 | 12개 Gate 중 11개는 통과 조건이 정의되지 않음 | 미해결 |
| H2 | `SPEC_AMBIGUITY_BLOCKERS = 0`을 계산할 수 없음 (blocker 칸 없음, 값 형식 불일치) | 미해결 |
| H3 | `review.md`, `tasks.md` 형식 없음 | 미해결 |
| H4 | 대상 프로젝트 적용 방법 없음, 템플릿과 자기 기록이 같은 `docs/`에 섞임 | 미해결 (폴더 재구성은 사용자 승인 필요) |
| H5 | converge 산출물과 쓰기 허용 범위 모순, 재작업 루프 없음 | 미해결 |
| H6 | 쓰기 허용 범위 표에 verify 행 없음 | 수정함 |
| H7 | 앞 단계 문서 변경 시 Gate가 무효화되지 않음 | 일부 수정함 (convention §5의 기준 커밋 비교). 재작업 루프는 미해결 |
| H8 | 계산된 DONE이 Definition of Done과 다름 (`not_applicable` 승인자 없음 등) | 미해결 |
| H9 | B_FINAL 기록이 없는데 "부트스트랩 수행됨"이라고 단정 | 수정함 (`docs/gates.md`, `AGENTS.md`, `CLAUDE.md`) |

## MEDIUM / LOW (요약)

- MEDIUM M1~M15: 리뷰어 분리 "가능하면" vs 필수 불일치, REQ 정의 위치 "02 또는 spec.md", 02 상태 칸 수동 기입, 상태 어휘 3종, red-team CRITICAL만 차단, discover Gate 기록 위치, 고아 문서(07, 10), 권한 데이터 범위 칸 없음, RULE·Q·A ID 미추적, AC→TC 매핑 중복, MASTER_PROMPT 복제 어긋남, 대체 규칙이 Claude 어댑터에만 있음, `@MASTER_PROMPT.md` 매 세션 로드, `ASSUMPTIONS.md` 없음, specs→docs 반영 규칙 없음. 전부 미해결.
- LOW L1~L4(`discovery.md` 사실 오류, `/init` 예약 불일치)와 Kiro 서술 혼동은 수정함. L5~L10은 미해결.

## 라이선스 (감사 결과)

- 외부 코드 복사 흔적 없음, attribution 누락 없음.
- `NEEDS LICENSE VERIFICATION`: 9개 외부 프로젝트의 라이선스 분류(근거는 설계 대화록의 ChatGPT 답변뿐이며 원 출처가 보존되지 않음), `MASTER_PROMPT.md`·`BOOTSTRAP.md`·대화록의 생성 경위와 권리 귀속, 단계 이름이 Spec Kit과 같은 점.

## 감사자가 본 시나리오 결과

- Greenfield(지출결의 웹앱), Brownfield(ERP 검증) 모두 "프레임워크를 대상 프로젝트에 적용하는 방법"이 없어 0단계에서 막힘 (H4).
- 이후에는 형식이 없어 Gate를 계산할 수 없는 지점이 단계마다 반복됨 (H1~H3).
