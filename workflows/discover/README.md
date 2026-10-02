# discover

규칙의 단일 출처: `MASTER_PROMPT.md` §5.1. 아래는 입출력과 Gate 색인이다. 규칙 본문은 해당 절이 우선한다.

| 항목 | 내용 |
|---|---|
| 담당 역할 | analyst |
| 목적 | 현재 프로젝트의 사실 파악 |
| 입력 | 저장소, 기존 문서, manifest, 빌드/테스트 명령 |
| 산출물 | `docs/discovery.md`, 위험·불확실성 목록, GREENFIELD/BROWNFIELD 판정 |
| Gate | `DISCOVERY_COMPLETE = true` |

BROWNFIELD이면 §3.2의 10개 절차를 따르고, `docs/`·`specs/` 초안은 **현재 구현에 근거해** 만든다. 기존 코드는 "자동으로 옳은 명세"가 아니며, 문서가 없다고 기존 동작을 제거하지 않는다. 자동화(`/project-discover`)는 `NEXT.md` 참조.
