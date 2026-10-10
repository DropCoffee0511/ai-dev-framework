# wave 002 잔여 지적 흡수 재검토 보고 — 커밋 `4ba3c2c` (런 `dwfrun-76f40125`)

- 일시: 2026-10-11 01시경 KST 판정 수신
- 대상: 커밋 `4ba3c2c`(잔여 지적 15건 흡수) + `8b40410`·`2611d22`(기록)
- 경로: dynamic-workflow, 결정론적 게이트 선행 + 검증자 2명 병렬(수정 검증 / 규칙 무결성), `GLM-5.3-Flash$high`, 커밋-핀 `git show` 판독
- 종합 판정: **FAIL** — 미해소 0건, 규칙 약화 없음, **새 CRITICAL/HIGH 1건(verified, 검증자가 실행으로 재현)**. 수정 검증 CONCERNS / 규칙 무결성 CLEAR

## 지적 15건에 대한 판정

잔여 지적 15건(N1·R1 HIGH, N2·N3·R2·R3 medium, R4~R8 LOW, EXTRA-1~4)에 대해 수정 검증자·규칙 무결성 검증자 모두 **15/15 RESOLVED**로 판정했다. 규칙 무결성 검증자는 규칙·템플릿 문서 변경 0줄, ADOPTING.md 1줄 추가의 근거 기록, 커밋 범위 청결(금지 파일 미스테이징), 기록 주장(self-test 건수·위반 0건·규칙 순증가 1줄) 일치를 확인해 CLEAR였다.

- 결정론적 게이트: `--self-test` exit 0(44건), 자기 저장소 적용 exit 0

## 새 지적 (HIGH, verified)

- 위치: `scripts/check_traceability.py:218` (커밋 `4ba3c2c`)
- 문제: 케이스 목록 헤더 판정 `cells[0] == 'ID' or any('대상' in c for c in cells)`이 데이터 행도 헤더로 오판한다 — 임의 칸에 '대상'이 포함된 TC 행은 결과 집계에서 탈락해 실행 PASS인 TC가 NOT RUN→Tests PARTIAL로 REQ가 DONE으로 계산되지 않고, `tc_target_col`이 그 행 기준으로 어긋나 이후 행들의 대상 칸도 잘못 읽는다(모두 비고 없이 침묵).
- 재현(검증자 실행): 절차 칸 '대상 화면 진입 후 입력'인 TC-001 행 → `tc_target_col=3`, `tc_result`에서 TC-001 누락, `effective_tc_result('TC-001')=NOT RUN` (정상 통제 행은 col=2로 정상 파싱)

## 처리 (본 보고와 같은 커밋 이후의 fix 커밋)

- 헤더 판정을 **첫 칸이 정확히 'ID'인 행**으로 한정했다. 데이터 행의 절차 칸에 '대상'이라는 말이 들어 있어도 헤더로 오판하지 않는다.
- self-test 사례 11을 추가했다(44건→47건): 절차 칸에 '대상'이 있어도 REQ-001 DONE 유지·TC-001 결과 집계 유지·대상 칸 위치(col=2) 유지 3건.
- 수정 후 NEW-1 시나리오 재현 확인: REQ-001 = DONE, `tc_target_col = 2`, 구조 위반 0건.
- 2차 재검토를 수정 커밋 대상으로 접수한다(런 ID는 `PROGRESS.md` wave 002 기록에 남긴다).

## 전문에 관하여

항목별 판정 표 전문은 런 아티팩트(`reverify-report`, 런 `dwfrun-76f40125`)에 보존되어 있다. 전문 회수는 검증자 재실행 비용(약 100만 토큰)을 요구하므로, 이 보고는 워크플로 반환값·보고 항목에서 작성했음을 명시한다 (`docs/audits/wave002-reverify-2026-10-10.md`와 같은 전례).

## 부록 — 2차 재검토의 RECORDS 항 종결: 반환값 직접 대조 (2026-10-11, 메인 세션 대리 기록)

2차 재검토(런 `dwfrun-12ca5a04`)의 규칙 무결성 검증자는 이 세션에서 런 아카이브 접근이 불가해(`workflow_introspection_unavailable`) 본 보고와 1차 런 반환값의 직접 대조를 못 했다(RECORDS·PARTIAL — 그 외 간접 근거는 전부 확인했다고 보고). 검증자가 제시한 방법("런 아카이브에 접근 가능한 세션에서 대조")대로 메인 세션이 보관 중인 1차 런 `dwfrun-76f40125` 반환값과 본 보고를 항목별로 대조한 결과 **종합 FAIL·미해소 0건·규칙 약화 없음·수정 검증 CONCERNS/무결성 CLEAR·15/15 RESOLVED·self-test 44건·NEW-1 내용과 재현 상세 — 전부 일치**했다. 대조표 전문은 `docs/audits/wave002-residual-reverify2-2026-10-11.md`에 있다. 이로 RECORDS 항은 닫히고 wave 002 잔여 지적 흡수는 완결된다.
