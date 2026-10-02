# Gate Record (project level)

이 프로젝트 자체(프레임워크 부트스트랩)의 Gate 판정 기록. 변경 단위의 Gate는 `specs/<change-id>/gates.md`에 같은 형식으로 기록한다.
기록 규칙의 단일 출처는 `docs/traceability-convention.md` §5이다. 이 파일은 **기록만** 담는다.

## 규칙 요약 (원문은 convention §5)

- **append-only**: 기존 줄을 수정·삭제하지 않는다. 값을 바꾸려면 새 줄을 추가한다. 같은 Gate의 **가장 아래 줄**이 현재 값이다.
- 판정자 유형은 `USER` / `INDEPENDENT_REVIEWER` / `AUTHOR`. Gate마다 허용되는 유형이 다르다(convention §5). 허용되지 않은 유형이 쓴 줄은 **무효**이며 그 Gate는 `UNKNOWN`으로 본다.
- implement 단계의 developer는 이 파일을 수정하지 않는다.
- 값은 `true | false | STALE`. `STALE`은 판정 이후 관련 산출물이 바뀌어 **재판정이 필요**하다는 뜻이며 통과로 계산하지 않는다 (convention §5.3).
- 메인 세션이 서브에이전트의 판정을 대신 적은 줄은 비고에 `대리 기록`이라고 적는다 (`workflows/README.md`).
- **현재 값 요약** (가장 아래 줄 기준): `B_FINAL = false`, `B0~B4`와 `DISCOVERY_COMPLETE`는 `STALE`. 이 요약은 편의용이며 아래 표가 원본이다.

## 기록

| 일시 | Gate | 값 | 판정자 유형 | 판정자 | 판정 기준 | 근거 | 비고 |
|---|---|---|---|---|---|---|---|
| 2026-10-02 | DISCOVERY_COMPLETE | true | AUTHOR | claude-code 세션 | 커밋 전 작업 트리 | `docs/discovery.md` | 자기 판정 |
| 2026-10-02 | B0_INSPECTED | true | AUTHOR | claude-code 세션 | `4d3d32c` | `docs/discovery.md` | 자기 판정 |
| 2026-10-02 | B1_FOUNDATION | true | AUTHOR | claude-code 세션 | `4d3d32c` | README, LICENSE 등 | 자기 판정 |
| 2026-10-02 | B2_WORKFLOW | true | AUTHOR | claude-code 세션 | `4d3d32c` | `workflows/` | 자기 판정. audit-001 H1이 "Gate 통과 조건 미정의"를 지적 |
| 2026-10-02 | B3_TRACEABILITY | true | AUTHOR | claude-code 세션 | `4d3d32c` | `docs/traceability-convention.md` | 자기 판정. audit-001 H8이 "계산된 DONE ≠ DoD"를 지적 |
| 2026-10-02 | B4_ADAPTERS | true | AUTHOR | claude-code 세션 | `4d3d32c` | `adapters/`, `AGENTS.md`, `CLAUDE.md` | 자기 판정 |
| 2026-10-02 | B_FINAL | true | INDEPENDENT_REVIEWER | claude-code critic 서브에이전트(새 컨텍스트) | 커밋 전 작업 트리 | 서브에이전트 보고(저장된 파일 없음) | 대리 기록(메인 세션). 검토 범위가 좁았음(7개 항목). 아래 감사로 **대체됨**. 파일 근거가 없는 줄이므로 이 줄만으로는 근거가 약함 |
| 2026-10-02 | B_FINAL | false | INDEPENDENT_REVIEWER | claude-code architect 서브에이전트(새 컨텍스트) | `b9c8c61` | `docs/audits/audit-001.md` | 대리 기록(메인 세션이 서브에이전트 보고를 요약해 파일로 저장). CRITICAL 3, HIGH 9. 첫 줄의 true를 대체 |
| 이 줄과 같은 커밋 | DISCOVERY_COMPLETE | STALE | AUTHOR | claude-code 세션 | 이 줄과 같은 커밋 | `docs/discovery.md` | 판정 이후 `docs/discovery.md`가 수정됨 (convention §5.3). 재판정 필요 |
| 이 줄과 같은 커밋 | B0_INSPECTED | STALE | AUTHOR | claude-code 세션 | 이 줄과 같은 커밋 | `docs/discovery.md` | 위와 같음 |
| 이 줄과 같은 커밋 | B1_FOUNDATION | STALE | AUTHOR | claude-code 세션 | 이 줄과 같은 커밋 | `README.md`, `LICENSE`, `THIRD_PARTY_NOTICES.md`, `REFERENCES.md`, `constitution/principles.md`, `docs/01_product.md`~`docs/10_release_checklist.md` | `THIRD_PARTY_NOTICES.md`, `REFERENCES.md`, `docs/09_test_cases.md`, `docs/10_release_checklist.md`가 수정됨 |
| 이 줄과 같은 커밋 | B2_WORKFLOW | STALE | AUTHOR | claude-code 세션 | 이 줄과 같은 커밋 | `workflows/` | `workflows/**`가 수정됨 |
| 이 줄과 같은 커밋 | B3_TRACEABILITY | STALE | AUTHOR | claude-code 세션 | 이 줄과 같은 커밋 | `docs/traceability-convention.md` | 수정됨 |
| 이 줄과 같은 커밋 | B4_ADAPTERS | STALE | AUTHOR | claude-code 세션 | 이 줄과 같은 커밋 | `adapters/`, `AGENTS.md`, `CLAUDE.md` | `adapters/codex/README.md`, `AGENTS.md`, `CLAUDE.md`가 수정됨 |
