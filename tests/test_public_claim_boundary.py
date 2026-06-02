from pathlib import Path

from scripts.check_oss_readiness import (
    PUBLIC_CLAIM_BOUNDARY_PATHS,
    check_public_claim_boundaries,
    is_negative_boundary_line,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_public_claim_boundaries_reject_app_overclaims():
    issues: list[str] = []
    check_public_claim_boundaries(REPO_ROOT, issues)
    assert issues == []


def test_public_claim_boundary_paths_cover_app_templates():
    assert "app/templates" in PUBLIC_CLAIM_BOUNDARY_PATHS


def test_unsafe_korean_claim_lines_are_not_negative_boundaries():
    unsafe_lines = [
        "AI로 분석하고 " + "법적" + "증거 생성",
        "분석 결과를 PDF로 저장해 " + "법적 " + "증거로 활용하세요.",
        "무결성 및 " + "법적 " + "검증",
        "확실한 " + "증거로 신고",
    ]
    for line in unsafe_lines:
        assert not is_negative_boundary_line(line)
