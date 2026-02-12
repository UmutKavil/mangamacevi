import axios from 'axios';
import { logger } from './logger';

// Use Next.js API routes as proxy to backend
const API_BASE_URL = '/api';
// Backend URL for static files
const BACKEND_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

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
export async function translateMangaPage(
  file: File, 
  useGPU: boolean = false,
  retries: number = 2
): Promise<TranslationResponse> {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('use_gpu', useGPU.toString());

  let lastError: Error | null = null;

  for (let attempt = 0; attempt <= retries; attempt++) {
    try {
      logger.debug(`Translation attempt ${attempt + 1}/${retries + 1}`);
      
      const response = await api.post<TranslationResponse>('/translate', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 120000, // 2 minutes timeout for processing
      });

      logger.success('Translation completed', {
        original: response.data.original_image_url,
        translated: response.data.translated_image_url,
        regions: response.data.total_text_regions,
        time: response.data.processing_time
      });
      
      // Validate response has required fields
      if (!response.data.translated_image_url || !response.data.original_image_url) {
        throw new Error('Sunucu geçersiz yanıt döndürdü');
      }
      
      return response.data;
    } catch (error) {
      lastError = error as Error;
      logger.error(`Translation failed (attempt ${attempt + 1})`, error);
      
      if (axios.isAxiosError(error)) {
        const apiError = error.response?.data as ApiError;
        
        // Don't retry on client errors (4xx)
        if (error.response && error.response.status >= 400 && error.response.status < 500) {
          logger.warn('Client error', { status: error.response.status, detail: apiError?.detail });
          throw new Error(apiError?.detail || 'Geçersiz istek. Lütfen görselinizi kontrol edin.');
        }
        
        // Network or timeout errors - retry
        if (error.code === 'ECONNABORTED' || error.code === 'ERR_NETWORK') {
          if (attempt < retries) {
            logger.info(`Retrying in ${(attempt + 1) * 2} seconds...`);
            await new Promise(resolve => setTimeout(resolve, (attempt + 1) * 2000));
            continue;
          }
          throw new Error('Bağlantı hatası. Lütfen internet bağlantınızı kontrol edin.');
        }
        
        // Server errors (5xx) - retry
        if (error.response && error.response.status >= 500) {
          if (attempt < retries) {
            logger.info(`Retrying in ${(attempt + 1) * 2} seconds...`);
            await new Promise(resolve => setTimeout(resolve, (attempt + 1) * 2000));
            continue;
          }
          throw new Error('Sunucu hatası. Lütfen daha sonra tekrar deneyin.');
        }
        
        throw new Error(apiError?.detail || 'Çeviri başarısız oldu');
      }
      
      // Unknown error - retry
      if (attempt < retries) {
        logger.info(`Retrying in ${(attempt + 1) * 2} seconds...`);
        await new Promise(resolve => setTimeout(resolve, (attempt + 1) * 2000));
        continue;
      }
    }
  }
  
  throw lastError || new Error('Çeviri başarısız oldu');
}

/**
 * Check backend health
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await api.get('/health', { timeout: 5000 });
    logger.debug('Health check passed');
    return response.status === 200;
  } catch (error) {
    logger.warn('Health check failed', error);
    return false;
  }
}

/**
 * Clean up temporary files
 */
export async function cleanupFiles(fileId: string): Promise<void> {
  try {
    await api.delete(`/cleanup/${fileId}`);
    logger.info('Cleanup completed', { fileId });
  } catch (error) {
    logger.error('Cleanup failed', error);
  }
}

/**
 * Get full image URL
 */
export function getImageUrl(relativeUrl: string): string {
  if (relativeUrl.startsWith('http')) {
    return relativeUrl;
  }
  const fullUrl = `${BACKEND_URL}${relativeUrl}`;
  logger.debug('Image URL', { relative: relativeUrl, full: fullUrl });
  return fullUrl;
}

export default api;
