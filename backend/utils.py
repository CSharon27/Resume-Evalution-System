"""
HireLens Backend Utilities
Helper functions for backend operations
"""

import os
from pathlib import Path
from typing import Optional
import hashlib


def generate_file_hash(file_path: str | Path) -> str:
    """
    Generate MD5 hash of file
    
    Args:
        file_path: Path to file
        
    Returns:
        MD5 hash string
    """
    hash_md5 = hashlib.md5()
    
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    
    return hash_md5.hexdigest()


def validate_file_size(file_path: str | Path, max_size_mb: int = 10) -> bool:
    """
    Validate file size
    
    Args:
        file_path: Path to file
        max_size_mb: Maximum size in MB
        
    Returns:
        True if valid, False otherwise
    """
    file_size = os.path.getsize(file_path)
    max_size_bytes = max_size_mb * 1024 * 1024
    
    return file_size <= max_size_bytes


def clean_filename(filename: str) -> str:
    """
    Clean filename by removing special characters
    
    Args:
        filename: Original filename
        
    Returns:
        Cleaned filename
    """
    import re
    # Remove special characters
    clean = re.sub(r'[^a-zA-Z0-9._-]', '_', filename)
    return clean


def ensure_upload_dir():
    """Ensure upload directory exists"""
    from config.config import UPLOAD_DIR
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_old_uploads(days: int = 7):
    """
    Clean up uploads older than specified days
    
    Args:
        days: Number of days to keep files
    """
    from config.config import UPLOAD_DIR
    import time
    
    if not UPLOAD_DIR.exists():
        return
    
    current_time = time.time()
    max_age = days * 24 * 60 * 60  # Convert to seconds
    
    for file_path in UPLOAD_DIR.iterdir():
        if file_path.is_file():
            file_age = current_time - os.path.getmtime(file_path)
            if file_age > max_age:
                file_path.unlink()
                print(f"Deleted old file: {file_path}")
