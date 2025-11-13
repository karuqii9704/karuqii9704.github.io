"""
Model Loader Module
Handles loading and managing the YOLO AI model from Hugging Face
"""

from ultralytics import YOLO
import torch
from pathlib import Path
import os
from huggingface_hub import hf_hub_download

# Configure PyTorch to allow loading custom model architectures
# This is safe for trusted model files from Ultralytics
os.environ['PYTORCH_ENABLE_MPS_FALLBACK'] = '1'

# Add safe globals for PyTorch 2.6+ compatibility
try:
    # Register Ultralytics classes as safe globals for torch.load
    from ultralytics.nn.tasks import DetectionModel, SegmentationModel, ClassificationModel, PoseModel, OBBModel
    from ultralytics.nn import modules
    
    if hasattr(torch.serialization, 'add_safe_globals'):
        # Add all necessary Ultralytics classes
        safe_classes = [
            DetectionModel,
            SegmentationModel, 
            ClassificationModel,
            PoseModel,
            OBBModel,
        ]
        
        # Add common nn.modules classes
        for module_name in dir(modules):
            if not module_name.startswith('_'):
                module_obj = getattr(modules, module_name)
                if isinstance(module_obj, type):
                    safe_classes.append(module_obj)
        
        torch.serialization.add_safe_globals(safe_classes)
        print("✅ Registered Ultralytics safe globals for PyTorch")
except Exception as e:
    print(f"⚠️ Warning: Could not register all safe globals: {e}")
    # Fallback: set environment to allow all torch.load operations
    os.environ['TORCH_FORCE_WEIGHTS_ONLY_LOAD'] = '0'


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
    
    def load_model(self, model_repo: str = None, model_file: str = None, cache_dir: str = None, 
                   confidence: float = 0.6, iou: float = 0.45, max_det: int = 300):
        """
        Load YOLO model from Hugging Face repository
        
        Args:
            model_repo: Hugging Face repository ID (e.g., 'rakaval/Qoffea_2')
            model_file: Name of the model file in the repository (e.g., 'best.pt')
            cache_dir: Directory to cache the downloaded model
            confidence: Confidence threshold for predictions (default: 0.6)
            iou: IoU threshold for NMS to eliminate overlapping boxes (default: 0.45)
            max_det: Maximum number of detections per image (default: 300)
            
        Returns:
            Loaded YOLO model
        """
        if self._model is None:
            try:
                print(f"🔍 Downloading model from Hugging Face...")
                print(f"   Repository: {model_repo}")
                print(f"   File: {model_file}")
                
                # Try to download as a Space first, then as a Model repo if that fails
                model_path = None
                
                # Common paths in Spaces where model files might be located
                possible_paths = [
                    model_file,  # Root directory (e.g., 'best.pt')
                    f"models/{model_file}",  # Common models subfolder
                    f"model/{model_file}",  # Singular models folder
                    f"weights/{model_file}",  # Weights folder
                ]
                
                # Try downloading from Space with different paths
                for file_path in possible_paths:
                    try:
                        print(f"   Attempting to download from Space: {file_path}...")
                        model_path = hf_hub_download(
                            repo_id=model_repo,
                            filename=file_path,
                            cache_dir=cache_dir,
                            repo_type="space"
                        )
                        print(f"   ✓ Found at: {file_path}")
                        break
                    except Exception as space_error:
                        print(f"   ✗ Not found at: {file_path}")
                        continue
                
                # If Space download failed, try Model repository
                if not model_path:
                    print(f"   Attempting to download from Model repository...")
                    try:
                        model_path = hf_hub_download(
                            repo_id=model_repo,
                            filename=model_file,
                            cache_dir=cache_dir,
                            repo_type="model"
                        )
                    except Exception as model_error:
                        print(f"   Model repo download failed: {model_error}")
                        print(f"   Attempting default download (no repo_type)...")
                        # Last resort: try without specifying repo_type
                        model_path = hf_hub_download(
                            repo_id=model_repo,
                            filename=model_file,
                            cache_dir=cache_dir
                        )
                
                if not model_path:
                    raise RuntimeError("Failed to download model from all attempted methods")
                
                print(f"✅ Model downloaded to: {model_path}")
                print(f"📦 Loading model...")
                
                self._model = YOLO(model_path)
                # Set detection parameters
                self._model.conf = confidence  # Confidence threshold
                self._model.iou = iou  # IoU threshold for NMS
                self._model.max_det = max_det  # Maximum detections per image
                
                # Get model info
                if hasattr(self._model, 'names'):
                    print(f"✅ Model loaded successfully!")
                    print(f"📊 Classes detected: {self._model.names}")
                    print(f"⚙️  Detection settings:")
                    print(f"   - Confidence threshold: {confidence}")
                    print(f"   - IoU threshold (NMS): {iou}")
                    print(f"   - Max detections: {max_det}")
                
            except Exception as e:
                print(f"❌ Error loading model from Hugging Face: {e}")
                print(f"   Make sure:")
                print(f"   1. Repository exists: {model_repo}")
                print(f"   2. File exists in repo: {model_file}")
                print(f"   3. You have internet connection")
                raise RuntimeError(f"Failed to load model from Hugging Face: {e}")
            
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
    
    def predict(self, image_path: str, conf: float = None, iou: float = None, max_det: int = None):
        """
        Run prediction on an image
        
        Args:
            image_path: Path to image file
            conf: Optional confidence threshold override
            iou: Optional IoU threshold override for NMS
            max_det: Optional max detections override
            
        Returns:
            Prediction results
        """
        model = self.get_model()
        
        # Store original settings
        original_conf = model.conf
        original_iou = model.iou
        original_max_det = model.max_det
        
        # Apply overrides if provided
        if conf is not None:
            model.conf = conf
        if iou is not None:
            model.iou = iou
        if max_det is not None:
            model.max_det = max_det
        
        # Run prediction
        results = model(image_path)
        
        # Restore original settings
        model.conf = original_conf
        model.iou = original_iou
        model.max_det = original_max_det
        
        return results
