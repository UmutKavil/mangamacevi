'use client';

import { useState } from 'react';
import { TranslationResponse, getImageUrl } from '@/lib/api';
import { FiRotateCw, FiDownload } from 'react-icons/fi';

interface BeforeAfterViewerProps {
  result: TranslationResponse;
  onReset: () => void;
}

export default function BeforeAfterViewer({ result, onReset }: BeforeAfterViewerProps) {
  const [showBefore, setShowBefore] = useState(true);

  const originalUrl = getImageUrl(result.original_image_url);
  const translatedUrl = getImageUrl(result.translated_image_url);

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = translatedUrl;
    link.download = 'mangama-translated.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
            <img
              src={showBefore ? originalUrl : translatedUrl}
              alt={showBefore ? 'Original' : 'Translated'}
              className="w-full h-auto rounded-lg shadow-md"
            />
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
