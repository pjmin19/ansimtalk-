# 목표추진 프롬프트

<!-- chars:goal_propulsion_prompt=2308 -->
<!-- prompt:goal_propulsion -->
너는 AnsimTalk의 Codex for Open Source 합격 가능성을 높이는 구현 에이전트다. 목적은 작은 문구 수정이 아니라 “초기 채택이지만 관리 증거가 강한 public OSS maintainer case”를 완성하는 것이다.

최종 그림:
- README 첫 화면에서 application packet, automated review doc, evidence map, roadmap, validator를 바로 찾게 한다.
- repo는 early adoption risk를 숨기지 않는다. stars/downloads가 약한 대신 ecosystem importance, active maintenance, PR/issue/release/security/code-quality evidence로 설득한다.
- 앱 UI, PDF/report, docs, examples, form answers 어디에도 legal/forensic/emergency/disciplinary/guaranteed-safety authority처럼 보이는 표현을 남기지 않는다.
- 모든 주장은 local test, validator, GitHub Actions, PR/issue/release evidence 중 하나와 연결한다.

DTT 방식:
1. Define: OpenAI reviewer가 떨어뜨릴 위험을 한 문장으로 정의한다.
2. Test: 그 위험을 잡는 pytest/validator를 먼저 만든다.
3. Transform: 가장 작은 코드/문서 수정으로 테스트를 통과시킨다.

TDD 규칙:
- 새 claim이나 문구를 추가하기 전에 실패 조건을 먼저 validator에 넣는다.
- `PASS: Auto-Verified`, `PASS: Auto-Review-Ready`, `Human-Verified`, `submitted`, `accepted`를 절대 섞지 않는다.
- official form submit, provider change, training, customer-ready claim은 실제 수행 전 `NOT_PERFORMED`로 둔다.

마일스톤:
M8 Claim Boundary Hardening: 앱 템플릿과 report에서 법적 증거/법적 검증/확실한 증거/보장 표현 제거. `tests/test_public_claim_boundary.py`와 readiness validator가 회귀를 막아야 한다.
M9 Public Evidence Sync: README, evidence doc, readiness audit, PR #23 이후 main 상태를 일치시킨다.
M10 Submission Packet Freeze: 500자 이하 신청 답변을 최신 evidence로 다시 검수하고 char count를 테스트한다.
M11 External Review Bundle: Deep Research 20-file bundle과 prompt를 최신 main 기준으로 갱신한다.
M12 Owner Submission Gate: OpenAI Organization ID 등 owner-only 필드만 남긴 상태로 공식 제출 대기한다.

현재 실행 slice:
M8을 먼저 끝낸다. 이유는 submission docs가 “not legal authority”라고 말해도 app UI가 “법적증거 생성”이라고 보이면 자동심사/안전심사에서 바로 감점되기 때문이다.

필수 검증:
`python -m compileall -q .`
`python -m pytest -q`
`python scripts/check_oss_readiness.py --repo-root . --json-out D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST\ansimtalk_oss_readiness_goal_propulsion.v1.json`
`python scripts/check_codex_for_oss_application.py --repo-root . --json-out D:\Codex\reports\codex_for_oss_ansimtalk_readiness\LATEST\ansimtalk_codex_for_oss_goal_propulsion.v1.json`
`git diff --check`

완료 기준:
- unsafe legal/guaranteed authority phrases가 app/templates, docs, examples에서 검출되지 않는다.
- 목표추진 프롬프트는 4000자 이하이며 실제 character count가 파일에 기록된다.
- PR을 만들고 GitHub `test`와 `codeql`이 main에서 success가 될 때까지 확인한다.
<!-- /prompt:goal_propulsion -->
