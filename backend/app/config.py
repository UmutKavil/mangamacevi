from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_prefix=""
    )
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    debug: bool = True
    
    # CORS Settings - will be split from comma-separated string
    cors_origins: str = "http://localhost:3000,http://localhost:3001"
    
    # File Storage
    temp_dir: str = "./temp"
    max_file_size: int = 10485760  # 10MB
    
    # OCR Settings - will be split from comma-separated string
    ocr_languages: str = "en,tr"
    ocr_gpu: bool = False
    
    # Translation Settings
    translation_source_lang: str = "en"
    translation_target_lang: str = "tr"
    
    # Inpainting Settings
    inpainting_model_path: str = "./models/lama"
    
    # Text Rendering
    default_font_path: str = "./fonts/arial.ttf"
    font_size_min: int = 12
    font_size_max: int = 48
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as list"""
        return [x.strip() for x in self.cors_origins.split(",")]
    
    @property
    def ocr_languages_list(self) -> List[str]:
        """Get OCR languages as list"""
        return [x.strip() for x in self.ocr_languages.split(",")]


# Global settings instance
settings = Settings()

# Ensure temp directory exists
os.makedirs(settings.temp_dir, exist_ok=True)
