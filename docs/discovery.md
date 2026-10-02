# Discovery — v0.1 Bootstrap (Phase 0)

- Date: 2026-10-02
- Scope: 이 저장소의 현재 사실 조사. 구현·리팩터링·dependency 변경 없음 (MASTER_PROMPT §5.1).
- Rule source: `MASTER_PROMPT.md` (최상위), `BOOTSTRAP.md` (첫 실행 지시)

## 1. 판정

**GREENFIELD.**

근거 (MASTER_PROMPT §3.1 / §3.2 기준):

| 확인 항목 | 결과 |
|---|---|
| `src`, `app`, `packages`, `server`, `client` | 없음 |
| package manifest (`package.json`, `pyproject.toml` 등) | 없음 |
| DB migration / schema | 없음 |
| 테스트 | 없음 |
| 실행 가능한 기능 | 없음 |
| 조사 시작 시점 git 저장소 여부 | 아님 (`fatal: not a git repository`) → 사용자 승인 후 `git init -b main` 실행, 커밋 없음 |
| 사용자의 명시 | "v0.1 구축 시작" — 새 프로젝트 |

## 2. 조사 시작 시점의 파일 (보존 대상)

| 파일 | 성격 | 처리 |
|---|---|---|
| `261002 대화내용.txt` | 설계 대화록 (ChatGPT). 요구사항의 **원천 기록**, 규범 문서 아님 | 수정·삭제 금지. 문서 인용 시 `:chatgpt-content-reference{…}` 같은 표식은 가져오지 않는다 |
| `BOOTSTRAP.md` | 사용자 제공 첫 실행 지시 | 수정 금지 |
| `MASTER_PROMPT.md` | 최상위 운영 규칙 (0.1-draft) | 수정 금지. 변경 필요 시 사용자 승인 후 별도 변경으로 처리 |
| `CLAUDE.md` | 이 세션 초반에 `/init`으로 생성된 Claude Code용 파일 | 아래 §3 충돌로 인해 **포인터 파일로 재작성** (사용자 승인 받음) |

디렉터리 이름은 `ai-dev-framwork`(철자 "framework"에서 `e` 누락)이다. **이름 변경은 대규모 재구성(MASTER_PROMPT §21)에 해당하므로 하지 않는다.** 문서 안의 프로젝트 이름은 아래 §5 가정을 따른다.

## 3. 기존 규칙과 MASTER_PROMPT의 충돌

충돌 우선순위는 MASTER_PROMPT §14를 따른다 (agent-specific adapter는 `constitution / MASTER_PROMPT`보다 아래).

| # | 기존 `CLAUDE.md`의 내용 | MASTER_PROMPT | 해결 |
|---|---|---|---|
| C1 | "파일은 대화록 하나뿐" | 이제 `BOOTSTRAP.md`, `MASTER_PROMPT.md`도 존재 | `CLAUDE.md` 재작성 시 제거 |
| C2 | Spec Kit Extension/Preset을 **"확정"** 결정으로 서술 | §15.2: "가능하면 extension/preset/workflow 방식 **우선**" (선호이지 확정 아님) | 확정 표현 폐기. `docs/01_product.md`에 "선호, 미확정"으로 기록 |
| C3 | 미결 8개 항목을 "사용자 확인 없이 결정하지 말 것"으로 일괄 금지 | §22: 사소한 선택은 `ASSUMPTION / IMPACT / REVERSIBLE`로 기록하고 진행. 핵심 업무 정책·돈 계산·인증/권한·개인정보·파괴적 migration·라이선스 불명 코드만 임의 확정 금지 | `CLAUDE.md`의 일괄 금지 문구 폐기. 아래 §5에서 항목별로 분류 |
| C4 | 계획 구조에 `agents/`, `standards/`, `src/` 등 전체 나열 | §12: "빈 디렉터리를 무의미하게 모두 만들 필요 없다" | 필요한 최소 구조부터 생성 |
| C5 | 라이선스 표에 대화록의 Spec Kit/OpenSpec 등 저작권 표기 예시를 그대로 옮김 | §16: `THIRD_PARTY_NOTICES.md`에는 **실제로 코드를 가져온 항목만** | 현재 가져온 코드 없음 → "없음"으로 기록 |

그 밖의 충돌은 발견하지 못했다.

## 4. 라이선스 조사 (이번 실행)

- 이번 실행에서 **외부 저장소의 소스 코드·텍스트를 복사하지 않았다.** 외부 프로젝트는 Methodology Reference(MASTER_PROMPT §15.1-A)로만 다룬다.
- 외부 프로젝트의 라이선스 분류는 `MASTER_PROMPT.md §15.2`와 대화록에 2026-10-02 기준으로 **기록된 내용**이며, 이번 실행에서 원 저장소의 LICENSE 파일을 **다시 열어 확인하지 않았다.** 코드 재사용이 필요해지는 시점에 원 저장소의 최신 LICENSE를 확인해야 한다(§15.3).
- 제한 대상: Task Master(소스·dependency 금지), BMAD/BMad(명칭·상표 금지). 이 이름들은 프로젝트명·역할명·워크플로 이름에 쓰지 않는다.

## 5. 가정 (ASSUMPTION / IMPACT / REVERSIBLE)

| ID | ASSUMPTION | IMPACT | REVERSIBLE |
|---|---|---|---|
| A1 | 프로젝트 작업명은 `ai-dev-framework` (확정된 이름 아님). 디렉터리 철자 오류는 그대로 둔다 | 문서 제목·LICENSE 문구에만 영향 | YES |
| A2 | 저작권자 표기는 `ai-dev-framework contributors` (사용자 선택) | LICENSE 한 줄 | YES |
| A3 | `docs/01_product.md ~ 10_release_checklist.md`는 **이 프레임워크를 쓰는 프로젝트가 채울 템플릿**이다 (MASTER_PROMPT §19 Phase 1의 문면 해석). 이 저장소 자체의 제품 문서가 아님 | 문서 내용이 "작성 안내 + 빈 칸" 형태가 됨. 단 `docs/discovery.md`와 이 프레임워크 자체의 정의는 이 저장소의 실문서 | YES |
| A4 | v0.1의 Traceability는 Markdown/YAML **명세**까지. 검사 스크립트는 구현에 해당하므로 별도 계획·리뷰 Gate를 거쳐 `NEXT.md`로 이월 | Phase 3 산출물이 규칙 문서 | YES |
| A5 | Phase 5(Self Test)는 이번 실행 범위 밖. `NEXT.md`에 기록 | BOOTSTRAP 완료 조건에 Phase 5 항목이 없음 | YES |
| A6 | Spec Kit 연동 방식(extension / preset / 독립 CLI)은 **미결**로 둔다. v0.1은 어느 쪽에도 종속되지 않는 Markdown 계약만 정의 | 어댑터가 얇은 이유 | YES |

### 미결 항목 분류 (대화록 §"결정해야 할 부분" 8개)

| # | 항목 | 분류 | 상태 |
|---|---|---|---|
| 1 | 프로젝트 이름 | 사용자 결정 (법적·브랜드) | 작업명 A1로 진행, **미결** |
| 2 | Spec Kit과의 관계 | 아키텍처 | A6, **미결** (선호: extension/preset) |
| 3 | CLI 명령어 체계 | 사용자 UX | v0.1은 `/init`, `/project-discover`, `/feature`를 **이름만 예약**(대화록 §9). 동작 정의는 `NEXT.md` |
| 4 | Claude/Codex/Gemini 공통 규격 | 아키텍처 | 공통 규칙은 파일(`MASTER_PROMPT.md`, `constitution/`, `docs/`, `specs/`), 에이전트별 파일은 adapter (§14) |
| 5 | 문서 포맷 | 아키텍처 | Markdown + 최소 YAML front matter (`docs/traceability-convention.md`) |
| 6 | Traceability 저장 방식 | 아키텍처 | Markdown/YAML (A4) |
| 7 | Gate 시스템 구현 방식 | 아키텍처 | v0.1은 문서화된 Gate 이름과 판정 규칙까지. 자동 강제는 `NEXT.md` |
| 8 | Brownfield 분석 방식 | 아키텍처 | `workflows/discover/`에 절차 정의. 자동화는 `NEXT.md` |

## 6. 위험·불확실성

| ID | 내용 | 심각도 |
|---|---|---|
| R1 | MASTER_PROMPT 버전이 `0.1-draft`. 이후 개정 시 하위 문서가 어긋날 수 있음 → 하위 문서는 MASTER_PROMPT를 **복제하지 않고 참조**한다 | MEDIUM |
| R2 | 외부 라이선스 분류가 이번에 재확인되지 않음(§4) | LOW (코드 미사용) |
| R3 | 자동 Gate 강제가 없어 v0.1의 Gate는 "에이전트가 규칙을 따른다"에 의존 | MEDIUM — `NEXT.md` 1순위 |
| R4 | `/init`·`/feature` 같은 이름이 Claude Code 내장 명령과 충돌할 수 있음 (`/init`은 이미 내장) | LOW — 이름 예약만 하고 확정 보류 |

## 7. Gate

```text
DISCOVERY_COMPLETE = true
```

조건 충족 근거: GREENFIELD 판정 및 근거(§1), 보존 목록(§2), 충돌 목록과 해결(§3), 라이선스 처리(§4), 가정(§5), 위험(§6) 기록.

이 Gate 판정은 자기 판정이다. 전체 부트스트랩 종료 시 독립 reviewer의 검토를 받는다.
