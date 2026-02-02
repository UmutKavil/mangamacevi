import cv2
import numpy as np
from typing import Optional
from simple_lama_inpainting import SimpleLama
import time


class InpaintingService:
    """Service for removing text from images using inpainting"""
    
    def __init__(self):
        """Initialize inpainting model"""
        self.lama_model = None
        self._initialize_model()
    
    def _initialize_model(self, max_retries: int = 3):
        """Lazy initialization of LaMa model with retry"""
        last_error = None
        for attempt in range(max_retries):
            try:
                print(f"📥 Loading LaMa inpainting model (attempt {attempt + 1}/{max_retries})...")
                self.lama_model = SimpleLama()
                print("✅ LaMa inpainting model initialized")
                return
            except Exception as e:
                last_error = e
                if "urlopen error" in str(e) or "name resolution" in str(e) or "Connection" in str(e):
                    print(f"⚠️ Network error during LaMa model download (attempt {attempt + 1}/{max_retries})")
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 2
                        print(f"⏳ Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                    else:
                        print(f"❌ Failed to download LaMa model after {max_retries} attempts")
                        print("📝 Falling back to OpenCV inpainting")
                else:
                    print(f"⚠️ Failed to initialize LaMa model: {e}")
                    print("📝 Falling back to OpenCV inpainting")
                    break
        
        self.lama_model = None
    
    def inpaint(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Remove text from image using inpainting
        
        Args:
            image: Input image (BGR format)
            mask: Binary mask where white (255) indicates areas to inpaint
            
        Returns:
            Inpainted image with text removed
        """
        if self.lama_model is not None:
            return self._inpaint_with_lama(image, mask)
        else:
            return self._inpaint_with_opencv(image, mask)
    
    def _inpaint_with_lama(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Inpaint using LaMa model (state-of-the-art)
        
        Args:
            image: Input image (BGR format)
            mask: Binary mask
            
        Returns:
            Inpainted image
        """
        try:
            # Convert BGR to RGB for LaMa
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # LaMa expects mask to be single channel
            if len(mask.shape) == 3:
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            
            # Perform inpainting
            result_rgb = self.lama_model(image_rgb, mask)
            
            # Convert back to BGR
            result_bgr = cv2.cvtColor(result_rgb, cv2.COLOR_RGB2BGR)
            
            print("✅ Inpainting completed with LaMa model")
            return result_bgr
            
        except Exception as e:
            print(f"⚠️ LaMa inpainting failed: {e}")
            print("📝 Falling back to OpenCV inpainting")
            return self._inpaint_with_opencv(image, mask)
    
    def _inpaint_with_opencv(self, image: np.ndarray, mask: np.ndarray) -> np.ndarray:
        """
        Inpaint using OpenCV (fallback method)
        
        Args:
            image: Input image (BGR format)
            mask: Binary mask
            
        Returns:
            Inpainted image
        """
        # Ensure mask is single channel
        if len(mask.shape) == 3:
            mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        
        # Use Telea algorithm for inpainting
        result = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        
        print("✅ Inpainting completed with OpenCV")
        return result
    
    def enhance_mask(self, mask: np.ndarray, dilation_size: int = 3) -> np.ndarray:
        """
        Enhance mask by dilating it slightly to ensure complete text removal
        
        Args:
            mask: Binary mask
            dilation_size: Size of dilation kernel
            
        Returns:
            Enhanced mask
        """
        kernel = np.ones((dilation_size, dilation_size), np.uint8)
        dilated_mask = cv2.dilate(mask, kernel, iterations=1)
        return dilated_mask
