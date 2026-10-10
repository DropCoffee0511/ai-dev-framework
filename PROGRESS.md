# PROGRESS — 자율 루프 진행 기록

상태의 기준 파일은 이 문서 하나다. 백로그는 `NEXT.md`, Gate 판정은 `docs/gates.md`이며 진행 상태를 여기서 따로 복제하지 않는다. 루프 규칙은 `AUTOPILOT.md`, 웨이브 기록 규약은 그 §8이다.

이 브랜치(`feature/traceability-script`, main `a33e74f` 기준)는 wave 002 전용이다. wave 001 기록은 `feature/audit-001-reverify` 브랜치(미푸시 2커밋)에서 이어 받아 아래 웨이브 기록에 보존했다.

## 최근 요약 (wave 002)

- 최종 갱신: 2026-10-09 20:52 KST
- 이번 과제: `NEXT.md` 구현 후보 2 — Traceability 검사 스크립트
- 상태: **구현 완료·독립 검토 대기** — 커밋 `3477dd6`(브랜치 `feature/traceability-script`), dynamic-workflow 리뷰 run `dwfrun-b216d5a7` 진행 중
- 변경한 문서: `scripts/check_traceability.py`(신규), `docs/traceability-convention.md`(도입 안내 1문장), `CHANGELOG.md`, `NEXT.md`, `README.md`, `AGENTS.md`, 이 파일. **규칙 순증가 2줄** (convention 안내 문장 + README 구조 목록 1줄 — 스프린트 카드 목표 ≤3줄 이내, 규칙 본문 변경 0)
- 4종 문서 게이트: 전부 통과(20:40경). 게이트 1·2 전체 스캔 위반 0건, 게이트 3 변경 6문서 §-참조 ↔ MASTER_PROMPT·convention 실제 섹션 대조 일치, 게이트 4 CHANGELOG [Unreleased] 갱신 확인. 조건부 게이트: ① workflows 미건드림(미해당) ② README 상태·한계 갱신 후 현실과 일치 ③ gates.md 판정 추가 없음(미해당)
- 스크립트 검증: `--self-test` 21건 전부 통과(종료 코드 0), 자기 저장소 적용 종료 코드 0 — `docs/gates.md`에서 `B_FINAL = false`(근거 커밋 bfbe160, 대리 기록 줄)를 판독하고 이력 구역 14줄을 현재 값에서 제외, 구조 위반 0건
- 독립 검토: dynamic-workflow(§7 기본 경로) 1-페이즈 — 결정적 게이트(`world.run`으로 self-test·자기 적용 재실행) + 읽기 전용 리뷰어 2명 병렬(규약 충실도 / 문서 일치, `GLM-5.3-Flash$high`, `git show 3477dd6` 커밋-핀 판독). claude/codex CLI는 미사용(dynamic-workflow가 기본 경로이며 평일 08:00–18:00 호출 금지 조항 유지)
- 커밋: `3477dd6` feat(traceability) — 미푸시. 웨이브 001 브랜치(`feature/audit-001-reverify`)의 미푸시 2커밋과 합쳐 저장소 전체 미푸시 3커밋 (push는 사용자 승인 대상)
- 다음 실행의 첫 작업: `dwfrun-b216d5a7` 판정 수신 → 지적 반영(REQUEST_CHANGES면 수정 후 재검토) → 본 기록 상태를 완료로 갱신. 검토 큐 대기는 wave 001 실측상 수 시간이 걸릴 수 있다(대기는 작업 시간이 아니다)

## 스프린트 카드 (wave 002)

- 과제 ID: `NEXT.md` 구현 후보 2 — "`docs/traceability-convention.md` §3–§5를 자동 계산. 입력은 Markdown/YAML"
- 문제: convention §3 차원 판정·§4 상태 계산·§5 Gate 기록 판독이 전부 수동이라 계산 누락·실수·우회가 가능하다 (`docs/discovery.md` R3의 하위 문제)
- 이번 결과: 단일 파일 스크립트(python3 표준 라이브러리만)가 traceability.md의 REQ별 차원·상태와 gates.md 기록의 현재 값을 계산하고, 내장 시험(--self-test)과 자기 저장소 적용으로 검증된다
- 범위: `scripts/check_traceability.py`(신규), `docs/traceability-convention.md`(도입 안내 1줄 포인터), `CHANGELOG.md`, `NEXT.md`, `README.md`·`AGENTS.md` 상태 문구 최소 갱신, 이 파일. 규칙 본문(convention §1–§7 내용)은 변경하지 않는다
- 규칙 순증가 목표: ≤3줄 → **실제 2줄** (convention 안내 문장, README 구조 목록. 규칙 추가 없음 — 스크립트는 규약의 계산기일 뿐이다)
- 불변식 영향(`AUTOPILOT.md` §2): 규칙 단일 출처 유지(스크립트가 규칙을 새로 정의하지 않고 convention §3–§5를 계산 — docstring에 명시), 최소 증가(실제 2줄), 템플릿·자기 기록 분리(`scripts/`는 양쪽 아님), 버전·이력 일치(CHANGELOG·README·AGENTS 갱신), 추적 가능성(`NEXT.md` 구현 후보 2와 연결)
- 수용 조건:
  1. 스크립트는 python3 표준 라이브러리만 쓰는 단일 파일이다 (외부 의존성·manifest 0) — ✅ import는 argparse·os·re·subprocess·sys·tempfile뿐
  2. `--self-test`가 §3 차원 판정(PASS/PARTIAL/MISSING)·§4 상태 계산(DONE/IN PROGRESS/NOT READY)·§5 기록 유효성(5칸, 값, 판정자 유형, 맨 아래 줄, 이력 구역 무시, STALE) 사례를 전부 통과한다 — ✅ 21건 전부 PASS(종료 코드 0)
  3. 자기 저장소 적용: 저장소 루트에서 실행해 `docs/gates.md` 기록 표를 판독하고(B_FINAL=false 유효 줄, 이력 구역 무시) 구조 위반 0건으로 종료한다 — ✅ B_FINAL=false 판독, 이력 14줄 제외, 위반 0건(종료 코드 0)
  4. 4종 문서 게이트 통과, `CHANGELOG.md`·`NEXT.md` 기록 갱신 후 작업 브랜치 커밋 (push는 승인 대상) — ✅ 커밋 `3477dd6`
  5. dynamic-workflow 독립 리뷰를 받는다 (지연 시 검토 대기 등재와 경로·상태 기록까지) — ⏳ run `dwfrun-b216d5a7` 진행 중
- 확인 수단: `--self-test` + 자기 저장소 실행 출력 + 4종 문서 게이트(`AUTOPILOT.md` §3.1) + dynamic-workflow 독립 리뷰어

## 웨이브 기록

### wave 002 — 구현 후보 2: Traceability 검사 스크립트 (2026-10-09, 구현 완료·검토 대기)

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
