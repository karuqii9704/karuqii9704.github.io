import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    DEBUG = os.getenv('FLASK_DEBUG', '0') == '1'  # Default False untuk production
    HOST = os.getenv('HOST', '0.0.0.0')
    PORT = int(os.getenv('PORT', 5000))
    
    # Model
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    # Hugging Face Model Configuration
    HF_MODEL_REPO = os.getenv('HF_MODEL_REPO', 'rakaval/Qoffea_2')
    HF_MODEL_FILE = os.getenv('HF_MODEL_FILE', 'best_2.pt')  # nama file model di repo
    MODEL_CACHE_DIR = os.getenv('MODEL_CACHE_DIR', os.path.join(BASE_DIR, 'model_cache'))
    
    # Detection Parameters
    CONFIDENCE_THRESHOLD = float(os.getenv('CONFIDENCE_THRESHOLD', 0.52))  # Confidence threshold for predictions
    IOU_THRESHOLD = float(os.getenv('IOU_THRESHOLD', 0.40))  # Lower = more aggressive NMS, removes more overlaps
    MAX_DETECTIONS = int(os.getenv('MAX_DETECTIONS', 300))  # Maximum number of detections per image
    
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
        os.makedirs(Config.MODEL_CACHE_DIR, exist_ok=True)
