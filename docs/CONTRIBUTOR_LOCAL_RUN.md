# Contributor Local Run

This guide gives contributors a credential-free way to prove that AnsimTalk can
run locally, analyze a synthetic fixture, and generate JSON/PDF sample report
artifacts.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pytest
```

## Generate A Sample Report

```powershell
python scripts/generate_sample_report.py --output-dir tmp/sample_report
```

Default inputs and outputs:

- input fixture: `examples/fixtures/cyberbullying_sample.txt`
- output JSON: `tmp/sample_report/sample_report.json`
- output PDF: `tmp/sample_report/sample_report.pdf`

The default mode clears provider-related environment variables inside the
process and uses the deterministic fallback path. This keeps contributor smoke
runs reproducible without external accounts.

## Validate

```powershell
python -m compileall -q .
python -m pytest -q
python scripts/check_oss_readiness.py --repo-root .
```

The test suite includes `tests/test_sample_report_command.py`, which runs the
sample command in a temporary output directory and verifies:

- JSON output exists
- PDF output exists and is non-empty
- provider mode is `offline_fallback`
- the payload records `human_review_required`

## Run The Domain Evaluation Smoke

```powershell
python scripts/run_domain_eval.py --output-json tmp/domain_eval/domain_eval_result.json
```

This command reads `examples/evaluations/domain_eval_cases.json`, keeps provider
calls disabled by default, and verifies the expected fallback risk labels plus
the human-review notice. See `docs/EVALUATION.md` for the evaluation boundary.

## Privacy Boundary

The fixture is synthetic and public-safe. Runtime outputs are generated under
`tmp/` by default and must not be committed. Do not use this command with real
student data unless the data has been reviewed, authorized, and handled outside
the public repository.
