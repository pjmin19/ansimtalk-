from app import create_app
from app.services import analyze_image_with_sightengine


def test_create_app_uses_runtime_secret_key():
    app = create_app()
    secret_key = app.config["SECRET_KEY"]
    assert isinstance(secret_key, str)
    assert len(secret_key) >= 32
    assert "ansimtalk-secret-key" not in secret_key


def test_missing_sightengine_credentials_returns_safe_status():
    app = create_app()
    app.config["SIGHTENGINE_API_USER"] = ""
    app.config["SIGHTENGINE_API_SECRET"] = ""

    with app.app_context():
        result = analyze_image_with_sightengine("missing-file.jpg")

    assert result["status"] == "credentials_missing"
    assert "not configured" in result["error"]
