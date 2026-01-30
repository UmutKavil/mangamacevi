import axios from 'axios';

// Configure base URL for API
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export interface DetectedText {
  text: string;
  bbox: {
    x: number;
    y: number;
    width: number;
    height: number;
    confidence: number;
  };
  language: string;
  translated_text?: string;
}

export interface TranslationResponse {
  original_image_url: string;
  translated_image_url: string;
  detected_texts: DetectedText[];
  processing_time: number;
  timestamp: string;
  total_text_regions: number;
}

export interface ApiError {
  detail: string;
}

/**
 * Upload and translate a manga page
 */
export async function translateMangaPage(file: File): Promise<TranslationResponse> {
  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await api.post<TranslationResponse>('/api/translate', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
      timeout: 120000, // 2 minutes timeout for processing
    });

    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      const apiError = error.response?.data as ApiError;
      throw new Error(apiError?.detail || 'Translation failed');
    }
    throw error;
  }
}

/**
 * Clean up temporary files
 */
export async function cleanupFiles(fileId: string): Promise<void> {
  try {
    await api.delete(`/api/cleanup/${fileId}`);
  } catch (error) {
    console.error('Cleanup failed:', error);
  }
}

/**
 * Get full image URL
 */
export function getImageUrl(relativeUrl: string): string {
  if (relativeUrl.startsWith('http')) {
    return relativeUrl;
  }
  return `${API_BASE_URL}${relativeUrl}`;
}

export default api;
