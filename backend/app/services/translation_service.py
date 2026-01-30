from deep_translator import GoogleTranslator
from typing import List
from app.models.schemas import DetectedText
from app.config import settings


class TranslationService:
    """Service for translating text using Google Translate"""
    
    def __init__(self):
        """Initialize translator"""
        self.translator = GoogleTranslator(
            source=settings.translation_source_lang,
            target=settings.translation_target_lang
        )
        print("✅ Translation service initialized")
    
    def translate_text(self, text: str) -> str:
        """
        Translate a single text string
        
        Args:
            text: Text to translate
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return ""
        
        try:
            translated = self.translator.translate(text)
            return translated
        except Exception as e:
            print(f"⚠️ Translation error for '{text}': {e}")
            return text  # Return original text on error
    
    def translate_detected_texts(self, detected_texts: List[DetectedText]) -> List[DetectedText]:
        """
        Translate all detected text objects
        
        Args:
            detected_texts: List of DetectedText objects
            
        Returns:
            List of DetectedText objects with translated_text filled
        """
        for det_text in detected_texts:
            translated = self.translate_text(det_text.text)
            det_text.translated_text = translated
            print(f"🔄 '{det_text.text}' → '{translated}'")
        
        print(f"✅ Translated {len(detected_texts)} text regions")
        return detected_texts
    
    def batch_translate(self, texts: List[str]) -> List[str]:
        """
        Translate multiple texts at once
        
        Args:
            texts: List of text strings to translate
            
        Returns:
            List of translated text strings
        """
        translations = []
        for text in texts:
            translations.append(self.translate_text(text))
        return translations
