# 안심톡 - AI 기반 디지털 안전망

AI 기술을 활용하여 딥페이크와 사이버폭력을 분석하고 디지털 증거를 안전하게 증거화하는 웹 서비스입니다.

## 🚀 라이브 데모

**Railway 배포**: https://ansimtalk-production-xxxx.up.railway.app

> Railway에서 도메인을 생성하고 환경 변수를 설정하면 서비스가 활성화됩니다.

## 📋 주요 기능

### 딥페이크 분석
- 이미지 파일(PNG, JPG, JPEG) 분석
- Sightengine API 기반 딥페이크 탐지
- 상세한 분석 리포트 생성
- PDF 증거 자료 다운로드
- 파일 메타데이터 및 SHA-256 해시 추출

### 사이버폭력 분석
- 텍스트 파일(TXT) 및 이미지 파일 분석
- Google Gemini API 기반 사이버폭력 내용 탐지
- 위험도 평가 및 대응 방안 제시
- 법적 증거 자료 생성
- 이미지에서 텍스트 자동 추출 (Google Cloud Vision API)

## 🛠 기술 스택

### 백엔드
- **Python 3.12**
- **Flask** - 웹 프레임워크
- **Gunicorn** - WSGI 서버
- **Google Gemini API** - AI 텍스트 분석
- **Google Cloud Vision API** - 이미지 텍스트 추출
- **Sightengine API** - 딥페이크 탐지
- **FPDF** - PDF 생성
- **WeasyPrint** - HTML to PDF 변환

### 프론트엔드
- **HTML5/CSS3** - 반응형 웹 디자인
- **JavaScript** - 동적 인터페이스
- **NanumGothic 폰트** - 한글 최적화

### 배포
- **Railway** - 클라우드 플랫폼
- **Docker** - 컨테이너화
- **GitHub** - 버전 관리

## 📁 프로젝트 구조

```
ansimtalk/
├── app/
│   ├── __init__.py          # Flask 앱 팩토리
│   ├── routes.py            # 라우트 정의 (파일 업로드, 분석 처리)
│   ├── services.py          # 비즈니스 로직 (API 호출, PDF 생성)
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # 스타일시트
│   │   ├── fonts/           # NanumGothic 폰트 파일
│   │   └── uploads/         # 업로드된 파일 저장소
│   └── templates/           # HTML 템플릿
│       ├── index.html       # 메인 페이지
│       ├── results.html     # 분석 결과 페이지
│       ├── evidence.html    # 증거 자료 페이지
│       ├── deepfake_help.html    # 딥페이크 도움말
│       └── cyberbullying_help.html # 사이버폭력 도움말
├── config.py               # 환경 변수 설정
├── run.py                  # 애플리케이션 시작점
├── requirements.txt        # Python 의존성
├── Dockerfile             # Docker 설정
├── railway.toml           # Railway 설정
├── dazzling-howl-465316-m7-6605bfd84de1.json # Google Cloud 인증 파일
└── README.md              # 프로젝트 문서
```

## 🚀 로컬 개발 환경 설정

### 1. 저장소 클론
```bash
git clone https://github.com/pjmin19/ansimtalk-.git
cd ansimtalk-
```

### 2. 가상환경 생성 및 활성화
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. 의존성 설치
```bash
pip install -r requirements.txt
```

### 4. 환경 변수 설정
`.env` 파일 생성:
```env
SECRET_KEY=ansimtalk-secret-key-2024
SIGHTENGINE_API_USER=1052068557
SIGHTENGINE_API_SECRET=JbRcN79c6iunXBHG29WRzyQyFHRoYnQa
GOOGLE_GEMINI_API_KEY=AIzaSyAZ__v5f-3pYxDfMi--rdCyphpcqsxxrLo
GOOGLE_CLOUD_VISION_API_KEY=your-vision-api-key-here
```

### 5. 애플리케이션 실행
```bash
python run.py
```

브라우저에서 `http://localhost:5000` 접속

## 🌐 Railway 배포

### 1. Railway 계정 생성
[Railway](https://railway.app)에서 GitHub 계정으로 로그인

### 2. 프로젝트 연결
- GitHub 저장소 선택
- 자동 배포 활성화

### 3. 환경 변수 설정
Railway 대시보드 > Settings > Variables에서:
```
SECRET_KEY=ansimtalk-secret-key-2024
SIGHTENGINE_API_USER=1052068557
SIGHTENGINE_API_SECRET=JbRcN79c6iunXBHG29WRzyQyFHRoYnQa
GOOGLE_GEMINI_API_KEY=AIzaSyAZ__v5f-3pYxDfMi--rdCyphpcqsxxrLo
GOOGLE_CLOUD_VISION_API_KEY=your-vision-api-key-here
GOOGLE_SERVICE_ACCOUNT_JSON={"type":"service_account",...}
```

### 4. 도메인 설정
- Settings > Domains에서 "Generate Domain" 클릭
- 제공된 URL로 서비스 접근

## 🔧 API 키 설정

### Sightengine API (딥페이크 탐지)
1. [Sightengine](https://sightengine.com/) 계정 생성
2. API 키 발급
3. 환경 변수에 설정

### Google Gemini API (텍스트 분석)
1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. API 키 생성
3. 환경 변수에 설정

### Google Cloud Vision API (이미지 텍스트 추출)
1. [Google Cloud Console](https://console.cloud.google.com/) 접속
2. Vision API 활성화
3. 서비스 계정 키 생성
4. 환경 변수에 설정

## 📊 사용 방법

### 딥페이크 분석
1. 메인 페이지에서 "딥페이크 분석" 섹션 선택
2. 이미지 파일 업로드 (PNG, JPG, JPEG, 최대 5MB)
3. "분석 시작" 버튼 클릭
4. Sightengine API를 통한 딥페이크 탐지 결과 확인
5. 분석 결과 및 PDF 증거 자료 다운로드

### 사이버폭력 분석
1. "사이버폭력 분석" 섹션 선택
2. 텍스트 파일(TXT) 또는 이미지 파일 업로드
3. "분석 시작" 버튼 클릭
4. Google Gemini API를 통한 사이버폭력 분석
5. 위험도 평가 및 대응 방안 확인
6. PDF 증거 자료 생성

## 🔒 보안 및 개인정보

- 업로드된 파일은 임시 저장 후 자동 삭제
- 분석 결과는 세션 기반으로 관리
- 모든 통신은 HTTPS 암호화
- 개인정보 수집하지 않음
- 파일 SHA-256 해시값 생성으로 무결성 보장

## 📈 분석 기능 상세

### 딥페이크 분석
- **Sightengine API** 활용
- 딥페이크, 불쾌감, 노골성, 폭력성 탐지
- 신뢰도 점수 제공
- 상세한 분석 리포트 생성

### 사이버폭력 분석
- **Google Gemini API** 활용
- 텍스트 내용 분석 및 위험도 평가
- 사이버폭력 유형 분류
- 구체적인 대응 방안 제시
- 법적 증거 자료 자동 생성

## 🤝 기여하기

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 👥 개발팀

- **윤여준팀장** - 프로젝트 관리
- **김태양** - 백엔드 개발
- **김태영** - 프론트엔드 개발

## 📞 문의

프로젝트 관련 문의사항은 GitHub Issues를 통해 연락주세요.

---

**안심톡** - AI로 더 안전한 디지털 세상을 만들어갑니다.