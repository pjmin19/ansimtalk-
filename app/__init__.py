from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
app.config['UPLOAD_FOLDER'] = app.config.get('UPLOAD_FOLDER')

from app.routes import bp as main_bp
app.register_blueprint(main_bp)

# pipe_table_to_html 필터 등록
try:
    from app.services import pipe_table_to_html
    app.jinja_env.filters['pipe_table_to_html'] = pipe_table_to_html
    print("=== pipe_table_to_html 필터 등록 완료 ===")
except Exception as e:
    print(f"=== pipe_table_to_html 필터 등록 실패: {e} ===")

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    from . import routes
    app.register_blueprint(routes.bp)
    
    # pipe_table_to_html 필터 등록
    try:
        from .services import pipe_table_to_html
        app.jinja_env.filters['pipe_table_to_html'] = pipe_table_to_html
        print("=== pipe_table_to_html 필터 등록 완료 ===")
    except Exception as e:
        print(f"=== pipe_table_to_html 필터 등록 실패: {e} ===")
    
    return app