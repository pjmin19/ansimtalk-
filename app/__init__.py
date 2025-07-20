import os
from flask import Flask
from .routes import bp

def create_app():
    app = Flask(__name__)
    
    # 로그 레벨을 DEBUG로 설정
    app.logger.setLevel('DEBUG')
    
    # 시크릿 키 설정
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ansimtalk-secret-key-2024')
    
    # 환경 변수에서 API 키들 가져오기
    app.config['SIGHTENGINE_API_USER'] = os.environ.get('SIGHTENGINE_API_USER', '1052068557')
    app.config['SIGHTENGINE_API_SECRET'] = os.environ.get('SIGHTENGINE_API_SECRET', 'JbRcN79c6iunXBHG29WRzyQyFHRoYnQa')
    app.config['GOOGLE_GEMINI_API_KEY'] = os.environ.get('GOOGLE_GEMINI_API_KEY', 'AIzaSyAZ__v5f-3pYxDfMi--rdCyphpcqsxxrLo')
    app.config['GOOGLE_CLOUD_VISION_API_KEY'] = os.environ.get('GOOGLE_CLOUD_VISION_API_KEY', 'your-vision-api-key-here')
    
    # Google Cloud Vision API 자격 증명 파일 경로 제거
    # app.config['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    
    # 블루프린트 등록
    app.register_blueprint(bp)
    
    return app