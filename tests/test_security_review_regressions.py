import pytest

from app import create_app


PATH_FIELD_NAMES = {
    "file_path",
    "uploaded_file_path",
    "static_file_path",
    "upload_path",
    "original_image_path",
}


def test_api_download_pdf_rejects_client_supplied_file_paths(monkeypatch):
    app = create_app()
    client = app.test_client()

    def fail_if_called(*_args, **_kwargs):
        raise AssertionError("PDF generation should not run for client-supplied paths")

    monkeypatch.setattr("app.routes.generate_pdf_report", fail_if_called)

    response = client.post(
        "/api/download_pdf",
        json={
            "analysis_type": "cyberbullying",
            "analysis_result": {
                "analysis_type": "cyberbullying",
                "cyberbullying_analysis": "| sentence | risk |\n| hi | none |",
                "file_path": "/tmp/attacker-controlled-path.png",
            },
        },
    )

    assert response.status_code == 400
    assert response.get_json()["error"] == "Client-supplied file paths are not allowed."


def test_create_app_requires_secret_key_when_configured_for_deploy(monkeypatch):
    monkeypatch.delenv("SECRET_KEY", raising=False)
    monkeypatch.setenv("ANSIMTALK_REQUIRE_STABLE_SECRET", "1")

    with pytest.raises(RuntimeError, match="SECRET_KEY"):
        create_app()


def test_create_app_accepts_secret_key_when_configured_for_deploy(monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "stable-test-secret-key-for-deploy-check")
    monkeypatch.setenv("ANSIMTALK_REQUIRE_STABLE_SECRET", "1")

    app = create_app()

    assert app.config["SECRET_KEY"] == "stable-test-secret-key-for-deploy-check"
