#!/usr/bin/env python3
"""Local OSS readiness checks for the AnsimTalk repository."""

from __future__ import annotations

import argparse
import compileall
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


REQUIRED_PATHS = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    ".env.example",
    ".github/workflows/test.yml",
    ".github/workflows/codeql.yml",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/ISSUE_TEMPLATE/maintenance_task.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/dependabot.yml",
    "docs/ROADMAP.md",
    "docs/MAINTAINER_GITHUB_CHECKLIST.md",
    "docs/MAINTAINER_AUTOMATION.md",
    "docs/ARCHITECTURE.md",
    "docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md",
    "docs/CONTRIBUTOR_LOCAL_RUN.md",
    "docs/EVALUATION.md",
    "docs/EDUCATOR_GUIDE.md",
    "docs/GITHUB_REFERENCE_PATTERNS.md",
    "docs/HUMAN_REVIEW_WORKFLOW.md",
    "docs/OPENAI_CODEX_FOR_OSS_EVIDENCE.md",
    "docs/PRIVACY_BOUNDARIES.md",
    "docs/RELEASE_NOTES_DRAFT.md",
    "docs/READINESS_AUDIT.md",
    "docs/openai-codex-for-oss-application.md",
    "examples/fixtures/cyberbullying_sample.txt",
    "examples/evaluations/domain_eval_cases.json",
    "examples/reports/human_review_sample.md",
    "scripts/check_oss_readiness.py",
    "scripts/generate_sample_report.py",
    "scripts/generate_maintainer_report.py",
    "scripts/run_domain_eval.py",
    "tests/test_app_smoke.py",
    "tests/test_application_packet.py",
    "tests/test_domain_eval_runner.py",
    "tests/test_human_review_boundary_docs.py",
    "tests/test_maintainer_report_command.py",
    "tests/test_oss_readiness.py",
    "tests/test_sample_report_command.py",
    "tests/test_security_review_regressions.py",
]

README_REQUIRED_TERMS = [
    "What It Does",
    "Limitations",
    "Quick Start",
    "Configuration",
    "Codex For OSS Submission Packet",
    "Tests",
    "Contributor Local Run",
    "Domain Evaluation",
    "Educator Guide",
    "Human Review Workflow",
    "Maintainer Automation",
    "Security",
    "Architecture",
    "Privacy Boundaries",
    "Maintainer Evidence",
]

README_REQUIRED_REFERENCES = [
    "docs/ARCHITECTURE.md",
    "docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md",
    "docs/CONTRIBUTOR_LOCAL_RUN.md",
    "docs/EVALUATION.md",
    "docs/EDUCATOR_GUIDE.md",
    "docs/HUMAN_REVIEW_WORKFLOW.md",
    "docs/MAINTAINER_AUTOMATION.md",
    "docs/PRIVACY_BOUNDARIES.md",
    "examples/evaluations/domain_eval_cases.json",
    "examples/fixtures/cyberbullying_sample.txt",
    "examples/reports/human_review_sample.md",
    "scripts/generate_sample_report.py",
    "scripts/generate_maintainer_report.py",
    "scripts/run_domain_eval.py",
]

SECRET_PATTERNS = [
    ("google_api_key", re.compile(r"AIza[0-9A-Za-z_-]{20,}")),
    ("private_key_block", re.compile("-----BEGIN " + "PRIVATE KEY-----")),
    ("service_account_private_key", re.compile(r'"private_key"\s*:\s*"')),
    ("sightengine_numeric_user", re.compile(r"SIGHTENGINE_API_USER\s*=\s*[\"']?\d{6,}")),
    (
        "sightengine_secret_literal",
        re.compile(
            r"SIGHTENGINE_API_SECRET\s*=\s*[\"']?(?!your_|change_|<|\$\{)"
            r"[A-Za-z0-9_-]{20,}"
        ),
    ),
    ("hardcoded_ansimtalk_secret", re.compile(r"ansimtalk-secret-key-\d+")),
    ("hardcoded_gcp_project", re.compile(r"dazzling-howl-[A-Za-z0-9-]+")),
    (
        "secret_key_literal_fallback",
        re.compile(
            r"SECRET_KEY\s*=\s*os\.environ\.get\([^)]*,\s*[\"'](?!change_|your_|dev_|test_)"
            r"[^\"']{12,}[\"']"
        ),
    ),
]

APPLICATION_REQUIRED_TERMS = [
    "M6 submission status: `READY_FOR_OWNER_SUBMISSION`",
    "Official OpenAI form submission: `NOT_PERFORMED`",
    "OpenAI Organization ID: `OWNER_INPUT_REQUIRED`",
    "Repository URL: `https://github.com/pjmin19/ansimtalk-`",
]

APPLICATION_REQUIRED_REFERENCES = [
    "docs/CODEX_FOR_OSS_SUBMISSION_PACKET.md",
    "docs/EDUCATOR_GUIDE.md",
    "docs/HUMAN_REVIEW_WORKFLOW.md",
    "docs/MAINTAINER_AUTOMATION.md",
    "docs/EVALUATION.md",
]

HUMAN_REVIEW_BOUNDARY_PATHS = [
    "docs/EDUCATOR_GUIDE.md",
    "docs/HUMAN_REVIEW_WORKFLOW.md",
    "examples/reports/human_review_sample.md",
]

HUMAN_REVIEW_REQUIRED_TERMS = [
    "Human review is required",
    "not a legal",
    "not a forensic",
    "not an emergency",
]

AFFIRMATIVE_AUTHORITY_PATTERNS = [
    ("guaranteed_safety", re.compile(r"\bguaranteed safety\b", re.IGNORECASE)),
    ("automated_action", re.compile(r"\bautomated action\b", re.IGNORECASE)),
    ("legal_determination", re.compile(r"\blegal determination\b", re.IGNORECASE)),
    ("forensic_conclusion", re.compile(r"\bforensic conclusion\b", re.IGNORECASE)),
    ("emergency_response_authority", re.compile(r"\bemergency response authority\b", re.IGNORECASE)),
]

NEGATIVE_BOUNDARY_MARKERS = (
    "not ",
    "not a ",
    "not an ",
    "does not",
    "do not",
    "must not",
    "without",
    "no ",
    "never",
)

SKIP_DIRS = {".git", ".pytest_cache", "__pycache__", ".venv", "venv", "env", "tmp", "logs"}
SKIP_SUFFIXES = {
    ".pdf",
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".ttf",
    ".woff",
    ".woff2",
    ".pyc",
}


@dataclass
class CheckResult:
    status: str
    issue_count: int
    issues: list[str]
    evidence: dict[str, object]


def iter_text_files(repo_root: Path) -> Iterable[Path]:
    for path in repo_root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.relative_to(repo_root).parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        yield path


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="cp949")
        except UnicodeDecodeError:
            return None


def check_required_paths(repo_root: Path, issues: list[str]) -> None:
    for relative in REQUIRED_PATHS:
        if not (repo_root / relative).exists():
            issues.append(f"missing_required_path:{relative}")


def check_readme(repo_root: Path, issues: list[str]) -> None:
    readme = read_text(repo_root / "README.md") or ""
    for term in README_REQUIRED_TERMS:
        if term not in readme:
            issues.append(f"readme_missing_term:{term}")
    for reference in README_REQUIRED_REFERENCES:
        if reference not in readme:
            issues.append(f"readme_missing_reference:{reference}")
    banned_claims = ["95%", "guarantee", "production-ready", "Human-Verified"]
    for claim in banned_claims:
        if claim in readme:
            issues.append(f"readme_overclaim:{claim}")


def is_negative_boundary_line(line: str) -> bool:
    lowered = line.lower()
    return any(marker in lowered for marker in NEGATIVE_BOUNDARY_MARKERS)


def check_human_review_boundary(repo_root: Path, issues: list[str]) -> None:
    for relative in HUMAN_REVIEW_BOUNDARY_PATHS:
        path = repo_root / relative
        if not path.exists():
            continue
        text = read_text(path) or ""
        for term in HUMAN_REVIEW_REQUIRED_TERMS:
            if term not in text:
                issues.append(f"human_review_missing_term:{relative}:{term}")
        for line_number, line in enumerate(text.splitlines(), start=1):
            if is_negative_boundary_line(line):
                continue
            for name, pattern in AFFIRMATIVE_AUTHORITY_PATTERNS:
                if pattern.search(line):
                    issues.append(f"human_review_overclaim:{name}:{relative}:{line_number}")


def check_secret_like_strings(repo_root: Path, issues: list[str]) -> int:
    scanned = 0
    for path in iter_text_files(repo_root):
        text = read_text(path)
        if text is None:
            continue
        scanned += 1
        relative = path.relative_to(repo_root).as_posix()
        for name, pattern in SECRET_PATTERNS:
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                issues.append(f"secret_like:{name}:{relative}:{line}")
    return scanned


def parse_answer_blocks(application_text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    pattern = re.compile(
        r"<!-- answer:([a-z0-9_-]+) -->(.*?)<!-- /answer:\1 -->",
        re.DOTALL,
    )
    for match in pattern.finditer(application_text):
        blocks[match.group(1)] = match.group(2).strip()
    return blocks


def parse_declared_counts(application_text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for name, value in re.findall(r"<!-- chars:([a-z0-9_-]+)=(\d+) -->", application_text):
        counts[name] = int(value)
    return counts


def check_application_packet(repo_root: Path, issues: list[str]) -> dict[str, int]:
    path = repo_root / "docs" / "openai-codex-for-oss-application.md"
    text = read_text(path) or ""
    for term in APPLICATION_REQUIRED_TERMS:
        if term not in text:
            issues.append(f"application_missing_term:{term}")
    for reference in APPLICATION_REQUIRED_REFERENCES:
        if reference not in text:
            issues.append(f"application_missing_reference:{reference}")
    blocks = parse_answer_blocks(text)
    declared = parse_declared_counts(text)
    required = {"repo_qualification", "api_credits_usage", "anything_else"}

    actual_counts: dict[str, int] = {}
    for name in required:
        if name not in blocks:
            issues.append(f"missing_application_answer:{name}")
            continue
        count = len(blocks[name])
        actual_counts[name] = count
        if count > 500:
            issues.append(f"application_answer_too_long:{name}:{count}")
        if declared.get(name) != count:
            issues.append(
                f"application_char_count_mismatch:{name}:declared={declared.get(name)}:actual={count}"
            )
    return actual_counts


def check_compile(repo_root: Path, issues: list[str]) -> bool:
    ok = compileall.compile_dir(str(repo_root), quiet=1)
    if not ok:
        issues.append("compileall_failed")
    return bool(ok)


def run_checks(repo_root: Path, run_compile: bool = True) -> CheckResult:
    repo_root = repo_root.resolve()
    issues: list[str] = []

    check_required_paths(repo_root, issues)
    check_readme(repo_root, issues)
    check_human_review_boundary(repo_root, issues)
    scanned_files = check_secret_like_strings(repo_root, issues)
    answer_counts = check_application_packet(repo_root, issues)
    compile_ok = check_compile(repo_root, issues) if run_compile else None

    status = "PASS: Auto-Verified" if not issues else "FAIL"
    return CheckResult(
        status=status,
        issue_count=len(issues),
        issues=issues,
        evidence={
            "repo_root": str(repo_root),
            "scanned_text_files": scanned_files,
            "application_answer_counts": answer_counts,
            "compileall": compile_ok,
            "live_actions": {
                "github_push": "NOT_PERFORMED",
                "github_issue_creation": "NOT_PERFORMED",
                "release_creation": "NOT_PERFORMED",
                "openai_form_submit": "NOT_PERFORMED",
                "provider_change": "NOT_PERFORMED",
                "training": "NOT_PERFORMED",
            },
        },
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", help="Repository root to check.")
    parser.add_argument("--json-out", default="", help="Optional JSON report path.")
    parser.add_argument("--skip-compile", action="store_true", help="Skip compileall.")
    args = parser.parse_args(argv)

    result = run_checks(Path(args.repo_root), run_compile=not args.skip_compile)
    payload = asdict(result)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    print(text)

    if args.json_out:
        out_path = Path(args.json_out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text + "\n", encoding="utf-8")

    return 0 if result.status == "PASS: Auto-Verified" else 1


if __name__ == "__main__":
    raise SystemExit(main())
