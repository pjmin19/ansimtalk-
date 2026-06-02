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
guaranteed safety authority.

Green condition: educator-facing docs and sample output clearly require human
review and describe what the project is not.

## M6 Official Submission Packet

Red condition: application text is generic, above field limits, or not tied to
current PR/CI/CodeQL/evaluation evidence.

Green condition: `docs/openai-codex-for-oss-application.md` is refreshed from
current evidence, all 500-character limits are verified, and official form
submission happens only after all exit criteria pass.
