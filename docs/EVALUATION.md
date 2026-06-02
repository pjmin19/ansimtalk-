# Domain Evaluation

AnsimTalk uses a small domain evaluation harness to prove that the public repo
can exercise the cyberbullying workflow without live provider credentials or
private student data.

This is a deterministic safety smoke, not a model benchmark. It checks that
synthetic Korean text and OCR-like fixtures flow through the offline fallback,
produce expected coarse risk labels, and keep the human-review notice visible.

## Fixture Set

Cases live in `examples/evaluations/domain_eval_cases.json`.

The current schema is `ansimtalk_domain_eval_cases.v1` and each case includes:

- `id`
- `source_type`
- `analysis_type`
- `input_text`
- `expected_overall_risk`
- `expected_risk_terms`
- `requires_human_review_notice`

The fixture content is synthetic and public-safe. Do not place real student
messages, real screenshots, private chat exports, or generated runtime reports
in the repository.

## Run

```powershell
python scripts/run_domain_eval.py --output-json tmp/domain_eval/domain_eval_result.json
```

Expected summary:

```json
{"status":"PASS","provider_mode":"offline_fallback","case_count":3,"passed_count":3,"issue_count":0}
```

## What The Harness Checks

- provider mode remains `offline_fallback` by default
- all synthetic cases return the expected `overall risk` label
- expected risk terms are present in fallback output
- every case keeps `Human review is required before any real-world action.`
- result JSON uses schema `ansimtalk_domain_eval_result.v1`

## Boundaries

- The fallback uses simple keyword rules and is intentionally limited.
- Passing this harness does not prove real-world accuracy.
- Passing this harness does not make the project a legal, forensic, emergency,
  or safety authority.
- External provider evaluation is opt-in with `--allow-provider` and should use
  reviewed, authorized, non-public data handling outside the public repo.
