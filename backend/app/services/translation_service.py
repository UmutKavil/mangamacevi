from deep_translator import GoogleTranslator, MyMemoryTranslator, LibreTranslator
from typing import List, Optional
from app.models.schemas import DetectedText
from app.config import settings
import time


class TranslationService:
    """Service for translating text with multiple fallback options"""
    
    def __init__(self):
        """Initialize translators with fallback chain"""
        self.translators = []
        
        # Primary: Google Translator
        try:
            self.translators.append((
                "Google",
                GoogleTranslator(
                    source=settings.translation_source_lang,
                    target=settings.translation_target_lang
                )
            ))
            print("✅ Google Translator initialized")
        except Exception as e:
            print(f"⚠️ Google Translator initialization failed: {e}")
        
        # Fallback 1: MyMemory Translator
        try:
            self.translators.append((
                "MyMemory",
                MyMemoryTranslator(
                    source=settings.translation_source_lang,
                    target=settings.translation_target_lang
                )
            ))
            print("✅ MyMemory Translator initialized as fallback")
        except Exception as e:
            print(f"⚠️ MyMemory Translator initialization failed: {e}")
        
        # Fallback 2: LibreTranslate (if available)
        try:
            self.translators.append((
                "Libre",
                LibreTranslator(
                    source=settings.translation_source_lang,
                    target=settings.translation_target_lang,
                    base_url="https://libretranslate.com"
                )
            ))
            print("✅ LibreTranslate initialized as fallback")
        except Exception as e:
            print(f"⚠️ LibreTranslate initialization failed: {e}")
        
        if not self.translators:
            print("⚠️ No translators available! Translation will return original text.")
        
        print(f"✅ Translation service initialized with {len(self.translators)} translator(s)")
    
    def translate_text(self, text: str, max_retries: int = 3) -> str:
        """
        Translate a single text string with retry and fallback
        
        Args:
            text: Text to translate
            max_retries: Maximum retry attempts per translator
            
        Returns:
            Translated text
        """
        if not text or not text.strip():
            return ""
        
        if not self.translators:
            print("⚠️ No translators available")
            return text
        
        # Try each translator in order
        for translator_name, translator in self.translators:
            for attempt in range(max_retries):
                try:
                    translated = translator.translate(text)
                    if translated and translated.strip():
                        return translated
                except Exception as e:
                    if attempt < max_retries - 1:
                        wait_time = (attempt + 1) * 0.5  # Progressive backoff
                        print(f"⚠️ {translator_name} error (attempt {attempt + 1}/{max_retries}), retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        print(f"⚠️ {translator_name} failed after {max_retries} attempts: {e}")
        
        # All translators failed, return original text
        print(f"⚠️ All translation services failed for '{text}', returning original")
        return text
    
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
