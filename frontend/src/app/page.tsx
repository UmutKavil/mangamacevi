'use client';

import { useState, useEffect } from 'react';
import ImageUploader from '@/components/ImageUploader';
import BeforeAfterViewer from '@/components/BeforeAfterViewer';
import ProcessingStatus from '@/components/ProcessingStatus';
import { translateMangaPage, TranslationResponse, checkHealth } from '@/lib/api';

interface BatchResult {
  file: File;
  result: TranslationResponse | null;
  error: string | null;
  status: 'pending' | 'processing' | 'completed' | 'failed';
}

export default function Home() {
  const [isProcessing, setIsProcessing] = useState(false);
  const [batchResults, setBatchResults] = useState<BatchResult[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [apiStatus, setApiStatus] = useState<'checking' | 'online' | 'offline'>('checking');

  // Check backend health on mount
  useEffect(() => {
    const checkBackend = async () => {
      const isHealthy = await checkHealth();
      setApiStatus(isHealthy ? 'online' : 'offline');
    };
    
    checkBackend();
    
    // Check every 30 seconds
    const interval = setInterval(checkBackend, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleImageUpload = async (files: File[]) => {
    // Check if API is online
    if (apiStatus === 'offline') {
      setError('API çevrimdışı. Lütfen backend servisinin çalıştığından emin olun.');
      return;
    }

    setIsProcessing(true);
    setError(null);
    setCurrentIndex(0);

    // Initialize batch results
    const initialResults: BatchResult[] = files.map(file => ({
      file,
      result: null,
      error: null,
      status: 'pending'
    }));
    setBatchResults(initialResults);

    // Process files sequentially
    for (let i = 0; i < files.length; i++) {
      setCurrentIndex(i);
      
      // Update status to processing
      setBatchResults(prev => 
        prev.map((r, idx) => idx === i ? { ...r, status: 'processing' } : r)
      );

      try {
        const response = await translateMangaPage(files[i]);
        
        // Update with result
        setBatchResults(prev =>
          prev.map((r, idx) => idx === i ? { 
            ...r, 
            result: response, 
            status: 'completed' 
          } : r)
        );
      } catch (err) {
        // Update with error
        setBatchResults(prev =>
          prev.map((r, idx) => idx === i ? { 
            ...r, 
            error: err instanceof Error ? err.message : 'Bir hata oluştu',
            status: 'failed'
          } : r)
        );
      }
    }

    setIsProcessing(false);
  };

  const handleReset = () => {
    setBatchResults([]);
    setError(null);
    setCurrentIndex(0);
  };

  const completedResults = batchResults.filter(r => r.status === 'completed');
  const hasResults = completedResults.length > 0;

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
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                apiStatus === 'online' 
                  ? 'bg-green-100 text-green-700' 
                  : apiStatus === 'offline'
                  ? 'bg-red-100 text-red-700'
                  : 'bg-yellow-100 text-yellow-700'
              }`}>
                {apiStatus === 'online' && '✓ API Hazır'}
                {apiStatus === 'offline' && '✗ API Çevrimdışı'}
                {apiStatus === 'checking' && '⟳ Kontrol Ediliyor...'}
              </span>
            </div>
          </div>
        </div>
      </hehasResults && !isProcessing && (
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-8">
              <h2 className="text-2xl font-semibold text-gray-800 mb-3">
                Manga Sayfalarınızı Yükleyin
              </h2>
              <p className="text-gray-600">
                Birden fazla manga sayfası seçebilirsiniz - tümü sırayla çevrilecek
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
            <div className="bg-white rounded-lg shadow-lg border p-8 mb-6">
              <div className="text-center">
                <h2 className="text-2xl font-bold text-gray-800 mb-4">
                  Toplu Çeviri İşleniyor
                </h2>
                <div className="mb-6">
                  <p className="text-lg text-gray-700 mb-2">
                    Sayfa {currentIndex + 1} / {batchResults.length}
                  </p>
                  <div className="w-full bg-gray-200 rounded-full h-4">
                    <div
                      className="bg-gradient-to-r from-blue-500 to-purple-500 h-4 rounded-full transition-all duration-500"
                      style={{ width: `${((currentIndex + 1) / batchResults.length) * 100}%` }}
                    />
                  </div>
                </div>
                <div className="space-y-2">
                  {batchResults.map((result, index) => (
                    <div
                      key={index}
                      className={`flex items-center gap-3 p-3 rounded-lg ${
                        result.status === 'completed'
                          ? 'bg-green-50 border border-green-200'
                          : result.status === 'processing'
                          ? 'bg-blue-50 border border-blue-200'
                          : result.status === 'failed'
                          ? 'bg-red-50 border border-red-200'
                          : 'bg-gray-50 border border-gray-200'
                      }`}
                    >
                      <span className="text-sm font-medium text-gray-700">
                        {index + 1}.
                      </span>
                      <span className="flex-1 text-sm text-gray-700 truncate">
                        {result.file.name}
                      </span>
                      {result.status === 'completed' && <span className="text-green-600">✓</span>}
                      {result.status === 'processing' && <span className="text-blue-600 animate-spin">⟳</span>}
                      {result.status === 'failed' && <span className="text-red-600">✗</span>}
                      {result.status === 'pending' && <span className="text-gray-400">⋯</span>}
                    </div>
                  ))}
                </div>
              </div>
            </div>
            <ProcessingStatus />
          </div>
        )}

        {hasResults && !isProcessing && (
          <div>
            <div className="mb-6 text-center">
              <button
                onClick={handleReset}
                className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                ← Yeni Çeviri
              </button>
            </div>
            <div className="space-y-12">
              {completedResults.map((item, index) => (
                <div key={index}>
                  <h3 className="text-xl font-semibold text-gray-800 mb-4 text-center">
                    Sayfa {batchResults.findIndex(r => r === item) + 1}: {item.file.name}
                  </h3>
                  {item.result && <BeforeAfterViewer result={item.result} onReset={handleReset} />}
                </div>
              ))}
            </div>
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
