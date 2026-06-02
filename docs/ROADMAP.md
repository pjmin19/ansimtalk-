# Roadmap

This roadmap uses DTT milestones and TDD-style acceptance checks.

## M0 Security Blocker

Red condition: secret-like values, hardcoded credential fallbacks, real API keys,
client-supplied PDF file paths, or deploy-mode missing `SECRET_KEY` appear in
public behavior.

Green condition: config is env-only, `.env.example` has placeholders, secret
rotation is documented, client path fields are rejected, deployed multi-worker
runs require a stable secret, and readiness validation passes.

## M1 OSS Surface

Red condition: the README makes broad claims without reproducible setup,
license, contribution, conduct, architecture, privacy, or security guidance.

Green condition: the repository has a concise README, MIT license, security
policy, contribution guide, code of conduct, issue templates, architecture
documentation, and privacy boundary documentation.

## M2 Reproducible Execution

Red condition: local tests require live provider credentials, there is no
synthetic sample fixture, or contributors cannot generate a sample JSON/PDF
report from the command line.

Green condition: compile, pytest, fallback-mode smoke tests, sample report
command tests, PDF path rejection, and deploy secret checks pass without live
provider credentials.

## M3 Domain Evaluation Harness

Red condition: the AI-assisted report path is only a demo and has no synthetic
domain cases, expected labels, or human-review notice checks.

Green condition: synthetic Korean text/OCR cases, provider-offline fallback
evaluation, expected coarse labels, and `docs/EVALUATION.md` are present and
tested.

## M4 Maintainer Automation

Red condition: Codex/API credit usage is described only as an intention.

Green condition: issue triage, PR security/privacy review, release-note draft,
and maintainer report automation are backed by repo-local commands or
templates.

Current M4 target artifacts:

- `.github/ISSUE_TEMPLATE/maintenance_task.md`
- `docs/MAINTAINER_AUTOMATION.md`
- `scripts/generate_maintainer_report.py`
- `tests/test_maintainer_report_command.py`

## M5 Educator And Human Review Boundary

Red condition: the repo can be misread as a legal, forensic, emergency, or
guaranteed-safety authority.

Green condition: educator-facing docs and sample output clearly require human
review and describe what the project is not.

Current M5 target artifacts:

- `docs/EDUCATOR_GUIDE.md`
- `docs/HUMAN_REVIEW_WORKFLOW.md`
- `examples/reports/human_review_sample.md`
- `tests/test_human_review_boundary_docs.py`

## M6 Official Submission Packet

Red condition: application text is generic, above field limits, or not tied to
current PR/CI/CodeQL/evaluation evidence.

Green condition: `docs/openai-codex-for-oss-application.md` is refreshed from
current evidence, all 500-character limits are verified, and official form
submission happens only after all exit criteria pass.

Current M6 target artifacts:

- `docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md`
- `docs/openai-codex-for-oss-application.md`
- `tests/test_application_packet.py`

## M8 Claim Boundary Hardening

Red condition: app UI, generated reports, docs, or examples describe AnsimTalk
as legal evidence, legal verification, guaranteed-safety, or an authority that
can decide discipline or emergency response.

Green condition: all public surfaces describe outputs as review material only,
and `tests/test_public_claim_boundary.py` plus
`scripts/check_oss_readiness.py` reject unsafe claim language.

Current M8 target artifacts:

- `app/templates/index.html`
- `app/templates/evidence.html`
- `app/templates/evidence_report.html`
- `app/templates/cyberbullying_help.html`
- `docs/CODEX_FOR_OSS_GOAL_PROPULSION_PLAN.md`
- `docs/CODEX_FOR_OSS_GOAL_PROPULSION_PROMPT_KO.md`
- `tests/test_public_claim_boundary.py`
