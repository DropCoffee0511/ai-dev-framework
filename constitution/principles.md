# Constitution — Principles

이 프로젝트에서 작업하는 모든 사람과 AI 에이전트가 지키는 최상위 원칙.
상세 규칙·Gate·형식의 **단일 출처는 `MASTER_PROMPT.md`** 이다. 이 문서는 그것을 복제하지 않고 가리킨다.

## 1. 핵심 공식

```text
아이디어 → 요구사항 → 업무흐름 → 상태 → 화면/API → 데이터 → 권한 → 예외 → 테스트 → 구현
구현 → 테스트 → 독립 리뷰 → 요구사항 대조 → 실제 사용자 검증
```

최우선 목표는 빠른 코드 생성이 아니라 **명세된 의도와 실제 프로그램 사이의 차이를 최소화하는 것**이다 (`MASTER_PROMPT.md` §25).

## 2. 원칙과 출처

| 원칙 | 출처 |
|---|---|
| 문서가 코드보다 먼저. 요구사항 없이 큰 기능을 구현하지 않는다 | MASTER_PROMPT §0 |
| "코드가 작성됨"은 "완료"가 아니다. 완료는 Definition of Done으로 판정한다 | §6 |
| Traceability가 비어 있으면 DONE이라고 보고하지 않는다 | §7, `docs/traceability-convention.md` |
| 구현자와 최종 검토자를 분리한다. 같은 컨텍스트가 자기 작업을 승인하지 않는다 | §0.7, §13 |
| 권한은 UI와 서버/API 양쪽에서 검사한다 | §9 |
| 핵심 업무 규칙·DB·인증·권한·결제·기술 스택은 사용자 승인 없이 바꾸지 않는다 | §0.10, §21 |
| 라이선스가 불명확하면 복사하지 않는다 | §15 |
| 사소한 선택은 `ASSUMPTION / IMPACT / REVERSIBLE`로 기록하고 진행한다 | §22 |

## 3. 우선순위

충돌 시 `MASTER_PROMPT.md` §14의 순서를 따른다.

```text
사용자의 현재 명시적 지시 > 승인된 spec/acceptance > constitution·MASTER_PROMPT > standards > adapter > AI의 선호
```

## 4. 개정 규칙

- 이 문서와 `MASTER_PROMPT.md`는 **사용자 승인 없이 에이전트가 수정하지 않는다.**
- 개정 시 변경 이유를 `CHANGELOG.md`에 기록한다.
- 하위 문서(`workflows/`, `adapters/`, `docs/`)가 상위 규칙과 어긋나면 하위 문서를 고친다.
