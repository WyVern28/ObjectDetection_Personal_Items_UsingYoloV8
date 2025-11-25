"""
Validation utilities for file uploads and inputs
"""

import os
import cv2
from app.config import Config


def allowed_file(filename: str) -> bool:
    """
    Check if file extension is allowed

    Args:
        filename: Name of the file

    Returns:
        True if extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def validate_image(filepath: str) -> bool:
    """
    Validate if file is a valid image

    Args:
        filepath: Path to the image file

    Returns:
        True if valid image, False otherwise
    """
    try:
        # Check if file exists
        if not os.path.exists(filepath):
            return False

        # Try to read with OpenCV
        img = cv2.imread(filepath)
        if img is None:
            return False

        # Check dimensions
        if img.shape[0] < 1 or img.shape[1] < 1:
            return False

        return True

    except Exception:
        return False


def validate_confidence(conf: float) -> bool:
    """
    Validate confidence threshold value

    Args:
        conf: Confidence value

    Returns:
        True if valid, False otherwise
    """
    return 0 < conf <= 1


def validate_camera_index(index: int) -> bool:
    """
    Validate camera index

    Args:
        index: Camera index

    Returns:
        True if valid, False otherwise
    """
    return 0 <= index < 10  # Reasonable limit
