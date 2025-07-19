import os

# Flask 기본 설정
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

# Sightengine API (환경 변수에서 가져옴)
SIGHTENGINE_API_USER = os.environ.get('SIGHTENGINE_API_USER', '')
SIGHTENGINE_API_SECRET = os.environ.get('SIGHTENGINE_API_SECRET', '')

# Google Cloud Vision/Gemini
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'dazzling-howl-465316-m7-6605bfd84de1.json')
GOOGLE_GEMINI_API_KEY = os.environ.get('GOOGLE_GEMINI_API_KEY', 'AIzaSyBQJQJQJQJQJQJQJQJQJQJQJQJQJQJQJQ')

# 실제 배포 시에는 환경변수로 민감정보를 관리하세요.

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'tmp')
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'} 