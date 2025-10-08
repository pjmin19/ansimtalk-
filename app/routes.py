import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, current_app, session, flash, send_file
from werkzeug.utils import secure_filename
from .services import analyze_file, generate_pdf_report
import shutil
from PIL import Image, ExifTags
import hashlib
import re
import unicodedata

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024

# 한글 파일명을 안전하게 처리하는 함수
def secure_korean_filename(filename):
    """
    한글 파일명을 안전하게 처리하는 함수
    - 한글 문자는 유니코드 정규화 후 유지
    - 특수문자는 제거하거나 안전한 문자로 변환
    - 파일 시스템에서 안전한 파일명 생성
    """
    if not filename:
        return ""
    
    # 파일명과 확장자 분리
    name, ext = os.path.splitext(filename)
    
    # 유니코드 정규화 (NFC)
    name = unicodedata.normalize('NFC', name)
    
    # 한글, 영문, 숫자, 일부 특수문자만 허용
    # 허용할 문자: 한글, 영문, 숫자, 공백, 하이픈, 언더스코어, 점
    safe_chars = re.sub(r'[^\w\s\-\.가-힣]', '', name)
    
    # 연속된 공백을 하나로 변환
    safe_chars = re.sub(r'\s+', ' ', safe_chars)
    
    # 앞뒤 공백 제거
    safe_chars = safe_chars.strip()
    
    # 빈 문자열이면 기본값 사용
    if not safe_chars:
        safe_chars = "uploaded_file"
    
    # 확장자는 소문자로 변환하고 안전한 문자만 허용
    safe_ext = re.sub(r'[^a-zA-Z0-9\.]', '', ext.lower())
    
    return safe_chars + safe_ext

# 파일 확장자 체크
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 파일 메타데이터 추출
def extract_metadata(image_path):
    try:
        img = Image.open(image_path)
        exif = img._getexif()
        meta = {}
        if exif:
            for tag, value in exif.items():
                decoded = ExifTags.TAGS.get(tag, tag)
                meta[decoded] = value
        meta['해상도'] = f"{img.width}x{img.height}"
        return meta
    except Exception:
        return {"해상도": "알수없음"}

# SHA-256 해시값 생성
def get_file_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(8192)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def _handle_file_upload_and_analysis(analysis_type):
    try:
        current_app.logger.info(f"=== {analysis_type} 분석 시작 ===")
        print(f"=== {analysis_type} 분석 시작 ===")
        
        if 'file' not in request.files:
            current_app.logger.error("오류: 파일이 요청에 없습니다.")
            print("오류: 파일이 요청에 없습니다.")
            flash('파일이 없습니다.')
            return redirect(url_for('main.index'))
        
        file = request.files['file']
        # 한글 파일명 로깅 개선
        try:
            current_app.logger.info(f"업로드된 파일명: {file.filename}")
            print(f"업로드된 파일명: {file.filename}")
        except UnicodeEncodeError:
            # 한글 파일명 로깅 오류 시 대체 방법
            safe_filename = file.filename.encode('utf-8', errors='replace').decode('utf-8')
            current_app.logger.info(f"업로드된 파일명 (안전): {safe_filename}")
            print(f"업로드된 파일명 (안전): {safe_filename}")
        
        if file.filename == '':
            current_app.logger.error("오류: 파일명이 비어있습니다.")
            print("오류: 파일명이 비어있습니다.")
            flash('파일을 선택해주세요.')
            return redirect(url_for('main.index'))
        
        if not allowed_file(file.filename):
            current_app.logger.error(f"오류: 허용되지 않는 파일 형식: {file.filename}")
            print(f"오류: 허용되지 않는 파일 형식: {file.filename}")
            flash('허용되지 않는 파일 형식입니다.')
            return redirect(url_for('main.index'))
        
        # 파일 크기 확인
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        current_app.logger.info(f"파일 크기: {file_size} bytes")
        print(f"파일 크기: {file_size} bytes")
        
        if file_size > MAX_FILE_SIZE:
            current_app.logger.error(f"오류: 파일 크기가 너무 큼: {file_size} bytes")
            print(f"오류: 파일 크기가 너무 큼: {file_size} bytes")
            flash('파일 크기가 너무 큽니다.')
            return redirect(url_for('main.index'))

        original_filename = secure_korean_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
        
        # 파일명 정보 로깅 (한글 지원)
        try:
            current_app.logger.info(f"원본 파일명: {original_filename}")
            current_app.logger.info(f"고유 파일명: {unique_filename}")
            current_app.logger.info(f"파일 확장자: {file_extension}")
            print(f"원본 파일명: {original_filename}")
            print(f"고유 파일명: {unique_filename}")
            print(f"파일 확장자: {file_extension}")
        except UnicodeEncodeError:
            # 한글 파일명 로깅 오류 시 대체 방법
            safe_original = original_filename.encode('utf-8', errors='replace').decode('utf-8')
            current_app.logger.info(f"원본 파일명 (안전): {safe_original}")
            current_app.logger.info(f"고유 파일명: {unique_filename}")
            current_app.logger.info(f"파일 확장자: {file_extension}")
            print(f"원본 파일명 (안전): {safe_original}")
            print(f"고유 파일명: {unique_filename}")
            print(f"파일 확장자: {file_extension}")
        
        # 현재 작업 디렉토리 확인
        current_dir = os.getcwd()
        current_app.logger.info(f"현재 작업 디렉토리: {current_dir}")
        print(f"현재 작업 디렉토리: {current_dir}")
        
        # 업로드 폴더를 현재 디렉토리 내에 생성
        upload_folder = os.path.join(current_dir, 'tmp')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
            current_app.logger.info(f"업로드 폴더 생성: {upload_folder}")
            print(f"업로드 폴더 생성: {upload_folder}")
        
        file_path = os.path.join(upload_folder, unique_filename)
        current_app.logger.info(f"파일 저장 경로: {file_path}")
        print(f"파일 저장 경로: {file_path}")
        
        # 파일 저장 (한글 파일명 지원)
        try:
            file.save(file_path)
            current_app.logger.info(f"파일 저장 완료: {file_path}")
            print(f"파일 저장 완료: {file_path}")
        except Exception as save_error:
            current_app.logger.error(f"파일 저장 오류: {save_error}")
            print(f"파일 저장 오류: {save_error}")
            # 한글 파일명으로 인한 오류 시 대체 방법 시도
            try:
                # 임시 파일명으로 저장 후 이름 변경
                temp_filename = f"temp_{uuid.uuid4().hex}.{file_extension}"
                temp_file_path = os.path.join(upload_folder, temp_filename)
                file.save(temp_file_path)
                os.rename(temp_file_path, file_path)
                current_app.logger.info(f"대체 방법으로 파일 저장 완료: {file_path}")
                print(f"대체 방법으로 파일 저장 완료: {file_path}")
            except Exception as rename_error:
                current_app.logger.error(f"대체 저장 방법도 실패: {rename_error}")
                print(f"대체 저장 방법도 실패: {rename_error}")
                flash('파일 저장에 실패했습니다.')
                return redirect(url_for('main.index'))
        
        # 파일 존재 확인
        if not os.path.exists(file_path):
            current_app.logger.error(f"오류: 파일 저장 후에도 존재하지 않음: {file_path}")
            print(f"오류: 파일 저장 후에도 존재하지 않음: {file_path}")
            flash('파일 저장에 실패했습니다.')
            return redirect(url_for('main.index'))
        
        # 파일 크기 재확인
        saved_file_size = os.path.getsize(file_path)
        current_app.logger.info(f"저장된 파일 크기: {saved_file_size} bytes")
        print(f"저장된 파일 크기: {saved_file_size} bytes")

        # static/uploads로 복사
        static_uploads = os.path.join(current_app.root_path, 'static', 'uploads')
        if not os.path.exists(static_uploads):
            os.makedirs(static_uploads)
            current_app.logger.info(f"static 업로드 폴더 생성: {static_uploads}")
            print(f"static 업로드 폴더 생성: {static_uploads}")
        
        static_file_path = os.path.join(static_uploads, unique_filename)
        try:
            shutil.copy(file_path, static_file_path)
            current_app.logger.info(f"static 폴더로 복사 완료: {static_file_path}")
            print(f"static 폴더로 복사 완료: {static_file_path}")
        except Exception as copy_error:
            current_app.logger.error(f"static 폴더 복사 오류: {copy_error}")
            print(f"static 폴더 복사 오류: {copy_error}")
            # 복사 실패 시에도 계속 진행 (분석은 가능)
            static_file_path = file_path

        # 파일 정보 추출
        file_stat = os.stat(file_path)
        metadata = extract_metadata(file_path)
        sha256 = get_file_sha256(file_path)
        
        current_app.logger.info(f"파일 메타데이터: {metadata}")
        current_app.logger.info(f"SHA-256: {sha256}")
        print(f"파일 메타데이터: {metadata}")
        print(f"SHA-256: {sha256}")

        # 세션에 저장 (한글 파일명 정보 포함)
        session['uploaded_file_path'] = file_path
        session['static_file_path'] = static_file_path
        session['original_filename'] = original_filename
        session['original_uploaded_filename'] = file.filename  # 원본 업로드 파일명 보존
        session['file_extension'] = file_extension
        session['file_stat'] = {'st_size': file_stat.st_size}
        session['metadata'] = metadata
        session['sha256'] = sha256
        session['static_image_url'] = f"uploads/{unique_filename}"
        session['original_image_path'] = static_file_path
        session['analysis_type'] = analysis_type
        
        current_app.logger.info("세션 정보 저장 완료")
        print("세션 정보 저장 완료")

        # 분석 결과 생성
        try:
            current_app.logger.info(f"분석 시작: {analysis_type}")
            current_app.logger.info(f"분석할 파일 경로: {file_path}")
            print(f"분석 시작: {analysis_type}")
            print(f"분석할 파일 경로: {file_path}")
            
            # 파일이 실제로 존재하는지 다시 한번 확인
            if not os.path.exists(file_path):
                current_app.logger.error(f"분석 전 파일 존재 확인 실패: {file_path}")
                print(f"분석 전 파일 존재 확인 실패: {file_path}")
                flash('분석할 파일을 찾을 수 없습니다.')
                return redirect(url_for('main.index'))
            
            analysis_result = analyze_file(file_path, analysis_type, file_extension)
            current_app.logger.info(f"분석 완료: {analysis_result}")
            print(f"분석 완료: {analysis_result}")
            
            # 업로더 정보 추가
            upload_timestamp = datetime.now()
            analysis_result['uploader_id'] = f"ANSIMTALK_USER_{upload_timestamp.strftime('%Y%m%d')}_{uuid.uuid4().hex[:8].upper()}"
            analysis_result['uploader_ip'] = request.remote_addr
            analysis_result['upload_timestamp'] = upload_timestamp.isoformat()
            analysis_result['file_size_bytes'] = file_stat.st_size
            analysis_result['file_size_mb'] = round(file_stat.st_size / (1024 * 1024), 2)
            
            # 파일 경로 정보 추가 (PDF 생성용)
            analysis_result['file_path'] = file_path
            analysis_result['upload_path'] = static_file_path
            analysis_result['original_image_path'] = static_file_path
            
            # 이미지 크기 정보 추가 및 Base64 인코딩 저장
            if file_extension in {'jpg', 'jpeg', 'png'}:
                try:
                    with Image.open(file_path) as img:
                        analysis_result['image_width'] = img.width
                        analysis_result['image_height'] = img.height
                        analysis_result['image_resolution'] = f"{img.width}x{img.height}"
                        current_app.logger.info(f"이미지 크기: {img.width}x{img.height}")
                        print(f"이미지 크기: {img.width}x{img.height}")
                    
                    # PDF 생성을 위해 이미지를 Base64로 인코딩하여 세션에 저장
                    import base64
                    with open(file_path, 'rb') as img_file:
                        img_data = img_file.read()
                        base64_img = base64.b64encode(img_data).decode('utf-8')
                        analysis_result['image_base64'] = base64_img
                        analysis_result['image_mime_type'] = f"image/{file_extension if file_extension != 'jpg' else 'jpeg'}"
                        print(f"✅ 이미지 Base64 인코딩 완료: {len(base64_img)} bytes")
                        
                except Exception as e:
                    current_app.logger.error(f"이미지 처리 오류: {e}")
                    print(f"이미지 처리 오류: {e}")
                    analysis_result['image_width'] = 'N/A'
                    analysis_result['image_height'] = 'N/A'
                    analysis_result['image_resolution'] = 'N/A'
            else:
                analysis_result['image_width'] = 'N/A'
                analysis_result['image_height'] = 'N/A'
                analysis_result['image_resolution'] = 'N/A'
            
            session['analysis_result'] = analysis_result
            current_app.logger.info("분석 결과 세션 저장 완료")
            print("분석 결과 세션 저장 완료")
            
        except Exception as e:
            current_app.logger.error(f"분석 중 오류 발생: {e}")
            print(f"분석 중 오류 발생: {e}")
            import traceback
            current_app.logger.error(f"상세 오류 정보: {traceback.format_exc()}")
            print(f"상세 오류 정보: {traceback.format_exc()}")
            flash(f'{analysis_type} 분석 중 오류: {e}')
            if os.path.exists(file_path):
                os.remove(file_path)
                current_app.logger.info(f"임시 파일 삭제: {file_path}")
                print(f"임시 파일 삭제: {file_path}")
            return redirect(url_for('main.index'))
        
        current_app.logger.info(f"=== {analysis_type} 분석 완료 ===")
        print(f"=== {analysis_type} 분석 완료 ===")
        return redirect(url_for('main.results'))
        
    except Exception as e:
        current_app.logger.error(f"파일 처리 중 예상치 못한 오류: {e}")
        print(f"파일 처리 중 예상치 못한 오류: {e}")
        import traceback
        current_app.logger.error(f"상세 오류 정보: {traceback.format_exc()}")
        print(f"상세 오류 정보: {traceback.format_exc()}")
        flash(f'파일 처리 중 오류: {e}')
        return redirect(url_for('main.index'))

@bp.route('/health')
def health():
    try:
        # 기본 상태 확인
        status = {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "service": "AnsimTalk AI Forensic Analysis",
            "version": "1.0.0",
            "environment": "production"
        }
        return status, 200
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 500

@bp.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"AnsimTalk is running! Error: {str(e)}", 200

@bp.route('/analyze_deepfake', methods=['POST'])
def analyze_deepfake():
    return _handle_file_upload_and_analysis('deepfake')

@bp.route('/analyze_cyberbullying', methods=['POST'])
def analyze_cyberbullying():
    return _handle_file_upload_and_analysis('cyberbullying')

@bp.route('/results')
def results():
    analysis_result = session.get('analysis_result')
    analysis_type = session.get('analysis_type') # 분석 타입 가져오기
    if not analysis_result:
        flash('분석 결과가 없습니다.')
        return redirect(url_for('main.index'))
    return render_template('results.html', result=analysis_result, analysis_type=analysis_type)

@bp.route('/evidence')
def evidence():
    return render_template('evidence.html')

@bp.route('/deepfake_help')
def deepfake_help():
    return render_template('deepfake_help.html')

@bp.route('/cyberbullying_help')
def cyberbullying_help():
    return render_template('cyberbullying_help.html')

@bp.route('/download_pdf')
def download_pdf():
    try:
        analysis_result = session.get('analysis_result')
        analysis_type = session.get('analysis_type') # 분석 타입 가져오기
        if not analysis_result:
            flash('분석 결과가 없습니다.')
            return redirect(url_for('main.index'))
        
        # 원본 이미지 경로 추가 - 모든 가능한 경로 정보 전달
        analysis_result['original_image_path'] = session.get('original_image_path', '')
        analysis_result['uploaded_file_path'] = session.get('uploaded_file_path', '')
        analysis_result['static_file_path'] = session.get('static_file_path', '')
        
        # tmp 디렉토리 생성
        tmp_dir = os.path.join(current_app.root_path, '..', 'tmp')
        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)
        
        # PDF 파일 경로 생성
        pdf_filename = f"evidence_{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = os.path.join(tmp_dir, pdf_filename)
        # PDF 생성
        generate_pdf_report(analysis_result, pdf_path, analysis_type) # analysis_type 전달
        print(f"Attempting to send file from: {pdf_path}")
        if not os.path.exists(pdf_path):
            print(f"Error: PDF file does not exist at {pdf_path} right before sending.")
            flash('PDF 파일 생성에 실패했습니다.')
            return redirect(url_for('main.index'))
        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename)
    except Exception as e:
        flash(f'PDF 생성/다운로드 중 오류: {e}')
        return redirect(url_for('main.index'))

@bp.route('/reset')
def reset():
    # 임시파일 삭제
    file_path = session.get('uploaded_file_path')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
    static_file_path = session.get('static_file_path')
    if static_file_path and os.path.exists(static_file_path):
        os.remove(static_file_path)
    
    # 세션 클리어
    session.clear()
    return redirect(url_for('main.index'))