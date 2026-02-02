import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from typing import List, Tuple, Optional
from app.models.schemas import DetectedText
import os


class TextRenderer:
    """Service for rendering translated text onto cleaned images"""
    
    def __init__(self, default_font_path: Optional[str] = None):
        """
        Initialize text renderer with fallback fonts
        
        Args:
            default_font_path: Path to default font file
        """
        self.default_font_path = default_font_path
        self.font_cache = {}
        
        # Define fallback font paths prioritizing Turkish character support
        self.fallback_fonts = [
            # macOS fonts with Turkish support
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",  # Best Unicode support
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            "/System/Library/Fonts/Supplemental/Verdana.ttf",
            "/System/Library/Fonts/Helvetica.ttc",
            "/Library/Fonts/Arial.ttf",
            # Linux fonts with Turkish support
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",  # Excellent Unicode
            "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-R.ttf",
            "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
            # Windows fonts with Turkish support
            "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\verdana.ttf",
            "C:\\Windows\\Fonts\\calibri.ttf",
            "C:\\Windows\\Fonts\\segoeui.ttf",
        ]
        
        # Find first available fallback font
        self.system_font = None
        for font_path in self.fallback_fonts:
            if os.path.exists(font_path):
                self.system_font = font_path
                print(f"✅ Found system font with Turkish support: {font_path}")
                break
        
        if not self.system_font:
            print("⚠️ No system fonts found, text may not display correctly")
        
        print("✅ Text renderer initialized")
    
    def render_text(self, 
                   image: np.ndarray, 
                   detected_texts: List[DetectedText],
                   font_path: Optional[str] = None) -> np.ndarray:
        """
        Render all translated texts onto the image with Turkish character support
        
        Args:
            image: Input image (BGR format from OpenCV)
            detected_texts: List of DetectedText objects with translations
            font_path: Optional custom font path
            
        Returns:
            Image with rendered text (BGR format)
        """
        # Convert BGR (OpenCV) to RGB (PIL)
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(image_rgb)
        draw = ImageDraw.Draw(pil_image)
        
        for det_text in detected_texts:
            if not det_text.translated_text:
                continue
            
            # Ensure text is properly encoded
            text_to_render = str(det_text.translated_text)
            
            # Calculate optimal font size for this text region
            font_size = self._calculate_font_size(
                text_to_render,
                det_text.bbox.width,
                det_text.bbox.height,
                font_path
            )
            
            # Load font with Turkish character support
            font = self._get_font(font_path or self.default_font_path or self.system_font, font_size)
            
            # Calculate text position (centered in bounding box)
            try:
                text_bbox = draw.textbbox((0, 0), text_to_render, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
            except Exception as e:
                print(f"⚠️ Error calculating text bbox: {e}")
                # Fallback to approximate dimensions
                text_width = len(text_to_render) * font_size // 2
                text_height = font_size
            
            x = det_text.bbox.x + (det_text.bbox.width - text_width) // 2
            y = det_text.bbox.y + (det_text.bbox.height - text_height) // 2
            
            # Draw text with black color (typical for manga)
            try:
                draw.text(
                    (x, y),
                    text_to_render,
                    font=font,
                    fill=(0, 0, 0),  # Black text
                    stroke_width=0,
                    encoding='utf-8'
                )
                print(f"✏️ Rendered: '{text_to_render}' at ({x}, {y})")
            except Exception as e:
                print(f"⚠️ Error rendering text '{text_to_render}': {e}")
        
        # Convert back to BGR for OpenCV
        result_rgb = np.array(pil_image)
        result_bgr = cv2.cvtColor(result_rgb, cv2.COLOR_RGB2BGR)
        
        print(f"✅ Rendered {len(detected_texts)} text regions")
        return result_bgr
    
    def _calculate_font_size(self, 
                            text: str, 
                            bbox_width: int, 
                            bbox_height: int,
                            font_path: Optional[str] = None,
                            min_size: int = 12,
                            max_size: int = 48) -> int:
        """
        Calculate optimal font size to fit text in bounding box
        
        Args:
            text: Text to render
            bbox_width: Width of bounding box
            bbox_height: Height of bounding box
            font_path: Path to font file
            min_size: Minimum font size
            max_size: Maximum font size
            
        Returns:
            Optimal font size
        """
        # Binary search for optimal font size
        low, high = min_size, max_size
        optimal_size = min_size
        
        draw = ImageDraw.Draw(Image.new('RGB', (1, 1)))
        
        while low <= high:
            mid = (low + high) // 2
            font = self._get_font(font_path or self.default_font_path, mid)
            
            # Get text dimensions
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Check if text fits
            if text_width <= bbox_width * 0.9 and text_height <= bbox_height * 0.9:
                optimal_size = mid
                low = mid + 1
            else:
                high = mid - 1
        
        return optimal_size
    
    def _get_font(self, font_path: Optional[str], size: int) -> ImageFont.FreeTypeFont:
        """
        Get font from cache or load it with fallback chain and Turkish character support
        
        Args:
            font_path: Path to font file
            size: Font size
            
        Returns:
            PIL ImageFont object
        """
        cache_key = f"{font_path}_{size}"
        
        if cache_key in self.font_cache:
            return self.font_cache[cache_key]
        
        # Try fonts in priority order
        font_candidates = []
        if font_path and os.path.exists(font_path):
            font_candidates.append(font_path)
        if self.system_font:
            font_candidates.append(self.system_font)
        font_candidates.extend([f for f in self.fallback_fonts if os.path.exists(f)])
        
        # Turkish test characters
        turkish_chars = "üşçığö ÜŞÇIĞÖ"
        
        font = None
        for candidate in font_candidates:
            try:
                test_font = ImageFont.truetype(candidate, size)
                # Test if font supports Turkish characters
                try:
                    # Try to get bbox for Turkish characters to verify support
                    test_image = Image.new('RGB', (1, 1))
                    test_draw = ImageDraw.Draw(test_image)
                    test_draw.textbbox((0, 0), turkish_chars, font=test_font)
                    font = test_font
                    print(f"✅ Using font: {candidate} (Turkish characters supported)")
                    break
                except:
                    # Font doesn't support Turkish characters well, try next
                    continue
            except Exception as e:
                continue
        
        # Ultimate fallback: use any working font
        if font is None:
            for candidate in font_candidates:
                try:
                    font = ImageFont.truetype(candidate, size)
                    print(f"⚠️ Using font: {candidate} (Turkish support uncertain)")
                    break
                except:
                    continue
        
        # Last resort: PIL default font
        if font is None:
            try:
                font = ImageFont.load_default()
                print("⚠️ Using PIL default font (limited character support)")
            except Exception as e:
                font = ImageFont.load_default()
        
        self.font_cache[cache_key] = font
        return font
    
    def add_background_box(self,
                          image: np.ndarray,
                          detected_texts: List[DetectedText],
                          bg_color: Tuple[int, int, int] = (255, 255, 255),
                          opacity: float = 0.9) -> np.ndarray:
        """
        Add semi-transparent background boxes behind text for better readability
        
        Args:
            image: Input image
            detected_texts: List of text regions
            bg_color: Background color (BGR)
            opacity: Background opacity (0-1)
            
        Returns:
            Image with background boxes
        """
        overlay = image.copy()
        
        for det_text in detected_texts:
            bbox = det_text.bbox
            cv2.rectangle(
                overlay,
                (bbox.x, bbox.y),
                (bbox.x + bbox.width, bbox.y + bbox.height),
                bg_color,
                -1  # Filled rectangle
            )
        
        # Blend overlay with original image
        result = cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0)
        return result
