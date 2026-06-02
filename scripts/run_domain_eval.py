#!/usr/bin/env python3
"""Run offline domain evaluation cases for AnsimTalk's fallback workflow."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


DEFAULT_CASES = REPO_ROOT / "examples" / "evaluations" / "domain_eval_cases.json"
DEFAULT_OUTPUT_JSON = REPO_ROOT / "tmp" / "domain_eval" / "domain_eval_result.json"
HUMAN_REVIEW_NOTICE = "Human review is required before any real-world action."


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run synthetic domain evaluation cases.")
    parser.add_argument("--cases", default=str(DEFAULT_CASES), help="Domain eval cases JSON path.")
    parser.add_argument("--output-json", default=str(DEFAULT_OUTPUT_JSON), help="Output JSON report path.")
    parser.add_argument(
        "--allow-provider",
        action="store_true",
        help="Allow configured external text-analysis providers. Defaults to offline fallback.",
    )
    return parser.parse_args(argv)


def force_offline_provider_mode() -> None:
    for name in (
        "GOOGLE_GEMINI_API_KEY",
        "SIGHTENGINE_API_USER",
        "SIGHTENGINE_API_SECRET",
        "GOOGLE_CLOUD_VISION_API_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GOOGLE_SERVICE_ACCOUNT_JSON",
    ):
        os.environ.pop(name, None)


def load_cases(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "ansimtalk_domain_eval_cases.v1":
        raise ValueError("Unsupported domain eval cases schema.")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("Domain eval cases must contain at least one case.")
    return cases


def evaluate_case(case: dict[str, Any]) -> dict[str, Any]:
    from app.services import analyze_text_with_gemini, extract_risk_line

    analysis = analyze_text_with_gemini(str(case.get("input_text", "")))
    table = str(analysis.get("table", ""))
    summary = str(analysis.get("summary", ""))
    actual_risk = extract_risk_line(summary)
    expected_risk = str(case.get("expected_overall_risk", "")).strip()
    expected_terms = [str(term) for term in case.get("expected_risk_terms", [])]
    combined_output = table + "\n" + summary

    issues: list[str] = []
    if actual_risk != expected_risk:
        issues.append(f"risk_mismatch:expected={expected_risk}:actual={actual_risk}")

    missing_terms = [term for term in expected_terms if term not in combined_output]
    if missing_terms:
        issues.append("missing_expected_terms:" + ",".join(missing_terms))

    notice_present = HUMAN_REVIEW_NOTICE in summary
    if case.get("requires_human_review_notice", True) and not notice_present:
        issues.append("missing_human_review_notice")

    return {
        "case_id": case.get("id", ""),
        "source_type": case.get("source_type", ""),
        "expected_overall_risk": expected_risk,
        "actual_overall_risk": actual_risk,
        "expected_terms_checked": expected_terms,
        "human_review_notice_present": notice_present,
        "fallback_used": bool(analysis.get("fallback_used")),
        "status": "PASS" if not issues else "FAIL",
        "issues": issues,
    }


def run_domain_eval(args: argparse.Namespace) -> dict[str, Any]:
    if not args.allow_provider:
        force_offline_provider_mode()

    from app import create_app

    cases_path = Path(args.cases).resolve()
    output_path = Path(args.output_json).resolve()
    cases = load_cases(cases_path)

    app = create_app()
    with app.app_context():
        results = [evaluate_case(case) for case in cases]

    issues = [
        f"{result['case_id']}:{issue}"
        for result in results
        for issue in result["issues"]
    ]
    if cases_path.is_relative_to(REPO_ROOT):
        cases_reference = cases_path.relative_to(REPO_ROOT).as_posix()
    else:
        cases_reference = str(cases_path)

    payload = {
        "schema": "ansimtalk_domain_eval_result.v1",
        "status": "PASS" if not issues else "FAIL",
        "issue_count": len(issues),
        "issues": issues,
        "provider_mode": "provider_allowed" if args.allow_provider else "offline_fallback",
        "cases": cases_reference,
        "case_count": len(results),
        "passed_count": sum(1 for result in results if result["status"] == "PASS"),
        "results": results,
        "live_actions": {
            "provider_call_requested": bool(args.allow_provider),
            "openai_form_submit": "NOT_PERFORMED",
            "training": "NOT_PERFORMED",
        },
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main(argv: list[str] | None = None) -> int:
    try:
        payload = run_domain_eval(parse_args(argv))
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    print(
        json.dumps(
            {
                "status": payload["status"],
                "provider_mode": payload["provider_mode"],
                "case_count": payload["case_count"],
                "passed_count": payload["passed_count"],
                "issue_count": payload["issue_count"],
            },
            ensure_ascii=False,
        )
    )
    return 0 if payload["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
