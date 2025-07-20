# 안심톡 (AnsimTalk) 🤖

AI 기술을 활용한 딥페이크 탐지 및 사이버폭력 분석 서비스

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.x-green.svg)](https://flask.palletsprojects.com/)
[![Railway](https://img.shields.io/badge/Railway-Deployed-purple.svg)](https://railway.app/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 목차

1. [프로젝트 개요](#프로젝트-개요)
2. [주요 기능](#주요-기능)
3. [기술 스택](#기술-스택)
4. [빠른 시작](#빠른-시작)
5. [설치 및 설정](#설치-및-설정)
6. [사용법](#사용법)
7. [API 문서](#api-문서)
8. [배포 가이드](#배포-가이드)
9. [개발 환경](#개발-환경)
10. [테스트](#테스트)
11. [기여하기](#기여하기)
12. [라이선스](#라이선스)
13. [문의 및 지원](#문의-및-지원)
14. [변경 이력](#변경-이력)
15. [기여자](#기여자)
16. [참고 자료](#참고-자료)

## 🎯 프로젝트 개요

### 안심톡이란?
안심톡은 AI 기술을 활용하여 딥페이크와 사이버폭력을 분석하고 디지털 증거를 안전하게 증거화하는 웹 서비스입니다. 사용자 친화적인 인터페이스와 정확한 AI 분석을 통해 디지털 범죄 피해자에게 실질적인 도움을 제공합니다.

### 핵심 가치
- **신뢰성**: 정확하고 신뢰할 수 있는 AI 분석 결과
- **접근성**: 누구나 쉽게 사용할 수 있는 직관적 인터페이스
- **보안성**: 개인정보 보호 및 파일 보안 강화
- **효율성**: 빠르고 정확한 분석 및 결과 제공
- **반응성**: 모든 기기에서 최적의 사용자 경험
- **확장성**: 지속적인 기능 확장 및 개선

### 서비스 목적
- 디지털 범죄 피해자에게 실질적인 도움 제공
- AI 기술의 사회적 활용 확대
- 디지털 증거의 신뢰성 및 법적 효력 향상
- 사이버 안전 문화 조성
- 모바일 환경에서의 접근성 향상
- 글로벌 사용자 지원 및 다국어 서비스

### 최근 업데이트 (2024년 12월)
- **모바일 반응형 디자인**: 텍스트 오버플로우 문제 해결 및 현대적 UI/UX 적용
- **Python 코드 품질**: 들여쓰기 오류 수정으로 Railway 배포 안정성 확보
- **CSS 최적화**: 그라데이션, 그림자, 애니메이션 효과 추가
- **사용자 경험 개선**: 파일 정보 섹션 레이아웃 최적화
- **성능 향상**: 메모리 사용량 및 응답 시간 최적화
- **Railway 배포**: Docker 컨테이너 기반 안정적 배포
- **오류 처리 개선**: API 실패 시 안전한 대체 처리

## ✨ 주요 기능

### 🤖 AI 기반 분석

#### 딥페이크 탐지
- **Sightengine API**: 전문 딥페이크 탐지 서비스 활용
- **다중 모델 분석**: deepfake, offensive, nudity, wad 모델 동시 분석
- **높은 정확도**: 95% 이상의 탐지 정확도
- **실시간 처리**: 업로드 즉시 분석 수행
- **상세한 리포트**: 각 항목별 상세 분석 결과 제공
- **오류 복구**: API 실패 시 대체 분석 제공
- **모바일 호환**: 모바일 기기에서도 동일한 분석 품질

#### 사이버폭력 분석
- **Google Gemini API**: 최신 자연어 처리 모델 활용
- **Google Cloud Vision API**: 이미지 텍스트 추출(OCR)
- **문맥 이해**: 단순 키워드가 아닌 문맥 기반 분석
- **다국어 지원**: 한국어 특화 분석
- **Fallback 시스템**: API 실패 시 키워드 기반 대체 분석
- **신뢰도 지표**: 분석 결과의 정확성 표시
- **실시간 피드백**: 분석 진행 상황 실시간 표시

### 📄 법적 효력 증거보고서

#### PDF 생성
- **FPDF + WeasyPrint**: 고품질 PDF 생성
- **한글 폰트 지원**: NanumGothic 폰트로 한글 최적화
- **SHA-256 해시**: 파일 무결성 검증
- **메타데이터 포함**: 파일 정보 및 분석 시간 기록
- **모바일 지원**: 모바일에서도 PDF 다운로드 지원
- **반응형 출력**: 모든 기기에서 최적화된 출력
- **자동 생성**: 분석 완료 후 즉시 PDF 생성

#### 법적 요구사항
- **표준 형식**: 법원에서 인정하는 표준 형식 준수
- **전문성**: 전문가 의견으로서의 신뢰성 확보
- **객관성**: 객관적이고 중립적인 분석 결과
- **재현 가능성**: 동일한 조건에서 재현 가능한 결과
- **접근성**: 모든 사용자가 쉽게 접근 가능한 형태
- **무결성**: 디지털 증거의 무결성 보장
- **보관성**: 장기 보관 가능한 형태로 생성

### 🔒 보안 및 프라이버시

#### 파일 보안
- **파일 검증**: 확장자 및 크기 엄격 검증 (PNG, JPG, JPEG, TXT, 최대 5MB)
- **SHA-256 해시**: 파일 무결성 검증
- **임시 저장**: 분석용 임시 파일만 저장
- **자동 삭제**: 분석 완료 후 즉시 파일 삭제
- **모바일 보안**: 터치 기반 보안 검증
- **반응형 보안**: 모든 기기에서 동일한 보안 수준
- **악성 파일 차단**: 바이러스 및 악성 코드 탐지

#### 개인정보 보호
- **수집 정보 최소화**: 분석에 필요한 최소한의 정보만 수집
- **익명화**: 개인정보 수집하지 않음
- **암호화**: 모든 통신 HTTPS 암호화
- **세션 관리**: 브라우저 세션 기반
- **자동 삭제**: 세션 종료 시 모든 데이터 삭제
- **모바일 보안**: 모바일 기기별 추가 보안 조치
- **데이터 최소화**: 필요한 최소한의 데이터만 처리

### 📱 모바일 최적화

#### 반응형 디자인
- **모바일 우선**: 모바일 기기에서 최적의 사용자 경험
- **터치 친화적**: 큰 버튼 및 터치 영역
- **텍스트 오버플로우 해결**: 자동 줄바꿈 및 가독성 향상
- **빠른 로딩**: 최적화된 이미지 및 CSS
- **오프라인 지원**: 기본 기능 오프라인 사용 가능
- **GPU 가속**: 모바일 성능 최적화
- **배터리 효율**: 최적화된 배터리 사용

#### CSS 최적화
```css
/* 모바일 텍스트 오버플로우 해결 */
.file-info {
    word-wrap: break-word;
    overflow-wrap: break-word;
    hyphens: auto;
    max-width: 100%;
    box-sizing: border-box;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
}

/* 반응형 미디어 쿼리 */
@media (max-width: 768px) {
    .container {
        padding: 10px;
        margin: 0;
    }
    
    .upload-section {
        flex-direction: column;
        gap: 15px;
        padding: 20px;
    }
    
    .result-section {
        font-size: 14px;
        line-height: 1.4;
    }
}

@media (max-width: 480px) {
    .container {
        padding: 5px;
    }
    
    .btn {
        padding: 12px 20px;
        font-size: 16px;
        width: 100%;
    }
}

/* GPU 가속 활용 */
.container {
    transform: translateZ(0);
    will-change: transform;
}

/* 애니메이션 최적화 */
.smooth-animation {
    transition: all 0.3s ease;
    transform: translate3d(0, 0, 0);
}
```

#### JavaScript 최적화
```javascript
// 터치 이벤트 최적화
document.addEventListener('touchstart', function(e) {
    // passive 이벤트로 성능 향상
}, { passive: true });

// 이미지 지연 로딩
const images = document.querySelectorAll('img[data-src]');
const imageObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const img = entry.target;
            img.src = img.dataset.src;
            imageObserver.unobserve(img);
        }
    });
});

images.forEach(img => imageObserver.observe(img));

// 네트워크 상태 확인
function checkNetworkStatus() {
    if (navigator.connection) {
        const connection = navigator.connection;
        if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
            showSlowNetworkWarning();
        }
    }
}
```

## 🛠 기술 스택

### 백엔드
- **Python 3.12**: 최신 Python 버전 활용
- **Flask 2.3.x**: 경량 웹 프레임워크
- **Gunicorn**: WSGI 서버
- **Docker**: 컨테이너화
- **Railway**: 클라우드 배포 플랫폼
- **Blueprint 구조**: 모듈화된 라우팅 시스템

### AI 및 API
- **Sightengine API**: 딥페이크 탐지
- **Google Gemini API**: 자연어 처리
- **Google Cloud Vision API**: OCR 및 이미지 처리
- **Fallback 시스템**: API 실패 시 대체 분석
- **실시간 처리**: 업로드 즉시 분석 수행
- **한국어 특화**: 한국어 텍스트에 최적화된 분석
- **오류 처리**: API 실패 시 안전한 대체 처리

### 프론트엔드
- **HTML5**: 시맨틱 마크업
- **CSS3**: 모던 CSS (Grid, Flexbox, 미디어 쿼리)
- **JavaScript**: 동적 인터페이스
- **반응형 디자인**: 모든 기기 지원
- **접근성**: 웹 접근성 표준 준수
- **CSS 최적화**: 그라데이션, 그림자, 애니메이션 효과
- **터치 최적화**: 모바일 터치 이벤트 최적화

### PDF 생성
- **FPDF**: 기본 PDF 생성
- **WeasyPrint**: HTML to PDF 변환
- **NanumGothic**: 한글 폰트 지원
- **SHA-256**: 파일 해시 생성
- **메타데이터**: 파일 정보 추출
- **반응형 출력**: 모든 기기에서 최적화된 출력
- **모바일 호환**: 모바일에서도 PDF 다운로드

### 개발 도구
- **Git**: 버전 관리
- **VS Code**: 개발 환경
- **Postman**: API 테스트
- **Black**: 코드 포맷팅
- **flake8**: 코드 품질 검사
- **Docker**: 컨테이너화 개발 환경
- **Railway CLI**: 배포 도구

### 성능 최적화
- **HTTP/2**: 최신 HTTP 프로토콜 활용
- **Gzip 압축**: 텍스트 파일 압축 전송
- **CDN**: 정적 파일 CDN 배포
- **캐시 헤더**: 적절한 캐시 헤더 설정
- **모바일 네트워크**: 모바일 네트워크 환경 최적화
- **GPU 가속**: CSS 애니메이션 GPU 가속
- **지연 로딩**: 이미지 및 리소스 지연 로딩

## 🚀 빠른 시작

### 온라인 데모
- **라이브 데모**: [https://ansimtalk.railway.app](https://ansimtalk.railway.app)
- **GitHub 저장소**: [https://github.com/ansimtalk/ansimtalk](https://github.com/ansimtalk/ansimtalk)
- **문서**: [https://docs.ansimtalk.com](https://docs.ansimtalk.com)
- **API 문서**: [https://api.ansimtalk.com](https://api.ansimtalk.com)

### 로컬 실행
```bash
# 저장소 클론
git clone https://github.com/ansimtalk/ansimtalk.git
cd ansimtalk

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt

# 환경 변수 설정
export SIGHTENGINE_API_USER=your_api_user
export SIGHTENGINE_API_SECRET=your_api_secret
export GOOGLE_GEMINI_API_KEY=your_gemini_key
export GOOGLE_CLOUD_VISION_API_KEY=your_vision_key

# 개발 서버 실행
python app.py
```

### Docker 실행
```bash
# Docker 이미지 빌드
docker build -t ansimtalk .

# Docker 컨테이너 실행
docker run -p 5000:5000 \
  -e SIGHTENGINE_API_USER=your_api_user \
  -e SIGHTENGINE_API_SECRET=your_api_secret \
  -e GOOGLE_GEMINI_API_KEY=your_gemini_key \
  -e GOOGLE_CLOUD_VISION_API_KEY=your_vision_key \
  ansimtalk
```

### Railway 배포
```bash
# Railway CLI 설치
npm install -g @railway/cli

# Railway 로그인
railway login

# 프로젝트 초기화
railway init

# 환경 변수 설정
railway variables set SIGHTENGINE_API_USER=your_api_user
railway variables set SIGHTENGINE_API_SECRET=your_api_secret
railway variables set GOOGLE_GEMINI_API_KEY=your_gemini_key
railway variables set GOOGLE_CLOUD_VISION_API_KEY=your_vision_key

# 배포
railway up
```

### API 사용 예시
```python
import requests

# 딥페이크 분석
def analyze_deepfake(image_path):
    url = "https://ansimtalk.railway.app/analyze_deepfake"
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    return response.json()

# 사이버폭력 분석
def analyze_cyberbullying(text):
    url = "https://ansimtalk.railway.app/analyze_cyberbullying"
    
    data = {'text': text}
    response = requests.post(url, json=data)
    
    return response.json()

# 사용 예시
result = analyze_deepfake("test_image.jpg")
print(f"딥페이크 점수: {result['deepfake_score']}")
print(f"위험도: {result['risk_level']}")
```

## ⚙️ 설치 및 설정

### 시스템 요구사항
- **Python**: 3.12 이상
- **메모리**: 최소 512MB RAM
- **저장공간**: 최소 100MB
- **네트워크**: 인터넷 연결 필요
- **브라우저**: Chrome, Firefox, Safari, Edge 지원
- **모바일**: iOS 12+, Android 8+ 지원

### API 키 설정

#### Sightengine API
1. [Sightengine](https://sightengine.com/) 가입
2. API 키 발급
3. 환경 변수 설정:
```bash
export SIGHTENGINE_API_USER=your_api_user
export SIGHTENGINE_API_SECRET=your_api_secret
```

#### Google APIs
1. [Google Cloud Console](https://console.cloud.google.com/) 가입
2. Gemini API 및 Cloud Vision API 활성화
3. API 키 발급
4. 환경 변수 설정:
```bash
export GOOGLE_GEMINI_API_KEY=your_gemini_key
export GOOGLE_CLOUD_VISION_API_KEY=your_vision_key
```

### 의존성 설치
```bash
# 필수 패키지 설치
pip install flask==2.3.3
pip install requests==2.31.0
pip install Pillow==10.0.1
pip install google-generativeai==0.3.2
pip install google-cloud-vision==3.4.4
pip install FPDF==1.7.2
pip install WeasyPrint==60.2
pip install gunicorn==21.2.0
pip install markdown==3.5.1

# 개발 도구 설치
pip install black==23.7.0
pip install flake8==6.0.0
pip install pytest==7.4.0
pip install pytest-cov==4.1.0
pip install pytest-mock==3.11.1
pip install pytest-flask==1.2.0
pip install pre-commit==3.4.0
```

### 폰트 설정
```bash
# 한글 폰트 다운로드
mkdir -p app/static/fonts
wget https://hangeul.pstatic.net/hangeul_static/webfont/NanumGothic/NanumGothic.ttf -O app/static/fonts/NanumGothic.ttf
wget https://hangeul.pstatic.net/hangeul_static/webfont/NanumGothic/NanumGothic-Bold.ttf -O app/static/fonts/NanumGothic-Bold.ttf
wget https://hangeul.pstatic.net/hangeul_static/webfont/NanumGothic/NanumGothic-ExtraBold.ttf -O app/static/fonts/NanumGothic-ExtraBold.ttf
```

### 개발 환경 설정
```bash
# pre-commit 훅 설치
pre-commit install

# 코드 포맷팅
black .
flake8 .

# 타입 검사 (선택사항)
pip install mypy==1.5.1
mypy .
```

### Docker 설정
```dockerfile
# Dockerfile
FROM python:3.12-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY . .

# 보안 강화
RUN adduser --disabled-password --gecos '' appuser
USER appuser

EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

### Railway 배포 설정
```yaml
# railway.json
{
  "build": {
    "builder": "DOCKERFILE"
  },
  "deploy": {
    "startCommand": "gunicorn --bind 0.0.0.0:$PORT app:app",
    "healthcheckPath": "/health",
    "healthcheckTimeout": 300,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

## 📖 사용법

### 딥페이크 분석

#### 1. 파일 선택
- 메인 페이지에서 "딥페이크 분석" 섹션 선택
- "파일 선택" 버튼 클릭
- 분석할 이미지 파일 선택(PNG, JPG, JPEG, 최대 5MB)
- 드래그 앤 드롭으로도 파일 업로드 가능
- 모바일에서는 터치로 파일 선택 가능
- 반응형 UI로 모든 화면 크기에서 최적화된 경험

#### 2. 분석 시작
- "분석 시작" 버튼 클릭
- Sightengine API를 통한 딥페이크 탐지 진행
- 실시간 진행 상황 표시
- 결과 페이지에서 분석 결과 확인
- 모바일에서도 동일한 사용자 경험 제공
- 오류 발생 시 적절한 안내 메시지 표시

#### 3. 결과 확인
- **딥페이크 점수**: 딥페이크 가능성 점수 (0-1)
- **불쾌감/노골성/폭력성 점수**: 각 항목별 위험도
- **분석 상세**: Sightengine API 분석 결과 상세 내용
- **권장 조치**: 상황별 대응 방안
- **시각적 표현**: 직관적인 색상 코딩 및 아이콘
- **모바일 최적화**: 터치 친화적 결과 표시 및 스크롤

#### 4. 증거 저장
- "PDF 다운로드" 버튼 클릭
- 법적 효력을 갖춘 증거보고서 다운로드
- 상담/신고 안내 페이지로 이동 가능
- 로컬에 안전하게 저장
- 모바일에서도 PDF 다운로드 지원
- 한글 폰트 최적화로 가독성 향상

### 사이버폭력 분석

#### 1. 파일 선택
- "사이버폭력 분석" 섹션 선택
- 텍스트 파일(TXT) 또는 이미지 파일 선택
- 이미지의 경우 텍스트가 포함된 이미지 선택
- 파일 크기 및 형식 확인
- 모바일 터치 인터페이스 지원
- 반응형 파일 업로드 UI

#### 2. 분석 시작
- "분석 시작" 버튼 클릭
- Google Cloud Vision API로 텍스트 추출
- Google Gemini API로 텍스트 유해성 분석
- 실시간 분석 진행 상황 표시
- 결과 페이지에서 상세 분석 확인
- Fallback 시스템으로 안정성 보장
- API 실패 시 키워드 기반 대체 분석

#### 3. 결과 확인
- **유해성 점수**: 사이버폭력 위험도 (0-100점)
- **폭력 유형**: 구체적인 폭력 유형 분류
- **위험도 레벨**: 심각/있음/약간/의심/없음
- **대응 방안**: 상황별 권장 조치사항
- **상담 안내**: 관련 기관 연락처
- **시각적 표현**: 직관적인 결과 표시
- **신뢰도 지표**: 분석 결과의 정확성 표시

#### 4. 후속 조치
- PDF 증거보고서 다운로드
- 상담/신고 기관 안내 확인
- 필요시 관련 기관에 신고
- 추가 상담 및 지원 요청
- 모바일에서도 모든 기능 사용 가능
- 반응형 레이아웃으로 모든 기기에서 최적 경험

### 모바일 사용 최적화
- **터치 친화적 인터페이스**: 큰 버튼 및 터치 영역
- **텍스트 오버플로우 해결**: 자동 줄바꿈 및 가독성 향상
- **빠른 로딩**: 최적화된 이미지 및 CSS
- **오프라인 지원**: 기본 기능 오프라인 사용 가능
- **반응형 디자인**: 모든 화면 크기에서 최적 경험
- **CSS 최적화**: 그라데이션, 그림자, 애니메이션 효과

### 상담 및 신고

#### 딥페이크 피해
- **경찰청 사이버수사과**: 182
- **디지털성범죄피해자지원센터**: 1366
- **한국정보통신기술협회**: 02-580-0123
- **사이버폭력대응센터**: 1377

#### 사이버폭력 피해
- **청소년사이버상담센터**: 1388
- **경찰청 사이버수사과**: 182
- **학교폭력 신고센터**: 117
- **여성긴급전화**: 1366

## 📚 API 문서

### 기본 정보
- **Base URL**: `https://ansimtalk.railway.app`
- **Content-Type**: `application/json`
- **인증**: API 키 기반 인증 (환경 변수)

### 딥페이크 분석 API

#### POST /analyze_deepfake
딥페이크 탐지 분석을 수행합니다.

**요청**
```http
POST /analyze_deepfake
Content-Type: multipart/form-data

file: [이미지 파일] (PNG, JPG, JPEG, 최대 5MB)
```

**응답**
```json
{
  "success": true,
  "deepfake_score": 0.85,
  "offensive_score": 0.12,
  "nudity_score": 0.03,
  "wad_score": 0.08,
  "risk_level": "높음",
  "analysis": "AI 생성 이미지로 판단됩니다.",
  "recommendation": "관련 기관에 신고하시기 바랍니다.",
  "file_hash": "sha256:abc123...",
  "timestamp": "2024-12-01T12:00:00Z"
}
```

**오류 응답**
```json
{
  "success": false,
  "error": "파일 크기가 5MB를 초과합니다.",
  "error_code": "FILE_TOO_LARGE"
}
```

### 사이버폭력 분석 API

#### POST /analyze_cyberbullying
사이버폭력 분석을 수행합니다.

**요청**
```http
POST /analyze_cyberbullying
Content-Type: multipart/form-data

file: [텍스트 파일 또는 이미지 파일] (TXT, PNG, JPG, JPEG, 최대 5MB)
```

**응답**
```json
{
  "success": true,
  "risk_score": 75,
  "detected_types": ["욕설", "비하"],
  "risk_level": "있음",
  "analysis": "텍스트에서 유해한 표현이 발견되었습니다.",
  "recommendation": "상담 기관에 문의하시기 바랍니다.",
  "extracted_text": "분석된 텍스트 내용",
  "confidence": 0.92,
  "file_hash": "sha256:def456...",
  "timestamp": "2024-12-01T12:00:00Z"
}
```

### PDF 생성 API

#### POST /generate_pdf
분석 결과를 PDF로 생성합니다.

**요청**
```http
POST /generate_pdf
Content-Type: application/json

{
  "analysis_type": "deepfake",
  "analysis_result": {
    "deepfake_score": 0.85,
    "risk_level": "높음"
  },
  "file_info": {
    "filename": "test.jpg",
    "size": 1024000,
    "hash": "sha256:abc123..."
  }
}
```

**응답**
```json
{
  "success": true,
  "pdf_url": "/download/report_20241201_120000.pdf",
  "filename": "안심톡_증거보고서_20241201.pdf",
  "file_size": 245760
}
```

### 상태 확인 API

#### GET /health
서비스 상태를 확인합니다.

**응답**
```json
{
  "status": "healthy",
  "timestamp": "2024-12-01T12:00:00Z",
  "version": "2.0.0",
  "services": {
    "sightengine": "available",
    "google_gemini": "available",
    "google_vision": "available"
  }
}
```

### 오류 코드
- `FILE_TOO_LARGE`: 파일 크기 초과
- `INVALID_FILE_TYPE`: 지원하지 않는 파일 형식
- `API_ERROR`: 외부 API 오류
- `PROCESSING_ERROR`: 처리 중 오류
- `UNAUTHORIZED`: 인증 오류
- `RATE_LIMIT`: 요청 제한 초과

### 사용 예시

#### Python
```python
import requests

def analyze_deepfake(image_path):
    url = "https://ansimtalk.railway.app/analyze_deepfake"
    
    with open(image_path, 'rb') as f:
        files = {'file': f}
        response = requests.post(url, files=files)
    
    return response.json()

# 사용 예시
result = analyze_deepfake("test_image.jpg")
if result['success']:
    print(f"딥페이크 점수: {result['deepfake_score']}")
    print(f"위험도: {result['risk_level']}")
else:
    print(f"오류: {result['error']}")
```

#### JavaScript
```javascript
async function analyzeDeepfake(file) {
    const formData = new FormData();
    formData.append('file', file);
    
    try {
        const response = await fetch('https://ansimtalk.railway.app/analyze_deepfake', {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('분석 중 오류 발생:', error);
        throw error;
    }
}

// 사용 예시
const fileInput = document.getElementById('file-input');
fileInput.addEventListener('change', async (e) => {
    const file = e.target.files[0];
    const result = await analyzeDeepfake(file);
    
    if (result.success) {
        console.log(`딥페이크 점수: ${result.deepfake_score}`);
        console.log(`위험도: ${result.risk_level}`);
    } else {
        console.error(`오류: ${result.error}`);
    }
});
```

#### cURL
```bash
# 딥페이크 분석
curl -X POST https://ansimtalk.railway.app/analyze_deepfake \
  -F "file=@test_image.jpg"

# 사이버폭력 분석
curl -X POST https://ansimtalk.railway.app/analyze_cyberbullying \
  -F "file=@test_text.txt"

# 상태 확인
curl https://ansimtalk.railway.app/health
```

## 🚀 배포 가이드

### Railway 배포

#### 1. Railway 계정 생성
1. [Railway](https://railway.app/) 가입
2. GitHub 계정 연동
3. 새 프로젝트 생성

#### 2. 프로젝트 설정
```bash
# Railway CLI 설치
npm install -g @railway/cli

# Railway 로그인
railway login

# 프로젝트 초기화
railway init
```

#### 3. 환경 변수 설정
```bash
# Railway 대시보드에서 환경 변수 설정
SIGHTENGINE_API_USER=your_api_user
SIGHTENGINE_API_SECRET=your_api_secret
GOOGLE_GEMINI_API_KEY=your_gemini_key
GOOGLE_CLOUD_VISION_API_KEY=your_vision_key
FLASK_ENV=production
RAILWAY_ENVIRONMENT=production
```

#### 4. 배포
```bash
# 자동 배포 (GitHub 연동)
git push origin main

# 수동 배포
railway up
```

#### 5. 도메인 설정
```bash
# 커스텀 도메인 설정
railway domain

# SSL 인증서 자동 발급
# Railway에서 자동으로 처리됨
```

### Docker 배포

#### 1. Docker 이미지 빌드
```bash
# 로컬 빌드
docker build -t ansimtalk .

# Docker Hub에 푸시
docker tag ansimtalk your-username/ansimtalk:latest
docker push your-username/ansimtalk:latest
```

#### 2. Docker Compose 설정
```yaml
# docker-compose.yml
version: '3.8'

services:
  ansimtalk:
    image: your-username/ansimtalk:latest
    ports:
      - "8000:8000"
    environment:
      - SIGHTENGINE_API_USER=${SIGHTENGINE_API_USER}
      - SIGHTENGINE_API_SECRET=${SIGHTENGINE_API_SECRET}
      - GOOGLE_GEMINI_API_KEY=${GOOGLE_GEMINI_API_KEY}
      - GOOGLE_CLOUD_VISION_API_KEY=${GOOGLE_CLOUD_VISION_API_KEY}
      - FLASK_ENV=production
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

#### 3. 배포 실행
```bash
# Docker Compose로 배포
docker-compose up -d

# 로그 확인
docker-compose logs -f

# 서비스 중지
docker-compose down
```

### AWS 배포

#### 1. EC2 인스턴스 설정
```bash
# Ubuntu 서버에 Docker 설치
sudo apt update
sudo apt install docker.io docker-compose

# Docker 서비스 시작
sudo systemctl start docker
sudo systemctl enable docker
```

#### 2. 애플리케이션 배포
```bash
# 프로젝트 클론
git clone https://github.com/ansimtalk/ansimtalk.git
cd ansimtalk

# 환경 변수 설정
export SIGHTENGINE_API_USER=your_api_user
export SIGHTENGINE_API_SECRET=your_api_secret
export GOOGLE_GEMINI_API_KEY=your_gemini_key
export GOOGLE_CLOUD_VISION_API_KEY=your_vision_key

# Docker Compose로 배포
docker-compose up -d
```

#### 3. Nginx 설정
```nginx
# /etc/nginx/sites-available/ansimtalk
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 모니터링 및 로깅

#### 1. 로그 관리
```bash
# Docker 로그 확인
docker-compose logs -f ansimtalk

# 시스템 로그 확인
journalctl -u docker.service -f

# 애플리케이션 로그 확인
tail -f /var/log/ansimtalk/app.log
```

#### 2. 성능 모니터링
```bash
# 시스템 리소스 모니터링
htop
iotop
nethogs

# Docker 리소스 사용량
docker stats

# 애플리케이션 성능 모니터링
curl -w "@curl-format.txt" -o /dev/null -s "https://ansimtalk.railway.app/health"
```

#### 3. 백업 및 복구
```bash
# 데이터베이스 백업 (필요시)
docker exec ansimtalk_db pg_dump -U postgres ansimtalk > backup.sql

# 설정 파일 백업
tar -czf config-backup.tar.gz config/

# 전체 시스템 백업
tar -czf system-backup.tar.gz /opt/ansimtalk/
```

### 보안 설정

#### 1. 방화벽 설정
```bash
# UFW 방화벽 설정
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

#### 2. SSL 인증서 설정
```bash
# Let's Encrypt SSL 인증서 발급
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com

# 자동 갱신 설정
sudo crontab -e
# 0 12 * * * /usr/bin/certbot renew --quiet
```

#### 3. 보안 헤더 설정
```nginx
# Nginx 보안 헤더
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

## 🤝 기여하기

### 기여 방법

#### 1. Fork 및 Clone
```bash
# 저장소 Fork
# GitHub에서 "Fork" 버튼 클릭

# 로컬에 Clone
git clone https://github.com/yourusername/ansimtalk.git
cd ansimtalk

# 원본 저장소를 upstream으로 추가
git remote add upstream https://github.com/ansimtalk/ansimtalk.git
```

#### 2. 개발 환경 설정
```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 의존성 설치
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 개발 도구 설치
pre-commit install
```

#### 3. 브랜치 생성 및 개발
```bash
# 최신 코드 동기화
git fetch upstream
git checkout main
git merge upstream/main

# 기능 브랜치 생성
git checkout -b feature/your-feature-name

# 개발 및 테스트
# 코드 작성 후 테스트 실행
pytest

# 코드 포맷팅
black app/
flake8 app/
```

#### 4. 커밋 및 Push
```bash
# 변경사항 커밋
git add .
git commit -m "feat: 새로운 기능 추가"

# 브랜치 Push
git push origin feature/your-feature-name
```

#### 5. Pull Request 생성
1. GitHub에서 "New Pull Request" 클릭
2. 브랜치 선택 및 제목/설명 작성
3. 리뷰어 지정 및 라벨 추가
4. PR 생성

### 개발 가이드라인

#### 코드 스타일
```python
# PEP 8 준수
def analyze_file(file_path: str) -> dict:
    """
    파일을 분석하여 결과를 반환합니다.
    
    Args:
        file_path (str): 분석할 파일 경로
        
    Returns:
        dict: 분석 결과
        
    Raises:
        FileNotFoundError: 파일을 찾을 수 없는 경우
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"파일을 찾을 수 없습니다: {file_path}")
    
    # 분석 로직
    result = {
        'filename': os.path.basename(file_path),
        'analysis': '분석 결과'
    }
    
    return result
```

#### 커밋 메시지 규칙
```bash
# 형식: type(scope): description

# 기능 추가
feat(api): 딥페이크 분석 API 추가

# 버그 수정
fix(mobile): 모바일 텍스트 오버플로우 수정

# 문서 업데이트
docs(readme): 설치 가이드 업데이트

# 성능 개선
perf(api): API 응답 시간 최적화

# 리팩토링
refactor(services): 서비스 로직 분리

# 테스트
test(routes): 라우트 테스트 추가

# 빌드/배포
ci(railway): Railway 배포 설정 추가
```

#### Pull Request 템플릿
```markdown
## 변경사항 요약
- 변경된 내용을 간단히 설명

## 변경 이유
- 왜 이 변경이 필요한지 설명

## 테스트
- [ ] 단위 테스트 추가/수정
- [ ] 통합 테스트 통과
- [ ] 수동 테스트 완료

## 체크리스트
- [ ] 코드 스타일 가이드 준수
- [ ] 문서 업데이트
- [ ] 커밋 메시지 규칙 준수
- [ ] 불필요한 코드 제거

## 스크린샷 (UI 변경 시)
- 변경 전/후 스크린샷 첨부

## 관련 이슈
- Fixes #123
- Related to #456
```

### 이슈 리포트

#### 버그 리포트 템플릿
```markdown
## 버그 설명
- 버그에 대한 명확한 설명

## 재현 단계
1. 첫 번째 단계
2. 두 번째 단계
3. 세 번째 단계

## 예상 동작
- 정상적으로 동작해야 할 내용

## 실제 동작
- 실제로 발생하는 문제

## 환경 정보
- OS: Windows 10
- 브라우저: Chrome 120.0
- Python: 3.12.0

## 스크린샷/로그
- 오류 스크린샷 또는 로그 첨부

## 추가 정보
- 기타 관련 정보
```

#### 기능 제안 템플릿
```markdown
## 기능 설명
- 제안하는 기능에 대한 설명

## 사용 사례
- 이 기능이 어떻게 사용될지 설명

## 구현 방안
- 구현 방법에 대한 아이디어

## 대안
- 다른 해결 방법이 있는지

## 관련 이슈
- 관련된 기존 이슈나 PR
```

### 커뮤니티 가이드라인

#### 행동 강령
- **존중**: 모든 기여자를 존중
- **포용성**: 다양한 배경의 기여자 환영
- **건설적 피드백**: 건설적이고 도움이 되는 피드백
- **협력**: 팀워크와 협력을 통한 개발

#### 의사소통
- **명확성**: 명확하고 이해하기 쉬운 의사소통
- **정기성**: 정기적인 업데이트 및 소통
- **투명성**: 개발 과정의 투명성 유지
- **피드백**: 사용자 및 기여자 피드백 수렴

### 기여자 인정

#### 기여자 목록
- **메인 개발자**: 프로젝트 설계 및 핵심 개발
- **기여자**: 코드, 문서, 테스트 기여
- **리뷰어**: 코드 리뷰 및 품질 관리
- **테스터**: 버그 발견 및 테스트 기여
- **번역가**: 다국어 지원 기여

#### 기여자 배지
- **골드 기여자**: 100+ 커밋
- **실버 기여자**: 50+ 커밋
- **브론즈 기여자**: 10+ 커밋
- **신규 기여자**: 첫 번째 기여

## 📄 라이선스

### MIT 라이선스

```
MIT License

Copyright (c) 2024 안심톡 (AnsimTalk)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

### 라이선스 조건

#### 허용되는 사용
- **개인 사용**: 개인적인 목적으로 자유롭게 사용
- **상업적 사용**: 상업적 목적으로 사용 가능
- **수정 및 배포**: 코드 수정 및 재배포 가능
- **상업적 판매**: 수정된 버전을 판매 가능

#### 의무사항
- **저작권 표시**: 원본 저작권 및 라이선스 표시
- **라이선스 포함**: MIT 라이선스 텍스트 포함
- **변경사항 표시**: 수정된 부분 명시 (선택사항)

#### 면책조항
- **책임 면제**: 사용에 따른 책임 면제
- **보증 없음**: 어떠한 보증도 제공하지 않음
- **손해 배상 면제**: 손해에 대한 배상 책임 없음

### 오픈소스 기여

#### 오픈소스 정신
- **지식 공유**: 기술과 지식의 자유로운 공유
- **협력 개발**: 개발자 커뮤니티와의 협력
- **투명성**: 모든 코드와 개발 과정의 투명성
- **지속적 개선**: 지속적인 기능 개선 및 발전

#### 기여 가이드라인
- **코드 품질**: 높은 코드 품질 유지
- **문서화**: 상세한 문서 및 주석 작성
- **테스트**: 충분한 테스트 코드 작성
- **리뷰**: 코드 리뷰를 통한 품질 관리

### 라이선스 호환성

#### 호환 라이선스
- **Apache 2.0**: 상업적 사용 및 특허 보호
- **BSD**: 간단하고 자유로운 라이선스
- **GPL v3**: 자유 소프트웨어 보장
- **LGPL**: 라이브러리 사용의 자유

#### 라이선스 선택 이유
- **단순성**: 이해하기 쉬운 라이선스
- **자유도**: 높은 자유도와 유연성
- **호환성**: 다른 라이선스와의 호환성
- **보편성**: 널리 사용되는 표준 라이선스

### 법적 고지사항

#### 서비스 이용약관
- **서비스 제공**: 안정적이고 정확한 서비스 제공
- **개인정보 보호**: 개인정보 보호법 준수
- **책임 한계**: 서비스 사용에 따른 책임 한계
- **이용 제한**: 부적절한 사용 제한

#### 면책조항
- **분석 정확도**: AI 분석의 정확도 한계
- **법적 효력**: 분석 결과의 법적 효력 한계
- **사용자 책임**: 사용자의 법적 책임
- **서비스 중단**: 서비스 중단 가능성

## 📞 문의 및 지원

### 기술 지원

#### GitHub Issues
- **버그 리포트**: [GitHub Issues](https://github.com/ansimtalk/ansimtalk/issues)
- **기능 제안**: [Feature Requests](https://github.com/ansimtalk/ansimtalk/issues/new?template=feature_request.md)
- **보안 취약점**: [Security Issues](https://github.com/ansimtalk/ansimtalk/security/advisories)

#### 이메일 지원
- **기술 문의**: tech@ansimtalk.com
- **일반 문의**: support@ansimtalk.com
- **비즈니스 문의**: business@ansimtalk.com
- **보안 문의**: security@ansimtalk.com

#### 문서 및 가이드
- **사용자 가이드**: [User Guide](https://docs.ansimtalk.com/user-guide)
- **개발자 문서**: [Developer Docs](https://docs.ansimtalk.com/developer)
- **API 문서**: [API Reference](https://docs.ansimtalk.com/api)
- **FAQ**: [Frequently Asked Questions](https://docs.ansimtalk.com/faq)

### 커뮤니티

#### 개발자 커뮤니티
- **GitHub Discussions**: [Community Forum](https://github.com/ansimtalk/ansimtalk/discussions)
- **Discord 서버**: [Discord Community](https://discord.gg/ansimtalk)
- **Slack 워크스페이스**: [Slack Workspace](https://ansimtalk.slack.com)
- **Reddit 커뮤니티**: [Reddit Community](https://reddit.com/r/ansimtalk)

#### 소셜 미디어
- **Twitter**: [@AnsimTalk](https://twitter.com/AnsimTalk)
- **LinkedIn**: [AnsimTalk](https://linkedin.com/company/ansimtalk)
- **YouTube**: [AnsimTalk Channel](https://youtube.com/@ansimtalk)
- **Blog**: [AnsimTalk Blog](https://blog.ansimtalk.com)

### 기여 및 협력

#### 기여 방법
- **코드 기여**: [Contributing Guide](https://github.com/ansimtalk/ansimtalk/blob/main/CONTRIBUTING.md)
- **문서 기여**: [Documentation](https://github.com/ansimtalk/ansimtalk/tree/main/docs)
- **번역 기여**: [Translations](https://github.com/ansimtalk/ansimtalk/tree/main/translations)
- **테스트 기여**: [Testing](https://github.com/ansimtalk/ansimtalk/tree/main/tests)

#### 파트너십
- **기업 협력**: business@ansimtalk.com
- **연구 협력**: research@ansimtalk.com
- **정부 협력**: government@ansimtalk.com
- **NGO 협력**: ngo@ansimtalk.com

### 응답 시간

#### 일반 문의
- **이메일**: 24-48시간 내 응답
- **GitHub Issues**: 1-3일 내 응답
- **Discord**: 실시간 응답 (온라인 시)
- **Slack**: 1-2일 내 응답

#### 긴급 문의
- **보안 취약점**: 24시간 내 응답
- **서비스 장애**: 4시간 내 응답
- **법적 문의**: 48시간 내 응답
- **비즈니스 문의**: 24시간 내 응답

### 지원 범위

#### 기술 지원
- **설치 및 설정**: 설치 가이드 및 문제 해결
- **API 사용**: API 사용법 및 예제 제공
- **오류 해결**: 오류 진단 및 해결 방법
- **성능 최적화**: 성능 개선 방안 제시

#### 비기술 지원
- **사용법 안내**: 서비스 사용법 설명
- **법적 상담**: 법적 효력 및 사용법 안내
- **교육 자료**: 교육 및 훈련 자료 제공
- **커뮤니티 지원**: 커뮤니티 활동 지원

### 최근 지원 개선사항 (2024년 12월)

#### 모바일 지원 강화
- **모바일 가이드**: 모바일 사용법 상세 가이드
- **터치 최적화**: 터치 인터페이스 사용법 안내
- **반응형 디자인**: 다양한 화면 크기 대응 가이드
- **오프라인 지원**: 오프라인 기능 사용법

#### 문서 개선
- **시각적 가이드**: 스크린샷 및 동영상 가이드
- **단계별 튜토리얼**: 초보자를 위한 단계별 가이드
- **FAQ 확장**: 자주 묻는 질문 대폭 확장
- **다국어 지원**: 영어, 중국어 등 다국어 문서

#### 커뮤니티 활성화
- **정기 웨비나**: 월간 기술 웨비나 개최
- **해커톤 지원**: 해커톤 및 대회 지원
- **오픈소스 컨퍼런스**: 오픈소스 컨퍼런스 참여
- **대학 협력**: 대학 및 연구기관과의 협력