# Release Notes Draft

## v0.1.0-oss-candidate

Status: `PERFORMED`

Release URL:
https://github.com/pjmin19/ansimtalk-/releases/tag/v0.1.0-oss-candidate

This release candidate prepares AnsimTalk for public open-source maintenance.

### Added

- Public-safe README, license, security policy, contribution guide, and code of
  conduct.
- GitHub issue templates and pull request checklist.
- CI workflow for compile, pytest, and OSS readiness validation.
- Local readiness validator for required files, answer length, compile status,
  and secret-like strings.
- Fallback smoke tests for missing external provider credentials.
- Security regression tests for client-supplied PDF file paths and deployed
  stable secret enforcement.

### Changed

- Runtime configuration now expects credentials from environment variables.
- Docker deployments require a stable `SECRET_KEY` through
  `ANSIMTALK_REQUIRE_STABLE_SECRET=1`.
- The README no longer presents broad production or accuracy claims.

### Security

- Real credentials must be revoked and rotated if they were ever exposed in
  public history.
- `.env.example` contains placeholders only.
- `/api/download_pdf` rejects client-supplied local path fields before PDF
  generation.

## Next Maintenance Draft

Status: `DRAFT`

### Added

- M3 domain evaluation harness with synthetic Korean text/OCR cases.
- M4 maintainer automation report generator for issue triage, PR
  security/privacy review, release-note inputs, and Codex/API credit planning.
- M5 educator guide, human review workflow, and safe sample output boundary.

### Validation

- `python -m compileall -q .`
- `python -m pytest -q`
- `python scripts/run_domain_eval.py --output-json tmp/domain_eval/domain_eval_result.json`
- `python scripts/generate_maintainer_report.py --output-dir tmp/maintainer_report`
- `python scripts/check_oss_readiness.py --repo-root .`
