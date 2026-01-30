from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from app.models.schemas import TranslationResponse, DetectedText
from app.services.pipeline import TranslationPipeline
from app.config import settings
import os
import uuid
import time
import aiofiles

router = APIRouter()

# Initialize the translation pipeline
pipeline = TranslationPipeline()


@router.post("/translate", response_model=TranslationResponse)
async def translate_manga(
    file: UploadFile = File(..., description="Manga page image (JPG/PNG)")
):
    """
    Main endpoint to process manga translation
    
    Workflow:
    1. Upload and validate image
    2. Detect text regions (OCR)
    3. Translate detected text
    4. Inpaint (remove) original text
    5. Render translated text
    6. Return processed image
    """
    start_time = time.time()
    
    # Validate file type
    if not file.content_type in ["image/jpeg", "image/png", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Only JPG/PNG images are supported")
    
    # Check file size
    file_content = await file.read()
    if len(file_content) > settings.max_file_size:
        raise HTTPException(
            status_code=400, 
            detail=f"File size exceeds maximum allowed size ({settings.max_file_size} bytes)"
        )
    
    # Generate unique filename
    file_id = str(uuid.uuid4())
    file_extension = os.path.splitext(file.filename)[1]
    original_filename = f"{file_id}_original{file_extension}"
    original_path = os.path.join(settings.temp_dir, original_filename)
    
    # Save uploaded file
    async with aiofiles.open(original_path, 'wb') as f:
        await f.write(file_content)
    
    try:
        # Process the image through the pipeline
        result = await pipeline.process_image(
            image_path=original_path,
            file_id=file_id
        )
        
        processing_time = time.time() - start_time
        
        # Construct response
        response = TranslationResponse(
            original_image_url=f"/static/{original_filename}",
            translated_image_url=f"/static/{result['translated_filename']}",
            detected_texts=result['detected_texts'],
            processing_time=round(processing_time, 2),
            total_text_regions=len(result['detected_texts'])
        )
        
        return response
        
    except Exception as e:
        # Clean up uploaded file on error
        if os.path.exists(original_path):
            os.remove(original_path)
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")


@router.delete("/cleanup/{file_id}")
async def cleanup_files(file_id: str):
    """Clean up temporary files for a given file_id"""
    try:
        deleted_files = []
        for filename in os.listdir(settings.temp_dir):
            if filename.startswith(file_id):
                file_path = os.path.join(settings.temp_dir, filename)
                os.remove(file_path)
                deleted_files.append(filename)
        
        return {"message": f"Cleaned up {len(deleted_files)} files", "files": deleted_files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup error: {str(e)}")
