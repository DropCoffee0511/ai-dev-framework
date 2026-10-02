# REFERENCES

아이디어·방법론만 참고한 외부 프로젝트 목록. **여기에 적힌 프로젝트의 코드는 이 저장소에 들어 있지 않다.**
(코드를 가져오면 `THIRD_PARTY_NOTICES.md`로 옮긴다 — `MASTER_PROMPT.md` §15·§16.)

라이선스 분류는 2026-10-02 설계 대화와 `MASTER_PROMPT.md` §15.2에 **기록된 내용**이다. 이번 부트스트랩에서 원 저장소 LICENSE를 다시 열어 확인하지 않았다. 코드를 재사용하기 전에 반드시 최신 LICENSE를 확인한다.

| 프로젝트 | 기록된 분류 | 참고한 개념 | 우리 쪽 구현 |
|---|---|---|---|
| GitHub Spec Kit | MIT | specify → plan → tasks → analyze → implement 흐름 | 독립 문서 계약 |
| OpenSpec | MIT | 변경 단위 spec lifecycle | `specs/<change-id>/` |
| cc-sdd | MIT | brownfield 사전 분석, 멀티 에이전트 지원 | `workflows/discover/` |
| Agent OS | MIT | 기존 코드에서 standards 추출 | `workflows/discover/` |
| Claude Code Spec Workflow | MIT | spec/bug 워크플로 | 참고만 |
| RIPER-5 | MIT 계열(기록) | 단계별 읽기/쓰기 권한 제한 | Gate 규칙 (독립 구현) |
| devloop | Apache-2.0 | 작성자와 reviewer 컨텍스트 분리, red-team 리뷰 | `workflows/review-*`, `workflows/red-team/` |
| BMAD Method | MIT + 상표 고지 | 역할별 에이전트 분리라는 일반 개념 | 일반 역할명만 사용 (상표 사용 안 함) |
| Task Master | MIT + Commons Clause | 작업 분해·의존성 그래프라는 일반 개념 | 독립 설계 (소스·dependency 미사용) |
| Kiro | 독점 제품(오픈소스 라이선스 분류 없음). `MASTER_PROMPT.md` §15.2에는 없고 설계 대화록에서만 언급 | 방법론 언급 | 참고만 (프롬프트·에셋 미포함) |
