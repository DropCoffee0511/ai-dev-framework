# specs

변경 단위(change-id)별 명세 폴더. 아직 비어 있다 (v0.1은 프레임워크 골격만 만든다).

```text
specs/<change-id>/
├─ spec.md            요구사항 (specify)
├─ acceptance.md      완료조건 AC-### (specify)
├─ design.md          설계 (design)
├─ plan.md            구현 계획 (plan)
├─ tasks.md           TASK-### (plan)
├─ test-plan.md       테스트 계획 (plan)
├─ traceability.md    링크와 상태 (docs/traceability-convention.md)
└─ review.md          독립 리뷰 결과 (review-plan, review-implementation)
```

- `<change-id>` 형식(가정): `NNN-short-name` (예: `001-user-login`). 확정되지 않았다.
- 파일을 만드는 단계와 Gate는 `workflows/README.md`를 따른다.
