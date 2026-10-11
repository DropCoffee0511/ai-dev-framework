# PROGRESS — 자율 루프 진행 기록

상태의 기준 파일은 이 문서 하나다. 백로그는 `NEXT.md`, Gate 판정은 `docs/gates.md`이며 진행 상태를 여기서 따로 복제하지 않는다. 루프 규칙은 `AUTOPILOT.md`(로컬 전용 파일로 커밋하지 않는다 — R7), 웨이브 기록 규약은 그 §8이다.

이 브랜치(`feature/traceability-script`, main `a33e74f` 기준)는 wave 002 전용이다. wave 001 기록은 `feature/audit-001-reverify` 브랜치(미푸시 2커밋)에서 이어 받아 아래 웨이브 기록에 보존했다.

## 최근 요약 (wave 003)

- 최종 갱신: 2026-10-11 09:5X KST (웨이브 9 세션 — 구현 후보 3)
- 이번 과제: `NEXT.md` 구현 후보 3 — Brownfield discovery 절차 구체화(`workflows/discover/`)와 `/project-discover` 동작 정의
- 상태: **구현 완료·독립 검토 대기** — 커밋 `7b04987`(브랜치 `feature/brownfield-discovery`, wave 002 종결 브랜치 `feature/traceability-script` 위에서 분기). 결정론적 검증 전부 통과(4종 게이트, `--self-test`, 자기 저장소 적용 exit 0). 독립 검토는 런 `dwfrun-f56c5c4b`(검증자 2명: 수용 조건 6항목 / 규칙 무결성 6항목, `GLM-5.3-Flash$high`, 커밋-핀 판독) 접수 — 판정 수신 시 아래 웨이브 기록에 덧붙인다
- 다음 실행의 첫 작업: 런 `dwfrun-f56c5c4b` 판정 수신 → APPROVE면 wave 003 완료 기록, FAIL이면 지적 반영 후 재검토. REQUEST_CHANGES 항목은 규칙 약화 여부부터 확인
- push 승인 대기: `feature/audit-001-reverify` 2커밋 + `feature/traceability-script` 15커밋 + `feature/brownfield-discovery` (이번 세션 커밋 포함) — push는 사용자 승인 대상
- 사용자 참고: `사용자사용메뉴얼.md`는 커밋된 적 없는 미추적 파일이다(README가 참조하므로 커밋할지는 사용자 결정). wave 002의 5단계 사용자 샘플 테스트(메뉴얼 3단계)도 사용자 실행 차례다

## 스프린트 카드 (wave 003)

- 과제 ID: `NEXT.md` 구현 후보 3 — "Brownfield discovery 절차 구체화 (`workflows/discover/`) 와 `/project-discover` 동작 정의"
- 문제: `MASTER_PROMPT.md` §3.2의 10개 절차가 한 줄 나열뿐이라 실행 방법이 없다. `docs/audits/audit-002.md`가 "Greenfield/Brownfield 적용성 FAIL — Brownfield 조사 요구는 있으나 인벤토리·기준선 범위 형식이 없다"(L25), "ERP 전체와 이번 변경 중 어느 범위를 기준선으로 삼을지, 어떤 표로 완료를 확인할지 없다"(L77)를 지적했다. `/project-discover`는 이름만 예약돼 동작이 정의돼 있지 않다
- 이번 결과: 기존 프로젝트에서 discover를 실행할 수 있는 절차 문서(기준선 범위 판정 → §3.2 10개 절차별 확인 대상·기록 위치 → 인벤토리·완료 확인 표)와 `/project-discover` 동작 정의 초안이 생긴다
- 범위: `workflows/discover/brownfield.md`(신규), `workflows/discover/README.md`, `adapters/claude-code/README.md`, `NEXT.md`, `CHANGELOG.md`, 이 파일. 규칙 단일 출처 본문(`MASTER_PROMPT.md` §3.2·§5.1, convention)은 변경하지 않는다
- 규칙 순증가: 절차 문서 1개 — 근거는 구현 후보 3(`NEXT.md`) + `docs/discovery.md` 미결 #8("Brownfield 분석 방식 → `workflows/discover/`에 절차 정의") + audit-002 적용성 시나리오 지적. 단일 출처 본문 순증가 0줄(포인터만)
- 불변식 영향(`AUTOPILOT.md` §2): 규칙 단일 출처 유지(§3.2·§5.1을 복제하지 않고 실행 방법만 기술, 충돌 시 본문 우선을 문서 머리에 명시), 최소 증가(근거 있는 1:1 추가), 템플릿·자기 기록 분리(`docs/01~10` 템플릿 미건드림), 버전·이력 일치(CHANGELOG·NEXT 갱신), 추적 가능성(audit-002 시나리오·후보 3·미결 #8과 연결)
- 수용 조건:
  1. 절차 문서가 §3.2의 10개 항목 각각에 확인 대상·기록 위치를 대응시키고, 기준선 범위 판정(§3.2의 "어느 범위까지 조사하는가")과 완료 확인 표(audit-002 L77의 "어떤 표로 완료를 확인할지")를 포함한다
  2. `/project-discover` 동작 정의 초안이 목적·입력·수행·산출물·금지·Gate를 정의하고, 이름·동작의 확정이 사용자 결정임을 명시한다 (`docs/discovery.md` 미결 #3·R4 유지)
  3. `workflows/README.md`의 단계 목록·Gate 매핑과 모순이 없다 (조건부 게이트 ①)
  4. 4종 문서 게이트 + 스크립트 자기 저장소 적용 통과
  5. dynamic-workflow 독립 리뷰 접수 (지연 시 검토 대기 등재와 경로·상태 기록까지)
- 확인 수단: 4종 게이트(`AUTOPILOT.md` §3.1) + `scripts/check_traceability.py` 자기 적용 + dynamic-workflow 독립 리뷰어

- 과제 ID: `NEXT.md` 구현 후보 2 — "`docs/traceability-convention.md` §3–§5를 자동 계산. 입력은 Markdown/YAML"
- 문제: convention §3 차원 판정·§4 상태 계산·§5 Gate 기록 판독이 전부 수동이라 계산 누락·실수·우회가 가능하다 (`docs/discovery.md` R3의 하위 문제)
- 이번 결과: 단일 파일 스크립트(python3 표준 라이브러리만)가 traceability.md의 REQ별 차원·상태와 gates.md 기록의 현재 값을 계산하고, 내장 시험(--self-test)과 자기 저장소 적용으로 검증된다
- 범위: `scripts/check_traceability.py`(신규), `docs/traceability-convention.md`(도입 안내 1줄 포인터), `CHANGELOG.md`, `NEXT.md`, `README.md`·`AGENTS.md` 상태 문구 최소 갱신, 이 파일. 규칙 본문(convention §1–§7 내용)은 변경하지 않는다
- 규칙 순증가 목표: ≤3줄 → **실제 2줄** (convention 안내 문장, README 구조 목록. 규칙 추가 없음 — 스크립트는 규약의 계산기일 뿐이다)
- 불변식 영향(`AUTOPILOT.md` §2): 규칙 단일 출처 유지(스크립트가 규칙을 새로 정의하지 않고 convention §3–§5를 계산 — docstring에 명시), 최소 증가(실제 2줄), 템플릿·자기 기록 분리(`scripts/`는 양쪽 아님), 버전·이력 일치(CHANGELOG·README·AGENTS 갱신), 추적 가능성(`NEXT.md` 구현 후보 2와 연결)
- 수용 조건:
  1. 스크립트는 python3 표준 라이브러리만 쓰는 단일 파일이다 (외부 의존성·manifest 0) — ✅ import는 argparse·os·re·subprocess·sys·tempfile뿐
  2. `--self-test`가 §3 차원 판정(PASS/PARTIAL/MISSING)·§4 상태 계산(DONE/IN PROGRESS/NOT READY)·§5 기록 유효성(5칸, 값, 판정자 유형, 맨 아래 줄, 이력 구역 무시, STALE) 사례를 전부 통과한다 — ✅ 통과(종료 코드 0). 1차 검토가 "5칸·값·맨 아래 줄 사례 부재"를 지적해 보강했다(27건)
  3. 자기 저장소 적용: 저장소 루트에서 실행해 `docs/gates.md` 기록 표를 판독하고(B_FINAL=false 유효 줄, 이력 구역 무시) 구조 위반 0건으로 종료한다 — ✅ B_FINAL=false 판독, 이력 14줄 제외, 위반 0건(종료 코드 0). 1차 검토 수정 후 재확인
  4. 4종 문서 게이트 통과, `CHANGELOG.md`·`NEXT.md` 기록 갱신 후 작업 브랜치 커밋 (push는 승인 대상) — ✅ 커밋 `3477dd6` + 검토 반영 커밋
  5. dynamic-workflow 독립 리뷰를 받는다 (지연 시 검토 대기 등재와 경로·상태 기록까지) — ✅ 1차 FAIL(계산 격차 HIGH 2건) → 지적 수정 → 재검증 **APPROVE**(런 `dwfrun-edf17f7f`, 9건 전부 RESOLVED·약화 0건·새 CRITICAL/HIGH 0건)
- 확인 수단: `--self-test` + 자기 저장소 실행 출력 + 4종 문서 게이트(`AUTOPILOT.md` §3.1) + dynamic-workflow 독립 리뷰어

## 웨이브 기록

### wave 003 — 구현 후보 3: Brownfield discovery 절차 + /project-discover 동작 정의 (2026-10-11, 검토 대기)

- 최종 갱신: 2026-10-11 09:5X KST / 과제: `NEXT.md` 구현 후보 3 / 상태: 구현 완료·독립 검토 대기(커밋 `7b04987`, 미푸시)
- 근거 확인: `docs/audits/audit-002.md` L25·L77의 적용성 시나리오 지적("인벤토리·기준선 범위 형식 없다", "어느 범위를 기준선으로 삼을지, 어떤 표로 완료를 확인할지 없다")이 이 과제의 빈곳을 직접 지목. `docs/discovery.md` 미결 #8이 절차 정의 장소를 `workflows/discover/`로 정해 둠. 후보 1(Gate 자동 강제)은 사용자 결정 항목("Gate 구현 방식")과 겹쳐 착수하지 않음(§3.2-a)
- 변경한 문서: `workflows/discover/brownfield.md`(신규 — §0 기준선 범위 판정, §1 절차별 확인 대상·기록 위치 표, §2 기능 인벤토리 표, §3 완료 확인 표, §4 금지), `workflows/discover/README.md`(동작 정의 초안 절 추가), `adapters/claude-code/README.md`(예약 문구 갱신), `NEXT.md`(후보 3 완료 표기), `CHANGELOG.md`, 이 파일. `MASTER_PROMPT.md`·convention·`workflows/README.md`·`docs/01~10` 미변경
- 규칙 순증가: 절차 문서 1개(58줄, 근거는 후보 3+미결 #8+audit-002). 단일 출처 본문 순증가 0줄 — 카드 목표대로. 문서 관행은 평서체·기존 표 형식 유지
- 4종 게이트: ① 참조(세션당 1회 전체 스캔, 시작 시 오탐 0건) ② 링크(신규 파일 포함 재스캔, 깨진 링크 0건) ③ §-참조(변경 5문서 — §3.1·§3.2·§5.1·§5.11·§9·§10·§15.3·§21·§22 ↔ MASTER_PROMPT 실제 섹션, §1·§2·§5.1·§5.2 ↔ convention — 전부 일치) ④ CHANGELOG 갱신 — 전부 통과. `--self-test`와 자기 저장소 적용도 exit 0. 조건부 게이트: ① workflows/README.md 단계·Gate 매핑과 모순 없음(단계·Gate 정의 미변경) ② README 상태 문구 실제와 일치(CLI 미존재 유지) ③ gates.md 판정 추가 없음(해당 없음)
- 독립 검토: 런 `dwfrun-f56c5c4b-99f8-41b6-926d-7ab1fec64b20`(1-페이즈: 결정론적 게이트 2건 + 검증자 2명 병렬 — 수용 조건 6항목 / 규칙 무결성 6항목, `GLM-5.3-Flash$high`, 커밋-핀 `7b04987` 판독, 초안 `.zcode/workflow-drafts/wave-003-독립-검토-커밋-7b04987.dwf.ts`). 판정 대기 — 대기 시간은 스프린트 예산에 세지 않는다(전례 실측: wave 001 약 9시간)
- 도구로 확인한 근거: 위 게이트 실행 출력. 외부 조사(WebFetch 등) 미사용 — 이번 과제는 저장소 내 근거(감사·규약·백로그)로 충분했다
- 유지보수: 없음 (과제 작업만 수행)
- 커밋: `7b04987`(feat, 6개 파일 +107/−11) + 기록 커밋(아래) — 브랜치 `feature/brownfield-discovery`(신규 분기, `git config aidev-framework.auto-branch`에 기록), 전부 미푸시
- 블로커: 없음. 다음 시도 조건: 판정 수신
- 다음 실행의 첫 작업: 판정 수신 → 지적 반영(있으면) → wave 003 완료 기록. 이후 후보: `NEXT.md` 구현 후보 4(Phase 5 Self Test — 실행·판정 범위는 사용자 승인 필요로 표기됨) 또는 §9 백로그 점검

### wave 002 — 구현 후보 2: Traceability 검사 스크립트 (2026-10-09~10, 재검증 APPROVE·잔여 지적 후속 접수)

- 최종 갱신: 2026-10-09 20:52 KST / 과제: `NEXT.md` 구현 후보 2 / 상태: 구현 완료·독립 검토 대기(커밋 `3477dd6`, 미푸시)
- 변경한 문서: 위 요약 참조. 규칙 순증가 2줄(카드 목표 ≤3줄 이내)
- 구현 요약: `scripts/check_traceability.py` — traceability.md의 제한된 YAML 블록을 파싱해 §1 ID 형식·정의 위치 대조, §2 링크 규칙(dangling, not_applicable 허용 차원, 활성 AC·등록 PERM/ERR 전부 연결, code 경로 존재), §3 차원 판정, §4 상태 계산, §5 기록 판독(맨 아래 유효 줄·이력 제외·판정자 규칙·§5.3 커밋-핀 재판정은 Review 차원)을 수행한다. 계산 근거가 없는 항목은 PASS 대신 보수적으로 PARTIAL/MISSING 처리한다(거짓 DONE 방지). 규약이 문맥 판단을 요구하는 항목(AC 검증 가능성, not_applicable 사유 타당성, 판정자 진위, 실행 커밋 이후 코드 변경 재실행)은 docstring에 v0 한계로 명시했다
- 개발 중 발견·수정한 자체 결함 4건: acceptance 중첩 키의 숫자가 키 정규식에 걸리지 않음, 여러 줄 not_applicable 사유 유실, gates 경로를 디렉터리로 전달, 이력 줄 수 집계에 헤더 행 포함 — 전부 `--self-test` 픽스처가 잡아냈다
- 4종 게이트: 전부 통과(요약 참조). 조건부 게이트: ① workflows 미건드림 ② README 갱신 후 일치 ③ gates.md 미건드림
- 독립 검토: `dwfrun-b216d5a7`(1-페이즈: world.run 결정적 게이트 2건 + 리뷰어 2명 병렬, `git show 3477dd6` 커밋-핀) — 판정 대기. 이 워크스페이스의 저장된 워크플로는 없었으므로 첫 사용 때 새로 만들었다(초안 `.zcode/workflow-drafts/wave-002-독립-검토-traceability-스크립트.dwf.ts`)
- 도구로 확인한 근거: `--self-test` 21건(종료 0), 자기 적용(종료 0, B_FINAL=false·이력 14줄·위반 0건), 4종 게이트 grep 출력. 리뷰어에게도 동일 검증을 `world.run`으로 직접 제공해 주장이 아니라 실행으로 검증하게 했다
- 이슈: 검토 워크플로의 호스트 큐 대기가 wave 001 실측 9시간이었다 — 이번에도 대기가 길어지면 상태는 '검토 대기'로 남고 대기 시간은 스프린트 예산에 세지 않는다
- 이슈(환경): 이 세션의 샌드박스 시계가 실제보다 약 12시간 늦게 표시됐다(세션 시작 실측 2026-10-09 20:07 KST 표기, 실제는 2026-10-10 08:07 KST경). 그 사이 밤새 후속 자율 세션(웨이브 3~6, `.autopilot-skip.log` 참조)이 만료된 잠금을 정상 인수했고, 08:09 KST에 웨이브 7 세션이 잠금을 인수한 뒤 이 세션과 병렬로 같은 커밋 `3477dd6`의 검토를 준비했다. 현재 커밋 `3477dd6`에 대한 검토 런이 **6건 큐 적재**(최초 = 이 세션의 `dwfrun-b216d5a7` 08:59:53 KST, 이후 웨이브 7경으로 보이는 4건 + 기존 라벨 1건, 전부 토큰 0 대기 중). 판정은 **최초로 완료되는 런**을 사용하고 나머지는 중복으로 기록한다. 중복 런 취소는 다른 세션 소유 산출물이라 사용자 승인 대상이며, 이 세션은 잠금 파일을 건드리지 않는다(현재 잠금은 웨이브 7 소유)
- 유지보수: 없음 (과제 작업만 수행)
- 블로커: 없음. 다음 시도 조건: 리뷰 판정 수신
- 다음 실행의 첫 작업: 판정 수신 → 지적 반영 → 상태 갱신(완료). REQUEST_CHANGES면 수정 후 규약 대조 재검토

#### 2026-10-10 (웨이브 7 세션) — 1차 판정 수신·지적 수정

- 최종 갱신: 2026-10-10 10:27 KST / 상태: 지적 수정 완료·재검토 대기
- 1차 독립 검토: 6건 중복 런 중 **첫 완료 런 `dwfrun-3d1d3dfe`**(09:00:46 KST 디스패치, 10:04:39 KST 완료, 1,000,625 토큰)의 판정을 채택 — 종합 **FAIL**(규약 일치 FAIL / 규칙 무결성 APPROVE, 규칙 약화 0건). HIGH 2건(빈 AC 목록·증거 필드 미채움 PASS가 거짓 DONE 경로), MEDIUM 4건, LOW 7건, 전부 verified. 전문은 `docs/audits/wave002-review-2026-10-10.md`. `dwfrun-b216d5a7` 등 나머지 5런은 중복 판정으로 기록만 남긴다(다른 세션 소유 산출물이라 취소는 사용자 승인 대상)
- 웨이브 7 세션 자신의 중복 런 `dwfrun-500dee96`은 판정 확보 후 토큰 0인 채 중단했다(자기 런이라 승인 불필요, 슬롯 양보)
- 지적 수정(스크립트와 기록 문서만 — 규칙 문서 순증가 0줄): HIGH 2건(AC 빈 TC 목록·필수 권한 테스트 빈 TC → Tests MISSING / 실행 증거 §4 필수 칸 미채움 PASS는 증거 아님), MEDIUM 3건(§5.2 3행 Gate 판정자 빈 칸 무효·보고 표시 / self-test 사례 보강 / Review에서 값 false 우선 평가), LOW 4건(docstring·CHANGELOG 주장 정정 / screen_api SCR-/API- 외 ID 위반 / code 저장소 밖 경로 위반 / 초과 REQ 위반→비고 완화). LOW 8(작성자 판별)은 §5.4 고지 한계라 미수정 — 1차 검토도 같은 판정
- 재검증: `--self-test` 27건 전부 통과(종료 0, 21건→27건), 자기 저장소 적용 위반 0건(종료 0), 게이트 1·2 전체 스캔 통과, 게이트 3(변경 문서 §-참조 ↔ convention 실제 섹션 `## 1`~`## 7`, `### 5.1`~`### 5.4`) 통과, 게이트 4 CHANGELOG [Unreleased] 갱신. 조건부 게이트: ① workflows 미건드림 ② README 상태·한계 — 이번 변경으로 무관 ③ gates.md 판정 추가 없음
- 추가 접수(2번째 완료 중복 런 `dwfrun-4505d5b5`의 신규 지적 2건 — 판정 자체는 구 커밋 대상 중복이지만 지적은 유효): ① ADOPTING.md §1 복사 허용 목록에 `scripts/` 분류 누락(medium — wave 002 후속 1줄 수정 후보, 규칙 순증가를 수반하므로 근거와 함께 기록 필요) ② audit-002 L-1(not_applicable 사용 시 등록 PERM/ERR가 있어도 PASS 가능) 트랩이 self-test에 미시험(medium — L-1은 NEXT.md 미수정·사용자 승인 대상 항목이라 자율 착수하지 않는다)
- 유지보수: 없음 (과제 작업만 수행)
- 커밋: 검토 보고·스크립트 수정 fix 커밋 + progress 기록 커밋 (브랜치 `feature/traceability-script`, 미푸시 — push는 사용자 승인 대상)
- 블로커: 없음. 다음 시도 조건: 재검토 판정 수신
- 다음 실행의 첫 작업: 재검토 런 `dwfrun-edf17f7f-343f-4929-bb58-37b9c91d2b07`(수정 커밋 `fbfeaa4` 대상) 판정 수신 → APPROVE면 wave 002 완료 기록·AC-5 ✅·추가 접수 2건 처리 판단, FAIL이면 지적 반영 → 규칙 약화 여부도 다시 확인

#### 2026-10-10 (웨이브 7 세션) — 재검증 APPROVE, 잔여 지적 인계 접수

- 최종 갱신: 2026-10-10 11:35 KST / 상태: 재검증 APPROVE + 잔여 지적 후속 접수
- 재검증: 런 `dwfrun-edf17f7f-343f-4929-bb58-37b9c91d2b07` — 수정 검증자·규칙 무결성 검증자 모두 **CLEAR**, 지적 9건 전부 **RESOLVED**(9/9 일치), 규칙 약화 0건, 새 CRITICAL/HIGH 0건, 결정론적 게이트 통과(`--self-test` exit 0·27건, 자기 적용 exit 0) — 종합 **APPROVE**. 전문 `docs/audits/wave002-reverify-2026-10-10.md`(항목별 file:line 표 전문은 런 아티팩트 보존 — 전문 회수는 검증자 재실행 약 100만 토큰을 요구해 생략하고 반환값·보고 항목에서 작성했다고 명시)
- **잔여 지적 인계(완료된 구 런들에서 1차 13지적에 없던 것 — 검증자들이 /tmp 픽스처 실행 재현까지 수행했고 메인 세션이 코드 판독으로 HIGH 2건을 재확인했다):**
  - N1(HIGH, 런 `87a8f59c`): gates.md에 `## 기록` 절이 없거나 0바이트면 `parse_gates`가 rows=None을 반환하고 `_load_gates`가 이를 순회해 TypeError 크래시 — exit 1(구조 위반과 혼동)·보고 소실. 신규 채택 프로젝트의 첫 실행 경로
  - R1(HIGH, 런 `b216d5a7`): plan_files 정규식 `[\w.-]+(?:/[\w.-]+)+`가 슬래시 없는 plan 경로(NOTICE 등)를 §5.3 재판정 대상에서 누락 — 거짓 DONE 경로 잔존
  - N2(medium): spec.md가 REQ를 선언해도 traceability.md 파일 자체가 없으면 위반 0건·exit 0(§2 회피) / N3(medium): spec.md가 없으면 범위 검사를 비고 없이 생략
  - R2(medium): tc_targets가 09 표 행 전체를 스캔(절차 칸의 ERR 언급도 커버 인정 — 대상 칸만 읽어야) / R3(medium): TASK 완료 휴리스틱이 "완료 후 재검토 필요"를 완료로 오판(`\[x\]|\bDONE\b|✅`로 축소 + 고지)
  - R4(LOW): REQ 상세 블록 없으면 Requirement PASS → PARTIAL이 보수적(1차 LOW-6과 상반 — 다음 검토에서 방향 확정) / R5(LOW): gates 근거 칸의 커밋 해시 미요구(convention §5.1 대조 후 처리) / R6(LOW): README "소스코드·CLI는 아직 없다" 문구 / R7(LOW): PROGRESS.md의 미추적 AUTOPILOT.md 참조에 "로컬 전용" 명시 / R8(LOW): .gitignore에 .autopilot.lock·.autopilot-skip.log 누락(AUTOPILOT.md는 사용자 파일이라 제외)
  - 런 `5ecaf5b2`의 신규 3건: CLAUDE.md 미갱신(스크립트 존재 반영), git 바이너리 요구 문서화, TRACEABILITY_COMPLETE ↔ 계산 DONE 교차검증 부재(계산기 범위에서 비고 경로로 검토)
  - 처리 방침: N1·R1 HIGH 최소 수정 + self-test 사례(N1·R1·R2·R3) → M/LOW 최소 수정 → 자체 검증 → 커밋 → 신규 커밋 대상 재검토 1회. R4·R5처럼 검토자 간 상반·규약 확인이 필요한 것은 수정 전 convention 대조를 먼저 한다
- 유지보수: 없음. 커밋: `f01d64b`(추가 접수)·`ed95dde`(재검증 보고·완료 기록) + 잔여 지적 접수 커밋 — 전부 미푸시
- 블로커: 없음. 다음 실행의 첫 작업: 최근 요약 헤더 참조(잔여 지적 흡수가 최우선)

#### 2026-10-10 (웨이브 8 세션) — 잔여 지적 흡수(사용자 편의 개선 1~4단계)

- 최종 갱신: 2026-10-10 23:05 KST / 과제: wave 002 잔여 지적 흡수 + 사용자 샘플 테스트 준비 / 상태: 수정 완료·재검토 대기
- 배경: 사용자가 "사용자 편의 개선 1~5단계 진행"을 지시했다. 1단계(N1·R1 흡수)·2단계(안내 문서 정비)·3단계(스크립트 결과 이해성)·4단계(ADOPTING scripts/ 분류)를 수행했고 5단계(사용자 샘플 테스트)는 사용자 실행이므로 준비 완료 보고까지가 이번 세션 범위다
- 스크립트 수정(`scripts/check_traceability.py`): N1 — `parse_gates`가 `## 기록` 절 부재 시 None 대신 빈 목록을 반환하고 보고에 "새 프로젝트의 정상 상태" 안내를 추가 / R1 — plan_files 정규식을 `[\w.-]+(?:/[\w.-]+)*`로 완화해 슬래시 없는 파일명도 재판정 대상에 포함(후보는 존재하는 파일로 한정) / N2 — spec.md가 REQ를 선언하는데 traceability.md 파일이 없으면 전 차원 MISSING(NOT READY) 항목 생성 / N3 — change 폴더의 spec.md 부재를 비고로 보고 / R2 — 케이스 목록 표의 헤더에서 대상 칸 위치를 찾아 그 칸만 읽는다 / R3 — TASK 휴리스틱을 `\[x\]|\bDONE\b|✅`로 축소 + 비고 고지 / R5 — USER 승인 Gate 제외 기록 줄의 근거 해시 부재를 비고로 보고 / TRACEABILITY_COMPLETE=true ↔ DONE 아닌 REQ 모순을 비고로 교차 보고 / R4 — 동작 유지(Requirement PASS+비고), docstring v0 한계에 상반 의견과 방향 미확정을 명시
- self-test 사례 추가(27건→44건): N1 크래시 회귀 4건, R1 NOTICE 대상 3건, R2 1건, R3 2건, N2 2건, N3 2건, R5 2건, 교차검증 1건
- 문서 보완: CLAUDE.md를 AGENTS.md의 스크립트 문구와 동기화(런 `5ecaf5b2` 지적), git 실행 요구를 README·AGENTS.md·CLAUDE.md·메뉴얼에 추가, README 상태 문구 모순 제거(R6)+메뉴얼 안내, 메뉴얼 §1 준비물(git)·§2 사례(44건)·§4-2 복사 목록(스크립트)·§5 갱신(버그 수정 상태), .gitignore R8, PROGRESS.md R7, ADOPTING.md §1 scripts/ 분류(근거는 `CHANGELOG.md`·`NEXT.md`)
- 검증: `--self-test` 44건 전부 통과(종료 0) / 자기 저장소 적용 종료 0(위반 0건, B_FINAL=false 판독, 이력 14줄 제외) / N1 재현(gates.md에 기록 절만 있는 저장소) 종료 0+안내 문구 확인 / ADOPTING 절차 /tmp 시뮬레이션 — 복사함 목록 복사 후 (a) 완전 새 프로젝트(gates.md 없음) (b) change 폴더(기록 절 없음) 모두 종료 0 / 게이트 1·2 전체 스캔 통과(오탐 0건), 게이트 3(변경 5문서의 §-참조 ↔ 대상 문서 실제 섹션) 통과, 게이트 4 CHANGELOG [Unreleased] 갱신. 조건부 게이트: ① workflows 미건드림 ② README 상태·한계 갱신 후 실제와 대조 ③ gates.md 판정 추가 없음
- 독립 검토: 신규 커밋 대상 재검토를 dynamic-workflow로 접수 — 런 `dwfrun-76f40125`(검증자 2명: 지적 15건 해소 / 규칙 무결성, `GLM-5.3-Flash$high`, 커밋-핀 `4ba3c2c` 판독). 판정 대기(대기 시간은 스프린트 예산에 세지 않는다). 판정 수신 시 이 항목에 결과를 덧붙인다
- 유지보수: 없음 (과제 작업만 수행)
- 커밋: fix(스크립트+문서 보완+기록) 1건 + docs(progress) 1건 — 전부 미푸시
- 블로커: 없음. 다음 실행의 첫 작업: 재검토 판정 수신 → 지적 반영(있으면) → 5단계 사용자 테스트 준비 보고 완료

#### 2026-10-11 (웨이브 8 세션 계속) — 재검토 1차 판정 수신(FAIL·신규 HIGH 1건)·수정·2차 접수

- 최종 갱신: 2026-10-11 01:2X KST / 상태: NEW-1 수정 완료·2차 재검토 대기
- 1차 재검토 판정: 런 `dwfrun-76f40125` — 잔여 지적 15건 전부 RESOLVED(검증자 2명 일치), 규칙 약화 없음, 규칙 무결성 CLEAR, 결정론적 게이트 통과. 단 수정 검증자가 **신규 HIGH 1건(NEW-1)을 실행으로 재현**해 종합 FAIL. 전문은 `docs/audits/wave002-residual-review-2026-10-11.md`(항목별 표 전문은 런 아티팩트 보존 — 회수 비용으로 반환값 기반 작성을 명시)
- NEW-1(HIGH·verified): R2 수정에서 넣은 헤더 판정 `cells[0] == 'ID' or any('대상' in c for c in cells)`이 데이터 행의 임의 칸에 '대상'이 있으면(절차 칸 "대상 화면 진입 후 입력") 그 행을 헤더로 오판 — TC가 결과 집계에서 탈락(NOT RUN→Tests PARTIAL)하고 `tc_target_col`이 어긋나 이후 행들도 잘못 읽음
- 수정(스크립트만 — 규칙 문서 0줄): 헤더 판정을 첫 칸이 정확히 'ID'인 행으로 한정. self-test 사례 11 추가(44건→47건): DONE 유지·TC-001 집계 유지·대상 칸 위치 유지 3건. 수정 후 검증자 재현 시나리오를 동일 픽스처로 재실행해 REQ-001=DONE·col=2·위반 0건 확인
- 2차 재검토 접수: 런 `dwfrun-12ca5a04`(NEW-1 해소·R2 원 요구 유지·회귀·기록 일치를 검증자 2명이 판정, `GLM-5.3-Flash$high`, 초안 `.zcode/workflow-drafts/wave-002-잔여지적-재검토2-커밋-71f085d.dwf.ts`). 판정 수신 시 이 항목에 결과를 덧붙인다
- 유지보수: 없음. 커밋: fix(NEW-1) + 기록(보고·CHANGELOG·NEXT·이 항목) — 전부 미푸시
- 블로커: 없음. 다음 실행의 첫 작업: 2차 재검토 판정 수신 → APPROVE면 wave 002 완전 종결, FAIL이면 지적 반영

#### 2026-10-11 — 2차 재검토 판정 수신·RECORDS 종결 (wave 002 잔여 지적 흡수 완결)

- 최종 갱신: 2026-10-11 02:1X KST / 상태: 완료·종결
- 2차 재검토 판정: 런 `dwfrun-12ca5a04` — **수정 검증 CLEAR(4/4 RESOLVED)·규칙 무결성 CLEAR(3/4)**, 규칙 약화 없음, 새 CRITICAL/HIGH 0건, 결정론적 게이트 통과(self-test 47건·자기 적용 exit 0). NEW-1 해소·R2 원 요구 유지·회귀 없음을 양쪽 검증자가 확인. 판정식은 미해소 1건(RECORDS·PARTIAL)으로 FAIL을 출력했다 — 코드 결함이 아니라 검증자 세션이 런 아카이브에 접근 불가해 감사 보고 ↔ 1차 런 반환값의 직접 대조를 못 한 것. 전문은 `docs/audits/wave002-residual-reverify2-2026-10-11.md`
- RECORDS 종결: 검증자가 제시한 방법("런 아카이브에 접근 가능한 세션에서 대조")대로 메인 세션이 1차 런 `dwfrun-76f40125` 반환값과 감사 보고를 항목별 대조 — 종합 FAIL·미해소 0건·약화 없음·15/15 RESOLVED·self-test 44건·NEW-1 재현 상세 **전부 일치**. 1차 보고에 부록으로 기록
- 종결 근거: ① 검증자 2명 CLEAR ② 규칙 약화 0건·새 CRITICAL/HIGH 0건 ③ 유일 PARTIAL(RECORDS)을 검증자 지정 방법으로 닫음. 사용자가 이 판단에 이의를 제기하면 재검토를 다시 접수할 수 있다
- 유지보수: 없음. 커밋: 종결 기록 1건 — 미푸시. 이후의 첫 작업: 사용자 샘플 테스트 지원 또는 구현 후보 3

#### wave 002 스프린트 카드 (참고용 보존)

- 과제 ID: `NEXT.md` 구현 후보 2 — "`docs/traceability-convention.md` §3–§5를 자동 계산. 입력은 Markdown/YAML"
- 문제: convention §3 차원 판정·§4 상태 계산·§5 Gate 기록 판독이 전부 수동이라 계산 누락·실수·우회가 가능하다 (`docs/discovery.md` R3의 하위 문제)
- 이번 결과: 단일 파일 스크립트(python3 표준 라이브러리만)가 traceability.md의 REQ별 차원·상태와 gates.md 기록의 현재 값을 계산하고, 내장 시험(--self-test)과 자기 저장소 적용으로 검증된다
- 범위: `scripts/check_traceability.py`(신규), `docs/traceability-convention.md`(도입 안내 1줄 포인터), `CHANGELOG.md`, `NEXT.md`, `README.md`·`AGENTS.md` 상태 문구 최소 갱신, 이 파일. 규칙 본문(convention §1–§7 내용)은 변경하지 않는다
- 규칙 순증가 목표: ≤3줄 → **실제 2줄** (convention 안내 문장, README 구조 목록. 규칙 추가 없음 — 스크립트는 규약의 계산기일 뿐이다)
- 수용 조건 5건: ① 단일 파일·외부 의존성 0 ② `--self-test`가 §3·§4·§5 사례 전부 통과 ③ 자기 저장소 적용 위반 0건 ④ 4종 게이트 통과·기록 갱신·커밋 ⑤ dynamic-workflow 독립 리뷰 — 전부 ✅ (최종: self-test 47건, 재검증 APPROVE 런 `dwfrun-edf17f7f`, 잔여 지적 흡수 후 2차 재검토 CLEAR 런 `dwfrun-12ca5a04`. 상세는 위 웨이브 기록)
- 확인 수단: `--self-test` + 자기 저장소 실행 출력 + 4종 문서 게이트 + dynamic-workflow 독립 리뷰어

### wave 001 — audit-001 2차 지적 반영분 재검증 (2026-10-09, 완료)

- 최종 갱신: 2026-10-09 19:57 KST / 과제: audit-001 2차 반영분 재검증 / 상태: 완료(미푸시)
- 변경한 문서: 검증 보고 신규 1개 + `NEXT.md`·`CHANGELOG.md`·`PROGRESS.md` 갱신. 규칙 순증가 0줄
- 4종 게이트: 전부 통과. 게이트 1·2 전체 스캔 통과(09:54 최초, 19:55 재실행, 오탐 0건). 게이트 3 통과(변경 4문서의 §-참조 대조). 게이트 4 통과(CHANGELOG [Unreleased] 갱신). 조건부 게이트: ② README "상태·현재 한계" 대조 — 현실과 일치해 변경 불필요. ① workflows 대조·③ gates.md convention 대조 — 해당 문서를 건드리지 않아 미해당
- 독립 검토: dynamic-workflow 리뷰어 2명(각자 새 컨텍스트, 읽기 전용, `GLM-5.3-Flash$high`) — HIGH 2건 + 열거된 MEDIUM 3건 전부 **RESOLVED**, 규칙 약화 없음, 종합 **CLEAR**, 새 CRITICAL/HIGH 없음 (run `dwfrun-f4f2d763`, 1-페이즈, 커밋-핀 `git show` 판독). claude/codex CLI는 평일 08:00–18:00 호출 금지 조항과 크레딧·세션 상태 때문에 미사용(§7 우선순위대로 dynamic-workflow가 기본 경로)
- 도구로 확인한 근거: 리뷰어 2명의 판정 원문(항목별 file:line)을 캐시 재생으로 전문 회수해 보고 파일에 기록. 메인 세션이 convention L131–132·L104·L106·L113·L120–124, `workflows/README.md` L45를 표본 대조해 리뷰어 인용의 일치를 확인
- 이슈: 리뷰 워크플로가 호스트 큐 대기로 벽시시간 약 9시간 소요(디스패치 09:55 → 완료 19:44 KST). 실제 작업 시간과 구분되며, 스프린트 예산(50분) 초과분은 대기 시간이다. 이로 인해 스프린트 2 이후는 진행하지 않고 이번 세션은 wave 001 완료로 종료
- 유지보수: 없음 (과제 작업만 수행)
- 커밋: 브랜치 `feature/audit-001-reverify`에 미푸시 2커밋 — `4c6c4c6`(audit 보고) + progress 기록 커밋. push는 사용자 승인 대상
- 블로커: 없음. 다음 시도 조건: 없음
- 다음 실행의 첫 작업: `git fetch`로 origin/main 대조 후 §3.2-e 구현 후보 2(Traceability 검사 스크립트) 착수 — 이번 웨이브에서 수행 중

#### wave 001 스프린트 카드 (참고용 보존)

- 과제 ID: audit-001 2차 지적 반영분 재검증 (`NEXT.md` "진행 중 / 보류")
- 수용 조건 충족: 리뷰어 2명 항목별 RESOLVED + file:line 근거 ✅ / 규칙 약화 판단 확인(weakened=false 전 항목) ✅ / 검증 보고 `docs/audits/audit-verification-2026-10-09.md` 저장·`NEXT.md` 연결 ✅ / CHANGELOG [Unreleased] 기록 ✅ / 게이트 통과 후 커밋 ✅
- 규칙 순증가: 0줄 (기록 추가뿐)
- 검증 대상 커밋: `a33e74f`
