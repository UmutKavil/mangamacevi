from PIL import ImageFont
import os
from typing import Optional, List


def get_available_fonts() -> List[str]:
    """
    Get list of available system fonts
    
    Returns:
        List of font paths
    """
    font_dirs = [
        "/usr/share/fonts/truetype/",
        "/System/Library/Fonts/",
        "C:/Windows/Fonts/",
    ]
    
    available_fonts = []
    
    for font_dir in font_dirs:
        if os.path.exists(font_dir):
            for root, dirs, files in os.walk(font_dir):
                for file in files:
                    if file.endswith(('.ttf', '.otf')):
                        available_fonts.append(os.path.join(root, file))
    
    return available_fonts


def find_font_with_unicode_support(unicode_ranges: Optional[List[str]] = None) -> Optional[str]:
    """
    Find a system font that supports specified Unicode ranges
    
    Args:
        unicode_ranges: List of Unicode ranges to check
        
    Returns:
        Path to suitable font or None
    """
    # Common fonts with good Turkish support
    preferred_fonts = [
        "DejaVuSans.ttf",
        "Arial.ttf",
        "LiberationSans-Regular.ttf",
        "FreeSans.ttf",
    ]
    
    available_fonts = get_available_fonts()
    
    # Check for preferred fonts first
    for preferred in preferred_fonts:
        for font_path in available_fonts:
            if preferred in font_path:
                return font_path
    
    # Return first available font
    return available_fonts[0] if available_fonts else None


def get_default_manga_font() -> str:
    """
    Get default font suitable for manga text
    
    Returns:
        Path to default font
    """
    font_path = find_font_with_unicode_support()
    
    if font_path is None:
        # Fallback to PIL default font
        return ""
    
    return font_path
