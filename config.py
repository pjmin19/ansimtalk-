import os
import secrets


SECRET_KEY = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

SIGHTENGINE_API_USER = os.environ.get("SIGHTENGINE_API_USER", "")
SIGHTENGINE_API_SECRET = os.environ.get("SIGHTENGINE_API_SECRET", "")

GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS", "")
GOOGLE_GEMINI_API_KEY = os.environ.get("GOOGLE_GEMINI_API_KEY", "")
GOOGLE_CLOUD_VISION_API_KEY = os.environ.get("GOOGLE_CLOUD_VISION_API_KEY", "")
GCP_PROJECT = os.environ.get("GCP_PROJECT", "")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "tmp")
ALLOWED_EXTENSIONS = {"txt", "png", "jpg", "jpeg"}


