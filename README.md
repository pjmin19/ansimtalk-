# AnsimTalk

AnsimTalk is a small Flask OSS toolkit for turning uploaded images or text into
a digital safety evidence report. It was built for education and youth safety
workflows where a maintainer needs a repeatable way to collect metadata, run
basic AI-assisted analysis, generate a PDF report, and keep human review in the
loop.

This repository is being prepared as a public open-source project. The current
priority is reproducibility, safe configuration, and clear maintainer evidence,
not production claims.

## What It Does

- Accepts image or text uploads through a Flask web interface.
- Extracts file metadata and SHA-256 hashes for evidence tracking.
- Routes image and text content through optional external analysis providers.
- Generates a PDF report from the captured analysis result.
- Provides API endpoints for health checks, upload analysis, and PDF download.

## Limitations

- External AI providers are optional and require local environment variables.
- Missing provider credentials should produce safe fallback behavior in tests.
- Deployed or multi-worker runs must set a stable `SECRET_KEY`.
- API PDF generation rejects client-supplied local file paths.
- The project is not a legal, forensic, medical, or safety authority.
- Model output must be reviewed by a human before real-world action.
- The current public readiness state is `PASS: Auto-Verified` only after the
  local validators pass. It has not been manually submitted or reviewed.

## Quick Start

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pytest
Copy-Item .env.example .env
python run.py
```

Open `http://127.0.0.1:5000` after the server starts.

## Configuration

All credentials must come from environment variables. Do not commit real
provider keys, service-account JSON, `.env`, or runtime uploads.

Use `.env.example` as the local template:

```text
SECRET_KEY=change_me_to_a_secure_random_value
SIGHTENGINE_API_USER=your_sightengine_user
SIGHTENGINE_API_SECRET=your_sightengine_secret
GOOGLE_GEMINI_API_KEY=your_gemini_api_key
GOOGLE_CLOUD_VISION_API_KEY=your_google_cloud_vision_api_key
GOOGLE_APPLICATION_CREDENTIALS=
GOOGLE_SERVICE_ACCOUNT_JSON=
GCP_PROJECT=your-gcp-project-id
GEMINI_LOCATION=us-central1
LOG_LEVEL=INFO
```

## Tests

```powershell
python -m compileall -q .
python -m pytest -q
python scripts/check_oss_readiness.py --repo-root .
```

The OSS readiness validator checks required project files, public application
answer character counts, compile status, security regression tests, and
secret-like strings.

## Contributor Local Run

Contributors can generate a local sample report without external provider
accounts:

```powershell
python scripts/generate_sample_report.py --output-dir tmp/sample_report
```

The command reads `examples/fixtures/cyberbullying_sample.txt`, runs the
cyberbullying workflow in offline fallback mode, and writes JSON/PDF outputs
under `tmp/sample_report`.

See `docs/CONTRIBUTOR_LOCAL_RUN.md` for setup, expected outputs, and validation
commands.

## Domain Evaluation

AnsimTalk includes a credential-free domain evaluation harness for synthetic
Korean text and OCR-like cyberbullying cases:

```powershell
python scripts/run_domain_eval.py --output-json tmp/domain_eval/domain_eval_result.json
```

The command reads `examples/evaluations/domain_eval_cases.json`, runs the
provider-offline fallback workflow, checks expected coarse risk labels, and
verifies that every case keeps the human-review notice visible.

See `docs/EVALUATION.md` for the fixture schema, expected output, and limits.
The harness is a deterministic safety smoke, not a model benchmark.

## Maintainer Automation

Maintainers can generate a local automation report from public repo templates
and docs:

```powershell
python scripts/generate_maintainer_report.py --output-dir tmp/maintainer_report
```

The command reads issue templates, the PR security/privacy checklist, release
draft notes, and validation commands. It writes a JSON/Markdown report that
shows how Codex/API credits would support issue triage, PR review, release
notes, and maintainer status reporting.

See `docs/MAINTAINER_AUTOMATION.md` for inputs, expected outputs, and live
provider boundaries.

## Architecture

The project keeps a small, inspectable Flask architecture:

- `app/routes.py` handles web/API routes, upload validation, session state, and
  PDF download boundaries.
- `app/services.py` handles file analysis, optional provider calls, fallback
  behavior, report HTML, and PDF rendering.
- `scripts/run_domain_eval.py` runs synthetic domain evaluation cases in
  offline fallback mode.
- `scripts/generate_maintainer_report.py` generates public-safe maintainer
  automation reports from repo templates and docs.
- `scripts/check_oss_readiness.py` validates the public OSS surface before
  release or application work.

See `docs/ARCHITECTURE.md` for the full data flow and component map.

## Security

If real credentials were ever committed to public history, revoke and rotate
them before using any deployment. See `SECURITY.md` for the rotation checklist
and secret-scanning procedure.

## Privacy Boundaries

Do not commit real student data, private chat exports, uploaded evidence,
generated PDFs, provider keys, service-account JSON, or `.env` files.

Provider calls are optional and controlled by environment variables. Missing
credentials should keep the local workflow testable through fallback behavior.

See `docs/PRIVACY_BOUNDARIES.md` for public repository, runtime data, provider,
and human-review boundaries.

## Maintainer Evidence

The public maintainer story should be kept in small, reviewable artifacts:

- `docs/ROADMAP.md` for DTT milestones.
- `docs/ARCHITECTURE.md` for the project component map and runtime flow.
- `docs/PRIVACY_BOUNDARIES.md` for student data, provider, and human-review
  boundaries.
- `docs/CONTRIBUTOR_LOCAL_RUN.md` for the credential-free sample report path.
- `docs/EVALUATION.md` for synthetic provider-offline domain evaluation.
- `docs/MAINTAINER_AUTOMATION.md` for issue triage, PR review, release-note,
  and maintainer report automation.
- `docs/MAINTAINER_GITHUB_CHECKLIST.md` for Issues, Milestones, and Releases.
- `docs/READINESS_AUDIT.md` for the latest local M0-M6 audit.
- `docs/OPENAI_CODEX_FOR_OSS_EVIDENCE.md` for a criteria-to-evidence map.
- `docs/GITHUB_REFERENCE_PATTERNS.md` for clean-room public GitHub patterns.
- `.github/workflows/test.yml` for reproducible checks.
- `.github/workflows/codeql.yml` for CodeQL security analysis.
- `.github/dependabot.yml` for dependency update monitoring.
- `.github/ISSUE_TEMPLATE/config.yml` for issue routing.
- `docs/openai-codex-for-oss-application.md` for application copy.
- `examples/evaluations/domain_eval_cases.json` for synthetic evaluation cases.
- `scripts/generate_maintainer_report.py` for local maintainer automation
  reporting.
- `scripts/run_domain_eval.py` for the offline domain eval runner.

## Status

This repository is a public OSS candidate, not a finished product. Before an
OpenAI Codex for Open Source application is submitted, the maintainer should
review the application packet and submit the official OpenAI form manually.

Maintainer evidence already created:

- PR #8 security review hardening merged.
- Issues #2-#6 closed.
- Milestone `v0.1.0-oss-candidate` closed.
- Release `v0.1.0-oss-candidate` published.
- Issue routing, Dependabot, and CodeQL configuration prepared.
- Architecture and privacy boundaries documented for M1 public OSS shape.
- Contributor local run documented with a synthetic fixture and sample report
  command for M2.
- Domain evaluation documented with synthetic Korean text/OCR cases and an
  offline fallback runner for M3.
- Maintainer automation documented with an issue triage template, PR
  security/privacy checklist, and local report generator for M4.
