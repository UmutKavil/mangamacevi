'use client';

import { useEffect, useState } from 'react';

const stages = [
  { id: 1, name: 'Görsel Yükleniyor', icon: '📤', duration: 1000 },
  { id: 2, name: 'Metin Tespit Ediliyor (OCR)', icon: '🔍', duration: 3000 },
  { id: 3, name: 'Metin Çevriliyor', icon: '🌐', duration: 2000 },
  { id: 4, name: 'Orijinal Metin Temizleniyor', icon: '🎨', duration: 4000 },
  { id: 5, name: 'Türkçe Metin Ekleniyor', icon: '✏️', duration: 2000 },
];

export default function ProcessingStatus() {
  const [currentStage, setCurrentStage] = useState(0);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    let timer: NodeJS.Timeout;
    
    if (currentStage < stages.length) {
      const duration = stages[currentStage].duration;
      const increment = 100 / (duration / 100);
      
      timer = setInterval(() => {
        setProgress((prev) => {
          if (prev >= 100) {
            setCurrentStage((s) => s + 1);
            return 0;
          }
          return prev + increment;
        });
      }, 100);
    }

    return () => clearInterval(timer);
  }, [currentStage]);

  return (
    <div className="bg-white rounded-lg shadow-lg border p-8">
      <div className="text-center mb-8">
        <div className="inline-block animate-pulse-slow">
          <div className="text-6xl mb-4">
            {currentStage < stages.length ? stages[currentStage].icon : '✅'}
          </div>
        </div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">
          {currentStage < stages.length
            ? stages[currentStage].name
            : 'İşlem Tamamlandı!'}
        </h2>
        <p className="text-gray-600">
          {currentStage < stages.length
            ? `Adım ${currentStage + 1} / ${stages.length}`
            : 'Sonuçlarınız hazırlanıyor...'}
        </p>
      </div>

      {/* Progress Bar */}
      <div className="mb-8">
        <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-blue-500 to-purple-500 h-full transition-all duration-300 ease-out"
            style={{
              width: `${
                ((currentStage * 100 + progress) / stages.length).toFixed(0)
              }%`,
            }}
          />
        </div>
        <p className="text-center text-sm text-gray-500 mt-2">
          {((currentStage * 100 + progress) / stages.length).toFixed(0)}%
        </p>
      </div>

      {/* Stage List */}
      <div className="space-y-3">
        {stages.map((stage, index) => (
          <div
            key={stage.id}
            className={`flex items-center gap-3 p-3 rounded-lg transition-colors ${
              index < currentStage
                ? 'bg-green-50 border border-green-200'
                : index === currentStage
                ? 'bg-blue-50 border border-blue-200'
                : 'bg-gray-50 border border-gray-200'
            }`}
          >
            <span className="text-2xl">{stage.icon}</span>
            <span
              className={`flex-1 font-medium ${
                index < currentStage
                  ? 'text-green-700'
                  : index === currentStage
                  ? 'text-blue-700'
                  : 'text-gray-500'
              }`}
            >
              {stage.name}
            </span>
            {index < currentStage && (
              <span className="text-green-600">✓</span>
            )}
            {index === currentStage && (
              <span className="text-blue-600 animate-spin">⟳</span>
            )}
          </div>
        ))}
      </div>

      <div className="mt-6 text-center text-sm text-gray-500">
        <p>⏱️ Bu işlem 10-30 saniye arasında sürebilir</p>
      </div>
    </div>
  );
}
