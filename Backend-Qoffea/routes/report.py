"""
Report Routes
Handles PDF report generation and download
"""

from flask import Blueprint, jsonify, send_file
import os
from config import Config
from modules import CoffeeAnalyzer
from utils import FileHandler
from app import model_loader

report_bp = Blueprint('report', __name__)


@report_bp.route('/report/<analysis_id>/download', methods=['GET'])
def download_report(analysis_id):
    """
    Generate and download PDF report
    
    Args:
        analysis_id: ID of analysis
        
    Returns:
        PDF file
    """
    try:
        # Use absolute paths
        abs_upload_folder = os.path.abspath(Config.UPLOAD_FOLDER)
        abs_report_folder = os.path.abspath(Config.REPORT_FOLDER)
        
        # Find image file
        image_files = [f for f in os.listdir(abs_upload_folder) 
                      if f.startswith(analysis_id) and not f.startswith('annotated_')]
        
        if not image_files:
            return jsonify({
                'success': False,
                'error': 'Analysis not found'
            }), 404
        
        filepath = os.path.abspath(os.path.join(abs_upload_folder, image_files[0]))
        annotated_path = os.path.abspath(os.path.join(abs_upload_folder, f"annotated_{image_files[0]}"))
        
        # Re-analyze to get fresh data with all NMS parameters
        analyzer = CoffeeAnalyzer(model_loader)
        analysis_result = analyzer.analyze_image(
            filepath, 
            Config.CONFIDENCE_THRESHOLD,
            Config.IOU_THRESHOLD,
            Config.MAX_DETECTIONS
        )
        
        # Generate PDF report
        from modules.pdf_generator import PDFGenerator
        pdf_generator = PDFGenerator()
        
        pdf_filename = f"report_{analysis_id}.pdf"
        pdf_path = os.path.abspath(os.path.join(abs_report_folder, pdf_filename))
        
        pdf_generator.generate_report(
            analysis_result=analysis_result,
            original_image_path=filepath,
            annotated_image_path=annotated_path if os.path.exists(annotated_path) else None,
            output_path=pdf_path,
            analyzer=analyzer
        )
        
        # Send PDF file
        return send_file(
            pdf_path,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=pdf_filename
        )
        
    except Exception as e:
        print(f"❌ Error generating report: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@report_bp.route('/cleanup', methods=['POST'])
def cleanup_files():
    """
    Cleanup old temporary files
    
    Returns:
        JSON with cleanup status
    """
    try:
        abs_upload_folder = os.path.abspath(Config.UPLOAD_FOLDER)
        abs_report_folder = os.path.abspath(Config.REPORT_FOLDER)
        
        FileHandler.cleanup_old_files(abs_upload_folder, max_age_hours=24)
        FileHandler.cleanup_old_files(abs_report_folder, max_age_hours=24)
        
        return jsonify({
            'success': True,
            'message': 'Cleanup completed'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
