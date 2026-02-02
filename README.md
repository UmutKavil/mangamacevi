# MangaMa - Manga Translation Tool 📚🇹🇷

**MangaMa** (Manga Translation Automation) is a powerful web application that automatically translates manga pages from English to Turkish using AI-powered OCR, translation, and image processing technologies.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![Next.js](https://img.shields.io/badge/next.js-14-black)
![FastAPI](https://img.shields.io/badge/fastapi-0.109-009688)
![Docker](https://img.shields.io/badge/docker-ready-blue)

> **⚠️ IMPORTANT: First Run Info**  
> Backend downloads AI models (~500MB total) on **first use**, not at startup.  
> **First translation:** 2-5 minutes | **Subsequent:** 10-30 seconds  
> See [Troubleshooting](#%EF%B8%8F-first-translation-taking-too-long-2-5-minutes) for details.

## 🎯 Features

- **🔍 Text Detection**: Advanced OCR using EasyOCR to detect text regions in manga pages
- **🌐 Smart Translation**: English to Turkish translation using Google Translate API with fallback support
- **🎨 AI Inpainting**: Remove original text using LaMa (Large Mask Inpainting) model with OpenCV fallback
- **✏️ Text Rendering**: Automatically render translated text with Turkish font support (DejaVu Sans)
- **📊 Before/After Comparison**: Interactive visual comparison with instant switching between original and translated
- **⚡ Fast Processing**: Complete translation pipeline in 10-30 seconds with instant result display
- **🐳 Docker Ready**: Fully containerized with Docker Compose - one command deployment
- **🔄 Error Resilience**: Automatic retry mechanisms for network failures with smart fallbacks
- **🏥 Health Monitoring**: Real-time API status checking with auto-reconnect
- **📝 Smart Logging**: Production-ready logging system with different levels
- **🖼️ Image Preloading**: Optimized image loading with preload for instant display
- **🔌 API Proxy**: Next.js API routes for seamless Docker networking

## 🏗️ Tech Stack

### Backend
- **FastAPI**: Modern async web framework
- **EasyOCR**: Multi-language OCR engine
- **OpenCV**: Image processing
- **Pillow**: Text rendering
- **Deep-Translator**: Translation service
- **Simple-Lama-Inpainting**: AI-powered inpainting

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe development
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client
- **React Icons**: Icon library

## 📋 Prerequisites

- Docker & Docker Compose (recommended)
- OR:
  - Python 3.11+
  - Node.js 20+
  - npm or yarn

## 🚀 Quick Start

### Using Docker (Recommended) ⭐

1. **Clone the repository**
```bash
git clone https://github.com/UmutKavil/mangamacevi.git
cd mangamacevi
```

2. **Start the application**
```bash
docker-compose up -d --build
```

That's it! The application will:
- ✅ Build both frontend and backend containers
- ✅ Download required AI models (first run only, ~2GB)
- ✅ Start all services automatically
- ✅ Set up internal Docker networking

3. **Access the application**
- 🌐 **Frontend**: http://localhost:3000
- 🔧 **Backend API**: http://localhost:8000
- 📚 **API Documentation**: http://localhost:8000/docs

4. **⚠️ IMPORTANT - First Run (Model Download)**

**Backend will take 2-5 minutes on first startup!** This is completely normal.

The backend needs to download AI models:
- 📥 **EasyOCR model** (~300MB) - Text detection
- 📥 **LaMa inpainting model** (~200MB) - Image cleaning
- 📥 **Recognition model** (~50MB) - Character recognition

**What you'll see:**

```bash
# Watch the download progress
docker-compose logs -f backend

# You'll see messages like:
# "Downloading: 'https://github.com/...' to /root/.cache/torch/..."
# "Progress: |████████| 100.0% Complete"
# "✅ EasyOCR initialized successfully"
# "✅ Translation Pipeline ready"
# "INFO: Application startup complete"
```

**Frontend will show:**
- 🔴 "✗ API Çevrimdışı" → This is NORMAL during model download
- 🟢 "✓ API Hazır" → Backend is ready to use!

**After first run:**
- Models are cached in Docker volumes
- Subsequent starts take only 10-15 seconds
- No re-download needed unless you run `docker-compose down -v`

### Useful Docker Commands

```bash
# View logs
docker-compose logs -f

# View only backend logs
docker-compose logs -f backend

# Stop services
docker-compose stop

# Start services
docker-compose start

# Restart a specific service
docker-compose restart frontend

# Stop and remove containers
docker-compose down

# Rebuild after code changes
docker-compose up -d --build

# Check container status
docker-compose ps
```

### Manual Setup

#### Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

## 📁 Project Structure

```
mangamacevi/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py            # Application entry point with CORS
│   │   ├── config.py          # Environment-based configuration
│   │   ├── routers/           # API endpoints
│   │   │   └── translation.py # Translation endpoint
│   │   ├── services/          # Business logic
│   │   │   ├── ocr_service.py        # EasyOCR text detection
│   │   │   ├── translation_service.py # Multi-provider translation
│   │   │   ├── inpainting_service.py  # LaMa AI inpainting
│   │   │   ├── text_renderer.py      # Turkish text rendering
│   │   │   └── pipeline.py           # Main processing pipeline
│   │   ├── models/            # Pydantic schemas
│   │   │   └── schemas.py
│   │   └── utils/             # Helper functions
│   │       ├── image_utils.py
│   │       └── font_utils.py
│   ├── temp/                  # Temporary processed images
│   ├── models/                # AI model weights (auto-downloaded)
│   ├── fonts/                 # Turkish font files
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env                   # Environment variables
│
├── frontend/                   # Next.js 14 Frontend
│   ├── src/
│   │   ├── app/               # App Router pages & API routes
│   │   │   ├── page.tsx       # Main page
│   │   │   ├── layout.tsx     # Root layout
│   │   │   └── api/           # Next.js API Routes (Proxy)
│   │   │       ├── health/route.ts      # Health check proxy
│   │   │       ├── translate/route.ts   # Translation proxy
│   │   │       └── cleanup/[fileId]/route.ts
│   │   ├── components/        # React components
│   │   │   ├── ImageUploader.tsx        # Drag & drop uploader
│   │   │   ├── BeforeAfterViewer.tsx    # Result comparison viewer
│   │   │   └── ProcessingStatus.tsx     # Progress indicator
│   │   └── lib/               # Utilities
│   │       ├── api.ts         # API client with retry logic
│   │       └── logger.ts      # Structured logging
│   ├── public/
│   ├── package.json
│   ├── next.config.js         # Next.js configuration
│   ├── tailwind.config.ts     # Tailwind CSS config
│   └── Dockerfile
│
├── docker-compose.yml          # Docker orchestration
└── README.md
```
Architecture

### Frontend → Backend Communication

The application uses **Next.js API Routes** as a proxy layer between the frontend and backend:

```
Browser → Next.js API Route (/api/*) → FastAPI Backend (Docker network)
```

This architecture provides:
- ✅ **Docker networking**: Frontend container connects to backend via `http://backend:8000`
- ✅ **Browser compatibility**: Browser still uses `http://localhost:8000` for static images
- ✅ **Unified origin**: No CORS issues for API calls
- ✅ **Request logging**: Centralized error handling

### Backend API Endpoints

#### POST `/api/translate`
Upload and translate manga page

**Request:**
```bash
curl -X POST "http://localhost:8000/api/translate" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@manga_page.jpg"
```

**Response:**
```json
{
  "original_image_url": "/static/abc123_original.jpg",
  "translated_image_url": "/static/abc123_translated.png",
  "detected_texts": [
    {
      "text": "Hello",
      "translated_text": "Merhaba",
      "bbox": {"x": 100, "y": 200, "width": 80, "height": 30, "confidence": 0.95},
      "language": "en"
    }
  ],
  "processing_time": 12.5,
  "total_text_regions": 1,
  "timestamp": "2026-02-02T12:30:45"
}
```

#### GET `/health`
Health check endpoint - Returns API status

**Response:**
```json
{
  "status": "healthy",
  "sDocker Compose Environment Variables

The `docker-compose.yml` file contains all necessary configuration:

**Backend:**
```yaml
environment:
  - API_HOST=0.0.0.0
  - API_PORT=8000
  - DEBUG=True
  - CORS_ORIGINS=http://localhost:3000,http://localhost:3001,http://frontend:3000
  - OCR_GPU=False
```

**Frontend:**
```yaml
environment:
  - NEXT_PUBLIC_API_URL=http://localhost:8000  # For browser-side static file access
  - BACKEND_URL=http://backend:8000             # For server-side API proxy
```

### Backend `.env` Configuration

Located at `backend/.env` (already configured):

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# CORS Settings (allows frontend containers)
CORS_ORIGINS=http://localhost:3000,http://localhost:3001

# OCR Settings
OCR_LANGUAGES=en,tr
OCR_GPU=False  # Set to True if CUDA-enabled GPU available

# Translation
TRANSLATION_SOURCE_LANG=en
TRANSLATION_TARGET_LANG=tr

# File Settings
MAX_FILE_SIZE=10485760  # 10MB
TEMP_DIR=./temp

# Inpainting
INPAINTING_MODEL_PATH=./models/lama

# Text Rendering
DEFAULT_FONT_PATH=./fonts/arial.ttf
FONT_SIZE_MIN=12
FONT_SIZE_MAX=48
```

### Network Configuration

The application uses Docker's bridge network for inter-container communication:

```yaml
networks:
  mangama-network:
    driver: bridge
```

**Key Points:**
- Frontend container accesses backend via `http://backend:8000`
- Browser accesses frontend via `http://localhost:3000`
- Backend API accessible at `http://localhost:8000` (for testing)
- Static images served from backend to browser via localhost
## ⚙️ Configuration

### Backend Environment Variables

```bash
### 🔴 "API Çevrimdışı" Error on First Startup

**This is COMPLETELY NORMAL on first run!** Don't panic. 😊

**Why it happens:**
- Backend is downloading AI models (300MB+ total)
- Models download from GitHub releases and PyTorch Hub
- Download speed depends on your internet connection
- Can take 2-5 minutes

**How to monitor:**
```bash
# Open a terminal and watch the backend logs
docker-compose logs -f backend

# You should see download progress bars:
# "Downloading: 'https://github.com/enesmsahin/simple-lama-inpainting/releases/...'"
# "Progress: |████████████████| 100.0% Complete"

# Wait until you see:
# "✅ EasyOCR initialized successfully"
# "✅ Translation Pipeline ready"  
# "INFO: Application startup complete"
```

**When to worry:**
- If downloads stop/hang for more than 10 minutes → Check internet connection
- If you see "Connection refused" errors → Backend container may have crashed
- If you see "Out of memory" → Increase Docker memory limit (Settings > Resources)

**Solution:**
```bash
# Just wait! Refresh browser when you see "✓ API Hazır" status
# Or restart if it's been too long:
docker-compose restart backend
```

### ⏱️ First Translation Taking Too Long (2-5 minutes)

**This is 100% NORMAL!** The backend downloads AI models on first use (not at startup).

**Timeline:**
```
📤 User uploads first image
  ↓
🔄 Backend starts OCR → Triggers model download
  ↓  
📥 Downloading EasyOCR models (~300MB)
  ├─ craft_mlt_25k.pth (OCR detection model)
  ├─ english_g2.pth (Recognition model)
  └─ Takes 30-90 seconds depending on internet speed
  ↓
📥 Downloading LaMa model (~200MB)  
  └─ big-lama.pt (Inpainting model)
  └─ Takes 20-60 seconds
  ↓
✅ Models cached - loading into memory (10-20 seconds)
  ↓
✅ Translation complete!

⏱️ Total first run: 2-5 minutes
⏱️ Subsequent runs: 10-30 seconds (models cached!)
```

**How to monitor progress:**
```bash
# Watch the download live
docker-compose logs -f backend

# Look for these messages:
"Downloading: 'https://github.com/enesmsahin/simple-lama-inpainting/releases/download/v0.1.0/big-lama.pt'"
"Progress: |████████████████| 100.0% Complete"
"Downloading recognition model, please wait..."
"✅ EasyOCR initialized successfully"
```

**Important:**
- ⚠️ **Don't restart during download!** You'll lose progress and start over
- ✅ **Models are saved** in Docker volume - won't re-download on restart
- ✅ **Second translation is MUCH faster** - only 10-30 seconds
- ❌ **Don't run `docker-compose down -v`** - this deletes the models!

**If download hangs/fails:**
```bash
# Check internet connection
ping github.com
ping download.pytorch.org

# Check disk space (need 2GB+)
docker system df

# Restart backend only (keeps models if already downloaded)
docker-compose restart backend
```

### Backend Connection Issues
- **Health Check**: Frontend automatically checks backend health every 30 seconds
- **API Status**: Watch the status indicator in the UI (green = online, red = offline)
- **Docker Containers**: Ensure both containers are running
  ```bash
  docker-compose ps
  # Both should show "Up" status
  ```
- **Ports**: Verify ports 3000 and 8000 are not in use
  ```bash
  lsof -i :3000
  lsof -i :8000
  ```
- **Container Networking**: Verify Docker network exists
  ```bash
  docker network ls | grep mangama
  ```

### Container Build Issues
```bash
# Clean rebuild
docker-compose down
docker system prune -f
docker-compose up -d --build
```
# CORS Settings
CORS_ORIGINS=http://localhost:3000

# OCR Settings
OCR_LANGUAGES=en,tr
OCR_GPU=False  # Set to True if CUDA-enabled GPU available

# Translation
TRANSLATION_SOURCE_LANG=en
TRANSLATION_TARGET_LANG=tr

# File Settings
MAX_FILE_SIZE=10485760  # 10MB
```

### Frontend Environment Variables

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🔧 Development
Image Preloading**: Both images (original & translated) preload simultaneously for instant display
- **Loading States**: "Görseller yükleniyor..." message while loading
- **Error Handling**: "Tekrar Yükle" button appears if image fails to load
- **Cache Headers**: Images cached for 1 hour for better performance
- **CORS**: Properly configured for localhost:3000 access
- **Docker Volumes**: Temp files persisted across restarts via Docker volumes

### Backend Optimizations
- **GPU Acceleration**: Set `OCR_GPU=True` if CUDA GPU available (10x faster OCR)
- **Image Preprocessing**: Images automatically resized to max 2048px
- **Font Caching**: Font objects cached for repeated use
- **Async Processing**: FastAPI handles requests asynchronously
- **Lazy Loading**: Heavy models (OCR, LaMa) load on first use, not startup
- **Connection Pooling**: Reusable HTTP connections for translation APIs
- **Docker Volumes**: Models persist between container restarts

### Frontend Optimizations  
- **Image Preloading**: Both original and translated images preload simultaneously
- **API Proxy**: Next.js API routes eliminate CORS preflight requests
- **Static Caching**: Images cached for 1 hour with proper headers
- **Instant Display**: Results show immediately when backend responds (no fake delays)
- **Smart Retry**: Automatic retry logic with exponential backoff
- **Health Monitoring**: Background health checks don't block user interaction

### Docker Optimizations
- **Layer Caching**: Multi-stage builds for faster rebuilds
- **Volume Mounting**: Development mode with hot reload
- **Resource Limits**: Configure in docker-compose.yml if needed
  ```yaml
  deploy:
    resources:
      limits:
        cpus: '2'
        memory: 4G
  ```s are cached.

### Container Restart Issues
```bash
# If frontend shows old cached page
docker-compose restart frontend

# If backend behaves strangely
docker-compose restart backend

# Nuclear option - complete reset
docker-compose down -v  # Warning: removes downloaded models
docker-compose up -d --build
```
# Run with auto-reload
uvicorn app.main:app --reload

# Run tests (coming soon)
pytest

# Format code
black app/
```

### Frontend Development

```bash
# Development server
npm run dev

# Build for production
npm run build

# Lint
npm run lint
```

## 📦 Building for Production

```bash
# Build Docker images
docker-compose build

# Run in production mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 🐛 Troubleshooting

### Backend Connection Issues
- **Health Check**: Frontend automatically checks backend health every 30 seconds
- **API Status**: Watch the status indicator in the UI (green = online, red = offline)
- **Docker**: Ensure both containers are running: `docker ps`
- **Ports**: Verify ports 3000 and 8000 are not in use by other services

### OCR not working
- Ensure EasyOCR models are downloaded (automatic on first run, requires internet)
- Check available disk space for model downloads (2GB+)
- Verify language codes in configuration
- **Lazy Loading**: OCR initializes on first use, not at startup
- **Retry Logic**: 3 automatic retries with progressive backoff (2s, 4s, 6s)

### Translation failures
- **Multiple Translators**: System tries Google, MyMemory, and LibreTranslate in sequence
- **Retry Logic**: Each translator retried 3 times before moving to fallback
- **Network Errors**: Automatic retry with exponential backoff
- Verify internet connection
- Check rate limits for translation APIs

### Inpainting errors
- LaMa model requires significant memory (2GB+)
- **Automatic Fallback**: Falls back to OpenCV inpainting if LaMa fails
- **Retry Logic**: 3 automatic retries for model download
- Check logs for specific error messages

### Turkish Character Issues
- **Font Support**: DejaVu Sans font installed in Docker container
- **Character Testing**: System automatically validates Turkish character support (ü,ş,ç,ı,ö,ğ)
- **Fallback Fonts**: Multiple font fallbacks configured (Liberation, Noto)
- **UTF-8 Encoding**: All text rendering uses UTF-8

### Image Loading Problems
- **Loading States**: Images show spinner while loading
- **Error Handling**: "Tekrar Yükle" button appears if image fails to load
- **Cache Headers**: Images cached for 1 hour for better performance
- **CORS**: Properly configured for localhost:3000 access

## 🚀 Performance Optimization

- **GPU Acceleration**: Set `OCR_GPU=True` if CUDA GPU available
- **Image Preprocessing**: Images are automatically resized to max 2048px
- **Caching**: Font objects are cached for better performance
- **Async Processing**: FastAPI handles requests asynchronously
- **Static File Caching**: 1-hour cache for translated images
- **Lazy Loading**: Heavy models (OCR, LaMa) load on first use
- **Connection Pooling**: Reusable HTTP connections for translations

## 🛡️ Error Handling & Resilience

### Automatic Recovery Features

1. **Network Failure Recovery**
   - 3 automatic retries with progressive backoff (2s, 4s, 6s)
   - Applies to OCR model downloads, translation API calls, and inpainting

2. **Translation Fallback Chain**
   - Primary: Google Translate
   - Fallback 1: MyMemory Translator
   - Fallback 2: LibreTranslate
   - Each service tried 3 times before moving to next

3. **Frontend Error Handling**
   - User-friendly Turkish error messages
   - Distinguishes between client (4xx) and server (5xx) errors
   - Automatic retry for network and timeout errors
   - Backend health monitoring with real-time status

4. **Image Processing Fallbacks**
   - LaMa inpainting → OpenCV inpainting fallback
   - Multiple font sources for Turkish characters
   - Graceful degradation if one stage fails

5. **Logging & Monitoring**
   - Structured logging with levels (DEBUG, INFO, WARN, ERROR)
   - Production mode suppresses debug logs
   - Ready for Sentry/LogRocket integration

## 📄 License

MIT License - feel free to use this project for personal or commercial purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👨‍💻 Author

Built with ❤️ for the manga translation community

## 🙏 Acknowledgments

- [EasyOCR](https://github.com/JaidedAI/EasyOCR) - OCR Engine
- [LaMa](https://github.com/advimman/lama) - Inpainting Model
- [FastAPI](https://fastapi.tiangolo.com/) - Backend Framework
- [Next.js](https://nextjs.org/) - Frontend Framework

---

**Star ⭐ this repo if you find it useful!**
