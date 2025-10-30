"""
Main Flask Application
"""

from flask import Flask, send_from_directory, redirect, url_for
from flask_cors import CORS
from config import Config
from modules import ModelLoader

# Initialize model loader globally
model_loader = ModelLoader()

def create_app():
    """Create and configure Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app, origins=Config.CORS_ORIGINS)
    
    # Initialize folders
    Config.init_app()
    
    # Load AI model on startup
    try:
        print("🚀 Initializing Qoffea Backend...")
        model_loader.load_model(Config.MODEL_PATH, Config.CONFIDENCE_THRESHOLD)
        print("✅ Model loaded successfully!")
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        raise
    
    # Register blueprints
    from routes import upload_bp, report_bp
    app.register_blueprint(upload_bp, url_prefix='/api')
    app.register_blueprint(report_bp, url_prefix='/api')
    
    # Serve uploaded files
    @app.route('/uploads/<filename>')
    def serve_upload(filename):
        """Serve uploaded images"""
        import os
        abs_upload_folder = os.path.abspath(Config.UPLOAD_FOLDER)
        return send_from_directory(abs_upload_folder, filename)
    
    # Serve report files
    @app.route('/reports/<filename>')
    def serve_report(filename):
        """Serve generated reports"""
        import os
        abs_report_folder = os.path.abspath(Config.REPORT_FOLDER)
        return send_from_directory(abs_report_folder, filename)
    
    # Serve frontend HTML pages
    @app.route('/index')
    @app.route('/index.html')
    def serve_index():
        """Serve index.html"""
        import os
        frontend_path = os.path.abspath(os.path.join(Config.BASE_DIR, '..', 'Frontend-Qoffea'))
        return send_from_directory(frontend_path, 'index.html')
    
    @app.route('/aksi')
    @app.route('/aksi.html')
    def serve_aksi():
        """Serve aksi.html"""
        import os
        frontend_path = os.path.abspath(os.path.join(Config.BASE_DIR, '..', 'Frontend-Qoffea'))
        return send_from_directory(frontend_path, 'aksi.html')
    
    @app.route('/panduan')
    @app.route('/panduan.html')
    def serve_panduan():
        """Serve panduan.html"""
        import os
        frontend_path = os.path.abspath(os.path.join(Config.BASE_DIR, '..', 'Frontend-Qoffea'))
        return send_from_directory(frontend_path, 'panduan.html')
    
    @app.route('/test-integration')
    @app.route('/test-integration.html')
    def serve_test():
        """Serve test-integration.html"""
        import os
        frontend_path = os.path.abspath(os.path.join(Config.BASE_DIR, '..', 'Frontend-Qoffea'))
        return send_from_directory(frontend_path, 'test-integration.html')
    
    @app.route('/assets/<path:filename>')
    @app.route('/Assets/<path:filename>')
    def serve_assets(filename):
        """Serve frontend assets (case-insensitive)"""
        import os
        assets_path = os.path.abspath(os.path.join(Config.BASE_DIR, '..', 'Frontend-Qoffea', 'Assets'))
        return send_from_directory(assets_path, filename)
    
    @app.route('/css/<path:filename>')
    def serve_css(filename):
        """Serve CSS files"""
        import os
        css_path = os.path.abspath(os.path.join(Config.BASE_DIR, '..', 'Frontend-Qoffea', 'css'))
        return send_from_directory(css_path, filename)
    
    @app.route('/js/<path:filename>')
    def serve_js(filename):
        """Serve JS files"""
        import os
        js_path = os.path.abspath(os.path.join(Config.BASE_DIR, '..', 'Frontend-Qoffea', 'js'))
        return send_from_directory(js_path, filename)
    
    @app.route('/style.css')
    def serve_main_css():
        """Serve main style.css"""
        import os
        frontend_path = os.path.abspath(os.path.join(Config.BASE_DIR, '..', 'Frontend-Qoffea'))
        return send_from_directory(frontend_path, 'style.css')
    
    # Health check endpoint
    @app.route('/api/health', methods=['GET'])
    def health_check():
        return {
            'status': 'healthy',
            'model_loaded': model_loader._model is not None,
            'classes': model_loader.get_class_names()
        }
    
    # Homepage - redirect to index
    @app.route('/')
    def homepage():
        """Redirect to index page"""
        return redirect(url_for('serve_index'))
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
