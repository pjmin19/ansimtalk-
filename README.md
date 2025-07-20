# 안심톡 - AI 기반 디지털 안전망

AI 기술을 활용하여 딥페이크와 사이버폭력을 분석하고 디지털 증거를 안전하게 증거화하는 웹 서비스입니다.

## 📋 목차

1. [프로젝트 소개](#프로젝트-소개)
2. [주요 기능](#주요-기능)
3. [기술 스택](#기술-스택)
4. [프로젝트 구조](#프로젝트-구조)
5. [설치 및 실행](#설치-및-실행)
6. [배포 가이드](#배포-가이드)
7. [API 설정](#api-설정)
8. [사용 방법](#사용-방법)
9. [보안 및 개인정보](#보안-및-개인정보)
10. [분석 기능 상세](#분석-기능-상세)
11. [개발 가이드](#개발-가이드)
12. [테스트](#테스트)
13. [기여하기](#기여하기)
14. [라이선스](#라이선스)
15. [개발팀](#개발팀)
16. [문의 및 지원](#문의-및-지원)

## 🚀 라이브 데모

**Railway 배포**: https://ansimtalk-production.up.railway.app

> Railway에서 도메인을 생성하고 환경 변수를 설정하면 서비스가 활성화됩니다.

## 🎯 프로젝트 소개

### 안심톡이란?
안심톡은 AI 기술을 활용하여 디지털 범죄 피해자에게 실질적인 도움을 제공하는 혁신적인 플랫폼입니다. 딥페이크와 사이버폭력을 자동으로 분석하고, 법적 효력을 갖춘 증거보고서를 생성하여 피해자의 권리 보호를 돕습니다.

### 핵심 가치
- **신뢰성**: 정확하고 신뢰할 수 있는 AI 분석 결과
- **접근성**: 기술적 지식 없이도 누구나 쉽게 사용 가능
- **보안성**: 개인정보 보호 및 파일 보안 강화
- **효율성**: 빠르고 정확한 분석 및 결과 제공

### 사회적 기여
- 디지털 범죄 피해자 보호 및 예방
- AI 기술의 사회적 활용 확대
- 디지털 증거의 신뢰성 및 법적 효력 향상
- 사이버 안전 문화 조성

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

### 증거보고서 생성
- 법적 효력을 갖춘 PDF 보고서
- SHA-256 해시값으로 파일 무결성 보장
- 상세한 분석 결과 및 위험도 평가
- 상담/신고 기관 정보 포함

### 사용자 인터페이스
- 직관적이고 사용하기 쉬운 웹 인터페이스
- 반응형 디자인으로 모바일/데스크톱 호환
- 실시간 분석 진행 상황 표시
- 한글 최적화 (NanumGothic 폰트)

## 🛠 기술 스택

### 백엔드
- **Python 3.12** - 메인 프로그래밍 언어
- **Flask 3.1.1** - 웹 프레임워크
- **Gunicorn 23.0.0** - WSGI 서버
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

### 개발 도구
- **Git** - 버전 관리
- **VS Code** - 코드 에디터
- **Postman** - API 테스트
- **Chrome DevTools** - 프론트엔드 디버깅

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

### 핵심 파일 설명

#### `app/__init__.py`
Flask 애플리케이션 팩토리 패턴을 구현하여 확장 가능한 구조로 설계되었습니다.

#### `app/routes.py`
웹 라우팅 및 요청 처리를 담당하며, 파일 업로드와 분석 처리를 관리합니다.

#### `app/services.py`
AI 분석 및 PDF 생성 서비스를 담당하며, 외부 API 호출과 PDF 생성을 처리합니다.

#### `config.py`
환경 변수 및 설정을 관리하며, API 키와 서비스 설정을 중앙화합니다.

## 🚀 설치 및 실행

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

### 6. 개발 모드 실행
```bash
export FLASK_ENV=development
export FLASK_DEBUG=1
python run.py
```

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

### 5. 배포 모니터링
- Railway 대시보드에서 배포 상태 확인
- 로그를 통한 오류 추적
- 성능 메트릭 모니터링

## 🔑 API 설정

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

### API 키 보안
- 환경 변수를 통한 API 키 관리
- 서버 내부에서만 API 호출
- 정기적인 API 키 순환
- 사용량 모니터링 및 제한

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

### 결과 해석
- **위험도 등급**: 심각/있음/약간/의심/없음
- **신뢰도 점수**: 0-100점 척도
- **상세 분석**: 구체적인 분석 결과 및 근거
- **대응 방안**: 상황별 권장 조치사항

### 상담 및 신고
- **딥페이크 피해**: 경찰청 사이버수사과 (182)
- **사이버폭력 피해**: 청소년사이버상담센터 (1388)
- **긴급 신고**: 경찰청 사이버수사과 (182)
- **상담 지원**: 디지털성범죄피해자지원센터 (1366)

## 🔒 보안 및 개인정보

### 파일 보안
- 업로드된 파일은 임시 저장 후 자동 삭제
- 파일 형식 및 크기 엄격 검증
- SHA-256 해시값으로 무결성 보장
- 악성 파일 차단 및 보안 검증

### 개인정보 보호
- 분석에 필요한 최소한의 정보만 수집
- 개인정보 수집하지 않음
- 세션 기반 임시 데이터 관리
- 모든 통신 HTTPS 암호화

### API 보안
- 환경 변수를 통한 API 키 관리
- 서버 내부에서만 API 호출
- 요청 제한 및 모니터링
- 정기적인 보안 업데이트

### 데이터 처리
- 분석 완료 후 즉시 데이터 삭제
- 사용자별 독립적인 세션 관리
- 접근 로그 및 감사 추적
- 백업 데이터 보안 관리

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

### 이미지 텍스트 추출
- **Google Cloud Vision API** 활용
- OCR 기술로 이미지에서 텍스트 추출
- 다국어 지원 (한국어, 영어 등)
- 높은 정확도의 텍스트 인식

### PDF 증거보고서
- **FPDF + WeasyPrint** 조합
- 법적 효력을 위한 표준 형식
- 한글 폰트 지원
- 상세한 분석 결과 포함

## 🔧 개발 가이드

### 개발 환경 설정
```bash
# 개발 의존성 설치
pip install -r requirements-dev.txt

# 코드 포맷팅
black app/
flake8 app/

# 타입 체크
mypy app/
```

### 코드 구조
- **MVC 패턴**: Model-View-Controller 구조
- **모듈화**: 기능별 독립적인 모듈 설계
- **의존성 주입**: 환경 변수를 통한 설정 관리
- **에러 핸들링**: 체계적인 오류 처리

### API 개발
```python
# 새로운 분석 유형 추가
def add_analysis_type(analysis_type, handler):
    analysis_handlers[analysis_type] = handler

# API 응답 표준화
def create_response(success, data=None, error=None):
    return {
        'success': success,
        'data': data,
        'error': error,
        'timestamp': datetime.now().isoformat()
    }
```

### 데이터베이스 연동
- **SQLAlchemy**: ORM을 통한 데이터베이스 관리
- **마이그레이션**: Alembic을 통한 스키마 관리
- **백업**: 정기적인 데이터베이스 백업
- **모니터링**: 데이터베이스 성능 모니터링

## 🧪 테스트

### 단위 테스트
```python
import unittest
from app.services import analyze_file

class TestAnalysis(unittest.TestCase):
    def test_deepfake_analysis(self):
        result = analyze_file('test_image.jpg', 'deepfake', 'jpg')
        self.assertIn('deepfake_analysis', result)
        self.assertIsInstance(result['deepfake_analysis'], dict)
```

### 통합 테스트
- **API 테스트**: Postman을 통한 엔드포인트 테스트
- **브라우저 테스트**: Selenium을 통한 웹 인터페이스 테스트
- **성능 테스트**: Locust를 통한 부하 테스트
- **보안 테스트**: OWASP ZAP을 통한 보안 취약점 테스트

### 테스트 자동화
- **GitHub Actions**: 자동 테스트 및 배포
- **코드 커버리지**: pytest-cov를 통한 커버리지 측정
- **품질 게이트**: 코드 품질 기준 설정
- **지속적 통합**: CI/CD 파이프라인 구축

## 🤝 기여하기

### 기여 방법
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### 개발 가이드라인
- **코드 스타일**: PEP 8 준수
- **문서화**: 모든 함수에 docstring 작성
- **테스트**: 새로운 기능에 대한 테스트 작성
- **리뷰**: 모든 변경사항에 대한 코드 리뷰

### 이슈 리포트
- **버그 리포트**: 상세한 재현 단계 포함
- **기능 제안**: 구체적인 사용 사례 설명
- **문서 개선**: 더 나은 문서화 제안
- **성능 개선**: 성능 최적화 아이디어

### 커뮤니티
- **GitHub Discussions**: 프로젝트 토론
- **이슈 트래커**: 버그 리포트 및 기능 제안
- **위키**: 상세한 개발 가이드
- **블로그**: 프로젝트 업데이트 및 기술 블로그

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

### 라이선스 조건
- **자유로운 사용**: 개인 및 상업적 사용 가능
- **수정 및 배포**: 코드 수정 및 재배포 가능
- **저작권 표시**: 원본 저작권 표시 필요
- **책임 면제**: 사용에 따른 책임 면제

### 오픈소스 기여
- **오픈소스 정신**: 지식 공유 및 협력
- **커뮤니티 기반**: 개발자 커뮤니티 참여
- **지속적 개선**: 지속적인 기능 개선
- **투명성**: 모든 코드 공개 및 검토 가능

## 👥 개발팀

### 팀 구성
- **윤여준팀장** - 프로젝트 관리 및 기획
- **김태양** - 백엔드 개발 및 AI 연동
- **김태영** - 프론트엔드 개발 및 UI/UX

### 역할 분담
- **프로젝트 관리**: 전체 프로젝트 기획 및 관리
- **백엔드 개발**: 서버 로직 및 AI API 연동
- **프론트엔드 개발**: 사용자 인터페이스 및 UX 설계
- **AI/ML**: 머신러닝 모델 및 알고리즘 개발

### 협업 방식
- **애자일 개발**: 스프린트 기반 개발
- **코드 리뷰**: 팀원 간 코드 검토
- **정기 회의**: 주간 진행 상황 공유
- **문서화**: 상세한 기술 문서 작성

## 📞 문의 및 지원

### 기술 지원
- **GitHub Issues**: 버그 리포트 및 기능 제안
- **이메일**: ansimtalk@example.com
- **문서**: 상세한 사용 가이드 제공
- **FAQ**: 자주 묻는 질문 및 답변

### 커뮤니티
- **GitHub Discussions**: 프로젝트 토론
- **Discord 서버**: 실시간 개발자 소통
- **블로그**: 프로젝트 업데이트 및 기술 블로그
- **뉴스레터**: 정기적인 프로젝트 소식

### 기여 방법
- **코드 기여**: Pull Request를 통한 코드 기여
- **문서 기여**: 문서 개선 및 번역
- **테스트 기여**: 테스트 케이스 작성
- **홍보 기여**: 프로젝트 홍보 및 커뮤니티 확산

### 파트너십
- **기업 협력**: 기업 솔루션 및 파트너십
- **연구 협력**: 학술 연구 및 논문 협력
- **정부 협력**: 공공 서비스 및 정책 지원
- **NGO 협력**: 비영리 기관과의 협력

---

**안심톡** - AI로 더 안전한 디지털 세상을 만들어갑니다.