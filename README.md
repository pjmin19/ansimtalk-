# AnsimTalk

AnsimTalk is a Flask prototype for turning uploaded images or text into a
digital safety evidence report. It was built for education and youth safety
workflows where a maintainer needs a repeatable way to collect metadata, run
basic AI-assisted analysis, and generate a PDF report.

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

## Security

If real credentials were ever committed to public history, revoke and rotate
them before using any deployment. See `SECURITY.md` for the rotation checklist
and secret-scanning procedure.

## Maintainer Evidence

The public maintainer story should be kept in small, reviewable artifacts:

- `docs/ROADMAP.md` for DTT milestones.
- `docs/MAINTAINER_GITHUB_CHECKLIST.md` for Issues, Milestones, and Releases.
- `docs/READINESS_AUDIT.md` for the latest local M0-M6 audit.
- `.github/workflows/test.yml` for reproducible checks.
- `docs/openai-codex-for-oss-application.md` for application copy.

## Status

This repository is a public OSS candidate, not a finished product. Before an
OpenAI Codex for Open Source application is submitted, the maintainer should
push the security hardening branch, create the public GitHub issues/milestone,
publish a small release, and submit the official form manually.
