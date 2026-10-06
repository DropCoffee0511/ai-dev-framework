# Audit 002 — Independent audit by Codex CLI (cross-model)

- 일자: 2026-10-06
- 대상: 커밋 `bfbe160` (규칙 단순화 반영 후)
- 감사자: Codex CLI 0.160.0, 모델 `gpt-6.1-sol`, 읽기 전용 샌드박스(`-s read-only`). 이 저장소를 작성한 Claude 계열과 **다른 모델 계열**이다
- 판정: **`B_FINAL = FAIL`** (CRITICAL 0, HIGH 4, MEDIUM 12, LOW 3)
- 프롬프트: 10월 2일 감사의 프롬프트 원본이 보존되어 있지 않아 같은 취지로 새로 작성했다(항목 9개). 따라서 audit-001과 **같은 기준의 비교는 아니다**
- 한계: 정적 감사 1회이며 자동 실행 테스트는 없다. audit-001 대조표의 M1~M15 번호는 감사자가 `audit-001.md`의 나열 순서로 **임시 대응**한 것이라 정확하지 않고, L1~L10은 개별 내용이 없어 대조되지 않았다
- 아래 본문은 감사자의 최종 보고 **원문**이다. 로컬 절대 경로가 담긴 링크 대상만 제거했다(표시 텍스트 `파일:줄`은 그대로)
- 이 감사의 지적에 대한 처리는 `NEXT.md`에서 추적한다

---

감사 대상은 **`bfbe160ed56d9ac188e45a861eabd848ace31a58`**이며, 시작·종료 시 작업 트리에 변경이 없었습니다. 파일은 수정하지 않았습니다. 지정된 문서를 먼저 읽고 독립 판단을 정리한 뒤 `audit-001.md`를 대조했습니다. 문서의 “PASS”, “수정함”, “검증됨”은 해소 근거로 사용하지 않았습니다.

**결론: 문서 골격은 갖췄지만, 추적성의 완전성과 완료 판정·재판정에 HIGH 결함이 남아 있습니다.** 아래 우회 사례는 문서 규칙에 따른 정적 시뮬레이션이며, 실제 에이전트의 우회 실행은 미확인입니다.

**1~9 항목별 판정**

| 항목 | 판정 | 직접 확인한 근거 |
|---|---|---|
| 1. MASTER_PROMPT 준수 | PARTIAL | §23~§24에 대응하는 조사·템플릿·11단계·어댑터 골격은 존재한다. 그러나 계산된 DONE은 §6의 테스트 종류·문서 일치·변경 기록을 모두 검사하지 않는다. `MASTER_PROMPT.md:543`, `MASTER_PROMPT.md:551`, `docs/traceability-convention.md:62`, `docs/traceability-convention.md:77`. 사용자 승인과 독립 리뷰 필수화는 하위 문서의 추가 규약으로 명시되어 있어, 숨겨진 덮어쓰기로 단정하지 않는다. `workflows/README.md:36`, `workflows/README.md:61`. |
| 2. Gate 정합성·우회 가능성 | FAIL | 순서·별도 기록·append-only·판정자·STALE 규칙은 존재한다. 다만 재판정 기준점, 다중 REQ 최신값 선택, 구현 완료 전이 조건이 불완전하다. 사용자 승인 3곳은 문서 절차로만 강제된다. `docs/traceability-convention.md:98`, `docs/traceability-convention.md:102`, `docs/traceability-convention.md:128`, `docs/traceability-convention.md:132`, `workflows/README.md:22`. |
| 3. Traceability 완결성 | FAIL | ID·링크·차원별 계산은 정의되어 있다. 그러나 등록된 요구사항/AC 전체와 연결 집합의 일치 검사가 없고, TASK 완료 형식도 없다. 계산된 DONE과 DoD는 일치하지 않는다. `docs/traceability-convention.md:24`, `docs/traceability-convention.md:52`, `docs/traceability-convention.md:62`, `docs/traceability-convention.md:69`, `docs/traceability-convention.md:93`. |
| 4. Greenfield/Brownfield 적용성 | FAIL | 사용법은 “이 저장소 루트”에서 실행하는 방법뿐이다. 대상 저장소에 배치·병합·초기화하는 절차가 없다. Brownfield 조사 요구는 있으나 인벤토리·기준선 범위 형식이 없다. `README.md:30`, `workflows/discover/README.md:10`, `workflows/discover/README.md:13`, `NEXT.md:17`. |
| 5. 과잉 설계·복잡도 | PARTIAL | 규칙 참조와 Gate 기록 통합은 중복을 줄였다. 그러나 문서 변경에도 동일 승인 체계를 적용하고, 네 리뷰 단계 모두 다른 컨텍스트를 요구한다. 작은 변경에 대한 비용이 크다는 판단은 추론이며, 실제 사용자 사용성은 미확인이다. `workflows/README.md:3`, `workflows/README.md:46`, `workflows/README.md:61`. |
| 6. 라이선스·출처 | PARTIAL | 현재 추적 파일에는 애플리케이션 코드·의존성 manifest가 없고, Task Master 포함이나 BMAD 제품 브랜딩 흔적은 확인되지 않았다. 미검증 항목은 표시되어 있다. 다만 외부 원본과의 비교, 실제 라이선스 분류 및 원천 문서의 권리 귀속은 미확인이다. `MASTER_PROMPT.md:1062`, `MASTER_PROMPT.md:1089`, `THIRD_PARTY_NOTICES.md:34`, `THIRD_PARTY_NOTICES.md:41`, `THIRD_PARTY_NOTICES.md:42`. |
| 7. 공개 저장소 위험 | PARTIAL | 현재 추적 파일에서 비밀값·민감한 개인정보는 확인되지 않았다. 원천 대화록에는 해석 불가능한 내부 인용 표식 16개와 예시 로컬 경로가 있다. `261002 대화내용.txt:18`, `261002 대화내용.txt:560`, `261002 대화내용.txt:790`. 과거 모든 커밋의 비밀정보 부재는 미확인이다. |
| 8. 에이전트 어댑터 | PARTIAL | 공통 규칙을 대체하는 핵심 도구 로직은 확인되지 않았다. 다만 교차 도구 리뷰 전달 자료에서 중앙 `docs/` 등록부가 빠지고, 진입 파일에 저장소 사실이 중복된다. `adapters/README.md:16`, `adapters/README.md:29`, `adapters/codex/README.md:18`, `CLAUDE.md:24`, `AGENTS.md:21`. |
| 9. 기존 감사 대조 | PARTIAL | 기록 분리·승인 기록·테스트 증거·verify 범위 등은 개선됐다. 주요 계산·적용 결함은 남았다. 이전 감사는 요약본이며 LOW 개별 내용이 없어 ID별 완전 대조는 불가능하다. `docs/audits/audit-001.md:8`, `docs/audits/audit-001.md:34`, `docs/audits/audit-001.md:35`. |

**지적 목록**

**CRITICAL**

이번 감사에서 CRITICAL로 확정한 지적은 없습니다.

**HIGH**

| ID | 근거 | 이유 | 한 줄 수정 제안 |
|---|---|---|---|
| H-01 | docs/traceability-convention.md:52, 같은 파일 `:62`, `:68`, `:93`, `:138`; `docs/02_requirements.md:29` | **완료조건과 요구사항을 연결 목록에서 제외하는 누락을 탐지하지 못한다.** 등록부에 AC-001 저장, AC-002 무권한 거부, AC-003 중복 방지가 있어도 YAML에 AC-001만 넣으면 Requirement·Tests가 PASS가 될 수 있다. PERM/ERR 전체 집합의 일치 규칙과 “범위 안 모든 REQ”의 기준 집합도 없다. | 변경 범위의 REQ 집합을 선언하고, 각 REQ의 활성 AC·PERM·ERR 전체와 추적 링크의 일치를 검사한다. |
| H-02 | docs/traceability-convention.md:77, 같은 파일 `:87`, `:93`; `MASTER_PROMPT.md:551`, `:555`, `:556`, `:557`; `workflows/README.md:25`, `:26` | **계산된 DONE이 DoD보다 약하다.** 정상·예외·권한·회귀 테스트의 필요한 종류, 문서 현행화, 변경 기록을 모두 계산하지 않는다. 구현 리뷰 이후 red-team에서 새 HIGH가 발견돼도 red-team과 최종 이슈 Gate는 CRITICAL만 명시적으로 차단한다. 릴리스 체크리스트를 최종 Gate의 필수 입력으로 연결한 규칙도 없다. | 최종 DONE을 §6 전체 조건과 후속 리뷰·converge·사용자 수용에 연결하고, 미해결 CRITICAL/HIGH를 함께 차단한다. |
| H-03 | docs/traceability-convention.md:102, 같은 파일 `:127`, `:128` | **재판정의 기준점과 변경 범위가 불완전하다.** “커밋 전” 기록은 허용하지만 비교 방법은 커밋 해시를 요구한다. `git log`만으로는 미커밋 변경을 검출하지 못한다. 추적 링크·증거·공유 인증 모듈·설정 등의 변경을 어떤 Gate에 연결할지도 명확하지 않다. 현재 작업 트리가 깨끗하다는 사실은 이 규약 결함을 해소하지 않는다. | Gate별 검토 파일 목록과 검토 시점의 스냅샷을 기록하고, 커밋 변경과 작업 트리 변경 모두를 재판정 대상으로 삼는다. |
| H-04 | README.md:30, `docs/01_product.md:3`, `docs/discovery.md:60`, `docs/gates.md:3`, `NEXT.md:17` | **대상 프로젝트 설치·적용 방법이 없다.** 프레임워크 자체 기록과 대상 프로젝트 템플릿이 섞여 있다. 새 앱 저장소나 기존 ERP에 무엇을 가져오고, 기존 AGENTS/CLAUDE/docs/LICENSE를 어떻게 보존·병합할지 정해져 있지 않다. | Greenfield 시작 절차와 Brownfield 비파괴 적용 절차를 분리하고 파일 배치·충돌·초기화 정책을 명시한다. |

**MEDIUM**

| ID | 근거 | 이유 | 한 줄 수정 제안 |
|---|---|---|---|
| M-01 | specs/README.md:5, `docs/02_requirements.md:35`, `docs/traceability-convention.md:69`, `:101` | **blocker·TASK·리뷰 발견 사항의 계산 형식이 없다.** 질문에는 OPEN/RESOLVED만 있고 blocker 여부가 없다. TASK 상태·완료 조건과 리뷰 발견 사항의 해결 상태·증거 형식도 없다. `tasks: `을 완료로 볼지 역시 명확하지 않다. | 최소 필드·상태값·빈 목록 처리와 Gate별 판정 조건을 정의한다. |
| M-02 | workflows/specify/README.md:10, `workflows/design/README.md:10`, `workflows/plan/README.md:10`, `docs/traceability-convention.md:17`, `:24`, `:51` | **산출물의 “또는” 경로와 중앙 등록부 의무가 어긋난다.** change 문서만 작성하면 지정된 `docs/` 정의 위치에 ID가 없어 dangling reference가 된다. TC를 `test-plan.md`에 작성한 뒤 중앙 등록하는 단계도 빠져 있다. | 중앙 ID 등록과 변경 상세 문서 작성을 함께 요구한다. |
| M-03 | docs/traceability-convention.md:98, 같은 파일 `:70`, `:103` | **다중 REQ의 최신 Gate 선택이 모호하다.** REQ별 적용 목록은 요구하지만 현재값은 “같은 Gate의 가장 아래 줄”이다. REQ-001 승인 뒤 REQ-002 승인을 추가했을 때 REQ-001에 적용할 행 선택 규칙이 없다. | 적용 REQ를 구조화하고 `(Gate, REQ)`별 최신 적용 기록을 선택한다. |
| M-04 | workflows/README.md:22, 같은 파일 `:23`; `workflows/implement/README.md:11` | **`IMPLEMENTATION_COMPLETE`가 다음 단계 진입 조건에 사용되지 않는다.** verify가 기록한다고 하지만 review 진입은 테스트 Gate만 요구한다. | verify 종료 시 두 Gate 모두 통과해야 구현 리뷰에 진입하도록 한다. |
| M-05 | workflows/converge/README.md:10, `docs/traceability-convention.md:127` | **재작업 루프가 완결되지 않았다.** 해당 단계에서 고친다는 지시는 있으나 불일치 유형별 복귀 단계와 재실행 순서가 없다. | 불일치 유형별 복귀 단계 및 verify→review→red-team→converge 재진입 규칙을 명시한다. |
| M-06 | docs/traceability-convention.md:49, 같은 파일 `:63`, `:66`, `:67` | **N/A는 이유 문자열만으로 PASS가 된다.** 권한·예외를 부적절하게 N/A로 지정해도 계산 자체는 이를 차단하지 않는다. 적합성 승인 주체도 없다. | N/A를 spec 승인 범위에 포함하고 독립 리뷰에서 적합성을 확인한다. |
| M-07 | docs/traceability-convention.md:105, 같은 파일 `:113`, `:114`, `:122`, `:132` | **승인·독립성은 실제 권한 경계가 아니다.** 판정자·인용·대리 기록은 텍스트이며, 구현자의 파일 수정 금지는 사후 검사에 의존한다. 이는 v0.1의 명시된 한계지만 “강제” 목표는 충족하지 못한다. | 수동 규약임을 명확히 표시하고 승인 출처·리뷰어 신원·기록 변경을 검증하는 경계를 마련한다. |
| M-08 | adapters/README.md:29, `adapters/codex/README.md:18`, `docs/traceability-convention.md:9` | **독립 리뷰 전달 자료가 불완전하다.** 코드와 change 폴더만 넘기면 중앙 요구사항·권한·오류·TC 정의가 빠진다. | 리뷰 전달 목록에 관련 `docs/` 등록부, 공통 규약, gates와 테스트 증거를 포함한다. |
| M-09 | docs/06_permissions.md:14, 같은 파일 `:20`, `:26`; `docs/05_data_model.md:7` | **권한의 데이터 범위 정책을 표현하는 칸이 없다.** 역할×권한과 검사 위치는 있지만 소유자·회사·조직 등의 접근 범위와 조건을 구조적으로 연결하지 못한다. 타인 데이터 테스트만으로 정책 정의를 대체할 수 없다. | PERM에 자원 범위·접근 조건·소유권 규칙과 검증 TC를 연결한다. |
| M-10 | docs/gates.md:7, `docs/traceability-convention.md:98`, `:104`, `:122` | **구 형식 기록을 그대로 인정하는 예외가 지나치게 넓다.** 저장된 리뷰 파일이 없는 과거 기록도 형식 예외에 들어간다. 최신 false가 현재 덮고 있어 현재의 false→true 우회는 확인되지 않았지만, 형식 호환과 근거 유효성 검사가 분리되지 않았다. | 구 형식은 읽되 승인 출처·독립성·증거·재판정 요건은 계속 검증한다. |
| M-11 | workflows/README.md:36, 같은 파일 `:46`, `:61`; `constitution/principles.md:4` | **작은 변경의 비용과 규칙 출처가 부담스럽다.** 문서 변경에도 동일 승인을 요구한다. MASTER가 단일 출처라는 설명과 하위 문서의 추가 필수 규약도 함께 존재한다. 엄격한 추가 규약 자체를 위반으로 단정하지는 않는다. | 규칙의 권위·추가 규약을 구분하고 저위험 변경의 최소 경로를 정의한다. |
| M-12 | THIRD_PARTY_NOTICES.md:42, `LICENSE:5`, `REFERENCES.md:25` | **원천 문서의 MIT 공개 권한은 미확인이다.** 미검증 표시와 별개로 저장소의 LICENSE는 associated documentation에도 이용 권한을 부여한다. 실제 권리 침해 여부는 미확인이다. | 원천 문서의 공개·재배포 권한을 확인하고 확인되지 않은 항목의 라이선스 적용 범위를 명시한다. |

**LOW**

| ID | 근거 | 이유 | 한 줄 수정 제안 |
|---|---|---|---|
| L-01 | docs/02_requirements.md:10, `docs/traceability-convention.md:21`, `:77`, `docs/01_product.md:26`, `docs/02_requirements.md:37` | DRAFT·RETIRED·계산 상태의 관계와 RULE/Q/A ID의 수명·추적 규칙이 명확하지 않다. | 문서 작성 상태·폐기 상태·계산 결과를 구분하고 보조 ID 규칙을 정의한다. |
| L-02 | REFERENCES.md:24, `MASTER_PROMPT.md:978` | “원 저장소 URL이 보존되지 않았다”는 표현은 부정확하다. MASTER에는 URL이 있다. 없는 것은 검증 시점의 LICENSE 원문·버전 근거다. | URL 부재와 라이선스 검증 증거 부재를 구분한다. |
| L-03 | 261002 대화내용.txt:18, 같은 파일 `:560`, `:790`; `NEXT.md:15` | 내부 인용 표식은 16개로, NEXT의 15개와 다르다. 예시 로컬 경로도 공개되어 있다. 해당 경로가 실제 개인 환경을 식별한다는 근거는 없다. | 승인된 별도 정리본에서 해석 가능한 출처로 교체하고 표식 개수를 정정한다. |

**두 적용 시나리오**

| 단계 | Greenfield — 지출결의 웹앱 | Brownfield — 기존 ERP |
|---|---|---|
| 0단계: 적용 | 별도 앱 저장소에 무엇을 설치할지 몰라 처음 막힌다. 프레임워크 저장소 자체를 앱 저장소로 쓰는 것은 추가 가정이다. `README.md:30`, `docs/01_product.md:3`. | 기존 AGENTS/CLAUDE/docs/LICENSE를 보존하며 적용하는 정책이 없다. `README.md:30`, `NEXT.md:17`. |
| DISCOVER | 위 가정을 두면 GREENFIELD 조사 기록은 작성할 수 있다. 제품 템플릿과 프레임워크 자체 기록은 분리해야 한다. `docs/discovery.md:60`. | 기능·API·DB·권한·테스트를 추출하라는 요구는 있다. 다만 ERP 전체와 이번 변경 중 어느 범위를 기준선으로 삼을지, 어떤 표로 완료를 확인할지 없다. `MASTER_PROMPT.md:94`, `workflows/discover/README.md:13`. |
| SPECIFY/CLARIFY | 등록·제출·승인·반려·중복 방지 등의 REQ/AC를 작성할 수 있다. 그러나 열린 질문을 blocker로 분류하는 형식이 없어 `SPEC_AMBIGUITY_BLOCKERS = 0` 계산이 일관되지 않다. `docs/02_requirements.md:35`, `docs/traceability-convention.md:101`. | 현재 구현과 승인된 업무 의도를 구분하고 기존 ID를 이관하는 형식이 없다. 문서와 코드의 불일치는 `INTENT_UNKNOWN`으로 남길 수 있지만 기준선 승인 절차는 구체화되지 않았다. `MASTER_PROMPT.md:102`, `docs/traceability-convention.md:143`. |
| DESIGN/PLAN/REVIEW | change 문서만 작성하는 경로와 중앙 등록부 의무가 어긋난다. TASK 완료·리뷰 해결 상태 형식도 없어 판정이 주관적이다. `workflows/design/README.md:10`, `docs/traceability-convention.md:69`. | 동일한 문제에 더해 여러 REQ의 Gate 선택과 공유 인증·권한 모듈 변경의 재판정 범위가 불명확하다. `docs/traceability-convention.md:98`, `:103`, `:127`. |
| VERIFY/완료 | 저장 테스트만 연결하고 다른 AC를 누락해도 계산상 PASS가 가능하다. 후속 red-team HIGH와 DoD 전체를 최종 DONE에 연결하는 규칙이 부족하다. `docs/traceability-convention.md:62`, `:68`, `MASTER_PROMPT.md:555`. | 직접 수정 파일 밖의 공유 의존성 변경과 미커밋 변경을 기존 증거·Gate에 연결하는 규칙이 부족하다. `docs/traceability-convention.md:128`. |

**audit-001 대조표**

C/H의 개별 설명은 보존되어 있습니다. M1~M15는 `audit-001.md:34`의 나열 순서로 **임시 대응**했으며, 원 보고서의 실제 ID 대응은 미확인입니다. L1~L10은 개별 설명이 없어 판정을 만들어 넣지 않았습니다.

| ID | 판정 | 현재 커밋에서 확인한 근거 |
|---|---|---|
| C1 | 부분 해소 | 리뷰 Gate를 별도 파일로 분리하고 구현자 수정을 금지했다. 실제 위조·수정 방지는 없다. `docs/traceability-convention.md:45`, `:97`, `:105`, `:132`. |
| C2 | 부분 해소 | 승인 기록 3종과 USER-only 규칙은 생겼다. 실제 승인 출처를 강제하는 장치는 없다. `workflows/README.md:40`, `docs/traceability-convention.md:113`, `:118`, `:132`. |
| C3 | 해소 | 규약 수준에서 실행 증거·TC 코드 연결·증거 없는 PASS 처리와 verify 쓰기 범위가 정의됐다. 실제 실행 효과는 미확인이다. `docs/09_test_cases.md:11`, `:15`, `docs/traceability-convention.md:84`, `workflows/README.md:55`. |
| H1 | 미해결 | 단계 목적·산출물은 있으나 통과 조건을 재현 가능하게 판정할 필드·조건이 부족하다. `workflows/specify/README.md:11`, `workflows/plan/README.md:11`, `specs/README.md:5`. |
| H2 | 부분 해소 | 숫자 Gate를 true로 기록하는 표현은 정의됐다. blocker 분류·집계 필드는 없다. `docs/traceability-convention.md:101`, `docs/02_requirements.md:35`. |
| H3 | 미해결 | tasks/review 파일 위치만 있고 상태·해결 증거 형식이 없다. `specs/README.md:11`, `:16`, `docs/traceability-convention.md:69`. |
| H4 | 미해결 | 대상 프로젝트 적용 절차와 템플릿/자체 기록 분리가 없다. `README.md:30`, `docs/discovery.md:60`, `NEXT.md:17`. |
| H5 | 부분 해소 | converge는 추적 파일을 읽기만 하도록 정리됐다. 복귀·재검증 루프는 부족하다. `workflows/converge/README.md:10`, `docs/traceability-convention.md:127`. |
| H6 | 해소 | verify 행과 수정 금지 범위가 있다. `workflows/README.md:55`. |
| H7 | 부분 해소 | 변경 후 재판정·STALE 규칙은 생겼다. 커밋 전·미커밋 변경·공유 의존성 범위는 불완전하다. `docs/traceability-convention.md:102`, `:127`, `:128`. |
| H8 | 미해결 | 계산 DONE과 DoD의 차이, N/A 적합성 승인 부재가 남았다. `docs/traceability-convention.md:49`, `:62`, `:77`, `MASTER_PROMPT.md:551`. |
| H9 | 해소 | 부트스트랩 완료를 가정하지 않고 Gate 기록을 읽도록 한다. 과거 true도 후속 false 기록으로 대체됐다. `AGENTS.md:15`, `CLAUDE.md:18`, `docs/gates.md:22`, `:23`. |
| M1* | 부분 해소 | 공통 workflow에는 독립 컨텍스트 필수 규약이 있다. MASTER의 “가능하면”과 출처 설명은 그대로다. `workflows/README.md:61`, `MASTER_PROMPT.md:887`. |
| M2* | 부분 해소 | REQ/AC 중앙 등록 의무는 명확해졌다. 단계 산출물의 “또는” 표현은 남았다. `docs/traceability-convention.md:24`, `workflows/specify/README.md:10`. |
| M3* | 미해결 | 요구사항 표의 수동 DRAFT 칸과 계산 상태 관계가 정의되지 않았다. `docs/02_requirements.md:10`, `docs/traceability-convention.md:81`. |
| M4* | 부분 해소 | workflow의 별도 단계 상태명은 제거됐지만 DRAFT·RETIRED·계산 상태 관계는 남았다. `workflows/README.md:12`, `docs/02_requirements.md:10`, `docs/traceability-convention.md:21`. |
| M5* | 미해결 | red-team과 최종 이슈 Gate는 CRITICAL만 명시적으로 차단한다. `workflows/red-team/README.md:11`, `workflows/README.md:26`. |
| M6* | 해소 | 프로젝트·변경 단위 Gate 위치가 정의됐다. `workflows/README.md:32`, `docs/traceability-convention.md:98`. |
| M7* | 부분 해소 | 07은 design의 03~08 범위에 포함된다. 10 릴리스 체크리스트는 최종 Gate 필수 입력에 연결되지 않았다. `workflows/design/README.md:10`, `workflows/converge/README.md:9`, `docs/10_release_checklist.md:10`. |
| M8* | 미해결 | 역할×권한·검사 위치는 있지만 자원 접근 범위 정책 칸은 없다. `docs/06_permissions.md:14`, `:20`. |
| M9* | 미해결 | RULE/Q/A는 사용하지만 핵심 ID 규약에 포함되지 않는다. `docs/01_product.md:26`, `docs/02_requirements.md:37`, `docs/traceability-convention.md:20`. |
| M10* | 미해결 | AC→TC가 요구사항 표와 trace YAML에 중복되며 상호 일치 검사가 없다. `docs/02_requirements.md:29`, `docs/traceability-convention.md:37`. |
| M11* | 부분 해소 | 참조 중심으로 중복을 줄였지만 추가 필수 규약과 단일 출처 설명의 차이가 남았다. `constitution/principles.md:4`, `workflows/README.md:36`, `:61`. |
| M12* | 해소 | 독립 리뷰가 불가능할 때 UNKNOWN 및 USER 직접 리뷰 경로가 공통 규약에 있다. `docs/traceability-convention.md:123`. |
| M13* | 부분 해소 | 어댑터는 일상 작업과 BOOTSTRAP을 구분한다. MASTER의 첫 실행 지시 자체는 매 세션 import되는 본문에 남아 있다. 실제 반복 실행 여부는 미확인이다. `CLAUDE.md:7`, `:18`, `MASTER_PROMPT.md:1410`. |
| M14* | 해소 — 원 지적 재평가 | 별도 `ASSUMPTIONS.md`는 필수가 아니다. MASTER는 spec 기록을 허용하고 제품 템플릿에도 가정 표가 있다. `MASTER_PROMPT.md:244`, `docs/01_product.md:34`. |
| M15* | 미해결 | 등록 ID 사용은 정의됐지만 change 상세를 중앙 문서에 반영하는 시점·필드·충돌 처리 규칙은 없다. `docs/traceability-convention.md:24`, `specs/README.md:20`. |
| L1 | 미확인 | 개별 지적 내용이 미보존되어 대응 불가. `docs/audits/audit-001.md:35`. |
| L2 | 미확인 | 동일. `docs/audits/audit-001.md:35`. |
| L3 | 미확인 | 동일. `docs/audits/audit-001.md:35`. |
| L4 | 미확인 | 동일. `docs/audits/audit-001.md:35`. |
| L5 | 미확인 | 개별 내용 없이 “미해결” 묶음만 남아 있다. `docs/audits/audit-001.md:35`. |
| L6 | 미확인 | 동일. `docs/audits/audit-001.md:35`. |
| L7 | 미확인 | 동일. `docs/audits/audit-001.md:35`. |
| L8 | 미확인 | 동일. `docs/audits/audit-001.md:35`. |
| L9 | 미확인 | 동일. `docs/audits/audit-001.md:35`. |
| L10 | 미확인 | 동일. `docs/audits/audit-001.md:35`. |

이전 요약에 명시되지 않은 새 문제는 **등록 AC/REQ의 부분집합 누락(H-01), 커밋 전·미커밋 상태의 재판정 공백(H-03), 다중 REQ 최신 Gate 선택(M-03), 리뷰 전달 자료의 중앙 등록부 누락(M-08), 구 형식 기록의 포괄 인정(M-10)**입니다.

한계: 같은 저장소를 읽은 **한 번의 독립 정적 감사**입니다. 문서 열람·Git 대조·정적 검색·두 시나리오 시뮬레이션을 수행했으며 **자동 실행 테스트는 없습니다**. 외부 라이선스 원문 비교, 저장소 밖의 승인 통제, 실제 도구별 실행 효과 및 과거 전체 이력의 비밀정보 부재는 미확인입니다.

B_FINAL = FAIL