import easyocr
import cv2
import numpy as np
from typing import List, Tuple
from app.models.schemas import DetectedText, BoundingBox
from app.config import settings
import time


class OCRService:
    """Service for text detection and recognition using EasyOCR"""
    
    def __init__(self):
        """Initialize EasyOCR reader"""
        self.reader = None
        print("⏳ OCR Service created, will initialize on first use")
    
    def _initialize_reader(self, max_retries: int = 3):
        """Lazy initialization of EasyOCR reader with retry"""
        if self.reader is not None:
            return
        
        last_error = None
        for attempt in range(max_retries):
            try:
                print(f"📥 Downloading EasyOCR models (attempt {attempt + 1}/{max_retries})...")
                self.reader = easyocr.Reader(
                    settings.ocr_languages_list,
                    gpu=settings.ocr_gpu,
                    verbose=True,
                    download_enabled=True
                )
                print("✅ EasyOCR initialized successfully")
                return
            except Exception as e:
                last_error = e
                if "urlopen error" in str(e) or "name resolution" in str(e) or "Connection" in str(e):
                    wait_time = (attempt + 1) * 2  # Progressive backoff: 2s, 4s, 6s
                    print(f"⚠️ Network error during EasyOCR initialization (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        print(f"⏳ Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        print(f"❌ Failed to initialize EasyOCR after {max_retries} attempts due to network issues")
                        print(f"💡 Please check your internet connection or DNS settings")
                else:
                    print(f"❌ Failed to initialize EasyOCR: {e}")
                    break
        
        raise RuntimeError(f"Failed to initialize EasyOCR: {last_error}")
    
    def detect_text(self, image_path: str) -> List[DetectedText]:
        """
        Detect and extract text from image
        
        Args:
            image_path: Path to the manga page image
            
        Returns:
            List of DetectedText objects with bounding boxes and extracted text
        """
        # Initialize reader on first use
        self._initialize_reader()
        
        # Read image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to read image: {image_path}")
        
        # Perform OCR
        results = self.reader.readtext(image)
        
        detected_texts = []
        for detection in results:
            bbox_coords, text, confidence = detection
            
            # Convert bbox coordinates to our format
            # EasyOCR returns [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
            x_coords = [point[0] for point in bbox_coords]
            y_coords = [point[1] for point in bbox_coords]
            
            x = int(min(x_coords))
            y = int(min(y_coords))
            width = int(max(x_coords) - min(x_coords))
            height = int(max(y_coords) - min(y_coords))
            
            # Filter out low confidence detections
            if confidence < 0.3:
                continue
            
            # Filter out very small text regions (likely noise)
            if width < 10 or height < 10:
                continue
            
            bbox = BoundingBox(
                x=x,
                y=y,
                width=width,
                height=height,
                confidence=round(confidence, 3)
            )
            
            detected_text = DetectedText(
                text=text.strip(),
                bbox=bbox,
                language=settings.translation_source_lang
            )
            
            detected_texts.append(detected_text)
        
        print(f"📝 Detected {len(detected_texts)} text regions")
        return detected_texts
    
    def get_text_mask(self, image_shape: Tuple[int, int, int], 
                      detected_texts: List[DetectedText],
                      padding: int = 5) -> np.ndarray:
        """
        Create a binary mask for all detected text regions
        
        Args:
            image_shape: Shape of the original image (height, width, channels)
            detected_texts: List of detected text objects
            padding: Extra padding around text regions (pixels)
            
        Returns:
            Binary mask with text regions marked as white (255)
        """
        height, width = image_shape[:2]
        mask = np.zeros((height, width), dtype=np.uint8)
        
        for det_text in detected_texts:
            bbox = det_text.bbox
            x1 = max(0, bbox.x - padding)
            y1 = max(0, bbox.y - padding)
            x2 = min(width, bbox.x + bbox.width + padding)
            y2 = min(height, bbox.y + bbox.height + padding)
            
            # Mark text region in mask
            mask[y1:y2, x1:x2] = 255
        
        return mask
