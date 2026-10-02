# BOOTSTRAP.md
# AI Development Framework — First Run

이 저장소에서 작업을 시작하기 전에 루트의 `MASTER_PROMPT.md`를 전체 읽고 최상위 운영 규칙으로 적용하라.

## 첫 실행 목표

이번 실행의 목표는 **대규모 제품 구현이 아니라 프레임워크 v0.1의 안전한 기반을 만드는 것**이다.

다음 순서로 진행하라.

1. 현재 저장소와 git 상태를 조사한다.
2. GREENFIELD 또는 BROWNFIELD로 분류한다.
3. 기존 파일과 규칙을 보존해야 할 항목을 확인한다.
4. `MASTER_PROMPT.md`의 라이선스 정책을 적용한다.
5. 라이선스를 확인하지 않은 외부 코드를 복사하지 않는다.
6. 필요한 최소 폴더/문서 구조를 만든다.
7. `constitution/`, `docs/`, `specs/`, `workflows/`의 v0.1 골격을 만든다.
8. Traceability ID 규칙을 정의한다.
9. Claude Code와 Codex CLI가 같은 공통 문서를 읽도록 adapter 전략을 만든다.
10. 아직 큰 기능 구현은 하지 않는다.
11. 생성/수정한 파일과 남은 작업을 보고한다.

## 라이선스 관련 특별 금지

- Task Master 소스 코드를 복사하거나 핵심 dependency로 포함하지 않는다.
- BMAD/BMad 계열 상표를 프로젝트명·제품명·로고·마케팅에 사용하지 않는다.
- Apache-2.0/MIT 등 외부 코드를 직접 가져올 경우 provenance 및 필요한 고지를 기록한다.
- 라이선스가 불명확하면 복사하지 않고 독립 구현한다.

## 완료 조건

첫 실행 종료 시 최소한 다음을 확인하라.

```text
[ ] repository inspected
[ ] greenfield/brownfield classified
[ ] README/constitution strategy established
[ ] docs templates established
[ ] workflow skeleton established
[ ] traceability convention established
[ ] third-party/license policy established
[ ] Claude Code adapter plan established
[ ] Codex CLI adapter plan established
[ ] no restricted third-party source copied
```

마지막 보고 형식:

```text
## 현재 프로젝트 상태

## 생성/수정 파일

## 결정한 구조

## 라이선스 확인

## 위험/불확실성

## 다음 작업

## Gate 상태
```

`MASTER_PROMPT.md`와 충돌하는 행동은 하지 않는다.
