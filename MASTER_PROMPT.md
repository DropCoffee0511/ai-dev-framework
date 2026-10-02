# MASTER_PROMPT.md
# AI Development Framework — Master Operating Prompt
# Version: 0.1-draft

> 이 파일은 Claude Code, Codex CLI 및 기타 AI 코딩 에이전트가 이 저장소에서 작업할 때 따라야 하는 최상위 운영 규칙이다.
> 이 파일의 목적은 AI에게 “코드를 많이 작성하라”고 요구하는 것이 아니라,
> **요구사항·업무흐름·데이터·권한·예외·테스트·완료조건을 먼저 명확히 하고,
> 그 명세에 맞는 최소 변경만 구현한 뒤 독립적으로 검증하도록 강제하는 것**이다.

---

## 0. 최우선 지시

이 저장소에서 작업하는 AI 에이전트는 다음 원칙을 항상 지킨다.

1. **문서가 코드보다 먼저다.**
2. **요구사항 없이 큰 기능을 구현하지 않는다.**
3. **기존 기능을 임의로 삭제하거나 변경하지 않는다.**
4. **대규모 변경은 구현 전에 계획과 영향 범위를 작성한다.**
5. **요구사항 → 화면 → 데이터 → 권한 → 예외 → 테스트 → 코드 사이의 추적 가능성(Traceability)을 유지한다.**
6. **“코드가 작성됨”을 “완료”로 간주하지 않는다.**
7. **구현자와 최종 검토자의 관점을 분리한다.**
8. **라이선스가 불명확한 외부 코드를 복사하지 않는다.**
9. **기존 프로젝트(Brownfield)는 먼저 현재 상태를 역분석한다.**
10. **사용자 승인 없이 핵심 업무 규칙·DB 구조·인증·권한·결제·주요 기술 스택을 바꾸지 않는다.**

문서와 코드가 충돌하면 임의로 한쪽을 정답으로 간주하지 않는다.
충돌을 기록하고, 어느 쪽이 현재 의도인지 확인 가능한 근거를 찾는다.

---

# 1. 프로젝트 목적

이 프로젝트는 비개발자 또는 소규모 팀이 AI 코딩 도구를 사용하면서 흔히 겪는 다음 문제를 줄이기 위한
**AI 개발 운영 프레임워크**를 구축한다.

- 처음에는 잘 작동하지만 기능이 늘수록 구조가 무너지는 문제
- AI가 요구사항을 일부 누락하는 문제
- 한 기능을 수정하다 기존 기능을 깨뜨리는 문제
- 화면과 API의 권한이 불일치하는 문제
- 예외 상황과 오류 처리가 뒤늦게 발견되는 문제
- AI가 스스로 “완료”라고 판단하지만 실제 완료조건이 충족되지 않는 문제
- 여러 AI 도구가 서로 다른 방식으로 프로젝트를 이해하는 문제
- 이미 상당 부분 개발된 프로젝트를 어떻게 정리해야 할지 모르는 문제

최종 목표는 다음과 같다.

> **“AI에게 앱을 만들어 달라”가 아니라,
> “명세를 만족하는 프로그램을 구현하고,
> 테스트하고,
> 요구사항과 실제 구현을 대조하고,
> 독립 검토까지 통과하라”고 지시할 수 있는 구조를 만든다.**

---

# 2. 프로젝트가 하지 않을 것

초기 버전에서는 다음을 목표로 하지 않는다.

- 특정 LLM 공급자 하나에 종속되는 프레임워크
- 모든 언어/프레임워크를 직접 빌드하는 범용 IDE
- 자동 배포 플랫폼
- 상용 프로젝트 관리 서비스 복제
- 기존 오픈소스 프로젝트의 브랜드/상표를 이용한 파생 제품
- 라이선스가 제한된 프로젝트 코드를 우회적으로 재배포하는 것
- 사용자 확인 없이 프로덕션 데이터/인프라를 변경하는 것

---

# 3. 운영 모드

작업 시작 시 저장소를 검사하고 다음 둘 중 하나를 선택한다.

## 3.1 GREENFIELD

다음 조건이면 GREENFIELD로 본다.

- 실질적인 애플리케이션 코드가 아직 없음
- 프로젝트 목적이나 명세를 처음 작성하는 단계
- 사용자가 새 프로젝트라고 명시함

GREENFIELD에서는 **문서 → 설계 → 계획 → 구현** 순서를 따른다.

## 3.2 BROWNFIELD

다음 조건이면 BROWNFIELD로 본다.

- 기존 `src`, `app`, `packages`, `server`, `client`, DB migration 등이 존재함
- 이미 작동하는 기능이 있음
- 기존 프로젝트의 완성도를 높이거나 구조를 복구하려는 목적임

BROWNFIELD에서는 먼저 다음을 수행한다.

1. 저장소 구조 조사
2. 실행 방법 조사
3. 현재 기능 목록 추출
4. 주요 사용자 흐름 추출
5. API/DB/권한/상태 모델 추출
6. 테스트 현황 조사
7. 문서와 구현의 불일치 조사
8. 위험 영역 식별
9. `docs/`와 `specs/`의 초안을 **현재 구현에 근거해** 생성
10. 이후 개선 요구사항을 별도 Change Spec으로 작성

Brownfield에서 기존 코드는 “자동으로 옳은 명세”가 아니다.
그러나 문서가 없다고 해서 기존 동작을 임의로 제거해서도 안 된다.

---

# 4. 표준 개발 흐름

기본 흐름은 다음과 같다.

```text
DISCOVER
   ↓
SPECIFY
   ↓
CLARIFY
   ↓
DESIGN
   ↓
PLAN
   ↓
REVIEW-PLAN
   ↓
IMPLEMENT
   ↓
VERIFY
   ↓
REVIEW-IMPLEMENTATION
   ↓
RED-TEAM
   ↓
CONVERGE
   ↓
DONE
```

각 단계는 별도의 Gate를 가진다.

---

# 5. 단계별 규칙

## 5.1 DISCOVER

목적:
현재 프로젝트의 사실을 파악한다.

수행:

- 파일/디렉터리 구조 조사
- README, 기존 agent instruction, package manifest 확인
- 빌드/테스트/실행 명령 확인
- 주요 기능 및 엔트리포인트 확인
- DB schema/migration 확인
- 인증/권한 확인
- 외부 서비스 확인
- 테스트 구조 확인
- 기존 문서 확인

금지:

- 이 단계에서 기능 구현 금지
- 대규모 리팩터링 금지
- dependency 교체 금지

산출물:

- `docs/discovery.md` 또는 동등한 분석 문서
- 위험/불확실성 목록
- Greenfield/Brownfield 판정

Gate:

```text
DISCOVERY_COMPLETE = true
```

---

## 5.2 SPECIFY

목적:
사용자가 원하는 결과를 검증 가능한 요구사항으로 바꾼다.

각 기능은 ID를 가진다.

예:

```text
REQ-001
REQ-002
REQ-003
```

각 요구사항에는 최소한 다음을 포함한다.

- 기능명
- 목적
- 사용자
- 사전조건
- 정상 동작
- 예외 상황
- 권한
- 데이터 영향
- 완료조건(Acceptance Criteria)

완료조건은 “로그인 기능 구현” 같은 추상 문구로 끝내지 않는다.

예:

```text
AC-001 정상 계정으로 로그인할 수 있다.
AC-002 잘못된 비밀번호는 거부된다.
AC-003 비활성 계정은 로그인할 수 없다.
AC-004 인증 없는 사용자는 보호된 API에 접근할 수 없다.
AC-005 새로고침 후 인증 상태 정책이 요구사항대로 유지된다.
```

Gate:

```text
SPEC_READY = true
```

---

## 5.3 CLARIFY

다음을 탐지한다.

- 모순되는 요구사항
- 정의되지 않은 상태
- 불명확한 권한
- 누락된 예외
- 데이터 소유권 불명확
- 삭제/취소 정책 불명확
- 동일 기능의 명칭 불일치
- 사용자 흐름의 끊김
- 성공 기준이 검증 불가능한 항목

합리적인 기본값으로 처리 가능한 사소한 사항은 `ASSUMPTIONS.md` 또는 해당 spec에 명시한다.

핵심 업무 규칙에 영향을 주는 가정을 몰래 확정하지 않는다.

Gate:

```text
SPEC_AMBIGUITY_BLOCKERS = 0
```

---

## 5.4 DESIGN

설계 시 다음을 연결한다.

```text
Requirement
  ↓
Workflow
  ↓
Screen/API
  ↓
Data Model
  ↓
Permission
  ↓
Error Case
  ↓
Test
```

필요한 경우 다음 ID 체계를 사용한다.

```text
REQ-###
WF-###
SCR-###
API-###
DATA-###
PERM-###
ERR-###
TC-###
TASK-###
```

설계는 기술적으로 화려한 구조보다 요구사항 추적 가능성과 유지보수성을 우선한다.

대규모 기술 스택 변경은 사용자 승인 없이 수행하지 않는다.

Gate:

```text
DESIGN_READY = true
```

---

## 5.5 PLAN

구현 계획에는 최소한 다음을 포함한다.

1. 변경 이유
2. 변경할 파일
3. 새로 만들 파일
4. 변경할 데이터
5. 변경될 API
6. 영향을 받는 기존 기능
7. migration 필요 여부
8. 보안/권한 영향
9. 예상 위험
10. 테스트 방법
11. 롤백 또는 복구 방법
12. 문서 업데이트 항목

아직 구현하지 않는다.

Gate:

```text
PLAN_READY = true
```

---

## 5.6 REVIEW-PLAN

가능하면 계획을 작성한 에이전트와 다른 에이전트/서브에이전트가 검토한다.

검토 항목:

- 요구사항 누락
- 과도한 범위 확대
- 잘못된 가정
- DB migration 위험
- 권한 우회 가능성
- 데이터 손실 가능성
- 회귀 위험
- 테스트 부족
- 불필요한 dependency 추가
- 라이선스 위험

심각도:

```text
CRITICAL
HIGH
MEDIUM
LOW
```

CRITICAL 또는 HIGH가 해결되지 않은 계획은 구현 Gate를 통과하지 못한다.

Gate:

```text
PLAN_REVIEW_PASS = true
```

---

## 5.7 IMPLEMENT

구현 규칙:

- 승인된 계획 범위 안에서만 수정
- 필요한 최소 범위 수정
- 기존 public behavior를 불필요하게 변경하지 않음
- 데이터 검증은 UI뿐 아니라 서버/API 경계에서도 수행
- 권한 검사는 UI 숨김만으로 구현하지 않음
- 오류를 조용히 무시하지 않음
- 중요 상태 변경은 기록 가능하도록 설계
- 코드 변경과 함께 필요한 테스트 추가
- 요구사항 변경이 발견되면 spec을 먼저 업데이트

구현 도중 새로운 큰 문제가 발견되면 임의로 작업 범위를 확대하지 않는다.
`BLOCKER` 또는 `FOLLOW-UP`으로 기록한다.

Gate:

```text
IMPLEMENTATION_COMPLETE = true
```

---

## 5.8 VERIFY

최소 검증 범위:

### 정상 케이스

- 정상 입력
- 저장
- 조회
- 수정
- 삭제/취소 정책
- 상태 전이

### 잘못된 경우

- 필수값 누락
- 잘못된 형식
- 권한 없는 사용자
- 존재하지 않는 데이터
- 중복 요청
- 네트워크/서버 오류
- 세션 만료

### 경계값

- 0
- 최소값
- 최대값
- 빈 목록
- 매우 긴 문자열
- 큰 숫자/금액
- 많은 데이터

### 회귀

- 로그인/로그아웃
- 주요 화면
- 핵심 API
- 데이터 저장/조회/수정
- 권한
- 주요 업무 흐름

검증 결과는 성공/실패를 숨기지 않는다.

Gate:

```text
REQUIRED_TESTS_PASS = true
```

---

## 5.9 REVIEW-IMPLEMENTATION

가능하면 구현자와 다른 컨텍스트를 가진 reviewer가 수행한다.

검토:

- spec과 실제 구현 불일치
- 누락 기능
- 잠재 버그
- 권한 문제
- 보안 경계 문제
- 데이터 손실
- race condition / 중복 처리
- 예외 처리 부족
- UI/UX 일관성
- 기존 기능 파손
- 유지보수성
- 테스트가 실제 요구사항을 검증하는지 여부

Reviewer는 단순히 코드를 예쁘게 만드는 역할이 아니다.
**요구사항과 구현 사이의 불일치를 찾는 역할**이다.

Gate:

```text
IMPLEMENTATION_REVIEW_PASS = true
```

---

## 5.10 RED-TEAM

Red Team은 “작성자가 기대한 방식”이 아니라
“사용자/공격자/예상 밖의 환경이 사용하는 방식”으로 기능을 검토한다.

예:

- URL 직접 접근
- API 직접 호출
- 숨겨진 버튼 기능 호출
- 중복 클릭/중복 제출
- 동시 수정
- 오래된 화면 상태에서 저장
- 승인 후 수정 시도
- 삭제된 데이터 참조
- 잘못된 파일 업로드
- 예상보다 큰 입력
- 재시도에 따른 중복 생성

모든 기능에 고도의 보안 공격 시뮬레이션이 필요한 것은 아니다.
위험도에 맞춰 수행한다.

Gate:

```text
NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS = true
```

---

## 5.11 CONVERGE

마지막으로 문서와 코드를 다시 맞춘다.

검사:

- 요구사항 ↔ 구현
- 요구사항 ↔ 테스트
- 화면 ↔ API
- API ↔ 권한
- 데이터 ↔ migration
- 오류 정의 ↔ 오류 처리
- 완료조건 ↔ 테스트 결과
- 문서 ↔ 현재 코드

불일치를 발견하면 다음 중 하나로 분류한다.

```text
CODE_BUG
SPEC_OUTDATED
DOC_OUTDATED
TEST_MISSING
INTENT_UNKNOWN
```

모든 항목을 조용히 자동 수정하지 않는다.
의도가 불명확한 경우 `INTENT_UNKNOWN`으로 남긴다.

Gate:

```text
TRACEABILITY_COMPLETE = true
NO_CRITICAL_OPEN_ISSUES = true
```

---

# 6. 완료 정의(Definition of Done)

기능은 다음 조건을 모두 만족해야 완료다.

- [ ] 요구사항이 문서화되어 있다.
- [ ] 완료조건이 검증 가능하다.
- [ ] 관련 workflow가 정의되어 있다.
- [ ] 필요한 화면/API가 정의되어 있다.
- [ ] 필요한 데이터 구조가 정의되어 있다.
- [ ] 권한이 정의되어 있다.
- [ ] 주요 예외가 정의되어 있다.
- [ ] 구현이 요구사항과 연결되어 있다.
- [ ] 정상 테스트가 통과한다.
- [ ] 예외 테스트가 통과한다.
- [ ] 권한 테스트가 통과한다.
- [ ] 필요한 회귀 테스트가 통과한다.
- [ ] 독립 리뷰에서 Critical/High blocker가 없다.
- [ ] 관련 문서가 현재 구현과 일치한다.
- [ ] 변경 내용이 기록되어 있다.

“코드가 컴파일된다” 또는 “화면이 보인다”는 완료 기준이 아니다.

---

# 7. Traceability Matrix

프레임워크의 핵심 기능이다.

예:

```text
REQ-023 지출결의 등록

REQ-023
 ├─ WF-004
 ├─ SCR-014
 ├─ API-021
 ├─ DATA-008
 ├─ PERM-011
 ├─ ERR-019
 ├─ TC-104
 ├─ TC-105
 ├─ TC-106
 ├─ TASK-078
 └─ TASK-079
```

기능 상태 예:

```text
REQ-023

Requirement     PASS
Workflow        PASS
Screen/API      PASS
Data            PASS
Permission      PASS
Error Cases     PASS
Tests           PASS
Implementation  PASS
Review          PASS

STATUS: DONE
```

누락 예:

```text
REQ-031

Requirement     PASS
Workflow        PASS
Screen/API      PASS
Data            PASS
Permission      MISSING
Error Cases     PASS
Tests           MISSING
Implementation  PARTIAL

STATUS: NOT READY
```

누락 항목이 있으면 AI는 해당 기능을 “완료”라고 보고해서는 안 된다.

---

# 8. 상태 관리 원칙

업무 상태가 있는 기능은 명시적으로 상태 전이를 정의한다.

예:

```text
DRAFT
  ↓
SUBMITTED
  ↓
REVIEWING
  ├─→ APPROVED
  └─→ REJECTED
         ↓
       DRAFT
```

각 상태마다 정의:

- 의미
- 진입 조건
- 가능한 이전 상태
- 가능한 다음 상태
- 가능한 사용자 행동
- 상태 변경 권한
- 변경 이력 저장 여부

상태 전이를 UI 코드 여러 곳에 흩어놓지 않는다.

---

# 9. 권한 원칙

권한은 다음 두 층 이상에서 고려한다.

```text
UI
+
Server/API
```

버튼을 숨겼다고 권한 제어가 완료된 것이 아니다.

예:

> 승인 버튼이 화면에 보이지 않는 사용자가 API를 직접 호출해도 승인할 수 없어야 한다.

권한 변경 시 테스트해야 할 것:

- 정상 역할
- 권한 없는 역할
- 다른 사용자의 데이터
- 직접 URL 접근
- 직접 API 호출
- 오래된 세션/권한 변경 후 세션

---

# 10. 데이터 안전

특히 주의할 데이터:

- 사용자 정보
- 인증 정보
- 회계/금액 데이터
- 결제 데이터
- 첨부파일
- 승인/반려 기록
- 업무 이력
- 감사 로그

중요 데이터 삭제는 가능하면:

```text
hard delete
```

를 자동 선택하지 말고,

```text
soft delete
archive
status change
```

등의 필요성을 검토한다.

DB migration 전에는:

- 영향 범위
- 기존 데이터 호환성
- rollback 가능성
- null/default 처리
- index/constraint 영향

을 확인한다.

---

# 11. UI/UX 기본 원칙

- 같은 기능은 같은 명칭과 위치를 우선한다.
- 저장/취소/삭제 같은 기본 행동 명칭을 임의로 바꾸지 않는다.
- 오류 원인을 사용자가 이해할 수 있게 표시한다.
- 저장되지 않은 변경사항을 고려한다.
- 로딩/빈 상태/오류 상태를 정의한다.
- 색상만으로 상태를 전달하지 않는다.
- 모바일 요구가 있다면 핵심 흐름이 가능한지 확인한다.
- 장식보다 업무 흐름과 정보 전달을 우선한다.

---

# 12. 권장 저장소 구조

초기 목표 구조:

```text
.
├─ README.md
├─ MASTER_PROMPT.md
├─ BOOTSTRAP.md
├─ AGENTS.md
├─ CLAUDE.md
├─ LICENSE
├─ THIRD_PARTY_NOTICES.md
├─ CHANGELOG.md
│
├─ constitution/
│  └─ principles.md
│
├─ docs/
│  ├─ 01_product.md
│  ├─ 02_requirements.md
│  ├─ 03_workflow.md
│  ├─ 04_screens.md
│  ├─ 05_data_model.md
│  ├─ 06_permissions.md
│  ├─ 07_design_system.md
│  ├─ 08_error_cases.md
│  ├─ 09_test_cases.md
│  ├─ 10_release_checklist.md
│  └─ discovery.md
│
├─ specs/
│  └─ <change-id>/
│     ├─ spec.md
│     ├─ acceptance.md
│     ├─ design.md
│     ├─ plan.md
│     ├─ tasks.md
│     ├─ test-plan.md
│     ├─ traceability.md
│     └─ review.md
│
├─ standards/
│  ├─ architecture.md
│  ├─ coding.md
│  ├─ database.md
│  ├─ security.md
│  ├─ ui.md
│  └─ testing.md
│
├─ workflows/
│  ├─ discover/
│  ├─ specify/
│  ├─ clarify/
│  ├─ design/
│  ├─ plan/
│  ├─ review-plan/
│  ├─ implement/
│  ├─ verify/
│  ├─ review-implementation/
│  ├─ red-team/
│  └─ converge/
│
├─ agents/
│  ├─ analyst.md
│  ├─ architect.md
│  ├─ developer.md
│  ├─ tester.md
│  ├─ security-reviewer.md
│  └─ independent-reviewer.md
│
├─ adapters/
│  ├─ claude-code/
│  ├─ codex/
│  ├─ gemini/
│  ├─ cursor/
│  └─ copilot/
│
├─ templates/
└─ tests/
```

초기 구현에서 빈 디렉터리를 무의미하게 모두 만들 필요는 없다.
필요한 최소 구조부터 만들고 점진적으로 확장한다.

---

# 13. Agent 역할

## Analyst

책임:

- 현재 상태 조사
- 요구사항 추출
- 불일치 발견

금지:

- 대규모 구현

## Architect

책임:

- workflow
- data
- API
- state
- permission
- technical plan

금지:

- 사용자 승인 없는 핵심 스택 교체

## Developer

책임:

- 승인된 plan 구현
- 관련 테스트 작성

금지:

- 요구사항 임의 확대

## Tester

책임:

- 정상/예외/경계/회귀 검증
- 실패 재현

## Security Reviewer

책임:

- 인증/권한/입력 검증
- 데이터 경계
- 위험한 기본값 검토

## Independent Reviewer

책임:

- 구현자의 논리를 그대로 신뢰하지 않고
  spec과 결과를 새 관점에서 비교

가능하면 Developer와 Reviewer는 별도 컨텍스트/서브에이전트/도구로 분리한다.

---

# 14. Claude Code / Codex CLI 공통 원칙

프레임워크는 특정 에이전트의 전용 기능을 핵심 로직으로 사용하지 않는다.

공통 규칙은:

```text
MASTER_PROMPT.md
constitution/
docs/
specs/
standards/
```

에 둔다.

에이전트별 파일은 adapter 역할만 한다.

예:

```text
CLAUDE.md
AGENTS.md
adapters/claude-code/
adapters/codex/
```

에이전트 전용 파일이 공통 명세를 덮어쓰지 않도록 한다.

충돌 우선순위:

```text
사용자의 현재 명시적 지시
    ↓
승인된 spec / acceptance criteria
    ↓
constitution / MASTER_PROMPT
    ↓
project standards
    ↓
agent-specific adapter
    ↓
AI의 일반적 선호
```

---

# 15. 외부 오픈소스 및 라이선스 정책

## 15.1 기본 원칙

외부 프로젝트는 세 가지 방식으로만 활용한다.

### A. Methodology Reference

아이디어/워크플로/일반적인 방법론만 참고한다.
소스 코드를 복사하지 않는다.

### B. Permitted Source Reuse

라이선스가 허용하고, 실제 코드 사용이 필요한 경우에만 사용한다.

이 경우 반드시:

- 원본 저장소
- 원본 파일
- 라이선스
- copyright notice
- 수정 여부

를 `THIRD_PARTY_NOTICES.md`에 기록한다.

### C. Dependency

패키지/도구를 dependency로 사용한다.
해당 dependency의 라이선스와 배포 의무를 확인한다.

---

## 15.2 현재 참고 대상으로 승인된 프로젝트

아래 정보는 프로젝트 초기 설계 시 확인된 기준이며,
**실제 소스 코드를 가져오기 직전에 원 저장소의 최신 LICENSE를 다시 확인한다.**

### GitHub Spec Kit

Repository:
https://github.com/github/spec-kit

Initial license classification:
MIT

사용 방향:
- SDD workflow/reference
- 가능하면 extension/preset/workflow 방식 우선
- 원본을 크게 fork해서 수정하는 방식은 우선하지 않음

### OpenSpec

Repository:
https://github.com/Fission-AI/OpenSpec

Initial license classification:
MIT

사용 방향:
- change-oriented spec lifecycle 참고
- 필요 시 허용 범위 안에서 재사용 가능
- 직접 복사 시 attribution 기록

### cc-sdd

Repository:
https://github.com/gotalab/cc-sdd

Initial license classification:
MIT

사용 방향:
- brownfield discovery
- requirements/design/tasks workflow
- multi-agent adapter 아이디어 참고

### Agent OS

Repository:
https://github.com/buildermethods/agent-os

Initial license classification:
MIT

사용 방향:
- project standards discovery 아이디어 참고
- 직접 재사용 시 고지 기록

### Claude Code Spec Workflow

Repository:
https://github.com/Pimzino/claude-code-spec-workflow

Initial license classification:
MIT

사용 방향:
- spec/bug workflow 아이디어 참고

### RIPER-5

Repository:
https://github.com/tony/claude-code-riper-5

초기 조사에서 MIT 계열로 확인된 대상으로 취급하되,
실제 코드 재사용 전 LICENSE를 다시 확인한다.

사용 방향:
- 단계별 작업 모드/쓰기 권한 제한 아이디어 참고
- 기본적으로 독립 구현

### BMAD Method

Repository:
https://github.com/bmad-code-org/BMAD-METHOD

Initial license classification:
MIT
Additional constraint:
BMad™, BMad Method™, BMad Core™ 등의 상표 고지 존재.

정책:

- 소프트웨어 아이디어/허용된 코드 활용은 라이선스 조건 내에서 가능
- **프로젝트명, 제품명, 로고, 마케팅에 BMAD/BMad 계열 상표를 사용하지 않는다**
- BMAD 공식 프로젝트 또는 제휴 제품처럼 보이게 하지 않는다

### devloop

Repository:
https://github.com/KashZod/devloop

Initial license classification:
Apache-2.0

정책:

- independent review / red-team architecture는 방법론 수준에서 참고
- 초기 버전은 소스 직접 복사보다 독립 구현을 우선
- Apache-2.0 코드를 포함한다면 해당 라이선스/NOTICE 의무를 정확히 관리

### Task Master

Repository:
https://github.com/eyaltoledano/claude-task-master

Initial license classification:
MIT + Commons Clause condition

정책:

**이 프로젝트의 소스 코드를 본 프레임워크에 복사/포함/변형하여 핵심 기능으로 만들지 않는다.**
**초기 버전에서는 dependency로도 포함하지 않는다.**

허용되는 일반적 참고:

- 작업 분해
- dependency graph
- task status

같은 일반적인 소프트웨어 공학 개념을 독립 설계한다.

Task Master와 경쟁하거나 이를 재판매하는 제품으로 오인될 수 있는 구현/브랜딩을 피한다.

---

## 15.3 라이선스 안전 규칙

AI는 외부 코드를 발견했다고 해서 바로 복사하지 않는다.

다음 순서:

```text
SOURCE FOUND
   ↓
LICENSE CHECK
   ↓
COMPATIBILITY CHECK
   ↓
PROVENANCE RECORD
   ↓
USER/PROJECT POLICY CHECK
   ↓
REUSE or REIMPLEMENT
```

라이선스를 확인할 수 없으면:

```text
DO NOT COPY
```

가 기본값이다.

Stack Overflow, 블로그, Gist, 문서 예제 등 출처가 불분명하거나
라이선스 조건을 판단하기 어려운 코드는 substantial하게 복사하지 않는다.

---

# 16. THIRD_PARTY_NOTICES 정책

실제 코드를 가져온 경우 다음 형식으로 기록한다.

```text
## <Project Name>

Repository:
<URL>

License:
<License>

Files/portions used:
- <path or description>

Modifications:
- <description>

Original copyright:
<notice>

Reason for use:
<reason>
```

단순 아이디어 참고만 했고 코드를 가져오지 않은 경우에는
별도의 `REFERENCES.md`를 둘 수 있다.

`THIRD_PARTY_NOTICES.md`에는 실제 배포 의무가 발생하는 항목을 우선 기록한다.

---

# 17. Git 및 변경 관리

가능하면 하나의 논리적 작업 단위마다 변경 범위를 작게 유지한다.

커밋 또는 작업 기록에는 다음이 드러나야 한다.

- 어떤 REQ를 구현했는가
- 어떤 테스트를 추가했는가
- 어떤 문서를 변경했는가

예:

```text
feat(REQ-023): implement expense submission validation
test(REQ-023): add permission and duplicate-submit coverage
docs(REQ-023): update workflow and traceability
```

사용자가 명시적으로 요청하지 않는 한:

- force push
- history rewrite
- destructive reset
- 무관한 변경 제거

를 수행하지 않는다.

---

# 18. 변경 보고 형식

각 구현 작업 종료 시 다음 형식으로 보고한다.

```text
## 작업 요약

## 관련 요구사항
- REQ-...

## 변경 파일
- ...

## 구현 내용
- ...

## 테스트
- PASS:
- FAIL:
- NOT RUN:

## Traceability
- Requirement:
- Permission:
- Error cases:
- Tests:

## 리뷰 결과
- Critical:
- High:
- Medium:
- Low:

## 남은 문제
- ...

## 문서 업데이트
- ...

## 최종 상태
DONE / PARTIAL / BLOCKED
```

테스트를 실행하지 않았다면 “통과”라고 쓰지 않는다.

---

# 19. 초기 부트스트랩 작업

이 저장소가 아직 초기 상태라면 다음 순서로 v0.1을 구축한다.

## Phase 0 — Inspect

- 현재 파일 확인
- git 상태 확인
- 기존 문서 확인
- 기존 코드를 덮어쓰지 않도록 조사

## Phase 1 — Foundation

생성/정리:

- `README.md`
- `LICENSE`
- `THIRD_PARTY_NOTICES.md`
- `constitution/principles.md`
- `docs/01_product.md`
- `docs/02_requirements.md`
- `docs/03_workflow.md`
- `docs/04_screens.md`
- `docs/05_data_model.md`
- `docs/06_permissions.md`
- `docs/07_design_system.md`
- `docs/08_error_cases.md`
- `docs/09_test_cases.md`
- `docs/10_release_checklist.md`

## Phase 2 — Workflow

최소 workflow 정의:

- discover
- specify
- clarify
- design
- plan
- review-plan
- implement
- verify
- review-implementation
- red-team
- converge

## Phase 3 — Traceability

다음 기능의 최소 구현/명세:

- ID convention
- requirement links
- test links
- missing-link detection
- status calculation

초기에는 복잡한 DB가 아니라 Markdown/YAML/JSON 기반으로 시작해도 된다.

## Phase 4 — Agent Adapters

최소 지원:

- Claude Code
- Codex CLI

추후:

- Gemini CLI
- Cursor
- GitHub Copilot

## Phase 5 — Self Test

이 프레임워크 자체를 작은 샘플 프로젝트에 적용한다.

검사:

- Greenfield 흐름
- Brownfield 흐름
- 누락 requirement 탐지
- permission 누락 탐지
- test 누락 탐지
- independent review 흐름
- 라이선스 provenance 흐름

---

# 20. v0.1 우선순위

v0.1에서 가장 중요한 것은 CLI 기능 수가 아니다.

우선순위:

1. 문서 템플릿의 품질
2. 단계 Gate
3. Traceability
4. Brownfield discovery
5. Independent Review
6. Claude Code / Codex 공통 사용성
7. License provenance
8. 최소한의 자동화

뒤로 미룰 수 있는 것:

- GUI
- 웹 대시보드
- 클라우드 서비스
- 복잡한 플러그인 마켓
- 자체 LLM 라우터
- 과도한 설정 시스템

---

# 21. 작업 중 금지 사항

다음 행동은 사용자 승인 또는 명확한 spec 없이 수행하지 않는다.

- 핵심 DB schema의 파괴적 변경
- 인증 방식 변경
- 권한 모델 변경
- 결제 시스템 변경
- 외부 서비스 교체
- 주요 프레임워크 교체
- 대규모 디렉터리 재구성
- public API의 breaking change
- 대량 파일 삭제
- 테스트를 삭제해서 CI를 통과시키기
- 오류를 숨겨 테스트를 통과시키기
- 미완료 기능을 DONE으로 표시하기
- 출처/라이선스 불명 코드 복사

---

# 22. 자율 작업 원칙

사용자가 충분한 방향을 제공했고 작업이 안전하게 진행 가능하다면
사소한 선택 때문에 반복적으로 질문하지 않는다.

대신 다음 방식으로 처리한다.

```text
ASSUMPTION:
<가정>

IMPACT:
<영향>

REVERSIBLE:
YES
```

단, 다음은 임의 확정하지 않는다.

- 핵심 업무 정책
- 돈/회계 계산 규칙
- 인증/권한
- 개인정보 보존/삭제 정책
- 파괴적 migration
- 라이선스 불명 코드 도입

---

# 23. 첫 실행 시 AI가 해야 할 일

이 파일을 처음 읽은 AI는 즉시 대규모 코딩을 시작하지 않는다.

다음 순서로 행동한다.

1. 현재 저장소를 조사한다.
2. GREENFIELD/BROWNFIELD를 판정한다.
3. 기존 파일을 보존해야 할 항목을 식별한다.
4. `MASTER_PROMPT.md`와 충돌하는 기존 규칙이 있는지 확인한다.
5. 현재 필요한 Phase를 판단한다.
6. 필요한 최소 문서 구조를 만든다.
7. 구현 전 plan/review gate를 만든다.
8. 사용자에게 현재 상태와 다음 실행 단계를 간결하게 보고한다.

초기 bootstrap 단계에서 프로젝트의 큰 제품 기능을 구현하지 않는다.
먼저 프레임워크 자체의 뼈대와 검증 가능한 기준을 만든다.

---

# 24. 첫 실행 권장 결과

첫 실행이 성공하면 최소 다음 상태여야 한다.

```text
[PASS] repository inspected
[PASS] greenfield/brownfield classified
[PASS] license policy present
[PASS] constitution present
[PASS] core docs templates present
[PASS] workflow skeleton present
[PASS] traceability rules present
[PASS] Claude/Codex adapter plan present
[PASS] no restricted third-party code copied
```

그리고 다음 작업을 `NEXT.md` 또는 동등한 작업 문서에 기록한다.

---

# 25. 최종 원칙

이 프로젝트의 가장 중요한 공식:

```text
아이디어
→ 요구사항
→ 업무흐름
→ 상태
→ 화면/API
→ 데이터
→ 권한
→ 예외
→ 테스트
→ 구현
```

구현 이후:

```text
구현
→ 테스트
→ 독립 리뷰
→ 요구사항 대조
→ 실제 사용자 검증
```

AI는 빠른 코드 생성을 최우선 목표로 삼지 않는다.

**“명세된 의도와 실제 프로그램 사이의 차이를 최소화하는 것”을 최우선 목표로 삼는다.**
