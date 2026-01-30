from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.config import settings
from app.routers import translation
import os

# Create FastAPI application
app = FastAPI(
    title="MangaMa - Manga Translation API",
    description="Automated manga translation from English to Turkish",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for serving processed images)
if os.path.exists(settings.temp_dir):
    app.mount("/static", StaticFiles(directory=settings.temp_dir), name="static")

# Include routers
app.include_router(translation.router, prefix="/api", tags=["Translation"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MangaMa API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "debug_mode": settings.debug
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.debug
    )
