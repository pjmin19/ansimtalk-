import os

# Flask 기본 설정
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-secret-key')

# Sightengine API (정확한 값 입력)
SIGHTENGINE_API_USER = "1052068557"
SIGHTENGINE_API_SECRET = "JbRcN79c6iunXBHG29WRzyQyFHRoYnQa"

# Google Cloud Vision/Gemini
GOOGLE_APPLICATION_CREDENTIALS = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS', 'dazzling-howl-465316-m7-6605bfd84de1.json')

# 실제 배포 시에는 환경변수 또는 별도 json 파일로 민감정보를 관리하세요.

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'tmp')
ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}