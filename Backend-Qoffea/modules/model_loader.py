"""
Model Loader Module
Handles loading and managing the YOLO AI model
"""

from ultralytics import YOLO
import torch
from pathlib import Path


class ModelLoader:
    _instance = None
    _model = None
    
    def __new__(cls):
        """Singleton pattern to ensure only one model instance"""
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize model loader"""
        if self._model is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
            print(f"🔧 Using device: {self.device}")
    
    def load_model(self, model_path: str, confidence: float = 0.5):
        """
        Load YOLO model from file
        
        Args:
            model_path: Path to the .pt model file
            confidence: Confidence threshold for predictions
            
        Returns:
            Loaded YOLO model
        """
        if self._model is None:
            model_file = Path(model_path)
            
            if not model_file.exists():
                raise FileNotFoundError(f"Model file not found: {model_path}")
            
            print(f"📦 Loading model from: {model_path}")
            self._model = YOLO(model_path)
            self._model.conf = confidence
            
            # Get model info
            if hasattr(self._model, 'names'):
                print(f"✅ Model loaded successfully!")
                print(f"📊 Classes detected: {self._model.names}")
            
        return self._model
    
    def get_model(self):
        """Get the loaded model instance"""
        if self._model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        return self._model
    
    def get_class_names(self):
        """Get class names from the model"""
        model = self.get_model()
        return model.names if hasattr(model, 'names') else {}
    
    def predict(self, image_path: str, conf: float = None):
        """
        Run prediction on an image
        
        Args:
            image_path: Path to image file
            conf: Optional confidence threshold override
            
        Returns:
            Prediction results
        """
        model = self.get_model()
        
        if conf is not None:
            original_conf = model.conf
            model.conf = conf
            results = model(image_path)
            model.conf = original_conf
        else:
            results = model(image_path)
        
        return results
