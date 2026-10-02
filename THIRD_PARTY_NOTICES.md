# THIRD_PARTY_NOTICES

이 파일에는 **실제로 코드나 상당 부분을 가져온** 외부 항목만 기록한다 (`MASTER_PROMPT.md` §16).
아이디어만 참고한 프로젝트는 `REFERENCES.md`에 기록한다.

## 현재 상태 (2026-10-02)

**가져온 제3자 소스 코드·파일·텍스트: 없음.**

외부 프로젝트에서 가져온 코드·텍스트는 없다. (사용자가 제공한 원천 문서 — `MASTER_PROMPT.md`, `BOOTSTRAP.md`, `261002 대화내용.txt` — 와 표준 MIT 라이선스 본문은 제외한 판단이다.) 따라서 현재 제3자 배포 의무가 발생하는 항목이 없다.

## 기록 형식 (코드를 가져올 때 사용)

`MASTER_PROMPT.md` §16과 동일하다. 코드를 가져오기 **전에** 원 저장소의 최신 LICENSE를 확인하고(§15.3), 아래 항목을 채운다.

```text
## <Project Name>

Repository:
License:
Files/portions used:
Modifications:
Original copyright:
Reason for use:
```

## 사용 금지 정책 (재확인용 요약)

| 대상 | 정책 |
|---|---|
| Task Master | 소스 코드를 포함하지 않는다. dependency로도 포함하지 않는다. |
| BMAD Method | 명칭·상표·로고·브랜딩을 포함하지 않는다. |
| devloop | 아이디어 참고만. 코드를 가져오려면 Apache-2.0 고지 의무를 이 파일에 먼저 기록한다. |
| jasonkneen/kiro SDD | 대화록에서만 언급(`MASTER_PROMPT.md` §15.2에는 없음). 라이선스 `NEEDS LICENSE VERIFICATION`. 방법론 참고만 하며 코드·텍스트를 포함하지 않는다. |
| Amazon Kiro (제품) | 독점 제품. 방법론 참고만 하며 독점 프롬프트·에셋을 포함하지 않는다. |

## `NEEDS LICENSE VERIFICATION` (미검증 사항)

독립 감사(`docs/audits/audit-001.md`)가 확인하지 못한 사항이다. 추측하지 않고 열린 항목으로 둔다.

- 외부 9개 프로젝트의 라이선스 분류: 근거가 설계 대화록의 ChatGPT 답변뿐이고 원 출처가 보존되지 않음 (`REFERENCES.md`)
- `MASTER_PROMPT.md`, `BOOTSTRAP.md`, `261002 대화내용.txt`의 생성 경위와 권리 귀속, 그리고 이 저장소의 MIT 라이선스로 공개해도 되는지 (사용자 확인 필요)
- 단계 이름(specify, clarify, plan, constitution 등)이 GitHub Spec Kit의 용어와 같은 점 (일반적으로 개념·용어는 저작물이 아니라고 보나 확정하지 않음)
