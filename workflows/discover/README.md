# discover

규칙의 단일 출처: `MASTER_PROMPT.md` §5.1. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | analyst |
| 목적 | 현재 프로젝트의 사실 파악 |
| 입력 | 저장소, 기존 문서, manifest, 빌드/테스트 명령 |
| 산출물 | `docs/discovery.md`, 위험·불확실성 목록, GREENFIELD/BROWNFIELD 판정 |
| Gate | `DISCOVERY_COMPLETE = true` |

GREENFIELD이면 §5.1의 수행 목록을 따른다. BROWNFIELD이면 §3.2의 10개 절차를 `brownfield.md`의 절차(기준선 범위 판정 → 절차별 확인 대상·기록 위치 → 인벤토리·완료 확인 표)로 실행한다. 기존 코드는 "자동으로 옳은 명세"가 아니며, 문서가 없다고 기존 동작을 제거하지 않는다.

## 자동화 명령 `/project-discover` — 동작 정의 (초안)

이름은 예약돼 있고(`docs/discovery.md` 미결 #3), 동작 정의는 `NEXT.md` 구현 후보 3으로 아래에 둔다. **이름·동작의 확정과 어댑터 명령 등록은 사용자 결정 사항이다** (`NEXT.md`). 이 절은 동작을 정의할 뿐 명령을 등록하지 않는다.

| 항목 | 내용 |
|---|---|
| 목적 | 사용자가 새 저장소나 기존 저장소에서 "먼저 조사해 달라"고 할 때 discover 단계를 표준 절차로 수행한다 |
| 입력 | 대상 저장소, 사용자의 목적 설명(개선하려는 기능 등, 선택) |
| 수행 | ① §5.1의 수행 목록으로 저장소를 조사한다 ② §3.1·§3.2 기준으로 GREENFIELD/BROWNFIELD를 판정한다 ③ GREENFIELD는 §5.1 산출물로, BROWNFIELD는 `brownfield.md` 절차(0→10)로 진행한다 ④ 완료 확인 표를 채우고 `DISCOVERY_COMPLETE` Gate 줄을 기록한다 (판정자: 조사를 수행한 컨텍스트, convention §5.2) |
| 금지 | 코드 수정·dependency 변경 없음 (§5.1). 쓰기 허용 범위는 `workflows/README.md`의 discover 행을 따른다 |
| 종료 | 판정·기준선 범위 제안·위험·다음 단계(specify)를 사용자에게 보고하고 끝낸다. 사용자 답이 필요한 질문은 blocker로 모아 한 번에 묻는다 |
