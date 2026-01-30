from pydantic import BaseModel, Field
from typing import List, Tuple, Optional
from datetime import datetime


class BoundingBox(BaseModel):
    """Bounding box coordinates for detected text"""
    x: int
    y: int
    width: int
    height: int
    confidence: float = Field(ge=0.0, le=1.0)


class DetectedText(BaseModel):
    """Detected text with metadata"""
    text: str
    bbox: BoundingBox
    language: str = "en"
    translated_text: Optional[str] = None


class TranslationRequest(BaseModel):
    """Request model for translation"""
    source_lang: str = "en"
    target_lang: str = "tr"


class TranslationResponse(BaseModel):
    """Response model after processing"""
    original_image_url: str
    translated_image_url: str
    detected_texts: List[DetectedText]
    processing_time: float
    timestamp: datetime = Field(default_factory=datetime.now)
    total_text_regions: int


class ProcessingStatus(BaseModel):
    """Processing status for real-time updates"""
    stage: str  # "uploading", "ocr", "translating", "inpainting", "rendering", "complete"
    progress: int = Field(ge=0, le=100)
    message: str
