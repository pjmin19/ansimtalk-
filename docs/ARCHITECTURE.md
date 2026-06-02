# Architecture

AnsimTalk is a small Flask OSS toolkit for building and reviewing
AI-assisted digital safety evidence reports. The architecture is intentionally
simple so contributors can inspect data flow, run the project without provider
credentials, and verify the human-review boundary.

## Runtime Shape

```text
Browser or API client
  -> Flask routes in app/routes.py
  -> upload validation and temporary file storage
  -> app/services.py analysis helpers
  -> optional external providers or offline fallback behavior
  -> HTML templates and PDF report generation
  -> human review before real-world action
```

## Main Components

- `run.py` starts the Flask app for local development.
- `app/__init__.py` creates the app, loads environment configuration, and
  rejects deploy-style runs that require a stable `SECRET_KEY` but do not set
  one.
- `app/routes.py` owns web routes, API routes, upload validation, session state,
  and PDF download endpoints.
- `app/services.py` owns file analysis, text preprocessing, optional provider
  calls, fallback analysis, report HTML, and PDF rendering.
- `app/templates/` and `app/static/` hold the web UI and report styling.
- `tests/` covers smoke behavior and security regressions.
- `scripts/check_oss_readiness.py` checks public OSS readiness, required files,
  application field character counts, compile status, and secret-like strings.
- `scripts/run_domain_eval.py` checks synthetic Korean text and OCR-like
  fixtures against the provider-offline fallback workflow.
- `.github/workflows/` runs CI and CodeQL on GitHub.

## Analysis Flow

1. A user uploads a `.txt`, `.png`, `.jpg`, or `.jpeg` file.
2. `app/routes.py` validates extension and size, normalizes the filename, and
   writes a generated filename under `tmp/`.
3. `app/services.py` computes file metadata and SHA-256 evidence.
4. Deepfake analysis uses image metadata and optional Sightengine credentials.
5. Cyberbullying analysis uses text files or OCR output, then optional Gemini
   credentials or a deterministic fallback.
6. Results are rendered for review and can be converted into a PDF report.

## Evaluation Flow

`examples/evaluations/domain_eval_cases.json` stores synthetic public-safe
cases. `scripts/run_domain_eval.py` clears provider credentials by default,
runs each case through the same text-analysis fallback path, and writes a JSON
result with expected risk labels and human-review notice checks.

## Provider Boundary

Provider credentials are optional. Missing credentials must not break local
tests or prevent fallback-mode review. All credentials must come from runtime
environment variables; they are not stored in source files.

## Security Boundary

The API PDF endpoint rejects client-supplied local path fields before PDF
generation. Uploads and generated reports are runtime files and must stay out
of git.

## Non-Goals

AnsimTalk is not a legal, forensic, medical, emergency, or safety authority.
Reports are structured review aids. Human review is required before any
real-world action.
