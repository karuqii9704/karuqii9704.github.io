"""
File Handler Utility
Handles file operations (save, delete, cleanup)
"""

import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta


class FileHandler:
    
    @staticmethod
    def save_upload(file, upload_folder: str) -> tuple:
        """
        Save uploaded file with unique name
        
        Args:
            file: File object from request
            upload_folder: Folder to save file
            
        Returns:
            Tuple of (filename, filepath)
        """
        # Generate unique filename
        original_filename = secure_filename(file.filename)
        ext = Path(original_filename).suffix
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        
        # Save file
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        return unique_filename, filepath
    
    @staticmethod
    def delete_file(filepath: str) -> bool:
        """
        Delete a file safely
        
        Args:
            filepath: Path to file
            
        Returns:
            True if deleted, False otherwise
        """
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {filepath}: {e}")
            return False
    
    @staticmethod
    def cleanup_old_files(folder: str, max_age_hours: int = 24):
        """
        Clean up old files in folder
        
        Args:
            folder: Folder to clean
            max_age_hours: Maximum age of files in hours
        """
        if not os.path.exists(folder):
            return
        
        cutoff_time = datetime.now() - timedelta(hours=max_age_hours)
        
        for filename in os.listdir(folder):
            filepath = os.path.join(folder, filename)
            
            # Skip .gitkeep files
            if filename == '.gitkeep':
                continue
            
            try:
                file_time = datetime.fromtimestamp(os.path.getmtime(filepath))
                if file_time < cutoff_time:
                    os.remove(filepath)
                    print(f"🗑️ Cleaned up old file: {filename}")
            except Exception as e:
                print(f"Error cleaning up {filename}: {e}")
    
    @staticmethod
    def get_file_size(filepath: str) -> int:
        """
        Get file size in bytes
        
        Args:
            filepath: Path to file
            
        Returns:
            File size in bytes
        """
        return os.path.getsize(filepath) if os.path.exists(filepath) else 0
    
    @staticmethod
    def ensure_folder_exists(folder: str):
        """
        Ensure folder exists, create if not
        
        Args:
            folder: Folder path
        """
        os.makedirs(folder, exist_ok=True)
