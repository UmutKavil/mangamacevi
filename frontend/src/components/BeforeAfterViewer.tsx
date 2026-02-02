'use client';

import { useState, useEffect } from 'react';
import { TranslationResponse, getImageUrl } from '@/lib/api';
import { FiRotateCw, FiDownload } from 'react-icons/fi';

interface BeforeAfterViewerProps {
  result: TranslationResponse;
  onReset: () => void;
}

export default function BeforeAfterViewer({ result, onReset }: BeforeAfterViewerProps) {
  const [showBefore, setShowBefore] = useState(true);
  const [imageError, setImageError] = useState<string | null>(null);
  const [imagesLoaded, setImagesLoaded] = useState(false);

  const originalUrl = getImageUrl(result.original_image_url);
  const translatedUrl = getImageUrl(result.translated_image_url);

  // Preload both images when component mounts
  useEffect(() => {
    let mounted = true;
    const loadImages = async () => {
      try {
        const promises = [originalUrl, translatedUrl].map(url => {
          return new Promise((resolve, reject) => {
            const img = new Image();
            img.onload = () => resolve(url);
            img.onerror = () => reject(new Error(`Failed to load ${url}`));
            img.src = url;
          });
        });
        
        await Promise.all(promises);
        if (mounted) {
          setImagesLoaded(true);
          setImageError(null);
        }
      } catch (error) {
        if (mounted) {
          setImageError('Görsel yüklenemedi. Lütfen tekrar deneyin.');
          setImagesLoaded(true);
        }
      }
    };
    
    loadImages();
    
    return () => {
      mounted = false;
    };
  }, [originalUrl, translatedUrl]);

  const handleImageError = () => {
    setImageError('Görsel yüklenemedi. Lütfen tekrar deneyin.');
  };

  const handleDownload = async () => {
    try {
      // Fetch the image as blob to bypass CORS restrictions
      const response = await fetch(translatedUrl);
      const blob = await response.blob();
      
      // Create object URL from blob
      const blobUrl = window.URL.createObjectURL(blob);
      
      // Create download link
      const link = document.createElement('a');
      link.href = blobUrl;
      link.download = `mangama-translated-${Date.now()}.png`;
      document.body.appendChild(link);
      link.click();
      
      // Cleanup
      document.body.removeChild(link);
      window.URL.revokeObjectURL(blobUrl);
    } catch (error) {
      console.error('Download failed:', error);
      // Fallback: open in new tab if download fails
      window.open(translatedUrl, '_blank');
    }
  };

  return (
    <div className="max-w-6xl mx-auto">
      {/* Stats Bar */}
      <div className="bg-white rounded-lg shadow-sm border p-4 mb-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="flex items-center gap-6">
            <div>
              <span className="text-2xl font-bold text-blue-600">
                {result.total_text_regions}
              </span>
              <p className="text-xs text-gray-600 mt-1">Metin Bölgesi</p>
            </div>
            <div>
              <span className="text-2xl font-bold text-green-600">
                {result.processing_time}s
              </span>
              <p className="text-xs text-gray-600 mt-1">İşlem Süresi</p>
            </div>
          </div>
          <div className="flex gap-2">
            <button
              onClick={handleDownload}
              className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
            >
              <FiDownload />
              İndir
            </button>
            <button
              onClick={onReset}
              className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
            >
              <FiRotateCw />
              Yeni Çeviri
            </button>
          </div>
        </div>
      </div>

      {/* Image Comparison */}
      <div className="bg-white rounded-lg shadow-lg border overflow-hidden">
        <div className="flex border-b">
          <button
            onClick={() => setShowBefore(true)}
            className={`flex-1 py-3 px-6 font-medium transition-colors ${
              showBefore
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Önce (Orijinal)
          </button>
          <button
            onClick={() => setShowBefore(false)}
            className={`flex-1 py-3 px-6 font-medium transition-colors ${
              !showBefore
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            Sonra (Çevrilmiş)
          </button>
        </div>

        <div className="p-6 bg-gray-50">
          <div className="relative mx-auto max-w-4xl">
            {!imagesLoaded && !imageError && (
              <div className="flex flex-col items-center justify-center py-20">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                <p className="text-gray-600 text-sm">Görseller yükleniyor...</p>
              </div>
            )}
            {imageError && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-6 text-center">
                <span className="text-red-600 text-lg">⚠️</span>
                <p className="text-red-800 mt-2">{imageError}</p>
                <button
                  onClick={() => {
                    setImageError(null);
                    setImagesLoaded(false);
                  }}
                  className="mt-4 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
                >
                  Tekrar Yükle
                </button>
              </div>
            )}
            {imagesLoaded && !imageError && (
              <img
                src={showBefore ? originalUrl : translatedUrl}
                alt={showBefore ? 'Original' : 'Translated'}
                className="w-full h-auto rounded-lg shadow-md"
                onError={handleImageError}
              />
            )}
          </div>
        </div>
      </div>

      {/* Detected Texts */}
      <div className="bg-white rounded-lg shadow-sm border p-6 mt-6">
        <h3 className="text-lg font-semibold text-gray-800 mb-4">
          🔤 Tespit Edilen ve Çevrilen Metinler
        </h3>
        <div className="space-y-3 max-h-96 overflow-y-auto">
          {result.detected_texts.map((text, index) => (
            <div
              key={index}
              className="flex items-start gap-4 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
            >
              <span className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                {index + 1}
              </span>
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-sm text-gray-600">EN:</span>
                  <span className="text-sm font-medium text-gray-800">
                    {text.text}
                  </span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-sm text-gray-600">TR:</span>
                  <span className="text-sm font-medium text-blue-700">
                    {text.translated_text}
                  </span>
                </div>
                <div className="flex items-center gap-2 mt-1">
                  <span className="text-xs text-gray-400">
                    Güven: {(text.bbox.confidence * 100).toFixed(0)}%
                  </span>
                  <span className="text-xs text-gray-300">•</span>
                  <span className="text-xs text-gray-400">
                    Konum: ({text.bbox.x}, {text.bbox.y})
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
