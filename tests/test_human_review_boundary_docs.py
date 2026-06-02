from pathlib import Path

from scripts.check_oss_readiness import (
    AFFIRMATIVE_AUTHORITY_PATTERNS,
    HUMAN_REVIEW_BOUNDARY_PATHS,
    HUMAN_REVIEW_REQUIRED_TERMS,
    is_negative_boundary_line,
    run_checks,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_human_review_boundary_docs_are_present_and_checked():
    result = run_checks(REPO_ROOT, run_compile=False)
    assert result.status == "PASS: Auto-Verified", result.issues

    for relative in HUMAN_REVIEW_BOUNDARY_PATHS:
        text = (REPO_ROOT / relative).read_text(encoding="utf-8")
        for term in HUMAN_REVIEW_REQUIRED_TERMS:
            assert term in text


def test_affirmative_authority_patterns_reject_overclaims():
    unsafe_lines = [
        "This is a legal determination for discipline.",
        "This report is a forensic conclusion.",
        "The output provides guaranteed safety.",
        "The workflow triggers automated action.",
    ]

    for line in unsafe_lines:
        assert not is_negative_boundary_line(line)
        assert any(pattern.search(line) for _, pattern in AFFIRMATIVE_AUTHORITY_PATTERNS)


def test_negative_boundary_lines_are_allowed():
    safe_line = (
        "This sample is not a legal determination, not a forensic conclusion, "
        "and not an emergency response tool."
    )
    assert is_negative_boundary_line(safe_line)
