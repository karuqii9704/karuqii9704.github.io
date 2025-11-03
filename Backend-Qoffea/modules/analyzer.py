"""
Analyzer Module
Main analysis logic for coffee bean grading
"""

from typing import Dict, List, Tuple
import numpy as np


class CoffeeAnalyzer:
    
    def __init__(self, model_loader):
        """
        Initialize analyzer with model loader
        
        Args:
            model_loader: Instance of ModelLoader
        """
        self.model_loader = model_loader
    
    def analyze_image(self, image_path: str, confidence: float = 0.5) -> Dict:
        """
        Analyze coffee beans in image
        
        Args:
            image_path: Path to image file
            confidence: Confidence threshold
            
        Returns:
            Dictionary with analysis results
        """
        # Run prediction
        results = self.model_loader.predict(image_path, conf=confidence)
        
        if len(results) == 0:
            return {
                'success': False,
                'error': 'No detection results',
                'total_beans': 0
            }
        
        # Extract detection data
        result = results[0]
        
        if result.boxes is None or len(result.boxes) == 0:
            return {
                'success': True,
                'total_beans': 0,
                'good_beans': 0,
                'defect_beans': 0,
                'good_percentage': 0,
                'defect_percentage': 0,
                'grade': 'N/A',
                'detections': []
            }
        
        # Get class names and detections
        class_names = result.names
        boxes = result.boxes.xyxy.cpu().numpy()
        classes = result.boxes.cls.cpu().numpy()
        confidences = result.boxes.conf.cpu().numpy()
        
        # Count good and defect beans
        good_count = 0
        defect_count = 0
        detections = []
        
        for box, cls, conf in zip(boxes, classes, confidences):
            class_id = int(cls)
            class_name = class_names[class_id]
            
            detection = {
                'class_id': class_id,
                'class_name': class_name,
                'confidence': float(conf),
                'bbox': box.tolist()
            }
            detections.append(detection)
            
            # Classify as good or defect
            # coffee-grade-break = defect (cacat)
            # coffee-grade-good = good (baik)
            if 'break' in class_name.lower() or 'defect' in class_name.lower() or 'bad' in class_name.lower():
                defect_count += 1
            else:
                good_count += 1
        
        total_beans = good_count + defect_count
        
        # Calculate percentages
        good_percentage = (good_count / total_beans * 100) if total_beans > 0 else 0
        defect_percentage = (defect_count / total_beans * 100) if total_beans > 0 else 0
        
        # Determine overall grade
        grade = self._calculate_grade(good_percentage)
        
        return {
            'success': True,
            'total_beans': total_beans,
            'good_beans': good_count,
            'defect_beans': defect_count,
            'good_percentage': round(good_percentage, 2),
            'defect_percentage': round(defect_percentage, 2),
            'grade': grade,
            'detections': detections,
            'class_names': class_names
        }
    
    def _calculate_grade(self, good_percentage: float) -> str:
        """
        Calculate overall grade based on good percentage
        
        Args:
            good_percentage: Percentage of good beans
            
        Returns:
            Grade (A, B, or C)
        """
        if good_percentage >= 85:
            return 'A'
        elif good_percentage >= 70:
            return 'B'
        else:
            return 'C'
    
    def get_grade_description(self, grade: str) -> str:
        """
        Get description for grade
        
        Args:
            grade: Grade letter (A, B, or C)
            
        Returns:
            Description text
        """
        descriptions = {
            'A': 'Excellent quality - Very low defect rate, suitable for specialty coffee',
            'B': 'Good quality - Acceptable for commercial grade coffee',
            'C': 'Fair quality - Higher defect rate, may require additional sorting'
        }
        return descriptions.get(grade, 'No description available')
