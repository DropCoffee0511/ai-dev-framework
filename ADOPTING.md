# ADOPTING — 이 프레임워크를 다른 프로젝트에 적용하기

이 저장소에는 **규칙 모음**과 **이 저장소 자신의 기록**이 함께 있다. 대상 프로젝트에는 아래 §1의 "복사함"만 가져가고, **목록에 없는 파일은 가져가지 않는다.** 이 저장소를 그대로 앱 저장소로 쓰지 않는다. 이 저장소의 Gate 기록(`B_FINAL = false` 등)이 섞여 들어가면 에이전트가 이를 대상 프로젝트의 상태로 오해할 수 있다.

## 1. 가져갈 것 / 만들 것 / 가져가지 않을 것

| 구분 | 파일 |
|---|---|
| 복사함 | `MASTER_PROMPT.md`, `constitution/principles.md`, `workflows/` 전체, `docs/01_product.md`~`docs/10_release_checklist.md`, `docs/traceability-convention.md`, `specs/README.md`, `scripts/check_traceability.py`, `adapters/README.md`와 쓰는 도구의 `adapters/<도구>/README.md` |
| 대상이 자기 것으로 만듦 | `docs/discovery.md` (discover 단계 산출물), `docs/gates.md` (첫 Gate를 기록할 때 만든다. 형식은 `docs/traceability-convention.md` §5.1. 없으면 모든 Gate는 `UNKNOWN`), `NEXT.md`, `THIRD_PARTY_NOTICES.md`, `CHANGELOG.md`. `NEXT.md`·`THIRD_PARTY_NOTICES.md`·`CHANGELOG.md`가 이미 있으면 새로 만들지 않고 기존 파일에 이어서 쓴다 (같은 용도일 때만. §4의 3번) |
| 가져가지 않음 | `ADOPTING.md`, `BOOTSTRAP.md`, `README.md`, `LICENSE`, `REFERENCES.md`, `CLAUDE.md`, `AGENTS.md`, `docs/audits/`, 이 저장소의 `docs/discovery.md`·`docs/gates.md`·`NEXT.md`·`CHANGELOG.md`·`THIRD_PARTY_NOTICES.md`, `261002 대화내용.txt`, `.gitignore` |

## 2. 진입 파일 (`CLAUDE.md` / `AGENTS.md`)

이 저장소의 `CLAUDE.md`·`AGENTS.md`는 이 저장소 전용 내용이 있어 복사하지 않는다. 대상의 진입 파일에 아래 블록을 넣는다. 파일이 이미 있으면 **끝에 추가**하고 기존 내용은 보존한다. Claude Code는 `@MASTER_PROMPT.md` 줄을 쓰고, Codex CLI 등 import가 없는 도구는 그 줄을 뺀다.

```text
## ai-dev-framework
이 저장소는 ai-dev-framework 규칙을 따른다. 규칙은 이 파일에 복사하지 않고 아래 파일을 가리킨다.
@MASTER_PROMPT.md
작업 전에 전체 읽을 파일: MASTER_PROMPT.md, constitution/principles.md, docs/discovery.md (없으면 discover 단계에서 만든다), workflows/README.md, docs/traceability-convention.md, docs/gates.md (없으면 모든 Gate는 UNKNOWN), NEXT.md (없으면 새로 만든다)
이 규칙집이 자기 v0.1을 구축하는 절차(MASTER_PROMPT.md §19·§24의 "이 저장소", workflows/README.md의 부트스트랩 절, B_FINAL, BOOTSTRAP.md)는 이 프로젝트에 적용하지 않는다. 이는 규칙 변경이 아니라 적용 범위 안내이며, §23의 조사·판정은 discover 단계가 수행한다.
이 규칙과 이 파일의 다른 규칙이 충돌하면 MASTER_PROMPT.md §14의 우선순위를 확인하고, 그래도 정해지지 않으면 docs/discovery.md의 충돌 목록에 기록해 사용자에게 묻는다.
```

## 3. Greenfield (새 프로젝트)

1. 새 저장소를 만든다. 이 프레임워크 저장소(§5의 URL)는 clone해 둔다.
2. §1의 "복사함"을 clone한 프레임워크 저장소에서 복사하고 §2 블록으로 진입 파일을 만든다.
3. 자기 `LICENSE`를 만든다 (이 프레임워크의 `LICENSE`를 복사하지 않는다).
4. §5대로 출처를 기록한다.
5. discover를 시작한다: `docs/discovery.md`에 `GREENFIELD` 판정을 적는다 (`workflows/discover/README.md`). 이후 `workflows/README.md`의 Gate 순서를 따른다.

## 4. Brownfield (기존 프로젝트)

1. **새 브랜치**에서만 작업한다. 소스 코드는 수정하지 않고, 기존 파일은 3번의 예외 외에는 수정하지 않는다.
2. 복사 전에 "복사할 파일 목록"과 "이미 있는 같은 이름 파일 목록"을 사용자에게 보여주고 승인받는다.
3. 같은 이름의 기존 파일이 있으면 **덮어쓰지 않고 `BLOCKED`로 보고**하고 사용자 결정을 기다린다 (예: 이미 있는 `docs/01_product.md`, `workflows/`, 다른 용도의 `docs/discovery.md`). 예외(끝에 추가만 허용): `CLAUDE.md`·`AGENTS.md`(§2 블록), 같은 용도의 `NEXT.md`·`CHANGELOG.md`·`THIRD_PARTY_NOTICES.md`. 다른 용도로 쓰이는 파일이면 예외가 아니라 `BLOCKED`다.
4. 복사분은 사용자가 허락하면 소스 변경과 분리된 별도 커밋으로 만든다.
5. discover를 수행해 `docs/discovery.md`에 다음을 적는다: `BROWNFIELD` 판정, `MASTER_PROMPT.md` §3.2의 조사 결과, 기존 규칙과 `MASTER_PROMPT.md`의 **충돌 목록**(§23), 조사 **기준선**(시스템 전체인지 이번 변경 대상 범위인지. 사용자에게 확인받고 그 답을 인용해 적는다).
6. 문서가 없다는 이유로 기존 동작을 제거하지 않는다 (`MASTER_PROMPT.md` §3.2).

## 5. 출처·라이선스

대상의 `LICENSE`는 덮어쓰지 않는다. 프레임워크 파일을 복사했으면 대상의 `THIRD_PARTY_NOTICES.md`에 `MASTER_PROMPT.md` §16 형식으로 기록한다.

- Project Name: `ai-dev-framework` (작업명, 확정 아님)
- Repository: `https://github.com/DropCoffee0511/ai-dev-framework`
- License: MIT
- Files/portions used: 복사한 파일 목록, Modifications: 있으면 적는다, Reason for use: 이 프레임워크의 규칙을 사용하기 위해
- Original copyright: `Copyright (c) 2026 ai-dev-framework contributors`. MIT 허가문(프레임워크 `LICENSE`의 본문)도 함께 넣는다
- **복사한 프레임워크 커밋 해시**: 프레임워크 저장소에서 `git rev-parse HEAD`로 얻은, GitHub에 올라간(push된) 커밋이다. 나중에 새 버전과 비교하는 기준이다
- 프레임워크의 `THIRD_PARTY_NOTICES.md`에는 `MASTER_PROMPT.md` 등의 권리 귀속이 `NEEDS LICENSE VERIFICATION`으로 남아 있다. 대상 프로젝트를 공개·배포하기 전에 확인한다

## 6. 적용 확인 (수동)

- [ ] §1 "복사함"이 모두 있고, "가져가지 않음"에 있는 프레임워크 쪽 파일의 내용은 들어 있지 않다
- [ ] 진입 파일에 §2 블록이 있고 기존 내용이 보존되어 있다 (`git diff`에 삭제된 줄이 없다)
- [ ] 대상의 `LICENSE`와 소스 코드가 바뀌지 않았다
- [ ] `THIRD_PARTY_NOTICES.md`에 프레임워크 고지와 커밋 해시가 있다
- [ ] `docs/discovery.md`가 있고 판정(GREENFIELD/BROWNFIELD)이 적혀 있다. Brownfield는 충돌 목록과 기준선도 있다
- [ ] 사용자에게 현재 상태와 다음 단계를 보고했다

## 7. 한계

- 복사한 문서 안의 프레임워크 자체 기록 참조는 대상 프로젝트에 대응하는 기록이 없다 (예: `docs/discovery.md` A4·R4, `docs/gates.md`의 "이력 구역", `NEXT.md`가 가리키는 프레임워크의 결정 사항). 부트스트랩 관련 부분은 §2 블록대로 적용하지 않는다.
- 프레임워크 새 버전을 반영하는 자동 절차가 없다 (기록한 커밋 해시와 `git diff`로 수동 비교).
- 자동 검사가 없고, 이 절차는 아직 실제 프로젝트에 적용해 시험하지 않았다 (`NEXT.md`의 Self Test).
- 이 저장소의 `docs/`에는 자체 기록이 템플릿과 함께 있다. 구분은 위 §1의 목록으로만 한다. 물리적 분리는 `NEXT.md`의 결정 사항이다.
