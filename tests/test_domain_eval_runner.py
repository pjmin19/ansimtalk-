import json
import os
import subprocess
import sys
from pathlib import Path


def test_domain_eval_runner_passes_offline_cases(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
    output_json = tmp_path / "domain_eval_result.json"
    env = os.environ.copy()
    for name in (
        "GOOGLE_GEMINI_API_KEY",
        "SIGHTENGINE_API_USER",
        "SIGHTENGINE_API_SECRET",
        "GOOGLE_CLOUD_VISION_API_KEY",
        "GOOGLE_APPLICATION_CREDENTIALS",
        "GOOGLE_SERVICE_ACCOUNT_JSON",
    ):
        env.pop(name, None)

    result = subprocess.run(
        [
            sys.executable,
            str(repo_root / "scripts" / "run_domain_eval.py"),
            "--output-json",
            str(output_json),
        ],
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )

    assert result.returncode == 0, result.stderr

    summary = json.loads(result.stdout)
    assert summary["status"] == "PASS"
    assert summary["provider_mode"] == "offline_fallback"
    assert summary["case_count"] == 3
    assert summary["passed_count"] == 3

    payload = json.loads(output_json.read_text(encoding="utf-8"))
    assert payload["schema"] == "ansimtalk_domain_eval_result.v1"
    assert payload["status"] == "PASS"
    assert payload["issue_count"] == 0
    assert payload["provider_mode"] == "offline_fallback"
    assert all(result["human_review_notice_present"] for result in payload["results"])
    assert all(result["fallback_used"] for result in payload["results"])
