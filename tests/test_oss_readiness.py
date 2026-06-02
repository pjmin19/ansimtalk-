from pathlib import Path

from scripts.check_oss_readiness import run_checks


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_oss_readiness_static_checks_pass():
    result = run_checks(REPO_ROOT, run_compile=False)
    assert result.status == "PASS: Auto-Verified", result.issues
