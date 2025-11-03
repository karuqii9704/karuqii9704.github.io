"""
Upload Routes
Handles image upload and analysis
"""

from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
import os
from config import Config
from modules import ImageProcessor, CoffeeAnalyzer
from utils import FileHandler, Validator
from app import model_loader

upload_bp = Blueprint('upload', __name__)


@upload_bp.route('/upload', methods=['POST'])
def upload_image():
    """
    Upload and analyze coffee bean image
    
    Expected form data:
    - file: Image file
    - confidence (optional): Confidence threshold (0-1)
    
    Returns:
    - JSON with analysis results
    """
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file provided'
            }), 400
        
        file = request.files['file']
        
        # Validate file
        is_valid, message = Validator.validate_upload(
            file, 
            Config.ALLOWED_EXTENSIONS,
            Config.MAX_FILE_SIZE
        )
        
        if not is_valid:
            return jsonify({
                'success': False,
                'error': message
            }), 400
        
        # Get confidence threshold (optional)
        confidence = request.form.get('confidence', Config.CONFIDENCE_THRESHOLD)
        is_valid_conf, conf_msg = Validator.validate_confidence(confidence)
        
        if not is_valid_conf:
            return jsonify({
                'success': False,
                'error': conf_msg
            }), 400
        
        confidence = float(confidence)
        
        # Save uploaded file
        filename, filepath = FileHandler.save_upload(file, Config.UPLOAD_FOLDER)
        
        # Validate image
        if not ImageProcessor.validate_image(filepath):
            FileHandler.delete_file(filepath)
            return jsonify({
                'success': False,
                'error': 'Invalid or corrupted image file'
            }), 400
        
        # Use absolute path
        abs_filepath = os.path.abspath(filepath)
        
        # Get image info
        image_info = ImageProcessor.get_image_info(abs_filepath)
        
        # Analyze image
        analyzer = CoffeeAnalyzer(model_loader)
        analysis_result = analyzer.analyze_image(abs_filepath, confidence)
        
        if not analysis_result['success']:
            FileHandler.delete_file(filepath)
            return jsonify(analysis_result), 500
        
        # Draw detections on image
        annotated_filename = f"annotated_{filename}"
        abs_upload_folder = os.path.abspath(Config.UPLOAD_FOLDER)
        annotated_path = os.path.abspath(os.path.join(abs_upload_folder, annotated_filename))
        
        # Get results for drawing
        from modules.model_loader import ModelLoader
        results = model_loader.predict(abs_filepath, conf=confidence)
        ImageProcessor.draw_detections(abs_filepath, results, annotated_path)
        
        # Prepare response
        response = {
            'success': True,
            'analysis_id': filename.split('.')[0],
            'original_filename': secure_filename(file.filename),
            'uploaded_filename': filename,
            'annotated_filename': annotated_filename,
            'image_info': image_info,
            'analysis': {
                'total_beans': analysis_result['total_beans'],
                'good_beans': analysis_result['good_beans'],
                'defect_beans': analysis_result['defect_beans'],
                'good_percentage': analysis_result['good_percentage'],
                'defect_percentage': analysis_result['defect_percentage'],
                'grade': analysis_result['grade'],
                'grade_description': analyzer.get_grade_description(analysis_result['grade']),
                'confidence_threshold': confidence
            },
            'detections_count': len(analysis_result.get('detections', []))
        }
        
        return jsonify(response), 200
        
    except Exception as e:
        print(f"❌ Error in upload: {str(e)}")
        return jsonify({
            'success': False,
            'error': f'Internal server error: {str(e)}'
        }), 500


@upload_bp.route('/analyze/<analysis_id>', methods=['GET'])
def get_analysis(analysis_id):
    """
    Get detailed analysis results
    
    Args:
        analysis_id: ID of analysis (filename without extension)
        
    Returns:
        JSON with detailed analysis
    """
    try:
        # Use absolute path
        abs_upload_folder = os.path.abspath(Config.UPLOAD_FOLDER)
        
        # Find image file
        image_files = [f for f in os.listdir(abs_upload_folder) 
                      if f.startswith(analysis_id) and not f.startswith('annotated_')]
        
        if not image_files:
            return jsonify({
                'success': False,
                'error': 'Analysis not found'
            }), 404
        
        filepath = os.path.abspath(os.path.join(abs_upload_folder, image_files[0]))
        
        # Get confidence from query params
        confidence = float(request.args.get('confidence', Config.CONFIDENCE_THRESHOLD))
        
        # Re-analyze
        analyzer = CoffeeAnalyzer(model_loader)
        analysis_result = analyzer.analyze_image(filepath, confidence)
        
        return jsonify(analysis_result), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
