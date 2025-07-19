import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, current_app, session, flash, send_file
from werkzeug.utils import secure_filename
from .services import analyze_file, generate_pdf_report
import shutil
from PIL import Image, ExifTags
import hashlib

bp = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'txt', 'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024

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
        if 'file' not in request.files:
            flash('파일이 없습니다.')
            return redirect(url_for('main.index'))
        file = request.files['file']
        if file.filename == '':
            flash('파일을 선택해주세요.')
            return redirect(url_for('main.index'))
        if not allowed_file(file.filename):
            flash('허용되지 않는 파일 형식입니다.')
            return redirect(url_for('main.index'))
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        if file_size > MAX_FILE_SIZE:
            flash('파일 크기가 너무 큽니다.')
            return redirect(url_for('main.index'))

        original_filename = secure_filename(file.filename)
        file_extension = original_filename.rsplit('.', 1)[1].lower()
        unique_filename = f"{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
        upload_folder = os.path.join(current_app.root_path, '..', 'tmp')
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        file_path = os.path.join(upload_folder, unique_filename)
        file.save(file_path)

        # static/uploads로 복사
        static_uploads = os.path.join(current_app.root_path, 'static', 'uploads')
        if not os.path.exists(static_uploads):
            os.makedirs(static_uploads)
        static_file_path = os.path.join(static_uploads, unique_filename)
        shutil.copy(file_path, static_file_path)

        # 파일 정보 추출
        file_stat = os.stat(file_path)
        metadata = extract_metadata(file_path)
        sha256 = get_file_sha256(file_path)

        # 세션에 저장
        session['uploaded_file_path'] = file_path
        session['static_file_path'] = static_file_path
        session['original_filename'] = original_filename
        session['file_extension'] = file_extension
        session['file_stat'] = {'st_size': file_stat.st_size}
        session['metadata'] = metadata
        session['sha256'] = sha256
        session['static_image_url'] = f"uploads/{unique_filename}"
        session['original_image_path'] = static_file_path  # 원본 이미지 절대 경로 저장
        session['analysis_type'] = analysis_type # 분석 타입 세션에 저장

        # 분석 결과 생성(서비스 함수 활용)
        try:
            analysis_result = analyze_file(file_path, analysis_type, file_extension)
            
            # 업로더 정보 추가 - 더 확실한 증거로 채택될 수 있도록 개선
            upload_timestamp = datetime.now()
            analysis_result['uploader_id'] = f"ANSIMTALK_USER_{upload_timestamp.strftime('%Y%m%d')}_{uuid.uuid4().hex[:8].upper()}"
            analysis_result['uploader_ip'] = request.remote_addr
            analysis_result['upload_timestamp'] = upload_timestamp.isoformat()
            analysis_result['file_size_bytes'] = file_stat.st_size
            analysis_result['file_size_mb'] = round(file_stat.st_size / (1024 * 1024), 2)
            
            # 이미지 크기 정보 추가
            if file_extension in {'jpg', 'jpeg', 'png'}:
                try:
                    with Image.open(file_path) as img:
                        analysis_result['image_width'] = img.width
                        analysis_result['image_height'] = img.height
                        analysis_result['image_resolution'] = f"{img.width}x{img.height}"
                except Exception as e:
                    analysis_result['image_width'] = 'N/A'
                    analysis_result['image_height'] = 'N/A'
                    analysis_result['image_resolution'] = 'N/A'
            else:
                analysis_result['image_width'] = 'N/A'
                analysis_result['image_height'] = 'N/A'
                analysis_result['image_resolution'] = 'N/A'
            
            session['analysis_result'] = analysis_result
        except Exception as e:
            flash(f'{analysis_type} 분석 중 오류: {e}')
            if os.path.exists(file_path):
                os.remove(file_path)
            return redirect(url_for('main.index'))
        return redirect(url_for('main.results'))
    except Exception as e:
        flash(f'파일 처리 중 오류: {e}')
        return redirect(url_for('main.index'))

@bp.route('/')
def index():
    return render_template('index.html')

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
        
        # 원본 이미지 경로 추가
        analysis_result['original_image_path'] = session.get('original_image_path', '')
        
        # PDF 파일 경로 생성
        pdf_filename = f"evidence_{uuid.uuid4().hex}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
        pdf_path = os.path.join(current_app.root_path, '..', 'tmp', pdf_filename)
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
    static_file_path = session.get('static_file_path')
    if file_path and os.path.exists(file_path):
        os.remove(file_path)
    if static_file_path and os.path.exists(static_file_path):
        os.remove(static_file_path)
    session.clear()
    return redirect(url_for('main.index'))