/**
 * Common type definitions used across the application
 */

export interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  department?: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  last_login?: string;
}

export interface Role {
  id: number;
  name: string;
  display_name: string;
  description?: string;
  created_at: string;
}

export interface Permission {
  id: number;
  name: string;
  resource: string;
  action: string;
  description?: string;
  created_at: string;
}

export interface PaginationParams {
  page?: number;
  limit?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  pages: number;
}

export interface ApiError {
  detail: string;
  status_code?: number;
}

export type LoadingState = 'idle' | 'loading' | 'succeeded' | 'failed';

export interface AsyncState<T> {
  data: T | null;
  loading: LoadingState;
  error: string | null;
}
