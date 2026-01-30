# MangaMa - Manga Translation Tool 📚🇹🇷

**MangaMa** (Manga Translation Automation) is a powerful web application that automatically translates manga pages from English to Turkish using AI-powered OCR, translation, and image processing technologies.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![Next.js](https://img.shields.io/badge/next.js-14-black)
![FastAPI](https://img.shields.io/badge/fastapi-0.109-009688)

## 🎯 Features

- **🔍 Text Detection**: Advanced OCR using EasyOCR to detect text regions in manga pages
- **🌐 Smart Translation**: English to Turkish translation using Google Translate API
- **🎨 AI Inpainting**: Remove original text using LaMa (Large Mask Inpainting) model
- **✏️ Text Rendering**: Automatically render translated text with optimal font sizing
- **📊 Before/After Comparison**: Visual comparison of original and translated pages
- **⚡ Fast Processing**: Complete translation pipeline in 10-30 seconds
- **🐳 Docker Ready**: Easy deployment with Docker Compose

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

### Using Docker (Recommended)

1. **Clone the repository**
```bash
cd /Users/hayperlez/Desktop/mangama
```

2. **Configure environment**
```bash
cp backend/.env.example backend/.env
```

3. **Build and run**
```bash
docker-compose up --build
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

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
mangama/
├── backend/                    # Python FastAPI Backend
│   ├── app/
│   │   ├── main.py            # Application entry point
│   │   ├── config.py          # Configuration settings
│   │   ├── routers/           # API endpoints
│   │   ├── services/          # Business logic
│   │   │   ├── ocr_service.py
│   │   │   ├── translation_service.py
│   │   │   ├── inpainting_service.py
│   │   │   ├── text_renderer.py
│   │   │   └── pipeline.py
│   │   ├── models/            # Pydantic schemas
│   │   └── utils/             # Helper functions
│   ├── temp/                  # Temporary files
│   ├── models/                # AI model weights
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/                   # Next.js Frontend
│   ├── src/
│   │   ├── app/               # App Router pages
│   │   ├── components/        # React components
│   │   │   ├── ImageUploader.tsx
│   │   │   ├── BeforeAfterViewer.tsx
│   │   │   └── ProcessingStatus.tsx
│   │   └── lib/               # API client
│   ├── public/
│   ├── package.json
│   └── Dockerfile
│
└── docker-compose.yml
```

## 🔄 Processing Pipeline

```
1. Upload Image → 2. OCR Detection → 3. Translation → 4. Inpainting → 5. Text Rendering
      📤              🔍                 🌐              🎨               ✏️
```

### Detailed Workflow:

1. **Image Upload**: User uploads manga page (JPG/PNG)
2. **Text Detection**: EasyOCR detects text regions and extracts English text
3. **Translation**: Google Translate converts English to Turkish
4. **Inpainting**: LaMa model removes original text while preserving background
5. **Text Rendering**: Pillow renders Turkish text with optimal font size
6. **Result**: User gets translated manga page with before/after comparison

## 🎨 API Endpoints

### POST `/api/translate`
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
      "bbox": {"x": 100, "y": 200, "width": 80, "height": 30, "confidence": 0.95}
    }
  ],
  "processing_time": 12.5,
  "total_text_regions": 1
}
```

### GET `/health`
Health check endpoint

### DELETE `/api/cleanup/{file_id}`
Clean up temporary files

## ⚙️ Configuration

### Backend Environment Variables

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

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

### Backend Development

```bash
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

### OCR not working
- Ensure EasyOCR models are downloaded (automatic on first run)
- Check available disk space for model downloads
- Verify language codes in configuration

### Inpainting errors
- LaMa model requires significant memory (2GB+)
- Falls back to OpenCV inpainting if LaMa fails
- Check logs for specific error messages

### Translation failures
- Verify internet connection for Google Translate API
- Check rate limits (use DeepL API for production)

## 🚀 Performance Optimization

- **GPU Acceleration**: Set `OCR_GPU=True` if CUDA GPU available
- **Image Preprocessing**: Images are automatically resized to max 2048px
- **Caching**: Font objects are cached for better performance
- **Async Processing**: FastAPI handles requests asynchronously

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
