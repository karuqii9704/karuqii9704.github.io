"""
Image Processor Module
Handles image preprocessing and validation
"""

import cv2
import numpy as np
from PIL import Image
from pathlib import Path


class ImageProcessor:
    
    @staticmethod
    def validate_image(file_path: str) -> bool:
        """
        Validate if file is a valid image
        
        Args:
            file_path: Path to image file
            
        Returns:
            True if valid image, False otherwise
        """
        try:
            img = Image.open(file_path)
            img.verify()
            return True
        except Exception as e:
            print(f"❌ Invalid image: {e}")
            return False
    
    @staticmethod
    def get_image_info(file_path: str) -> dict:
        """
        Get image information
        
        Args:
            file_path: Path to image file
            
        Returns:
            Dictionary with image info
        """
        try:
            img = Image.open(file_path)
            return {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'size_kb': Path(file_path).stat().st_size / 1024
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def preprocess_image(file_path: str, target_size: tuple = None) -> np.ndarray:
        """
        Preprocess image for model input
        
        Args:
            file_path: Path to image file
            target_size: Optional target size (width, height)
            
        Returns:
            Preprocessed image as numpy array
        """
        img = cv2.imread(file_path)
        
        if img is None:
            raise ValueError(f"Failed to load image: {file_path}")
        
        # Convert BGR to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize if target size specified
        if target_size:
            img = cv2.resize(img, target_size)
        
        return img
    
    @staticmethod
    def draw_detections(image_path: str, results, output_path: str) -> str:
        """
        Draw detection boxes on image
        
        Args:
            image_path: Path to original image
            results: YOLO prediction results
            output_path: Path to save annotated image
            
        Returns:
            Path to saved annotated image
        """
        # Read original image
        img = cv2.imread(image_path)
        
        if len(results) > 0 and results[0].boxes is not None:
            # Get boxes, classes, and confidences
            boxes = results[0].boxes.xyxy.cpu().numpy()
            classes = results[0].boxes.cls.cpu().numpy()
            confidences = results[0].boxes.conf.cpu().numpy()
            names = results[0].names
            
            # Draw each detection
            for box, cls, conf in zip(boxes, classes, confidences):
                x1, y1, x2, y2 = map(int, box)
                class_name = names[int(cls)]
                label = f"{class_name} {conf:.2f}"
                
                # Choose color based on class
                color = (0, 255, 0) if 'good' in class_name.lower() else (0, 0, 255)
                
                # Draw rectangle and label
                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                cv2.putText(img, label, (x1, y1 - 10), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
        # Save annotated image
        cv2.imwrite(output_path, img)
        return output_path
