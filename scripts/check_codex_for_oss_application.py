#!/usr/bin/env python3
"""Deterministic readiness check for the Codex for OSS application packet.

This script is not an OpenAI review. It verifies that the repository exposes the
signals an automated reviewer is likely to look for from the public application
criteria: maintainer evidence, active maintenance, ecosystem-importance
framing, security quality, bounded claims, and under-limit form answers.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path

try:
    from .check_oss_readiness import parse_answer_blocks, parse_declared_counts, read_text
except ImportError:
    from check_oss_readiness import parse_answer_blocks, parse_declared_counts, read_text


REQUIRED_PATHS = [
    "README.md",
    "docs/CODEX_FOR_OSS_AUTOMATED_REVIEW.md",
    "docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md",
    "docs/OPENAI_CODEX_FOR_OSS_EVIDENCE.md",
    "docs/READINESS_AUDIT.md",
    "docs/openai-codex-for-oss-application.md",
    "docs/MAINTAINER_AUTOMATION.md",
    "docs/MAINTAINER_GITHUB_CHECKLIST.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/workflows/test.yml",
    ".github/workflows/codeql.yml",
    ".github/dependabot.yml",
]

REQUIRED_REVIEW_TERMS = [
    "PASS: Auto-Review-Ready",
    "READY_FOR_OWNER_SUBMISSION",
    "adoption is early",
    "clear workflow importance",
    "active maintainer evidence",
    "not on broad usage metrics",
    "OpenAI Organization ID",
]

REQUIRED_README_TERMS = [
    "Codex For OSS Automated Review",
    "docs/CODEX_FOR_OSS_AUTOMATED_REVIEW.md",
    "PASS: Auto-Review-Ready",
    "primary maintainer",
    "early adoption risk",
]

REQUIRED_EVIDENCE_TERMS = [
    "Public open-source project",
    "Active maintenance",
    "PR review and issue triage",
    "Release management",
    "Security and quality",
    "Codex/API-credit fit",
    "Automated review risk",
]

REQUIRED_APPLICATION_TERMS = [
    "Repository URL: `https://github.com/pjmin19/ansimtalk-`",
    "Maintainer role: `primary maintainer`",
    "M6 submission status: `READY_FOR_OWNER_SUBMISSION`",
    "Official OpenAI form submission: `NOT_PERFORMED`",
    "OpenAI Organization ID: `OWNER_INPUT_REQUIRED`",
]

ANSWER_REQUIRED_TERMS = {
    "repo_qualification": [
        "public Flask OSS toolkit",
        "education workflows",
        "CodeQL",
        "Dependabot",
        "human-review boundaries",
        "maintenance load",
    ],
    "api_credits_usage": [
        "PR security/privacy review",
        "issue triage",
        "release-note",
        "provider-adapter",
        "eval expansion",
        "public-safe",
    ],
    "anything_else": [
        "Adoption is early",
        "ecosystem importance",
        "responsible maintainer evidence",
        "reproducible without credentials",
        "no legal",
    ],
}

BLOCKED_ANSWER_TERMS = [
    "accepted by OpenAI",
    "already submitted",
    "guaranteed acceptance",
    "guaranteed safety",
    "legal authority",
    "forensic authority",
]


@dataclass
class ApplicationCheck:
    status: str
    issue_count: int
    risk_count: int
    issues: list[str]
    risks: list[str]
    evidence: dict[str, object]


def require_paths(repo_root: Path, issues: list[str]) -> None:
    for relative in REQUIRED_PATHS:
        if not (repo_root / relative).exists():
            issues.append(f"missing_required_path:{relative}")


def require_terms(label: str, text: str, terms: list[str], issues: list[str]) -> None:
    for term in terms:
        if term not in text:
            issues.append(f"{label}_missing_term:{term}")


def check_application_answers(repo_root: Path, issues: list[str]) -> dict[str, int]:
    path = repo_root / "docs" / "openai-codex-for-oss-application.md"
    text = read_text(path) or ""
    require_terms("application_packet", text, REQUIRED_APPLICATION_TERMS, issues)

    blocks = parse_answer_blocks(text)
    declared = parse_declared_counts(text)
    counts: dict[str, int] = {}

    for name, required_terms in ANSWER_REQUIRED_TERMS.items():
        answer = blocks.get(name)
        if not answer:
            issues.append(f"missing_application_answer:{name}")
            continue
        counts[name] = len(answer)
        if len(answer) > 500:
            issues.append(f"application_answer_too_long:{name}:{len(answer)}")
        if declared.get(name) != len(answer):
            issues.append(
                f"application_char_count_mismatch:{name}:declared={declared.get(name)}:actual={len(answer)}"
            )
        for term in required_terms:
            if term not in answer:
                issues.append(f"application_answer_missing_term:{name}:{term}")
        lowered = answer.lower()
        for term in BLOCKED_ANSWER_TERMS:
            if term in lowered:
                issues.append(f"application_answer_overclaim:{name}:{term}")

    return counts


def count_public_maintenance_markers(text: str) -> int:
    markers = [
        r"\bPR #\d+",
        r"\bIssues? #\d+",
        r"\bmilestone\b",
        r"\brelease\b",
        r"\bCodeQL\b",
        r"\bDependabot\b",
        r"\bpytest\b",
        r"\bissue triage\b",
        r"\bPR review\b",
    ]
    return sum(1 for marker in markers if re.search(marker, text, re.IGNORECASE))


def run_checks(repo_root: Path) -> ApplicationCheck:
    repo_root = repo_root.resolve()
    issues: list[str] = []
    risks: list[str] = []

    require_paths(repo_root, issues)

    readme = read_text(repo_root / "README.md") or ""
    review_doc = read_text(repo_root / "docs" / "CODEX_FOR_OSS_AUTOMATED_REVIEW.md") or ""
    evidence_doc = read_text(repo_root / "docs" / "OPENAI_CODEX_FOR_OSS_EVIDENCE.md") or ""
    audit_doc = read_text(repo_root / "docs" / "READINESS_AUDIT.md") or ""

    require_terms("readme", readme, REQUIRED_README_TERMS, issues)
    require_terms("automated_review_doc", review_doc, REQUIRED_REVIEW_TERMS, issues)
    require_terms("evidence_doc", evidence_doc, REQUIRED_EVIDENCE_TERMS, issues)

    answer_counts = check_application_answers(repo_root, issues)

    maintenance_marker_count = count_public_maintenance_markers(
        "\n".join([readme, review_doc, evidence_doc, audit_doc])
    )
    if maintenance_marker_count < 7:
        issues.append(f"insufficient_maintenance_markers:{maintenance_marker_count}")

    if "Adoption is early" not in review_doc:
        issues.append("adoption_risk_not_disclosed")
    else:
        risks.append("early_adoption_low_popularity_signal")

    if "not a legal" not in readme or "human-review" not in readme:
        issues.append("readme_missing_safety_boundary")

    status = "PASS: Auto-Review-Ready" if not issues else "FAIL"
    return ApplicationCheck(
        status=status,
        issue_count=len(issues),
        risk_count=len(risks),
        issues=issues,
        risks=risks,
        evidence={
            "repo_root": str(repo_root),
            "application_answer_counts": answer_counts,
            "maintenance_marker_count": maintenance_marker_count,
            "official_form_submission": "NOT_PERFORMED",
            "openai_acceptance": "NOT_CLAIMED",
            "github_push": "NOT_PERFORMED",
            "risk_boundary": "early adoption disclosed; no acceptance guarantee",
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root to check.")
    parser.add_argument("--json-out", default="", help="Optional JSON report path.")
    args = parser.parse_args(argv)

    result = run_checks(Path(args.repo_root))
    payload = asdict(result)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")

    return 0 if result.status == "PASS: Auto-Review-Ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
