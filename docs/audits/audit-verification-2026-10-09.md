# Verification 001 — audit-001 2차 지적 반영분 재검증

- 일자: 2026-10-09
- 대상: 커밋 `a33e74f` (두 리뷰어 모두 `git show a33e74f:<경로>`로 커밋 고정 판독)
- 배경: audit-001(2026-10-02, `B_FINAL = FAIL`) 수정분에 대한 2차 검증(새 컨텍스트, FAIL — HIGH 2·MEDIUM 5)의 반영분이 재검증 없이 남아 있었다(`NEXT.md`). 반영 이후 규칙 단순화(`bfbe160`, 별도 2회 검증, 2차 PASS)와 audit-002(`bfbe160` 대상) 및 그 HIGH 수정분 검증(2차 PASS)이 같은 영역을 지나갔다. 따라서 이 검증의 질문은 "옛 반영 문구가 그대로 남아 있는가"가 아니라 **"원 2차 지적이 요구한 규칙이 현재 문서에서 충족되는가"**다
- 검증자: ZCode dynamic-workflow 서브에이전트 2명 (모델 `GLM-5.3-Flash`, reasoning level high, 읽기 전용, 각자 새 컨텍스트). 렌즈 1 = 규약 정합성(지적↔문구 대응 추적), 렌즈 2 = 약화·우회 시나리오 공격
- 판정 항목: HIGH 2건 + 원 보고에서 열거 가능한 MEDIUM 3건(STALE, 대리 기록, 범위 규칙) = 5건
- **결과: 5건 전부 RESOLVED, 규칙 약화 없음, 종합 CLEAR (리뷰어 2명 일치). 새 CRITICAL/HIGH 없음 (양측 newFindings 빈 배열)**
- 한계: 원 2차 보고가 저장되지 않아 MEDIUM 5건 중 열거된 3건만 판정했다(나머지 2건은 판정 불가). audit-001·audit-002의 미수정 항목과 `B_FINAL` 재판정은 범위 밖이다. 리뷰어 2명이 같은 모델 계열이므로 모델 편향은 상쇄되지 않는다. 줄 번호는 각 리뷰어가 `git show a33e74f:<경로>` 출력 기준으로 확인한 값이다 (메인 세션이 convention §5.3 L131–132, §5.1 L104·L106, §5.2 L113·L120–124, `workflows/README.md` L45를 표본 대조해 일치를 확인했다)
- 아래 본문은 두 리뷰어의 판정 원문이다 (요약·편집 없음)

## 원 2차 지적 목록 (`NEXT.md`가 유일한 기록)

- HIGH-1: 코드 변경 후 리뷰·승인 재판정 규칙 없음
- HIGH-2: gates.md 기록 주체 규칙 충돌
- MEDIUM 5건 중 열거된 3건: STALE 값 도입(MED-STALE), 메인 컨텍스트 대리 기록 규칙(MED-PROXY), 범위 규칙(MED-SCOPE)

---

## 규약 정합성 리뷰어 — 종합 CLEAR

### HIGH-1 — RESOLVED (약화 없음)

`git show a33e74f:docs/traceability-convention.md:131` — 판정 근거 커밋 이후 산출물 변경 시 재판정을 규정하고, 'IMPLEMENTATION_REVIEW_PASS, NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS, REQUIRED_TESTS_PASS, ACCEPTANCE는 REQ의 code·테스트 파일과 plan의 "변경할 파일"이 바뀐 경우도 같다' — 리뷰 Gate와 승인 Gate(ACCEPTANCE) 모두 코드 변경 후 재판정 의무가 생김. :132 — 확인 명령 'git diff --stat <근거 커밋> -- <해당 파일>'과 'git status --short -- <해당 파일>' 둘 다 점검(미커밋·미추적 파일 포함), '재판정이 필요한 Gate는 통과로 계산하지 않는다'. `workflows/README.md:45` — '승인 뒤에 승인 범위의 spec/plan/코드가 바뀌면 재확인이 필요하다 (convention §5.3)'. '변경할 파일'은 plan 형식의 실제 항목임을 확인(`MASTER_PROMPT.md:307`, §5.5 항목 2). §3:72 Review PASS 조건도 '유효(§5.2, §5.3)'로 재판정을 통과 조건에 결합.

### HIGH-2 — RESOLVED (약화 없음)

`docs/traceability-convention.md:113` '판정자 유형은 두 가지다'(USER :117, REVIEWER :118), :120-124 Gate별 허용 기록자 표 — APPROVAL_SPEC·APPROVAL_IMPLEMENTATION·ACCEPTANCE는 'USER만', PLAN_REVIEW_PASS·IMPLEMENTATION_REVIEW_PASS 등 6종은 'REVIEWER 또는 USER. 작성자가 쓴 줄은 무효', 나머지 Gate는 산출물 단계 컨텍스트이며 'IMPLEMENTATION_COMPLETE·REQUIRED_TESTS_PASS는 verify 컨텍스트가 기록하며 developer는 기록하지 않는다'. :109 'implement 단계의 developer는 gates.md를 수정하지 않는다'. 문서 간 모순 없음 확인: `workflows/README.md:44`(승인 3종 기록자 USER만, 방법은 §5.2 위임), :54(implement 행 'gates.md … 수정하지 않는다'), :55(verify 행 해당 2 Gate 줄만), :61(작성자가 쓴 리뷰 Gate 줄 무효), `docs/gates.md:4`(규칙 단일 출처는 convention §5, 이 파일은 기록만), `adapters/codex/README.md:10`(§5 가리킴, 복제 없음). 구 판정자 유형(AUTHOR/INDEPENDENT_REVIEWER) 줄은 `docs/gates.md:10` 이력 구역으로 격리되어 :106과 `docs/gates.md:7`에 따라 현재 값 계산에서 제외.

### MED-STALE — RESOLVED (약화 없음)

`docs/traceability-convention.md:104` — Gate 값 어휘 'true | false | STALE'. :106 — 이력 구역 구 형식 줄은 '읽을 수 있지만 통과로 계산하지 않는다(STALE과 같은 취급)', 현재 값은 기록 표 줄로만 결정. :132 — '재판정이 필요한 Gate는 통과로 계산하지 않는다. 눈에 보이게 하려면 값 STALE인 새 줄을 추가한다'. §3:72 Review PARTIAL에 '§5.3에 따라 재판정이 필요함'이 반영되어 재판정 필요 상태가 계산에도 드러남. 실제 사용례: `docs/gates.md:24-29` DISCOVERY_COMPLETE 등 6개 Gate에 STALE 줄 기록.

### MED-PROXY — RESOLVED (약화 없음)

`docs/traceability-convention.md:126` — '사용자와 대화하는 메인 컨텍스트(implement를 수행하는 동안은 제외)는 위 줄을 대신 적을 수 있다. 판정자 칸 끝에 (대리 기록)을 붙이고, 근거에 사용자 메시지 인용(USER) 또는 리뷰어가 저장한 결과 파일·사용자가 확인한 리뷰 보고(REVIEWER)를 적는다. 근거가 없으면 기록하지 않는다' — 대리 기록의 주체·예외·표시·근거 요건을 규정. 실제 기록이 이를 따름: `docs/gates.md:35` 'REVIEWER codex gpt-6.1-sol (대리 기록)' + 근거 '저장된 결과 파일 docs/audits/audit-002.md'. `workflows/README.md:44`가 '기록 방법(메시지 인용, 대리 기록)은 convention §5.2'로 위임해 이중 규정 없음.

### MED-SCOPE — RESOLVED (약화 없음)

`docs/traceability-convention.md:52`(§2) — '변경의 REQ 목록은 specs/<change-id>/spec.md가 선언하고, traceability.md는 그 REQ 전부의 항목을 가져야 한다. 항목이 없는 REQ는 MISSING이다'. §5.1:101 — '변경 단위: specs/<change-id>/gates.md (그 REQ의 traceability.md와 같은 폴더의 것만 읽는다). Gate는 change 폴더 단위로 범위(§2의 REQ 목록) 전체에 함께 적용한다. REQ마다 진행이 다르면 change를 나눈다', :102 — '프로젝트 단위(부트스트랩 등): docs/gates.md'. §5:95 TRACEABILITY_COMPLETE도 '범위 안의 모든 REQ'를 조건으로 삼아 범위 개념과 일치. 인용한 §2 참조는 실제로 존재(§2 링크 스키마 내 범위 항목, :52).

### 종합 요약

원 2차 지적(HIGH 2·MEDIUM 열거 3건)의 반영분을 커밋 a33e74f 기준으로 재검증한 결과 5건 전부 RESOLVED이고 규칙 약화 없음. HIGH-1은 convention §5.3이 리뷰·승인 Gate의 코드 변경 후 재판정 조건과 확인 명령을 규정하고 workflows/README.md:45가 승인 재확인을 연결하며, HIGH-2는 §5.2의 Gate별 허용 기록자 표가 단일 출처(convention §5)로 통합되어 문서 간 충돌이 남지 않았다. MED-STALE·MED-PROXY·MED-SCOPE도 각각 STALE 값 도입·대리 기록 근거 요건·범위 선언/Gate 적용 범위 규칙이 실제 기록(docs/gates.md)과 일치하게 존재한다. 검증에 사용한 5개 파일 외에 어댑터·MASTER_PROMPT §5.5·§5.7의 교차 참조도 확인했고 깨진 참조는 없었다(§0.10은 §0 목록 10번 항목으로 존재 확인). 이번 5건 반영으로 새로 생긴 CRITICAL/HIGH 모순은 없으며(구 형식 잔존 줄은 §5.1:106과 docs/gates.md 이력 구역으로 격리), 열거되지 않은 나머지 MEDIUM 2건은 원 보고가 저장되지 않아(NEXT.md:22가 'MEDIUM 5'와 3건의 반영 주제만 기록) 판정 불가다.

---

## 약화·우회 리뷰어 — 종합 CLEAR

### HIGH-1 — RESOLVED (약화 없음)

`docs/traceability-convention.md:131` 'IMPLEMENTATION_REVIEW_PASS, NO_UNRESOLVED_CRITICAL_REDTEAM_FINDINGS, REQUIRED_TESTS_PASS, ACCEPTANCE는 REQ의 code·테스트 파일과 plan의 "변경할 파일"이 바뀐 경우도 같다'; :132 확인 방법 'git diff --stat <근거 커밋>'과 'git status --short'(미추적 ?? 포함) 둘 다 + '재판정이 필요한 Gate는 통과로 계산하지 않는다'; :105 '그 Gate가 검토한 산출물(§5.3의 대상 파일)에 미커밋 변경이 있는 상태에서는 판정하지 않는다(그때 쓴 줄은 무효)'; :72 Review 차원 '§5.3에 따라 재판정이 필요함'=PARTIAL(→§4 IN PROGRESS, DONE 불가); `workflows/README.md:45` '승인 뒤에 승인 범위의 spec/plan/코드가 바뀌면 재확인이 필요하다 (convention §5.3)'. 우회 시나리오(리뷰 통과 뒤 코드 수정 후 무재판정 진행)는 STALE/재판정 필요 Gate 미인정(§5.3:132)→Review PARTIAL(:72)→TRACEABILITY_COMPLETE 불가(:95 '범위 안의 모든 REQ가 DONE')로 차단됨을 확인했다. 확인 명령: git show a33e74f:docs/traceability-convention.md | cat -n, git show a33e74f:workflows/README.md.

### HIGH-2 — RESOLVED (약화 없음)

`docs/traceability-convention.md:91-93` '§5. Gate 기록 규칙 (이 규약의 단일 출처)…다른 문서(workflows/README.md, 어댑터 등)는 이 절을 복제하지 않고 가리킨다'; :113-118 판정자 2유형(USER/REVIEWER) 표; :120-124 Gate별 허용 기록자 표 3행, :123 'REVIEWER 또는 USER. 작성자가 쓴 줄은 무효'; :108 '기록이 없거나 아래 판정자 규칙을 어긴 줄만 있으면 그 Gate는 UNKNOWN이다. 에이전트는 진행하지 않고'; :109 'implement 단계의 developer는 gates.md를 수정하지 않는다'; `workflows/README.md:3` 'Gate 기록 규칙(위치·형식·판정자·재판정)의 단일 출처는 docs/traceability-convention.md §5이다', :44 '기록자는 USER만이다. 기록 방법(메시지 인용, 대리 기록)은 convention §5.2', :61 '작성자가 쓴 리뷰 Gate 줄은 무효이고'. 우회 시나리오(작성자가 자기 리뷰 Gate 줄 직접 추가)는 :123 무효+:108 UNKNOWN→진행 금지로 차단. 교차 확인 실행: git show a33e74f:MASTER_PROMPT.md 및 adapters/codex·claude-code/README.md, workflows/{implement,verify,review-plan,review-implementation,converge}/README.md grep — 게이트 기록 주체에 관한 상충 규칙 없음(codex 어댑터:10-11은 §5를 가리킴, implement README:11·13은 verify 기록·gates.md 수정 금지로 일치).

### MED-STALE — RESOLVED (약화 없음)

`docs/traceability-convention.md:104` '값: true | false | STALE'; :106 '이력 구역: 규칙 단순화 이전의 구 형식 줄…통과로 계산하지 않는다(STALE과 같은 취급). 현재 값은 맨 아래 기록 표의 줄로만 정한다'; :132 '재판정이 필요한 Gate는 통과로 계산하지 않는다. 눈에 보이게 하려면 값 STALE인 새 줄을 추가한다'; `docs/gates.md:24-29` 이력 구역에 STALE 줄 실제 기록, :7 '이력 구역의 줄은 통과로 계산하지 않는다 (docs/traceability-convention.md §5.1)'. 보호(통과로 계산하지 않음)는 STALE 줄 추가와 무관하게 작동하므로 요구 본질(재판정 필요 상태가 계산에서 보이게)은 충족. 단순화 후 M-10 수정(git show 5d49335 diff 확인: 구 형식 줄 '기록된 값 그대로 인정'→'통과로 계산하지 않음')으로 오히려 엄격해짐.

### MED-PROXY — RESOLVED (약화 없음)

`docs/traceability-convention.md:126` '대리 기록: 사용자와 대화하는 메인 컨텍스트(implement를 수행하는 동안은 제외)는 위 줄을 대신 적을 수 있다. 판정자 칸 끝에 (대리 기록)을 붙이고, 근거에 사용자 메시지 인용(USER) 또는 리뷰어가 저장한 결과 파일·사용자가 확인한 리뷰 보고(REVIEWER)를 적는다. 근거가 없으면 기록하지 않는다'; :117 'AI는 승인을 추정해서 적지 않는다…사용자가 실제로 보낸 메시지를 근거 칸에 인용(일시·승인 범위 포함)할 때만'; `workflows/README.md:44` 대리 기록 방법을 §5.2로 가리킴. 우회 시나리오(대리 기록 형식으로 근거 없는 승인 흉내)는 :126 근거 없으면 기록 금지+:108 위반 줄만 있으면 UNKNOWN으로 차단(위조 자체의 사후 탐지 한계는 §5.4:136에 선언됨). `docs/gates.md:35` 'REVIEWER codex gpt-6.1-sol (대리 기록)' + 근거 '저장된 결과 파일 docs/audits/audit-002.md' — 실제 기록이 형식 준수.

### MED-SCOPE — RESOLVED (약화 없음)

`docs/traceability-convention.md:52` '범위: 변경의 REQ 목록은 specs/<change-id>/spec.md가 선언하고, traceability.md는 그 REQ 전부의 항목을 가져야 한다. 항목이 없는 REQ는 MISSING이다'; :101 '변경 단위: specs/<change-id>/gates.md (그 REQ의 traceability.md와 같은 폴더의 것만 읽는다). Gate는 change 폴더 단위로 범위(§2의 REQ 목록) 전체에 함께 적용한다. REQ마다 진행이 다르면 change를 나눈다'; :102 '프로젝트 단위(부트스트랩 등): docs/gates.md'; :95 TRACEABILITY_COMPLETE='범위 안의 모든 REQ가 DONE으로 계산되고'. 우회 시나리오(REQ 목록 일부만 선언)의 차단 근거: 선언 목록 전부 강제(:52)+implement는 '승인된 plan에 적힌 파일만'(`workflows/README.md:54`)+review-plan이 '누락·범위 확대'를 평가하고 CRITICAL/HIGH 미해결 시 IMPLEMENT 불가(`workflows/review-plan/README.md:8`, :13, 입력에 plan·spec·design)+이미 추적된 REQ의 파일 변경 시 §5.3으로 기존 Gate 줄 재판정 필요. 잔여 구멍(plan도 영향 REQ을 빠뜨리는 경우)은 §5.4:136이 선언한 한계이며 audit-002 H-01 수정분(git show 5d49335, 선언 REQ/AC/PERM/ERR 전부 강제, 2회 검증 PASS)이 재판정한 영역이라 새 모순으로 보지 않음.

### 종합 요약

5개 항목 모두 커밋 a33e74f 기준 규칙이 존재하고 원 지적이 요구한 행위를 실제로 규정하며, 우회 시나리오(리뷰 후 코드 무재판정 진행, 작성자 자기 Gate 줄 추가, REQ 목록 일부만 선언, 근거 없는 대리 기록)마다 문서 안의 차단 근거를 확인해 전부 RESOLVED, 약화 없음. 단순화(bfbe160)는 이 영역을 느슨하게 하지 않았고 이후 H-01·H-03·M-03·M-10 수정(5d49335)이 재판정 확인 방법과 이력 줄 처리를 오히려 강화했다. 새로 생긴 CRITICAL/HIGH 모순은 없다(CLEAR). 열거되지 않은 나머지 MEDIUM 2건은 원 보고가 저장되지 않아(NEXT.md 명시 한계) 판정 불가다.

---

## 새로 보고된 모순

없음 — 두 리뷰어 모두 newFindings가 빈 배열이었다.
