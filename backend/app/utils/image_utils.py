import cv2
import numpy as np
from typing import Tuple


def resize_image(image: np.ndarray, max_dimension: int = 2048) -> np.ndarray:
    """
    Resize image if it exceeds maximum dimension while maintaining aspect ratio
    
    Args:
        image: Input image
        max_dimension: Maximum allowed dimension (width or height)
        
    Returns:
        Resized image
    """
    height, width = image.shape[:2]
    
    if height <= max_dimension and width <= max_dimension:
        return image
    
    # Calculate scaling factor
    scale = max_dimension / max(height, width)
    new_width = int(width * scale)
    new_height = int(height * scale)
    
    resized = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
    return resized


def preprocess_for_ocr(image: np.ndarray) -> np.ndarray:
    """
    Preprocess image for better OCR results
    
    Args:
        image: Input image (BGR)
        
    Returns:
        Preprocessed image
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding for better text detection
    processed = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        11,
        2
    )
    
    return processed


def enhance_contrast(image: np.ndarray) -> np.ndarray:
    """
    Enhance image contrast using CLAHE
    
    Args:
        image: Input image
        
    Returns:
        Enhanced image
    """
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge channels
    enhanced_lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    return enhanced


def validate_image(image_path: str) -> Tuple[bool, str]:
    """
    Validate if image can be loaded and processed
    
    Args:
        image_path: Path to image file
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        image = cv2.imread(image_path)
        if image is None:
            return False, "Failed to load image"
        
        height, width = image.shape[:2]
        if height < 100 or width < 100:
            return False, "Image too small (minimum 100x100 pixels)"
        
        return True, "Valid image"
        
    except Exception as e:
        return False, f"Image validation error: {str(e)}"
