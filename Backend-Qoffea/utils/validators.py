"""
Validator Utility
Input validation functions
"""

from pathlib import Path
from werkzeug.datastructures import FileStorage


class Validator:
    
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def allowed_file(filename: str, allowed_extensions: set = None) -> bool:
        """
        Check if file extension is allowed
        
        Args:
            filename: Name of file
            allowed_extensions: Set of allowed extensions
            
        Returns:
            True if allowed, False otherwise
        """
        if allowed_extensions is None:
            allowed_extensions = Validator.ALLOWED_EXTENSIONS
        
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in allowed_extensions
    
    @staticmethod
    def validate_file_size(file: FileStorage, max_size: int = None) -> tuple:
        """
        Validate file size
        
        Args:
            file: File object
            max_size: Maximum size in bytes
            
        Returns:
            Tuple of (is_valid, message)
        """
        if max_size is None:
            max_size = Validator.MAX_FILE_SIZE
        
        # Read file to check size
        file.seek(0, 2)  # Seek to end
        size = file.tell()
        file.seek(0)  # Reset to beginning
        
        if size > max_size:
            max_mb = max_size / (1024 * 1024)
            return False, f"File size exceeds {max_mb}MB limit"
        
        return True, "Valid size"
    
    @staticmethod
    def validate_upload(file: FileStorage, allowed_extensions: set = None, 
                       max_size: int = None) -> tuple:
        """
        Complete validation for uploaded file
        
        Args:
            file: File object
            allowed_extensions: Set of allowed extensions
            max_size: Maximum size in bytes
            
        Returns:
            Tuple of (is_valid, message)
        """
        # Check if file exists
        if not file or file.filename == '':
            return False, "No file provided"
        
        # Check extension
        if not Validator.allowed_file(file.filename, allowed_extensions):
            return False, f"Invalid file type. Allowed: {', '.join(Validator.ALLOWED_EXTENSIONS)}"
        
        # Check size
        is_valid_size, size_msg = Validator.validate_file_size(file, max_size)
        if not is_valid_size:
            return False, size_msg
        
        return True, "Valid file"
    
    @staticmethod
    def validate_confidence(confidence: float) -> tuple:
        """
        Validate confidence threshold value
        
        Args:
            confidence: Confidence value
            
        Returns:
            Tuple of (is_valid, message)
        """
        try:
            conf = float(confidence)
            if 0 <= conf <= 1:
                return True, "Valid confidence"
            else:
                return False, "Confidence must be between 0 and 1"
        except (ValueError, TypeError):
            return False, "Invalid confidence value"
