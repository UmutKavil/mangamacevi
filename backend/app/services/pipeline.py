import cv2
import os
from typing import Dict, List
from app.services.ocr_service import OCRService
from app.services.translation_service import TranslationService
from app.services.inpainting_service import InpaintingService
from app.services.text_renderer import TextRenderer
from app.models.schemas import DetectedText
from app.config import settings


class TranslationPipeline:
    """
    Main pipeline orchestrating the entire manga translation process
    
    Workflow:
    1. OCR - Detect and extract text
    2. Translation - Translate text to target language
    3. Inpainting - Remove original text from image
    4. Rendering - Draw translated text
    """
    
    def __init__(self):
        """Initialize all services"""
        print("🚀 Initializing Translation Pipeline...")
        self.ocr_service = OCRService()
        self.translation_service = TranslationService()
        self.inpainting_service = InpaintingService()
        self.text_renderer = TextRenderer(settings.default_font_path)
        print("✅ Translation Pipeline ready")
    
    async def process_image(self, image_path: str, file_id: str, use_gpu: bool = False) -> Dict:
        """
        Process a manga page through the complete pipeline with error handling
        
        Args:
            image_path: Path to the uploaded manga page
            file_id: Unique identifier for this processing job
            use_gpu: Whether to use GPU for processing (default: False)
            
        Returns:
            Dictionary with processing results
        """
        print(f"\n{'='*60}")
        print(f"📖 Processing manga page: {file_id}")
        print(f"🖥️ Device: {'GPU (Ekran Kartı)' if use_gpu else 'CPU (İşlemci)'}")
        print(f"{'='*60}\n")
        
        try:
            # Step 1: OCR - Detect text regions
            print("🔍 Step 1: Detecting text regions...")
            try:
                detected_texts = self.ocr_service.detect_text(image_path, use_gpu=use_gpu)
            except Exception as e:
                print(f"❌ OCR failed: {e}")
                raise RuntimeError(f"Text detection failed: {str(e)}")
            
            if not detected_texts:
                print("⚠️ No text detected in image")
                # Return original image if no text detected
                import shutil
                translated_filename = f"{file_id}_translated.png"
                translated_path = os.path.join(settings.temp_dir, translated_filename)
                shutil.copy(image_path, translated_path)
                return {
                    'translated_filename': translated_filename,
                    'detected_texts': [],
                    'message': 'No text detected, returning original image'
                }
            
            # Step 2: Translation
            print(f"\n🌐 Step 2: Translating {len(detected_texts)} text regions...")
            try:
                detected_texts = self.translation_service.translate_detected_texts(detected_texts)
            except Exception as e:
                print(f"⚠️ Translation service error: {e}")
                print("📝 Continuing with original text...")
                # If translation fails, use original text
                for text in detected_texts:
                    if not text.translated_text:
                        text.translated_text = text.text
            
            # Step 3: Inpainting - Remove original text
            print("\n🎨 Step 3: Removing original text (inpainting)...")
            try:
                image = cv2.imread(image_path)
                if image is None:
                    raise ValueError(f"Failed to read image: {image_path}")
                    
                mask = self.ocr_service.get_text_mask(image.shape, detected_texts, padding=5)
                
                # Enhance mask for better inpainting
                mask = self.inpainting_service.enhance_mask(mask, dilation_size=5)
                
                # Perform inpainting
                cleaned_image = self.inpainting_service.inpaint(image, mask)
            except Exception as e:
                print(f"⚠️ Inpainting failed: {e}")
                print("📝 Using original image as base...")
                cleaned_image = image if image is not None else cv2.imread(image_path)
            
            # Step 4: Rendering - Add translated text
            print("\n✏️ Step 4: Rendering translated text...")
            try:
                final_image = self.text_renderer.render_text(cleaned_image, detected_texts)
            except Exception as e:
                print(f"⚠️ Text rendering failed: {e}")
                print("📝 Using cleaned image without new text...")
                final_image = cleaned_image
            
            # Save final image
            translated_filename = f"{file_id}_translated.png"
            translated_path = os.path.join(settings.temp_dir, translated_filename)
            
            try:
                success = cv2.imwrite(translated_path, final_image)
                if not success:
                    raise IOError(f"Failed to save image to {translated_path}")
            except Exception as e:
                print(f"❌ Failed to save final image: {e}")
                raise RuntimeError(f"Failed to save processed image: {str(e)}")
            
            print(f"\n✅ Processing complete!")
            print(f"📁 Output saved: {translated_filename}")
            print(f"{'='*60}\n")
            
            return {
                'translated_filename': translated_filename,
                'detected_texts': detected_texts,
                'message': 'Processing successful'
            }
            
        except Exception as e:
            print(f"\n❌ Pipeline error: {e}")
            print(f"{'='*60}\n")
            raise
    
    def cleanup(self, file_id: str):
        """
        Clean up temporary files for a given processing job
        
        Args:
            file_id: Unique identifier for the processing job
        """
        for filename in os.listdir(settings.temp_dir):
            if filename.startswith(file_id):
                file_path = os.path.join(settings.temp_dir, filename)
                try:
                    os.remove(file_path)
                    print(f"🗑️ Removed: {filename}")
                except Exception as e:
                    print(f"⚠️ Failed to remove {filename}: {e}")
