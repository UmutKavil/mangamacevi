'use client';

import { useState } from 'react';
import ImageUploader from '@/components/ImageUploader';
import BeforeAfterViewer from '@/components/BeforeAfterViewer';
import ProcessingStatus from '@/components/ProcessingStatus';
import { translateMangaPage, TranslationResponse } from '@/lib/api';

export default function Home() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<TranslationResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleImageUpload = async (file: File) => {
    setIsProcessing(true);
    setError(null);
    setResult(null);

    try {
      const response = await translateMangaPage(file);
      setResult(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Bir hata oluştu');
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                📚 MangaMa
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Manga Çeviri Otomasyonu - İngilizce → Türkçe
              </p>
            </div>
            <div className="text-right">
              <span className="inline-block px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-medium">
                ✓ API Hazır
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-12">
        {!result && !isProcessing && (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-3">
                Manga Sayfanızı Yükleyin
              </h2>
              <p className="text-gray-600">
                İngilizce manga sayfanızı yükleyin, otomatik olarak Türkçe'ye çevirelim
              </p>
            </div>
            <ImageUploader onUpload={handleImageUpload} />
            
            {/* Info Section */}
            <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="text-3xl mb-3">🔍</div>
                <h3 className="font-semibold text-gray-800 mb-2">OCR Teknolojisi</h3>
                <p className="text-sm text-gray-600">
                  EasyOCR ile yüksek doğrulukta metin tanıma
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="text-3xl mb-3">🌐</div>
                <h3 className="font-semibold text-gray-800 mb-2">Akıllı Çeviri</h3>
                <p className="text-sm text-gray-600">
                  Google Translate ile doğal çeviri
                </p>
              </div>
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                <div className="text-3xl mb-3">🎨</div>
                <h3 className="font-semibold text-gray-800 mb-2">AI Inpainting</h3>
                <p className="text-sm text-gray-600">
                  LaMa model ile profesyonel temizleme
                </p>
              </div>
            </div>
          </div>
        )}

        {isProcessing && (
          <div className="max-w-2xl mx-auto">
            <ProcessingStatus />
          </div>
        )}

        {result && !isProcessing && (
          <div>
            <BeforeAfterViewer result={result} onReset={handleReset} />
          </div>
        )}

        {error && (
          <div className="max-w-2xl mx-auto mt-6">
            <div className="bg-red-50 border border-red-200 rounded-lg p-4">
              <div className="flex items-center">
                <span className="text-red-600 mr-2">❌</span>
                <span className="text-red-800">{error}</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="bg-white border-t mt-auto">
        <div className="container mx-auto px-4 py-6 text-center text-sm text-gray-600">
          <p>MangaMa v1.0 - 2026 🇹🇷</p>
        </div>
      </footer>
    </main>
  );
}
