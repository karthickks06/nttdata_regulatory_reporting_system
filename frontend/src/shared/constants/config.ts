/**
 * Application configuration constants
 */

export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1';
export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://localhost:8000/ws';
export const APP_NAME = import.meta.env.VITE_APP_NAME || 'NTT Data Regulatory Reporting System';
export const APP_VERSION = import.meta.env.VITE_APP_VERSION || '1.0.0';

export const CONFIG = {
  API_TIMEOUT: 30000, // 30 seconds
  DEBOUNCE_DELAY: 300, // milliseconds
  PAGINATION_PAGE_SIZE: 20,
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_FILE_TYPES: [
    'application/pdf',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'text/csv',
  ],
} as const;
