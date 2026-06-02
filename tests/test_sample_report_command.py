import json
import os
import subprocess
import sys
from pathlib import Path


def test_sample_report_command_generates_json_and_pdf(tmp_path):
    repo_root = Path(__file__).resolve().parents[1]
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
            str(repo_root / "scripts" / "generate_sample_report.py"),
            "--output-dir",
            str(tmp_path),
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

    json_path = Path(summary["json"])
    pdf_path = Path(summary["pdf"])
    assert json_path.exists()
    assert pdf_path.exists()
    assert pdf_path.stat().st_size > 1000

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["schema"] == "ansimtalk_sample_report.v1"
    assert payload["sample_run"]["human_review_required"] is True
    assert payload["sample_run"]["provider_mode"] == "offline_fallback"
    assert payload["analysis"]["analysis_type"] == "cyberbullying"
