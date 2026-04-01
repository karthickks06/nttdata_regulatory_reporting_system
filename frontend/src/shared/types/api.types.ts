/**
 * API-related type definitions
 */

export interface ApiResponse<T = any> {
  data?: T;
  message?: string;
  status: number;
}

export interface ApiErrorResponse {
  detail: string;
  status_code: number;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
  full_name?: string;
  department?: string;
}
