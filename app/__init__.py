import os
import secrets

from flask import Flask

from .routes import bp


def create_app():
    app = Flask(__name__)
    app.logger.setLevel(os.environ.get("LOG_LEVEL", "INFO"))

    secret_key = os.environ.get("SECRET_KEY")
    require_stable_secret = os.environ.get("ANSIMTALK_REQUIRE_STABLE_SECRET", "").lower()
    if not secret_key and require_stable_secret in {"1", "true", "yes"}:
        raise RuntimeError("SECRET_KEY is required when ANSIMTALK_REQUIRE_STABLE_SECRET is enabled.")

    # Never ship a hardcoded Flask secret. Local-only runs get an ephemeral key.
    app.config["SECRET_KEY"] = secret_key or secrets.token_hex(32)

    # API credentials must come from the runtime environment.
    app.config["SIGHTENGINE_API_USER"] = os.environ.get("SIGHTENGINE_API_USER", "")
    app.config["SIGHTENGINE_API_SECRET"] = os.environ.get("SIGHTENGINE_API_SECRET", "")
    app.config["GOOGLE_GEMINI_API_KEY"] = os.environ.get("GOOGLE_GEMINI_API_KEY", "")
    app.config["GOOGLE_CLOUD_VISION_API_KEY"] = os.environ.get("GOOGLE_CLOUD_VISION_API_KEY", "")

    # Optional local credential file path. Do not commit credential files.
    app.config["GOOGLE_APPLICATION_CREDENTIALS"] = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
    app.config["GCP_PROJECT"] = os.environ.get("GCP_PROJECT", "")

    app.register_blueprint(bp)
    return app


