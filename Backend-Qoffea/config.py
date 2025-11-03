import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', '1') == '1'
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Model
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MODEL_PATH = os.getenv('MODEL_PATH', os.path.join(BASE_DIR, 'models', 'best.pt'))
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.5))
    
    # Upload
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(BASE_DIR, 'uploads'))
    REPORT_FOLDER = os.getenv('REPORT_FOLDER', os.path.join(BASE_DIR, 'reports'))
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10485760))  # 10MB
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    
    # CORS
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')
    
    @staticmethod
    def init_app():
        """Initialize application folders"""
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.REPORT_FOLDER, exist_ok=True)
